from uuid import UUID
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from dal.suggerimento_repository import SuggerimentoRepository
from dal.corsa_repository import CorsaRepository
from dal.abbonamento_repository import AbbonamentoRepository
from dal.pagamento_repository import PagamentoRepository
from bll.servizio_ai_adapter import ServizioAIAdapter
from model.suggerimento import Suggerimento, StatoSuggerimento, TipoSuggerimento
from config import engine


TIPI_VALIDI = {t.value for t in TipoSuggerimento}


class ServizioSuggerimenti:
    """[IF-UT.14] BLL per i suggerimenti intelligenti."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._suggerimento_repo = SuggerimentoRepository()
        self._corsa_repo = CorsaRepository(engine)
        self._abbonamento_repo = AbbonamentoRepository()
        self._pagamento_repo = PagamentoRepository()
        self._servizio_ai = ServizioAIAdapter()

    def get_suggerimenti(self, utente_id: UUID) -> list[dict]:
        suggerimenti = self._suggerimento_repo.find_by_utente(utente_id)
        return [self._to_dict(s) for s in suggerimenti]

    def genera_suggerimenti(self, utente_id: UUID) -> list[dict]:
        dati = self._raccogli_dati(utente_id)

        raw = self._servizio_ai.genera_suggerimenti(dati)
        if not raw:
            return self.get_suggerimenti(utente_id)

        self._suggerimento_repo.elimina_per_utente(utente_id)

        entita = [
            Suggerimento(
                utente_id=utente_id,
                tipo=s.get("tipo", "generale") if s.get("tipo") in TIPI_VALIDI else "generale",
                testo=s["testo"],
                dati_contesto=s.get("dati_contesto", {}),
            )
            for s in raw
        ]
        salvati = self._suggerimento_repo.save_batch(entita)
        return [self._to_dict(s) for s in salvati]

    def segna_visto(self, suggerimento_id: UUID, utente_id: UUID) -> None:
        self._suggerimento_repo.aggiorna_stato(suggerimento_id, StatoSuggerimento.visto)

    def _raccogli_dati(self, utente_id: UUID) -> dict:
        corse = self._corsa_repo.find_by_utente_order_by_data(utente_id)

        abbonamento = self._abbonamento_repo.get_attivo(utente_id, self._db)
        abb_dict = None
        if abbonamento:
            abb_dict = {
                "data_inizio": str(abbonamento.data_inizio),
                "data_fine": str(abbonamento.data_fine),
                "stato": abbonamento.stato,
            }

        pagamenti_raw = self._pagamento_repo.trova_per_utente(utente_id)
        pagamenti = [
            {
                "importo": float(p.importo) if p.importo else 0,
                "stato": p.stato.value if hasattr(p.stato, "value") else str(p.stato),
                "created_at": str(p.created_at),
            }
            for p in pagamenti_raw[:20]
        ]

        return {
            "corse": corse[:20],
            "abbonamento_attivo": abb_dict,
            "pagamenti_recenti": pagamenti,
            "n_corse_totali": len(corse),
        }

    @staticmethod
    def _to_dict(s: Suggerimento) -> dict:
        return {
            "id": str(s.id),
            "tipo": s.tipo.value if hasattr(s.tipo, "value") else str(s.tipo),
            "testo": s.testo,
            "dati_contesto": s.dati_contesto or {},
            "stato": s.stato.value if hasattr(s.stato, "value") else str(s.stato),
            "creato_at": s.creato_at.isoformat() if s.creato_at else None,
        }
