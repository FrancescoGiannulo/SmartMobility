"""[IF-OP.06] Test Definisce Offerta — scenari base e alternativi."""
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


def _ieri() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()


# ── Scenario base: lista offerte ─────────────────────────────────────────────

def test_lista_offerte_operatore_autenticato(operatore_test):
    """[IF-OP.06] Operatore autenticato riceve lista offerte."""
    token = _login(operatore_test["email"], operatore_test["password"])
    resp = http.get("/operatore/offerte", headers=_auth(token))
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_lista_offerte_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/operatore/offerte")
    assert resp.status_code == 401


# ── Scenario base: crea promozione ───────────────────────────────────────────

def test_crea_promozione_valida(operatore_test):
    """[IF-OP.06] Crea promozione con sconto e scadenza futura → 201."""
    token = _login(operatore_test["email"], operatore_test["password"])
    for o in http.get("/operatore/offerte", headers=_auth(token)).json():
        if o["nome"] == "Black Friday 2026":
            http.delete(f"/operatore/offerte/{o['id']}", headers=_auth(token))
    payload = {
        "nome": "Black Friday 2026",
        "tipo": "promozione",
        "descrizione": "Sconto del 20% su tutte le corse",
        "sconto_percentuale": 20.0,
        "data_scadenza": _domani(),
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 201
    body = resp.json()
    assert body["nome"] == "Black Friday 2026"
    assert body["tipo"] == "promozione"
    assert body["stato"] == "attiva"
    assert float(body["sconto_percentuale"]) == 20.0
    # cleanup
    http.delete(f"/operatore/offerte/{body['id']}", headers=_auth(token))


# ── Scenario base: crea abbonamento ──────────────────────────────────────────

def test_crea_abbonamento_valido(operatore_test):
    """[IF-OP.06] Crea abbonamento con prezzo e durata → 201."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Abbonamento Mensile",
        "tipo": "abbonamento",
        "descrizione": "30 giorni illimitati",
        "prezzo": 29.99,
        "durata_giorni": 30,
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 201
    body = resp.json()
    assert body["tipo"] == "abbonamento"
    assert float(body["prezzo"]) == 29.99
    assert body["durata_giorni"] == 30
    # cleanup
    http.delete(f"/operatore/offerte/{body['id']}", headers=_auth(token))


# ── Scenario alternativo: nome duplicato → 409 ───────────────────────────────

def test_crea_offerta_nome_duplicato(operatore_test):
    """[IF-OP.06] Nome già esistente → 409."""
    token = _login(operatore_test["email"], operatore_test["password"])
    for o in http.get("/operatore/offerte", headers=_auth(token)).json():
        if o["nome"] == "Offerta Unica Dup Test":
            http.delete(f"/operatore/offerte/{o['id']}", headers=_auth(token))
    payload = {
        "nome": "Offerta Unica Dup Test",
        "tipo": "promozione",
        "sconto_percentuale": 10.0,
        "data_scadenza": _domani(),
    }
    resp1 = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp1.status_code == 201
    resp2 = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp2.status_code == 409
    # cleanup
    http.delete(f"/operatore/offerte/{resp1.json()['id']}", headers=_auth(token))


# ── Scenario alternativo: scadenza nel passato → 422 ─────────────────────────

def test_crea_promozione_scadenza_passata(operatore_test):
    """[IF-OP.06] Data scadenza nel passato → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Offerta Scaduta",
        "tipo": "promozione",
        "sconto_percentuale": 10.0,
        "data_scadenza": _ieri(),
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 422


# ── Scenario alternativo: sconto non valido → 422 ────────────────────────────

def test_crea_promozione_sconto_zero(operatore_test):
    """[IF-OP.06] Sconto = 0 → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Sconto Zero",
        "tipo": "promozione",
        "sconto_percentuale": 0.0,
        "data_scadenza": _domani(),
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 422


# ── Scenario alternativo: abbonamento prezzo negativo → 422 ──────────────────

def test_crea_abbonamento_prezzo_negativo(operatore_test):
    """[IF-OP.06] Prezzo ≤ 0 → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Abbonamento Gratis",
        "tipo": "abbonamento",
        "prezzo": -5.0,
        "durata_giorni": 30,
    }
    resp = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert resp.status_code == 422


# ── Elimina offerta ───────────────────────────────────────────────────────────

def test_elimina_offerta(operatore_test):
    """[IF-OP.06] Crea poi elimina → 204."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "nome": "Offerta Da Eliminare",
        "tipo": "promozione",
        "sconto_percentuale": 15.0,
        "data_scadenza": _domani(),
    }
    created = http.post("/operatore/offerte", json=payload, headers=_auth(token))
    assert created.status_code == 201
    offerta_id = created.json()["id"]

    del_resp = http.delete(f"/operatore/offerte/{offerta_id}", headers=_auth(token))
    assert del_resp.status_code == 204

    lista = http.get("/operatore/offerte", headers=_auth(token)).json()
    ids = [o["id"] for o in lista]
    assert offerta_id not in ids
