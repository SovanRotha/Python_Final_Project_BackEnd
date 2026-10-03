import json
from json import JSONDecodeError
from typing import Any

from fastapi import Depends, HTTPException, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.api.deps import get_current_user
from app.controllers.trip.trip_controller import TripController
from app.core.database import get_db
from app.models.user.user import User
from app.routes.common.scoped_factory import create_scoped_router
from app.schemas.trip.trip import TripCreate, TripRead, TripUpdate
from app.services.trip_cover_service import (
    save_trip_cover,
    trip_cover_path,
)

router = create_scoped_router(
    TripController,
    TripCreate,
    TripRead,
    "trips",
    "trips",
    TripUpdate,
    include_create=False,
)


@router.post(
    "",
    response_model=TripRead,
    status_code=status.HTTP_201_CREATED,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "required": [
                            "destination_id",
                            "name",
                            "start_date",
                            "end_date",
                            "currency",
                        ],
                        "properties": {
                            "destination_id": {"type": "integer"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "start_date": {"type": "string", "format": "date"},
                            "end_date": {"type": "string", "format": "date"},
                            "currency": {"type": "string"},
                            "budget_amount": {"type": "number"},
                            "status": {"type": "string"},
                            "data": {"type": "string", "description": "JSON object"},
                            "cover_image": {"type": "string", "format": "binary"},
                        },
                    }
                },
                "application/json": {"schema": TripCreate.model_json_schema()},
            },
        }
    },
)
async def create_trip(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content_type = request.headers.get("content-type", "")
    cover_upload: UploadFile | None = None
    if content_type.startswith("multipart/form-data"):
        form = await request.form()
        fields: dict[str, Any] = {}
        for key, value in form.multi_items():
            if isinstance(value, StarletteUploadFile):
                if key != "cover_image" or cover_upload is not None:
                    raise HTTPException(
                        status_code=422,
                        detail="Only one cover_image file is accepted.",
                    )
                cover_upload = value
            else:
                if key == "cover_image":
                    if value:
                        raise HTTPException(
                            status_code=422,
                            detail="Send cover_image as a file in a multipart/form-data request.",
                        )
                    continue
                fields[key] = value
    elif content_type.startswith("application/json"):
        fields = await request.json()
        if not isinstance(fields, dict):
            raise HTTPException(status_code=422, detail="Trip data must be a JSON object.")
        if fields.get("cover_image") is not None:
            raise HTTPException(
                status_code=422,
                detail="Send cover_image as a file in a multipart/form-data request.",
            )
    else:
        raise HTTPException(
            status_code=415,
            detail="Send trip details as JSON or multipart/form-data.",
        )

    if isinstance(fields.get("data"), str):
        try:
            fields["data"] = json.loads(fields["data"])
        except JSONDecodeError as error:
            raise HTTPException(
                status_code=422,
                detail="The data field must contain a valid JSON object.",
            ) from error

    try:
        payload = TripCreate.model_validate(fields)
    except ValidationError as error:
        raise RequestValidationError(error.errors()) from error

    controller = TripController(db, current_user)
    values = payload.model_dump(exclude_unset=True)
    controller.validate_create(values)

    filename = await save_trip_cover(cover_upload) if cover_upload else None
    if filename is not None:
        values["cover_image"] = filename
    try:
        return controller.create(values)
    except Exception:
        if filename is not None:
            trip_cover_path(filename).unlink(missing_ok=True)
        raise


@router.get("/{trip_id}/cover-image")
def get_trip_cover_image(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trip = TripController(db, current_user).get(trip_id)
    if not trip.cover_image:
        raise HTTPException(status_code=404, detail="Trip cover image not found.")
    image_path = trip_cover_path(trip.cover_image)
    if not image_path.is_file():
        raise HTTPException(status_code=404, detail="Trip cover image file not found.")
    return FileResponse(image_path)
