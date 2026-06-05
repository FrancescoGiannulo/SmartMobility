from decimal import Decimal
from sqlalchemy import CheckConstraint, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class ParametriSistema(Base):
    """[CS-15] Parametri numerici operativi del sistema — riga singleton (id = 1)."""

    __tablename__ = "parametri_sistema"
    __table_args__ = (
        CheckConstraint("id = 1", name="singleton"),
        CheckConstraint("durata_max_prenotazione_min >= 0", name="durata_max_prenotazione_non_negativa"),
        CheckConstraint("durata_periodo_grazia_min >= 0", name="durata_grazia_non_negativa"),
        CheckConstraint("max_mezzi_per_utente >= 1", name="max_mezzi_positivo"),
        CheckConstraint("addebito_pausa_min >= 0", name="addebito_non_negativo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    durata_max_prenotazione_min: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    durata_periodo_grazia_min: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    max_mezzi_per_utente: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    addebito_pausa_min: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False, default=Decimal("0.0000"))
