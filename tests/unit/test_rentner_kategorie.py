"""Kategorie Rentner: waehlbar, eigener Auftrag, Antwortformat laesst nur sie zu."""
from __future__ import annotations

from datetime import date

from app.studio import schemas
from app.studio.radar import trends


def test_rentner_ist_waehlbare_kategorie():
    assert "rentner" in trends.KATEGORIEN
    assert schemas.TrendLaufIn(kategorie="rentner").kategorie == "rentner"


def test_rentner_auftrag_ist_liebevoll_und_ohne_altersspott():
    text = trends.anweisung(6, date(2026, 11, 26), "rentner")
    assert "RENTNER & RUHESTAND" in text
    assert "Krankheit" in text
    assert text.rstrip().endswith("rentner.")


def test_einzelkategorie_erlaubt_nur_sich_selbst_im_antwortformat():
    for kategorie in ("rentner", "funshirt", "stadtliebe"):
        fmt = trends.antwort_format(6, kategorie)
        enum = fmt["schema"]["properties"]["empfehlungen"]["items"]["properties"]["kategorie"]["enum"]
        assert enum == [kategorie]


def test_marktbild_steht_im_auftrag_und_verbietet_wortlaut():
    for kategorie in ("rentner", "funshirt", "gothic", "mix"):
        text = trends.anweisung(6, date(2026, 11, 27), kategorie)
        assert "MARKTBILD" in text
        assert "kein Wortlaut" in text
    assert "Grillen:" in trends.anweisung(6, date(2026, 11, 27), "funshirt")


def test_mix_bleibt_bei_den_sieben_mix_kategorien():
    enum = trends.antwort_format(6)["schema"]["properties"]["empfehlungen"]["items"][
        "properties"]["kategorie"]["enum"]
    assert "rentner" not in enum and len(enum) == 7
