from uuid import UUID
from dal.notifica_repository import NotificaRepository


class NotificaService:
    """[IF-OP.09 / IF-OP.08] Logica di invio (persistenza) notifiche all'Utente."""

    def __init__(self) -> None:
        self._repo = NotificaRepository()

    def notifica(self, id_utente: UUID, messaggio: str) -> None:
        self._repo.crea(id_utente, messaggio)
