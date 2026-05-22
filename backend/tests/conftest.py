import os
import pytest
from uuid import UUID
from supabase import create_client
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def supa():
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


@pytest.fixture(scope="session")
def db():
    return create_engine(os.environ["DATABASE_URL"])


def _crea_auth_user(supa, email: str, password: str) -> UUID:
    resp = supa.auth.admin.create_user({
        "email": email,
        "password": password,
        "email_confirm": True,
    })
    return UUID(resp.user.id)


def _elimina_auth_user(supa, user_id: UUID) -> None:
    try:
        supa.auth.admin.delete_user(str(user_id))
    except Exception:
        pass


def _pulisci_tentativi(db, email: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM tentativi_login WHERE email = :e"), {"e": email})
        s.commit()


@pytest.fixture
def utente_test(supa, db):
    email, password = "ut_test@smartmobility.test", "TestPass123!"
    uid = _crea_auth_user(supa, email, password)
    with Session(db) as s:
        s.execute(
            text("INSERT INTO utenti (id, nome, cognome) VALUES (:id, 'Test', 'Utente')"),
            {"id": str(uid)},
        )
        s.commit()
    yield {"id": uid, "email": email, "password": password}
    _pulisci_tentativi(db, email)
    with Session(db) as s:
        s.execute(text("DELETE FROM utenti WHERE id = :id"), {"id": str(uid)})
        s.commit()
    _elimina_auth_user(supa, uid)


@pytest.fixture
def utente_sospeso(supa, db):
    email, password = "ut_sospeso@smartmobility.test", "TestPass123!"
    uid = _crea_auth_user(supa, email, password)
    with Session(db) as s:
        s.execute(
            text("INSERT INTO utenti (id, nome, cognome, sospeso) VALUES (:id, 'Sospeso', 'Test', true)"),
            {"id": str(uid)},
        )
        s.commit()
    yield {"id": uid, "email": email, "password": password}
    _pulisci_tentativi(db, email)
    with Session(db) as s:
        s.execute(text("DELETE FROM utenti WHERE id = :id"), {"id": str(uid)})
        s.commit()
    _elimina_auth_user(supa, uid)


@pytest.fixture
def operatore_test(supa, db):
    email, password = "op_test@smartmobility.test", "TestPass123!"
    uid = _crea_auth_user(supa, email, password)
    with Session(db) as s:
        s.execute(
            text("INSERT INTO operatori (id, nome) VALUES (:id, 'OperatoreTest')"),
            {"id": str(uid)},
        )
        s.commit()
    yield {"id": uid, "email": email, "password": password}
    _pulisci_tentativi(db, email)
    with Session(db) as s:
        s.execute(text("DELETE FROM operatori WHERE id = :id"), {"id": str(uid)})
        s.commit()
    _elimina_auth_user(supa, uid)


@pytest.fixture
def ap_test(supa, db):
    email, password = "ap_test@smartmobility.test", "TestPass123!"
    uid = _crea_auth_user(supa, email, password)
    with Session(db) as s:
        s.execute(
            text("INSERT INTO amministratori (id, nome) VALUES (:id, 'APTest')"),
            {"id": str(uid)},
        )
        s.commit()
    yield {"id": uid, "email": email, "password": password}
    _pulisci_tentativi(db, email)
    with Session(db) as s:
        s.execute(text("DELETE FROM amministratori WHERE id = :id"), {"id": str(uid)})
        s.commit()
    _elimina_auth_user(supa, uid)
