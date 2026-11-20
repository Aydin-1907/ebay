"""Hype-Puls: gemessene Trends als Ausgangspunkt der Websuche - netzwerkfrei.

Kern: Nur Werte, die die Quelle nennt. Geschuetzte Hypes (Spiele, Marken) bleiben
nutzbar, aber nur als Lebensgefuehl; Unglueck und Politik fliegen raus. Ein Ausfall
einer Quelle stoppt nichts.
"""
from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest

from app.studio.radar import hype_puls

HEUTE = date(2026, 11, 20)

RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:ht="https://trends.google.com/trending/rss" version="2.0"><channel>
<item><title>gta 6</title><ht:approx_traffic>500.000+</ht:approx_traffic>
  <ht:news_item><ht:news_item_title>Release-Tag: Fans stuermen die Laeden</ht:news_item_title>
  <ht:news_item_url>https://news.example/gta</ht:news_item_url></ht:news_item></item>
<item><title>Glatteis</title><ht:approx_traffic>20.000+</ht:approx_traffic></item>
<item><title>Unfall A7</title><ht:approx_traffic>10.000+</ht:approx_traffic></item>
<item><title>GTA 6</title><ht:approx_traffic>1.000+</ht:approx_traffic></item>
</channel></rss>"""

WIKI = {"items": [{"articles": [
    {"article": "Hauptseite", "views": 900000, "rank": 1},
    {"article": "Spezial:Suche", "views": 400000, "rank": 2},
    {"article": "Erster_Advent", "views": 48210, "rank": 3},
    {"article": "Bundestagswahl_2029", "views": 30000, "rank": 4},
]}]}


def _filter(text):
    return SimpleNamespace(allowed="gta" not in text.lower(), reason="franchises:gta")


def test_google_rss_liest_wert_und_schlagzeile():
    funde = hype_puls.lies_google_trends(RSS)
    assert funde[0].thema == "gta 6"
    assert funde[0].wert == "500.000+ Suchanfragen"
    assert funde[0].kontext.startswith("Release-Tag")
    assert funde[0].url == "https://news.example/gta"
    assert funde[1].wert == "20.000+ Suchanfragen"


def test_kaputtes_rss_ist_leer_statt_absturz():
    assert hype_puls.lies_google_trends("<rss><kaputt") == []


def test_wikipedia_ohne_verwaltungsseiten_und_mit_echter_zahl():
    funde = hype_puls.lies_wikipedia(WIKI)
    assert [f.thema for f in funde] == ["Erster Advent", "Bundestagswahl 2029"]
    assert funde[0].wert == "48.210 Aufrufe gestern"
    assert hype_puls.lies_wikipedia({}) == []


def test_osterformel():
    assert hype_puls.ostersonntag(2026) == date(2026, 4, 5)
    assert hype_puls.ostersonntag(2027) == date(2027, 3, 28)


def test_kalender_naechste_wochen_mit_listen_bis():
    anlaesse = {h.thema: h for h in hype_puls.kalender(HEUTE)}
    assert anlaesse["Black Friday"].datum == "2026-11-27"
    assert anlaesse["1. Advent"].datum == "2026-11-29"
    assert anlaesse["Weihnachten"].listen_bis == "2026-12-10"
    # Schon zu nah: listen_bis faellt nicht in die Vergangenheit.
    assert anlaesse["Black Friday"].listen_bis == HEUTE.isoformat()
    # Jahreswechsel: Neujahr kommt aus dem Folgejahr, Valentinstag liegt zu weit weg.
    assert anlaesse["Neujahr"].datum == "2027-01-01"
    assert "Valentinstag" not in anlaesse
    assert "Halloween" not in anlaesse


def test_einordnen_geschuetzt_ungeeignet_frei():
    gta, glatteis, unfall = hype_puls.lies_google_trends(RSS)[:3]
    assert hype_puls.einordnen(gta, _filter).ampel == hype_puls.GESCHUETZT
    assert hype_puls.einordnen(glatteis, _filter).ampel == hype_puls.FREI
    assert hype_puls.einordnen(unfall, _filter).ampel == hype_puls.UNGEEIGNET
    wahl = hype_puls.lies_wikipedia(WIKI)[1]
    assert hype_puls.einordnen(wahl, _filter).ampel == hype_puls.UNGEEIGNET


@pytest.mark.asyncio
async def test_sammle_doppelte_weg_und_ausfall_einer_quelle():
    async def text(url):
        return RSS

    async def json_kaputt(url):
        raise RuntimeError("403")

    bericht = await hype_puls.sammle(HEUTE, hole_text=text, hole_json=json_kaputt,
                                     filter_check=_filter)
    themen = [h.thema for h in bericht.hypes]
    assert themen.count("gta 6") == 1 and "GTA 6" not in themen
    assert bericht.fehler == [{"quelle": "wikipedia", "grund": "403"}]
    assert any(h.quelle == "kalender" for h in bericht.hypes)


@pytest.mark.asyncio
async def test_marktkontext_markiert_geschuetzt_und_laesst_ungeeignetes_weg():
    async def text(url):
        return RSS

    async def js(url):
        return WIKI

    bericht = await hype_puls.sammle(HEUTE, hole_text=text, hole_json=js, filter_check=_filter)
    kontext = hype_puls.marktkontext(bericht)
    assert "gta 6 | 500.000+ Suchanfragen" in kontext
    assert "[GESCHUETZT: nur Lebensgefuehl]" in kontext
    assert "Unfall" not in kontext and "Bundestagswahl" not in kontext
    assert "Black Friday am 2026-11-27" in kontext
    assert "Erfinde keine weiteren Zahlen" in kontext


def test_leerer_puls_ergibt_keinen_kontext():
    assert hype_puls.marktkontext(hype_puls.HypeBericht(stand="2026-11-20")) == ""
