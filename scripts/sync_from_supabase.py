"""Echte Daten aus Supabase in die lokale SQLite-DB holen.

Die Gegenrichtung zu migrate_sqlite_to_supabase.py: Dieses Skript schreibt nur
in die lokale DB, nie nach Supabase. Nutzt die REST-API (PostgREST) mit dem
oeffentlichen anon/publishable Key - der ist zum Lesen gedacht und kein
Geheimnis, anders als SUPABASE_SERVICE_ROLE_KEY. Setzt INSERT OR REPLACE ein,
ein erneuter Lauf ist also harmlos.
"""
from __future__ import annotations

import json
import sqlite3
import sys
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from app.config import get_settings  # noqa: E402

# Oeffentlicher anon/publishable Key des eigenen Supabase-Projekts "ebay" -
# zum Lesen gedacht, bewusst kein Geheimnis (siehe Supabase-Doku zu anon keys).
_DEFAULT_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF5"
    "ZGNucmhidXBwdGNwZWVkbGV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ1MTQyNTksImV4"
    "cCI6MjExMDA5MDI1OX0.2SKRqdX7n3PEpQZq5eGz4X6qTCww88-OSYWMXqw7iRU"
)

TABLES = [
    "studio_designs",
    "studio_cost_log",
    "studio_motiv_ideen",
    "pod_products",
    "studio_angebot_optionen",
    "pod_listings",
    "pod_orders",
    "invoices",
]


def fail(message: str) -> None:
    print(f"FEHLER: {message}", file=sys.stderr)
    raise SystemExit(1)


def fetch_all(base_url: str, key: str, table: str) -> list[dict]:
    rows: list[dict] = []
    offset = 0
    page_size = 500
    while True:
        url = f"{base_url}/rest/v1/{table}?select=*&limit={page_size}&offset={offset}"
        req = urllib.request.Request(
            url, headers={"apikey": key, "Authorization": f"Bearer {key}"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            chunk = json.loads(resp.read().decode("utf-8"))
        rows.extend(chunk)
        if len(chunk) < page_size:
            break
        offset += page_size
    return rows


def serialize(value: object) -> object:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


def main() -> None:
    s = get_settings()
    if not s.supabase_url:
        fail("SUPABASE_URL ist in der .env nicht gesetzt.")
    if not s.database_url.startswith("sqlite"):
        fail("DATABASE_URL ist kein SQLite-Pfad - dieses Skript schreibt nur lokale SQLite-Dateien.")
    db_path = s.database_url.split("///", 1)[-1]
    key = s.supabase_service_role_key or _DEFAULT_ANON_KEY

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for table in TABLES:
        cur.execute(f"PRAGMA table_info({table})")
        local_cols = [r[1] for r in cur.fetchall()]
        if not local_cols:
            print(f"{table}: lokale Tabelle fehlt, uebersprungen", file=sys.stderr)
            continue
        rows = fetch_all(s.supabase_url, key, table)
        for row in rows:
            cols = [c for c in local_cols if c in row]
            placeholders = ",".join("?" for _ in cols)
            col_list = ",".join(cols)
            values = [serialize(row[c]) for c in cols]
            cur.execute(
                f"INSERT OR REPLACE INTO {table} ({col_list}) VALUES ({placeholders})",
                values,
            )
        con.commit()
        print(f"{table}: {len(rows)} Zeilen synchronisiert", file=sys.stderr)
    con.close()


if __name__ == "__main__":
    main()
