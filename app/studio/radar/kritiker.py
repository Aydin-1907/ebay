"""Kritiker: eine ZWEITE, strenge Meinung zu jeder Trend-Empfehlung.

Nutzerwunsch (17.11.2026): "deine Empfehlungen sind nicht so gut" - ein Skill,
der jede Empfehlung kritisch prueft, BEVOR sie beim Betreiber landet. Der
Websuche-Auftrag in ``trends.py`` waehlt seine eigenen Vorschlaege schon selbst
aus (dieselbe Instanz bewertet sich selten hart genug). Hier urteilt ein
UNABHAENGIGER, zweiter Aufruf ueber jeden EINZELNEN ueberlebenden Vorschlag,
mit einer einzigen Frage: wuerde das WIRKLICH gut verkaufen - oder ist es nur
plausibel klingender Durchschnitt?

Zwei Stufen, dieselbe Reihenfolge wie ueberall in diesem Programm:

1. ``pruefe_regeln()`` - harte, kostenlose Regeln (austauschbare Floskeln,
   Allerweltsmotive, hohle Risikoangaben). Laeuft IMMER, ohne Netz.
2. ``urteile()`` / ``filtere()`` - ein kleiner, kostenpflichtiger Zusatzaufruf
   an ein billiges Modell. Abschaltbar ueber ``trend_kritiker_aktiv``
   (Kostenbremse bucht vorher, Standard AN - der Betreiber wollte ausdruecklich
   die besten Empfehlungen, nicht die billigsten).
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from app.studio.radar.trends import Trend

logger = logging.getLogger("app.studio.radar.kritiker")

KOSTEN_JE_URTEIL_USD = 0.01

#: Floskeln, die fast jede Empfehlung passieren liesse - wer sie im Verkaufswinkel
#: oder Kaufmoment nennt, hat noch keinen eigenen Gedanken formuliert.
_FLOSKELN = (
    "fuer jeden", "für jeden", "jeder mag", "alle lieben", "ideal fuer jeden",
    "ideal für jeden", "perfekt fuer jeden", "perfekt für jeden", "beliebtes motiv",
    "zeitloses design", "klassisches design",
)


def pruefe_regeln(t: Trend) -> str | None:
    """Harte, kostenlose Vorpruefung. Grund fuer eine Ablehnung - oder ``None``."""
    text = " ".join([t.warum, t.verkaufswinkel, t.kaufmoment]).lower()
    treffer = next((f for f in _FLOSKELN if f in text), None)
    if treffer:
        return f"Floskel statt eigenem Gedanken: '{treffer}'"
    risiko = t.risiko.strip().lower().rstrip(".")
    if risiko in {"keine", "keins", "keine bedenken", "keine risiken", "unbedenklich"}:
        return "Risikoangabe ist eine Leerformel - kein ehrlicher Pruefpunkt"
    return None


def _auftrag(t: Trend) -> str:
    return f"""Du bist ein strenger, erfahrener Einkaeufer fuer Print-on-Demand-Mode
(T-Shirts, Hoodies, Tassen) in Deutschland. Dir wird GENAU EIN Vorschlag vorgelegt.
Deine einzige Aufgabe: ehrlich einschaetzen, ob das WIRKLICH gut verkaufen wuerde -
nicht, ob es plausibel klingt. Die meisten Vorschlaege sind Durchschnitt; lehne
Durchschnitt konsequent ab.

Vorschlag:
Thema: {t.thema}
Zielgruppe: {t.zielgruppe}
Kaufmoment: {t.kaufmoment}
Verkaufswinkel (was ihn von Standardmotiven unterscheidet): {t.verkaufswinkel}
Motiv: {t.motiv}
Spruch: {t.spruch or "(keiner)"}

Lehne ab, wenn mindestens eines zutrifft:
- Die Zielgruppe ist austauschbar (koennte auf zehn andere Motive genauso passen).
- Der "Verkaufswinkel" ist keiner - er beschreibt nur das Motiv nochmal.
- Es gibt vermutlich schon zu viele sehr aehnliche Motive im Markt (gleiche Pose,
  gleicher Spruchaufbau wie unzaehlige andere POD-Shirts).
- Der Kaufmoment ist vage ("fuer alle, die X mögen" statt eines konkreten Anlasses).

Antworte NUR als JSON: {{"bestehen": true/false, "begruendung": "hoechstens 20 Woerter"}}"""


async def urteile(t: Trend, *, api_key: str, modell: str, client: Any = None) -> tuple[bool, str]:
    """Das Urteil zu EINEM Vorschlag. Bei einem Anbieterfehler: durchlassen, nicht blockieren."""
    eigener = client is None
    if eigener:
        import openai

        client = openai.AsyncOpenAI(api_key=api_key, max_retries=0, timeout=60.0)
    try:
        antwort = await client.responses.create(
            model=modell, input=_auftrag(t), store=False,
            text={"format": {"type": "json_schema", "name": "kritik", "strict": True,
                             "schema": {"type": "object", "additionalProperties": False,
                                        "properties": {"bestehen": {"type": "boolean"},
                                                      "begruendung": {"type": "string"}},
                                        "required": ["bestehen", "begruendung"]}}})
        daten = json.loads(getattr(antwort, "output_text", "") or "{}")
        return bool(daten.get("bestehen", True)), str(daten.get("begruendung") or "")[:160]
    except Exception as exc:  # noqa: BLE001 - ein kaputter Kritiker darf keine Idee sperren
        logger.warning("Kritiker-Urteil fehlgeschlagen - Vorschlag bleibt drin",
                       extra={"thema": t.thema, "error": str(exc)[:160]})
        return True, ""
    finally:
        if eigener:
            await client.aclose()


async def filtere(trends: list[Trend], *, api_key: str, modell: str,
                  client: Any = None) -> tuple[list[Trend], list[dict]]:
    """Regeln zuerst (kostenlos), dann je ueberlebendem Vorschlag das Urteil."""
    bestanden: list[Trend] = []
    abgelehnt: list[dict] = []
    for t in trends:
        grund = pruefe_regeln(t)
        if grund:
            abgelehnt.append({"thema": t.thema, "grund": f"Kritiker: {grund}"})
            continue
        ok, begruendung = await urteile(t, api_key=api_key, modell=modell, client=client)
        if ok:
            bestanden.append(t)
        else:
            abgelehnt.append({"thema": t.thema,
                             "grund": f"Kritiker: {begruendung or 'zu durchschnittlich'}"})
    logger.info("kritiker fertig", extra={"geprueft": len(trends), "bestanden": len(bestanden)})
    return bestanden, abgelehnt
