from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class StoricoModifiche:
    """[IF-OP.12] Voce dello storico delle modifiche alle configurazioni del servizio."""

    id: UUID
    tipo_configurazione: str
    descrizione: str
    valore_precedente: str | None
    valore_nuovo: str | None
    operatore_id: UUID
    created_at: datetime | None = None
