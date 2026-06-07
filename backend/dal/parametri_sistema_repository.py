from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text
from model.parametri_sistema import ParametriSistema

_SINGLETON_ID = 1

_DEFAULT_ROW = {
    "durata_max_prenotazione_min": 15,
    "durata_periodo_grazia_min": 5,
    "max_mezzi_per_utente": 1,
    "addebito_pausa_min": Decimal("0.0000"),
}


class ParametriSistemaRepository:

    def get(self, db: Session) -> ParametriSistema:
        """Legge la riga singleton con SQL grezzo — bypassa identity map e cache ORM."""
        row = db.execute(
            text("SELECT * FROM parametri_sistema WHERE id = :id"),
            {"id": _SINGLETON_ID},
        ).mappings().first()

        if row is None:
            db.execute(
                text("""
                    INSERT INTO parametri_sistema
                        (id, durata_max_prenotazione_min, durata_periodo_grazia_min,
                         max_mezzi_per_utente, addebito_pausa_min)
                    VALUES (:id, :dur, :grazia, :max_mezzi, :addebito)
                    ON CONFLICT DO NOTHING
                """),
                {
                    "id": _SINGLETON_ID,
                    "dur": _DEFAULT_ROW["durata_max_prenotazione_min"],
                    "grazia": _DEFAULT_ROW["durata_periodo_grazia_min"],
                    "max_mezzi": _DEFAULT_ROW["max_mezzi_per_utente"],
                    "addebito": _DEFAULT_ROW["addebito_pausa_min"],
                },
            )
            db.commit()
            row = db.execute(
                text("SELECT * FROM parametri_sistema WHERE id = :id"),
                {"id": _SINGLETON_ID},
            ).mappings().first()

        obj = ParametriSistema()
        obj.id = row["id"]
        obj.durata_max_prenotazione_min = row["durata_max_prenotazione_min"]
        obj.durata_periodo_grazia_min = row["durata_periodo_grazia_min"]
        obj.max_mezzi_per_utente = row["max_mezzi_per_utente"]
        obj.addebito_pausa_min = Decimal(str(row["addebito_pausa_min"]))
        return obj

    def save(
        self,
        durata_max_prenotazione_min: int,
        durata_periodo_grazia_min: int,
        max_mezzi_per_utente: int,
        addebito_pausa_min: Decimal,
        db: Session,
    ) -> ParametriSistema:
        """Aggiorna la riga singleton con SQL grezzo — garantisce la scrittura effettiva."""
        db.execute(
            text("""
                INSERT INTO parametri_sistema
                    (id, durata_max_prenotazione_min, durata_periodo_grazia_min,
                     max_mezzi_per_utente, addebito_pausa_min)
                VALUES (:id, :dur, :grazia, :max_mezzi, :addebito)
                ON CONFLICT (id) DO UPDATE
                    SET durata_max_prenotazione_min = EXCLUDED.durata_max_prenotazione_min,
                        durata_periodo_grazia_min   = EXCLUDED.durata_periodo_grazia_min,
                        max_mezzi_per_utente        = EXCLUDED.max_mezzi_per_utente,
                        addebito_pausa_min          = EXCLUDED.addebito_pausa_min
            """),
            {
                "id": _SINGLETON_ID,
                "dur": durata_max_prenotazione_min,
                "grazia": durata_periodo_grazia_min,
                "max_mezzi": max_mezzi_per_utente,
                "addebito": addebito_pausa_min,
            },
        )
        db.commit()
        return self.get(db)
