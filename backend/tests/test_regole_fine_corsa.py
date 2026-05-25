import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session


# ── Helpers ────────────────────────────────────────────────────────────────

def _login(email: str, password: str) -> str:
    import httpx
    r = httpx.post("http://localhost:8000/auth/login",
                   json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _inserisci_zona_parcheggio(db, nome: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO zone (nome, tipo, perimetro)
            VALUES (:nome, 'parcheggio',
                    ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[16.87,41.11],[16.88,41.11],[16.88,41.12],[16.87,41.12],[16.87,41.11]]]}'))
        """), {"nome": nome})
        s.commit()
        row = s.execute(
            text("SELECT id FROM zone WHERE nome = :n"), {"n": nome}
        ).fetchone()
    return str(row.id)


def _elimina_zona(db, zona_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM regole_fine_corsa WHERE zona_parcheggio_id = :id"), {"id": zona_id})
        s.execute(text("DELETE FROM zone WHERE id = :id"), {"id": zona_id})
        s.commit()


def _pulisci_regole(db) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM regole_fine_corsa"))
        s.commit()


# ── TestRegolaFineCorsaRepository ─────────────────────────────────────────

class TestRegolaFineCorsaRepository:

    @pytest.mark.integration
    def test_crea_e_trova_tutte(self, db):
        from dal.regola_fine_corsa_repository import RegolaFineCorsaRepository
        nome = f"Z-TEST-{_uuid.uuid4().hex[:6]}"
        zona_id = _inserisci_zona_parcheggio(db, nome)
        try:
            repo = RegolaFineCorsaRepository(db)
            repo.crea(_uuid.UUID(zona_id), 20, 5.0, "penale")
            regole = repo.trova_tutte()
            assert any(r["zona_parcheggio_id"] == zona_id for r in regole)
        finally:
            _elimina_zona(db, zona_id)

    @pytest.mark.integration
    def test_elimina_tutto(self, db):
        from dal.regola_fine_corsa_repository import RegolaFineCorsaRepository
        nome = f"Z-TEST-{_uuid.uuid4().hex[:6]}"
        zona_id = _inserisci_zona_parcheggio(db, nome)
        try:
            repo = RegolaFineCorsaRepository(db)
            repo.crea(_uuid.UUID(zona_id), None, 0.0, "avviso")
            repo.elimina_tutto()
            assert repo.trova_tutte() == []
        finally:
            _elimina_zona(db, zona_id)


# ── TestServizioMobilitaRegole ─────────────────────────────────────────────

class TestServizioMobilitaRegole:

    @pytest.mark.integration
    def test_salva_regole_crea_una_per_zona(self, db, operatore_test):
        from bll.servizio_mobilita import ServizioMobilita
        nome = f"Z-SVC-{_uuid.uuid4().hex[:6]}"
        zona_id = _inserisci_zona_parcheggio(db, nome)
        try:
            svc = ServizioMobilita(db)
            svc.salva_regole_fine_corsa(
                operatore_test["id"], 30, 10, 1, "penale", 15, 3.0
            )
            from dal.regola_fine_corsa_repository import RegolaFineCorsaRepository
            regole = RegolaFineCorsaRepository(db).trova_tutte()
            assert any(r["zona_parcheggio_id"] == zona_id for r in regole)
            r = next(x for x in regole if x["zona_parcheggio_id"] == zona_id)
            assert r["tipo_vincolo"] == "penale"
            assert r["batteria_minima"] == 15
        finally:
            _elimina_zona(db, zona_id)
            _pulisci_regole(db)

    @pytest.mark.integration
    def test_get_zona_parcheggio_e_regole(self, db, operatore_test):
        from bll.servizio_mobilita import ServizioMobilita
        cfg = ServizioMobilita(db).get_zona_parcheggio_e_regole(operatore_test["id"])
        assert "durata_max_prenotazione_min" in cfg
        assert "tipo_vincolo" in cfg
        assert "zone_parcheggio" in cfg


# ── TestConfigurazioneFineCorsaHTTP ────────────────────────────────────────

class TestConfigurazioneFineCorsaHTTP:

    @pytest.mark.integration
    def test_get_configurazione_200(self, operatore_test):
        import httpx
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.get(
            "http://localhost:8000/operatore/configurazione/fine-corsa",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        assert "tipo_vincolo" in data
        assert "zone_parcheggio" in data

    @pytest.mark.integration
    def test_post_configurazione_201(self, db, operatore_test):
        import httpx
        nome = f"Z-HTTP-{_uuid.uuid4().hex[:6]}"
        zona_id = _inserisci_zona_parcheggio(db, nome)
        try:
            token = _login(operatore_test["email"], operatore_test["password"])
            r = httpx.post(
                "http://localhost:8000/operatore/configurazione/fine-corsa",
                json={
                    "durata_max_prenotazione_min": 30,
                    "durata_periodo_grazia_min": 10,
                    "max_mezzi_per_utente": 2,
                    "tipo_vincolo": "penale",
                    "batteria_minima": 20,
                    "penale_fuori_zona": 5.0,
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
        finally:
            _elimina_zona(db, zona_id)
            _pulisci_regole(db)

    @pytest.mark.integration
    def test_post_tipo_vincolo_non_valido_422(self, operatore_test):
        import httpx
        token = _login(operatore_test["email"], operatore_test["password"])
        r = httpx.post(
            "http://localhost:8000/operatore/configurazione/fine-corsa",
            json={
                "durata_max_prenotazione_min": 30,
                "durata_periodo_grazia_min": 10,
                "max_mezzi_per_utente": 1,
                "tipo_vincolo": "invalido",
                "batteria_minima": None,
                "penale_fuori_zona": 0.0,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 422

    @pytest.mark.integration
    def test_post_non_autenticato_401(self):
        import httpx
        r = httpx.post(
            "http://localhost:8000/operatore/configurazione/fine-corsa",
            json={
                "durata_max_prenotazione_min": 30,
                "durata_periodo_grazia_min": 10,
                "max_mezzi_per_utente": 1,
                "tipo_vincolo": "avviso",
                "batteria_minima": None,
                "penale_fuori_zona": 0.0,
            },
        )
        assert r.status_code == 401
