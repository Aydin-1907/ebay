"""Eigene Ideen: Motiv-Empfehlungen, die Claude im Chat schreibt - ohne OpenAI-Websuche.

Anlass (Betreiber, 27.11.2026): Die OpenAI-Abrechnung zeigte, dass 13 Websuchen
mit gpt-5.5 fast 5 $ kosteten (rund 0,38 $ je Lauf), mehr als 100 Motivbilder.
Wunsch: "dass die motive von dir beschrieben werden ... keine websuche mehr durch
chatgpt und nur bild generation durch denen".

Claude legt die Ideen als JSON-Dateien in ``data/eigene_ideen/`` ab - eine Liste
von Eintraegen mit denselben Feldern wie eine Trend-Empfehlung (``trends.aus_eintrag``).
``lade()`` legt sie ueber ``trends.speichere`` ab. Damit laufen sie durch GENAU
dieselben Pruefungen wie die Websuche-Ideen (Qualitaet, Schutzfilter, Motivart)
und bekommen denselben Bild-Prompt. Kostet nichts; mehrfaches Laden verdoppelt
nichts, weil der Schluessel aus Kategorie und Thema gebildet wird.
"""
from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Callable

from app.studio.radar import trends

logger = logging.getLogger("app.studio.radar.eigene_ideen")

ORDNER = Path("data/eigene_ideen")


class IdeenDateiFehler(ValueError):
    """Eine Ideen-Datei ist kein gueltiges JSON oder keine Liste von Eintraegen."""


def lies(ordner: Path = ORDNER) -> list[dict]:
    """Alle Eintraege aus ``*.json`` im Ordner, in Dateireihenfolge."""
    if not ordner.is_dir():
        return []
    eintraege: list[dict] = []
    for datei in sorted(ordner.glob("*.json")):
        try:
            daten = json.loads(datei.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise IdeenDateiFehler(f"{datei.name}: nicht lesbar ({exc})") from exc
        if not isinstance(daten, list) or not all(isinstance(d, dict) for d in daten):
            raise IdeenDateiFehler(f"{datei.name}: erwartet wird eine Liste von Eintraegen")
        eintraege.extend(daten)
    return eintraege


def lade(db: Any, *, ordner: Path = ORDNER,
         filter_check: Callable[[str], Any] | None = None,
         heute: date | None = None) -> dict:
    """Eigene Ideen als Empfehlungen ablegen. Kostenlos, erzeugt kein Bild."""
    je_kategorie: dict[str, list[trends.Trend]] = defaultdict(list)
    for d in lies(ordner):
        t = trends.aus_eintrag(d)
        je_kategorie[t.kategorie].append(t)

    gesamt = {"neu": 0, "aufgefrischt": 0, "abgelehnt": [], "vorschlaege": 0}
    for kategorie, liste in je_kategorie.items():
        bericht = trends.speichere(
            db, liste, belege=[], angebote={},
            filter_check=filter_check or trends._schutzfilter_check,
            heute=heute or date.today(), erwartete_kategorie=kategorie)
        gesamt["neu"] += bericht["neu"]
        gesamt["aufgefrischt"] += bericht["aufgefrischt"]
        gesamt["abgelehnt"].extend(bericht["abgelehnt"])
        gesamt["vorschlaege"] += bericht["vorschlaege"]
    gesamt["kosten_usd"] = 0.0
    logger.info("eigene Ideen geladen", extra={"neu": gesamt["neu"],
                                                "abgelehnt": len(gesamt["abgelehnt"])})
    return gesamt
