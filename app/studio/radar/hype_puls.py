"""Hype-Puls: was Deutschland GERADE sucht und liest - kostenlos, ohne Schluessel.

Wunsch des Betreibers (20.11.2026): Die Empfehlungen sollen trendbasiert sein.
Beispiel: GTA 6 erscheint, alle reden davon - und das Radar schlaegt trotzdem nur
allgemeine Gaming-Kultur vor. Die Websuche in ``trends.py`` findet den Hype nicht
zuverlaessig von selbst; sie braucht einen gemessenen Ausgangspunkt.

Drei kostenlose Quellen, keine davon braucht einen Key:

1. **Google Trends "Jetzt im Trend"** (RSS, Deutschland). Liefert die Suchbegriffe,
   die gerade steil gehen, mit Googles eigener Groessenangabe ("500+", "20.000+").
2. **Wikipedia-Seitenaufrufe** (Wikimedia REST, de.wikipedia, gestern). Die
   meistgelesenen Artikel mit der echten Aufrufzahl.
3. **Anlass-Kalender** (lokal berechnet): Feiertage und Geschenkanlaesse der
   naechsten Wochen, mit dem Tag, an dem man spaetestens listen sollte.

Danach wird jedes Thema eingeordnet - eine Ampel, keine Punktzahl:

* ``frei``         - darf als Thema direkt verwendet werden.
* ``geschuetzt``   - Marke, Spiel, Film, Figur (Rechtefilter schlaegt an). Der Hype
                     darf nur ueber das allgemeine Lebensgefuehl genutzt werden; Name,
                     Logo, Cover, Figuren und Schauplaetze bleiben draussen. Genau das
                     ist der Fall "GTA 6": Ein Shirt mit dem Cover waere eine VeRO-
                     Meldung und eine Abmahnung, ein eigenes 80er-Neon-Motiv nicht.
* ``ungeeignet``   - Unglueck, Tod, Verbrechen, Politik, Wahlen. Fliegt raus.

**Keine erfundenen Zahlen** (Eiserne Regel 3): Es stehen nur die Werte da, die die
Quelle selbst nennt. Es gibt keinen ausgedachten "Hype-Score". Faellt eine Quelle
aus, fehlt sie - der Lauf geht ohne sie weiter.
"""
from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from typing import Any
from urllib.parse import quote

logger = logging.getLogger("app.studio.radar.hype_puls")

GOOGLE_TRENDS_RSS = "https://trends.google.de/trending/rss?geo=DE"
WIKIPEDIA_TOP = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
                 "de.wikipedia.org/all-access/{jahr}/{monat:02d}/{tag:02d}")
# Wikimedia verlangt einen erkennbaren User-Agent, sonst 403.
USER_AGENT = "PODShop-HypePuls/1.0 (Medienwerk; privates Werkzeug)"

VORSCHAU_WOCHEN = 8
MAX_GOOGLE = 20
MAX_WIKIPEDIA = 15

FREI = "frei"
GESCHUETZT = "geschuetzt"
UNGEEIGNET = "ungeeignet"

# Themen, an denen kein Shirt verdient werden soll. Bewusst grob: lieber ein
# harmloses Thema zu viel aussortieren als ein Unglueck bedrucken.
_UNGEEIGNET = re.compile(
    # Wortstaemme, die im Deutschen in Komposita stecken ("Bundestagswahl",
    # "Zugunglueck", "Messerangriff") - auch mitten im Wort.
    r"\w*(wahl|unfall|ungl[uü]ck|absturz|anschlag|attentat|terror|mord|krieg|"
    r"angriff|erdbeben|hochwasser|schie[sß]erei|festnahme|polizei|minister|kanzler)\w*"
    # Kurze Woerter nur als ganzes Wort, sonst trifft "tod" auch "Todesstern" usw.
    r"|\b(tot|tote|toten|tod|gestorben|stirbt|verstorben|t[oö]tung|messer|explosion|"
    r"brand|feuer|flut|verhaftet|prozess|urteil|gericht|vermisst|partei|bundestag|"
    r"regierung|afd|cdu|csu|spd|fdp|gr[uü]ne|linke|bsw)\b",
    re.IGNORECASE)

# Wikipedia-Seiten, die keine Themen sind.
_WIKI_RAUSCHEN = re.compile(
    r"^(Hauptseite|Spezial:|Special:|Datei:|Wikipedia:|Benutzer:|Kategorie:|Portal:|"
    r"Hilfe:|Vorlage:|Diskussion:|-$)")


@dataclass
class Hype:
    thema: str
    quelle: str                      # "google_trends" | "wikipedia" | "kalender"
    wert: str = ""                   # wie die Quelle ihn nennt, z. B. "500+" oder "48.210 Aufrufe"
    kontext: str = ""                # Schlagzeile, Datum oder Kaufmoment
    url: str = ""
    ampel: str = FREI
    grund: str = ""                  # warum geschuetzt/ungeeignet
    datum: str = ""                  # nur Kalender: Tag des Anlasses (ISO)
    listen_bis: str = ""             # nur Kalender: spaetester sinnvoller Listing-Tag (ISO)


@dataclass
class HypeBericht:
    stand: str
    hypes: list[Hype] = field(default_factory=list)
    fehler: list[dict] = field(default_factory=list)

    def nutzbar(self) -> list[Hype]:
        return [h for h in self.hypes if h.ampel != UNGEEIGNET]

    def als_dict(self) -> dict:
        return {"stand": self.stand, "hypes": [asdict(h) for h in self.hypes],
                "fehler": self.fehler}


# --------------------------------------------------------------------------- #
# Quellen lesen (reine Funktionen, netzwerkfrei testbar)
# --------------------------------------------------------------------------- #

def lies_google_trends(xml_text: str) -> list[Hype]:
    """Den Google-Trends-RSS zerlegen. Namensraum-unabhaengig, weil Google ihn wechselt."""
    try:
        wurzel = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    funde: list[Hype] = []
    for item in wurzel.iter("item"):
        titel = (item.findtext("title") or "").strip()
        if not titel:
            continue
        verkehr = schlagzeile = link = ""
        for kind in item.iter():
            tag = kind.tag.rsplit("}", 1)[-1]
            if tag == "approx_traffic" and not verkehr:
                verkehr = (kind.text or "").strip()
            elif tag == "news_item_title" and not schlagzeile:
                schlagzeile = (kind.text or "").strip()
            elif tag == "news_item_url" and not link:
                link = (kind.text or "").strip()
        funde.append(Hype(
            thema=titel[:120], quelle="google_trends",
            wert=f"{verkehr} Suchanfragen" if verkehr else "",
            kontext=schlagzeile[:200],
            url=link or f"https://trends.google.de/trends/explore?geo=DE&q={quote(titel)}"))
        if len(funde) >= MAX_GOOGLE:
            break
    return funde


def lies_wikipedia(daten: dict) -> list[Hype]:
    """Die meistgelesenen de.wikipedia-Artikel, ohne Verwaltungsseiten."""
    try:
        artikel = daten["items"][0]["articles"]
    except (KeyError, IndexError, TypeError):
        return []
    funde: list[Hype] = []
    for a in artikel:
        name = str(a.get("article") or "")
        if not name or _WIKI_RAUSCHEN.match(name):
            continue
        aufrufe = a.get("views")
        wert = f"{int(aufrufe):,} Aufrufe gestern".replace(",", ".") if aufrufe else ""
        funde.append(Hype(
            thema=name.replace("_", " ")[:120], quelle="wikipedia", wert=wert,
            url=f"https://de.wikipedia.org/wiki/{quote(name)}"))
        if len(funde) >= MAX_WIKIPEDIA:
            break
    return funde


# --------------------------------------------------------------------------- #
# Anlass-Kalender (lokal, ohne Netz)
# --------------------------------------------------------------------------- #

def ostersonntag(jahr: int) -> date:
    """Gaußsche Osterformel (anonymer gregorianischer Algorithmus)."""
    a = jahr % 19
    b, c = divmod(jahr, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    monat, tag = divmod(h + l_ - 7 * m + 114, 31)
    return date(jahr, monat, tag + 1)


def _nter_wochentag(jahr: int, monat: int, wochentag: int, n: int) -> date:
    """n-ter Wochentag (0=Mo) im Monat."""
    erster = date(jahr, monat, 1)
    versatz = (wochentag - erster.weekday()) % 7
    return erster + timedelta(days=versatz + 7 * (n - 1))


def _anlaesse(jahr: int) -> list[tuple[date, str, str]]:
    """(Datum, Anlass, Kaufmoment) fuer ein Jahr."""
    ostern = ostersonntag(jahr)
    weihnachten = date(jahr, 12, 25)
    erster_advent = weihnachten - timedelta(days=weihnachten.weekday() + 1 + 21)
    thanksgiving = _nter_wochentag(jahr, 11, 3, 4)
    return [
        (date(jahr, 1, 1), "Neujahr", "Vorsatz-Humor, Start ins neue Jahr"),
        (date(jahr, 2, 14), "Valentinstag", "Paargeschenk, Partnerlook"),
        (ostern - timedelta(days=52), "Weiberfastnacht / Karneval", "Kostuem-Ersatz, Gruppenshirts"),
        (date(jahr, 3, 8), "Weltfrauentag", "Geschenk unter Freundinnen und Kolleginnen"),
        (ostern, "Ostern", "Familiengeschenk, Kinder- und Elternshirts"),
        (_nter_wochentag(jahr, 5, 6, 2), "Muttertag", "Geschenk fuer Mama, Oma, Bonusmama"),
        (ostern + timedelta(days=39), "Vatertag (Christi Himmelfahrt)", "Bollerwagentour, Gruppenshirts"),
        (date(jahr, 8, 8), "Weltkatzentag", "Katzenhalter beschenken sich selbst"),
        (date(jahr, 10, 10), "Welthundetag", "Hundehalter-Geschenk"),
        (date(jahr, 10, 31), "Halloween", "Party-Outfit ohne Kostuem"),
        (thanksgiving + timedelta(days=1), "Black Friday", "Rabattwoche, Vorrat an Geschenken"),
        (erster_advent, "1. Advent", "Wichteln, Adventskalender-Kleinigkeit"),
        (date(jahr, 12, 6), "Nikolaus", "Kleines Geschenk, Tasse"),
        (date(jahr, 12, 24), "Weihnachten", "Hauptgeschenksaison, Familienlook"),
        (date(jahr, 12, 31), "Silvester", "Partyshirts, Jahresrueckblick-Humor"),
    ]


# Vorlauf fuer POD: Druck plus Versand dauern grob eine Woche; ein Listing braucht
# ausserdem ein paar Tage, bis es in der Suche anzieht.
VORLAUF_TAGE = 14


def kalender(heute: date, wochen: int = VORSCHAU_WOCHEN) -> list[Hype]:
    """Anlaesse von heute bis ``wochen`` voraus, naechster zuerst."""
    ende = heute + timedelta(weeks=wochen)
    funde: list[Hype] = []
    for jahr in (heute.year, heute.year + 1):
        for tag, name, kaufmoment in _anlaesse(jahr):
            if heute <= tag <= ende:
                listen_bis = max(heute, tag - timedelta(days=VORLAUF_TAGE))
                funde.append(Hype(
                    thema=name, quelle="kalender", wert=f"in {(tag - heute).days} Tagen",
                    kontext=kaufmoment, datum=tag.isoformat(),
                    listen_bis=listen_bis.isoformat()))
    return sorted(funde, key=lambda h: h.datum)


# --------------------------------------------------------------------------- #
# Einordnen
# --------------------------------------------------------------------------- #

def einordnen(hype: Hype, filter_check: Callable[[str], Any]) -> Hype:
    """Ampel setzen. Der Kalender ist immer frei - Feiertage gehoeren niemandem."""
    if hype.quelle == "kalender":
        return hype
    text = f"{hype.thema} {hype.kontext}"
    treffer = _UNGEEIGNET.search(text)
    if treffer:
        hype.ampel = UNGEEIGNET
        hype.grund = f"heikles Thema ({treffer.group(0)})"
        return hype
    pruefung = filter_check(hype.thema)
    if not getattr(pruefung, "allowed", True):
        hype.ampel = GESCHUETZT
        hype.grund = (getattr(pruefung, "reason", "") or "geschuetzter Name")[:160]
    return hype


def _doppelt_weg(hypes: list[Hype]) -> list[Hype]:
    gesehen: set[str] = set()
    raus: list[Hype] = []
    for h in hypes:
        k = re.sub(r"[^a-z0-9äöüß]+", "", h.thema.lower())
        if k and k not in gesehen:
            gesehen.add(k)
            raus.append(h)
    return raus


# --------------------------------------------------------------------------- #
# Abholen
# --------------------------------------------------------------------------- #

async def _hole_text(url: str) -> str:
    import httpx

    async with httpx.AsyncClient(timeout=15.0, headers={"User-Agent": USER_AGENT},
                                 follow_redirects=True) as client:
        antwort = await client.get(url)
        antwort.raise_for_status()
        return antwort.text


async def _hole_json(url: str) -> dict:
    import httpx

    async with httpx.AsyncClient(timeout=15.0, headers={"User-Agent": USER_AGENT},
                                 follow_redirects=True) as client:
        antwort = await client.get(url)
        antwort.raise_for_status()
        return antwort.json()


def _schutzfilter_check(text: str) -> Any:
    from app.studio.generation.service import _schutzfilter

    return _schutzfilter().check(text)


async def sammle(heute: date | None = None, *,
                 hole_text: Callable[[str], Awaitable[str]] | None = None,
                 hole_json: Callable[[str], Awaitable[dict]] | None = None,
                 filter_check: Callable[[str], Any] | None = None) -> HypeBericht:
    """Alle drei Quellen lesen und einordnen. Wirft nie - Ausfaelle stehen in ``fehler``."""
    heute = heute or date.today()
    hole_text = hole_text or _hole_text
    hole_json = hole_json or _hole_json
    filter_check = filter_check or _schutzfilter_check
    bericht = HypeBericht(stand=heute.isoformat())

    try:
        bericht.hypes.extend(lies_google_trends(await hole_text(GOOGLE_TRENDS_RSS)))
    except Exception as exc:  # noqa: BLE001 - eine Quelle darf den Puls nicht stoppen
        bericht.fehler.append({"quelle": "google_trends", "grund": str(exc)[:160]})

    gestern = heute - timedelta(days=1)
    try:
        bericht.hypes.extend(lies_wikipedia(await hole_json(WIKIPEDIA_TOP.format(
            jahr=gestern.year, monat=gestern.month, tag=gestern.day))))
    except Exception as exc:  # noqa: BLE001
        bericht.fehler.append({"quelle": "wikipedia", "grund": str(exc)[:160]})

    bericht.hypes.extend(kalender(heute))
    bericht.hypes = [einordnen(h, filter_check) for h in _doppelt_weg(bericht.hypes)]
    logger.info("hype-puls gesammelt", extra={
        "hypes": len(bericht.hypes), "nutzbar": len(bericht.nutzbar()),
        "fehler": len(bericht.fehler)})
    return bericht


# --------------------------------------------------------------------------- #
# Fuer die Websuche aufbereiten
# --------------------------------------------------------------------------- #

def marktkontext(bericht: HypeBericht, *, max_trends: int = 15) -> str:
    """Den Puls als Auftrag fuer ``trends.anweisung`` - gemessen, nicht erfunden."""
    aktuell = [h for h in bericht.nutzbar() if h.quelle != "kalender"][:max_trends]
    anlaesse = [h for h in bericht.nutzbar() if h.quelle == "kalender"]
    if not aktuell and not anlaesse:
        return ""
    zeilen = [f"AKTUELLER HYPE-PULS (heute gemessen, Stand {bericht.stand}):"]
    if aktuell:
        zeilen.append("Gerade stark gesucht oder gelesen in Deutschland:")
        for h in aktuell:
            teile = [h.thema]
            if h.wert:
                teile.append(h.wert)
            if h.kontext:
                teile.append(h.kontext)
            marke = " [GESCHUETZT: nur Lebensgefuehl]" if h.ampel == GESCHUETZT else ""
            zeilen.append(f"  - {' | '.join(teile)}{marke} ({h.url})")
    if anlaesse:
        zeilen.append("Anlaesse der naechsten Wochen (spaetestens listen bis):")
        for h in anlaesse:
            zeilen.append(f"  - {h.thema} am {h.datum}, listen bis {h.listen_bis}: {h.kontext}")
    zeilen.append(
        "\nSo nutzt du den Puls:\n"
        "- Mindestens die Haelfte der Empfehlungen muss erkennbar an einen Punkt aus dieser "
        "Liste andocken. Waehle die Hypes, zu denen die gewaehlte Kategorie wirklich passt und "
        "eine kaufbereite Zielgruppe existiert - nicht einfach den lautesten.\n"
        "- Bei [GESCHUETZT] (Spiele, Filme, Serien, Marken, Figuren): Der Name dient NUR "
        "intern als Nachfragebeleg. Niemals Titel, Logo, Cover, Figuren, Schauplatz- oder "
        "Fantasie-Ortsnamen aus dem Werk, typische UI-Elemente oder Zitate nennen oder "
        "nachahmen. Nutze stattdessen, was Fans gerade gemeinsam erleben und was niemandem "
        "gehoert: die allgemeine Stilepoche oder Aesthetik, das Ritual rund um den Release "
        "(Urlaub nehmen, Nacht durchzocken, lange Vorfreude) und Insider-Humor ohne Titel.\n"
        "- Personen, Unglueck, Politik und Verbrechen sind tabu, auch wenn sie im Puls stehen.\n"
        "- Nenne in 'warum' den Puls-Punkt mit seinem gemessenen Wert und setze seine URL in "
        "'quellen'. Erfinde keine weiteren Zahlen.\n"
        "- Bei Anlaessen: Das Verkaufsfenster endet am Anlass, nicht danach.")
    return "\n".join(zeilen)
