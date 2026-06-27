"""[IF-OP.08] Test Gestisce Segnalazione — transizione a stato 'risolta'."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _crea_segnalazione(db, utente_id) -> str:
    with Session(db) as s:
        row = s.execute(
            text(
                "INSERT INTO segnalazioni (utente_id, tipologia, descrizione) "
                "VALUES (:uid, 'Altro', 'Test segnalazione') RETURNING id"
            ),
            {"uid": str(utente_id)},
        ).fetchone()
        s.commit()
    return str(row.id)


def _elimina_segnalazione(db, segnalazione_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM segnalazioni WHERE id = :id"), {"id": segnalazione_id})
        s.commit()


@pytest.mark.integration
def test_risolvi_segnalazione_scenario_base(db, utente_test, operatore_test):
    """[IF-OP.08] Segnalazione in_carico -> risolvi -> stato 'risolta', visibile nello storico utente."""
    segnalazione_id = _crea_segnalazione(db, utente_test["id"])
    try:
        token_op = _login(operatore_test["email"], operatore_test["password"])
        resp = http.patch(
            f"/operatore/segnalazioni/{segnalazione_id}/prendi-in-carico",
            headers=_auth(token_op),
        )
        assert resp.status_code == 200, resp.text

        resp = http.patch(
            f"/operatore/segnalazioni/{segnalazione_id}/risolvi",
            headers=_auth(token_op),
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["stato"] == "risolta"

        token_ut = _login(utente_test["email"], utente_test["password"])
        storico = http.get("/utente/segnalazioni", headers=_auth(token_ut))
        assert storico.status_code == 200
        assert any(s["id"] == segnalazione_id and s["stato"] == "risolta" for s in storico.json())
    finally:
        _elimina_segnalazione(db, segnalazione_id)


@pytest.mark.integration
def test_risolvi_segnalazione_aperta_422(db, utente_test, operatore_test):
    """[IF-OP.08] Tentativo di risolvere una segnalazione ancora 'aperta' -> 422."""
    segnalazione_id = _crea_segnalazione(db, utente_test["id"])
    try:
        token_op = _login(operatore_test["email"], operatore_test["password"])
        resp = http.patch(
            f"/operatore/segnalazioni/{segnalazione_id}/risolvi",
            headers=_auth(token_op),
        )
        assert resp.status_code == 422
    finally:
        _elimina_segnalazione(db, segnalazione_id)


@pytest.mark.integration
def test_risolvi_segnalazione_non_trovata_404(operatore_test):
    """[IF-OP.08] Id inesistente -> 404."""
    import uuid
    token_op = _login(operatore_test["email"], operatore_test["password"])
    resp = http.patch(
        f"/operatore/segnalazioni/{uuid.uuid4()}/risolvi",
        headers=_auth(token_op),
    )
    assert resp.status_code == 404
