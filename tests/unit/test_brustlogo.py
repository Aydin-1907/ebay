"""Icon-Motive (random_kollektion) kommen klein als Brustlogo, nicht gross mittig.

Nutzerwunsch (20.11.2026), woertlich: "wenn du die auf ebay einstellt und
motiv fuer dich bearbeitest ... soll nicht wie bei den anderen motiven
zentral in der mitte sein sondern als brust logo link in 8 cm groesse ...
aber nur bei diesen random motiven."
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from PIL import Image

from app.studio.postprocess.umrechner import FormatFehler, platziere_brustlogo, zielformat
from app.studio.produktweg import BRUSTLOGO_BREITE_CM, _ist_brustlogo_motiv, erzeuge_druckdatei
from app.studio.radar.random_kollektion import GRUPPE as ICON_GRUPPE


def _icon_bild(seite: int = 1536) -> Image.Image:
    """Ein einfaches, undurchsichtiges Quadrat als Ersatz fuer ein echtes Icon."""
    img = Image.new("RGBA", (seite, seite), (0, 0, 0, 0))
    rand = seite // 20
    mitte = Image.new("RGBA", (seite - 2 * rand, seite - 2 * rand), (255, 128, 0, 255))
    img.paste(mitte, (rand, rand))
    return img


def test_brustlogo_landet_klein_und_nicht_mittig():
    ziel = zielformat("textil")
    ergebnis = platziere_brustlogo(_icon_bild(), ziel, breite_cm=8.0)
    assert ergebnis.size == ziel.groesse

    kasten = ergebnis.getbbox()
    assert kasten is not None
    breite_motiv = kasten[2] - kasten[0]
    # 8 cm bei 15 Zoll Druckbreite (4500 px) sind deutlich schmaler als die
    # Leinwand - das Motiv darf nicht die ganze Breite einnehmen wie bei
    # platziere() (zentriert, volle Groesse).
    assert breite_motiv < ziel.breite * 0.3

    mitte_motiv_x = (kasten[0] + kasten[2]) / 2
    # Nicht zentriert: der Mittelpunkt liegt rechts der Bildmitte (= links auf
    # der getragenen Brust) und oben in der oberen Haelfte.
    assert mitte_motiv_x > ziel.breite * 0.55
    mitte_motiv_y = (kasten[1] + kasten[3]) / 2
    assert mitte_motiv_y < ziel.hoehe * 0.4


def test_brustlogo_bricht_ab_wenn_motiv_zu_klein_fuer_die_groesse_ist():
    winzig = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    kern = Image.new("RGBA", (30, 30), (255, 0, 0, 255))
    winzig.paste(kern, (10, 10))
    with pytest.raises(FormatFehler):
        platziere_brustlogo(winzig, "textil", breite_cm=8.0)


def test_erkennt_icon_kollektion_ueber_die_gruppe_in_meta_json():
    design_icon = SimpleNamespace(meta_json=json.dumps({
        "radar": {"beschreibung": {"gruppe": ICON_GRUPPE}}}))
    design_anderes = SimpleNamespace(meta_json=json.dumps({
        "radar": {"beschreibung": {"gruppe": "Motiv groß, Text klein"}}}))
    design_ohne_meta = SimpleNamespace(meta_json=None)

    assert _ist_brustlogo_motiv(design_icon) is True
    assert _ist_brustlogo_motiv(design_anderes) is False
    assert _ist_brustlogo_motiv(design_ohne_meta) is False


def test_erzeuge_druckdatei_nimmt_den_brustlogo_weg_fuer_icon_motive(tmp_path):
    bildordner = tmp_path
    datei = bildordner / "icon-test.png"
    _icon_bild().save(datei)

    design = SimpleNamespace(
        id=1, image_url=f"/studio/bilder/{datei.name}",
        meta_json=json.dumps({"radar": {"beschreibung": {"gruppe": ICON_GRUPPE}}}))

    ziel = erzeuge_druckdatei(design, produkttyp_key="tshirt", bildordner=bildordner)
    assert ziel.name.endswith("__brustlogo.png")
    with Image.open(ziel) as fertig:
        kasten = fertig.getbbox()
    assert kasten is not None
    breite_motiv = kasten[2] - kasten[0]
    assert breite_motiv < fertig.width * 0.3


def test_erzeuge_druckdatei_lehnt_brustlogo_fuer_tasse_ab(tmp_path):
    bildordner = tmp_path
    datei = bildordner / "icon-test.png"
    _icon_bild().save(datei)
    design = SimpleNamespace(
        id=2, image_url=f"/studio/bilder/{datei.name}",
        meta_json=json.dumps({"radar": {"beschreibung": {"gruppe": ICON_GRUPPE}}}))

    from app.studio.produktweg import MotivFehler

    with pytest.raises(MotivFehler):
        erzeuge_druckdatei(design, produkttyp_key="mug", bildordner=bildordner)
