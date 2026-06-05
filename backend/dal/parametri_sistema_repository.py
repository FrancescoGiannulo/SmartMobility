from decimal import Decimal
from sqlalchemy.orm import Session
from model.parametri_sistema import ParametriSistema

_SINGLETON_ID = 1


class ParametriSistemaRepository:

    def get(self, db: Session) -> ParametriSistema:
        """Restituisce l'unica riga di configurazione (sempre presente dopo la migrazione)."""
        row = db.query(ParametriSistema).filter(ParametriSistema.id == _SINGLETON_ID).first()
        if row is None:
            row = ParametriSistema(id=_SINGLETON_ID)
            db.add(row)
            db.commit()
            db.refresh(row)
        return row

    def save(
        self,
        durata_max_prenotazione_min: int,
        durata_periodo_grazia_min: int,
        max_mezzi_per_utente: int,
        addebito_pausa_min: Decimal,
        db: Session,
    ) -> ParametriSistema:
        """Aggiorna la riga singleton con i nuovi valori."""
        row = self.get(db)
        row.durata_max_prenotazione_min = durata_max_prenotazione_min
        row.durata_periodo_grazia_min = durata_periodo_grazia_min
        row.max_mezzi_per_utente = max_mezzi_per_utente
        row.addebito_pausa_min = addebito_pausa_min
        db.commit()
        db.refresh(row)
        return row
