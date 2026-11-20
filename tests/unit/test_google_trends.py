"""Google-Trends-Signal: echter Wert, wenn verfuegbar, sonst None - nie erfunden."""
from __future__ import annotations

import sys
from types import ModuleType, SimpleNamespace

import pandas as pd
import pytest

from app.studio.radar import google_trends


def _fake_pytrends_modul(tabelle=None, *, wirft=None):
    modul = ModuleType("pytrends")
    anfrage_modul = ModuleType("pytrends.request")

    class _FakeTrendReq:
        def __init__(self, **kw):
            pass

        def build_payload(self, kw_list, **kw):
            self._kw = kw_list
            if wirft:
                raise wirft

        def interest_over_time(self):
            return tabelle

    anfrage_modul.TrendReq = _FakeTrendReq
    modul.request = anfrage_modul
    return modul, anfrage_modul


@pytest.fixture
def mit_fake_pytrends(monkeypatch):
    def setze(tabelle=None, *, wirft=None):
        modul, anfrage = _fake_pytrends_modul(tabelle, wirft=wirft)
        monkeypatch.setitem(sys.modules, "pytrends", modul)
        monkeypatch.setitem(sys.modules, "pytrends.request", anfrage)
    return setze


async def test_echtes_interesse_wird_gemittelt(mit_fake_pytrends):
    tabelle = pd.DataFrame({"Kaffee Shirt": [10, 20, 30], "isPartial": [False] * 3})
    mit_fake_pytrends(tabelle)

    ergebnis = await google_trends.interesse(["Kaffee Shirt"])

    assert ergebnis == 20.0


async def test_leere_tabelle_ist_kein_erfundener_wert(mit_fake_pytrends):
    mit_fake_pytrends(pd.DataFrame())

    assert await google_trends.interesse(["Nichts Shirt"]) is None


async def test_fehler_bei_google_bricht_den_lauf_nicht_ab(mit_fake_pytrends):
    mit_fake_pytrends(None, wirft=RuntimeError("429 Too Many Requests"))

    assert await google_trends.interesse(["Angeln Shirt"]) is None


async def test_leere_suchbegriffe_fragen_nichts_ab(mit_fake_pytrends):
    mit_fake_pytrends(pd.DataFrame())

    assert await google_trends.interesse([]) is None


async def test_fehlendes_pytrends_liefert_none(monkeypatch):
    monkeypatch.setitem(sys.modules, "pytrends", None)
    monkeypatch.setitem(sys.modules, "pytrends.request", None)

    assert await google_trends.interesse(["Angeln Shirt"]) is None
