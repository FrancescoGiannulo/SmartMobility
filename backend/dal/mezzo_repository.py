from contextlib import contextmanager
from math import radians, cos, sin, asin, sqrt
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return R * 2 * asin(sqrt(a))


class MezzoRepository:

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

    def lista_per_mappa(self, solo_disponibili: bool) -> list[dict]:
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi
            WHERE lat IS NOT NULL AND lng IS NOT NULL
              AND (:solo_disponibili = false OR stato = 'Disponibile')
            ORDER BY created_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"solo_disponibili": solo_disponibili}).fetchall()
        return [
            {
                "id": row.id,
                "codice": row.codice,
                "tipo": row.tipo,
                "stato": row.stato,
                "lat": row.lat,
                "lng": row.lng,
                "batteria": row.batteria,
            }
            for row in rows
        ]

    def trova_per_id(self, mezzo_id: UUID) -> dict | None:
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi WHERE id = :id
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"id": str(mezzo_id)}).fetchone()
        if row is None:
            return None
        return {
            "id": str(row.id),
            "codice": row.codice,
            "tipo": row.tipo,
            "stato": row.stato,
            "lat": row.lat,
            "lng": row.lng,
            "batteria": row.batteria,
        }

    # [IF-UT.02] CS-04 — verifica disponibilità batch per prenotazione multipla
    def trova_disponibili_da_lista(self, mezzo_ids: list[UUID]) -> list[dict]:
        if not mezzo_ids:
            return []
        ids_str = [str(i) for i in mezzo_ids]
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi
            WHERE id::text = ANY(:ids) AND stato = 'Disponibile'
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"ids": ids_str}).fetchall()
        return [
            {
                "id": str(row.id),
                "codice": row.codice,
                "tipo": row.tipo,
                "stato": row.stato,
                "lat": row.lat,
                "lng": row.lng,
                "batteria": row.batteria,
            }
            for row in rows
        ]

    # [IF-UT.04] CS-05 — mezzi sbloccabili: prenotati dall'utente + disponibili nelle vicinanze
    def trova_sbloccabili(
        self,
        utente_id: UUID,
        lat: float | None = None,
        lng: float | None = None,
        raggio_km: float = 0.5,
    ) -> list[dict]:
        sql = text("""
            SELECT m.id, m.codice, m.tipo, m.stato, m.lat, m.lng, m.batteria,
                   (p.id IS NOT NULL) AS prenotato,
                   p.id AS prenotazione_id
            FROM mezzi m
            LEFT JOIN prenotazioni p
                ON p.mezzo_id = m.id
               AND p.utente_id = :utente_id
               AND p.stato = 'attiva'
               AND p.scade_at > now()
            WHERE (m.stato = 'Prenotato' AND p.id IS NOT NULL)
               OR  m.stato = 'Disponibile'
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"utente_id": str(utente_id)}).fetchall()

        risultato = []
        for row in rows:
            if row.stato == "Disponibile" and lat is not None and lng is not None:
                if row.lat is None or row.lng is None:
                    continue
                if _haversine_km(lat, lng, row.lat, row.lng) > raggio_km:
                    continue
            risultato.append({
                "id": str(row.id),
                "codice": row.codice,
                "tipo": row.tipo,
                "stato": row.stato,
                "lat": row.lat,
                "lng": row.lng,
                "batteria": row.batteria,
                "prenotato": bool(row.prenotato),
                "prenotazione_id": str(row.prenotazione_id) if row.prenotazione_id else None,
            })
        return risultato

    def aggiorna_stato(self, mezzo_id: UUID, nuovo_stato: str) -> None:
        sql = text("UPDATE mezzi SET stato = :stato WHERE id = :id")
        with self._sessione() as s:
            s.execute(sql, {"stato": nuovo_stato, "id": str(mezzo_id)})
            s.commit()

    def esiste_by_codice(self, codice: str) -> bool:
        sql = text("SELECT EXISTS(SELECT 1 FROM mezzi WHERE codice = :codice) AS esiste")
        with self._sessione() as s:
            row = s.execute(sql, {"codice": codice}).fetchone()
        return bool(row.esiste) if row else False

    def crea(self, tipo: str, codice: str, lat: float, lng: float, stato: str) -> dict:
        sql = text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng)
            VALUES (:codice, :tipo, :stato, :lat, :lng)
            RETURNING id, codice, tipo, stato, lat, lng, batteria
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "codice": codice, "tipo": tipo, "stato": stato, "lat": lat, "lng": lng,
            }).fetchone()
            s.commit()
        if row is None:
            raise RuntimeError(f"INSERT mezzi non ha restituito righe per codice={codice!r}")
        return {
            "id": str(row.id),
            "codice": row.codice,
            "tipo": row.tipo,
            "stato": row.stato,
            "lat": row.lat,
            "lng": row.lng,
            "batteria": row.batteria,
        }

    def lista_tutti(self) -> list[dict]:
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi
            WHERE stato != 'Dismesso'
            ORDER BY created_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql).fetchall()
        return [
            {
                "id": str(row.id),
                "codice": row.codice,
                "tipo": row.tipo,
                "stato": row.stato,
                "lat": row.lat,
                "lng": row.lng,
                "batteria": row.batteria,
            }
            for row in rows
        ]

    def ha_corse_attive(self, mezzo_id: UUID) -> bool:
        sql = text("""
            SELECT EXISTS(
                SELECT 1 FROM corse
                WHERE mezzo_id = :mezzo_id
                  AND stato != 'terminata'
            ) AS ha_corse
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"mezzo_id": str(mezzo_id)}).fetchone()
        return bool(row.ha_corse) if row else False
