import uuid
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from dal.pagamento_repository import PagamentoRepository, MetodoNonTrovatoException
from dal.tariffa_repository import TariffaRepository
from dal.promozione_repository import PromozioneRepository
from model.pagamento import StatoPagamento
from providers.provider_pagamenti import ProviderPagamentiStub, DatiNonValidiException


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


class TariffaNonTrovata(Exception):
    pass


class TariffaGiaEsistente(Exception):
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

    # [IF-OP.07] — engine pattern
    def get_tariffe(self) -> list[dict]:
        tariffe = self._tariffa_repo.find_all()
        return [
            {
                "id": str(t.id),
                "tipo_mezzo": t.tipo_mezzo,
                "costo_al_minuto": float(t.costo_al_minuto),
                "costo_al_km": float(t.costo_al_km),
            }
            for t in tariffe
        ]

    def aggiorna_tariffa(self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float) -> dict:
        tariffa = self._tariffa_repo.aggiorna(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        if not tariffa:
            raise TariffaNonTrovata(f"Nessuna tariffa per '{tipo_mezzo}'")
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }

    def crea_tariffa(self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float) -> dict:
        if self._tariffa_repo.exists_by_tipologia(tipo_mezzo):
            raise TariffaGiaEsistente(f"Tariffa per '{tipo_mezzo}' già esistente")
        tariffa = self._tariffa_repo.crea(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }

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

    # [IF-UT.12] Salva Metodi di Pagamento
    def aggiungi_metodo(self, utente_id: uuid.UUID, tipo: str, dati: dict) -> dict:
        try:
            token = self._provider.valida_dati_pagamento(tipo, dati)
        except DatiNonValidiException as exc:
            raise DatiNonValidi(str(exc)) from exc

        if self._repo.exists_by_token(token):
            raise MetodoDuplicato("Metodo di pagamento già presente")

        last_four = dati.get("last_four")
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

    # [IF-UT.20] Effettua Pagamento
    def effettua_pagamento(
        self,
        corsa_id: uuid.UUID,
        utente_id: uuid.UUID,
        tipo_mezzo: str,
        durata_min: float,
        distanza_km: float,
    ) -> dict:
        metodi = self._repo.lista_metodi(utente_id)
        if not metodi:
            raise NessunMetodoPredefinito("Nessun metodo di pagamento salvato")
        if len(metodi) == 1:
            metodo = self._repo.trova_metodo(metodi[0].id, utente_id)
        else:
            metodo = self._repo.trova_predefinito(utente_id)
            if not metodo:
                raise NessunMetodoPredefinito("Imposta un metodo di pagamento predefinito")

        importo = self.calcola_importo(tipo_mezzo, durata_min, distanza_km)
        risposta = self._provider.autorizza(metodo.token_esterno, importo)

        stato = StatoPagamento.completato if risposta.autorizzato else StatoPagamento.rifiutato
        pagamento = self._repo.crea_pagamento(corsa_id, utente_id, metodo.id, importo, stato)

        if not risposta.autorizzato:
            raise PagamentoRifiutato("Il provider ha rifiutato il pagamento")

        return {
            "id": str(pagamento.id),
            "importo": float(pagamento.importo),
            "stato": pagamento.stato.value if hasattr(pagamento.stato, "value") else str(pagamento.stato),
            "transazione_id": risposta.transazione_id,
        }
