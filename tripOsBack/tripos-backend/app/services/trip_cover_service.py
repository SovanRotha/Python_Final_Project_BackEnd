import re
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.core.config import settings

MAX_TRIP_COVER_SIZE = 10 * 1024 * 1024
TRIP_COVER_TYPES = {
    b"\x89PNG\r\n\x1a\n": ("image/png", ".png"),
    b"\xff\xd8\xff": ("image/jpeg", ".jpg"),
    b"GIF87a": ("image/gif", ".gif"),
    b"GIF89a": ("image/gif", ".gif"),
}


def trip_cover_directory() -> Path:
    return settings.UPLOAD_DIR / "trip-covers"


def trip_cover_path(filename: str) -> Path:
    if re.fullmatch(r"[0-9a-f]{32}\.(png|jpg|gif|webp)", filename) is None:
        raise HTTPException(status_code=404, detail="Trip cover image not found.")
    return trip_cover_directory() / filename


async def save_trip_cover(upload: UploadFile) -> str:
    content = await upload.read(MAX_TRIP_COVER_SIZE + 1)
    if len(content) > MAX_TRIP_COVER_SIZE:
        raise HTTPException(status_code=413, detail="Trip cover image must be 10 MB or smaller.")

    image_type = next(
        (
            image_type
            for signature, image_type in TRIP_COVER_TYPES.items()
            if content.startswith(signature)
        ),
        None,
    )
    if image_type is None and content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        image_type = ("image/webp", ".webp")
    if image_type is None:
        raise HTTPException(
            status_code=415,
            detail="Upload a valid PNG, JPEG, GIF, or WebP image.",
        )
    if upload.content_type not in {
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/webp",
    }:
        raise HTTPException(status_code=415, detail="Upload a valid image file.")

    filename = f"{uuid4().hex}{image_type[1]}"
    directory = trip_cover_directory()
    directory.mkdir(parents=True, exist_ok=True)
    trip_cover_path(filename).write_bytes(content)
    return filename
