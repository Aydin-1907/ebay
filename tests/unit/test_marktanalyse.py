"""Marktanalyse: echte eBay-Verkaufszahlen vieler Haendler als Beleg - kein Vorbild."""
from __future__ import annotations

import pytest

from app.studio.radar import marktanalyse
from app.studio.radar.ernte import ErnteFehler, Fund


def _fund(titel, verkauft):
    return Fund(titel=titel, url=f"https://www.ebay.de/itm/{titel}", verkauft=verkauft)


def test_suche_quelle_baut_eine_suche_ueber_alle_verkaeufer():
    q = marktanalyse.suche_quelle("Fußball T-Shirt")
    assert q.plattform == "ebay"
    assert "_nkw=Fu" in q.listen_url and "/sch/i.html" in q.listen_url
    assert "str/" not in q.listen_url   # kein einzelner Shop


async def test_beobachte_sortiert_nach_verkaufszahl(monkeypatch):
    async def fake_ernte(quelle, *, limit, nur_verkauft):
        assert nur_verkauft is True
        return [_fund("Wenig", 3), _fund("Viel", 50), _fund("Ohne Zahl", None)]

    monkeypatch.setattr(marktanalyse, "ernte", fake_ernte)

    ergebnis = await marktanalyse.beobachte(["Fußball T-Shirt"])

    assert ergebnis["fehler"] == []
    b = ergebnis["beobachtungen"][0]
    assert b["suchbegriff"] == "Fußball T-Shirt"
    assert [t["titel"] for t in b["treffer"]] == ["Viel", "Wenig"]
    assert b["insgesamt_gelesen"] == 3


async def test_ein_fehlgeschlagener_begriff_stoppt_nicht_die_anderen(monkeypatch):
    async def fake_ernte(quelle, *, limit, nur_verkauft):
        if "schwarz" in quelle.shop:
            raise ErnteFehler("Anmeldung fehlt")
        return [_fund("Treffer", 10)]

    monkeypatch.setattr(marktanalyse, "ernte", fake_ernte)

    ergebnis = await marktanalyse.beobachte(["schwarzes shirt", "Angeln"])

    assert ergebnis["fehler"] == [{"suchbegriff": "schwarzes shirt", "grund": "Anmeldung fehlt"}]
    assert [b["suchbegriff"] for b in ergebnis["beobachtungen"]] == ["Angeln"]


def test_marktkontext_ist_leer_ohne_treffer():
    assert marktanalyse.marktkontext([{"suchbegriff": "x", "treffer": []}]) == ""


def test_marktkontext_nennt_beleg_aber_verlangt_eigenstaendigkeit():
    text = marktanalyse.marktkontext([
        {"suchbegriff": "Angeln T-Shirt",
         "treffer": [{"titel": "Fuchs beim Angeln", "verkauft": 42, "url": "x"}]},
    ])
    assert "42+ verkauft" in text
    assert "Fuchs beim Angeln" in text
    assert "niemals Titel, Spruch oder Gestaltung uebernehmen" in text
    assert "eigenstaendiges" in text


def test_anweisung_haengt_marktkontext_ans_ende():
    from datetime import date

    from app.studio.radar import trends

    ohne = trends.anweisung(6, date(2026, 9, 13))
    mit = trends.anweisung(6, date(2026, 9, 13), marktkontext="BELEG-TEXT-XYZ")

    assert "BELEG-TEXT-XYZ" not in ohne
    assert mit.endswith("BELEG-TEXT-XYZ")
