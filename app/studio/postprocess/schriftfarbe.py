"""Weisse Schrift fuer dunkle Shirts, schwarze Schrift fuer das weisse Shirt.

Vorgabe des Betreibers (18.09.2026): Die Schrift ist immer weiss - nur auf dem
weissen Shirt ist sie schwarz. Das Bildmodell bekommt deshalb die Anweisung, den
Schriftzug reinweiss zu setzen (``SCHRIFTREGEL``), das Motiv aber ohne Weiss.
Fuer das weisse Shirt entsteht aus derselben Datei eine Fassung, in der alle
weissen Pixel dunkel sind. Es wird nichts neu erzeugt und nichts bezahlt.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

SCHRIFTREGEL = (
    "Der Schriftzug steht in kraeftiger, sehr gut lesbarer Druckschrift "
    "(serifenlose Blockschrift, Versalien, gleichmaessige Strichstaerke), "
    "keine Schreibschrift, keine Handschrift, keine Kalligrafie, keine "
    "verspielten Buchstaben. Die Schriftfarbe ist reines Weiss (#FFFFFF). "
    "Das kleine Motiv verwendet kein Weiss."
)

DUNKEL = (17, 17, 17)
#: Ab dieser Helligkeit (und darunter liegender Saettigung) gilt ein Pixel als "weiss".
_HELL = 200
_SAETTIGUNG = 40

#: Fund 14.11.2026: Der Tausch griff nur bei EXAKT "#FFFFFF"/"white" - "Sand"
#: (#D6C4A6, siehe ``mockup_plan.FARBEN``) und jede helle Printify-Variante ausser
#: "White" bekamen weiterhin die weisse Schrift und waren darauf schlecht lesbar.
#: Jetzt entscheidet die WAHRGENOMMENE HELLIGKEIT der Ware, nicht der Name.
HELLIGKEITS_SCHWELLE = 170

#: Namen heller Printify-Varianten, die KEINEN Hex-Wert mitliefern (nur den Titel,
#: siehe ``printify/factory.ist_weisse_variante``). Teilstring-Treffer, Gross-/
#: Kleinschreibung egal. Ergaenzen, sobald ein neuer Blueprint eine weitere helle
#: Farbe anbietet - lieber eine Zeile mehr hier als eine weisse Schrift auf Sand.
HELLE_FARBNAMEN: frozenset[str] = frozenset({
    "white", "natural", "sand", "cream", "ivory", "bone", "ash", "silver",
    "light grey", "light gray", "beige", "vanilla", "oatmeal", "stone", "weiß",
})


def _helligkeit(rgb: tuple[int, int, int]) -> float:
    """Wahrgenommene Helligkeit 0-255 (ITU-R BT.601)."""
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b


def ist_helle_farbe(hex_farbe: str, *, schwelle: int = HELLIGKEITS_SCHWELLE) -> bool:
    """Braucht diese Farbe die dunkle Schrift-Fassung? Nach Helligkeit, nicht nach Name."""
    h = (hex_farbe or "").lstrip("#")
    if len(h) != 6:
        return False
    try:
        rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return False
    return _helligkeit(rgb) >= schwelle


def ist_heller_farbname(name: str) -> bool:
    """Dasselbe fuer Varianten, von denen nur ein Name (kein Hex) vorliegt."""
    n = (name or "").strip().lower()
    return any(schluessel in n for schluessel in HELLE_FARBNAMEN)


def dunkle_fassung_pfad(quelle: Path) -> Path:
    return quelle.with_name(f"{quelle.stem}-schwarzschrift.png")


def dunkle_fassung(quelle: Path) -> Path:
    """Legt neben ``quelle`` die Fassung mit dunkler statt weisser Schrift ab.

    Aus der Quelle wird nichts veraendert. Liegt die Fassung schon und ist
    juenger als die Quelle, wird sie wiederverwendet.
    """
    ziel = dunkle_fassung_pfad(quelle)
    if ziel.is_file() and ziel.stat().st_mtime >= quelle.stat().st_mtime:
        return ziel
    with Image.open(quelle) as roh:
        rgba = np.array(roh.convert("RGBA"))
    rgb = rgba[..., :3].astype(np.int16)
    hell = rgb.min(axis=-1) >= _HELL
    blass = (rgb.max(axis=-1) - rgb.min(axis=-1)) <= _SAETTIGUNG
    weiss = hell & blass
    rgba[weiss, 0], rgba[weiss, 1], rgba[weiss, 2] = DUNKEL
    Image.fromarray(rgba, "RGBA").save(ziel, "PNG")
    return ziel
