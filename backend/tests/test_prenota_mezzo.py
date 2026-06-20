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


def _inserisci_mezzo(db, codice: str, stato: str, lat: float = 41.11, lng: float = 16.85) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, :lat, :lng, 80)
        """), {"codice": codice, "stato": stato, "lat": lat, "lng": lng})
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


# ── TestMezzoRepository.trova_disponibili_da_lista ────────────────────────

class TestTrovaDisponibiliDaLista:

    @pytest.mark.integration
    def test_restituisce_solo_disponibili(self, db, utente_test):
        from dal.mezzo_repository import MezzoRepository
        codice_disp = f"TEST-DISP-{_uuid.uuid4().hex[:6]}"
        codice_occ = f"TEST-OCC-{_uuid.uuid4().hex[:6]}"
        id_disp = _inserisci_mezzo(db, codice_disp, "Disponibile")
        id_occ = _inserisci_mezzo(db, codice_occ, "In uso")
        try:
            repo = MezzoRepository(db)
            risultato = repo.trova_disponibili_da_lista(
                [_uuid.UUID(id_disp), _uuid.UUID(id_occ)]
            )
            ids = {r["id"] for r in risultato}
            assert id_disp in ids
            assert id_occ not in ids
        finally:
            _elimina_mezzo(db, id_disp)
            _elimina_mezzo(db, id_occ)


# ── TestServizioPrenotazione ───────────────────────────────────────────────

class TestServizioPrenotazione:

    @pytest.mark.integration
    def test_crea_prenotazioni_tutti_disponibili(self, db, utente_test):
        from bll.servizio_prenotazione import ServizioPrenotazione
        c1 = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        c2 = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        id1 = _inserisci_mezzo(db, c1, "Disponibile")
        id2 = _inserisci_mezzo(db, c2, "Disponibile")
        try:
            svc = ServizioPrenotazione(db)
            prens = svc.crea_prenotazioni(
                [_uuid.UUID(id1), _uuid.UUID(id2)], utente_test["id"]
            )
            assert len(prens) == 2
            for p in prens:
                assert p["stato"] == "attiva"
            # verifica stato mezzi aggiornato
            with Session(db) as s:
                for mid in [id1, id2]:
                    row = s.execute(
                        text("SELECT stato FROM mezzi WHERE id = :id"), {"id": mid}
                    ).fetchone()
                    assert row.stato == "Prenotato"
        finally:
            _elimina_mezzo(db, id1)
            _elimina_mezzo(db, id2)

    @pytest.mark.integration
    def test_crea_prenotazioni_un_mezzo_non_disponibile(self, db, utente_test):
        from bll.servizio_prenotazione import (
            ServizioPrenotazione, AlcuniMezziNonDisponibiliException
        )
        c1 = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        c2 = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        id1 = _inserisci_mezzo(db, c1, "Disponibile")
        id2 = _inserisci_mezzo(db, c2, "In uso")
        try:
            svc = ServizioPrenotazione(db)
            with pytest.raises(AlcuniMezziNonDisponibiliException) as exc_info:
                svc.crea_prenotazioni(
                    [_uuid.UUID(id1), _uuid.UUID(id2)], utente_test["id"]
                )
            assert id2 in exc_info.value.non_disponibili
            # id1 deve essere ancora Disponibile (nessun booking parziale)
            with Session(db) as s:
                row = s.execute(
                    text("SELECT stato FROM mezzi WHERE id = :id"), {"id": id1}
                ).fetchone()
            assert row.stato == "Disponibile"
        finally:
            _elimina_mezzo(db, id1)
            _elimina_mezzo(db, id2)

    @pytest.mark.integration
    def test_crea_prenotazioni_mezzo_fuori_raggio_gruppo(self, db, utente_test):
        # [IF-UT.02] CS-04 — il primo mezzo è il riferimento; un secondo mezzo
        # troppo lontano (oltre RAGGIO_GRUPPO_KM) non può entrare nel gruppo
        from bll.servizio_prenotazione import (
            ServizioPrenotazione, MezziFuoriRaggioGruppoException
        )
        c1 = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        c2 = f"TEST-SVC-{_uuid.uuid4().hex[:6]}"
        id1 = _inserisci_mezzo(db, c1, "Disponibile")  # Bari (riferimento)
        id2 = _inserisci_mezzo(db, c2, "Disponibile", lat=41.9028, lng=12.4964)  # Roma (~375 km)
        try:
            svc = ServizioPrenotazione(db)
            with pytest.raises(MezziFuoriRaggioGruppoException) as exc_info:
                svc.crea_prenotazioni(
                    [_uuid.UUID(id1), _uuid.UUID(id2)], utente_test["id"]
                )
            assert id2 in exc_info.value.fuori_raggio
            # nessun booking parziale: entrambi restano Disponibile
            with Session(db) as s:
                for mid in [id1, id2]:
                    row = s.execute(
                        text("SELECT stato FROM mezzi WHERE id = :id"), {"id": mid}
                    ).fetchone()
                    assert row.stato == "Disponibile"
        finally:
            _elimina_mezzo(db, id1)
            _elimina_mezzo(db, id2)

    @pytest.mark.integration
    def test_crea_prenotazioni_mezzo_non_trovato(self, db, utente_test):
        from bll.servizio_prenotazione import (
            ServizioPrenotazione, AlcuniMezziNonDisponibiliException
        )
        svc = ServizioPrenotazione(db)
        # UUID inesistente viene trattato come non disponibile
        with pytest.raises(AlcuniMezziNonDisponibiliException):
            svc.crea_prenotazioni([_uuid.uuid4()], utente_test["id"])

    @pytest.mark.integration
    def test_limite_mezzi_superato(self, db, utente_test):
        from bll.servizio_prenotazione import (
            ServizioPrenotazione, LimiteMezziSuperatoException
        )
        svc = ServizioPrenotazione(db)
        troppi_ids = [_uuid.uuid4() for _ in range(10)]
        with pytest.raises(LimiteMezziSuperatoException):
            svc.crea_prenotazioni(troppi_ids, utente_test["id"], n_max=3)


# ── TestPrenotaMezzoHTTP ──────────────────────────────────────────────────

class TestPrenotaMezzoHTTP:

    @pytest.mark.integration
    def test_prenota_singolo_mezzo_201(self, db, utente_test):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_ids": [mezzo_id]},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            data = r.json()
            assert "prenotazioni" in data
            assert len(data["prenotazioni"]) == 1
            assert data["prenotazioni"][0]["stato"] == "attiva"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_prenota_piu_mezzi_201(self, db, utente_test):
        import httpx
        c1 = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        c2 = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        id1 = _inserisci_mezzo(db, c1, "Disponibile")
        id2 = _inserisci_mezzo(db, c2, "Disponibile")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_ids": [id1, id2]},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            data = r.json()
            assert len(data["prenotazioni"]) == 2
        finally:
            _elimina_mezzo(db, id1)
            _elimina_mezzo(db, id2)

    @pytest.mark.integration
    def test_prenota_mezzo_non_disponibile_409(self, db, utente_test):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_ids": [mezzo_id]},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
            detail = r.json()["detail"]
            assert mezzo_id in detail["non_disponibili"]
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_prenota_parziale_409(self, db, utente_test):
        """CS-04.01: un mezzo disponibile + uno non disponibile → 409, nessuno prenotato."""
        import httpx
        c1 = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        c2 = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        id_ok = _inserisci_mezzo(db, c1, "Disponibile")
        id_ko = _inserisci_mezzo(db, c2, "Prenotato")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_ids": [id_ok, id_ko]},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
            detail = r.json()["detail"]
            assert id_ko in detail["non_disponibili"]
            # id_ok non deve essere stato prenotato
            with Session(db) as s:
                row = s.execute(
                    text("SELECT stato FROM mezzi WHERE id = :id"), {"id": id_ok}
                ).fetchone()
            assert row.stato == "Disponibile"
        finally:
            _elimina_mezzo(db, id_ok)
            _elimina_mezzo(db, id_ko)

    @pytest.mark.integration
    def test_prenota_non_autenticato_401(self, db):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            r = httpx.post(
                "http://localhost:8000/utente/prenotazioni",
                json={"mezzo_ids": [mezzo_id]},
            )
            assert r.status_code == 401
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_get_caratteristiche_mezzo_200(self, db, utente_test):
        import httpx
        codice = f"TEST-HTTP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            token = _login(utente_test["email"], utente_test["password"])
            r = httpx.get(
                f"http://localhost:8000/utente/mezzi/{mezzo_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200, r.text
            data = r.json()
            assert data["id"] == mezzo_id
            assert data["codice"] == codice
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_get_caratteristiche_mezzo_inesistente_404(self, utente_test):
        import httpx
        token = _login(utente_test["email"], utente_test["password"])
        r = httpx.get(
            f"http://localhost:8000/utente/mezzi/{_uuid.uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404