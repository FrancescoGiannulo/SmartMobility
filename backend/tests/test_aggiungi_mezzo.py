import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

LAT_BARI = 41.1177
LNG_BARI = 16.8719


def _inserisci_mezzo(db, codice: str, stato: str = "Disponibile") -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, :lat, :lng, 80)
        """), {"codice": codice, "stato": stato, "lat": LAT_BARI, "lng": LNG_BARI})
        s.commit()
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


class TestMezzoRepositoryAggiungi:

    @pytest.mark.integration
    def test_esiste_by_codice_trovato(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-EX-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            assert MezzoRepository(db).esiste_by_codice(codice) is True
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_esiste_by_codice_non_trovato(self, db):
        from dal.mezzo_repository import MezzoRepository
        assert MezzoRepository(db).esiste_by_codice(f"NOEXIST-{_uuid.uuid4().hex}") is False

    @pytest.mark.integration
    def test_crea_mezzo(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-CR-{_uuid.uuid4().hex[:6]}"
        repo = MezzoRepository(db)
        mezzo = repo.crea("monopattino", codice, LAT_BARI, LNG_BARI, "Disponibile")
        try:
            assert mezzo["codice"] == codice
            assert mezzo["tipo"] == "monopattino"
            assert mezzo["stato"] == "Disponibile"
            assert mezzo["lat"] == pytest.approx(LAT_BARI)
        finally:
            _elimina_mezzo(db, str(mezzo["id"]))

    @pytest.mark.integration
    def test_lista_tutti_esclude_dismessi(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice_disp = f"TEST-LD-{_uuid.uuid4().hex[:6]}"
        codice_dism = f"TEST-DI-{_uuid.uuid4().hex[:6]}"
        id_disp = _inserisci_mezzo(db, codice_disp, "Disponibile")
        id_dism = _inserisci_mezzo(db, codice_dism, "Dismesso")
        try:
            lista = MezzoRepository(db).lista_tutti()
            codici = [m["codice"] for m in lista]
            assert codice_disp in codici
            assert codice_dism not in codici
        finally:
            _elimina_mezzo(db, id_disp)
            _elimina_mezzo(db, id_dism)

    @pytest.mark.integration
    def test_ha_corse_attive_true(self, db, utente_test):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-CA-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        corsa_id = str(_uuid.uuid4())
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at)
                VALUES (:id, :uid, :mid, 'in_uso', now())
            """), {"id": corsa_id, "uid": str(utente_test["id"]), "mid": mezzo_id})
            s.commit()
        try:
            assert MezzoRepository(db).ha_corse_attive(_uuid.UUID(mezzo_id)) is True
        finally:
            with Session(db) as s:
                s.execute(text("DELETE FROM corse WHERE id = :id"), {"id": corsa_id})
                s.commit()
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_ha_corse_attive_false(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-CF-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            assert MezzoRepository(db).ha_corse_attive(_uuid.UUID(mezzo_id)) is False
        finally:
            _elimina_mezzo(db, mezzo_id)


class TestZonaRepositoryPunto:

    @pytest.mark.integration
    def test_punto_dentro_zona_operativa(self, db):
        from dal.zona_repository import ZonaRepository
        zona_id = None
        with Session(db) as s:
            row = s.execute(text("""
                INSERT INTO zone (nome, tipo, perimetro, limite_velocita)
                VALUES ('ZonaTestOP', 'operativa',
                    ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[16.8,41.0],[16.95,41.0],[16.95,41.2],[16.8,41.2],[16.8,41.0]]]}'),
                    NULL)
                RETURNING id
            """)).fetchone()
            s.commit()
            assert row is not None, "INSERT zone non ha restituito righe"
            zona_id = str(row.id)
        try:
            # lat=41.11, lng=16.87 è dentro il poligono
            assert ZonaRepository(db).punto_in_zona_operativa(41.11, 16.87) is True
        finally:
            with Session(db) as s:
                s.execute(text("DELETE FROM zone WHERE id = :id"), {"id": zona_id})
                s.commit()

    @pytest.mark.integration
    def test_punto_fuori_zona_operativa(self, db):
        from dal.zona_repository import ZonaRepository
        # Coordinate lontane da Bari (Roma)
        assert ZonaRepository(db).punto_in_zona_operativa(41.90, 12.49) is False
