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


# ── TestPrenotazioneRepository ─────────────────────────────────────────────

class TestPrenotazioneRepository:

    @pytest.mark.integration
    def test_trova_attiva_trovata(self, db, utente_test):
        from dal.prenotazione_repository import PrenotazioneRepository
        codice = f"TEST-PR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            repo = PrenotazioneRepository(db)
            pren = repo.trova_attiva_per_utente_e_mezzo(
                utente_test["id"], _uuid.UUID(mezzo_id)
            )
            assert pren is not None
            assert str(pren["utente_id"]) == str(utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_trova_attiva_non_trovata(self, db, utente_test):
        from dal.prenotazione_repository import PrenotazioneRepository
        repo = PrenotazioneRepository(db)
        risultato = repo.trova_attiva_per_utente_e_mezzo(
            utente_test["id"], _uuid.uuid4()
        )
        assert risultato is None

    @pytest.mark.integration
    def test_aggiorna_stato_prenotazione(self, db, utente_test):
        from dal.prenotazione_repository import PrenotazioneRepository
        codice = f"TEST-APR-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
            pren_id = s.execute(text("""
                SELECT id FROM prenotazioni
                WHERE mezzo_id = :mid AND utente_id = :uid
            """), {"mid": mezzo_id, "uid": str(utente_test["id"])}).fetchone().id
        try:
            repo = PrenotazioneRepository(db)
            repo.aggiorna_stato(_uuid.UUID(str(pren_id)), "convertita")
            with Session(db) as s:
                row = s.execute(
                    text("SELECT stato FROM prenotazioni WHERE id = :id"),
                    {"id": str(pren_id)}
                ).fetchone()
            assert row.stato == "convertita"
        finally:
            _elimina_mezzo(db, mezzo_id)


# ── TestServizioMobilita ───────────────────────────────────────────────────

class TestServizioMobilita:

    @pytest.mark.integration
    def test_sblocca_mezzo_disponibile(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SM-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            svc = ServizioMobilita(db)
            corsa = svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
            assert corsa["stato"] == "in_uso"
            assert corsa["prenotazione_id"] is None
            with Session(db) as s:
                row = s.execute(
                    text("SELECT stato FROM mezzi WHERE id = :id"),
                    {"id": mezzo_id}
                ).fetchone()
            assert row.stato == "In uso"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_mezzo_prenotato_da_utente(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SMP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            svc = ServizioMobilita(db)
            corsa = svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
            assert corsa["stato"] == "in_uso"
            assert corsa["prenotazione_id"] is not None
            with Session(db) as s:
                row = s.execute(text("""
                    SELECT stato FROM prenotazioni
                    WHERE mezzo_id = :mid AND utente_id = :uid
                """), {"mid": mezzo_id, "uid": str(utente_test["id"])}).fetchone()
            assert row.stato == "convertita"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_mezzo_non_trovato(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonTrovatoException
        svc = ServizioMobilita(db)
        with pytest.raises(MezzoNonTrovatoException):
            svc.sblocca_mezzo(_uuid.uuid4(), utente_test["id"])

    @pytest.mark.integration
    def test_sblocca_mezzo_non_disponibile(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonDisponibileException
        codice = f"TEST-SMN-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            svc = ServizioMobilita(db)
            with pytest.raises(MezzoNonDisponibileException):
                svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_mezzo_prenotato_senza_prenotazione(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonDisponibileException
        codice = f"TEST-SMX-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        try:
            svc = ServizioMobilita(db)
            with pytest.raises(MezzoNonDisponibileException):
                svc.sblocca_mezzo(_uuid.UUID(mezzo_id), utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)


# ── TestSbloccaMezzoHTTP ───────────────────────────────────────────────────

class TestSbloccaMezzoHTTP:

    @pytest.mark.integration
    def test_sblocca_disponibile_201(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            data = r.json()
            assert data["stato"] == "in_uso"
            assert str(data["mezzo_id"]) == mezzo_id
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_da_prenotazione_201(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        scade_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO prenotazioni (utente_id, mezzo_id, stato, scade_at)
                VALUES (:uid, :mid, 'attiva', :scade)
            """), {"uid": str(utente_test["id"]),
                   "mid": mezzo_id, "scade": scade_at})
            s.commit()
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            data = r.json()
            assert data["stato"] == "in_uso"
            assert data["prenotazione_id"] is not None
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_mezzo_in_uso_409(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_mezzo_prenotato_da_altri_409(self, db, utente_test):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Prenotato")
        try:
            import httpx
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sblocca_mezzo_inesistente_404(self, utente_test):
        import httpx
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.post(
            f"http://localhost:8000/utente/mezzi/{_uuid.uuid4()}/sblocca",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    @pytest.mark.integration
    def test_sblocca_non_autenticato_401(self, db):
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            import httpx
            r = httpx.post(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}/sblocca"
            )
            assert r.status_code == 401
        finally:
            _elimina_mezzo(db, mezzo_id)
