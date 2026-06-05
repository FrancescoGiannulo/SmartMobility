"""[CS-15] Test Configura Parametri Numerici di Sistema (IF-OP.08, IF-OP.09, IF-OP.10, IF-OP.14)."""
import pytest
from fastapi.testclient import TestClient
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── Autenticazione ────────────────────────────────────────────────────────────

def test_get_parametri_non_autenticato():
    """[IIN-2] GET senza token → 401."""
    resp = http.get("/operatore/configurazione/parametri")
    assert resp.status_code == 401


def test_put_parametri_non_autenticato():
    """[IIN-2] PUT senza token → 401."""
    resp = http.put("/operatore/configurazione/parametri", json={})
    assert resp.status_code == 401


def test_get_parametri_utente_non_autorizzato(utente_test):
    """[IIN-2] UT non può accedere alla configurazione → 403."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.get("/operatore/configurazione/parametri", headers=_auth(token))
    assert resp.status_code == 403


# ── Scenario base GET ─────────────────────────────────────────────────────────

def test_get_parametri_restituisce_valori_correnti(operatore_test):
    """[IF-OP.08/09/10/14] GET restituisce i 4 parametri numerici."""
    token = _login(operatore_test["email"], operatore_test["password"])
    resp = http.get("/operatore/configurazione/parametri", headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert "durata_max_prenotazione_min" in body
    assert "durata_periodo_grazia_min" in body
    assert "max_mezzi_per_utente" in body
    assert "addebito_pausa_min" in body


# ── Scenario base PUT ─────────────────────────────────────────────────────────

def test_aggiorna_tutti_i_parametri(operatore_test):
    """[CS-15] PUT con tutti i valori validi → 200 e valori aggiornati."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": 30,
        "durata_periodo_grazia_min": 10,
        "max_mezzi_per_utente": 3,
        "addebito_pausa_min": "0.50",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["durata_max_prenotazione_min"] == 30
    assert body["durata_periodo_grazia_min"] == 10
    assert body["max_mezzi_per_utente"] == 3
    assert float(body["addebito_pausa_min"]) == 0.50


def test_aggiorna_parametri_upsert(operatore_test):
    """[CS-15] Seconda PUT aggiorna la riga singleton, non ne crea una nuova."""
    token = _login(operatore_test["email"], operatore_test["password"])
    http.put(
        "/operatore/configurazione/parametri",
        json={"durata_max_prenotazione_min": 20, "durata_periodo_grazia_min": 5,
              "max_mezzi_per_utente": 2, "addebito_pausa_min": "0.00"},
        headers=_auth(token),
    )
    http.put(
        "/operatore/configurazione/parametri",
        json={"durata_max_prenotazione_min": 45, "durata_periodo_grazia_min": 0,
              "max_mezzi_per_utente": 1, "addebito_pausa_min": "1.00"},
        headers=_auth(token),
    )
    resp = http.get("/operatore/configurazione/parametri", headers=_auth(token))
    body = resp.json()
    assert body["durata_max_prenotazione_min"] == 45
    assert body["durata_periodo_grazia_min"] == 0
    assert float(body["addebito_pausa_min"]) == 1.00


def test_grazia_zero_disabilita_pausa_gratuita(operatore_test):
    """[IF-OP.09] durata_periodo_grazia_min = 0 è valido (pausa gratuita disabilitata)."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": 15,
        "durata_periodo_grazia_min": 0,
        "max_mezzi_per_utente": 1,
        "addebito_pausa_min": "0.00",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    assert resp.json()["durata_periodo_grazia_min"] == 0


def test_addebito_zero_valido(operatore_test):
    """[IF-OP.14] addebito_pausa_min = 0 è valido (nessun addebito durante pausa)."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": 15,
        "durata_periodo_grazia_min": 5,
        "max_mezzi_per_utente": 1,
        "addebito_pausa_min": "0.00",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    assert float(resp.json()["addebito_pausa_min"]) == 0.0


# ── Sequenza alternativa — valori non validi ──────────────────────────────────

def test_durata_prenotazione_negativa(operatore_test):
    """[CS-15 alt] durata_max_prenotazione_min negativa → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": -1,
        "durata_periodo_grazia_min": 5,
        "max_mezzi_per_utente": 1,
        "addebito_pausa_min": "0.00",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_durata_grazia_negativa(operatore_test):
    """[CS-15 alt] durata_periodo_grazia_min negativa → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": 15,
        "durata_periodo_grazia_min": -1,
        "max_mezzi_per_utente": 1,
        "addebito_pausa_min": "0.00",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_max_mezzi_zero(operatore_test):
    """[CS-15 alt] max_mezzi_per_utente = 0 → 422 (deve essere >= 1)."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": 15,
        "durata_periodo_grazia_min": 5,
        "max_mezzi_per_utente": 0,
        "addebito_pausa_min": "0.00",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_max_mezzi_negativo(operatore_test):
    """[CS-15 alt] max_mezzi_per_utente negativo → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": 15,
        "durata_periodo_grazia_min": 5,
        "max_mezzi_per_utente": -2,
        "addebito_pausa_min": "0.00",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_addebito_negativo(operatore_test):
    """[CS-15 alt] addebito_pausa_min negativo → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "durata_max_prenotazione_min": 15,
        "durata_periodo_grazia_min": 5,
        "max_mezzi_per_utente": 1,
        "addebito_pausa_min": "-0.10",
    }
    resp = http.put("/operatore/configurazione/parametri", json=payload, headers=_auth(token))
    assert resp.status_code == 422
