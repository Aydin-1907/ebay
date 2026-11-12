"""Upload existing Studio assets to the private Supabase Storage buckets.

Run this only after SUPABASE_SERVICE_ROLE_KEY has been added to the local .env.
The source folders are read-only; deletion is a separate, manual final step.
"""
from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from urllib.parse import quote

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def upload_tree(
    client: httpx.Client, *, source: Path, bucket: str, base_url: str, headers: dict[str, str]
) -> int:
    if not source.exists():
        return 0
    uploaded = 0
    for file_path in source.rglob("*"):
        if not file_path.is_file():
            continue
        key = file_path.relative_to(source).as_posix()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        response = client.post(
            f"{base_url}/storage/v1/object/{bucket}/{quote(key, safe='/')}",
            headers={**headers, "Content-Type": content_type, "x-upsert": "true"},
            content=file_path.read_bytes(),
        )
        response.raise_for_status()
        uploaded += 1
        print(f"  {bucket}/{key}")
    return uploaded


def main() -> None:
    base_url = os.getenv("SUPABASE_URL", "").rstrip("/")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not base_url.startswith("https://"):
        raise SystemExit("SUPABASE_URL fehlt.")
    if not service_key.startswith("sb_secret_"):
        raise SystemExit("SUPABASE_SERVICE_ROLE_KEY fehlt. Den vorhandenen Secret Key aus Supabase in .env eintragen.")

    headers = {"apikey": service_key, "Authorization": f"Bearer {service_key}"}
    with httpx.Client(timeout=90) as client:
        assets = upload_tree(
            client,
            source=ROOT / "data" / "studio_images",
            bucket=os.getenv("SUPABASE_ASSETS_BUCKET", "studio-assets"),
            base_url=base_url,
            headers=headers,
        )
        invoices = upload_tree(
            client,
            source=ROOT / "data" / "invoices",
            bucket=os.getenv("SUPABASE_INVOICES_BUCKET", "studio-invoices"),
            base_url=base_url,
            headers=headers,
        )
    print(f"Upload abgeschlossen: {assets} Studio-Dateien, {invoices} Rechnungen.")


if __name__ == "__main__":
    main()
