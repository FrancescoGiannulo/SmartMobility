from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from model.regola_fine_corsa import RegolaFinecorsa, TipoVincoloFinecorsa


class RegolaFinecorsaRepository:

    def get_corrente(self, db: Session) -> Optional[RegolaFinecorsa]:
        """Restituisce l'unica configurazione globale, o None se non esiste."""
        return (
            db.query(RegolaFinecorsa)
            .filter(RegolaFinecorsa.zona_parcheggio_id.is_(None))
            .order_by(RegolaFinecorsa.created_at.desc())
            .first()
        )

    def salva(
        self,
        tipo_vincolo: TipoVincoloFinecorsa,
        penale_fuori_zona: Decimal,
        batteria_minima: Optional[int],
        bonus_parcheggi_corretti: Optional[int],
        bonus_valore: Optional[Decimal],
        db: Session,
    ) -> RegolaFinecorsa:
        """Upsert: aggiorna la config esistente o ne crea una nuova."""
        regola = self.get_corrente(db)
        if regola is None:
            regola = RegolaFinecorsa(zona_parcheggio_id=None)
            db.add(regola)
        regola.tipo_vincolo = tipo_vincolo
        regola.penale_fuori_zona = penale_fuori_zona
        regola.batteria_minima = batteria_minima
        regola.bonus_parcheggi_corretti = bonus_parcheggi_corretti
        regola.bonus_valore = bonus_valore
        db.commit()
        db.refresh(regola)
        return regola
