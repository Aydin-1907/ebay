"""Bereits bei eBay eingestellte Ideen duerfen nicht mehr als Empfehlung auftauchen.

Nutzerwunsch (20.11.2026), woertlich: "ich moechte von dir dass du ein system
aufbaust dass alle motive die schonmal auf ebay geupdaten wurden nicht mehr
als emofehung sinchtbar sind."

``MotivIdee.status`` allein reicht nicht als Signal: "uebernommen" wird schon
beim Erzeugen des Bildes gesetzt, nicht erst beim erfolgreichen Einstellen -
siehe ``app/studio/router.py::batch_fortschritt`` fuer denselben Fund. Darum
prueft ``ideen.liste`` zusaetzlich gegen ein echtes, aktives ``PodListing``.
"""
from __future__ import annotations

from app.studio.models import MotivIdee, PodListing, PodProduct
from app.studio.radar import ideen


def _idee(db, **kw) -> MotivIdee:
    basis = dict(quelle_plattform="trend", quelle_shop="eigen", fremdtitel="",
                 status="neu", thema="Testthema")
    basis.update(kw)
    i = MotivIdee(**basis)
    db.add(i)
    db.commit()
    return i


def test_idee_ohne_design_bleibt_sichtbar(db):
    _idee(db, fremd_id="a")
    treffer = ideen.liste(db, status="neu")
    assert len(treffer) == 1


def test_idee_mit_aktivem_listing_verschwindet_trotz_status_neu(db):
    i = _idee(db, fremd_id="b", design_id=1, status="neu")
    produkt = PodProduct(design_id=1, title="Test", produktart="tshirt")
    db.add(produkt)
    db.commit()
    db.add(PodListing(product_id=produkt.id, status="active", channel="ebay"))
    db.commit()

    treffer = ideen.liste(db, status="neu")
    assert i.id not in [t.id for t in treffer]


def test_idee_mit_nur_entworfenem_design_bleibt_sichtbar(db):
    i = _idee(db, fremd_id="c", design_id=2, status="neu")
    produkt = PodProduct(design_id=2, title="Test", produktart="tshirt")
    db.add(produkt)
    db.commit()
    db.add(PodListing(product_id=produkt.id, status="ended", channel="ebay"))
    db.commit()

    treffer = ideen.liste(db, status="neu")
    assert i.id in [t.id for t in treffer]
