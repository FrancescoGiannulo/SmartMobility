import pytest
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session
from bll.servizio_utenti import ServizioUtenti
from dal.attore_repository import AttoreNonTrovatoException, AccountGiaSospesoException
from dal.notifica_repository import NotificaRepository


@pytest.mark.integration
class TestGetUtenti:

    def test_get_utenti_contiene_utente_test(self, utente_test):
        utenti = ServizioUtenti().get_utenti()
        assert any(u["id"] == str(utente_test["id"]) for u in utenti)


@pytest.mark.integration
class TestGetDettaglioUtente:

    def test_get_dettaglio_utente_ok(self, utente_test):
        u = ServizioUtenti().get_dettaglio_utente(utente_test["id"])
        assert u["email"] == utente_test["email"]

    def test_get_dettaglio_utente_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            ServizioUtenti().get_dettaglio_utente(uuid4())


@pytest.mark.integration
class TestSospendiAccount:

    def test_sospendi_account_crea_notifica(self, db, utente_test):
        try:
            ServizioUtenti().sospendi_account(utente_test["id"], "Comportamento scorretto")

            u = ServizioUtenti().get_dettaglio_utente(utente_test["id"])
            assert u["sospeso"] is True

            notifiche = NotificaRepository().find_by_utente(utente_test["id"])
            assert len(notifiche) == 1
            assert "Comportamento scorretto" in notifiche[0].messaggio
        finally:
            with Session(db) as s:
                s.execute(
                    text("DELETE FROM notifiche WHERE utente_id = :id"),
                    {"id": str(utente_test["id"])},
                )
                s.commit()

    def test_sospendi_account_motivazione_vuota(self, utente_test):
        with pytest.raises(ValueError):
            ServizioUtenti().sospendi_account(utente_test["id"], "   ")

    def test_sospendi_account_gia_sospeso(self, utente_sospeso):
        with pytest.raises(AccountGiaSospesoException):
            ServizioUtenti().sospendi_account(utente_sospeso["id"], "Motivo")

    def test_sospendi_account_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            ServizioUtenti().sospendi_account(uuid4(), "Motivo")
