from datetime import date, datetime, time, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import case, func
from sqlalchemy.orm import Session, joinedload

from app.models.ai.ai import AIUsageEvent
from app.models.admin.audit_log import AdminAuditLog
from app.models.admin.report import Report
from app.models.destination.destination import Destination
from app.models.place.place import Place, PlaceStatus
from app.models.trip.trip import Trip, TripStatus
from app.core.config import settings
from app.models.user.user import User
from app.schemas.admin.admin import ReportStatus


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

    def dashboard(
        self, start_date: date | None = None, end_date: date | None = None
    ) -> dict:
        period_end = end_date or datetime.now(timezone.utc).date()
        period_start = start_date or period_end - timedelta(days=29)
        if period_start > period_end:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="start_date must be on or before end_date",
            )
        period_start_at = datetime.combine(
            period_start, time.min, tzinfo=timezone.utc
        )
        period_end_at = datetime.combine(
            period_end + timedelta(days=1), time.min, tzinfo=timezone.utc
        )
        statistics = {
            "users": self.db.query(User).count(),
            "active_users": self.db.query(User).filter(User.status.is_(True)).count(),
            "suspended_users": self.db.query(User)
            .filter(User.status.is_(False))
            .count(),
            "destinations": self.db.query(Destination).count(),
            "published_destinations": self.db.query(Destination)
            .filter(Destination.status == "published")
            .count(),
            "places": self.db.query(Place).count(),
            "trips": self.db.query(Trip).count(),
            "new_users": self.db.query(User)
            .filter(
                User.created_at >= period_start_at,
                User.created_at < period_end_at,
            )
            .count(),
            "new_trips": self.db.query(Trip)
            .filter(
                Trip.created_at >= period_start_at,
                Trip.created_at < period_end_at,
            )
            .count(),
            "reports": self.db.query(Report).count(),
            "open_reports": self.db.query(Report)
            .filter(Report.status == "open")
            .count(),
            "resolved_reports": self.db.query(Report)
            .filter(Report.status == ReportStatus.RESOLVED.value)
            .count(),
            "ai_usage": self.db.query(AIUsageEvent).count(),
        }
        reports_by_status = dict(
            self.db.query(Report.status, func.count(Report.id))
            .filter(
                Report.created_at >= period_start_at,
                Report.created_at < period_end_at,
            )
            .group_by(Report.status)
            .all()
        )
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
        recent_activity.extend(
            {
                "type": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "created_at": log.created_at,
            }
            for log in self.db.query(AdminAuditLog)
            .order_by(AdminAuditLog.created_at.desc(), AdminAuditLog.id.desc())
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
        return {
            "period": {"start_date": period_start, "end_date": period_end},
            "statistics": statistics,
            "reports_by_status": reports_by_status,
            "recent_activity": recent_activity[:10],
        }

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
                    "is_admin": user.email.casefold() in settings.admin_emails,
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
            "is_admin": user.email.casefold() in settings.admin_emails,
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
            "is_admin": user.email.casefold() in settings.admin_emails,
            "created_at": user.created_at,
            "trip_count": trip_count,
        }

    def list_destinations(
        self,
        page: int,
        page_size: int,
        destination_status: str | None,
        search: str | None,
    ) -> dict:
        query = self.db.query(Destination)
        if destination_status:
            query = query.filter(Destination.status == destination_status)
        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                Destination.name.ilike(pattern) | Destination.country.ilike(pattern)
            )
        total = query.count()
        items = (
            query.order_by(Destination.created_at.desc(), Destination.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    def create_destination(self, actor: User, fields: dict) -> Destination:
        destination = Destination(user_id=actor.id, **fields)
        self.db.add(destination)
        self.db.flush()
        self._log(
            actor,
            "destination_created",
            "destination",
            destination.id,
            {"status": destination.status},
        )
        self.db.commit()
        self.db.refresh(destination)
        return destination

    def get_destination(self, destination_id: int) -> Destination:
        destination = self.db.get(Destination, destination_id)
        if destination is None:
            raise HTTPException(status_code=404, detail="Destination not found")
        return destination

    def update_destination(
        self, actor: User, destination_id: int, fields: dict
    ) -> Destination:
        destination = self.get_destination(destination_id)
        required = {"name", "country", "country_code"}
        if any(name in fields and fields[name] is None for name in required):
            raise HTTPException(
                status_code=422,
                detail="Destination name, country, and country_code cannot be null",
            )
        for name, value in fields.items():
            setattr(destination, name, value)
        self._log(actor, "destination_updated", "destination", destination.id)
        self.db.commit()
        self.db.refresh(destination)
        return destination

    def set_destination_status(
        self, actor: User, destination_id: int, destination_status: str
    ) -> Destination:
        destination = self.get_destination(destination_id)
        previous_status = destination.status
        destination.status = destination_status
        self._log(
            actor,
            "destination_status_updated",
            "destination",
            destination.id,
            {"previous_status": previous_status, "status": destination_status},
        )
        self.db.commit()
        self.db.refresh(destination)
        return destination

    def list_places(
        self,
        page: int,
        page_size: int,
        destination_id: int | None,
        place_status: PlaceStatus | None,
        search: str | None,
    ) -> dict:
        query = self.db.query(Place)
        if destination_id is not None:
            query = query.filter(Place.destination_id == destination_id)
        if place_status:
            query = query.filter(Place.status == place_status)
        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                Place.name.ilike(pattern) | Place.category.ilike(pattern)
            )
        total = query.count()
        items = (
            query.order_by(Place.created_at.desc(), Place.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    def list_trips(
        self,
        page: int,
        page_size: int,
        user_id: int | None,
        trip_status: TripStatus | None,
        search: str | None,
    ) -> dict:
        query = self.db.query(Trip).join(User, Trip.user_id == User.id)
        if user_id is not None:
            query = query.filter(Trip.user_id == user_id)
        if trip_status is not None:
            query = query.filter(Trip.status == trip_status)
        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                Trip.name.ilike(pattern)
                | User.name.ilike(pattern)
                | User.email.ilike(pattern)
            )
        total = query.count()
        items = (
            query.options(joinedload(Trip.user))
            .order_by(Trip.created_at.desc(), Trip.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return {"items": items, "total": total, "page": page, "page_size": page_size}

    def get_trip(self, trip_id: int) -> Trip:
        trip = (
            self.db.query(Trip)
            .options(joinedload(Trip.user))
            .filter(Trip.id == trip_id)
            .first()
        )
        if trip is None:
            raise HTTPException(status_code=404, detail="Trip not found")
        return trip

    def get_place(self, place_id: int) -> Place:
        place = self.db.get(Place, place_id)
        if place is None:
            raise HTTPException(status_code=404, detail="Place not found")
        return place

    def create_place(self, actor: User, fields: dict) -> Place:
        if self.db.get(Destination, fields["destination_id"]) is None:
            raise HTTPException(status_code=404, detail="Destination not found")
        place = Place(**fields)
        self.db.add(place)
        self.db.flush()
        self._log(actor, "place_created", "place", place.id)
        self.db.commit()
        self.db.refresh(place)
        return place

    def update_place(self, actor: User, place_id: int, fields: dict) -> Place:
        place = self.get_place(place_id)
        if any(
            name in fields and fields[name] is None for name in {"name", "category"}
        ):
            raise HTTPException(
                status_code=422,
                detail="Place name and category cannot be null",
            )
        destination_id = fields.get("destination_id")
        if destination_id is not None and self.db.get(
            Destination, destination_id
        ) is None:
            raise HTTPException(status_code=404, detail="Destination not found")
        for name, value in fields.items():
            setattr(place, name, value)
        self._log(actor, "place_updated", "place", place.id)
        self.db.commit()
        self.db.refresh(place)
        return place

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
        try:
            validated_status = ReportStatus(report_status)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid report status",
            ) from exc
        report = self.db.get(Report, report_id)
        if report is None:
            raise HTTPException(status_code=404, detail="Report not found")
        report.status = validated_status.value
        report.resolution = resolution
        report.reviewed_by_id = actor.id
        report.reviewed_at = datetime.now(timezone.utc)
        self._log(
            actor,
            "report_reviewed",
            "report",
            report.id,
            {"status": validated_status.value},
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

    def ai_monitoring(self) -> dict:
        total, failures, average_latency, input_tokens, output_tokens = (
            self.db.query(
                func.count(AIUsageEvent.id),
                func.sum(case((AIUsageEvent.succeeded.is_(False), 1), else_=0)),
                func.avg(AIUsageEvent.duration_ms),
                func.coalesce(func.sum(AIUsageEvent.input_tokens), 0),
                func.coalesce(func.sum(AIUsageEvent.output_tokens), 0),
            ).one()
        )
        latest_event = (
            self.db.query(AIUsageEvent)
            .order_by(AIUsageEvent.created_at.desc(), AIUsageEvent.id.desc())
            .first()
        )
        last_success = (
            self.db.query(AIUsageEvent.created_at)
            .filter(AIUsageEvent.succeeded.is_(True))
            .order_by(AIUsageEvent.created_at.desc(), AIUsageEvent.id.desc())
            .first()
        )
        errors_by_type = (
            self.db.query(AIUsageEvent.error_type, func.count(AIUsageEvent.id))
            .filter(AIUsageEvent.succeeded.is_(False))
            .group_by(AIUsageEvent.error_type)
            .all()
        )
        failures = failures or 0
        return {
            "requests": total,
            "succeeded": total - failures,
            "failed": failures,
            "average_latency_ms": (
                float(average_latency) if average_latency is not None else None
            ),
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
            },
            "estimated_cost": None,
            "estimated_cost_available": False,
            "errors_by_type": [
                {"type": error_type or "unknown", "count": count}
                for error_type, count in errors_by_type
            ],
            "service_health": {
                "configured": bool(settings.OPENAI_API_KEY),
                "last_request_succeeded": (
                    latest_event.succeeded if latest_event is not None else None
                ),
                "last_success_at": last_success[0] if last_success else None,
            },
        }
