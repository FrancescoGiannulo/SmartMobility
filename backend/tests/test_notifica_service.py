import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from bll.notifica_service import NotificaService
from dal.notifica_repository import NotificaRepository


@pytest.mark.integration
class TestNotificaService:

    def test_notifica_persiste_messaggio(self, db, utente_test):
        try:
            NotificaService().notifica(utente_test["id"], "Account sospeso: test")
            notifiche = NotificaRepository().find_by_utente(utente_test["id"])
            assert len(notifiche) == 1
            assert notifiche[0].messaggio == "Account sospeso: test"
        finally:
            with Session(db) as s:
                s.execute(
                    text("DELETE FROM notifiche WHERE utente_id = :id"),
                    {"id": str(utente_test["id"])},
                )
                s.commit()
