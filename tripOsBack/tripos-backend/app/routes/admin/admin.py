from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.controllers.admin.admin_controller import AdminController
from app.core.config import settings
from app.core.database import get_db
from app.models.user.user import User
from app.models.place.place import PlaceStatus
from app.schemas.admin.admin import (
    AdminDestinationCreate,
    AdminDestinationStatusUpdate,
    AdminDestinationUpdate,
    AdminAuditLogRead,
    AdminReportRead,
    AdminUserRead,
    AdminUserStatusUpdate,
    ReportCreate,
    ReportReview,
    ReportStatus,
)
from app.schemas.destination.destination import DestinationRead, DestinationStatus
from app.schemas.place.place import PlaceCreate, PlaceRead, PlaceUpdate

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
reports_router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db), _: User = Depends(require_admin)
):
    return AdminController(db).dashboard()


@router.get("/users/count")
def count_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return {"count": AdminController(db).count_users()}


@router.get("/users", response_model=dict)
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    search: str | None = Query(default=None, max_length=255),
    active: bool | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return AdminController(db).list_users(page, page_size, search, active)


@router.get("/users/{user_id}", response_model=AdminUserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return AdminController(db).get_user(user_id)


@router.patch("/users/{user_id}", response_model=AdminUserRead)
def update_user_status(
    user_id: int,
    payload: AdminUserStatusUpdate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_admin),
):
    return AdminController(db).set_user_status(actor, user_id, payload.status)


@router.get("/destinations", response_model=dict)
def list_destinations(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    destination_status: DestinationStatus | None = Query(default=None, alias="status"),
    search: str | None = Query(default=None, max_length=255),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = AdminController(db).list_destinations(
        page,
        page_size,
        destination_status.value if destination_status else None,
        search,
    )
    result["items"] = [
        DestinationRead.model_validate(destination) for destination in result["items"]
    ]
    return result


@router.post(
    "/destinations",
    response_model=DestinationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_destination(
    payload: AdminDestinationCreate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_admin),
):
    fields = payload.model_dump()
    fields["status"] = payload.status.value
    return AdminController(db).create_destination(actor, fields)


@router.get("/destinations/{destination_id}", response_model=DestinationRead)
def get_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return AdminController(db).get_destination(destination_id)


@router.patch("/destinations/{destination_id}", response_model=DestinationRead)
def update_destination(
    destination_id: int,
    payload: AdminDestinationUpdate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_admin),
):
    return AdminController(db).update_destination(
        actor,
        destination_id,
        payload.model_dump(exclude_unset=True),
    )


@router.patch("/destinations/{destination_id}/status", response_model=DestinationRead)
def update_destination_status(
    destination_id: int,
    payload: AdminDestinationStatusUpdate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_admin),
):
    return AdminController(db).set_destination_status(
        actor, destination_id, payload.status.value
    )


@router.get("/places", response_model=dict)
def list_places(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    destination_id: int | None = Query(default=None, ge=1),
    place_status: PlaceStatus | None = Query(default=None, alias="status"),
    search: str | None = Query(default=None, max_length=255),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = AdminController(db).list_places(
        page,
        page_size,
        destination_id,
        place_status,
        search,
    )
    result["items"] = [PlaceRead.model_validate(place) for place in result["items"]]
    return result


@router.post(
    "/places",
    response_model=PlaceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_place(
    payload: PlaceCreate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_admin),
):
    fields = payload.model_dump()
    fields["status"] = payload.status
    return AdminController(db).create_place(actor, fields)


@router.get("/places/{place_id}", response_model=PlaceRead)
def get_place(
    place_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return AdminController(db).get_place(place_id)


@router.patch("/places/{place_id}", response_model=PlaceRead)
def update_place(
    place_id: int,
    payload: PlaceUpdate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_admin),
):
    return AdminController(db).update_place(
        actor,
        place_id,
        payload.model_dump(exclude_unset=True),
    )


@router.get("/reports", response_model=dict)
def list_reports(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    report_status: ReportStatus | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = AdminController(db).list_reports(
        page, page_size, report_status.value if report_status else None
    )
    result["items"] = [
        AdminReportRead.model_validate(report) for report in result["items"]
    ]
    return result


@router.patch("/reports/{report_id}", response_model=AdminReportRead)
def review_report(
    report_id: int,
    payload: ReportReview,
    db: Session = Depends(get_db),
    actor: User = Depends(require_admin),
):
    return AdminController(db).review_report(
        actor, report_id, payload.status.value, payload.resolution
    )


@router.get("/settings")
def read_admin_settings(_: User = Depends(require_admin)):
    return {
        "app_name": settings.APP_NAME,
        "admin_emails": sorted(settings.admin_emails),
    }


@router.get("/ai/monitoring")
def ai_monitoring(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return AdminController(db).ai_monitoring()


@router.get("/audit-logs", response_model=dict)
def list_audit_logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = AdminController(db).list_audit_logs(page, page_size)
    result["items"] = [
        AdminAuditLogRead.model_validate(log) for log in result["items"]
    ]
    return result


@reports_router.post(
    "",
    response_model=AdminReportRead,
    status_code=status.HTTP_201_CREATED,
)
def submit_report(
    payload: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = AdminController(db).create_report(
        current_user, payload.model_dump(exclude_unset=True)
    )
    return report
