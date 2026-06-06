import uuid as _uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


class CorsaRepository:

    def __init__(self, db: Session | Engine) -> None:
        self._engine = db if isinstance(db, Engine) else None
        self._session = db if not isinstance(db, Engine) else None

    @contextmanager
    def _sessione(self):
        if self._session is not None:
            yield self._session
        else:
            with Session(self._engine) as s:
                yield s

    def trova_per_id(self, corsa_id: UUID) -> dict | None:
        sql = text("SELECT id, utente_id, mezzo_id, stato FROM corse WHERE id = :id")
        with self._sessione() as s:
            row = s.execute(sql, {"id": str(corsa_id)}).fetchone()
        if row is None:
            return None
        return {
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "stato": row.stato,
        }

    def aggiorna_stato(self, corsa_id: UUID, nuovo_stato: str) -> None:
        # [IF-UT.06] Imposta fine_at quando la corsa termina, per calcolare durata_min nello storico
        if nuovo_stato == "terminata":
            sql = text("UPDATE corse SET stato = :stato, fine_at = NOW() WHERE id = :id")
        else:
            sql = text("UPDATE corse SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {"stato": nuovo_stato, "id": str(corsa_id)})
            s.commit()

    # [IF-UT.04] CS-05 — crea corsa all'avvio del mezzo
    def crea(
        self,
        utente_id: UUID,
        mezzo_id: UUID,
        prenotazione_id: UUID | None,
        gruppo_corsa_id: _uuid.UUID | None = None,
    ) -> dict:
        sql = text("""
            INSERT INTO corse
                (id, utente_id, mezzo_id, prenotazione_id, stato,
                 inizio_at, gruppo_corsa_id)
            VALUES
                (:id, :utente_id, :mezzo_id, :prenotazione_id, 'in_uso',
                 :inizio_at, :gruppo_corsa_id)
            RETURNING id, utente_id, mezzo_id, prenotazione_id, stato,
                      inizio_at, gruppo_corsa_id
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "id": str(_uuid.uuid4()),
                "utente_id": str(utente_id),
                "mezzo_id": str(mezzo_id),
                "prenotazione_id": str(prenotazione_id) if prenotazione_id else None,
                "inizio_at": datetime.now(timezone.utc),
                "gruppo_corsa_id": str(gruppo_corsa_id) if gruppo_corsa_id else None,
            }).fetchone()
            s.commit()
        return {
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "prenotazione_id": str(row.prenotazione_id) if row.prenotazione_id else None,
            "stato": row.stato,
            "inizio_at": row.inizio_at.isoformat(),
            "gruppo_corsa_id": str(row.gruppo_corsa_id) if row.gruppo_corsa_id else None,
        }

    # [IF-UT.07] CS-06 — riepilogo corsa terminata, restituisce campi Corsa (diagramma classi)
    def trova_riepilogo(self, corsa_id: UUID, utente_id: UUID) -> dict | None:
        sql = text("""
            SELECT
                c.id, c.inizio_at, c.fine_at, c.stato,
                c.distanza_km, c.gruppo_corsa_id,
                p.importo    AS costo_totale,
                p.importo_pieno
            FROM corse c
            LEFT JOIN pagamenti p ON p.corsa_id = c.id AND p.stato = 'completato'
            WHERE c.id = :corsa_id AND c.utente_id = :utente_id
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"corsa_id": str(corsa_id), "utente_id": str(utente_id)}).fetchone()
        if row is None:
            return None
        return {
            "id": str(row.id),
            "inizio_at": row.inizio_at,
            "fine_at": row.fine_at,
            "stato": row.stato,
            "distanza_km": float(row.distanza_km) if row.distanza_km is not None else None,
            "gruppo_corsa_id": row.gruppo_corsa_id,
            "costo_totale": float(row.costo_totale) if row.costo_totale is not None else None,
            "importo_pieno": float(row.importo_pieno) if row.importo_pieno is not None else None,
        }

    # [IF-UT.14] CS-11 — storico corse per utente, ordinate per data decrescente
    def find_by_utente_order_by_data(self, utente_id: UUID) -> list[dict]:
        sql = text("""
            SELECT
                c.id,
                c.inizio_at,
                c.fine_at,
                c.distanza_km,
                c.gruppo_corsa_id,
                m.tipo   AS tipo_mezzo,
                m.codice AS codice_mezzo,
                EXTRACT(EPOCH FROM (c.fine_at - c.inizio_at)) / 60 AS durata_min,
                p.importo,
                p.importo_pieno,
                o.nome AS nome_offerta_applicata
            FROM corse c
            JOIN mezzi m ON c.mezzo_id = m.id
            LEFT JOIN pagamenti p ON p.corsa_id = c.id AND p.stato = 'completato'
            LEFT JOIN offerte o ON o.id = p.offerta_applicata_id
            WHERE c.utente_id = :utente_id
              AND c.stato = 'terminata'
            ORDER BY c.inizio_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"utente_id": str(utente_id)}).fetchall()
        return [
            {
                "id": str(r.id),
                "tipo_mezzo": r.tipo_mezzo,
                "codice_mezzo": r.codice_mezzo,
                "inizio_at": r.inizio_at.isoformat(),
                "fine_at": r.fine_at.isoformat() if r.fine_at else None,
                "durata_min": float(r.durata_min) if r.durata_min is not None else None,
                "distanza_km": float(r.distanza_km) if r.distanza_km is not None else None,
                "gruppo_corsa_id": str(r.gruppo_corsa_id) if r.gruppo_corsa_id else None,
                "costo_totale": float(r.importo) if r.importo is not None else None,
                "importo_pieno": float(r.importo_pieno) if r.importo_pieno is not None else None,
                "nome_offerta_applicata": r.nome_offerta_applicata,
            }
            for r in rows
        ]
