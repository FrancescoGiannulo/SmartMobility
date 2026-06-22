"""[IF-OP.12] Test Visualizza Recensioni (lato Operatore) — scenari base e alternativi."""
import uuid as _uuid
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
import controllers.recensione_controller as rec_ctrl

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _inserisci_recensione(db, voto: int, commento: str | None) -> str:
    rid = str(_uuid.uuid4())
    with Session(db) as s:
        s.execute(
            text(
                "INSERT INTO recensioni (id, utente_id, voto, commento) "
                "VALUES (:id, :uid, :voto, :commento)"
            ),
            {"id": rid, "uid": str(_uuid.uuid4()), "voto": voto, "commento": commento},
        )
        s.commit()
    return rid


def _elimina_recensione(db, recensione_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM recensioni WHERE id = :id"), {"id": recensione_id})
        s.commit()


# ── Scenario base OP-12 ──────────────────────────────────────────────────────

@pytest.mark.integration
def test_visualizza_recensioni_scenario_base(operatore_test, db):
    """[IF-OP.12] OP autenticato ottiene l'elenco recensioni + voto medio aggregato → 200."""
    id1 = _inserisci_recensione(db, 5, "Ottimo servizio")
    id2 = _inserisci_recensione(db, 3, None)
    try:
        token = _login(operatore_test["email"], operatore_test["password"])
        resp = http.get("/operatore/recensioni", headers=_auth(token))
        assert resp.status_code == 200
        body = resp.json()
        assert "recensioni" in body and "voto_medio" in body

        ids = {r["id"] for r in body["recensioni"]}
        assert {id1, id2} <= ids

        # voto_medio coerente con il calcolo su tutte le recensioni restituite
        voti = [r["voto"] for r in body["recensioni"]]
        atteso = round(sum(voti) / len(voti), 1)
        assert body["voto_medio"] == atteso
    finally:
        _elimina_recensione(db, id1)
        _elimina_recensione(db, id2)


# ── Scenario alternativo OP-12.01 NessunaRecensione ──────────────────────────

@pytest.mark.integration
def test_visualizza_recensioni_nessuna_recensione(operatore_test, monkeypatch):
    """[IF-OP.12.01] Nessuna recensione presente → 200, elenco vuoto e voto medio 0.0."""
    monkeypatch.setattr(rec_ctrl._servizio._repo, "find_all", lambda: [])
    token = _login(operatore_test["email"], operatore_test["password"])
    resp = http.get("/operatore/recensioni", headers=_auth(token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["recensioni"] == []
    assert body["voto_medio"] == 0.0


# ── Sicurezza IIN-2: solo ruolo OP ───────────────────────────────────────────

@pytest.mark.integration
def test_visualizza_recensioni_ruolo_non_op(utente_test):
    """[IIN-2] Un Utente (ruolo UT) non può accedere alle recensioni operatore → 403."""
    token = _login(utente_test["email"], utente_test["password"])
    resp = http.get("/operatore/recensioni", headers=_auth(token))
    assert resp.status_code == 403


@pytest.mark.integration
def test_visualizza_recensioni_non_autenticato():
    """[IIN-2] Senza token → 401."""
    resp = http.get("/operatore/recensioni")
    assert resp.status_code == 401
