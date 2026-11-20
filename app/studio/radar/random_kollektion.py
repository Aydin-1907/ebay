"""Icon-Kollektion: kleine, freistehende Symbole (Emoji, Herz, Baum, Sterne, ...).

Wunsch des Betreibers (20.11.2026), woertlich: "so random motive ... zb emoji,
schmetterling herz baum sterne etc" - UND: anders als alle anderen Motive
sollen diese beim Einstellen/Produktbau NICHT grossflaechig zentriert
gedruckt werden, sondern klein als Brustlogo links, 8 cm Durchmesser.

Die zweite Haelfte des Wunsches ist technisch, nicht inhaltlich - sie steckt
in ``produktweg.py`` (``_ist_brustlogo_motiv`` erkennt genau diese Gruppe und
platziert entsprechend klein links statt mittig-gross). Dieses Modul traegt
nur den Inhalt: reine Icon-Motive, kein Text, flaches Grafikdesign statt
Fotorealismus - so wie ein Symbol auch bei 8 cm noch klar erkennbar bleibt.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable

from app.studio.radar import trends

KATEGORIE = "funshirt"
GRUPPE = "Icon-Motiv (Brustlogo links, 8 cm)"

_STIL = ("Flaches, grafisches Icon-/Sticker-Design: wenige reine Flaechenfarben, "
         "kraeftige gleichmaessige Konturlinie, stark vereinfachte Formen ohne "
         "Schattierung oder Verlauf - auch sehr klein gedruckt noch klar erkennbar")
_DRUCK = ("Das Symbol allein, freigestellt, geschlossene Silhouette, keine "
          "haarfeinen Linien oder Details, die bei 8 cm Druckgroesse verschwimmen "
          "wuerden")
_RISIKO = "Nur ein allgemeines Symbol, kein Markenzeichen, kein Logo, keine Schriftmarke"
_ZEITRAUM = "Immergruen"
_WARUM = ("Kleine, klare Symbol-Motive eignen sich als dezentes Brustlogo statt "
          "als grossflaechiger Druck und sprechen Kaeufer an, die ein schlichtes "
          "Zeichen statt eines grossen Spruchs wollen.")
_PRODUKT = "T-Shirt, alternativ Hoodie"

# Je Eintrag: (thema, symbol-beschreibung, zielgruppe, suchwort, farben)
_Eintrag = tuple[str, str, str, str, str]

_EINTRAEGE: tuple[_Eintrag, ...] = (
    ("Icon-Smiley", "Ein rundes, lachendes Smiley-Gesicht mit zwei einfachen "
     "Punktaugen und einem breiten Halbmondlaecheln",
     "Kaeufer, die ein froehliches, kleines Zeichen suchen", "Smiley",
     "Sonnengelb, Schwarz"),
    ("Icon-Herz", "Ein einzelnes, symmetrisches Herz mit glatter Kontur und "
     "einem kleinen Lichtreflex oben links",
     "Kaeufer, die ein schlichtes Herz-Symbol suchen", "Herz",
     "Kirschrot, Weiss"),
    ("Icon-Schmetterling", "Ein Schmetterling mit symmetrisch ausgebreiteten "
     "Fluegeln von oben, klares Flügelmuster aus wenigen Flaechen",
     "Kaeufer, die ein zartes Natur-Symbol suchen", "Schmetterling",
     "Himmelblau, Orange, Anthrazit"),
    ("Icon-Baum", "Ein einzelner Baum mit runder Krone und schlankem Stamm, "
     "als klare geschlossene Silhouette",
     "Kaeufer, die ein ruhiges Natur-Symbol suchen", "Baum",
     "Tannengruen, Braun"),
    ("Icon-Sternenhaufen", "Drei unterschiedlich grosse, fuenfzackige Sterne, "
     "versetzt zueinander angeordnet",
     "Kaeufer, die ein kleines Stern-Symbol suchen", "Sterne",
     "Gold, Anthrazit"),
    ("Icon-Blitz", "Ein einzelner, kantiger Blitz von oben nach unten, "
     "klare scharfe Zacken",
     "Kaeufer, die ein kraftvolles, kleines Symbol suchen", "Blitz",
     "Gelb, Anthrazit"),
    ("Icon-Regenbogen", "Ein halbrunder Regenbogen aus wenigen klar "
     "abgegrenzten Farbstreifen, darunter zwei kleine Wolken",
     "Kaeufer, die ein froehliches, buntes Symbol suchen", "Regenbogen",
     "Rot, Gelb, Blau, Weiss"),
    ("Icon-Anker", "Ein klassischer Schiffsanker mit Querbalken, als klare "
     "geschlossene Silhouette",
     "Kaeufer mit Bezug zum Meer, die ein kleines Symbol suchen", "Anker",
     "Marineblau, Weiss"),
    ("Icon-Feder", "Eine einzelne Vogelfeder von der Seite, mit klar "
     "gezeichneter Mittelrippe und wenigen Faserlinien",
     "Kaeufer, die ein leichtes, naturnahes Symbol suchen", "Feder",
     "Taubenblau, Anthrazit"),
    ("Icon-Mondsichel", "Eine schlanke Mondsichel mit glatter Kontur, daneben "
     "ein einzelner kleiner Stern",
     "Kaeufer, die ein ruhiges Nacht-Symbol suchen", "Mond",
     "Nachtblau, Silbergrau"),
    ("Icon-Sonne", "Eine runde Sonne mit gleichmaessigen kurzen Strahlen "
     "ringsherum, als klare geschlossene Form",
     "Kaeufer, die ein froehliches Sommer-Symbol suchen", "Sonne",
     "Sonnengelb, Orange"),
    ("Icon-Kleeblatt", "Ein vierblaettriges Kleeblatt mit symmetrischen, "
     "herzfoermigen Blaettern",
     "Kaeufer, die ein kleines Glueck-Symbol suchen", "Kleeblatt",
     "Kleegruen, Anthrazit"),
    ("Icon-Krone", "Eine einfache Krone mit drei Zacken und je einem kleinen "
     "runden Edelstein darauf",
     "Kaeufer, die ein verspieltes Status-Symbol suchen", "Krone",
     "Gold, Rubinrot"),
    ("Icon-Diamant", "Ein geschliffener Diamant von vorn, mit wenigen klaren "
     "Facettenlinien",
     "Kaeufer, die ein klares, edles Symbol suchen", "Diamant",
     "Eisblau, Weiss"),
    ("Icon-Flamme", "Eine einzelne stilisierte Flamme mit glatter, geschwungener "
     "Kontur",
     "Kaeufer, die ein energiegeladenes, kleines Symbol suchen", "Flamme",
     "Orange, Gelb"),
    ("Icon-Welle", "Eine einzelne stilisierte Wasserwelle mit glatter, "
     "geschwungener Kontur und kleiner Gischtspitze",
     "Kaeufer, die ein ruhiges Meeres-Symbol suchen", "Welle",
     "Petrol, Weiss"),
)

ANZAHL = len(_EINTRAEGE)


def _bauen(e: _Eintrag) -> trends.Trend:
    thema, symbol, ziel, suchwort, farben = e
    motiv = (f"{symbol}. Nur das Symbol, mittig und freigestellt, geschlossene "
             "Silhouette, fuellt den groessten Teil des Bildes aus (das Symbol "
             "selbst nimmt mindestens 85 Prozent der Bildbreite ein, nur ein "
             "schmaler Rand bleibt frei - dieses Motiv wird spaeter stark "
             "verkleinert gedruckt und braucht darum jeden Bildpunkt), kein "
             "Text und keine Buchstaben im Bild.")
    return trends.Trend(
        thema=thema, kategorie=KATEGORIE, warum=_WARUM, zeitraum=_ZEITRAUM,
        zielgruppe=ziel,
        kaufmoment="Ein kleines, klares Symbol wirkt dezent statt aufdringlich.",
        verkaufswinkel=f"Reines Icon-Motiv zum Thema {suchwort} ganz ohne Text",
        motiv=motiv, stil=_STIL, farben=[f.strip() for f in farben.split(",")],
        spruch="", produkt=_PRODUKT, druckhinweis=_DRUCK, risiko=_RISIKO,
        suchbegriffe=[f"{suchwort} Shirt", f"{suchwort} Brustlogo",
                      f"{suchwort} T-Shirt klein"],
        quellen=[], gruppe=GRUPPE, aufbau="nur_motiv")


def eintraege() -> list[trends.Trend]:
    return [_bauen(e) for e in _EINTRAEGE]


def lade(db: Any, *, filter_check: Callable[[str], Any] | None = None,
         heute: date | None = None) -> dict:
    """Kollektion als Empfehlungen ablegen. Kostenlos; mehrfaches Laden verdoppelt nichts."""
    bericht = trends.speichere(
        db, eintraege(), belege=[], angebote={},
        filter_check=filter_check or trends._schutzfilter_check,
        heute=heute or date.today(), erwartete_kategorie=KATEGORIE)
    bericht["kosten_usd"] = 0.0
    return bericht
