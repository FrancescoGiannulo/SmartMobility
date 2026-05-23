import json
from contextlib import contextmanager
from uuid import UUID
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
from model.zona import Zona, TipoZona


class ZonaNonTrovataException(Exception):
    pass


class ZonaRepository:

    def __init__(self, db: Session | Engine) -> None:
        # Accetta sia Engine (test) sia Session (produzione via get_db())
        self._engine = db if isinstance(db, Engine) else None
        self._session = db if not isinstance(db, Engine) else None

    @contextmanager
    def _sessione(self):
        """Context manager centralizzato: restituisce la session iniettata o ne apre una nuova dall'engine."""
        if self._session is not None:
            yield self._session
        else:
            with Session(self._engine) as s:
                yield s

    def lista_zone(self, solo_attive: bool = True) -> list[dict]:
        sql = text("""
            SELECT id, nome, tipo, limite_velocita, attiva,
                   ST_AsGeoJSON(perimetro)::json AS perimetro
            FROM zone
            WHERE (:solo_attive = false OR attiva = true)
            ORDER BY created_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"solo_attive": solo_attive}).fetchall()
        return [
            {
                "id": row.id,
                "nome": row.nome,
                "tipo": row.tipo,
                "limite_velocita": row.limite_velocita,
                "attiva": row.attiva,
                "perimetro": row.perimetro,
            }
            for row in rows
        ]

    def trova_per_id(self, zona_id: UUID) -> dict:
        sql = text("""
            SELECT id, nome, tipo, limite_velocita, attiva,
                   ST_AsGeoJSON(perimetro)::json AS perimetro
            FROM zone WHERE id = :zona_id
        """)
        params = {"zona_id": str(zona_id)}
        with self._sessione() as s:
            row = s.execute(sql, params).fetchone()
        if not row:
            raise ZonaNonTrovataException(f"Zona {zona_id} non trovata")
        return {
            "id": row.id,
            "nome": row.nome,
            "tipo": row.tipo,
            "limite_velocita": row.limite_velocita,
            "attiva": row.attiva,
            "perimetro": row.perimetro,
        }

    def crea(self, nome: str, tipo: str, coordinate: list[list[float]], limite_velocita: int | None) -> Zona:
        geojson = json.dumps({
            "type": "Polygon",
            "coordinates": [coordinate],
        })
        sql = text("""
            INSERT INTO zone (nome, tipo, perimetro, limite_velocita)
            VALUES (:nome, :tipo, ST_GeomFromGeoJSON(:geojson), :limite)
            RETURNING id, nome, tipo, limite_velocita, attiva
        """)
        params = {"nome": nome, "tipo": tipo, "geojson": geojson, "limite": limite_velocita}
        with self._sessione() as s:
            row = s.execute(sql, params).fetchone()
            s.commit()
        if row is None:
            raise RuntimeError(f"INSERT INTO zone non ha restituito righe per nome={nome!r}")
        zona = Zona()
        zona.id = row.id
        zona.nome = row.nome
        zona.tipo = TipoZona(row.tipo)
        zona.limite_velocita = row.limite_velocita
        zona.attiva = row.attiva
        return zona

    def elimina(self, zona_id: UUID) -> None:
        sql = text("DELETE FROM zone WHERE id = :zona_id")
        params = {"zona_id": str(zona_id)}
        with self._sessione() as s:
            result = s.execute(sql, params)
            rowcount = result.rowcount
            s.commit()
        if rowcount == 0:
            raise ZonaNonTrovataException(f"Zona {zona_id} non trovata")

    # [IF-OP.02] Verifica che il poligono ricada all'interno di una zona operativa attiva
    def esiste_zona_operativa_contenente(self, coordinate: list[list[float]]) -> bool:
        """True se esiste almeno una zona operativa attiva che contiene ST_Within il poligono dato."""
        if coordinate[0] != coordinate[-1]:
            coordinate = coordinate + [coordinate[0]]
        geojson = json.dumps({"type": "Polygon", "coordinates": [coordinate]})
        sql = text("""
            SELECT EXISTS(
                SELECT 1 FROM zone
                WHERE tipo = 'operativa'
                  AND attiva = true
                  AND ST_Within(ST_GeomFromGeoJSON(:geojson), perimetro)
            )
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"geojson": geojson}).fetchone()
        return bool(row[0]) if row else False
