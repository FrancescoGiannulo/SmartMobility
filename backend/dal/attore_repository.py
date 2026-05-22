from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.utente import Utente
from model.operatore import Operatore
from model.amministrazione_pubblica import AmministrazionePubblica


class AttoreNonTrovatoException(Exception):
    pass


class AttoreRepository:

    def trova_per_id(self, id: UUID) -> tuple:
        """Cerca in utenti → operatori → amministratori. Restituisce (profilo, ruolo)."""
        with Session(engine) as session:
            row = session.execute(
                text("SELECT nome, cognome, sospeso FROM utenti WHERE id = :id"),
                {"id": str(id)},
            ).fetchone()
            if row:
                return (
                    Utente(id=id, nome=row.nome, cognome=row.cognome, sospeso=row.sospeso),
                    "UT",
                )

            row = session.execute(
                text(
                    "SELECT nome, durata_max_prenotazione_min, "
                    "durata_periodo_grazia_min, max_mezzi_per_utente "
                    "FROM operatori WHERE id = :id"
                ),
                {"id": str(id)},
            ).fetchone()
            if row:
                return (
                    Operatore(
                        id=id,
                        nome=row.nome,
                        durata_max_prenotazione_min=row.durata_max_prenotazione_min,
                        durata_periodo_grazia_min=row.durata_periodo_grazia_min,
                        max_mezzi_per_utente=row.max_mezzi_per_utente,
                    ),
                    "OP",
                )

            row = session.execute(
                text("SELECT nome FROM amministratori WHERE id = :id"),
                {"id": str(id)},
            ).fetchone()
            if row:
                return (AmministrazionePubblica(id=id, nome=row.nome), "AP")

        raise AttoreNonTrovatoException(f"Attore {id} non trovato")

    def trova_per_email(self, email: str) -> tuple:
        """Risolve email → UUID via auth.users (richiede service_role), poi trova_per_id."""
        with Session(engine) as session:
            row = session.execute(
                text("SELECT id FROM auth.users WHERE email = :email"),
                {"email": email},
            ).fetchone()
            if not row:
                raise AttoreNonTrovatoException(f"Nessun attore con email {email}")
        return self.trova_per_id(UUID(str(row.id)))

    def crea_utente(self, id: UUID, nome: str, cognome: str) -> None:
        with Session(engine) as session:
            session.execute(
                text("INSERT INTO utenti (id, nome, cognome) VALUES (:id, :nome, :cognome)"),
                {"id": str(id), "nome": nome, "cognome": cognome},
            )
            session.commit()

    def conta_tentativi_falliti(self, email: str) -> int:
        with Session(engine) as session:
            result = session.execute(
                text(
                    "SELECT COUNT(*) FROM tentativi_login "
                    "WHERE email = :email AND riuscito = false "
                    "AND tentativo_at > NOW() - INTERVAL '15 minutes'"
                ),
                {"email": email},
            ).scalar()
            return int(result or 0)

    def registra_tentativo(self, email: str, riuscito: bool) -> None:
        with Session(engine) as session:
            session.execute(
                text(
                    "INSERT INTO tentativi_login (email, riuscito) VALUES (:email, :riuscito)"
                ),
                {"email": email, "riuscito": riuscito},
            )
            session.commit()
