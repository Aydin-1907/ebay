"""Private Supabase Storage access for server-side file delivery."""
from __future__ import annotations

from pathlib import PurePosixPath
from urllib.parse import quote

import httpx
from fastapi.responses import Response

from app.config import get_settings


class StorageError(RuntimeError):
    """The configured cloud storage could not serve a requested file."""


def private_file(bucket: str, key: str, *, media_type: str, filename: str | None = None) -> Response | None:
    """Return a private object, or ``None`` when it does not exist remotely."""
    path = PurePosixPath(key)
    if path.is_absolute() or ".." in path.parts:
        return None

    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        return None
    url = (
        f"{settings.supabase_url.rstrip('/')}/storage/v1/object/"
        f"{quote(bucket, safe='')}/{quote(path.as_posix(), safe='/')}"
    )
    headers = {
        "apikey": settings.supabase_service_role_key,
        "Authorization": f"Bearer {settings.supabase_service_role_key}",
    }
    try:
        response = httpx.get(url, headers=headers, timeout=30)
    except httpx.HTTPError as exc:
        raise StorageError("Supabase Storage ist nicht erreichbar.") from exc
    if response.status_code == 404:
        return None
    if response.is_error:
        raise StorageError(f"Supabase Storage antwortet mit HTTP {response.status_code}.")

    response_headers: dict[str, str] = {}
    if filename:
        response_headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return Response(content=response.content, media_type=media_type, headers=response_headers)
