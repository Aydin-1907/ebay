"""Gaming-Hype-Kollektion: der grosse Spiele-Release im November 2026, markenfrei.

Herkunft (20.11.2026): Ergebnis einer Trend-Runde zum meisterwarteten Spiele-
Release des Jahrzehnts (19.11.2026). Der Titel selbst ist geschuetzt und steht
deshalb NIRGENDS in dieser Datei - weder im Spruch noch im Motiv noch in den
Suchbegriffen. Genutzt wird nur, was Fans gemeinsam erleben und niemandem gehoert:
Urlaub fuer den Release, die lange Wartezeit, die 80er-Neon-Aesthetik, das
Gangster-Duo als Paar-Idee und Zocken ueber die Feiertage.

Die Eintraege laufen durch dieselbe Qualitaets- und Rechtepruefung wie die
Websuche (``trends.speichere``). Laden kostet nichts; Geld kostet erst
"Motiv erzeugen".
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable

from app.studio.radar import trends

KATEGORIE = "videospiele"
GRUPPE = "Release-Hype Nov 2026"

_BELEG_URLAUB = "https://www.zdfheute.de/wirtschaft/gta-6-verzoegerung-urlaubsantraege-hack-leak-100.html"
_BELEG_PERSONALISIERT = "https://www.gelato.com/de/blog/most-purchased-item-for-christmas"

_STIL = ("Realistische, reduzierte Siebdruck-Illustration im Editorial-Stil, kraeftige "
         "geschlossene Konturen, kontrollierte Schattierung, gut lesbare serifenlose "
         "Blockschrift in Versalien")
_DRUCK = ("Freigestellte Einheit aus Schriftzug und Motiv, kraeftige Konturen, keine "
          "feinen Verlaeufe, auf dunklen Shirts mit heller Schrift am staerksten")
_PRODUKT = "T-Shirt, alternativ Hoodie"
_RISIKO = ("Kein Spieltitel, kein Logo und keine Figur in Titel oder Beschreibung des "
           "Angebots verwenden, sonst droht eine Rechte-Meldung")


def _trend(thema: str, *, warum: str, zeitraum: str, zielgruppe: str, kaufmoment: str,
           verkaufswinkel: str, motiv: str, farben: list[str], spruch: str,
           suchbegriffe: list[str], quellen: list[str], stil: str = _STIL,
           produkt: str = _PRODUKT) -> trends.Trend:
    return trends.Trend(
        thema=thema, kategorie=KATEGORIE, warum=warum, zeitraum=zeitraum,
        zielgruppe=zielgruppe, kaufmoment=kaufmoment, verkaufswinkel=verkaufswinkel,
        motiv=motiv, stil=stil, farben=farben, spruch=spruch, produkt=produkt,
        druckhinweis=_DRUCK, risiko=_RISIKO, suchbegriffe=suchbegriffe,
        quellen=quellen, gruppe=GRUPPE)


def eintraege() -> list[trends.Trend]:
    return [
        _trend(
            "Release-Urlaub",
            warum=("Zum grossen Spiele-Release am 19.11.2026 stiegen die Urlaubsantraege "
                   "laut ZDF um 38 Prozent - das Ritual selbst ist der Witz."),
            zeitraum="Ab sofort bis Weihnachten, danach immergruen fuer jeden grossen Release",
            zielgruppe="Gamer zwischen 18 und 35 mit Buerojob und Sinn fuer Selbstironie",
            kaufmoment=("Partnerin oder Kumpel verschenkt es zu Weihnachten, weil er sich fuer "
                        "den Release extra freigenommen hat."),
            verkaufswinkel=("Statt Spielfigur oder Logo zeigt es das Erlebnis, das alle Fans "
                            "gerade teilen: Urlaub fuer ein Spiel."),
            motiv=("Ein realistisch gezeichneter Abreisskalender, auf dem ein Donnerstag mit "
                   "rotem Kreis markiert ist; davor liegt ein schlichter Gamecontroller ohne "
                   "jedes Logo. Kompakte Einheit unter dem Schriftzug, freigestellt, viel Freiraum."),
            farben=["Signalrot", "Anthrazit", "Creme"],
            spruch="Urlaub. Wichtige Mission.",
            suchbegriffe=["Gamer Shirt lustig", "Zocker Geschenk Mann", "Gaming T-Shirt Spruch"],
            quellen=[_BELEG_URLAUB]),
        _trend(
            "Lange gewartet",
            warum=("Fans haben rund dreizehn Jahre auf diesen Release gewartet; die Wartezeit "
                   "ist das meistgeteilte Meme rund um den Start."),
            zeitraum="Ab sofort bis Fruehjahr, danach als allgemeiner Geduld-Witz",
            zielgruppe="Langjaehrige Konsolenspieler, die seit ihrer Jugend auf Fortsetzungen warten",
            kaufmoment=("Freunde verschenken es zum Release oder zu Weihnachten als Anspielung "
                        "auf die jahrelange Vorfreude."),
            verkaufswinkel=("Die Pointe funktioniert ohne Titel: Wer wartet, versteht sie sofort, "
                            "und sie altert nicht mit dem Spiel."),
            motiv=("Eine realistisch gezeichnete Sanduhr aus Messing und Glas, durch die gerade "
                   "das allerletzte Sandkorn faellt; ein feiner Lichtreflex auf dem Glas. "
                   "Zentral unter dem Schriftzug, freigestellt, ohne Hintergrund."),
            farben=["Gold", "Schwarz", "Sandbeige"],
            spruch="Gewartet. Hat sich gelohnt.",
            suchbegriffe=["Gamer Geduld Shirt", "Zocker T-Shirt lustig", "Videospiel Geschenk"],
            quellen=[_BELEG_URLAUB]),
        _trend(
            "Sunset Drive 86",
            warum=("Der Release rueckt die 80er-Neon-Aesthetik von Sonnenkueste, Palmen und "
                   "Sportwagen in den Mittelpunkt; diese Optik gehoert niemandem."),
            zeitraum="Ab sofort, als Retro-Stil auch langfristig gefragt",
            zielgruppe="Retro- und Synthwave-Fans zwischen 20 und 45 mit Faible fuer Achtziger",
            kaufmoment=("Fan kauft es sich selbst zum Release oder bekommt es als Geschenk zu "
                        "Weihnachten fuer Gaming-Abende."),
            verkaufswinkel=("Eigener Fantasie-Schriftzug und eigene Szene statt Ortsnamen aus dem "
                            "Spiel; traegt den Hype, ueberlebt ihn aber."),
            motiv=("Die Silhouette eines flachen Cabrios aus den Achtzigern faehrt vor einer "
                   "grossen, horizontal gestreiften Neon-Sonne; zwei schlanke Palmen rahmen die "
                   "Szene seitlich. Geschlossene runde Gesamtform, freigestellt, ohne Landschaft."),
            farben=["Neonpink", "Orange", "Violett", "Tiefblau"],
            spruch="Sunset Drive 86",
            suchbegriffe=["Retro 80er Shirt", "Synthwave T-Shirt", "Neon Palmen Shirt"],
            quellen=[],
            stil=("Realistische Retro-Siebdruck-Illustration im Editorial-Stil der Achtziger, "
                  "klare Flaechen, kontrollierte Verlaeufe nur in der Sonne")),
        _trend(
            "Gangster-Duo Fahrerin",
            warum=("Das Spiel stellt erstmals ein Gangster-Paar in den Mittelpunkt; Paar-Shirts "
                   "zu gemeinsamen Hobbys sind vor Weihnachten gefragt."),
            zeitraum="Weihnachten und Valentinstag",
            zielgruppe="Paare zwischen 20 und 40, die gemeinsam zocken oder Krimis lieben",
            kaufmoment=("Ein Partner kauft beide Shirts als Set zu Weihnachten oder zum "
                        "Valentinstag fuer den gemeinsamen Spieleabend."),
            verkaufswinkel=("Rollenverteilung als Paar-Witz statt Figuren: Sie faehrt, er plant - "
                            "eigene Idee, kein fremder Charakter."),
            motiv=("Ein schlichter Steckbrief-Rahmen mit Nagel oben, darin ein realistisch "
                   "gezeichnetes Lenkrad mit Lederbezug. Klare Rechteckform unter dem "
                   "Schriftzug, freigestellt, viel Freiraum."),
            farben=["Senfgelb", "Schwarz", "Braun"],
            spruch="Die Fahrerin.",
            suchbegriffe=["Partner Shirts Paar", "Paar T-Shirt lustig", "Partnerlook Geschenk"],
            quellen=[]),
        _trend(
            "Gangster-Duo Plan",
            warum=("Gegenstueck zur Fahrerin: Paar-Sets verkaufen sich als Doppelpack und "
                   "erhoehen den Warenkorb pro Bestellung."),
            zeitraum="Weihnachten und Valentinstag",
            zielgruppe="Paare zwischen 20 und 40, die gemeinsam zocken oder Krimis lieben",
            kaufmoment=("Ein Partner kauft beide Shirts als Set zu Weihnachten oder zum "
                        "Valentinstag fuer den gemeinsamen Spieleabend."),
            verkaufswinkel=("Rollenverteilung als Paar-Witz statt Figuren: Er plant, sie faehrt - "
                            "eigene Idee, kein fremder Charakter."),
            motiv=("Ein schlichter Steckbrief-Rahmen mit Nagel oben, darin eine realistisch "
                   "gezeichnete, zusammengerollte Landkarte mit rotem Kreuz. Klare Rechteckform "
                   "unter dem Schriftzug, freigestellt, viel Freiraum."),
            farben=["Senfgelb", "Schwarz", "Rot"],
            spruch="Der Plan.",
            suchbegriffe=["Partner Shirts Paar", "Paar T-Shirt lustig", "Partnerlook Geschenk"],
            quellen=[]),
        _trend(
            "Feiertage durchgezockt",
            warum=("Der Release liegt fuenf Wochen vor Weihnachten - viele spielen ueber die "
                   "Feiertage, Weihnachtsshirts mit Gaming-Pointe sind selten."),
            zeitraum="Bis Weihnachten, spaetestens bis 10.12. listen wegen Druck und Versand",
            zielgruppe="Gamer jeden Alters ab 16, die Feiertage am liebsten vor der Konsole verbringen",
            kaufmoment=("Familie oder Partner verschenkt es an Heiligabend mit einem Augenzwinkern "
                        "auf die geplanten Zocknaechte."),
            verkaufswinkel=("Verbindet Weihnachtsmotiv und Gaming in einer Form, statt nur einen "
                            "Controller mit Muetze zu zeigen."),
            motiv=("Ein kleiner, realistisch gezeichneter Tannenbaum, dessen Lichterkette am "
                   "unteren Ende in ein Controllerkabel uebergeht; der Stecker liegt locker davor. "
                   "Kompakte Dreiecksform unter dem Schriftzug, freigestellt."),
            farben=["Tannengruen", "Warmgelb", "Rot"],
            spruch="Stille Nacht, durchgezockt.",
            suchbegriffe=["Gamer Weihnachtsshirt", "Weihnachten Zocker Geschenk",
                          "Gaming Weihnachten T-Shirt"],
            quellen=[]),
        _trend(
            "Gesucht Dauerzocker",
            warum=("Steckbrief-Optik passt zum Gangster-Thema des Releases; personalisierte "
                   "Geschenke wachsen laut Gelato Ende 2026 um ueber 30 Prozent."),
            zeitraum="Weihnachten, danach Geburtstage",
            zielgruppe="Geschwister, Partner und Freunde von Vielspielern zwischen 16 und 40",
            kaufmoment=("Jemand verschenkt es zu Weihnachten oder zum Geburtstag an den "
                        "Vielspieler, der nie vom Bildschirm wegkommt."),
            verkaufswinkel=("Klassischer Steckbrief-Witz auf Gamer gemuenzt; spaeter mit eigenem "
                            "Namen personalisierbar und dadurch hoeher zu bepreisen."),
            motiv=("Ein vergilbtes Fahndungsplakat mit eingerissenen Ecken und Reisszwecken, in der "
                   "Mitte statt eines Gesichts ein realistisch gezeichneter Gamecontroller ohne Logo. "
                   "Rechteckige geschlossene Form, freigestellt."),
            farben=["Sepia", "Schwarz", "Rostrot"],
            spruch="Gesucht: Dauerzocker.",
            suchbegriffe=["Zocker Shirt lustig", "Gamer Geschenk Freund", "Steckbrief T-Shirt"],
            quellen=[_BELEG_PERSONALISIERT]),
    ]


ANZAHL = len(eintraege())


def lade(db: Any, *, filter_check: Callable[[str], Any] | None = None,
         heute: date | None = None) -> dict:
    """Kollektion als Empfehlungen ablegen. Kostenlos; mehrfaches Laden verdoppelt nichts."""
    bericht = trends.speichere(
        db, eintraege(), belege=[], angebote={},
        filter_check=filter_check or trends._schutzfilter_check,
        heute=heute or date.today(), erwartete_kategorie=KATEGORIE)
    bericht["kosten_usd"] = 0.0
    return bericht
