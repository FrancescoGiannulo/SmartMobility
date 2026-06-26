"""[IF-OP.06] Test Definisce Regole Fine Corsa — scenari base e alternativi."""
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


def test_get_regole_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/operatore/regole-fine-corsa")
    assert resp.status_code == 401


def test_get_regole_autenticato(operatore_test):
    """[IF-OP.06] GET ritorna None o configurazione corrente."""
    token = _login(operatore_test["email"], operatore_test["password"])
    resp = http.get("/operatore/regole-fine-corsa", headers=_auth(token))
    assert resp.status_code == 200
    assert resp.json() is None or isinstance(resp.json(), dict)


def test_salva_regole_avviso(operatore_test):
    """[IF-OP.06] Salva config con vincolo 'avviso' → 200."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "avviso", "penale_fuori_zona": "0.00"}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["tipo_vincolo"] == "avviso"
    assert float(body["penale_fuori_zona"]) == 0.0


def test_salva_regole_penale(operatore_test):
    """[IF-OP.06] Salva config penale con importo positivo → 200."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "penale", "penale_fuori_zona": "5.00"}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["tipo_vincolo"] == "penale"
    assert float(body["penale_fuori_zona"]) == 5.0


def test_salva_regole_con_bonus(operatore_test):
    """[IF-OP.06] Salva config con bonus → 200."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {
        "tipo_vincolo": "avviso",
        "penale_fuori_zona": "0.00",
        "bonus_parcheggi_corretti": 5,
        "bonus_valore": "2.50",
    }
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["bonus_parcheggi_corretti"] == 5
    assert float(body["bonus_valore"]) == 2.50


def test_salva_regole_upsert(operatore_test):
    """[IF-OP.06] Seconda PUT aggiorna la config (non ne crea una nuova)."""
    token = _login(operatore_test["email"], operatore_test["password"])
    http.put("/operatore/regole-fine-corsa", json={"tipo_vincolo": "avviso", "penale_fuori_zona": "0.00"}, headers=_auth(token))
    http.put("/operatore/regole-fine-corsa", json={"tipo_vincolo": "divieto", "penale_fuori_zona": "0.00"}, headers=_auth(token))
    resp = http.get("/operatore/regole-fine-corsa", headers=_auth(token))
    assert resp.json()["tipo_vincolo"] == "divieto"


def test_penale_importo_zero(operatore_test):
    """[IF-OP.06] Penale con importo = 0 → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "penale", "penale_fuori_zona": "0.00"}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_bonus_incompleto(operatore_test):
    """[IF-OP.06] Bonus con solo parcheggi_corretti (senza valore) → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "avviso", "penale_fuori_zona": "0.00", "bonus_parcheggi_corretti": 5}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 422


def test_tipo_vincolo_non_valido(operatore_test):
    """[IF-OP.06] Tipo vincolo non riconosciuto → 422."""
    token = _login(operatore_test["email"], operatore_test["password"])
    payload = {"tipo_vincolo": "multa", "penale_fuori_zona": "0.00"}
    resp = http.put("/operatore/regole-fine-corsa", json=payload, headers=_auth(token))
    assert resp.status_code == 422
