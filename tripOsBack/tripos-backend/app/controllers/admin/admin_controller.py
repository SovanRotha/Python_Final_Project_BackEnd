from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.admin.audit_log import AdminAuditLog
from app.models.admin.report import Report
from app.models.destination.destination import Destination
from app.models.place.place import Place
from app.models.trip.trip import Trip
from app.core.config import settings
from app.models.user.user import User


class AdminController:
    def __init__(self, db: Session):
        self.db = db

    def _log(
        self,
        actor: User,
        action: str,
        resource_type: str,
        resource_id: int | None,
        details: dict | None = None,
    ) -> None:
        self.db.add(
            AdminAuditLog(
                actor_id=actor.id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details or {},
            )
        )

    def count_users(self) -> int:
        return self.db.query(User).count()

    def dashboard(self) -> dict:
        statistics = {
            "users": self.db.query(User).count(),
            "active_users": self.db.query(User).filter(User.status.is_(True)).count(),
            "destinations": self.db.query(Destination).count(),
            "places": self.db.query(Place).count(),
            "trips": self.db.query(Trip).count(),
            "open_reports": self.db.query(Report)
            .filter(Report.status == "open")
            .count(),
        }
        recent_activity = []
        for model, event_type in (
            (User, "user_registered"),
            (Destination, "destination_created"),
            (Place, "place_created"),
            (Trip, "trip_created"),
            (Report, "report_submitted"),
        ):
            recent_activity.extend(
                {
                    "type": event_type,
                    "resource_id": resource_id,
                    "created_at": created_at,
                }
                for resource_id, created_at in self.db.query(
                    model.id, model.created_at
                )
                .order_by(model.created_at.desc(), model.id.desc())
                .limit(5)
                .all()
            )
        recent_activity.sort(
            key=lambda event: (
                event["created_at"].replace(tzinfo=timezone.utc).timestamp()
                if event["created_at"] is not None
                and event["created_at"].tzinfo is None
                else event["created_at"].timestamp()
                if event["created_at"] is not None
                else float("-inf")
            ),
            reverse=True,
        )
        return {"statistics": statistics, "recent_activity": recent_activity[:10]}

    def list_users(
        self,
        page: int,
        page_size: int,
        search: str | None,
        active: bool | None,
    ) -> dict:
        query = (
            self.db.query(User, func.count(Trip.id).label("trip_count"))
            .outerjoin(Trip, Trip.user_id == User.id)
            .group_by(User.id)
        )
        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                User.name.ilike(pattern) | User.email.ilike(pattern)
            )
        if active is not None:
            query = query.filter(User.status.is_(active))
        total = query.count()
        rows = (
            query.order_by(User.created_at.desc(), User.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return {
            "items": [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "status": user.status,
                    "created_at": user.created_at,
                    "trip_count": trip_count,
                }
                for user, trip_count in rows
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def get_user(self, user_id: int) -> dict:
        user = self.db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status,
            "created_at": user.created_at,
            "trip_count": self.db.query(Trip).filter(Trip.user_id == user.id).count(),
        }

    def set_user_status(self, actor: User, user_id: int, active: bool) -> dict:
        user = self.db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not active and user.email.casefold() in settings.admin_emails:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An allowlisted admin account cannot be suspended",
            )
        previous_status = user.status
        user.status = active
        self._log(
            actor,
            "user_status_updated",
            "user",
            user.id,
            {"previous_status": previous_status, "status": active},
        )
        self.db.commit()
        self.db.refresh(user)
        trip_count = (
            self.db.query(Trip).filter(Trip.user_id == user.id).count()
        )
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status,
            "created_at": user.created_at,
            "trip_count": trip_count,
        }

    def create_report(self, user: User, fields: dict) -> Report:
        report = Report(user_id=user.id, **fields)
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def list_reports(
        self, page: int, page_size: int, report_status: str | None
    ) -> dict:
        query = self.db.query(Report)
        if report_status:
            query = query.filter(Report.status == report_status)
        total = query.count()
        items = (
            query.order_by(Report.created_at.desc(), Report.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    def review_report(
        self, actor: User, report_id: int, report_status: str, resolution: str | None
    ) -> Report:
        report = self.db.get(Report, report_id)
        if report is None:
            raise HTTPException(status_code=404, detail="Report not found")
        report.status = report_status
        report.resolution = resolution
        report.reviewed_by_id = actor.id
        report.reviewed_at = datetime.now(timezone.utc)
        self._log(
            actor,
            "report_reviewed",
            "report",
            report.id,
            {"status": report_status},
        )
        self.db.commit()
        self.db.refresh(report)
        return report

    def list_audit_logs(self, page: int, page_size: int) -> dict:
        query = self.db.query(AdminAuditLog)
        total = query.count()
        items = (
            query.order_by(AdminAuditLog.created_at.desc(), AdminAuditLog.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return {"items": items, "total": total, "page": page, "page_size": page_size}
