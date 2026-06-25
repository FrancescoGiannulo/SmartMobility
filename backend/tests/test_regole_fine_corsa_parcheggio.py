"""[IF-OP.13] Test enforcement parcheggio a fine corsa + bonus parcheggi corretti."""
import uuid as _uuid
from decimal import Decimal
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from dal.zona_repository import ZonaRepository
from dal.regola_fine_corsa_repository import RegoleFineCorsaRepository
from bll.servizio_mobilita import ServizioMobilita, ParcheggioVietatoException

# Punto dentro la zona di parcheggio di test
LAT_DENTRO, LNG_DENTRO = 41.111, 16.851
# Punto fuori da qualsiasi zona di parcheggio di test
LAT_FUORI, LNG_FUORI = 41.200, 16.950

ZONA_COORD = [
    [16.85, 41.11], [16.86, 41.11],
    [16.86, 41.12], [16.85, 41.12], [16.85, 41.11],
]


def _inserisci_mezzo(db, codice: str, lat: float, lng: float) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', 'In uso', :lat, :lng, 80)
        """), {"codice": codice, "lat": lat, "lng": lng})
        s.commit()
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
    return str(row.id)


def _crea_corsa(db, utente_id: str, mezzo_id: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO corse (utente_id, mezzo_id, stato, inizio_at)
            VALUES (:uid, :mid, 'in_uso', NOW())
        """), {"uid": utente_id, "mid": mezzo_id})
        s.commit()
        row = s.execute(
            text("SELECT id FROM corse WHERE utente_id = :uid AND mezzo_id = :mid ORDER BY inizio_at DESC LIMIT 1"),
            {"uid": utente_id, "mid": mezzo_id},
        ).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


def _reset_utente_bonus(db, utente_id) -> None:
    with Session(db) as s:
        s.execute(
            text("UPDATE utenti SET contatore_parcheggi_corretti = 0, credito_bonus = 0 WHERE id = :id"),
            {"id": str(utente_id)},
        )
        s.commit()


@pytest.fixture
def zona_parcheggio_test(db):
    repo = ZonaRepository(db)
    zona = repo.crea("test_parcheggio_fine_corsa", "parcheggio", ZONA_COORD, None)
    yield zona
    repo.elimina(zona.id)


@pytest.fixture
def regola_originale(db):
    """Salva la regola corrente e la ripristina a fine test (config globale condivisa)."""
    with Session(db) as s:
        originale = RegoleFineCorsaRepository().get_corrente(s)
        valori = None
        if originale is not None:
            valori = dict(
                tipo_vincolo=originale.tipo_vincolo,
                penale_fuori_zona=originale.penale_fuori_zona,
                batteria_minima=originale.batteria_minima,
                bonus_parcheggi_corretti=originale.bonus_parcheggi_corretti,
                bonus_valore=originale.bonus_valore,
            )
    yield
    with Session(db) as s:
        if valori is not None:
            RegoleFineCorsaRepository().salva(db=s, **valori)
        else:
            s.execute(text("DELETE FROM regole_fine_corsa"))
            s.commit()


def _imposta_regola(db, tipo_vincolo: str, penale_fuori_zona=Decimal("0"), bonus_n=None, bonus_valore=None):
    from model.regola_fine_corsa import TipoVincoloFinecorsa
    with Session(db) as s:
        RegoleFineCorsaRepository().salva(
            tipo_vincolo=TipoVincoloFinecorsa(tipo_vincolo),
            penale_fuori_zona=penale_fuori_zona,
            batteria_minima=None,
            bonus_parcheggi_corretti=bonus_n,
            bonus_valore=bonus_valore,
            db=s,
        )


@pytest.mark.integration
class TestEnforcementParcheggioFineCorsa:

    def test_nessuna_zona_parcheggio_nessun_effetto(self, db, utente_test, monkeypatch):
        """Scenario alternativo: senza zone di parcheggio configurate, termina_corsa non verifica nulla.
        Mocka esiste_zona_parcheggio_attiva perché nel DB condiviso possono già esisterne altre."""
        from dal.zona_repository import ZonaRepository
        monkeypatch.setattr(ZonaRepository, "esiste_zona_parcheggio_attiva", lambda self: False)
        codice = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, LAT_FUORI, LNG_FUORI)
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
        try:
            esito = ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa_id), utente_test["id"])
            assert esito["avviso_parcheggio"] is None
            with Session(db) as s:
                row = s.execute(text("SELECT stato FROM corse WHERE id = :id"), {"id": corsa_id}).fetchone()
            assert row.stato == "terminata"
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_avviso_parcheggio_scorretto_corsa_termina(self, db, utente_test, zona_parcheggio_test, regola_originale):
        """tipo_vincolo=avviso: corsa termina comunque, con messaggio informativo."""
        _imposta_regola(db, "avviso")
        codice = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, LAT_FUORI, LNG_FUORI)
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
        try:
            esito = ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa_id), utente_test["id"])
            assert esito["avviso_parcheggio"] is not None
            with Session(db) as s:
                row = s.execute(text("SELECT stato, penale_parcheggio_applicata FROM corse WHERE id = :id"), {"id": corsa_id}).fetchone()
            assert row.stato == "terminata"
            assert row.penale_parcheggio_applicata is False
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_penale_parcheggio_scorretto_marcata_su_corsa(self, db, utente_test, zona_parcheggio_test, regola_originale):
        """tipo_vincolo=penale: corsa termina, penale_parcheggio_applicata=True per il pagamento."""
        _imposta_regola(db, "penale", penale_fuori_zona=Decimal("3.50"))
        codice = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, LAT_FUORI, LNG_FUORI)
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
        try:
            ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa_id), utente_test["id"])
            with Session(db) as s:
                row = s.execute(text("SELECT penale_parcheggio_applicata FROM corse WHERE id = :id"), {"id": corsa_id}).fetchone()
            assert row.penale_parcheggio_applicata is True
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_divieto_blocca_terminazione(self, db, utente_test, zona_parcheggio_test, regola_originale):
        """tipo_vincolo=divieto: termina_corsa rifiuta, la corsa resta in_uso."""
        _imposta_regola(db, "divieto")
        codice = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, LAT_FUORI, LNG_FUORI)
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
        try:
            with pytest.raises(ParcheggioVietatoException):
                ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa_id), utente_test["id"])
            with Session(db) as s:
                row = s.execute(text("SELECT stato FROM corse WHERE id = :id"), {"id": corsa_id}).fetchone()
            assert row.stato == "in_uso"
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_parcheggio_corretto_nessuna_penale_nessun_blocco(self, db, utente_test, zona_parcheggio_test, regola_originale):
        """Parcheggiato correttamente: la corsa termina sempre, qualunque sia tipo_vincolo."""
        _imposta_regola(db, "divieto")
        codice = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, LAT_DENTRO, LNG_DENTRO)
        corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
        try:
            esito = ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa_id), utente_test["id"])
            assert esito["avviso_parcheggio"] is None
            with Session(db) as s:
                row = s.execute(text("SELECT stato FROM corse WHERE id = :id"), {"id": corsa_id}).fetchone()
            assert row.stato == "terminata"
        finally:
            _elimina_mezzo(db, mezzo_id)

    def test_bonus_accreditato_al_raggiungimento_soglia(self, db, utente_test, zona_parcheggio_test, regola_originale):
        """Due parcheggi corretti di fila con soglia=2 → credito_bonus accreditato e contatore azzerato."""
        _imposta_regola(db, "avviso", bonus_n=2, bonus_valore=Decimal("1.00"))
        _reset_utente_bonus(db, utente_test["id"])
        mezzo_ids = []
        try:
            for _ in range(2):
                codice = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
                mezzo_id = _inserisci_mezzo(db, codice, LAT_DENTRO, LNG_DENTRO)
                mezzo_ids.append(mezzo_id)
                corsa_id = _crea_corsa(db, str(utente_test["id"]), mezzo_id)
                ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa_id), utente_test["id"])

            with Session(db) as s:
                row = s.execute(
                    text("SELECT contatore_parcheggi_corretti, credito_bonus FROM utenti WHERE id = :id"),
                    {"id": str(utente_test["id"])},
                ).fetchone()
            assert row.contatore_parcheggi_corretti == 0
            assert Decimal(str(row.credito_bonus)) == Decimal("1.00")
        finally:
            for mid in mezzo_ids:
                _elimina_mezzo(db, mid)
            _reset_utente_bonus(db, utente_test["id"])

    def test_parcheggio_scorretto_azzera_contatore_consecutivo(self, db, utente_test, zona_parcheggio_test, regola_originale):
        """Serie consecutiva: un parcheggio scorretto in mezzo azzera il progresso verso il bonus."""
        _imposta_regola(db, "avviso", bonus_n=2, bonus_valore=Decimal("1.00"))
        _reset_utente_bonus(db, utente_test["id"])
        mezzo_ids = []
        try:
            codice1 = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
            mezzo1 = _inserisci_mezzo(db, codice1, LAT_DENTRO, LNG_DENTRO)
            mezzo_ids.append(mezzo1)
            corsa1 = _crea_corsa(db, str(utente_test["id"]), mezzo1)
            ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa1), utente_test["id"])

            codice2 = f"TEST-PARK-{_uuid.uuid4().hex[:6]}"
            mezzo2 = _inserisci_mezzo(db, codice2, LAT_FUORI, LNG_FUORI)
            mezzo_ids.append(mezzo2)
            corsa2 = _crea_corsa(db, str(utente_test["id"]), mezzo2)
            ServizioMobilita(db).termina_corsa(_uuid.UUID(corsa2), utente_test["id"])

            with Session(db) as s:
                row = s.execute(
                    text("SELECT contatore_parcheggi_corretti, credito_bonus FROM utenti WHERE id = :id"),
                    {"id": str(utente_test["id"])},
                ).fetchone()
            assert row.contatore_parcheggi_corretti == 0
            assert Decimal(str(row.credito_bonus)) == Decimal("0.00")
        finally:
            for mid in mezzo_ids:
                _elimina_mezzo(db, mid)
            _reset_utente_bonus(db, utente_test["id"])
