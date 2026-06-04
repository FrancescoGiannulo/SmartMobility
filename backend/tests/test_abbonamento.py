"""[IF-UT.16] Test Sottoscrive Abbonamento — scenari base e alternativi."""
import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _domani() -> str:
    return (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()


@pytest.fixture
def abbonamento_op(operatore_test):
    """Crea un piano abbonamento attivo e lo elimina dopo il test."""
    token = _login(operatore_test["email"], operatore_test["password"])
    resp = http.post("/operatore/offerte", json={
        "nome": "Piano Test Abbonamento",
        "tipo": "abbonamento",
        "descrizione": "30 giorni illimitati",
        "prezzo": 9.99,
        "durata_giorni": 30,
    }, headers=_auth(token))
    assert resp.status_code == 201
    offerta = resp.json()
    yield offerta
    http.delete(f"/operatore/offerte/{offerta['id']}", headers=_auth(token))


@pytest.fixture
def utente_con_metodo(utente_test):
    """Utente con un metodo di pagamento registrato."""
    token = _login(utente_test["email"], utente_test["password"])
    http.post("/pagamenti/metodi", json={"tipo": "carta", "last_four": "1234"}, headers=_auth(token))
    yield {**utente_test, "token": token}


# ── Autenticazione ────────────────────────────────────────────────────────────

def test_get_piani_non_autenticato():
    """[IIN-2] GET piani senza token → 401."""
    resp = http.get("/utente/abbonamenti/piani")
    assert resp.status_code == 401


def test_sottoscrivi_non_autenticato(abbonamento_op):
    """[IIN-2] POST senza token → 401."""
    resp = http.post(f"/utente/abbonamenti/{abbonamento_op['id']}")
    assert resp.status_code == 401


# ── Scenario base: visualizza piani ──────────────────────────────────────────

def test_get_piani_disponibili(utente_test, abbonamento_op):
    """[IF-UT.16] GET restituisce solo offerte di tipo abbonamento attive."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.get("/utente/abbonamenti/piani", headers=_auth(token))
    assert resp.status_code == 200
    piani = resp.json()
    assert isinstance(piani, list)
    assert all(p["tipo"] == "abbonamento" for p in piani)
    ids = [p["id"] for p in piani]
    assert abbonamento_op["id"] in ids


# ── Scenario base: sottoscrivi ────────────────────────────────────────────────

def test_sottoscrivi_abbonamento(utente_con_metodo, abbonamento_op):
    """[IF-UT.16] Sottoscrivi piano → 201 con abbonamento attivo."""
    resp = http.post(
        f"/utente/abbonamenti/{abbonamento_op['id']}",
        headers=_auth(utente_con_metodo["token"]),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["stato"] == "attivo"
    assert body["offerta_id"] == abbonamento_op["id"]
    assert "data_fine" in body


def test_sottoscrivi_imposta_data_fine_corretta(utente_con_metodo, abbonamento_op):
    """[IF-UT.16] data_fine = oggi + durata_giorni del piano."""
    resp = http.post(
        f"/utente/abbonamenti/{abbonamento_op['id']}",
        headers=_auth(utente_con_metodo["token"]),
    )
    assert resp.status_code == 201
    body = resp.json()
    data_fine = datetime.fromisoformat(body["data_fine"])
    attesa = datetime.now(timezone.utc) + timedelta(days=abbonamento_op["durata_giorni"])
    assert abs((data_fine - attesa).total_seconds()) < 10


def test_get_abbonamento_corrente(utente_con_metodo, abbonamento_op):
    """[IF-UT.16] Dopo sottoscrizione, GET /corrente restituisce abbonamento attivo."""
    http.post(
        f"/utente/abbonamenti/{abbonamento_op['id']}",
        headers=_auth(utente_con_metodo["token"]),
    )
    resp = http.get("/utente/abbonamenti/corrente", headers=_auth(utente_con_metodo["token"]))
    assert resp.status_code == 200
    assert resp.json()["stato"] == "attivo"


# ── Sequenza alternativa — nessun metodo di pagamento ────────────────────────

def test_sottoscrivi_senza_metodo_pagamento(utente_test, abbonamento_op):
    """[IF-UT.16 alt] Utente senza metodo di pagamento → 422."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.post(
        f"/utente/abbonamenti/{abbonamento_op['id']}",
        headers=_auth(token),
    )
    assert resp.status_code == 422


# ── Sequenza alternativa — offerta non valida ─────────────────────────────────

def test_sottoscrivi_offerta_non_trovata(utente_con_metodo):
    """[IF-UT.16 alt] ID offerta inesistente → 404."""
    import uuid
    resp = http.post(
        f"/utente/abbonamenti/{uuid.uuid4()}",
        headers=_auth(utente_con_metodo["token"]),
    )
    assert resp.status_code == 404


def test_sottoscrivi_offerta_non_abbonamento(utente_con_metodo, operatore_test):
    """[IF-UT.16 alt] Offerta di tipo promozione → 422."""
    op_token = _login(operatore_test["email"], operatore_test["password"])
    promo = http.post("/operatore/offerte", json={
        "nome": "Promo Non Abbonamento",
        "tipo": "promozione",
        "sconto_percentuale": 10.0,
        "data_scadenza": _domani(),
    }, headers=_auth(op_token)).json()

    resp = http.post(
        f"/utente/abbonamenti/{promo['id']}",
        headers=_auth(utente_con_metodo["token"]),
    )
    assert resp.status_code == 422
    # cleanup
    http.delete(f"/operatore/offerte/{promo['id']}", headers=_auth(op_token))
