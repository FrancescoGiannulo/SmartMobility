"""[IF-UT.15] Test Scrive Recensione — scenari base e alternativi."""
import uuid as _uuid
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session
from main import app

http = TestClient(app)

LAT_TEST = 41.11
LNG_TEST = 16.85


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _elimina_recensione(db, recensione_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM recensioni WHERE id = :id"), {"id": recensione_id})
        s.commit()


def _inserisci_mezzo(db, codice: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', 'Disponibile', :lat, :lng, 80)
        """), {"codice": codice, "lat": LAT_TEST, "lng": LNG_TEST})
        s.commit()
        row = s.execute(
            text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}
        ).fetchone()
    return str(row.id)


def _inserisci_corsa_conclusa(db, utente_id, mezzo_id) -> None:
    now = datetime.now(timezone.utc)
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
            VALUES (:id, :uid, :mid, 'terminata', :inizio, :fine, 3.5)
        """), {
            "id": str(_uuid.uuid4()), "uid": str(utente_id), "mid": mezzo_id,
            "inizio": now, "fine": now,
        })
        s.commit()


def _cleanup_corsa(db, utente_id, mezzo_id) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE utente_id = :uid"), {"uid": str(utente_id)})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


@pytest.fixture
def utente_con_corsa_conclusa(utente_test, db):
    mezzo_id = _inserisci_mezzo(db, "REC-TEST-01")
    _inserisci_corsa_conclusa(db, utente_test["id"], mezzo_id)
    yield utente_test
    _cleanup_corsa(db, utente_test["id"], mezzo_id)


# ── Scenario base: voto + commento ───────────────────────────────────────────

@pytest.mark.integration
def test_scrive_recensione_scenario_base(utente_con_corsa_conclusa, db):
    """[IF-UT.15] Utente con corsa conclusa scrive recensione con voto e commento → 201."""
    utente = utente_con_corsa_conclusa
    token = _login(utente["email"], utente["password"])
    resp = http.post(
        "/utente/recensioni",
        json={"voto": 5, "commento": "Servizio ottimo"},
        headers=_auth(token),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["voto"] == 5
    assert body["commento"] == "Servizio ottimo"
    assert "id" in body
    assert "created_at" in body
    # cleanup
    _elimina_recensione(db, body["id"])


# ── Scenario alternativo: voto valido senza commento ─────────────────────────

@pytest.mark.integration
def test_scrive_recensione_senza_commento(utente_con_corsa_conclusa, db):
    """[IF-UT.15] Voto valido senza commento → 201, commento null."""
    utente = utente_con_corsa_conclusa
    token = _login(utente["email"], utente["password"])
    resp = http.post(
        "/utente/recensioni",
        json={"voto": 3},
        headers=_auth(token),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["commento"] is None
    # cleanup
    _elimina_recensione(db, body["id"])


# ── Scenario alternativo: voto fuori range → 422 ─────────────────────────────

@pytest.mark.integration
def test_scrive_recensione_voto_fuori_range(utente_con_corsa_conclusa):
    """[IF-UT.15] Voto fuori dall'intervallo [1,5] → 422."""
    utente = utente_con_corsa_conclusa
    token = _login(utente["email"], utente["password"])
    resp = http.post(
        "/utente/recensioni",
        json={"voto": 6, "commento": "x"},
        headers=_auth(token),
    )
    assert resp.status_code == 422


# ── Scenario alternativo: precondizione non soddisfatta (nessuna corsa conclusa) → 422

@pytest.mark.integration
def test_scrive_recensione_senza_corsa_conclusa(utente_test):
    """[IF-UT.15] Utente senza corse concluse → 422 (precondizione UT-15 non soddisfatta)."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.post(
        "/utente/recensioni",
        json={"voto": 4},
        headers=_auth(token),
    )
    assert resp.status_code == 422


# ── Scenario alternativo: non autenticato → 401 ──────────────────────────────

@pytest.mark.integration
def test_scrive_recensione_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.post("/utente/recensioni", json={"voto": 4})
    assert resp.status_code == 401


# ── Le mie recensioni (storico) ──────────────────────────────────────────────

@pytest.mark.integration
def test_mie_recensioni_restituisce_lo_storico(utente_con_corsa_conclusa, db):
    """[IF-UT.15] GET /utente/recensioni restituisce le recensioni dell'utente autenticato."""
    utente = utente_con_corsa_conclusa
    token = _login(utente["email"], utente["password"])
    creata = http.post(
        "/utente/recensioni",
        json={"voto": 4, "commento": "Buona esperienza"},
        headers=_auth(token),
    ).json()
    resp = http.get("/utente/recensioni", headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert any(r["id"] == creata["id"] and r["voto"] == 4 for r in body)
    # cleanup
    _elimina_recensione(db, creata["id"])


@pytest.mark.integration
def test_mie_recensioni_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/utente/recensioni")
    assert resp.status_code == 401
