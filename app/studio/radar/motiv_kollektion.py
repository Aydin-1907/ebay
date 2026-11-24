"""Motiv-Kollektion: grosses Motiv als Blickfang, darunter nur ein kleiner Text.

Wunsch des Betreibers (20.11.2026): Nicht immer den Spruch nach vorn stellen,
sondern abwechseln. Beispiel aus dem Gespraech: "nur ein Zelt in gross und darunter
kleiner Text 'Mein Zuhause'". Diese Kollektion ist das Gegenstueck zu den
Fun-Shirt-Spruechen (``funshirt_kollektion.py``): Hier traegt das BILD, der Text
pointiert es mit hoechstens drei Woertern. Zwei Eintraege kommen ganz ohne Text aus.

Gleiche Kategorie wie die Fun-Shirts (``funshirt``), damit beides im Studio
nebeneinander steht, aber in eigener Gruppe "Motiv gross, Text klein".
Die Eintraege laufen durch dieselbe Qualitaets- und Rechtepruefung wie die
Websuche (``trends.speichere``). Laden kostet nichts; Geld kostet erst
"Motiv erzeugen".
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable

from app.studio.radar import trends

KATEGORIE = "funshirt"
GRUPPE = "Motiv groß, Text klein"

_STIL = ("Realistische Siebdruck-Illustration im Editorial-Stil: ein grosses, detailliertes "
         "Hauptmotiv mit kraeftigen Konturen und kontrollierter Schattierung, darunter eine "
         "kleine, gut lesbare serifenlose Blockschrift in Versalien")
_DRUCK = ("Grosses Motiv und kleiner Schriftzug als eine freigestellte Einheit, kraeftige "
          "Konturen, keine haarfeinen Linien, damit es auch auf Brustgroesse sauber druckt")
_RISIKO = "Vor dem Einstellen pruefen, dass das Motiv keiner bekannten Marke oder Vorlage aehnelt"
_ZEITRAUM = "Immergruen, Spitzen zu Geburtstagen, Weihnachten und zur jeweiligen Saison"
_WARUM = ("Hobby- und Lebensgefuehl-Motive verkaufen sich ganzjaehrig; ein starkes Bild mit "
          "kurzer Pointe wirkt in der eBay-Vorschau als Blickfang statt als reiner Textdruck.")
_PRODUKT = "T-Shirt, alternativ Hoodie oder Tasse"

# Je Eintrag: (thema, grosses motiv, kleiner text oder "", zielgruppe, suchwort, farben)
# Regeln: Text hoechstens drei Woerter; leer = reines Motiv. Keine Marken, keine Vorlagen.
_Eintrag = tuple[str, str, str, str, str, str]

_EINTRAEGE: tuple[_Eintrag, ...] = (
    ("Zelt-Zuhause", "Ein grosses Kuppelzelt mit hochgeschlagener Eingangsplane, im Eingang "
     "glimmt eine kleine Laterne, davor zwei Heringe im Gras",
     "Mein Zuhause.", "Campingfans, die jedes Wochenende draussen schlafen", "Camping",
     "Tannengruen, Orange, Anthrazit"),
    ("Hecht-Feierabend", "Ein grosser Hecht springt im Bogen aus dem Wasser, an seinem Maul "
     "spannt sich eine feine Angelschnur, Wassertropfen spritzen seitlich weg",
     "Feierabend.", "Hobbyangler, die nach der Arbeit direkt ans Wasser fahren", "Angeln",
     "Olivgruen, Silbergrau, Dunkelblau"),
    ("Wanderschuh-Gipfel", "Ein grosser, abgetragener Wanderschuh mit dicken Schnuersenkeln, "
     "dessen Schaft oben in eine Bergsilhouette mit verschneitem Gipfel uebergeht",
     "Gipfel statt Sofa.", "Wanderer und Bergfans, die jedes freie Wochenende in den Alpen sind",
     "Wandern", "Braun, Steingrau, Himmelblau"),
    ("Kaffeekanne-Elixier", "Eine grosse emaillierte Kaffeekanne mit kleinen Abplatzern am "
     "Rand, aus dem Ausguss steigt eine geschwungene Dampffahne",
     "Lebenselixier.", "Kaffeeliebhaber, die ohne die erste Tasse nicht funktionieren", "Kaffee",
     "Kaffeebraun, Creme, Rot"),
    ("Dackel-Chef", "Ein grosser Dackel liegt ausgestreckt und zufrieden schlafend auf einem "
     "dicken runden Kissen, die Ohren seitlich herabhaengend",
     "Chef im Haus.", "Dackelbesitzer, die zugeben, wer zuhause wirklich bestimmt", "Dackel",
     "Rotbraun, Senfgelb, Anthrazit"),
    ("Kater-Mitbewohner", "Ein grosser getigerter Kater liegt quer auf einem aufgeschlagenen "
     "Buch und schaut mit halb geschlossenen Augen gelangweilt nach vorn",
     "Mein Mitbewohner.", "Katzenhalter, die ihre Katze als heimlichen Mitbewohner sehen",
     "Katze", "Orange, Creme, Anthrazit"),
    ("Giesskanne-Garten", "Eine grosse verzinkte Giesskanne, aus deren Ausguss statt Wasser "
     "eine Tomatenpflanze mit drei roten Fruechten herauswaechst",
     "Gartenzeit.", "Hobbygaertner, die jede freie Minute im Beet verbringen", "Garten",
     "Grau, Tomatenrot, Blattgruen"),
    ("Motorrad-Kurvenliebe", "Ein grosses klassisches Motorrad ohne Markenzeichen in "
     "Seitenansicht, leicht in eine Kurve geneigt, mit runden Scheinwerfern und Speichenraedern",
     "Kurvenliebe.", "Motorradfahrer, die am Wochenende Landstrassen und Paesse fahren",
     "Motorrad", "Schwarz, Chrom, Rot"),
    ("Rennrad-Huegel", "Ein grosses schlankes Rennrad ohne Markenzeichen in Seitenansicht, "
     "dahinter steigt eine einzelne Linie wie ein Hoehenprofil steil an",
     "Noch ein Hügel.", "Rennradfahrer, die freiwillig jeden Anstieg mitnehmen", "Rennrad",
     "Anthrazit, Signalrot, Hellgrau"),
    ("Grill-Flamme", "Ein grosser runder Holzkohlegrill mit geoeffnetem Deckel, auf dem Rost "
     "zwei Wuerstchen, darunter zuengeln stilisierte Flammen",
     "Feuer und Flamme.", "Grillfans, die auch im Winter auf der Terrasse stehen", "Grillen",
     "Schwarz, Orange, Rot"),
    ("Buecherstapel-Kapitel", "Ein grosser, leicht schiefer Stapel abgegriffener Buecher, "
     "obenauf eine dampfende Teetasse und eine Lesebrille",
     "Noch ein Kapitel.", "Leseratten, die nachts nicht aufhoeren koennen zu lesen", "Lesen",
     "Dunkelgruen, Bordeaux, Creme"),
    ("Mond-Nachteule", "Ein grosser Vollmond mit fein gezeichneten Kratern, davor sitzt eine "
     "kleine Eule als Silhouette auf einem kahlen Ast",
     "Nachteule.", "Nachtmenschen, die erst nach Mitternacht richtig wach werden", "Nachteule",
     "Hellgrau, Nachtblau, Gold"),
    ("Camper-Freiheit", "Ein grosser kantiger Kastenwagen-Camper ohne Markenzeichen in "
     "Seitenansicht, auf dem Dach ein Surfbrett, die Schiebetuer offen",
     "Freiheit auf Rädern.", "Vanlife-Fans und Wohnmobilfahrer, die spontan losfahren",
     "Camper", "Mintgruen, Creme, Anthrazit"),
    ("Kanu-Ruhe", "Ein grosses Holzkanu von schraeg oben auf glattem Wasser, ein Paddel "
     "liegt quer darin, um das Boot ziehen sich zwei ruhige Wellenringe",
     "Wasser statt Stress.", "Paddler und Kanuwanderer, die am See abschalten", "Kanu",
     "Holzbraun, Petrol, Creme"),
    ("Biene-Fleissig", "Eine grosse, realistisch gezeichnete Honigbiene im Flug mit "
     "durchscheinenden Fluegeln, unter ihr haengt eine einzelne Wabe mit Honigtropfen",
     "Fleißig. Manchmal.", "Hobbyimker und Gartenfreunde mit Sinn fuer Selbstironie",
     "Biene", "Honiggelb, Schwarz, Bernstein"),
    ("Steinpilz-Revier", "Ein grosser Steinpilz mit praller brauner Kappe auf einem kleinen "
     "Moospolster, daneben ein einzelnes Eichenblatt",
     "Revier geheim.", "Pilzsammler, die ihre Fundstellen niemandem verraten", "Pilze",
     "Kastanienbraun, Moosgruen, Creme"),
    ("Fuchs-Schnee", "Ein grosser Rotfuchs sitzt aufrecht im Schnee, der buschige Schwanz "
     "um die Pfoten gelegt, sein Atem steigt als kleine Wolke auf",
     "", "Naturliebhaber und Winterfans, die ruhige Tiermotive moegen", "Fuchs",
     "Fuchsrot, Weissgrau, Anthrazit"),
    ("Berglinie-Minimal", "Eine grosse durchgehende Linie zeichnet drei Berggipfel nach, "
     "ueber dem hoechsten steht eine kleine runde Sonne, darunter ein schmaler See als Spiegelung",
     "", "Bergfans, die schlichte Linienmotive statt Sprueche tragen", "Berge",
     "Dunkelblau, Senfgelb"),
    ("Surfbrett-Welle", "Ein grosses Surfbrett steht aufrecht im Sand, dahinter rollt "
     "eine einzelne stilisierte Wellenlinie heran",
     "Horizont.", "Surfer und Strandfans, die vom naechsten Urlaub traeumen", "Surfen",
     "Petrol, Sandbeige, Weiss"),
    ("Kletterseil-Gipfel", "Ein aufgerolltes Kletterseil mit Karabiner liegt vor einer "
     "schroffen Felswand, die in eine spitze Gipfelsilhouette ausläuft",
     "Höher geht immer.", "Kletterer, die jedes Wochenende an der Wand haengen", "Klettern",
     "Steingrau, Signalrot, Anthrazit"),
    ("Segelboot-Horizont", "Ein grosses Segelboot mit gesetztem Hauptsegel gleitet seitlich "
     "ueber ruhige Wellenlinien, eine einzelne Moewe zieht darueber",
     "Kurs halten.", "Segler und Wassersportfans, die den Wind lieben", "Segeln",
     "Marineblau, Weiss, Senfgelb"),
    ("Akkordeon-Takt", "Ein grosses, detailliert gezeichnetes Akkordeon mit auseinandergezogenem "
     "Balg steht leicht schraeg im Bild",
     "Eigener Takt.", "Hobbymusiker mit Vorliebe fuer traditionelle Instrumente", "Akkordeon",
     "Perlmuttweiss, Bordeaux, Gold"),
    ("Schreibmaschine-Kapitel", "Eine grosse alte Schreibmaschine mit eingespanntem Blatt, "
     "aus der Walze ragt ein einzelnes beschriebenes Blatt",
     "Nächstes Kapitel.", "Schreibfans und Autoren mit Vorliebe fuer Nostalgie", "Schreiben",
     "Anthrazit, Elfenbein, Kupfer"),
    ("Globus-Fernweh", "Ein grosser alter Standglobus mit sichtbaren Laendergrenzen und "
     "einer kleinen Messingfassung am Fuss",
     "Nächstes Ziel.", "Reisefans mit Vorliebe fuer Fernweh und alte Landkarten", "Reisen",
     "Ozeanblau, Messing, Creme"),
    ("Weinflasche-Ernte", "Eine grosse, schlanke Weinflasche mit einfachem Etikett, davor "
     "liegt eine einzelne Traubenranke mit drei Beeren",
     "Gute Ernte.", "Weinliebhaber, die Wert auf einfache Eleganz legen", "Wein",
     "Bordeaux, Olivgruen, Creme"),
    ("Teekanne-Ruhe", "Eine grosse, rundliche Teekanne mit aufsteigender Dampffahne, "
     "daneben liegt ein einzelnes Teeblatt",
     "Kurz durchatmen.", "Teeliebhaber, die ihre Ruhepause zelebrieren", "Tee",
     "Jadegruen, Creme, Gold"),
    ("Werkzeugkasten-Ordnung", "Ein grosser, leicht geoeffneter Werkzeugkasten mit sauber "
     "sortierten Schraubenziehern und einem Schraubenschluessel obenauf",
     "Alles im Griff.", "Hobbyhandwerker, die Ordnung in der Werkstatt lieben", "Werkzeug",
     "Stahlblau, Rostrot, Anthrazit"),
    ("Angelrute-Geduld", "Eine grosse Angelrute steht schraeg in einer Rutenhalterung am "
     "Ufer, die Schnur haengt locker ins ruhige Wasser",
     "Geduld siegt.", "Angler, die die Ruhe am Wasser geniessen", "Angeln",
     "Olivgruen, Silbergrau, Dunkelblau"),
    ("Gitarre-Lagerfeuer", "Eine grosse akustische Gitarre lehnt an einem kleinen Baumstumpf, "
     "eine einzelne Note schwebt ueber dem Klangloch",
     "Eigene Melodie.", "Hobbymusiker, die am liebsten draussen spielen", "Gitarre",
     "Holzbraun, Creme, Anthrazit"),
    ("Skateboard-Tempo", "Ein grosses Skateboard steht leicht angekippt mit sichtbaren "
     "Rollen, eine kurze Bewegungslinie deutet Tempo an",
     "Volles Tempo.", "Skater, die jede freie Minute auf dem Board verbringen", "Skateboard",
     "Anthrazit, Signalrot, Hellgrau"),
    ("Fahrradkorb-Blumen", "Ein grosser Fahrradkorb aus Weidengeflecht, gefuellt mit drei "
     "einfachen Wiesenblumen, am Lenker befestigt",
     "Langsamer fahren.", "Fahrradfans mit Vorliebe fuer entschleunigte Touren", "Fahrrad",
     "Weidenbraun, Wiesengruen, Mohnrot"),
)

ANZAHL = len(_EINTRAEGE)


def _bauen(e: _Eintrag) -> trends.Trend:
    thema, motiv, text, ziel, suchwort, farben = e
    aufbau = "motiv" if text else "nur_motiv"
    schluss = ("Gross und zentral als klarer Blickfang, freigestellt, geschlossene Silhouette, "
               "viel Freiraum" + ("; darunter klein ein kurzer Schriftzug." if text else "; kein Text."))
    return trends.Trend(
        thema=thema, kategorie=KATEGORIE, warum=_WARUM, zeitraum=_ZEITRAUM,
        zielgruppe=ziel,
        kaufmoment=(f"Freunde oder Familie verschenken es zum Geburtstag oder zu Weihnachten, "
                    f"weil sich die Person im Motiv sofort wiedererkennt."),
        verkaufswinkel=(f"Ein starkes Bild zum Thema {suchwort} traegt das Motiv, der kurze Text "
                        "pointiert es nur" if text else
                        f"Ruhiges, hochwertiges Bildmotiv zum Thema {suchwort} ganz ohne Text"),
        motiv=f"{motiv}. {schluss}", stil=_STIL,
        farben=[f.strip() for f in farben.split(",")], spruch=text,
        produkt=_PRODUKT, druckhinweis=_DRUCK, risiko=_RISIKO,
        suchbegriffe=[f"{suchwort} Shirt", f"{suchwort} T-Shirt Motiv", f"Geschenk {suchwort}"],
        quellen=[], gruppe=GRUPPE, aufbau=aufbau)


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
