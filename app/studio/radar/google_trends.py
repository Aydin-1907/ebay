"""Google Trends als kostenloses Zusatzsignal zu einer Trend-Empfehlung.

Die Websuche in ``trends.py`` liefert Text, kein Suchvolumen (Eiserne Regel 3:
keine Schaetzungen). ``pytrends`` fragt die oeffentliche Google-Trends-Seite ab
(kein API-Key, keine Kosten) und liefert einen echten Interesse-Wert 0-100 fuer
die letzten drei Monate in Deutschland - ein tatsaechlich gemessener Wert, kein
erfundener.

``pytrends`` ist eine inoffizielle Bibliothek, die die Trends-Webseite abfragt.
Sie kann von Google zeitweise gedrosselt werden (HTTP 429) oder sich sonst
irren; deshalb gibt ``interesse()`` bei jedem Fehler ``None`` zurueck statt
abzustuerzen - der Trend-Lauf bleibt so verlaesslich wie vorher, das Signal ist
nur eine Zugabe, wenn es klappt.
"""
from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger("app.studio.radar.google_trends")

GEO = "DE"
ZEITRAUM = "today 3-m"


def _interesse_sync(suchbegriffe: list[str]) -> float | None:
    from pytrends.request import TrendReq

    begriffe = [b for b in (suchbegriffe or []) if b.strip()][:5]
    if not begriffe:
        return None
    pytrends = TrendReq(hl="de-DE", tz=60, timeout=(5, 10))
    pytrends.build_payload(begriffe, geo=GEO, timeframe=ZEITRAUM)
    tabelle = pytrends.interest_over_time()
    if tabelle is None or tabelle.empty:
        return None
    spalten = [b for b in begriffe if b in tabelle.columns]
    if not spalten:
        return None
    mittel = tabelle[spalten].tail(14).mean().mean()
    if mittel != mittel:  # NaN
        return None
    return round(min(100.0, max(0.0, float(mittel))), 1)


async def interesse(suchbegriffe: list[str]) -> float | None:
    """Mittleres Google-Trends-Interesse (0-100, DE, letzte ~2 Wochen von 3 Monaten).

    Gibt ``None`` zurueck, wenn pytrends fehlt, blockiert wird oder nichts liefert -
    niemals eine erfundene Zahl.
    """
    try:
        return await asyncio.to_thread(_interesse_sync, suchbegriffe)
    except ImportError:
        logger.warning("pytrends nicht installiert - Google-Trends-Signal uebersprungen")
        return None
    except Exception as exc:  # noqa: BLE001 - Drittanbieter, darf den Lauf nie stoppen
        logger.warning("Google Trends nicht lesbar", extra={"error": str(exc)[:160]})
        return None
