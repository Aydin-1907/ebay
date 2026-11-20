"""Flop-Radar: schwache eigene POD-Angebote erkennen und Ersatz vorschlagen.

**Propose-only (Eiserne Regel 1) und niemals automatisch loeschen (Regel 2).**
``lauf()`` liest nur Aufrufe (eBay Analytics, 7 Tage) und eigene Verkaeufe
(``PodOrder``) und legt dazu hoechstens einen Hinweis ab. Geloescht oder ein
Ersatz eingestellt wird ausschliesslich ueber ``entscheide()`` - und das immer
erst nach einem Klick eines Menschen, nie von selbst.

Schwelle (Nutzerwunsch 17.11.2026): fruehestens nach ``optimierung_mindestalter_tage``
(Standard 7) Tagen online. Ein Angebot ist ein Flop, wenn entweder
* die Aufrufe der letzten 7 Tage unter ``optimierung_min_aufrufe`` liegen, oder
* es trotz ``optimierung_min_aufrufe_ohne_verkauf`` Aufrufen keinen einzigen
  Verkauf hatte - viele Blicke, aber niemand kauft, ist ein eigenes Problem
  (Bild, Preis, Titel), kein Mangel an Sichtbarkeit.

Ein einmal von Hand entschiedener Vorschlag ("behalten"/"geloescht") wird von
einem spaeteren Lauf nie wieder auf "offen" zurueckgesetzt.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import func, select

from app.studio.models import MotivIdee, PodListing, PodOrder, StudioFlopVorschlag

logger = logging.getLogger("app.studio.optimierung")


class FlopFehler(RuntimeError):
    """Eine Entscheidung ueber einen Flop-Vorschlag liess sich nicht ausfuehren."""


@dataclass(frozen=True)
class FlopBewertung:
    listing_id: int
    aufrufe_7t: int | None
    verkaeufe_7t: int
    grund: str | None   # None = kein Flop


def _verkaeufe_7t(db, listing_ids: list[int], seit: datetime) -> dict[int, int]:
    if not listing_ids:
        return {}
    zeilen = db.execute(
        select(PodOrder.listing_id, func.count())
        .where(PodOrder.listing_id.in_(listing_ids), PodOrder.ordered_at >= seit,
               PodOrder.status.notin_(("cancelled", "refunded")))
        .group_by(PodOrder.listing_id)
    ).all()
    return {lid: n for lid, n in zeilen}


def bewerte(*, aufrufe: int | None, verkaeufe: int, min_aufrufe: int,
            min_aufrufe_ohne_verkauf: int) -> str | None:
    """Grund fuer eine Flop-Markierung - oder ``None``, wenn alles in Ordnung ist."""
    if aufrufe is None:
        return None   # keine Aufrufzahl lesbar -> keine Behauptung (Regel 3)
    if aufrufe < min_aufrufe:
        return f"Nur {aufrufe} Aufrufe in 7 Tagen (unter {min_aufrufe})"
    if verkaeufe == 0 and aufrufe >= min_aufrufe_ohne_verkauf:
        return f"{aufrufe} Aufrufe in 7 Tagen, aber kein Verkauf"
    return None


async def _aufrufe_je_listing(ebay: Any, listings: list[PodListing]) -> dict[int, int | None]:
    mit_item_id = {l.id: l.external_id for l in listings if l.external_id}
    if ebay is None or not mit_item_id:
        return {}
    roh = await ebay.get_traffic_batch(list(mit_item_id.values()), days=7)
    umgekehrt = {item_id: listing_id for listing_id, item_id in mit_item_id.items()}
    return {umgekehrt[item_id]: werte.get("views") for item_id, werte in roh.items()
            if item_id in umgekehrt}


def _naechste_offene_idee(db, bereits_verknuepft: set[int]) -> MotivIdee | None:
    """Die bestbewertete offene Trend-Idee, die noch keinem Flop zugeteilt ist."""
    kandidaten = db.execute(
        select(MotivIdee).where(MotivIdee.status == "neu")
        .order_by(MotivIdee.platz.is_(None), MotivIdee.platz)
    ).scalars().all()
    for k in kandidaten:
        if k.id not in bereits_verknuepft:
            return k
    return None


async def lauf(db, *, s: Any, ebay: Any = None, heute: date | None = None) -> dict:
    """Aktive eigene Angebote pruefen und offene Flop-Vorschlaege aktuell halten.

    Aendert nie ein eBay-Angebot - nur die eigene Hinweistabelle.
    """
    heute = heute or date.today()
    mindestalter = datetime.now(timezone.utc) - timedelta(days=s.optimierung_mindestalter_tage)
    sieben_tage = datetime.now(timezone.utc) - timedelta(days=7)

    listings = list(db.scalars(
        select(PodListing).where(PodListing.status == "active",
                                  PodListing.created_at <= mindestalter)
    ).all())
    if not listings:
        return {"geprueft": 0, "flops": 0}

    aufrufe = await _aufrufe_je_listing(ebay, listings)
    verkaeufe = _verkaeufe_7t(db, [l.id for l in listings], sieben_tage)

    bereits_verknuepft = {v.ersatz_idee_id for v in
                          db.scalars(select(StudioFlopVorschlag)
                                    .where(StudioFlopVorschlag.ersatz_idee_id.is_not(None))).all()
                          if v.ersatz_idee_id}

    flops = 0
    for listing in listings:
        a = aufrufe.get(listing.id)
        v = verkaeufe.get(listing.id, 0)
        grund = bewerte(aufrufe=a, verkaeufe=v, min_aufrufe=s.optimierung_min_aufrufe,
                        min_aufrufe_ohne_verkauf=s.optimierung_min_aufrufe_ohne_verkauf)

        vorschlag = db.execute(
            select(StudioFlopVorschlag).where(StudioFlopVorschlag.listing_id == listing.id)
        ).scalars().first()

        if grund is None:
            if vorschlag is not None and vorschlag.status == "offen":
                db.delete(vorschlag)   # hat sich erholt - der offene Hinweis entfaellt
            continue

        flops += 1
        if vorschlag is not None:
            # Eine bereits getroffene menschliche Entscheidung bleibt stehen -
            # ein spaeterer Lauf darf sie nie stillschweigend aufheben.
            if vorschlag.status != "offen":
                continue
            vorschlag.aufrufe_7t = a
            vorschlag.verkaeufe_7t = v
            vorschlag.grund = grund
        else:
            idee = _naechste_offene_idee(db, bereits_verknuepft)
            vorschlag = StudioFlopVorschlag(
                listing_id=listing.id, status="offen", aufrufe_7t=a, verkaeufe_7t=v,
                grund=grund, ersatz_idee_id=idee.id if idee else None,
            )
            if idee:
                bereits_verknuepft.add(idee.id)
            db.add(vorschlag)
    db.commit()
    logger.info("flop-radar fertig", extra={"geprueft": len(listings), "flops": flops})
    return {"geprueft": len(listings), "flops": flops}


def liste(db, *, status: str = "offen") -> list[StudioFlopVorschlag]:
    return list(db.scalars(
        select(StudioFlopVorschlag).where(StudioFlopVorschlag.status == status)
        .order_by(StudioFlopVorschlag.aufrufe_7t.is_(None), StudioFlopVorschlag.aufrufe_7t)
    ).all())


async def entscheide(db, vorschlag_id: int, *, aktion: str, bildordner: Path,
                     ersatz_erzeugen: bool = False, anbieter: str = "openai",
                     produkttyp_key: str = "tshirt", ebay: Any = None) -> dict:
    """Die MENSCHLICHE Entscheidung zu einem Flop-Vorschlag ausfuehren.

    ``aktion``: "behalten" laesst das Angebot unangetastet stehen; "geloeschen"
    beendet es bei eBay (echter Schreibzugriff - im Probebetrieb durch
    ``_NurLesenClient`` gesperrt) und markiert es lokal als beendet.
    """
    if aktion not in ("behalten", "loeschen"):
        raise FlopFehler(f"Unbekannte Aktion '{aktion}'. Moeglich: behalten, loeschen.")
    vorschlag = db.get(StudioFlopVorschlag, vorschlag_id)
    if vorschlag is None:
        raise FlopFehler(f"Flop-Vorschlag {vorschlag_id} gibt es nicht.")
    if vorschlag.status != "offen":
        raise FlopFehler(f"Vorschlag {vorschlag_id} ist bereits entschieden ({vorschlag.status}).")

    ergebnis: dict[str, Any] = {"vorschlag_id": vorschlag_id, "aktion": aktion}
    if aktion == "behalten":
        vorschlag.status = "behalten"
        vorschlag.entschieden_am = datetime.now(timezone.utc)
        db.commit()
        return ergebnis

    listing = db.get(PodListing, vorschlag.listing_id)
    if listing is not None and listing.external_id and ebay is not None:
        await ebay.end_item(listing.external_id, reason="NotAvailable")
    if listing is not None:
        listing.status = "ended"
    vorschlag.status = "geloescht"
    vorschlag.entschieden_am = datetime.now(timezone.utc)
    db.commit()

    if ersatz_erzeugen and vorschlag.ersatz_idee_id:
        from app.studio import produktweg
        from app.studio.radar import nutzen

        idee = db.get(MotivIdee, vorschlag.ersatz_idee_id)
        if idee is None:
            raise FlopFehler("Die verknuepfte Ersatzidee gibt es nicht mehr.")
        erzeugung = nutzen.erzeuge_aus_idee(db, idee, anbieter=anbieter, bildordner=bildordner)
        entwurf = await produktweg.lege_an(erzeugung["design"], produkttyp_key=produkttyp_key,
                                           bildordner=bildordner)
        ergebnis["ersatz"] = {"design_id": erzeugung["design"].id,
                              "kosten_usd": erzeugung["kosten_usd"], **entwurf}
    return ergebnis
