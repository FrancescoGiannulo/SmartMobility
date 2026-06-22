import pytest
from uuid import uuid4
from dal.attore_repository import (
    AttoreRepository,
    AttoreNonTrovatoException,
    AccountGiaSospesoException,
)


@pytest.mark.integration
class TestListaUtenti:

    def test_lista_utenti_contiene_utente_test(self, utente_test):
        utenti = AttoreRepository().lista_utenti()
        ids = {u["id"] for u in utenti}
        assert str(utente_test["id"]) in ids

    def test_lista_utenti_include_email(self, utente_test):
        utenti = AttoreRepository().lista_utenti()
        trovato = next(u for u in utenti if u["id"] == str(utente_test["id"]))
        assert trovato["email"] == utente_test["email"]
        assert trovato["sospeso"] is False


@pytest.mark.integration
class TestTrovaUtentePerId:

    def test_trova_utente_per_id_ok(self, utente_test):
        u = AttoreRepository().trova_utente_per_id(utente_test["id"])
        assert u["nome"] == "Test"
        assert u["email"] == utente_test["email"]

    def test_trova_utente_per_id_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            AttoreRepository().trova_utente_per_id(uuid4())


@pytest.mark.integration
class TestSospendi:

    def test_sospendi_account_attivo(self, utente_test):
        AttoreRepository().sospendi(utente_test["id"], "Comportamento scorretto")
        u = AttoreRepository().trova_utente_per_id(utente_test["id"])
        assert u["sospeso"] is True

    def test_sospendi_account_gia_sospeso(self, utente_sospeso):
        with pytest.raises(AccountGiaSospesoException):
            AttoreRepository().sospendi(utente_sospeso["id"], "Motivo")

    def test_sospendi_utente_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            AttoreRepository().sospendi(uuid4(), "Motivo")
