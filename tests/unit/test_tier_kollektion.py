"""Tier-Kollektion: reine Tiermotive (realistisch/animiert) - besteht die echte Pruefung."""
from __future__ import annotations

import pytest

from app.database import SessionLocal
from app.studio.radar import tier_kollektion as tk
from app.studio.radar import trends


@pytest.fixture
def db():
    sitzung = SessionLocal()
    yield sitzung
    sitzung.close()


def test_nur_das_tier_kein_text():
    ideen = tk.eintraege()
    assert len(ideen) == tk.ANZAHL >= 15
    assert len({i.thema for i in ideen}) == len(ideen)
    for i in ideen:
        assert i.aufbau == "nur_motiv"
        assert i.spruch == ""
        assert trends.qualitaetsgrund(i, "funshirt") is None, (i.thema, trends.qualitaetsgrund(i, "funshirt"))
        assert "kein Text" in trends.prompt_aus(i)


def test_beide_stilgruppen_vorhanden():
    ideen = tk.eintraege()
    gruppen = {i.gruppe for i in ideen}
    assert gruppen == {tk.GRUPPE_REALISTISCH, tk.GRUPPE_ANIMIERT}
    realistisch = [i for i in ideen if i.gruppe == tk.GRUPPE_REALISTISCH]
    animiert = [i for i in ideen if i.gruppe == tk.GRUPPE_ANIMIERT]
    for i in realistisch:
        assert "Comic" in i.stil or "naturgetreue" in i.stil.lower() or "Naturgetreue" in i.stil
    for i in animiert:
        assert "Animationsstil" in i.stil or "cartoon" in i.stil.lower() or "Konturlinien" in i.stil


def test_laden_besteht_die_echte_pruefung_und_verdoppelt_nichts(db):
    erst = tk.lade(db)
    assert erst["abgelehnt"] == [], erst["abgelehnt"]
    zweit = tk.lade(db)
    assert zweit["neu"] == 0 and zweit["aufgefrischt"] == tk.ANZAHL
