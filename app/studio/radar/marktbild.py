"""Marktbild je Kategorie: was auf dem Marktplatz gerade sichtbar verkauft wird.

Quelle: Spreadshirt-Suche ``https://www.spreadshirt.de/shop/s/<suchwort>``, vom
Betreiber als Beispiel vorgegeben (27.11.2026). Ausgewertet wurden die ersten rund 30
Designs je Suchwort: Titel, Shirtfarbe und Bildaufbau.

Festgehalten sind nur FORMATE (wie ein Motiv gebaut ist), nie Wortlaut. Die Sprueche
der fremden Shops sind deren Werk; uebernommen wird kein Satz und kein Wortspiel. Der
Auftrag an die Websuche sagt das ausdruecklich dazu.

Uebergreifend gilt fuer alle Suchwoerter: Der weit groesste Teil der vorn gezeigten
Designs sitzt auf schwarzer Ware, hell gedruckt - das passt zur Schwarz/Weiss-Linie.
"""
from __future__ import annotations

STAND = "27.11.2026"
QUELLE = "https://www.spreadshirt.de/shop/s/<suchwort>"

ALLGEMEIN = """\
- Auf dem Markt dominiert helle Schrift auf schwarzer Ware. Entwirf zuerst fuer Schwarz.
- Haeufigster Spruch-Aufbau: zentrierter Textblock in 2-4 Zeilen mit wechselnden
  Schriftgroessen, EIN Schluesselwort gross, dazu ein kleines Symbol.
- Wiederkehrende Formate, die sich verkaufen: Herzschlag-/EKG-Linie, die in ein Symbol
  des Hobbys uebergeht; Jahreszahl oder Alter als Aufhaenger (z. B. Abschluss oder Rente
  mit Jahr); Retro-Sonnenuntergang mit Silhouette; Wortspiel aus Hobby + Berufs- oder
  Rollenbezeichnung; Pseudo-Anleitung, Wochenplan oder ABC als Listenformat.
- Diese Formate sind Bauplaene. Wortlaut, Wortspiele und Bildideen fremder Shops werden
  NIE uebernommen oder abgewandelt - jeder Text ist neu und eigenstaendig."""

# Je Kategorie: was dort vorn steht.
KATEGORIE = {
    "rentner": """\
- Vorn: Ruhestands-Humor mit Jahreszahl (Rente + Jahr), der Wochenplan ohne Termine,
  Abschied aus dem Job als Ehrenrunde, Navigations- oder Ziel-erreicht-Gag, Hobby + Rente
  (Fahrrad, Angeln, Wohnmobil, Werkstatt). Fast nur schwarze Ware, Textblock mit Symbol.
- Kaufmoment ist fast immer der letzte Arbeitstag: Geschenk von Kollegen oder Familie.""",
    "fussball": """\
- Vorn: Herzschlag-Linie in Ball oder Spielerpose, freigestellte Spieler-Silhouette in
  Bewegung, Kreisliga- und Bolzplatz-Humor, Fussball + Bier, Abschied eines Spielers.
- Kein Verein, keine Vereinsfarben - der Markt zeigt, dass es auch ohne geht.""",
    "zeichen": """\
- Vorn: ein Kanji gross mit EINER Bildidee daneben (Kranich + rote Sonne, Oni-Maske,
  Welle, Katana), roter Akzent auf schwarzer Ware, Kampfkunst- und Bushido-Themen,
  Tugend-Zeichen (Harmonie, Weisheit, Leere) als ruhige Pinselschrift.""",
    "anime": """\
- Vorn: Kawaii und Chibi - niedliche Katzen und Tiere, Ramen, Dumplings, Kitsune-Masken,
  dazu Hobby-Bekenntnis mit kleinem Text. Japanische Alltagsobjekte als Motiv.""",
    "gothic": """\
- Vorn: Rabe oder Kraehe, Schaedel mit Rosen, Memento mori, Kreuz, Okkult-Vintage als
  Kupferstich- oder Linienzeichnung auf Schwarz. Gut laufen Brueche mit Alltag: dunkles
  Motiv + harmloser Gegenstand (z. B. Fledermaus mit Kaffeetasse).""",
    "astronomie": """\
- Vorn: detaillierte Mondkarte, Sonnensystem als Linie, Sternbild mit Namen, Teleskop
  unter Sternenhimmel, Astronomie-ABC, Hobby-Ausrede-Spruch. Zeitnah: die totale
  Sonnenfinsternis 2027 in Spanien wird schon als Reisemotiv verkauft.""",
    "sonntag": """\
- Vorn: Wochentag als reine Typografie, leere To-do-Liste, der fehlende Tag zwischen
  Sonntag und Montag, Akku-leer-Bild, Sonntag als Lieblingstag mit Herz.""",
    "videospiele": """\
- Vorn: Pixel-Art (Retro-8-Bit), Pause-Knopf-Ausrede, Gamer-Bekenntnis in grosser
  Typo, Tastatur- und Wuerfel-Symbole. Keine Spieltitel oder Konsolenlogos.""",
    "stadtliebe": """\
- Vorn: Skyline als Linie, Stadt + Herz, Koordinaten der Stadt, Dialektwort, Heimat-
  Bekenntnis. Wappen kommen auf dem Markt vor, bleiben hier trotzdem aus.""",
}

FUNSHIRT_GRUPPEN = {
    "Alltag": "Pseudo-Anleitung fuer den Alltag, Alltagsheld, ehrliches Selbstbild mit Augenzwinkern.",
    "Grillen": "Grillmeister-Rolle (Papa, Vatertag), Lizenz-/Ausweis-Format, Wortspiel Grill + Beruf, Herzschlag in Grillzange; Kochschuerze ist dort Hauptprodukt.",
    "Getraenke": "Bier mit Herzschlag, Bierglas-Evolution, Bier + Wochentag, Sixpack-Gag, Craft-Bier-Bekenntnis.",
    "Familie": "Herzschlag Familie, Tierfamilie (Baer, Elefant) als Eltern-Kind-Bild, Familien-Set im Partnerlook.",
    "Baby & Kinder": "Body mit Rollenspruch (Nachwuchs fuer das Hobby der Eltern), Befoerdert-zu-Format mit Jahr, kleines Tierbaby.",
    "Partnerschaft": "Partnerlook als Paar-Set (zwei Teile, die zusammen ein Bild ergeben), Jahrestag mit Jahreszahl.",
    "Haustiere": "Hund als Familie, Hund von hinten als Linie, Herrchen-/Frauchen-Gag, Hundeportrait mit Brille.",
    "Anlaesse": "Alter als grosse Zahl, runder Geburtstag mit Selbstironie, Jahrgangs-Format.",
    "Camping": "Wohnwagen oder Van als Zuhause, Camping-Team, Bus in den Bergen, Rentner-Camper.",
    "Angeln": "Retro-Sonnenuntergang mit Angler, Vollmond-Angler, Herzschlag in Angelschnur, Raubfisch als Trophaee, Norwegen-Trip.",
    "Wandern": "Herzschlag Berge, Abkuerzung/Umweg-Gag, Der-Berg-ruft-Format, Berglinie mit Gipfel.",
    "Reise & Haushalt": "Weltkarte/Globus, Retro-Reiseposter einer Landschaft, Fernweh-Bekenntnis.",
    "Nerd & Technik": "Fehler- und Code-Humor, KI-Gag, toter Pixel, Physik-Insider.",
    "Studium & Musik": "Abschluss mit Jahreszahl, Studienfach-Humor, Notenschluessel mit Herz, Instrument als Skizze, Kassette 80er.",
    "Regional": "Dialekt-ABC, Dialektausdruck gross, Heimat-Herzschlag, regionales Essen mit Charakter.",
    "Sternzeichen": "Sternzeichen-Tier halb realistisch, halb geometrisch, Symbol + Name, Sternbild-Linie.",
}


def fuer(kategorie: str) -> str:
    """Marktbild-Abschnitt fuer den Auftrag an die Websuche."""
    teile = [ALLGEMEIN]
    if kategorie == "funshirt":
        teile.append("Je Untergruppe:\n" + "\n".join(
            f"- {name}: {text}" for name, text in FUNSHIRT_GRUPPEN.items()))
    elif kategorie == "mix":
        teile.extend(KATEGORIE[k] for k in KATEGORIE if k not in ("rentner", "stadtliebe"))
    elif kategorie in KATEGORIE:
        teile.append(KATEGORIE[kategorie])
    return (f"MARKTBILD (Spreadshirt-Suche, Stand {STAND} - nur Formate, kein Wortlaut):\n"
            + "\n".join(teile))
