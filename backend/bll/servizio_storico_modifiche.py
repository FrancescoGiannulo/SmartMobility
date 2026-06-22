from uuid import UUID
from dal.storico_modifiche_repository import StoricoModificheRepository


class ServizioStoricoModifiche:
    """[IF-OP.13] Mostra Storico Modifiche — consultazione e registrazione delle modifiche
    apportate alle configurazioni del servizio (parametri di sistema, regole di fine corsa,
    zone operative)."""

    def __init__(self) -> None:
        self._repo = StoricoModificheRepository()

    def registra_modifica(
        self,
        tipo_configurazione: str,
        descrizione: str,
        valore_precedente: str | None,
        valore_nuovo: str | None,
        operatore_id: UUID,
    ) -> None:
        self._repo.crea(
            tipo_configurazione=tipo_configurazione,
            descrizione=descrizione,
            valore_precedente=valore_precedente,
            valore_nuovo=valore_nuovo,
            operatore_id=operatore_id,
        )

    def get_storico(self) -> list[dict]:
        return [
            {
                "id": str(v.id),
                "tipo_configurazione": v.tipo_configurazione,
                "descrizione": v.descrizione,
                "valore_precedente": v.valore_precedente,
                "valore_nuovo": v.valore_nuovo,
                "operatore_id": str(v.operatore_id),
                "created_at": v.created_at.isoformat() if v.created_at else None,
            }
            for v in self._repo.find_all()
        ]
