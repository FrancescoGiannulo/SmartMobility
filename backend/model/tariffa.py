import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Numeric, DateTime, text, CheckConstraint, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from model.mezzo import TipoMezzo
from database import Base


class Tariffa(Base):
    __tablename__ = "tariffe"
    __table_args__ = (
        CheckConstraint(
            "(costo_al_minuto IS NOT NULL AND costo_al_km IS NULL AND costo_al_minuto > 0) "
            "OR (costo_al_km IS NOT NULL AND costo_al_minuto IS NULL AND costo_al_km > 0)",
            name="tariffa_costo_xor",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tipo_mezzo: Mapped[TipoMezzo] = mapped_column(
        SAEnum(TipoMezzo, name="tipo_mezzo", create_type=False),
        unique=True,
        nullable=False,
    )
    costo_al_minuto: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    costo_al_km: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    aggiornata_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=func.now(),
    )
