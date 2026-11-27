"""Eigene Ideen statt OpenAI-Websuche (Nutzerwunsch 27.11.2026).

"kannst du so machen dass die motive von dir beschrieben werden dann keine
websuche mehr durch chatgpt und nur bild generation durch denen"
"""
from __future__ import annotations

import json
from datetime import date
from types import SimpleNamespace

import pytest

from app.config import Settings
from app.database import SessionLocal
from app.studio.models import MotivIdee
from app.studio.radar import eigene_ideen, trends

HEUTE = date(2026, 11, 27)


@pytest.fixture
def db():
    sitzung = SessionLocal()
    yield sitzung
    sitzung.close()


def _frei(_text):
    return SimpleNamespace(allowed=True, reason="")


def _idee(thema: str, **over) -> dict:
    d = {"thema": thema, "kategorie": "rentner",
         "warum": "Ruhestand ist ein fester Geschenkanlass, ganzjaehrig gesucht.",
         "zeitraum": "ganzjaehrig",
         "zielgruppe": "Frischgebackene Rentner mit Gartenleidenschaft",
         "kaufmoment": "Kollegen schenken es zur Abschiedsfeier am letzten Arbeitstag.",
         "verkaufswinkel": "Der Liegestuhl im eigenen Garten statt Uhr oder Kalender als Symbol.",
         "motiv": "Ein grosser Liegestuhl aus Holz steht im Gras, daneben eine Giesskanne "
                  "und ein kleiner Sonnenhut, klare geschlossene Silhouette ohne Hintergrund.",
         "stil": "Retro-Linienzeichnung", "farben": ["Creme", "Goldgelb", "Hellgrau"],
         "spruch": "Endlich Gartenzeit", "aufbau": "motiv", "produkt": "T-Shirt",
         "druckhinweis": "Kompakte Zentralform mit breiten Konturen ohne feine Verlaeufe.",
         "risiko": "Spruch vor Veroeffentlichung auf fremden Wortlaut pruefen.",
         "suchbegriffe": ["Rente Shirt", "Ruhestand Geschenk", "Rentner Garten T-Shirt"]}
    d.update(over)
    return d


def _schreibe(ordner, name, eintraege):
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / name).write_text(json.dumps(eintraege, ensure_ascii=False), encoding="utf-8")


def _aufraeumen(db, themen):
    for t in themen:
        fid = trends.schluessel(f"rentner-{t}")
        db.query(MotivIdee).filter(MotivIdee.quelle_plattform == trends.PLATTFORM,
                                   MotivIdee.fremd_id == fid).delete()
    db.commit()


def test_ideen_werden_kostenlos_abgelegt_und_nicht_verdoppelt(db, tmp_path):
    themen = ["Testidee Gartenzeit A", "Testidee Gartenzeit B"]
    _schreibe(tmp_path, "rente.json", [_idee(t) for t in themen])
    try:
        erst = eigene_ideen.lade(db, ordner=tmp_path, filter_check=_frei, heute=HEUTE)
        zweit = eigene_ideen.lade(db, ordner=tmp_path, filter_check=_frei, heute=HEUTE)
        assert erst["neu"] == 2 and erst["kosten_usd"] == 0.0
        assert zweit["neu"] == 0 and zweit["aufgefrischt"] == 2
        fid = trends.schluessel(f"rentner-{themen[0]}")
        idee = db.query(MotivIdee).filter(MotivIdee.fremd_id == fid).one()
        assert idee.eigener_prompt          # derselbe Bild-Prompt wie bei der Websuche
    finally:
        _aufraeumen(db, themen)


def test_eigene_ideen_durchlaufen_dieselbe_qualitaetspruefung(db, tmp_path):
    thema = "Testidee zu knapp"
    _schreibe(tmp_path, "a.json", [_idee(thema, zielgruppe="Rentner")])
    try:
        bericht = eigene_ideen.lade(db, ordner=tmp_path, filter_check=_frei, heute=HEUTE)
        assert bericht["neu"] == 0
        assert "Zielgruppe" in bericht["abgelehnt"][0]["grund"]
    finally:
        _aufraeumen(db, [thema])


def test_kaputte_datei_meldet_klaren_fehler(tmp_path):
    (tmp_path / "kaputt.json").write_text("{kein json", encoding="utf-8")
    with pytest.raises(eigene_ideen.IdeenDateiFehler, match="kaputt.json"):
        eigene_ideen.lies(tmp_path)


def test_fehlender_ordner_ist_leer(tmp_path):
    assert eigene_ideen.lies(tmp_path / "gibtsnicht") == []


def test_websuche_ist_standardmaessig_aus():
    assert Settings(_env_file=None).trend_websuche_aktiv is False


async def test_abgeschaltete_websuche_kostet_nichts(db, monkeypatch):
    from app.studio import kosten

    def _darf_nicht(*a, **k):
        raise AssertionError("Kostenbremse lief, obwohl die Websuche aus ist")

    monkeypatch.setattr(kosten, "pruefe", _darf_nicht)
    monkeypatch.setattr(kosten, "verbuche", _darf_nicht)
    s = Settings(_env_file=None, openai_api_key="k", trend_websuche_aktiv=False)
    with pytest.raises(trends.WebsucheAus):
        await trends.lauf(db, s=s, client=object(), heute=HEUTE)
