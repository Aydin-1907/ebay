"""Kritiker: eine zweite, strenge Meinung je Empfehlung - netzwerkfrei."""
from __future__ import annotations

import json
from types import SimpleNamespace

from app.studio.radar import kritiker
from app.studio.radar.trends import Trend


def _trend(**over):
    basis = dict(thema="Angeln Herbst", kategorie="mix", warum="Saisonstart im Oktober.",
                zielgruppe="Hobbyangler mit eigenem Boot", kaufmoment="Geschenk zum Saisonstart",
                verkaufswinkel="Ruhiger Moment statt Angeberfoto mit grossem Fisch",
                motiv="Ein Fuchs sitzt am Ufer", spruch="Ruhe am Haken", risiko="Saisonfenster ist kurz")
    basis.update(over)
    return Trend(**basis)


class _FakeKritiker:
    def __init__(self, urteile: dict[str, dict]):
        self._urteile = urteile
        self.gesehen: list[str] = []
        self.responses = SimpleNamespace(create=self._create)

    async def _create(self, *, input, **kw):
        thema = next(t for t in self._urteile if t in input)
        self.gesehen.append(thema)
        return SimpleNamespace(output_text=json.dumps(self._urteile[thema]))


def test_floskel_faellt_schon_bei_der_kostenlosen_vorpruefung_durch():
    t = _trend(verkaufswinkel="Ein beliebtes Motiv fuer jeden Anlass")
    assert kritiker.pruefe_regeln(t) is not None and "Floskel" in kritiker.pruefe_regeln(t)


def test_leere_risikoangabe_ist_keine_echte_pruefung():
    t = _trend(risiko="Keine")
    assert kritiker.pruefe_regeln(t) == "Risikoangabe ist eine Leerformel - kein ehrlicher Pruefpunkt"


def test_echter_pruefpunkt_besteht_die_vorpruefung():
    assert kritiker.pruefe_regeln(_trend()) is None


async def test_urteile_laesst_eine_gute_idee_durch():
    client = _FakeKritiker({"Angeln Herbst": {"bestehen": True, "begruendung": "stark"}})
    ok, begruendung = await kritiker.urteile(_trend(), api_key="k", modell="m", client=client)
    assert ok is True and begruendung == "stark"


async def test_urteile_lehnt_durchschnitt_ab():
    client = _FakeKritiker({"Angeln Herbst": {"bestehen": False, "begruendung": "zu generisch"}})
    ok, begruendung = await kritiker.urteile(_trend(), api_key="k", modell="m", client=client)
    assert ok is False and begruendung == "zu generisch"


async def test_ein_kaputter_kritiker_sperrt_keine_idee():
    class _Kaputt:
        responses = SimpleNamespace(create=None)

        async def _nie(self, **kw):
            raise RuntimeError("down")

    kaputt = _Kaputt()
    kaputt.responses.create = kaputt._nie
    ok, begruendung = await kritiker.urteile(_trend(), api_key="k", modell="m", client=kaputt)
    assert ok is True and begruendung == ""


async def test_filtere_trennt_regel_und_urteil_ablehnungen():
    gut = _trend(thema="Angeln Herbst")
    floskel = _trend(thema="Oktoberfest", verkaufswinkel="Perfekt fuer jeden")
    schwach = _trend(thema="Kaffeetasse")
    client = _FakeKritiker({"Angeln Herbst": {"bestehen": True, "begruendung": "stark"},
                            "Kaffeetasse": {"bestehen": False, "begruendung": "zu generisch"}})

    bestanden, abgelehnt = await kritiker.filtere([gut, floskel, schwach], api_key="k",
                                                  modell="m", client=client)

    assert [t.thema for t in bestanden] == ["Angeln Herbst"]
    assert {"thema": "Oktoberfest", "grund": "Kritiker: Floskel statt eigenem Gedanken: 'fuer jeden'"} in abgelehnt
    assert {"thema": "Kaffeetasse", "grund": "Kritiker: zu generisch"} in abgelehnt
    assert client.gesehen == ["Angeln Herbst", "Kaffeetasse"]   # die Floskel kostete keinen Aufruf
