"""Create the private Supabase Storage buckets used by the Studio.

The buckets are deliberately private. The FastAPI app remains responsible for
authorisation and streams a file only to an authenticated dashboard request.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def main() -> None:
    url = os.getenv("SUPABASE_DATABASE_URL", "")
    if not url.startswith("postgresql"):
        raise SystemExit("SUPABASE_DATABASE_URL fehlt.")

    buckets = ("studio-assets", "studio-invoices")
    engine = create_engine(url, future=True, connect_args={"connect_timeout": 10})
    try:
        with engine.begin() as connection:
            for bucket in buckets:
                connection.execute(
                    text(
                        "INSERT INTO storage.buckets (id, name, public) VALUES (:bucket, :bucket, false) "
                        "ON CONFLICT (id) DO UPDATE SET public = false"
                    ),
                    {"bucket": bucket},
                )
        print("Private Supabase-Buckets bereit: " + ", ".join(buckets))
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
