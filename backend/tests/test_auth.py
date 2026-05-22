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
from sqlalchemy.orm import Session as DbSession
from bll.servizio_utenti import (
    ServizioUtenti,
    CredenzialNonValideException,
    AccountBloccatoException,
    AccountSospesoException,
    EmailGiaRegistrataException,
)
import jwt as pyjwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from middleware.auth_middleware import verify_token
from config import SUPABASE_JWT_SECRET


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


class TestServizioUtenti:

    def test_registra_successo(self, supa, db):
        email = "reg_nuovo@smartmobility.test"
        result = ServizioUtenti().registra_account(email, "TestPass123!", "Nuovo", "Utente")
        assert result["ruolo"] == "UT"
        assert result["profilo"]["email"] == email
        assert "access_token" in result
        # cleanup
        profilo, _ = AttoreRepository().trova_per_email(email)
        with DbSession(db) as s:
            s.execute(text("DELETE FROM utenti WHERE id = :id"), {"id": str(profilo.id)})
            s.commit()
        supa.auth.admin.delete_user(str(profilo.id))

    def test_registra_email_duplicata(self, utente_test):
        with pytest.raises(EmailGiaRegistrataException):
            ServizioUtenti().registra_account(
                utente_test["email"], "TestPass123!", "Dup", "Utente"
            )

    def test_login_successo_ut(self, utente_test):
        result = ServizioUtenti().autentica_account(utente_test["email"], utente_test["password"])
        assert result["ruolo"] == "UT"
        assert "access_token" in result

    def test_login_successo_op(self, operatore_test):
        result = ServizioUtenti().autentica_account(
            operatore_test["email"], operatore_test["password"]
        )
        assert result["ruolo"] == "OP"

    def test_login_successo_ap(self, ap_test):
        result = ServizioUtenti().autentica_account(ap_test["email"], ap_test["password"])
        assert result["ruolo"] == "AP"

    def test_login_credenziali_errate(self, utente_test, db):
        with pytest.raises(CredenzialNonValideException):
            ServizioUtenti().autentica_account(utente_test["email"], "WrongPass!")
        with DbSession(db) as s:
            s.execute(
                text("DELETE FROM tentativi_login WHERE email = :e"),
                {"e": utente_test["email"]},
            )
            s.commit()

    def test_login_lockout(self, utente_test, db):
        repo = AttoreRepository()
        for _ in range(5):
            repo.registra_tentativo(utente_test["email"], riuscito=False)
        with pytest.raises(AccountBloccatoException):
            ServizioUtenti().autentica_account(utente_test["email"], utente_test["password"])
        with DbSession(db) as s:
            s.execute(
                text("DELETE FROM tentativi_login WHERE email = :e"),
                {"e": utente_test["email"]},
            )
            s.commit()

    def test_login_account_sospeso(self, utente_sospeso):
        with pytest.raises(AccountSospesoException):
            ServizioUtenti().autentica_account(
                utente_sospeso["email"], utente_sospeso["password"]
            )

    def test_login_op_non_bloccato_da_sospeso(self, operatore_test):
        # [IIN-2] Operatori non hanno campo sospeso — non devono essere bloccati
        result = ServizioUtenti().autentica_account(
            operatore_test["email"], operatore_test["password"]
        )
        assert result["ruolo"] == "OP"


def _crea_token(sub: str, email: str, exp_delta_s: int = 3600) -> str:
    payload = {
        "sub": sub,
        "email": email,
        "aud": "authenticated",
        "exp": datetime.now(timezone.utc) + timedelta(seconds=exp_delta_s),
    }
    return pyjwt.encode(payload, SUPABASE_JWT_SECRET, algorithm="HS256")


class TestMiddleware:

    def _app_protetta(self):
        app = FastAPI()

        @app.get("/protetta")
        def protetta(u=Depends(verify_token())):
            return {"ruolo": u["ruolo"]}

        @app.get("/solo-ut")
        def solo_ut(u=Depends(verify_token(["UT"]))):
            return {"ok": True}

        return TestClient(app)

    def test_token_valido_restituisce_ruolo(self, utente_test):
        token = _crea_token(str(utente_test["id"]), utente_test["email"])
        resp = self._app_protetta().get("/protetta", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["ruolo"] == "UT"

    def test_token_mancante_restituisce_401(self):
        resp = self._app_protetta().get("/protetta")
        assert resp.status_code == 401

    def test_token_scaduto_restituisce_401(self, utente_test):
        token = _crea_token(str(utente_test["id"]), utente_test["email"], exp_delta_s=-1)
        resp = self._app_protetta().get("/protetta", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 401

    def test_ruolo_errato_restituisce_403(self, operatore_test):
        token = _crea_token(str(operatore_test["id"]), operatore_test["email"])
        resp = self._app_protetta().get("/solo-ut", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 403
