import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.segnalazione import Segnalazione, StatoSegnalazione


class SegnalazioneNonTrovataException(Exception):
    pass


class SegnalazioneRepository:

    # [IF-UT.15] Invia Segnalazione
    def crea(self, utente_id: uuid.UUID, tipologia: str, descrizione: str) -> Segnalazione:
        with Session(engine) as session:
            segnalazione = Segnalazione(
                utente_id=utente_id,
                tipologia=tipologia,
                descrizione=descrizione,
            )
            session.add(segnalazione)
            session.commit()
            session.refresh(segnalazione)
            return segnalazione

    def find_by_utente(self, utente_id: uuid.UUID) -> list[Segnalazione]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, utente_id, tipologia, descrizione, stato, created_at "
                    "FROM segnalazioni WHERE utente_id = :uid ORDER BY created_at DESC"
                ),
                {"uid": str(utente_id)},
            ).fetchall()
        return [
            Segnalazione(
                id=r.id, utente_id=r.utente_id, tipologia=r.tipologia,
                descrizione=r.descrizione, stato=r.stato, created_at=r.created_at,
            )
            for r in rows
        ]

    # [IF-OP.08] Gestisce Segnalazione
    def find_all(self) -> list[dict]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT s.id, s.utente_id, s.tipologia, s.descrizione, s.stato, s.created_at, "
                    "       u.nome || ' ' || u.cognome AS nome_utente "
                    "FROM segnalazioni s "
                    "LEFT JOIN utenti u ON u.id = s.utente_id "
                    "ORDER BY s.created_at DESC"
                )
            ).fetchall()
        return [
            {
                "id": r.id,
                "utente_id": r.utente_id,
                "tipologia": r.tipologia,
                "descrizione": r.descrizione,
                "stato": r.stato,
                "created_at": r.created_at,
                "nome_utente": r.nome_utente,
            }
            for r in rows
        ]

    def find_by_id(self, segnalazione_id: uuid.UUID) -> dict | None:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT s.id, s.utente_id, s.tipologia, s.descrizione, s.stato, s.created_at, "
                    "       u.nome || ' ' || u.cognome AS nome_utente "
                    "FROM segnalazioni s "
                    "LEFT JOIN utenti u ON u.id = s.utente_id "
                    "WHERE s.id = :sid"
                ),
                {"sid": str(segnalazione_id)},
            ).fetchone()
        if not row:
            return None
        return {
            "id": row.id,
            "utente_id": row.utente_id,
            "tipologia": row.tipologia,
            "descrizione": row.descrizione,
            "stato": row.stato,
            "created_at": row.created_at,
            "nome_utente": row.nome_utente,
        }

    def aggiorna_stato(self, segnalazione_id: uuid.UUID, stato: StatoSegnalazione) -> bool:
        with Session(engine) as session:
            result = session.execute(
                text(
                    "UPDATE segnalazioni SET stato = :stato "
                    "WHERE id = :sid "
                    "RETURNING id"
                ),
                {"stato": stato.value, "sid": str(segnalazione_id)},
            ).fetchone()
            session.commit()
        return result is not None
