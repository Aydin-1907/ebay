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
