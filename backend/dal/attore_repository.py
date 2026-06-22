from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.utente import Utente
from model.operatore import Operatore
from model.amministrazione_pubblica import AmministrazionePubblica


class AttoreNonTrovatoException(Exception):
    pass


class AccountGiaSospesoException(Exception):
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

    def crea_utente(self, id: UUID, nome: str, cognome: str, consenso_privacy: bool = False) -> None:
        consenso_at = datetime.now(timezone.utc).isoformat() if consenso_privacy else None
        with Session(engine) as session:
            session.execute(
                text(
                    "INSERT INTO utenti (id, nome, cognome, consenso_privacy_at) "
                    "VALUES (:id, :nome, :cognome, :consenso_at)"
                ),
                {"id": str(id), "nome": nome, "cognome": cognome, "consenso_at": consenso_at},
            )
            session.commit()

    # [IF-OP.09] ──────────────────────────────────────────────────────────────

    def lista_utenti(self) -> list[dict]:
        """Elenco di tutti gli Utenti registrati, con email da auth.users."""
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT u.id, u.nome, u.cognome, u.sospeso, a.email "
                    "FROM utenti u JOIN auth.users a ON a.id = u.id "
                    "ORDER BY u.cognome, u.nome"
                )
            ).fetchall()
            return [
                {
                    "id": str(row.id),
                    "nome": row.nome,
                    "cognome": row.cognome,
                    "email": row.email,
                    "sospeso": row.sospeso,
                }
                for row in rows
            ]

    def trova_utente_per_id(self, id: UUID) -> dict:
        """Dettaglio di un singolo Utente, con email da auth.users."""
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT u.id, u.nome, u.cognome, u.sospeso, a.email "
                    "FROM utenti u JOIN auth.users a ON a.id = u.id "
                    "WHERE u.id = :id"
                ),
                {"id": str(id)},
            ).fetchone()
            if not row:
                raise AttoreNonTrovatoException(f"Utente {id} non trovato")
            return {
                "id": str(row.id),
                "nome": row.nome,
                "cognome": row.cognome,
                "email": row.email,
                "sospeso": row.sospeso,
            }

    def sospendi(self, id: UUID, motivazione: str) -> None:
        """[IF-OP.09] Sospende l'account di un Utente attivo."""
        with Session(engine) as session:
            row = session.execute(
                text("SELECT sospeso FROM utenti WHERE id = :id"),
                {"id": str(id)},
            ).fetchone()
            if not row:
                raise AttoreNonTrovatoException(f"Utente {id} non trovato")
            if row.sospeso:
                raise AccountGiaSospesoException(f"Utente {id} è già sospeso")

            session.execute(
                text(
                    "UPDATE utenti SET sospeso = true, "
                    "motivazione_sospensione = :motivazione, sospeso_at = NOW() "
                    "WHERE id = :id"
                ),
                {"id": str(id), "motivazione": motivazione},
            )
            session.commit()

    def leggi_config_sicurezza(self) -> dict:
        """Legge la configurazione di sicurezza globale (riga singleton)."""
        try:
            with Session(engine) as session:
                row = session.execute(
                    text("SELECT lockout_window_min, max_tentativi FROM configurazione_sicurezza LIMIT 1")
                ).fetchone()
                if row:
                    return {"lockout_window_min": row.lockout_window_min, "max_tentativi": row.max_tentativi}
        except Exception:
            pass
        return {"lockout_window_min": 15, "max_tentativi": 5}

    def aggiorna_config_sicurezza(self, lockout_window_min: int | None, max_tentativi: int | None) -> dict:
        """Aggiorna la configurazione di sicurezza globale."""
        with Session(engine) as session:
            if lockout_window_min is not None:
                session.execute(
                    text(
                        "UPDATE configurazione_sicurezza "
                        "SET lockout_window_min = :val, updated_at = NOW()"
                    ),
                    {"val": lockout_window_min},
                )
            if max_tentativi is not None:
                session.execute(
                    text(
                        "UPDATE configurazione_sicurezza "
                        "SET max_tentativi = :val, updated_at = NOW()"
                    ),
                    {"val": max_tentativi},
                )
            session.commit()
        return self.leggi_config_sicurezza()

    def conta_tentativi_falliti(self, email: str) -> int:
        config = self.leggi_config_sicurezza()
        window = config["lockout_window_min"]
        with Session(engine) as session:
            # [IIN-2] Conta solo i fallimenti consecutivi: esclude quelli precedenti
            # all'ultimo login riuscito nella stessa finestra temporale.
            result = session.execute(
                text(
                    "SELECT COUNT(*) FROM tentativi_login "
                    "WHERE email = :email AND riuscito = false "
                    "AND tentativo_at > NOW() - INTERVAL '1 minute' * :window "
                    "AND tentativo_at > COALESCE("
                    "  (SELECT MAX(tentativo_at) FROM tentativi_login "
                    "   WHERE email = :email AND riuscito = true "
                    "   AND tentativo_at > NOW() - INTERVAL '1 minute' * :window), "
                    "  'epoch'::timestamptz"
                    ")"
                ),
                {"email": email, "window": window},
            ).scalar()
            return int(result or 0)

    def max_tentativi(self) -> int:
        return self.leggi_config_sicurezza()["max_tentativi"]

    def registra_tentativo(self, email: str, riuscito: bool) -> None:
        with Session(engine) as session:
            session.execute(
                text(
                    "INSERT INTO tentativi_login (email, riuscito) VALUES (:email, :riuscito)"
                ),
                {"email": email, "riuscito": riuscito},
            )
            session.commit()

    # ── GDPR ──────────────────────────────────────────────────────────────────

    def esporta_dati_utente(self, utente_id: UUID) -> dict:
        """Raccoglie i dati personali dell'utente per il diritto di portabilità (art. 20 GDPR)."""
        with Session(engine) as session:
            profilo = session.execute(
                text("SELECT nome, cognome, consenso_privacy_at FROM utenti WHERE id = :id"),
                {"id": str(utente_id)},
            ).fetchone()
            if not profilo:
                raise AttoreNonTrovatoException(f"Utente {utente_id} non trovato")

            corse = session.execute(
                text(
                    "SELECT id, mezzo_id, inizio_corsa, fine_corsa, "
                    "distanza_km, costo_totale "
                    "FROM corse WHERE utente_id = :id ORDER BY inizio_corsa DESC"
                ),
                {"id": str(utente_id)},
            ).fetchall()

        return {
            "profilo": {
                "id": str(utente_id),
                "nome": profilo.nome,
                "cognome": profilo.cognome,
                "consenso_privacy_at": str(profilo.consenso_privacy_at) if profilo.consenso_privacy_at else None,
            },
            "corse": [
                {
                    "id": str(c.id),
                    "mezzo_id": str(c.mezzo_id),
                    "inizio_corsa": str(c.inizio_corsa),
                    "fine_corsa": str(c.fine_corsa) if c.fine_corsa else None,
                    "distanza_km": float(c.distanza_km) if c.distanza_km else None,
                    "costo_totale": float(c.costo_totale) if c.costo_totale else None,
                }
                for c in corse
            ],
        }

    def elimina_utente(self, utente_id: UUID) -> None:
        """Elimina i dati dell'utente dalla tabella utenti (diritto all'oblio, art. 17 GDPR)."""
        with Session(engine) as session:
            session.execute(
                text("DELETE FROM utenti WHERE id = :id"),
                {"id": str(utente_id)},
            )
            session.commit()
