"""Tier-Kollektion: reine Tiermotive, einmal realistisch, einmal animiert.

Wunsch des Betreibers (20.11.2026), woertlich: "realistische und animierte
tiere motive erstellen zb da soll nur das tier sein". Zwei Gruppen innerhalb
derselben Kategorie (``funshirt``, damit sie im Studio neben den anderen
Sammlungen stehen):

* "Tier realistisch" - naturgetreue Illustration, keine Comic-Vereinfachung.
* "Tier animiert" - Cartoon-/Animationsstil, flache Farben, klare Konturen.

Beide Gruppen sind reine Motive (``aufbau="nur_motiv"``): kein Text, kein
Spruch, nur das Tier, freigestellt. Keine bekannte Figur, kein Maskottchen,
keine Comicfigur einer Marke - nur das Tier selbst.

Gleiche Qualitaets- und Rechtepruefung wie die Websuche (``trends.speichere``).
Laden kostet nichts; Geld kostet erst "Motiv erzeugen".
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable

from app.studio.radar import trends

KATEGORIE = "funshirt"
GRUPPE_REALISTISCH = "Tier realistisch"
GRUPPE_ANIMIERT = "Tier animiert"

_STIL_REALISTISCH = ("Naturgetreue, detailreiche Tier-Illustration im Stil einer "
                     "hochwertigen Naturdokumentation: echte Fellstruktur, echte "
                     "Anatomie, keine vereinfachten Formen, keine vermenschlichte Mimik")
_STIL_ANIMIERT = ("Flacher, moderner Animationsstil wie in einem zeitgenoessischen "
                  "Trickfilm: vereinfachte runde Formen, klare dicke Konturlinien, "
                  "wenige flaechige Farben, grosse ausdrucksstarke Augen, freundliche "
                  "Mimik - erkennbar gezeichnet, kein Foto")
_DRUCK = ("Das Tier allein, freigestellt, geschlossene Silhouette, kraeftige Konturen, "
          "keine haarfeinen Linien, damit es auch auf Brustgroesse sauber druckt")
_RISIKO = ("Nur das Tier selbst, keine bekannte Zeichentrickfigur, kein Maskottchen "
           "und kein Logo-Tier einer Marke")
_ZEITRAUM = "Immergruen, Spitzen zu Geburtstagen und Weihnachten"
_WARUM_REALISTISCH = ("Naturgetreue Tiermotive sprechen Tierliebhaber an, die ein "
                      "hochwertiges, erwachsenes Bild statt eines Comics wollen.")
_WARUM_ANIMIERT = ("Animierte Tiermotive wirken verspielt und zugaenglich - ein "
                   "klassisches, nie aus der Mode kommendes Fun-Shirt-Thema.")
_PRODUKT = "T-Shirt, alternativ Hoodie oder Tasse"

# Je Eintrag: (thema, tier-beschreibung, zielgruppe, suchwort, farben)
_Eintrag = tuple[str, str, str, str, str]

_REALISTISCH: tuple[_Eintrag, ...] = (
    ("Fuchs-Realistisch", "Ein Rotfuchs sitzt aufrecht und aufmerksam, der buschige "
     "Schwanz um die Pfoten gelegt, der Blick leicht zur Seite gerichtet",
     "Naturliebhaber, die echte Tierportraets statt Comics tragen", "Fuchs",
     "Fuchsrot, Weissgrau, Anthrazit"),
    ("Wolf-Realistisch", "Ein grauer Wolf steht im Halbprofil, der Blick konzentriert "
     "nach vorn, das Fell dicht und mehrschichtig gezeichnet",
     "Wildtier- und Wolfsfans", "Wolf", "Graubraun, Weiss, Anthrazit"),
    ("Eule-Realistisch", "Eine Schleiereule sitzt mit ausgebreiteten Fluegeln auf einem "
     "kahlen Ast, der herzfoermige Gesichtsschleier klar gezeichnet",
     "Vogelbeobachter und Eulenfans", "Eule", "Cremeweiss, Goldbraun, Anthrazit"),
    ("Pferd-Realistisch", "Ein galoppierendes Pferd von der Seite, Maehne und Schweif "
     "im Wind, die Muskulatur klar modelliert",
     "Reiter und Pferdefans", "Pferd", "Kastanienbraun, Schwarz, Weiss"),
    ("Tiger-Realistisch", "Ein liegender Tiger von schraeg oben, der Kopf erhoben, das "
     "Streifenmuster praezise und symmetrisch",
     "Grosskatzen- und Raubtierfans", "Tiger", "Orange, Schwarz, Weiss"),
    ("Elefant-Realistisch", "Ein afrikanischer Elefant im Halbprofil mit weit "
     "ausgestellten Ohren und erhobenem Ruessel, die Haut fein texturiert",
     "Safari- und Naturfans", "Elefant", "Grau, Anthrazit, Beige"),
    ("Hirsch-Realistisch", "Ein Rothirsch mit vollem Geweih steht erhoben zwischen "
     "Farnkraut, der Blick wachsam zur Seite",
     "Jaeger, Foerster und Waldfans", "Hirsch", "Rotbraun, Tannengruen, Anthrazit"),
    ("Delfin-Realistisch", "Ein Delfin springt in anmutigem Bogen aus dem Wasser, "
     "Wassertropfen spritzen seitlich ab",
     "Meeres- und Delfinfans", "Delfin", "Petrol, Silbergrau, Weiss"),
    ("Igel-Realistisch", "Ein Igel rollt sich halb zusammen zwischen Herbstlaub, "
     "jede einzelne Stachel fein gezeichnet",
     "Gartenfreunde und Igelfans", "Igel", "Braun, Senfgelb, Anthrazit"),
    ("Panda-Realistisch", "Ein sitzender Panda haelt einen Bambushalm, das "
     "schwarz-weisse Fellmuster naturgetreu gezeichnet",
     "Panda- und Zoofans", "Panda", "Schwarz, Weiss, Bambusgruen"),
    ("Pinguin-Realistisch", "Ein Kaiserpinguin steht aufrecht im Halbprofil, das "
     "Gefieder fein schattiert, der Schnabel leicht geoeffnet",
     "Polarfans und Pinguinliebhaber", "Pinguin", "Schwarz, Weiss, Orange"),
    ("Hase-Realistisch", "Ein Feldhase sitzt geduckt im hohen Gras, die Loeffel "
     "aufgestellt, das Fell fein texturiert",
     "Naturfreunde und Hasenliebhaber", "Hase", "Sandbraun, Weiss, Anthrazit"),
    ("Eichhoernchen-Realistisch", "Ein Eichhoernchen sitzt aufrecht auf einem Ast "
     "und haelt eine Nuss mit beiden Vorderpfoten, der buschige Schwanz hochgestellt",
     "Garten- und Waldfans", "Eichhoernchen", "Rotbraun, Creme, Anthrazit"),
    ("Waschbaer-Realistisch", "Ein Waschbaer sitzt aufrecht, die typische "
     "Gesichtsmaske naturgetreu schattiert, die Vorderpfoten zusammengelegt",
     "Naturfreunde und Waschbaer-Fans", "Waschbaer", "Graubraun, Schwarz, Creme"),
    ("Flamingo-Realistisch", "Ein Flamingo steht auf einem Bein im seichten "
     "Wasser, der lange Hals elegant gebogen, das Gefieder fein gezeichnet",
     "Fans exotischer Vogelmotive", "Flamingo", "Pink, Korallrot, Anthrazit"),
    ("Schildkroete-Realistisch", "Eine Meeresschildkroete schwimmt seitlich, der "
     "Panzer mit klar gezeichnetem Musterwerk, die Flossen ausgestreckt",
     "Meeres- und Naturfans", "Schildkroete", "Olivgruen, Sandbeige, Petrol"),
    ("Zebra-Realistisch", "Ein Zebra steht im Halbprofil, das Streifenmuster "
     "praezise und symmetrisch, die Maehne kurz und aufrecht",
     "Safari- und Afrikafans", "Zebra", "Schwarz, Weiss, Anthrazit"),
    ("Giraffe-Realistisch", "Eine Giraffe steht mit erhobenem Hals im Halbprofil, "
     "das Fleckenmuster fein und unregelmaessig gezeichnet",
     "Safari- und Zoofans", "Giraffe", "Ockergelb, Braun, Creme"),
    ("Erdmaennchen-Realistisch", "Ein Erdmaennchen steht aufrecht Wache haltend "
     "auf den Hinterbeinen, die Vorderpfoten vor der Brust",
     "Fans afrikanischer Wildtiere", "Erdmaennchen", "Sandbraun, Creme, Anthrazit"),
    ("Papagei-Realistisch", "Ein Ara sitzt seitlich auf einem Ast, das bunte "
     "Gefieder in klaren Federreihen, der Schnabel kraeftig gebogen",
     "Vogelliebhaber und Exotik-Fans", "Papagei", "Scharlachrot, Kobaltblau, Gelb"),
    ("Seepferdchen-Realistisch", "Ein Seepferdchen schwebt aufrecht im Wasser, "
     "der geringelte Schwanz um einen Seegrashalm gelegt",
     "Meeresfans und Aquarienfreunde", "Seepferdchen", "Korallgelb, Petrol, Creme"),
    ("Qualle-Realistisch", "Eine Qualle schwebt mit durchscheinendem Schirm und "
     "fein gewellten Tentakeln im freien Wasser",
     "Fans ruhiger Meeresmotive", "Qualle", "Lavendel, Petrol, Weiss"),
    ("Otter-Realistisch", "Ein Fischotter liegt auf dem Ruecken im Wasser und "
     "haelt einen kleinen Stein auf dem Bauch, das Fell nass gezeichnet",
     "Fans verspielter Wildtiere", "Otter", "Braun, Creme, Anthrazit"),
    ("Chamaeleon-Realistisch", "Ein Chamaeleon klammert sich seitlich an einen "
     "Ast, die Haut fein geschuppt, ein Auge nach vorn gerichtet",
     "Terraristik- und Exotik-Fans", "Chamaeleon", "Laubgruen, Ockergelb, Anthrazit"),
    ("Nashorn-Realistisch", "Ein Nashorn steht im Halbprofil, die Haut in tiefen "
     "Falten gezeichnet, das Horn kraeftig und leicht gebogen",
     "Safari- und Naturschutzfans", "Nashorn", "Steingrau, Anthrazit, Beige"),
    ("Kaenguru-Realistisch", "Ein Kaenguru steht aufrecht auf den Hinterbeinen "
     "gestuetzt, der Schwanz als dritte Stuetze, das Fell kurz und dicht",
     "Fans australischer Wildtiere", "Kaenguru", "Sandbraun, Creme, Anthrazit"),
    ("Lama-Realistisch", "Ein Lama steht im Halbprofil, der lange Hals aufrecht, "
     "das wollige Fell in groben Strähnen gezeichnet",
     "Fans von Anden-Tieren", "Lama", "Beige, Braun, Creme"),
    ("Biber-Realistisch", "Ein Biber sitzt am Ufer und haelt einen kleinen "
     "Ast mit beiden Pfoten, der flache Schwanz seitlich sichtbar",
     "Naturfreunde und Biberfans", "Biber", "Dunkelbraun, Creme, Anthrazit"),
    ("Luchs-Realistisch", "Ein Luchs sitzt aufrecht im Schnee, die Pinselohren "
     "deutlich erkennbar, das gefleckte Fell fein texturiert",
     "Fans heimischer Raubkatzen", "Luchs", "Sandbraun, Weiss, Anthrazit"),
    ("Schneeeule-Realistisch", "Eine Schneeeule sitzt auf einem Felsen, das "
     "weisse Gefieder mit feinen dunklen Sprenkeln gezeichnet",
     "Fans arktischer Vogelmotive", "Schneeeule", "Weiss, Hellgrau, Anthrazit"),
    ("Dachs-Realistisch", "Ein Dachs steht im Profil mit gesenktem Kopf, das "
     "markante schwarz-weisse Gesichtsmuster klar gezeichnet",
     "Wald- und Wildtierfans", "Dachs", "Graubraun, Weiss, Schwarz"),
)

_ANIMIERT: tuple[_Eintrag, ...] = (
    ("Fuchs-Animiert", "Ein runder, froehlicher Zeichentrick-Fuchs sitzt mit grossen "
     "Augen und einem breiten Laecheln, der Schwanz ringelt sich verspielt ein",
     "Jugendliche und Fans verspielter Tiermotive", "Fuchs cartoon",
     "Orange, Creme, Anthrazit"),
    ("Faultier-Animiert", "Ein cartoonhaftes Faultier haengt entspannt an einem Ast, "
     "mit halb geschlossenen Augen und einem verschmitzten Laecheln",
     "Fans von Entspannungs- und Faultier-Humor", "Faultier cartoon",
     "Graubraun, Hellgruen, Creme"),
    ("Pinguin-Animiert", "Ein runder Zeichentrick-Pinguin steht breitbeinig mit "
     "ausgebreiteten Fluegeln, grosse Kulleraugen, froehliche Mimik",
     "Kinder und Fans niedlicher Tiermotive", "Pinguin cartoon",
     "Schwarz, Weiss, Orange"),
    ("Katze-Animiert", "Eine runde Zeichentrick-Katze sitzt mit geschlossenen Augen "
     "zufrieden schnurrend, der Schwanz elegant um die Pfoten gelegt",
     "Katzenbesitzer, die verspielte statt realistische Motive moegen", "Katze cartoon",
     "Orange, Creme, Anthrazit"),
    ("Hund-Animiert", "Ein froehlicher Zeichentrick-Hund sitzt mit heraushaengender "
     "Zunge und wedelndem Schwanz, grosse treue Augen",
     "Hundebesitzer, die verspielte statt realistische Motive moegen", "Hund cartoon",
     "Rotbraun, Creme, Anthrazit"),
    ("Koala-Animiert", "Ein rundlicher Zeichentrick-Koala haelt sich an einem "
     "Eukalyptuszweig fest, grosse runde Ohren, verschlafenes Laecheln",
     "Fans niedlicher australischer Tiermotive", "Koala cartoon",
     "Grau, Weiss, Eukalyptusgruen"),
    ("Eisbaer-Animiert", "Ein runder Zeichentrick-Eisbaer sitzt mit ausgebreiteten "
     "Armen auf einer Eisscholle, breites freundliches Laecheln",
     "Fans verspielter Wintertier-Motive", "Eisbaer cartoon",
     "Weiss, Hellblau, Anthrazit"),
    ("Löwe-Animiert", "Ein junger Zeichentrick-Loewe sitzt stolz mit kleiner "
     "zerzauster Maehne, grosse ausdrucksstarke Augen",
     "Fans verspielter Safari-Motive", "Loewe cartoon",
     "Goldgelb, Beige, Anthrazit"),
    ("Hase-Animiert", "Ein runder Zeichentrick-Hase sitzt aufrecht mit langen "
     "Loeffelohren, die Pfoten vor der Brust zusammengelegt",
     "Fans niedlicher Fruehlings- und Ostermotive", "Hase cartoon",
     "Creme, Rosa, Anthrazit"),
    ("Waschbaer-Animiert", "Ein frecher Zeichentrick-Waschbaer sitzt mit schiefem "
     "Grinsen und erhobener Pfote, die typische Gesichtsmaske klar gezeichnet",
     "Fans frecher, verspielter Tiermotive", "Waschbaer cartoon",
     "Graubraun, Schwarz, Creme"),
    ("Pinguin-Animiert2", "Ein runder Zeichentrick-Pinguin rutscht froehlich auf "
     "dem Bauch, die Fluegel seitlich ausgestreckt, breites Laecheln",
     "Kinder und Fans verspielter Wintertiere", "Pinguin cartoon rutschend",
     "Schwarz, Weiss, Hellblau"),
    ("Hase-Animiert2", "Ein Zeichentrick-Hase haeltet in froher Pose einen "
     "kleinen Osterkorb, grosse glaenzende Augen",
     "Fans froehlicher Fruehlingsmotive", "Osterhase cartoon", "Creme, Gruen, Rosa"),
    ("Eichhoernchen-Animiert", "Ein rundliches Zeichentrick-Eichhoernchen sitzt "
     "mit aufgeblasenen Backen und haelt eine riesige Nuss",
     "Fans niedlicher Waldtier-Motive", "Eichhoernchen cartoon",
     "Rotbraun, Creme, Anthrazit"),
    ("Waschbaer-Animiert2", "Ein verschmitzter Zeichentrick-Waschbaer blinzelt "
     "mit einem Auge, die Pfoten hinter dem Ruecken versteckt",
     "Fans frecher Tiermotive", "Waschbaer frech cartoon", "Graubraun, Creme, Schwarz"),
    ("Flamingo-Animiert", "Ein runder Zeichentrick-Flamingo balanciert auf einem "
     "Bein mit ausgebreiteten Fluegeln, breites Laecheln",
     "Fans froehlicher Sommer-Tiermotive", "Flamingo cartoon", "Pink, Weiss, Gelb"),
    ("Schildkroete-Animiert", "Eine runde Zeichentrick-Schildkroete laechelt "
     "entspannt, der Panzer mit einfachen bunten Sechsecken gemustert",
     "Fans gemuetlicher Tiermotive", "Schildkroete cartoon", "Hellgruen, Gelb, Creme"),
    ("Loewe-Animiert2", "Ein kleiner Zeichentrick-Loewenjunges spielt mit dem "
     "eigenen Schwanz, grosse treuherzige Augen",
     "Fans niedlicher Safari-Motive", "Loewenjunges cartoon", "Goldgelb, Creme, Braun"),
    ("Zebra-Animiert", "Ein froehliches Zeichentrick-Zebra tänzelt seitlich, "
     "die Streifen in weichen runden Formen gezeichnet",
     "Fans froehlicher Safari-Motive", "Zebra cartoon", "Schwarz, Weiss, Rosa"),
    ("Giraffe-Animiert", "Eine Zeichentrick-Giraffe mit langem geschwungenem "
     "Hals laechelt breit, grosse Wimpern, runde Flecken",
     "Fans niedlicher Safari-Motive", "Giraffe cartoon", "Gelb, Braun, Creme"),
    ("Erdmaennchen-Animiert", "Ein freches Zeichentrick-Erdmaennchen steht "
     "Wache mit Sonnenbrille, breites Grinsen",
     "Fans frecher Tiermotive", "Erdmaennchen cartoon", "Sandbraun, Schwarz, Creme"),
    ("Papagei-Animiert", "Ein bunter Zeichentrick-Papagei sitzt schraeg auf "
     "einem Ast und singt mit weit geoeffnetem Schnabel",
     "Fans froehlicher, bunter Tiermotive", "Papagei cartoon", "Rot, Gruen, Gelb"),
    ("Seepferdchen-Animiert", "Ein rundes Zeichentrick-Seepferdchen schwimmt "
     "mit geschwungenem Schwanz und froehlichem Laecheln",
     "Fans niedlicher Meeresmotive", "Seepferdchen cartoon", "Gelb, Petrol, Creme"),
    ("Qualle-Animiert", "Eine runde Zeichentrick-Qualle mit geschwungenen "
     "Tentakeln und froehlichem Gesicht schwebt sanft",
     "Fans niedlicher Meeresmotive", "Qualle cartoon", "Rosa, Lavendel, Creme"),
    ("Otter-Animiert", "Ein verspielter Zeichentrick-Otter liegt auf dem Ruecken "
     "und jongliert mit einem kleinen Stein, breites Laecheln",
     "Fans verspielter Tiermotive", "Otter cartoon", "Braun, Creme, Hellblau"),
    ("Chamaeleon-Animiert", "Ein buntes Zeichentrick-Chamaeleon rollt die Zunge "
     "spielerisch aus, grosse drehbare Augen",
     "Fans bunter, verspielter Tiermotive", "Chamaeleon cartoon", "Gruen, Gelb, Pink"),
    ("Nashorn-Animiert", "Ein rundliches Zeichentrick-Nashorn laechelt breit, "
     "das Horn klein und abgerundet gezeichnet",
     "Fans niedlicher Safari-Motive", "Nashorn cartoon", "Grau, Rosa, Creme"),
    ("Nilpferd-Animiert", "Ein rundes Zeichentrick-Nilpferd schwebt vergnuegt im "
     "Wasser, nur Augen und Ohren ragen heraus, breites Laecheln",
     "Fans niedlicher Flusstier-Motive", "Nilpferd cartoon", "Graublau, Rosa, Creme"),
    ("Kaenguru-Animiert", "Ein froehliches Zeichentrick-Kaenguru hupft mit einem "
     "Jungen im Beutel, grosse treue Augen",
     "Fans niedlicher Tierfamilien-Motive", "Kaenguru cartoon", "Sandbraun, Creme, Rosa"),
    ("Lama-Animiert", "Ein freches Zeichentrick-Lama streckt die Zunge raus, "
     "wolliges Fell in weichen runden Buescheln",
     "Fans frecher, verspielter Tiermotive", "Lama cartoon", "Beige, Pink, Creme"),
    ("Biber-Animiert", "Ein geschaeftiger Zeichentrick-Biber traegt einen "
     "viel zu grossen Ast mit stolzem Laecheln",
     "Fans verspielter Waldtier-Motive", "Biber cartoon", "Braun, Creme, Gruen"),
    ("Faultier-Animiert2", "Ein winkendes Zeichentrick-Faultier haengt kopfueber "
     "von einem Ast, traeumerisches Laecheln",
     "Fans entspannter Tiermotive", "Faultier winkend cartoon", "Graubraun, Hellgruen, Creme"),
)

ANZAHL = len(_REALISTISCH) + len(_ANIMIERT)


def _bauen(e: _Eintrag, *, gruppe: str, stil: str, warum: str) -> trends.Trend:
    thema, tier, ziel, suchwort, farben = e
    motiv = (f"{tier}. Nur das Tier, gross und zentral als klarer Blickfang, "
             "freigestellt, geschlossene Silhouette, viel Freiraum, kein Text und "
             "keine Buchstaben im Bild.")
    return trends.Trend(
        thema=thema, kategorie=KATEGORIE, warum=warum, zeitraum=_ZEITRAUM,
        zielgruppe=ziel,
        kaufmoment="Tierliebhaber erkennen sich im Motiv wieder oder verschenken es.",
        verkaufswinkel=f"Reines Tiermotiv zum Thema {suchwort} ganz ohne Text",
        motiv=motiv, stil=stil, farben=[f.strip() for f in farben.split(",")],
        spruch="", produkt=_PRODUKT, druckhinweis=_DRUCK, risiko=_RISIKO,
        suchbegriffe=[f"{suchwort} Shirt", f"{suchwort} T-Shirt Motiv",
                      f"Geschenk {suchwort}"],
        quellen=[], gruppe=gruppe, aufbau="nur_motiv")


def eintraege() -> list[trends.Trend]:
    return (
        [_bauen(e, gruppe=GRUPPE_REALISTISCH, stil=_STIL_REALISTISCH,
                warum=_WARUM_REALISTISCH) for e in _REALISTISCH]
        + [_bauen(e, gruppe=GRUPPE_ANIMIERT, stil=_STIL_ANIMIERT,
                  warum=_WARUM_ANIMIERT) for e in _ANIMIERT]
    )


def lade(db: Any, *, filter_check: Callable[[str], Any] | None = None,
         heute: date | None = None) -> dict:
    """Kollektion als Empfehlungen ablegen. Kostenlos; mehrfaches Laden verdoppelt nichts."""
    bericht = trends.speichere(
        db, eintraege(), belege=[], angebote={},
        filter_check=filter_check or trends._schutzfilter_check,
        heute=heute or date.today(), erwartete_kategorie=KATEGORIE)
    bericht["kosten_usd"] = 0.0
    return bericht
