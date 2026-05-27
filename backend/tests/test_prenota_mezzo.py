import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session


# ── Helpers (identici a test_sblocca_mezzo.py) ────────────────────────────

def _login(email: str, password: str) -> str:
    import httpx
    r = httpx.post("http://localhost:8000/auth/login",
                   json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _inserisci_mezzo(db, codice: str, stato: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, 41.11, 16.85, 80)
        """), {"codice": codice, "stato": stato})
        s.commit()
        row = s.execute(
            text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}
        ).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM prenotazioni WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


# ── TestPrenotazioneRepositoryCrea ────────────────────────────────────────

class TestPrenotazioneRepositoryCrea:

    @pytest.mark.integration
    def test_crea_prenotazione(self, db, utente_test):
        from dal.prenotazione_repository import PrenotazioneRepository
        codice = f"TEST-PREN-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = PrenotazioneRepository(db)
            pren = repo.crea(utente_test["id"], _uuid.UUID(mezzo_id), 30)
            assert pren["stato"] == "attiva"
            assert str(pren["mezzo_id"]) == mezzo_id
            assert str(pren["utente_id"]) == str(utente_test["id"])
            assert "scade_at" in pren
        finally:
            _elimina_mezzo(db, mezzo_id)


# ── TestServizioPrenotazione ───────────────────────────────────────────────

class TestServizioPrenotazione:

    @pytest.mark.integration
    def test_crea_prenotazione_disponibile(self, db, utente_test):
        from bll.servizio_prenotazione import ServizioPrenotazione
        codice = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            svc = ServizioPrenotazione(db)
            pren = svc.crea_prenotazione(_uuid.UUID(mezzo_id), utente_test["id"])
            assert pren["stato"] == "attiva"
            # verifica che il mezzo sia passato a "Prenotato"
            with Session(db) as s:
                row = s.execute(
                    text("SELECT stato FROM mezzi WHERE id = :id"), {"id": mezzo_id}
                ).fetchone()
            assert row.stato == "Prenotato"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_crea_prenotazione_mezzo_non_disponibile(self, db, utente_test):
        from bll.servizio_prenotazione import ServizioPrenotazione, MezzoNonDisponibileException
        codice = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            svc = ServizioPrenotazione(db)
            with pytest.raises(MezzoNonDisponibileException):
                svc.crea_prenotazione(_uuid.UUID(mezzo_id), utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_crea_prenotazione_mezzo_non_trovato(self, db, utente_test):
        from bll.servizio_prenotazione import ServizioPrenotazione, MezzoNonTrovatoException
        svc = ServizioPrenotazione(db)
        with pytest.raises(MezzoNonTrovatoException):
            svc.crea_prenotazione(_uuid.uuid4(), utente_test["id"])


# ── TestPrenotaMezzoHTTP ──────────────────────────────────────────────────

class TestPrenotaMezzoHTTP:

    @pytest.mark.integration
    def test_prenota_mezzo_201(self, db, utente_test):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_id": mezzo_id},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            data = r.json()
            assert data["stato"] == "attiva"
            assert data["mezzo_id"] == mezzo_id
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_prenota_mezzo_non_disponibile_409(self, db, utente_test):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_id": mezzo_id},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_prenota_mezzo_inesistente_404(self, utente_test):
        import httpx
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.post(
            "http://localhost:8000/utente/prenotazioni",
            json={"mezzo_id": str(_uuid.uuid4())},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    @pytest.mark.integration
    def test_prenota_non_autenticato_401(self, db):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_id": mezzo_id},
            )
            assert r.status_code == 401
        finally:
            _elimina_mezzo(db, mezzo_id)
