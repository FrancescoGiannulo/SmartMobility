import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from dal.notifica_repository import NotificaRepository


@pytest.mark.integration
class TestNotificaRepository:

    def test_crea_e_find_by_utente(self, db, utente_test):
        repo = NotificaRepository()
        try:
            notifica = repo.crea(utente_test["id"], "Messaggio di test")
            assert notifica.id_utente == utente_test["id"]
            assert notifica.messaggio == "Messaggio di test"
            assert notifica.letta is False

            trovate = repo.find_by_utente(utente_test["id"])
            assert any(n.id == notifica.id for n in trovate)
        finally:
            with Session(db) as s:
                s.execute(
                    text("DELETE FROM notifiche WHERE utente_id = :id"),
                    {"id": str(utente_test["id"])},
                )
                s.commit()

    def test_find_by_utente_vuoto_se_nessuna_notifica(self, db, utente_test):
        repo = NotificaRepository()
        assert repo.find_by_utente(utente_test["id"]) == []
