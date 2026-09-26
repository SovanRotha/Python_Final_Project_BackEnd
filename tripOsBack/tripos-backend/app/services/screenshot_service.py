from pathlib import Path

from fastapi import UploadFile


async def save_upload(upload: UploadFile, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / Path(upload.filename or "upload").name
    destination.write_bytes(await upload.read())
    return destination