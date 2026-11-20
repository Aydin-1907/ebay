"""Motiv-Kollektion: grosses Motiv, kleiner Text - besteht die echte Pruefung."""
from __future__ import annotations

import pytest

from app.database import SessionLocal
from app.studio.radar import motiv_kollektion as mk
from app.studio.radar import trends


@pytest.fixture
def db():
    sitzung = SessionLocal()
    yield sitzung
    sitzung.close()


def test_motiv_traegt_text_bleibt_kurz():
    ideen = mk.eintraege()
    assert len(ideen) == mk.ANZAHL >= 15
    assert len({i.thema for i in ideen}) == len(ideen)
    for i in ideen:
        assert i.aufbau in {"motiv", "nur_motiv"}
        assert len(i.spruch.split()) <= 3, i.spruch
        assert trends.qualitaetsgrund(i, "funshirt") is None, (i.thema, trends.qualitaetsgrund(i, "funshirt"))
    assert any(i.aufbau == "nur_motiv" for i in ideen)


def test_prompt_stellt_das_motiv_nach_vorn():
    zelt = next(i for i in mk.eintraege() if i.thema == "Zelt-Zuhause")
    prompt = trends.prompt_aus(zelt)
    assert "drei Viertel" in prompt and "deutlich kleiner" in prompt and "Mein Zuhause." in prompt
    ohne = next(i for i in mk.eintraege() if i.aufbau == "nur_motiv")
    assert "kein Text" in trends.prompt_aus(ohne)


def test_qualitaet_lehnt_widersprueche_ab():
    zelt = next(i for i in mk.eintraege() if i.thema == "Zelt-Zuhause")
    zelt.spruch = "Das hier ist mein Zuhause"
    assert "zu lang" in trends.qualitaetsgrund(zelt, "funshirt")
    zelt.aufbau, zelt.spruch = "nur_motiv", "Text"
    assert "Spruch" in trends.qualitaetsgrund(zelt, "funshirt")


def test_laden_besteht_die_echte_pruefung_und_verdoppelt_nichts(db):
    erst = mk.lade(db)
    assert erst["abgelehnt"] == [], erst["abgelehnt"]
    zweit = mk.lade(db)
    assert zweit["neu"] == 0 and zweit["aufgefrischt"] == mk.ANZAHL
