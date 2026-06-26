import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlalchemy import Integer, Numeric, DateTime, text, ForeignKey, CheckConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class TipoVincoloFinecorsa(str, Enum):
    penale = "penale"
    divieto = "divieto"
    avviso = "avviso"


class RegolaFinecorsa(Base):
    __tablename__ = "regole_fine_corsa"
    __table_args__ = (
        CheckConstraint(
            "bonus_parcheggi_corretti IS NULL OR bonus_parcheggi_corretti > 0",
            name="bonus_parcheggi_check",
        ),
        CheckConstraint(
            "bonus_valore IS NULL OR bonus_valore > 0",
            name="bonus_valore_check",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    zona_parcheggio_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("zone.id", ondelete="CASCADE"),
        nullable=True,
    )
    penale_fuori_zona: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00")
    )
    tipo_vincolo: Mapped[TipoVincoloFinecorsa] = mapped_column(
        SAEnum(TipoVincoloFinecorsa, name="tipo_vincolo_fine_corsa", create_type=False),
        nullable=False,
        default=TipoVincoloFinecorsa.avviso,
    )
    bonus_parcheggi_corretti: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bonus_valore: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
