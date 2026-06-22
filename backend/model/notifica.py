from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Notifica:
    """[IF-OP.09] Notifica persistita per l'Utente (es. sospensione account)."""

    id: UUID
    id_utente: UUID
    messaggio: str
    letta: bool = False
    data: datetime | None = None
