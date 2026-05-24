import pytest
import httpx
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
    # Zona operativa contenitore
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    svc.crea_zona("test_op_valida", "operativa", operativa, None)
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
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    svc.crea_zona("test_op_lista", "operativa", operativa, None)
    coordinate = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    svc.crea_zona("test_lista", "parcheggio", coordinate, None)
    zone = svc.ottieni_zone()
    nomi = [z["nome"] for z in zone]
    assert "test_lista" in nomi


def _login(email: str, password: str) -> str:
    r = httpx.post("http://localhost:8000/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def test_mappa_mezzi_utente_autenticato(utente_test):
    token = _login(utente_test["email"], utente_test["password"])
    r = httpx.get(
        "http://localhost:8000/utente/mappa/mezzi",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_mappa_mezzi_utente_non_autenticato():
    r = httpx.get("http://localhost:8000/utente/mappa/mezzi")
    assert r.status_code == 401


def test_crea_zona_via_http(operatore_test):
    token = _login(operatore_test["email"], operatore_test["password"])
    # Crea zona operativa contenitore
    r_op = httpx.post(
        "http://localhost:8000/operatore/zone",
        json={
            "nome": "test_op_http",
            "tipo": "operativa",
            "coordinate": [
                [16.84, 41.10], [16.88, 41.10],
                [16.88, 41.14], [16.84, 41.14],
            ],
            "limite_velocita": None,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r_op.status_code == 201
    op_id = r_op.json()["id"]

    payload = {
        "nome": "test_http_zona",
        "tipo": "vietata",
        "coordinate": [
            [16.85, 41.11], [16.86, 41.11],
            [16.86, 41.12], [16.85, 41.12],
        ],
        "limite_velocita": None,
    }
    r = httpx.post(
        "http://localhost:8000/operatore/zone",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["nome"] == "test_http_zona"
    assert data["tipo"] == "vietata"
    assert data["perimetro"]["type"] == "Polygon"
    zona_id = data["id"]
    httpx.delete(
        f"http://localhost:8000/operatore/zone/{zona_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    httpx.delete(
        f"http://localhost:8000/operatore/zone/{op_id}",
        headers={"Authorization": f"Bearer {token}"},
    )


def test_crea_zona_poligono_invalido(operatore_test):
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "test_invalido",
        "tipo": "vietata",
        "coordinate": [[16.85, 41.11], [16.86, 41.11]],
        "limite_velocita": None,
    }
    r = httpx.post(
        "http://localhost:8000/operatore/zone",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 422


def test_repo_esiste_zona_operativa_contenente_true(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    # Crea zona operativa grande
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    repo.crea("test_op_outer", "operativa", operativa, None)
    # Poligono piccolo interno
    interno = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    assert repo.esiste_zona_operativa_contenente(interno) is True


def test_repo_esiste_zona_operativa_contenente_false(db):
    from dal.zona_repository import ZonaRepository
    repo = ZonaRepository(db)
    # Nessuna zona operativa → False
    # Il cleanup_zone fixture elimina tutte le zone con nome LIKE 'test_%',
    # garantendo che non rimangano zone operative da test precedenti.
    # ATTENZIONE: il test fallisce se nel DB di integrazione esistono zone
    # operative con nomi che non iniziano con 'test_' (es. dati di seed).
    esterno = [
        [16.90, 41.15], [16.91, 41.15],
        [16.91, 41.16], [16.90, 41.16], [16.90, 41.15],
    ]
    assert repo.esiste_zona_operativa_contenente(esterno) is False


def test_servizio_gis_vincolo_zona_operativa_ok(db):
    """Zona non-operativa dentro una zona operativa → crea correttamente."""
    from bll.servizio_gis import ServizioGIS
    svc = ServizioGIS(db)
    operativa = [
        [16.84, 41.10], [16.88, 41.10],
        [16.88, 41.14], [16.84, 41.14], [16.84, 41.10],
    ]
    svc.crea_zona("test_op_vincolo", "operativa", operativa, None)
    interno = [
        [16.85, 41.11], [16.86, 41.11],
        [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
    ]
    zona = svc.crea_zona("test_vietata_interna", "vietata", interno, None)
    assert zona["nome"] == "test_vietata_interna"


def test_servizio_gis_vincolo_zona_operativa_fuori(db):
    """Zona non-operativa fuori da qualsiasi zona operativa → PoligonoFuoriZonaOperativaException."""
    from bll.servizio_gis import ServizioGIS, PoligonoFuoriZonaOperativaException
    svc = ServizioGIS(db)
    esterno = [
        [16.90, 41.15], [16.91, 41.15],
        [16.91, 41.16], [16.90, 41.16], [16.90, 41.15],
    ]
    with pytest.raises(PoligonoFuoriZonaOperativaException):
        svc.crea_zona("test_fuori", "vietata", esterno, None)


def test_crea_zona_fuori_operativa_http(operatore_test):
    """POST /operatore/zone con zona non-operativa fuori confine → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "test_fuori_http",
        "tipo": "limitata",
        "coordinate": [
            [16.90, 41.15], [16.91, 41.15],
            [16.91, 41.16], [16.90, 41.16],
        ],
        "limite_velocita": 30,
    }
    r = httpx.post(
        "http://localhost:8000/operatore/zone",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 422
