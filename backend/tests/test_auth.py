# backend/tests/test_auth.py
from uuid import UUID, uuid4
from model.persona import Persona
from model.utente import Utente
from model.operatore import Operatore
from model.amministrazione_pubblica import AmministrazionePubblica


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
