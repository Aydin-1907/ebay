"""gpt-image-2 lehnt background=transparent ab - Freistellung per Chroma-Key."""
from __future__ import annotations

import base64
import sys
import types
from io import BytesIO

import pytest
from PIL import Image

from app.studio.generation.base import ImageRequest
from app.studio.generation.openai_provider import OpenAIProvider, _chroma_entfernen


def _magenta_bild_mit_rotem_kreis() -> Image.Image:
    bild = Image.new("RGB", (40, 40), (255, 0, 255))
    for x in range(10, 30):
        for y in range(10, 30):
            bild.putpixel((x, y), (200, 20, 20))
    return bild


def test_chroma_entfernen_macht_rand_transparent_motiv_bleibt():
    bild = _magenta_bild_mit_rotem_kreis()
    frei = _chroma_entfernen(bild)
    assert frei.getpixel((0, 0))[3] == 0          # Rand (Chroma) ist weg
    assert frei.getpixel((20, 20)) == (200, 20, 20, 255)  # Motiv unveraendert


def test_chroma_verschwindet_auch_mitten_im_bild_nicht_nur_am_rand():
    # Ein duenner magentafarbener Fringe um eine Textkante (echter Fund,
    # 17.11.2026) ist mit dem Rand NICHT verbunden - muss trotzdem weg.
    bild = Image.new("RGB", (40, 40), (0, 180, 0))
    for x in range(18, 22):
        for y in range(18, 22):
            bild.putpixel((x, y), (255, 0, 255))
    frei = _chroma_entfernen(bild)
    assert frei.getpixel((0, 0))[3] == 255        # echte Motivfarbe bleibt
    assert frei.getpixel((20, 20))[3] == 0        # Chroma-Fleck verschwindet trotzdem


def test_echte_motivfarbe_bleibt_auch_nah_am_rand_erhalten():
    bild = Image.new("RGB", (10, 10), (200, 20, 20))   # sattes Rot, weit von Magenta
    frei = _chroma_entfernen(bild)
    assert frei.getpixel((0, 0))[3] == 255


def _fake_openai(monkeypatch, bild: Image.Image):
    puffer = BytesIO()
    bild.save(puffer, "PNG")
    b64 = base64.b64encode(puffer.getvalue()).decode()
    gesehen = {}

    class _Bilder:
        def generate(self, **kw):
            gesehen.update(kw)
            return types.SimpleNamespace(data=[types.SimpleNamespace(b64_json=b64)])

    class _Client:
        def __init__(self, **kw):
            self.images = _Bilder()

        def close(self):
            pass

    monkeypatch.setitem(sys.modules, "openai", types.SimpleNamespace(OpenAI=_Client))
    return gesehen


def test_generate_fragt_opak_an_und_stellt_danach_selbst_frei(monkeypatch):
    gesehen = _fake_openai(monkeypatch, _magenta_bild_mit_rotem_kreis())

    ergebnis = OpenAIProvider("sk-test").generate(
        ImageRequest(prompt="Ein roter Kreis", width=1024, height=1024, transparent=True))

    assert gesehen["background"] == "opaque"
    assert "Chroma-Magenta" in gesehen["prompt"]
    assert ergebnis.image.getpixel((0, 0))[3] == 0


def test_generate_ohne_transparenzwunsch_laesst_bild_unveraendert(monkeypatch):
    gesehen = _fake_openai(monkeypatch, _magenta_bild_mit_rotem_kreis())

    ergebnis = OpenAIProvider("sk-test").generate(
        ImageRequest(prompt="Ein roter Kreis", width=1024, height=1024, transparent=False))

    assert gesehen["background"] == "opaque"
    assert "Chroma-Magenta" not in gesehen["prompt"]
    assert ergebnis.image.getpixel((0, 0))[3] == 255   # nichts freigestellt
