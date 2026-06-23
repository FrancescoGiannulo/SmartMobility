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
                v["tipo_configurazione"] in ("regole_fine_corsa_creata", "regole_fine_corsa_modificata")
                and v["operatore_id"] == str(operatore_id)
                for v in storico
            )
        finally:
            _pulisci(db, operatore_id)

    def test_prima_definizione_regole_fine_corsa_genera_evento_creata(self, db):
        from decimal import Decimal
        from bll.servizio_regole_fine_corsa import ServizioRegolaFinecorsa
        from dal.regola_fine_corsa_repository import RegoleFineCorsaRepository

        operatore_id = _uuid.uuid4()
        with Session(db) as session:
            regola_corrente = RegoleFineCorsaRepository().get_corrente(session)
        if regola_corrente is not None:
            pytest.skip("Esiste già una configurazione di regole fine corsa: impossibile testare la prima definizione")
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
                v["tipo_configurazione"] == "regole_fine_corsa_creata"
                and v["operatore_id"] == str(operatore_id)
                for v in storico
            )
        finally:
            _pulisci(db, operatore_id)

    def test_seconda_modifica_regole_fine_corsa_genera_evento_modificata(self, db):
        from decimal import Decimal
        from bll.servizio_regole_fine_corsa import ServizioRegolaFinecorsa

        operatore_id = _uuid.uuid4()
        try:
            with Session(db) as session:
                # prima chiamata: definisce (o ridefinisce) la configurazione corrente
                ServizioRegolaFinecorsa().salva(
                    tipo_vincolo="avviso",
                    penale_fuori_zona=Decimal("0"),
                    batteria_minima=None,
                    bonus_parcheggi_corretti=None,
                    bonus_valore=None,
                    db=session,
                    operatore_id=_uuid.uuid4(),
                )
            with Session(db) as session:
                # seconda chiamata: la configurazione esiste già → è una modifica
                ServizioRegolaFinecorsa().salva(
                    tipo_vincolo="penale",
                    penale_fuori_zona=Decimal("5"),
                    batteria_minima=None,
                    bonus_parcheggi_corretti=None,
                    bonus_valore=None,
                    db=session,
                    operatore_id=operatore_id,
                )
            storico = ServizioStoricoModifiche().get_storico()
            voce = next(
                v for v in storico
                if v["tipo_configurazione"] == "regole_fine_corsa_modificata"
                and v["operatore_id"] == str(operatore_id)
            )
            assert voce["valore_precedente"] != voce["valore_nuovo"], (
                "valore_precedente e valore_nuovo non devono essere identici dopo una modifica reale"
            )
            assert "tipo_vincolo=avviso" in voce["valore_precedente"]
            assert "tipo_vincolo=penale" in voce["valore_nuovo"]
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

    def test_crea_e_aggiorna_tariffa_registrano_modifica_nello_storico(self, db):
        # [IF-OP.07 / IF-OP.08] `tipo_mezzo` è un enum Postgres con soli 3 valori
        # (monopattino, bicicletta, automobile) già seedati in modo univoco
        # (migrazione 003_seed_tariffe.sql), quindi non è possibile creare una
        # tariffa con un tipo_mezzo arbitrario di test. Si usa "bicicletta":
        # si elimina temporaneamente la riga esistente per poter esercitare
        # crea_tariffa, poi si esercita aggiorna_tariffa, e infine si ripristinano
        # i valori originali del seed in teardown.
        from bll.servizio_tariffa import ServizioTariffa

        operatore_id = _uuid.uuid4()
        tipo_mezzo = "bicicletta"
        originale = None
        try:
            with Session(db) as session:
                originale = session.execute(
                    text(
                        "SELECT costo_al_minuto, costo_al_km FROM tariffe WHERE tipo_mezzo = :t"
                    ),
                    {"t": tipo_mezzo},
                ).fetchone()
                session.execute(text("DELETE FROM tariffe WHERE tipo_mezzo = :t"), {"t": tipo_mezzo})
                session.commit()

            ServizioTariffa().crea_tariffa(tipo_mezzo, 0.05, 0.10, operatore_id)
            ServizioTariffa().aggiorna_tariffa(tipo_mezzo, 0.07, 0.12, operatore_id)
            storico = ServizioStoricoModifiche().get_storico()
            tipi_evento = [
                v["tipo_configurazione"]
                for v in storico
                if v["operatore_id"] == str(operatore_id)
            ]
            assert "tariffa_creata" in tipi_evento
            assert "tariffa_modificata" in tipi_evento
        finally:
            _pulisci(db, operatore_id)
            with Session(db) as session:
                session.execute(text("DELETE FROM tariffe WHERE tipo_mezzo = :t"), {"t": tipo_mezzo})
                if originale is not None:
                    session.execute(
                        text(
                            "INSERT INTO tariffe (tipo_mezzo, costo_al_minuto, costo_al_km) "
                            "VALUES (:t, :minuto, :km) ON CONFLICT (tipo_mezzo) DO NOTHING"
                        ),
                        {"t": tipo_mezzo, "minuto": str(originale.costo_al_minuto), "km": str(originale.costo_al_km)},
                    )
                session.commit()

    def test_crea_modifica_ed_elimina_offerta_registrano_modifica_nello_storico(self, db):
        from decimal import Decimal
        from datetime import datetime, timedelta, timezone
        from bll.servizio_offerte import ServizioOfferta

        operatore_id = _uuid.uuid4()
        nome = f"OffertaTest-{operatore_id.hex[:6]}"
        try:
            with Session(db) as session:
                offerta = ServizioOfferta().crea_offerta(
                    nome=nome,
                    tipo="promozione",
                    descrizione="Test",
                    sconto_percentuale=Decimal("10"),
                    prezzo=None,
                    durata_giorni=None,
                    data_inizio=None,
                    data_scadenza=datetime.now(timezone.utc) + timedelta(days=1),
                    db=session,
                    operatore_id=operatore_id,
                )
            with Session(db) as session:
                ServizioOfferta().modifica_offerta(
                    offerta_id=offerta.id,
                    db=session,
                    operatore_id=operatore_id,
                    sconto_percentuale=Decimal("20"),
                )
            with Session(db) as session:
                ServizioOfferta().elimina_offerta(offerta.id, session, operatore_id=operatore_id)
            storico = ServizioStoricoModifiche().get_storico()
            tipi_evento = [
                v["tipo_configurazione"]
                for v in storico
                if v["operatore_id"] == str(operatore_id)
            ]
            assert "offerta_creata" in tipi_evento
            assert "offerta_modificata" in tipi_evento
            assert "offerta_eliminata" in tipi_evento
        finally:
            _pulisci(db, operatore_id)
            with Session(db) as session:
                session.execute(text("DELETE FROM offerte WHERE nome = :n"), {"n": nome})
                session.commit()
