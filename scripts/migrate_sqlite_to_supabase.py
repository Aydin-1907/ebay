"""Copy the current local Studio database into Supabase PostgreSQL.

The script never changes the SQLite source. It also refuses to write into a
non-empty target database, which makes a mistaken second run harmless.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, func, inspect, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.sql.sqltypes import Boolean, Date, DateTime, Integer, JSON

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")


def fail(message: str) -> None:
    print(f"FEHLER: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalise(value: object, column_type: object) -> object:
    """Turn SQLite's text representations into PostgreSQL-ready values."""
    if value is None:
        return None
    if isinstance(column_type, JSON) and isinstance(value, str):
        return json.loads(value)
    if isinstance(column_type, Boolean) and isinstance(value, int):
        return bool(value)
    if isinstance(column_type, DateTime) and isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    if isinstance(column_type, Date) and not isinstance(column_type, DateTime) and isinstance(value, str):
        return date.fromisoformat(value)
    return value


def create_target_engine(url: str) -> Engine:
    return create_engine(url, pool_pre_ping=True, future=True, connect_args={"connect_timeout": 10})


def main() -> None:
    source_url = os.getenv("DATABASE_URL", "")
    target_url = os.getenv("SUPABASE_DATABASE_URL", "")
    if not source_url.startswith("sqlite"):
        fail("DATABASE_URL muss fuer den Import noch auf die lokale SQLite-Datei zeigen.")
    if not target_url.startswith("postgresql"):
        fail("SUPABASE_DATABASE_URL fehlt oder ist keine PostgreSQL-Verbindung.")

    # Importing the models registers every table with the shared metadata.
    from app import models  # noqa: F401
    from app.database import Base
    from app.studio import models as studio_models  # noqa: F401

    source_engine = create_engine(source_url, future=True)
    target_engine = create_target_engine(target_url)
    try:
        with target_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Supabase-Verbindung erfolgreich.")

        Base.metadata.create_all(target_engine)
        target_inspector = inspect(target_engine)
        with target_engine.connect() as target:
            existing_rows = {
                table.name: target.execute(select(func.count()).select_from(table)).scalar_one()
                for table in Base.metadata.sorted_tables
                if table.name in target_inspector.get_table_names()
            }
        occupied = {name: count for name, count in existing_rows.items() if count}
        if occupied:
            fail(f"Supabase enthaelt bereits Daten ({occupied}). Import wurde nicht gestartet.")

        source_tables = set(inspect(source_engine).get_table_names())
        copied: dict[str, int] = {}

        with source_engine.connect() as source, target_engine.begin() as target:
            for target_table in Base.metadata.sorted_tables:
                if target_table.name not in source_tables:
                    continue
                rows = source.execute(text(f'SELECT * FROM "{target_table.name}"')).mappings().all()
                if not rows:
                    copied[target_table.name] = 0
                    continue
                target_columns = {column.name: column for column in target_table.columns}
                payload = [
                    {
                        name: normalise(value, target_columns[name].type)
                        for name, value in row.items()
                        if name in target_columns
                    }
                    for row in rows
                ]
                target.execute(target_table.insert(), payload)
                copied[target_table.name] = len(payload)

            # Keep identity columns in sync after explicit primary-key inserts.
            for table in Base.metadata.sorted_tables:
                for column in table.columns:
                    if (
                        column.primary_key
                        and isinstance(column.type, Integer)
                        and getattr(column, "autoincrement", False)
                    ):
                        target.execute(
                            text(
                                "SELECT setval(pg_get_serial_sequence(:table_name, :column_name), "
                                "COALESCE((SELECT MAX(" + column.name + ") FROM " + table.name + "), 1), true)"
                            ),
                            {"table_name": table.name, "column_name": column.name},
                        )

        with target_engine.connect() as target:
            verified = {
                table.name: target.execute(select(func.count()).select_from(table)).scalar_one()
                for table in Base.metadata.sorted_tables
                if table.name in copied
            }
        mismatches = {
            name: (copied[name], verified[name])
            for name in copied
            if copied[name] != verified[name]
        }
        if mismatches:
            fail(f"Pruefung fehlgeschlagen (Quelle, Ziel): {mismatches}")

        print("Import abgeschlossen:")
        for name, count in copied.items():
            print(f"  {name}: {count}")
        print("Zeilenanzahl in Supabase verifiziert.")
    finally:
        source_engine.dispose()
        target_engine.dispose()


if __name__ == "__main__":
    main()
