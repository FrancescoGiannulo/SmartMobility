import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository


@pytest.mark.integration
def test_aggiorna_posizione_aggiorna_lat_lng(db):
    codice = f"POS-{_uuid.uuid4().hex[:6]}"
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng)
            VALUES (:c, 'monopattino', 'Disponibile', 41.1100, 16.8680)
        """), {"c": codice})
        s.commit()
        mezzo_id = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).scalar()
    try:
        MezzoRepository(db).aggiorna_posizione(mezzo_id, 41.1093, 16.8791)
        m = MezzoRepository(db).trova_per_id(mezzo_id)
        assert round(m["lat"], 4) == 41.1093
        assert round(m["lng"], 4) == 16.8791
    finally:
        with Session(db) as s:
            s.execute(text("DELETE FROM mezzi WHERE codice = :c"), {"c": codice})
            s.commit()


@pytest.mark.integration
def test_servizio_mappa_aggiorna_posizione_mezzo(db):
    import uuid as _uuid
    from bll.servizio_mappa import ServizioMappa
    codice = f"POS2-{_uuid.uuid4().hex[:6]}"
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng)
            VALUES (:c, 'bicicletta', 'In uso', 41.1100, 16.8680)
        """), {"c": codice})
        s.commit()
        mezzo_id = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).scalar()
    try:
        ServizioMappa(db).aggiorna_posizione_mezzo(mezzo_id, 41.1095, 16.8806)
        m = MezzoRepository(db).trova_per_id(mezzo_id)
        assert round(m["lat"], 4) == 41.1095
        assert round(m["lng"], 4) == 16.8806
    finally:
        with Session(db) as s:
            s.execute(text("DELETE FROM mezzi WHERE codice = :c"), {"c": codice})
            s.commit()
