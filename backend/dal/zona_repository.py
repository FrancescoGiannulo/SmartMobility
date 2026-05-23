import json
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

    def lista_zone(self, solo_attive: bool = True) -> list[dict]:
        filtro = "WHERE attiva = true" if solo_attive else ""
        sql = text(f"""
            SELECT id, nome, tipo, limite_velocita, attiva,
                   ST_AsGeoJSON(perimetro)::json AS perimetro
            FROM zone {filtro}
            ORDER BY created_at DESC
        """)
        if self._session is not None:
            rows = self._session.execute(sql).fetchall()
        else:
            with Session(self._engine) as s:
                rows = s.execute(sql).fetchall()
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

    def trova_per_id(self, id: UUID) -> dict:
        sql = text("""
            SELECT id, nome, tipo, limite_velocita, attiva,
                   ST_AsGeoJSON(perimetro)::json AS perimetro
            FROM zone WHERE id = :id
        """)
        params = {"id": str(id)}
        if self._session is not None:
            row = self._session.execute(sql, params).fetchone()
        else:
            with Session(self._engine) as s:
                row = s.execute(sql, params).fetchone()
        if not row:
            raise ZonaNonTrovataException(f"Zona {id} non trovata")
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
        if self._session is not None:
            row = self._session.execute(sql, params).fetchone()
            self._session.commit()
        else:
            with Session(self._engine) as s:
                row = s.execute(sql, params).fetchone()
                s.commit()
        zona = Zona()
        zona.id = row.id
        zona.nome = row.nome
        zona.tipo = TipoZona(row.tipo)
        zona.limite_velocita = row.limite_velocita
        zona.attiva = row.attiva
        return zona

    def elimina(self, id: UUID) -> None:
        sql = text("DELETE FROM zone WHERE id = :id")
        params = {"id": str(id)}
        if self._session is not None:
            result = self._session.execute(sql, params)
            self._session.commit()
            rowcount = result.rowcount
        else:
            with Session(self._engine) as s:
                result = s.execute(sql, params)
                rowcount = result.rowcount
                s.commit()
        if rowcount == 0:
            raise ZonaNonTrovataException(f"Zona {id} non trovata")
