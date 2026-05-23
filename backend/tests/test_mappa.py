import pytest
from uuid import UUID
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
