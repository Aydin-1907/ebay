"""Gaming-Hype-Kollektion: besteht die echte Qualitaets- und Rechtepruefung, nennt keinen Titel."""
from __future__ import annotations

import pytest

from app.database import SessionLocal
from app.studio.radar import gaming_hype_kollektion as gk
from app.studio.radar import trends


@pytest.fixture
def db():
    sitzung = SessionLocal()
    yield sitzung
    sitzung.close()


def test_jeder_eintrag_besteht_die_qualitaetspruefung():
    ideen = gk.eintraege()
    assert len(ideen) == 7
    assert len({i.thema for i in ideen}) == len(ideen)
    for i in ideen:
        assert i.kategorie == "videospiele"
        assert len(i.spruch.split()) <= 4, i.spruch
        assert trends.qualitaetsgrund(i, "videospiele") is None, (i.thema, trends.qualitaetsgrund(i, "videospiele"))


def test_kein_geschuetzter_name_in_irgendeinem_feld():
    from app.studio.generation.service import _schutzfilter

    for i in gk.eintraege():
        text = " ".join([i.thema, i.warum, i.motiv, i.spruch, i.verkaufswinkel, i.kaufmoment,
                         i.zielgruppe, *i.suchbegriffe])
        assert _schutzfilter().check(text).allowed, i.thema


def test_laden_besteht_die_echte_pruefung_und_verdoppelt_nichts(db):
    erst = gk.lade(db)
    assert erst["abgelehnt"] == [], erst["abgelehnt"]
    assert erst["kosten_usd"] == 0.0
    zweit = gk.lade(db)
    assert zweit["neu"] == 0 and zweit["aufgefrischt"] == len(gk.eintraege())
