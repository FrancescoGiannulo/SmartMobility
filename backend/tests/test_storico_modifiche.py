"""[IF-OP.13] Test Mostra Storico Modifiche — repository, servizio e controller."""
import uuid as _uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from dal.storico_modifiche_repository import StoricoModificheRepository
from bll.servizio_storico_modifiche import ServizioStoricoModifiche
from main import app

http = TestClient(app)


def _pulisci(db, operatore_id):
    with Session(db) as s:
        s.execute(
            text("DELETE FROM storico_modifiche WHERE operatore_id = :id"),
            {"id": str(operatore_id)},
        )
        s.commit()


@pytest.mark.integration
class TestStoricoModificheRepository:

    def test_crea_e_find_all_restituisce_la_voce_inserita(self, db):
        operatore_id = _uuid.uuid4()
        repo = StoricoModificheRepository()
        try:
            voce = repo.crea(
                tipo_configurazione="parametri_sistema",
                descrizione="Aggiornamento parametri di sistema",
                valore_precedente="durata_max_prenotazione_min=15",
                valore_nuovo="durata_max_prenotazione_min=30",
                operatore_id=operatore_id,
            )
            assert voce.tipo_configurazione == "parametri_sistema"

            storico = repo.find_all()
            trovata = next((v for v in storico if v.id == voce.id), None)
            assert trovata is not None
            assert trovata.descrizione == "Aggiornamento parametri di sistema"
            assert trovata.valore_precedente == "durata_max_prenotazione_min=15"
            assert trovata.valore_nuovo == "durata_max_prenotazione_min=30"
            assert trovata.operatore_id == operatore_id
        finally:
            _pulisci(db, operatore_id)

    def test_find_all_ordina_dalla_piu_recente(self, db):
        operatore_id = _uuid.uuid4()
        repo = StoricoModificheRepository()
        try:
            prima = repo.crea(
                tipo_configurazione="parametri_sistema",
                descrizione="Prima modifica",
                valore_precedente=None,
                valore_nuovo=None,
                operatore_id=operatore_id,
            )
            seconda = repo.crea(
                tipo_configurazione="parametri_sistema",
                descrizione="Seconda modifica",
                valore_precedente=None,
                valore_nuovo=None,
                operatore_id=operatore_id,
            )
            storico = repo.find_all()
            ids = [v.id for v in storico]
            assert ids.index(seconda.id) < ids.index(prima.id)
        finally:
            _pulisci(db, operatore_id)


@pytest.mark.integration
class TestServizioStoricoModifiche:

    def test_registra_modifica_e_get_storico(self, db):
        operatore_id = _uuid.uuid4()
        servizio = ServizioStoricoModifiche()
        try:
            servizio.registra_modifica(
                tipo_configurazione="regole_fine_corsa",
                descrizione="Modifica regole di fine corsa",
                valore_precedente="tipo_vincolo=avviso",
                valore_nuovo="tipo_vincolo=penale",
                operatore_id=operatore_id,
            )
            storico = servizio.get_storico()
            assert any(
                v["descrizione"] == "Modifica regole di fine corsa"
                and v["operatore_id"] == str(operatore_id)
                for v in storico
            )
        finally:
            _pulisci(db, operatore_id)


class TestStoricoModificheControllerAuth:

    def test_get_storico_modifiche_non_autenticato(self):
        """[IIN-2] GET senza token → 401."""
        resp = http.get("/operatore/storico-modifiche")
        assert resp.status_code == 401


@pytest.mark.integration
class TestIntegrazioneServiziEsistenti:
    """[IF-OP.13] I servizi che modificano configurazioni registrano la modifica nello storico."""

    def test_aggiorna_parametri_registra_modifica_nello_storico(self, db):
        from bll.servizio_parametri import ServizioParametri

        from decimal import Decimal

        operatore_id = _uuid.uuid4()
        try:
            with Session(db) as session:
                ServizioParametri().aggiorna_parametri(
                    durata_max_prenotazione_min=20,
                    durata_periodo_grazia_min=5,
                    max_mezzi_per_utente=2,
                    addebito_pausa_min=Decimal("0"),
                    db=session,
                    operatore_id=operatore_id,
                )
            storico = ServizioStoricoModifiche().get_storico()
            assert any(
                v["tipo_configurazione"] == "parametri_sistema"
                and v["operatore_id"] == str(operatore_id)
                for v in storico
            )
        finally:
            _pulisci(db, operatore_id)

    def test_salva_regole_fine_corsa_registra_modifica_nello_storico(self, db):
        from decimal import Decimal
        from bll.servizio_regole_fine_corsa import ServizioRegolaFinecorsa

        operatore_id = _uuid.uuid4()
        try:
            with Session(db) as session:
                ServizioRegolaFinecorsa().salva(
                    tipo_vincolo="avviso",
                    penale_fuori_zona=Decimal("0"),
                    batteria_minima=None,
                    bonus_parcheggi_corretti=None,
                    bonus_valore=None,
                    db=session,
                    operatore_id=operatore_id,
                )
            storico = ServizioStoricoModifiche().get_storico()
            assert any(
                v["tipo_configurazione"] == "regole_fine_corsa"
                and v["operatore_id"] == str(operatore_id)
                for v in storico
            )
        finally:
            _pulisci(db, operatore_id)

    def test_crea_ed_elimina_zona_registrano_modifica_nello_storico(self, db):
        from bll.servizio_mappa import ServizioMappa

        operatore_id = _uuid.uuid4()
        nome_zona = f"ZonaTest-{operatore_id}"
        coordinate = [[45.0, 9.0], [45.0, 9.01], [45.01, 9.01], [45.01, 9.0]]
        try:
            with Session(db) as session:
                zona = ServizioMappa(session).crea_zona(
                    nome=nome_zona,
                    tipo="operativa",
                    coordinate=coordinate,
                    limite_velocita=None,
                    operatore_id=operatore_id,
                )
            with Session(db) as session:
                ServizioMappa(session).elimina_zona(
                    zona_id=zona["id"],
                    operatore_id=operatore_id,
                )
            storico = ServizioStoricoModifiche().get_storico()
            tipi_evento = [
                v["tipo_configurazione"]
                for v in storico
                if v["operatore_id"] == str(operatore_id)
            ]
            assert "zona_creata" in tipi_evento
            assert "zona_eliminata" in tipi_evento
        finally:
            _pulisci(db, operatore_id)
            with Session(db) as session:
                session.execute(text("DELETE FROM zone WHERE nome = :n"), {"n": nome_zona})
                session.commit()
