"""Flop-Radar: schwache eigene Angebote erkennen, nie automatisch loeschen."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.config import Settings
from app.database import SessionLocal
from app.studio import optimierung
from app.studio.models import (
    MotivIdee,
    PodListing,
    PodOrder,
    PodProduct,
    StudioDesign,
    StudioFlopVorschlag,
)


class FakeEbay:
    def __init__(self, views: dict[str, int], *, beendet: list[str] | None = None):
        self._views = views
        self.beendet = beendet if beendet is not None else []
        self._client = None

    async def get_traffic_batch(self, item_ids, *, days=7):
        return {i: {"views": self._views[i]} for i in item_ids if i in self._views}

    async def end_item(self, item_id, *, reason="NotAvailable"):
        self.beendet.append(item_id)


def _s(**over):
    return Settings(_env_file=None, optimierung_mindestalter_tage=7,
                    optimierung_min_aufrufe=15, optimierung_min_aufrufe_ohne_verkauf=40, **over)


@pytest.fixture
def db():
    sitzung = SessionLocal()
    yield sitzung
    sitzung.close()


def _listing(db, *, item_id="123", alt_tage=10, status="active"):
    d = StudioDesign(title="Flop-Test", status="draft", source="test")
    db.add(d)
    db.commit()
    prod = PodProduct(design_id=d.id, title="t", status="active", provider="eigen")
    db.add(prod)
    db.commit()
    li = PodListing(product_id=prod.id, channel="ebay", external_id=item_id, status=status,
                    price_eur=14.9, quantity_available=5, url=f"https://www.ebay.de/itm/{item_id}")
    db.add(li)
    db.commit()
    alt = datetime.now(timezone.utc) - timedelta(days=alt_tage)
    db.execute(__import__("sqlalchemy").text(
        "UPDATE pod_listings SET created_at=:a WHERE id=:id"), {"a": alt, "id": li.id})
    db.commit()
    db.refresh(li)
    return d, prod, li


def _aufraeumen(db, *objekte):
    for o in objekte:
        db.delete(o)
    db.commit()


def test_wenig_aufrufe_ist_ein_flop():
    assert optimierung.bewerte(aufrufe=10, verkaeufe=0, min_aufrufe=15,
                               min_aufrufe_ohne_verkauf=40) == (
        "Nur 10 Aufrufe in 7 Tagen (unter 15)")


def test_viele_aufrufe_ohne_verkauf_ist_ein_flop():
    grund = optimierung.bewerte(aufrufe=50, verkaeufe=0, min_aufrufe=15,
                                min_aufrufe_ohne_verkauf=40)
    assert grund == "50 Aufrufe in 7 Tagen, aber kein Verkauf"


def test_gute_zahlen_sind_kein_flop():
    assert optimierung.bewerte(aufrufe=50, verkaeufe=2, min_aufrufe=15,
                               min_aufrufe_ohne_verkauf=40) is None
    assert optimierung.bewerte(aufrufe=20, verkaeufe=0, min_aufrufe=15,
                               min_aufrufe_ohne_verkauf=40) is None


def test_fehlende_aufrufzahl_wird_nicht_zum_flop_erklaert():
    # Regel 3: keine Schaetzungen - ohne lesbare Zahl keine Behauptung.
    assert optimierung.bewerte(aufrufe=None, verkaeufe=0, min_aufrufe=15,
                               min_aufrufe_ohne_verkauf=40) is None


async def test_lauf_markiert_flop_und_verknuepft_offene_idee(db):
    d, prod, li = _listing(db, item_id="100")
    idee = MotivIdee(quelle_plattform="trend", quelle_shop="websuche", fremd_id="x",
                     fremdtitel="", thema="Ersatzidee", status="neu", platz=1)
    db.add(idee)
    db.commit()
    ebay = FakeEbay({"100": 5})

    try:
        bericht = await optimierung.lauf(db, s=_s(), ebay=ebay)

        assert bericht == {"geprueft": 1, "flops": 1}
        vorschlag = optimierung.liste(db)[0]
        assert vorschlag.listing_id == li.id and vorschlag.status == "offen"
        assert vorschlag.aufrufe_7t == 5
        assert "Nur 5 Aufrufe" in vorschlag.grund
        assert vorschlag.ersatz_idee_id == idee.id
    finally:
        db.query(StudioFlopVorschlag).delete()
        _aufraeumen(db, idee, li, prod, d)


async def test_junges_angebot_wird_noch_nicht_geprueft(db):
    d, prod, li = _listing(db, item_id="200", alt_tage=2)
    ebay = FakeEbay({"200": 1})

    try:
        bericht = await optimierung.lauf(db, s=_s(), ebay=ebay)
        assert bericht == {"geprueft": 0, "flops": 0}
        assert optimierung.liste(db) == []
    finally:
        _aufraeumen(db, li, prod, d)


async def test_erholtes_angebot_verliert_den_offenen_hinweis(db):
    d, prod, li = _listing(db, item_id="300")
    ebay_schwach = FakeEbay({"300": 3})
    ebay_stark = FakeEbay({"300": 100})

    try:
        await optimierung.lauf(db, s=_s(), ebay=ebay_schwach)
        assert len(optimierung.liste(db)) == 1

        db.add(PodOrder(listing_id=li.id, channel="ebay", status="paid",
                        sale_total_eur=20, ordered_at=datetime.now(timezone.utc)))
        db.commit()
        await optimierung.lauf(db, s=_s(), ebay=ebay_stark)

        assert optimierung.liste(db) == []
    finally:
        db.query(PodOrder).filter(PodOrder.listing_id == li.id).delete()
        db.query(StudioFlopVorschlag).delete()
        _aufraeumen(db, li, prod, d)


async def test_lauf_setzt_eine_menschliche_entscheidung_nie_zurueck(db):
    d, prod, li = _listing(db, item_id="400")
    ebay = FakeEbay({"400": 2})

    try:
        await optimierung.lauf(db, s=_s(), ebay=ebay)
        vorschlag = optimierung.liste(db)[0]
        vorschlag.status = "behalten"
        db.commit()

        await optimierung.lauf(db, s=_s(), ebay=ebay)

        db.refresh(vorschlag)
        assert vorschlag.status == "behalten"
        assert optimierung.liste(db, status="offen") == []
    finally:
        db.query(StudioFlopVorschlag).delete()
        _aufraeumen(db, li, prod, d)


async def test_behalten_aendert_das_angebot_nicht(db, tmp_path):
    d, prod, li = _listing(db, item_id="500")
    ebay = FakeEbay({"500": 2})
    try:
        await optimierung.lauf(db, s=_s(), ebay=ebay)
        vorschlag = optimierung.liste(db)[0]

        ergebnis = await optimierung.entscheide(db, vorschlag.id, aktion="behalten",
                                                bildordner=tmp_path, ebay=ebay)

        assert ergebnis == {"vorschlag_id": vorschlag.id, "aktion": "behalten"}
        db.refresh(li)
        assert li.status == "active"
        assert ebay.beendet == []
        db.refresh(vorschlag)
        assert vorschlag.status == "behalten" and vorschlag.entschieden_am is not None
    finally:
        db.query(StudioFlopVorschlag).delete()
        _aufraeumen(db, li, prod, d)


async def test_loeschen_beendet_das_angebot_bei_ebay(db, tmp_path):
    d, prod, li = _listing(db, item_id="600")
    ebay = FakeEbay({"600": 2})
    try:
        await optimierung.lauf(db, s=_s(), ebay=ebay)
        vorschlag = optimierung.liste(db)[0]

        ergebnis = await optimierung.entscheide(db, vorschlag.id, aktion="loeschen",
                                                bildordner=tmp_path, ebay=ebay)

        assert ergebnis == {"vorschlag_id": vorschlag.id, "aktion": "loeschen"}
        assert ebay.beendet == ["600"]
        db.refresh(li)
        assert li.status == "ended"
        db.refresh(vorschlag)
        assert vorschlag.status == "geloescht"
    finally:
        db.query(StudioFlopVorschlag).delete()
        _aufraeumen(db, li, prod, d)


async def test_bereits_entschiedener_vorschlag_laesst_sich_nicht_nochmal_entscheiden(db, tmp_path):
    d, prod, li = _listing(db, item_id="700")
    ebay = FakeEbay({"700": 2})
    try:
        await optimierung.lauf(db, s=_s(), ebay=ebay)
        vorschlag = optimierung.liste(db)[0]
        await optimierung.entscheide(db, vorschlag.id, aktion="behalten",
                                     bildordner=tmp_path, ebay=ebay)

        with pytest.raises(optimierung.FlopFehler, match="bereits entschieden"):
            await optimierung.entscheide(db, vorschlag.id, aktion="loeschen",
                                        bildordner=tmp_path, ebay=ebay)
    finally:
        db.query(StudioFlopVorschlag).delete()
        _aufraeumen(db, li, prod, d)
