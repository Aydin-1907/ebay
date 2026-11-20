"""Gothic-Kollektion: Skelette bei Alltaeglichem und angsteinfloessende Kreaturen.

Wunsch des Betreibers (20.11.2026), woertlich: "so eine kategori fuer gothic
sachen wie zb ein skellet mit einer weihnachtsmann muetze oder sowas muss
aber nicht unbedingt was mit weihnachten sein zb ein skellet der buch liesst
oder gitarre spielt ... muss nicht unbedingt skellet sein kann auch so
angsteinfloessende kreaturen sein."

Zwei Linien in einer Gruppe:
* Skelette bei einer ALLTAEGLICHEN, meist harmlosen Taetigkeit (lesen, Gitarre
  spielen, Kaffee trinken) - der Kontrast aus gruseligem Motiv und banaler
  Handlung macht den Witz, nicht Weihnachten speziell.
* Eigenstaendige, angsteinfloessende Kreaturen (Geist, Gargoyle, Rabe mit
  Schaedel, Spinne, Fledermaus) ohne erkennbare Vorlage oder Marke.

Reine Motive ohne Text (``aufbau="nur_motiv"``), realistische, detailreiche
Illustration - kein Comic/Cartoon, das waere eine andere Gruppe. Gleiche
Qualitaets- und Rechtepruefung wie die Websuche (``trends.speichere``).
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable

from app.studio.radar import trends

KATEGORIE = "funshirt"
GRUPPE = "Gothic"

_STIL = ("Realistische, detailreiche Illustration im duesteren Gothic-Stil: "
         "starker Hell-Dunkel-Kontrast, feine Schraffuren, keine Comic-Vereinfachung")
_DRUCK = ("Das Motiv allein, freigestellt, geschlossene Silhouette, kraeftige "
          "Konturen, keine haarfeinen Linien, damit es auch auf Brustgroesse "
          "sauber druckt")
_RISIKO = ("Kein bekannter Charakter, kein Marken- oder Filmbezug - nur ein "
           "allgemeines Skelett- oder Kreaturen-Motiv")
_ZEITRAUM_ALLTAG = "Immergruen, unabhaengig von Jahreszeit oder Anlass"
_ZEITRAUM_WEIHNACHT = "Spitze zur Weihnachtszeit, sonst Immergruen"
_WARUM_SKELETT = ("Der Kontrast aus gruseligem Skelett und ganz banaler, "
                  "alltaeglicher Taetigkeit wirkt komisch statt gruselig und "
                  "spricht Fans von schwarzem Humor an.")
_WARUM_KREATUR = ("Dunkle, detailreiche Kreaturen-Motive sprechen Fans von "
                  "Gothic- und Horror-Aesthetik an, die ein hochwertiges Bild "
                  "statt eines Cartoons wollen.")
_PRODUKT = "T-Shirt, alternativ Hoodie"

# (thema, motiv-beschreibung, zielgruppe, suchwort, farben, warum, zeitraum)
_Eintrag = tuple[str, str, str, str, str, str, str]

_EINTRAEGE: tuple[_Eintrag, ...] = (
    ("Skelett-Weihnachtsmuetze", "Ein sitzendes menschliches Skelett traegt eine "
     "rote Weihnachtsmuetze mit weissem Bommel, die Haltung entspannt zurueckgelehnt",
     "Fans von schwarzem Humor zur Weihnachtszeit", "Skelett Weihnachten",
     "Knochenweiss, Tannengruen, Rot", _WARUM_SKELETT, _ZEITRAUM_WEIHNACHT),
    ("Skelett-Buchleser", "Ein sitzendes Skelett haelt ein aufgeschlagenes Buch "
     "vor sich und liest konzentriert, die Fingerknochen halten die Seiten",
     "Leseratten mit Sinn fuer schwarzen Humor", "Skelett liest",
     "Knochenweiss, Anthrazit, Bordeaux", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Gitarrist", "Ein stehendes Skelett spielt eine E-Gitarre in "
     "ausladender Rockpose, der Kiefer weit geoeffnet",
     "Rock- und Metal-Fans mit Sinn fuer schwarzen Humor", "Skelett Gitarre",
     "Knochenweiss, Schwarz, Violett", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Kaffeetrinker", "Ein sitzendes Skelett haelt eine dampfende "
     "Kaffeetasse mit beiden Handknochen und scheint sie genuesslich zu trinken",
     "Kaffeeliebhaber mit Sinn fuer schwarzen Humor", "Skelett Kaffee",
     "Knochenweiss, Kaffeebraun, Anthrazit", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Radfahrer", "Ein Skelett sitzt gebueckt auf einem alten "
     "Fahrrad, in voller Fahrt, der Umhang weht im Wind",
     "Radfahrer mit Sinn fuer schwarzen Humor", "Skelett Fahrrad",
     "Knochenweiss, Rostrot, Anthrazit", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Gaertner", "Ein kniendes Skelett giesst mit einer alten "
     "Giesskanne eine kleine Topfpflanze",
     "Hobbygaertner mit Sinn fuer schwarzen Humor", "Skelett Garten",
     "Knochenweiss, Blattgruen, Anthrazit", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Kreatur-Gargoyle", "Ein hockender Gargoyle mit grossen Fledermausfluegeln "
     "und spitzen Ohren blickt wachsam nach vorn, die Haut wie Stein texturiert",
     "Fans von Gothic- und Horror-Aesthetik", "Gargoyle",
     "Steingrau, Anthrazit, Moosgruen", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Rabe-Schaedel", "Ein grosser schwarzer Rabe sitzt auf einem "
     "menschlichen Schaedel, der Schnabel leicht geoeffnet",
     "Fans von Gothic- und Horror-Aesthetik", "Rabe Schaedel",
     "Tiefschwarz, Knochenweiss, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Geist", "Eine schwebende, durchscheinende Geistergestalt mit "
     "wehendem Umhang und zwei dunklen, leeren Augenhoehlen",
     "Fans von Gothic- und Horror-Aesthetik", "Geist",
     "Nebelweiss, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Spinne", "Eine grosse, detailreich gezeichnete Spinne sitzt "
     "mittig in einem weit gespannten Spinnennetz",
     "Fans von Gothic- und Horror-Aesthetik", "Spinne Netz",
     "Tiefschwarz, Silbergrau", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Fledermausschwarm", "Ein Schwarm Fledermaeuse fliegt in "
     "aufgefaecherter Formation vor einem grossen, runden Vollmond",
     "Fans von Gothic- und Horror-Aesthetik", "Fledermaus Mond",
     "Tiefschwarz, Nachtblau, Silbergrau", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Wolf-Daemon", "Ein aufrecht stehendes, wolfsaehnliches Wesen mit "
     "gefletschten Zaehnen und gluehenden Augen, die Silhouette drohend geneigt",
     "Fans von Gothic- und Horror-Aesthetik", "Daemon Wolf",
     "Tiefschwarz, Blutrot, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Hexenkatze", "Eine schwarze Katze mit aufgestelltem Ruecken und "
     "weit aufgerissenen gelben Augen sitzt vor einem grossen Vollmond",
     "Fans von Gothic- und Horror-Aesthetik", "Schwarze Katze",
     "Tiefschwarz, Mondgelb, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Totenkopfmotte", "Ein grosser Nachtfalter mit totenkopfaehnlicher "
     "Zeichnung auf dem Ruecken, die Fluegel detailreich geadert",
     "Fans von Gothic- und Horror-Aesthetik", "Totenkopfmotte",
     "Anthrazit, Knochenweiss, Rostbraun", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Knochenbaum", "Ein kahler, verdrehter Baum, dessen Aeste wie "
     "knochige Finger in einen nebligen Nachthimmel greifen",
     "Fans von Gothic- und Horror-Aesthetik", "Gruselbaum",
     "Anthrazit, Nebelgrau, Nachtblau", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Skelett-Skateboarder", "Ein Skelett steht in Schrittstellung auf einem Skateboard, "
     "ein Arm zum Gleichgewicht ausgestreckt, der Umhang weht leicht nach hinten",
     "Skater mit Sinn fuer schwarzen Humor", "Skelett Skateboard",
     "Knochenweiss, Anthrazit, Petrol", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Lagerfeuer", "Ein sitzendes Skelett haelt die Handknochen waermend vor ein "
     "kleines Lagerfeuer, der Schaedel leicht zur Seite geneigt",
     "Camper mit Sinn fuer schwarzen Humor", "Skelett Lagerfeuer",
     "Knochenweiss, Orange, Anthrazit", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Schachspieler", "Ein sitzendes Skelett stuetzt das Kinn auf eine Handknochen "
     "und betrachtet konzentriert ein Schachbrett vor sich",
     "Schachfans mit Sinn fuer schwarzen Humor", "Skelett Schach",
     "Knochenweiss, Anthrazit, Bordeaux", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Schwimmer", "Ein Skelett schwimmt mit ausgestreckten Armen durchs Wasser, "
     "kleine Wasserspritzer loesen sich von den Fingerknochen",
     "Schwimmer mit Sinn fuer schwarzen Humor", "Skelett Schwimmen",
     "Knochenweiss, Tuerkis, Anthrazit", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Pizzabaecker", "Ein stehendes Skelett haelt eine runde Pizza auf einem Schieber "
     "in die Hoehe, der Kiefer freudig geoeffnet",
     "Pizzafans mit Sinn fuer schwarzen Humor", "Skelett Pizza",
     "Knochenweiss, Tomatenrot, Anthrazit", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Skelett-Schrauber", "Ein kniendes Skelett haelt einen Schraubenschluessel an ein "
     "umgedrehtes Fahrrad, eine lose Schraube liegt daneben",
     "Hobbyschrauber mit Sinn fuer schwarzen Humor", "Skelett Werkstatt",
     "Knochenweiss, Rostrot, Anthrazit", _WARUM_SKELETT, _ZEITRAUM_ALLTAG),
    ("Kreatur-Werwolf", "Ein aufrecht stehender Werwolf mit zerzaustem Fell und erhobenen "
     "Krallen heult lautlos vor einem grossen Vollmond",
     "Fans von Gothic- und Horror-Aesthetik", "Werwolf",
     "Dunkelbraun, Nachtblau, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Vampirfledermaeuse", "Ein dichter Schwarm spitzzaehniger Fledermaeuse stuerzt "
     "aus einer dunklen Hoehlenoeffnung heraus",
     "Fans von Gothic- und Horror-Aesthetik", "Vampirfledermaus",
     "Tiefschwarz, Blutrot, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Mumie", "Eine aufrecht stehende, lose umwickelte Mumie mit ausgestreckten "
     "Armen und leeren, dunklen Augenhoehlen",
     "Fans von Gothic- und Horror-Aesthetik", "Mumie",
     "Verblasstes Beige, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Geisterhand", "Eine durchscheinende Geisterhand greift aus einem Nebelschleier "
     "nach vorn, die Finger leicht gespreizt",
     "Fans von Gothic- und Horror-Aesthetik", "Geisterhand",
     "Nebelweiss, Anthrazit", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Kraehenschwarm", "Ein dichter Schwarm Kraehen fliegt in unruhiger Formation "
     "vor einem kahlen, verdrehten Baum auf",
     "Fans von Gothic- und Horror-Aesthetik", "Kraehenschwarm",
     "Tiefschwarz, Anthrazit, Nebelgrau", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Sumpfwesen", "Ein aus Schlamm und Ranken geformtes, humanoides Sumpfwesen "
     "steht reglos zwischen duennen Schilfhalmen",
     "Fans von Gothic- und Horror-Aesthetik", "Sumpfmonster",
     "Moosgruen, Anthrazit, Schlammbraun", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Schattenwesen", "Eine konturlose, rabenschwarze Schattengestalt mit zwei "
     "gluehenden Augen loest sich von einer Hauswand",
     "Fans von Gothic- und Horror-Aesthetik", "Schattenwesen",
     "Tiefschwarz, Gluehrot", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Totenkopffalterschwarm", "Mehrere Nachtfalter mit totenkopfaehnlicher Zeichnung "
     "schwaermen gemeinsam um eine einzelne brennende Kerze",
     "Fans von Gothic- und Horror-Aesthetik", "Falterschwarm",
     "Anthrazit, Knochenweiss, Kerzengelb", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Hexenbesen", "Ein alter Reisigbesen lehnt schraeg an einer Wand, obenauf "
     "sitzt zusammengerollt eine schwarze Katze",
     "Fans von Gothic- und Horror-Aesthetik", "Hexenbesen",
     "Besenbraun, Tiefschwarz", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
    ("Kreatur-Poltergeist", "Mehrere Gegenstaende (Stuhl, Buch, Kerze) schweben lose "
     "verteilt in der Luft, umgeben von einem schwachen Nebelschleier",
     "Fans von Gothic- und Horror-Aesthetik", "Poltergeist",
     "Nebelweiss, Anthrazit, Kerzengelb", _WARUM_KREATUR, _ZEITRAUM_ALLTAG),
)

ANZAHL = len(_EINTRAEGE)


def _bauen(e: _Eintrag) -> trends.Trend:
    thema, motivtext, ziel, suchwort, farben, warum, zeitraum = e
    motiv = (f"{motivtext}. Nur das Motiv, gross und zentral als klarer "
             "Blickfang, freigestellt, geschlossene Silhouette, viel Freiraum, "
             "kein Text und keine Buchstaben im Bild.")
    return trends.Trend(
        thema=thema, kategorie=KATEGORIE, warum=warum, zeitraum=zeitraum,
        zielgruppe=ziel,
        kaufmoment="Fans erkennen sich im eigenwilligen, duesteren Humor wieder.",
        verkaufswinkel=f"Reines Gothic-Motiv zum Thema {suchwort} ganz ohne Text",
        motiv=motiv, stil=_STIL, farben=[f.strip() for f in farben.split(",")],
        spruch="", produkt=_PRODUKT, druckhinweis=_DRUCK, risiko=_RISIKO,
        suchbegriffe=[f"{suchwort} Shirt", f"{suchwort} T-Shirt Motiv",
                      f"Geschenk {suchwort}"],
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
