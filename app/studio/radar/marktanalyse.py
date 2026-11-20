"""Marktanalyse: was sich bei eBay WIRKLICH verkauft - ueber viele Verkaeufer hinweg.

Das Motiv-Radar (``dienst.py``) liest EINEN Shop. Hier geht es breiter: zu einem
Suchbegriff (z. B. "Fussball T-Shirt") liefert eBay Treffer von vielen
Verkaeufern, gefiltert auf TATSAECHLICH VERKAUFTE Artikel (``LH_Sold=1`` -
das beste Signal, das eBay hergibt, und das einzige, das eine Anmeldung im
Browser-Profil verlangt, siehe ``ernte.py``).

Die Treffer werden NICHT direkt als Motiv-Ideen abgelegt - sie sind nur der
Marktbeleg. Was daraus wird, entscheidet ``trends.py``: Der Websuche-Auftrag
bekommt diese Liste als zusaetzlichen, echten Nachfragebeleg dazu und muss
trotzdem ein EIGENES, unterscheidbares Motiv entwerfen (dieselbe Regel wie
immer: nie der Wortlaut, nie die Gestaltung eines fremden Treffers).
"""
from __future__ import annotations

import logging
from urllib.parse import quote_plus

from app.studio.radar.ernte import ErnteFehler, Fund, ernte
from app.studio.radar.quellen import Quelle

logger = logging.getLogger("app.studio.radar.marktanalyse")

TOP_JE_BEGRIFF = 5


def suche_quelle(suchbegriff: str) -> Quelle:
    """Eine eBay-Suche ueber ALLE Verkaeufer als Quelle - kein einzelner Shop."""
    begriff = suchbegriff.strip()
    url = f"https://www.ebay.de/sch/i.html?_nkw={quote_plus(begriff)}&_ipg=240&_sop=12"
    return Quelle("ebay", f"suche:{begriff}", url)


async def beobachte(suchbegriffe: list[str], *, limit_je_begriff: int = 60) -> dict:
    """Je Suchbegriff die meistverkauften Treffer holen. Ein Fehlschlag stoppt nicht alles."""
    beobachtungen: list[dict] = []
    fehler: list[dict] = []
    for begriff in suchbegriffe:
        try:
            funde: list[Fund] = await ernte(suche_quelle(begriff), limit=limit_je_begriff,
                                            nur_verkauft=True)
        except ErnteFehler as exc:
            fehler.append({"suchbegriff": begriff, "grund": str(exc)})
            continue
        mit_zahl = sorted((f for f in funde if f.verkauft is not None),
                          key=lambda f: f.verkauft, reverse=True)
        beobachtungen.append({
            "suchbegriff": begriff,
            "treffer": [{"titel": f.titel, "verkauft": f.verkauft, "url": f.url}
                       for f in mit_zahl[:TOP_JE_BEGRIFF]],
            "insgesamt_gelesen": len(funde),
        })
    logger.info("marktanalyse beobachtet",
               extra={"begriffe": len(suchbegriffe), "fehler": len(fehler)})
    return {"beobachtungen": beobachtungen, "fehler": fehler}


def marktkontext(beobachtungen: list[dict]) -> str:
    """Die Beobachtungen als Text fuer den Websuche-Auftrag - Beleg, kein Vorbild."""
    zeilen = []
    for b in beobachtungen:
        if not b["treffer"]:
            continue
        zeilen.append(f"„{b['suchbegriff']}" + '" - meistverkauft gerade:')
        for t in b["treffer"]:
            zeilen.append(f'  - "{t["titel"]}" ({t["verkauft"]}+ verkauft)')
    if not zeilen:
        return ""
    return (
        "ECHTE MARKTBEOBACHTUNG (eigene eBay-Recherche, tatsaechlich verkaufte Artikel "
        "mehrerer fremder Verkaeufer - NUR als Nachfragebeleg, niemals Titel, Spruch oder "
        "Gestaltung uebernehmen oder nachahmen):\n" + "\n".join(zeilen) +
        "\n\nLeite daraus ab, WARUM diese Nische kauft, und entwirf ein eigenstaendiges, "
        "klar unterscheidbares Motiv dafuer - keine Kopie und kein austauschbares "
        "Abwandeln des Gesehenen."
    )
