import pytest
from uuid import UUID, uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session


def _pulisci_zone(db):
    with Session(db) as s:
        s.execute(text("DELETE FROM zone WHERE nome LIKE 'test_%'"))
        s.commit()


@pytest.fixture(autouse=True)
def cleanup_zone(db):
    _pulisci_zone(db)
    yield
    _pulisci_zone(db)


def test_crea_e_lista_zona(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    coordinate = [
        [16.85, 41.11],
        [16.86, 41.11],
        [16.86, 41.12],
        [16.85, 41.12],
        [16.85, 41.11],
    ]
    zona = repo.crea("test_vietata", "vietata", coordinate, None)
    assert zona.id is not None
    assert zona.nome == "test_vietata"
    assert zona.tipo.value == "vietata"

    lista = repo.lista_zone(solo_attive=True)
    ids = [str(z["id"]) for z in lista]
    assert str(zona.id) in ids


def test_elimina_zona(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = repo.crea("test_elimina", "parcheggio", coordinate, None)
    repo.elimina(zona.id)
    lista = repo.lista_zone(solo_attive=True)
    assert str(zona.id) not in [str(z["id"]) for z in lista]


def test_trova_per_id(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = repo.crea("test_trova", "limitata", coordinate, 30)
    risultato = repo.trova_per_id(zona.id)
    assert str(risultato["id"]) == str(zona.id)
    assert risultato["nome"] == "test_trova"
    assert risultato["tipo"] == "limitata"


def test_trova_per_id_non_trovata(db):
    from dal.zona_repository import ZonaRepository, ZonaNonTrovataException
    repo = ZonaRepository(db)
    with pytest.raises(ZonaNonTrovataException):
        repo.trova_per_id(uuid4())


def test_lista_mezzi_disponibili(db):
    from dal.mezzo_repository import MezzoRepository
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES ('TEST-M01', 'monopattino', 'Disponibile', 41.11, 16.85, 80)
        """))
        s.commit()
    try:
        repo = MezzoRepository(db)
        mezzi = repo.lista_per_mappa(solo_disponibili=True)
        assert "TEST-M01" in [m["codice"] for m in mezzi]
    finally:
        with Session(db) as s:
            s.execute(text("DELETE FROM mezzi WHERE codice = 'TEST-M01'"))
            s.commit()


def test_lista_mezzi_tutti(db):
    from dal.mezzo_repository import MezzoRepository
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES ('TEST-M02', 'bicicletta', 'In manutenzione', 41.12, 16.86, 20)
        """))
        s.commit()
    try:
        repo = MezzoRepository(db)
        tutti = repo.lista_per_mappa(solo_disponibili=False)
        assert "TEST-M02" in [m["codice"] for m in tutti]
        disponibili = repo.lista_per_mappa(solo_disponibili=True)
        assert "TEST-M02" not in [m["codice"] for m in disponibili]
    finally:
        with Session(db) as s:
            s.execute(text("DELETE FROM mezzi WHERE codice = 'TEST-M02'"))
            s.commit()


def test_servizio_gis_crea_zona_valida(db):
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = svc.crea_zona("test_gis", "vietata", coordinate, None)
    assert zona["nome"] == "test_gis"
    assert zona["tipo"] == "vietata"
    assert zona["perimetro"]["type"] == "Polygon"


def test_servizio_gis_poligono_insufficiente(db):
    from bll.servizio_gis import ServizioGIS, PoligonoNonValidoException
    svc = ServizioGIS(db)
    with pytest.raises(PoligonoNonValidoException):
        svc.crea_zona("test_err", "vietata", [[16.85, 41.11], [16.86, 41.11]], None)


def test_servizio_gis_lista_zone(db):
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    svc.crea_zona("test_lista", "parcheggio", coordinate, None)
    zone = svc.ottieni_zone()
    nomi = [z["nome"] for z in zone]
    assert "test_lista" in nomi
