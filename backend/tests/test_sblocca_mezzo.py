import pytest
import uuid as _uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session


# ── Helpers ────────────────────────────────────────────────────────────────

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
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"),
                  {"id": mezzo_id})
        s.execute(text("DELETE FROM prenotazioni WHERE mezzo_id = :id"),
                  {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


# ── TestMezzoRepository ────────────────────────────────────────────────────

class TestMezzoRepository:

    @pytest.mark.integration
    def test_trova_per_id_esistente(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-TR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = MezzoRepository(db)
            mezzo = repo.trova_per_id(_uuid.UUID(mezzo_id))
            assert mezzo is not None
            assert mezzo["stato"] == "Disponibile"
            assert mezzo["codice"] == codice
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_trova_per_id_non_esistente(self, db):
        from dal.mezzo_repository import MezzoRepository
        repo = MezzoRepository(db)
        risultato = repo.trova_per_id(_uuid.uuid4())
        assert risultato is None

    @pytest.mark.integration
    def test_aggiorna_stato(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-AS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = MezzoRepository(db)
            repo.aggiorna_stato(_uuid.UUID(mezzo_id), "In uso")
            mezzo = repo.trova_per_id(_uuid.UUID(mezzo_id))
            assert mezzo["stato"] == "In uso"
        finally:
            _elimina_mezzo(db, mezzo_id)


# ── TestCorsaRepository ────────────────────────────────────────────────────

class TestCorsaRepository:

    @pytest.mark.integration
    def test_crea_corsa_diretta(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice = f"TEST-CR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            repo = CorsaRepository(db)
            corsa = repo.crea(utente_test["id"], _uuid.UUID(mezzo_id), None)
            assert corsa["stato"] == "in_uso"
            assert str(corsa["utente_id"]) == str(utente_test["id"])
            assert str(corsa["mezzo_id"]) == mezzo_id
            assert corsa["prenotazione_id"] is None
            assert "inizio_at" in corsa
        finally:
            _elimina_mezzo(db, mezzo_id)
