"""Bild-Anbieter GPT Image 2.

Starke Textwiedergabe und echte Transparenz - deshalb im Vorprojekt die erste
Wahl fuer Spruch- und Textmotive.

Uebernommen aus POD-Shop (src/pod/generation/openai_provider.py), mit zwei
Aenderungen:

* Kein Konfigurations-Objekt mehr im Konstruktor, sondern die zwei Werte, die
  wirklich gebraucht werden. So laesst sich der Anbieter testen, ohne die halbe
  Anwendung hochzufahren.
* Die Kosten werden gemeldet. Im Vorprojekt blieben sie leer, damit war die
  Kostenbremse auf diesen Anbieter blind.
"""

from __future__ import annotations

import base64
from io import BytesIO

import numpy as np
from PIL import Image

from app.studio.generation.base import SUPPORTED_SIZES, GeneratedImage, ImageRequest

_SIZE_ARG = {
    "square": "1024x1024",
    "portrait": "1024x1536",
    "landscape": "1536x1024",
}

# Fund 17.11.2026: "gpt-image-2" lehnt background="transparent" mit einer
# klaren 400-Antwort ab ("Transparent background is not supported for this
# model") - das alte "gpt-image-1" gibt es bei OpenAI nicht mehr. Statt
# Transparenz direkt zu verlangen, wird undurchsichtig auf einem reinen
# Chroma-Magenta erzeugt und die Farbe danach selbst herausgerechnet. Magenta,
# weil es in keiner im Studio verwendeten Motivfarbe vorkommt - anders als
# Gruen (Olivgruen u.a. ist eine gaengige Motivfarbe).
_CHROMA = (255, 0, 255)
_CHROMA_TEXT = (
    "Der Hintergrund ist eine einzige, vollkommen gleichmaessige Flaeche in "
    "reinem Chroma-Magenta (#FF00FF), randscharf zum Motiv, ohne Schatten, "
    "Verlauf oder Textur. Das Motiv selbst verwendet nirgends Magenta oder "
    "einen aehnlichen Pink-/Violettton."
)
#: Farbabstand (euklidisch im RGB-Raum, max. ca. 441). Innerhalb von KERN gilt
#: ein Pixel als sicher Chroma (alpha 0); zwischen KERN und SAUM nimmt die
#: Deckkraft weich zu - das entfernt auch den duennen magentafarbenen Rand-
#: Fringe um Textkanten, den ein reiner Flutfuellungs-Ansatz uebersah (Fund
#: 17.11.2026, echte Erzeugung: Eckfarbe lag bei (224, 12, 202), Abstand ~63,
#: Fringe um die Buchstaben naeher an Weiss, aber klar magentastichig).
#: Global statt nur vom Bildrand aus - unbedenklich, weil keine Motivfarbe im
#: Studio in Pink/Magenta liegt.
_CHROMA_KERN = 90
_CHROMA_SAUM = 170


def _chroma_entfernen(img: Image.Image) -> Image.Image:
    """Macht den magentafarbenen Erzeugungs-Hintergrund (und seinen Kantenrand-
    Fringe) transparent, ueberall im Bild - nicht nur am Rand verbunden."""
    rgba = np.array(img.convert("RGBA")).astype(np.float32)
    diff = rgba[..., :3] - np.array(_CHROMA, dtype=np.float32)
    abstand = np.sqrt((diff ** 2).sum(axis=-1))
    deckkraft = np.clip((abstand - _CHROMA_KERN) / (_CHROMA_SAUM - _CHROMA_KERN), 0.0, 1.0) * 255
    rgba[..., 3] = np.minimum(rgba[..., 3], deckkraft)
    return Image.fromarray(rgba.astype(np.uint8), "RGBA")

# Listenpreise je Bild (Stand 08/2026, grosszuegig aufgerundet). Lieber etwas zu
# hoch ansetzen: die Kostenbremse soll frueher greifen, nicht spaeter.
_PREIS_USD = {"low": 0.02, "medium": 0.04, "high": 0.08, "auto": 0.08}


class OpenAIProvider:
    """Bindet ``images.generate`` von GPT Image 2 an."""

    name = "openai"
    model = "gpt-image-2"

    def __init__(self, api_key: str, quality: str = "medium") -> None:
        if not api_key:
            raise ValueError("Kein OpenAI-Schluessel gesetzt (OPENAI_API_KEY in der .env).")
        self._api_key = api_key
        self._quality = quality or "medium"

    def geschaetzte_kosten(self) -> float:
        """Was ein Bild voraussichtlich kostet - fuer die Vorabpruefung."""
        return _PREIS_USD.get(self._quality, 0.08)

    def generate(self, request: ImageRequest) -> GeneratedImage:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - optionale Abhaengigkeit
            raise RuntimeError("openai-SDK nicht installiert (pip install openai).") from exc

        orientation = request.orientation()
        prompt = f"{request.prompt}\n\n{_CHROMA_TEXT}" if request.transparent else request.prompt
        # Keine automatischen Wiederholungen einer eventuell schon bezahlten Erzeugung.
        client = OpenAI(api_key=self._api_key, timeout=180.0, max_retries=0)
        try:
            result = client.images.generate(
                model=self.model,
                prompt=prompt,
                size=_SIZE_ARG[orientation],
                quality=self._quality,
                # "transparent" lehnt gpt-image-2 ab (s. Kommentar oben) - immer opak
                # erzeugen und bei Bedarf per Chroma-Key selbst freistellen.
                background="opaque",
                output_format="png",
                n=1,
            )
        except Exception as exc:  # SDK- und HTTP-Fehler einheitlich kapseln
            # Manche Auth-Fehler enthalten Teile des Schluessels. Nicht an Browser/Log geben.
            status = getattr(exc, "status_code", None)
            code = getattr(exc, "code", None)
            if status == 401:
                detail = "OpenAI hat den API-Schluessel abgelehnt. OPENAI_API_KEY pruefen."
            elif code in {"insufficient_quota", "billing_hard_limit_reached", "billing_limit_user_error"}:
                detail = "OpenAI-API-Guthaben oder Kontolimit erschoepft. Das lokale Tagesbudget ist davon unabhaengig."
            elif status == 429:
                # Kein Guthabenproblem (das faengt der Zweig darueber), sondern zu viele
                # Anfragen in kurzer Zeit - etwa, wenn parallel Vorlagen erzeugt werden.
                detail = ("OpenAI meldet zu viele Anfragen in kurzer Zeit (429). Eine Minute "
                          "warten und erneut erzeugen - es wurde nichts berechnet.")
            elif status == 403:
                detail = "OpenAI verweigert den Modellzugriff. Modellfreigabe und Organisationsverifizierung pruefen."
            else:
                detail = str(exc).replace(self._api_key, "[API-Schluessel entfernt]")
            raise RuntimeError(f"GPT Image 2 Aufruf fehlgeschlagen: {detail}") from exc
        finally:
            client.close()

        payload = result.data[0].b64_json if result.data else None
        if not payload:
            raise RuntimeError("GPT Image 2 lieferte kein Bild zurueck.")
        img = Image.open(BytesIO(base64.b64decode(payload))).convert("RGBA")
        if img.size != SUPPORTED_SIZES[orientation]:
            img = img.resize(SUPPORTED_SIZES[orientation])
        if request.transparent:
            img = _chroma_entfernen(img)

        return GeneratedImage(
            image=img,
            provider=self.name,
            model=self.model,
            cost_usd=self.geschaetzte_kosten(),
        )
