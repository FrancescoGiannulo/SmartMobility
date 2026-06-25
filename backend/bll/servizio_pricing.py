import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from dal.pagamento_repository import PagamentoRepository, MetodoNonTrovatoException
from dal.tariffa_repository import TariffaRepository
from dal.promozione_repository import PromozioneRepository
from dal.abbonamento_repository import AbbonamentoRepository
from dal.corsa_repository import CorsaRepository
from dal.parametri_sistema_repository import ParametriSistemaRepository
from model.offerta import Offerta
from model.pagamento import StatoPagamento
from providers.provider_pagamenti import ProviderPagamentiStub, DatiNonValidiException
from bll.servizio_tariffa import TariffaNonTrovata  # re-export per compatibilità


class MetodoNonTrovato(Exception):
    pass


class MetodoDuplicato(Exception):
    pass


class DatiNonValidi(Exception):
    pass


class NessunMetodoPredefinito(Exception):
    pass


class PagamentoRifiutato(Exception):
    pass


class ServizioPricing:

    def __init__(
        self,
        db: Session | None = None,
        repo: PagamentoRepository | None = None,
        provider: ProviderPagamentiStub | None = None,
        tariffa_repo: TariffaRepository | None = None,
    ):
        self._db = db
        self._repo = repo or PagamentoRepository()
        self._provider = provider or ProviderPagamentiStub()
        self._tariffa_repo = tariffa_repo or TariffaRepository(db)
        self._promozione_repo = PromozioneRepository(db)

    # [IF-UT.05] — db injection pattern
    def getTariffe(self) -> list[dict]:
        return self._tariffa_repo.findAll()

    # [IF-UT.13] — db injection pattern
    def getPromozioniAttive(self) -> list[dict]:
        return self._promozione_repo.getAttive()

    def calcola_importo(self, tipo_mezzo: str, durata_min: float, distanza_km: float) -> Decimal:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT costo_al_minuto, costo_al_km FROM tariffe WHERE tipo_mezzo = :tipo"
                ),
                {"tipo": tipo_mezzo},
            ).fetchone()
        if not row:
            raise TariffaNonTrovata(f"Nessuna tariffa per {tipo_mezzo}")
        return Decimal(str(durata_min)) * row.costo_al_minuto + Decimal(str(distanza_km)) * row.costo_al_km

    # [IF-UT.06] Salva Metodi di Pagamento
    def aggiungi_metodo(self, utente_id: uuid.UUID, tipo: str, dati: dict) -> dict:
        try:
            token = self._provider.valida_dati_pagamento(tipo, dati)
        except DatiNonValidiException as exc:
            raise DatiNonValidi(str(exc)) from exc

        if self._repo.exists_by_token(token, utente_id):
            raise MetodoDuplicato("Metodo di pagamento già presente")

        last_four = None
        if tipo == "carta":
            numero = (dati.get("numero") or "").replace(" ", "")
            last_four = numero[-4:] if len(numero) >= 4 else None

        metodo = self._repo.aggiungi_metodo(utente_id, tipo, token, last_four)
        return {
            "id": str(metodo.id),
            "tipo": metodo.tipo,
            "last_four": metodo.last_four,
            "predefinito": metodo.predefinito,
        }

    def lista_metodi(self, utente_id: uuid.UUID) -> list[dict]:
        metodi = self._repo.lista_metodi(utente_id)
        return [
            {
                "id": str(m.id),
                "tipo": m.tipo,
                "last_four": m.last_four,
                "predefinito": m.predefinito,
            }
            for m in metodi
        ]

    # [IF-UT.21] Imposta Metodo di Pagamento predefinito
    def imposta_predefinito(self, metodo_id: uuid.UUID, utente_id: uuid.UUID) -> None:
        try:
            self._repo.trova_metodo(metodo_id, utente_id)
        except MetodoNonTrovatoException as exc:
            raise MetodoNonTrovato(str(exc)) from exc
        self._repo.imposta_predefinito(metodo_id, utente_id)

    def rimuovi_metodo(self, metodo_id: uuid.UUID, utente_id: uuid.UUID) -> None:
        try:
            self._repo.trova_metodo(metodo_id, utente_id)
        except MetodoNonTrovatoException as exc:
            raise MetodoNonTrovato(str(exc)) from exc
        self._repo.rimuovi_metodo(metodo_id, utente_id)

    # [CS-07] Effettua Pagamento — metodo generico usato da corsa e abbonamento
    def paga_importo(
        self,
        utente_id: uuid.UUID,
        importo: Decimal,
        corsa_id: uuid.UUID | None = None,
        abbonamento_id: uuid.UUID | None = None,
        importo_pieno: Decimal | None = None,
        offerta_applicata_id: uuid.UUID | None = None,
    ) -> dict:
        """Addebita importo sul metodo predefinito. Registra il pagamento in DB."""
        metodi = self._repo.lista_metodi(utente_id)
        if not metodi:
            raise NessunMetodoPredefinito("Nessun metodo di pagamento salvato")
        metodo = self._repo.trova_predefinito(utente_id) if len(metodi) > 1 else self._repo.trova_metodo(metodi[0].id, utente_id)
        if not metodo:
            raise NessunMetodoPredefinito("Imposta un metodo di pagamento predefinito")

        risposta = self._provider.autorizza(metodo.token_esterno, importo)
        stato = StatoPagamento.completato if risposta.autorizzato else StatoPagamento.rifiutato

        pagamento = self._repo.crea_pagamento(
            utente_id=utente_id,
            metodo_id=metodo.id,
            importo=importo,
            stato=stato,
            corsa_id=corsa_id,
            abbonamento_id=abbonamento_id,
            importo_pieno=importo_pieno,
            offerta_applicata_id=offerta_applicata_id,
        )

        if not risposta.autorizzato:
            raise PagamentoRifiutato("Il provider ha rifiutato il pagamento")

        return {
            "id": str(pagamento.id),
            "importo": float(pagamento.importo),
            "stato": pagamento.stato.value if hasattr(pagamento.stato, "value") else str(pagamento.stato),
            "transazione_id": risposta.transazione_id,
        }

    # [IF-UT.20] Effettua Pagamento a fine corsa
    def effettua_pagamento(
        self,
        corsa_id: uuid.UUID,
        utente_id: uuid.UUID,
        tipo_mezzo: str,
        durata_min: float,
        distanza_km: float,
        offerta_id: uuid.UUID | None = None,
        penale_fuori_zona: bool = False,
    ) -> dict:
        # [CS-15 / IF-OP.09/14] Calcola addebito pausa e sottrai tempo di pausa dalla tariffa base
        pausa_accumulata_sec: int = 0
        addebito_pausa_extra = Decimal("0.00")
        with Session(engine) as s:
            corsa_repo = CorsaRepository(s)
            pausa_accumulata_sec = corsa_repo.get_pausa_accumulata_sec(corsa_id)
            parametri = ParametriSistemaRepository().get(s)
            grazia_sec = int(parametri.durata_periodo_grazia_min) * 60
            addebito_per_min = Decimal(str(parametri.addebito_pausa_min))

        # Tempo pausa oltre il periodo di grazia → addebito_pausa_min al minuto
        pausa_oltre_grazia_sec = max(0, pausa_accumulata_sec - grazia_sec)
        if pausa_oltre_grazia_sec > 0 and addebito_per_min > 0:
            pausa_oltre_grazia_min = Decimal(str(pausa_oltre_grazia_sec)) / Decimal("60")
            addebito_pausa_extra = (pausa_oltre_grazia_min * addebito_per_min).quantize(Decimal("0.01"))

        # Sottrai il tempo di pausa dalla durata addebitata a tariffa normale
        pausa_accumulata_min = Decimal(str(pausa_accumulata_sec)) / Decimal("60")
        effective_durata_min = max(Decimal("0"), Decimal(str(durata_min)) - pausa_accumulata_min)

        importo = self.calcola_importo(tipo_mezzo, float(effective_durata_min), distanza_km)
        importo += addebito_pausa_extra

        importo_pieno: Decimal | None = None
        offerta_applicata_id: uuid.UUID | None = None

        # Verifica se la corsa è di gruppo (gruppo_corsa_id presente)
        with Session(engine) as s:
            row = s.execute(
                text("SELECT gruppo_corsa_id FROM corse WHERE id = :id"),
                {"id": str(corsa_id)},
            ).fetchone()
            is_gruppo = row is not None and row.gruppo_corsa_id is not None

        # [IF-UT.16] Abbonamento attivo → corsa gratuita solo se compatibile con tipo_mezzo
        if not is_gruppo:
            with Session(engine) as s:
                abbonamento = AbbonamentoRepository().get_attivo(utente_id, s)
                if abbonamento and abbonamento.data_fine > datetime.now(timezone.utc):
                    offerta_abb = s.get(Offerta, abbonamento.offerta_id)
                    mezzo_compatibile = (
                        offerta_abb is None
                        or offerta_abb.tipo_mezzo is None
                        or offerta_abb.tipo_mezzo == tipo_mezzo
                    )
                    if mezzo_compatibile:
                        importo_pieno = importo
                        importo = Decimal("0.00")

        if importo > 0 and offerta_id is not None:
            with Session(engine) as s:
                offerta = s.get(Offerta, offerta_id)
            if offerta and offerta.tipo == "promozione" and offerta.stato == "attiva":
                importo_pieno = importo
                importo = importo * (1 - offerta.sconto_percentuale / 100)
                offerta_applicata_id = offerta.id

        # [IF-OP.06 / UT-04] Penale obbligatoria se la corsa è transitata in zona vietata /
        # fuori dalla zona operativa. Si applica sopra l'importo (anche con abbonamento/promo).
        if penale_fuori_zona:
            with Session(engine) as s:
                row = s.execute(
                    text(
                        "SELECT penale_fuori_zona FROM regole_fine_corsa "
                        "WHERE tipo_vincolo = 'penale' ORDER BY created_at DESC LIMIT 1"
                    )
                ).fetchone()
            penale = Decimal(str(row.penale_fuori_zona)) if row and row.penale_fuori_zona else Decimal("0.00")
            if penale > 0:
                if importo_pieno is None:
                    importo_pieno = importo
                importo += penale
                importo_pieno += penale

        return self.paga_importo(
            utente_id=utente_id,
            importo=importo,
            corsa_id=corsa_id,
            importo_pieno=importo_pieno,
            offerta_applicata_id=offerta_applicata_id,
        )
