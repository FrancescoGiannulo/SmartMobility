# backend/tests/test_auth.py
import pytest
from uuid import UUID, uuid4
from model.persona import Persona
from model.utente import Utente
from model.operatore import Operatore
from model.amministrazione_pubblica import AmministrazionePubblica
from dal.attore_repository import AttoreRepository, AttoreNonTrovatoException
from sqlalchemy import text
from sqlalchemy.orm import Session


class TestModel:

    def test_utente_istanziabile(self):
        u = Utente(id=uuid4(), nome="Mario", email="mario@test.it", cognome="Rossi")
        assert u.ruolo_atteso() == "UT"
        assert u.sospeso is False

    def test_operatore_istanziabile(self):
        o = Operatore(id=uuid4(), nome="FleetOp", email="op@test.it")
        assert o.ruolo_atteso() == "OP"
        assert o.durata_max_prenotazione_min == 15

    def test_ap_istanziabile(self):
        a = AmministrazionePubblica(id=uuid4(), nome="Comune", email="ap@test.it")
        assert a.ruolo_atteso() == "AP"


class TestAttoreRepository:

    def test_trova_per_id_utente(self, utente_test):
        profilo, ruolo = AttoreRepository().trova_per_id(utente_test["id"])
        assert ruolo == "UT"
        assert profilo.nome == "Test"

    def test_trova_per_id_operatore(self, operatore_test):
        _, ruolo = AttoreRepository().trova_per_id(operatore_test["id"])
        assert ruolo == "OP"

    def test_trova_per_id_ap(self, ap_test):
        _, ruolo = AttoreRepository().trova_per_id(ap_test["id"])
        assert ruolo == "AP"

    def test_trova_per_id_non_trovato(self):
        with pytest.raises(AttoreNonTrovatoException):
            AttoreRepository().trova_per_id(UUID("00000000-0000-0000-0000-000000000000"))

    def test_conta_tentativi_falliti_zero(self, utente_test):
        assert AttoreRepository().conta_tentativi_falliti(utente_test["email"]) == 0

    def test_registra_e_conta_tentativo(self, utente_test, db):
        repo = AttoreRepository()
        repo.registra_tentativo(utente_test["email"], riuscito=False)
        assert repo.conta_tentativi_falliti(utente_test["email"]) == 1
        with Session(db) as s:
            s.execute(
                text("DELETE FROM tentativi_login WHERE email = :e"),
                {"e": utente_test["email"]},
            )
            s.commit()
