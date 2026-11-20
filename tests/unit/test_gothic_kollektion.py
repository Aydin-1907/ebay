"""Gothic-Kollektion: Skelette bei Alltaeglichem und Kreaturen - besteht die echte Pruefung."""
from __future__ import annotations

import pytest

from app.database import SessionLocal
from app.studio.radar import gothic_kollektion as gk
from app.studio.radar import trends


@pytest.fixture
def db():
    sitzung = SessionLocal()
    yield sitzung
    sitzung.close()


def test_nur_das_motiv_kein_text():
    ideen = gk.eintraege()
    assert len(ideen) == gk.ANZAHL >= 10
    assert len({i.thema for i in ideen}) == len(ideen)
    for i in ideen:
        assert i.aufbau == "nur_motiv"
        assert i.spruch == ""
        assert trends.qualitaetsgrund(i, "funshirt") is None, (i.thema, trends.qualitaetsgrund(i, "funshirt"))
        assert "kein Text" in trends.prompt_aus(i)


def test_beide_linien_vorhanden():
    ideen = gk.eintraege()
    skelette = [i for i in ideen if i.thema.startswith("Skelett-")]
    kreaturen = [i for i in ideen if i.thema.startswith("Kreatur-")]
    assert skelette and kreaturen
    assert len(skelette) + len(kreaturen) == len(ideen)
    # Nicht alle Skelett-Eintraege sind weihnachtlich - der Wunsch war
    # ausdruecklich "muss nicht unbedingt was mit weihnachten sein".
    assert any("Weihnacht" not in i.zeitraum for i in skelette)


def test_laden_besteht_die_echte_pruefung_und_verdoppelt_nichts(db):
    erst = gk.lade(db)
    assert erst["abgelehnt"] == [], erst["abgelehnt"]
    zweit = gk.lade(db)
    assert zweit["neu"] == 0 and zweit["aufgefrischt"] == gk.ANZAHL
