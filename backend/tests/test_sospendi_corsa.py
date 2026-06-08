"""[IF-UT.10] Test sospendi corsa — scenario base e scenari alternativi."""
import pytest
import uuid as _uuid
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session

LAT_TEST = 41.11
LNG_TEST = 16.85


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
            VALUES (:codice, 'monopattino', :stato, :lat, :lng, 80)
        """), {"codice": codice, "stato": stato, "lat": LAT_TEST, "lng": LNG_TEST})
        s.commit()
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
    return str(row.id)


def _crea_corsa(db, utente_id: str, mezzo_id: str, stato: str = "in_uso", pausa_accumulata_sec: int = 0) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO corse (utente_id, mezzo_id, stato, inizio_at, pausa_durata_accumulata_sec)
            VALUES (:uid, :mid, :stato, NOW(), :pausa)
        """), {"uid": utente_id, "mid": mezzo_id, "stato": stato, "pausa": pausa_accumulata_sec})
        s.commit()
        row = s.execute(
            text("SELECT id FROM corse WHERE utente_id = :uid AND mezzo_id = :mid ORDER BY inizio_at DESC LIMIT 1"),
            {"uid": utente_id, "mid": mezzo_id},
        ).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM prenotazioni WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


def _get_parametri_grazia(db) -> int:
    """Restituisce durata_periodo_grazia_min dai parametri di sistema."""
    with Session(db) as s:
        row = s.execute(text("SELECT durata_periodo_grazia_min FROM parametri_sistema LIMIT 1")).fetchone()
    return int(row.durata_periodo_grazia_min) if row else 5


# ── TestSospendiCorsa (BLL) ───────────────────────────────────────────────

class TestSospendiCorsa:

    @pytest.mark.integration
    def test_scenario_base_corsa_in_uso(self, db, utente_test):
        """Scenario base: corsa in_uso → sospesa, mezzo In pausa, risposta con grace period."""
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SC-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
        try:
            svc = ServizioMobilita(db)
            risposta = svc.sospendiCorsa(_uuid.UUID(corsa_id), utente_test["id"])

            assert risposta["stato"] == "in_pausa"
            assert isinstance(risposta["tempo_gratuito_residuo_sec"], (int, float))
            assert risposta["tempo_gratuito_residuo_sec"] >= 0
            assert isinstance(risposta["addebito_pausa_min"], float)
            assert isinstance(risposta["periodo_grazia_scaduto"], bool)

            with Session(db) as s:
                mezzo_row = s.execute(text("SELECT stato FROM mezzi WHERE id = :id"), {"id": mezzo_id}).fetchone()
                corsa_row = s.execute(text("SELECT stato FROM corse WHERE id = :id"), {"id": corsa_id}).fetchone()
            assert mezzo_row.stato == "In pausa"
            assert corsa_row.stato == "in_pausa"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_grace_period_integro_pausa_zero(self, db, utente_test):
        """Prima pausa: pausa_accumulata=0 → tempo_gratuito_residuo == grazia totale."""
        from bll.servizio_mobilita import ServizioMobilita
        grazia_min = _get_parametri_grazia(db)
        codice = f"TEST-GZ-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id, pausa_accumulata_sec=0)
        try:
            risposta = ServizioMobilita(db).sospendiCorsa(_uuid.UUID(corsa_id), utente_test["id"])
            assert risposta["tempo_gratuito_residuo_sec"] == grazia_min * 60
            assert risposta["periodo_grazia_scaduto"] is False
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_periodo_grazia_scaduto_pausa_accumulata_supera_grazia(self, db, utente_test):
        """opt [periodo di grazia scaduto]: pausa accumulata >= grazia → periodo_grazia_scaduto=True, residuo=0."""
        from bll.servizio_mobilita import ServizioMobilita
        grazia_min = _get_parametri_grazia(db)
        pausa_accumulata = grazia_min * 60 + 60  # già oltre la grazia
        codice = f"TEST-PG-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id, pausa_accumulata_sec=pausa_accumulata)
        try:
            risposta = ServizioMobilita(db).sospendiCorsa(_uuid.UUID(corsa_id), utente_test["id"])
            assert risposta["periodo_grazia_scaduto"] is True
            assert risposta["tempo_gratuito_residuo_sec"] == 0
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_corsa_non_trovata_eccezione(self, db, utente_test):
        """Scenario alternativo: corsa inesistente → CorsaNonTrovataException."""
        from bll.servizio_mobilita import ServizioMobilita, CorsaNonTrovataException
        with pytest.raises(CorsaNonTrovataException):
            ServizioMobilita(db).sospendiCorsa(_uuid.uuid4(), utente_test["id"])

    @pytest.mark.integration
    def test_corsa_non_in_uso_eccezione(self, db, utente_test):
        """Scenario alternativo: corsa non in_uso (es. terminata) → CorsaNonInUsaException."""
        from bll.servizio_mobilita import ServizioMobilita, CorsaNonInUsaException
        codice = f"TEST-NU-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id, stato="terminata")
        try:
            with pytest.raises(CorsaNonInUsaException):
                ServizioMobilita(db).sospendiCorsa(_uuid.UUID(corsa_id), utente_test["id"])
        finally:
            _elimina_mezzo(db, mezzo_id)


# ── TestSospendiCorsaHTTP ─────────────────────────────────────────────────

class TestSospendiCorsaHTTP:

    @pytest.mark.integration
    def test_sospendi_200_con_grace_period(self, db, utente_test):
        """HTTP scenario base: POST /utente/corse/{id}/pausa → 200 con grace period."""
        import httpx
        codice = f"TEST-HTTP-SC-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/corse/{corsa_id}/pausa",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            data = r.json()
            assert data["stato"] == "in_pausa"
            assert "tempo_gratuito_residuo_sec" in data
            assert "addebito_pausa_min" in data
            assert "periodo_grazia_scaduto" in data
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_sospendi_non_autenticato_401(self, db):
        """Scenario alternativo: senza token → 401."""
        import httpx
        r = httpx.post(f"http://localhost:8000/utente/corse/{_uuid.uuid4()}/pausa")
        assert r.status_code == 401

    @pytest.mark.integration
    def test_sospendi_corsa_inesistente_404(self, db, utente_test):
        """Scenario alternativo: corsa non trovata → 404."""
        import httpx
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.post(
            f"http://localhost:8000/utente/corse/{_uuid.uuid4()}/pausa",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    @pytest.mark.integration
    def test_sospendi_corsa_non_in_uso_409(self, db, utente_test):
        """Scenario alternativo: corsa in stato terminata → 409 Conflict."""
        import httpx
        codice = f"TEST-HTTP-NU-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id, stato="terminata")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                f"http://localhost:8000/utente/corse/{corsa_id}/pausa",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, mezzo_id)
