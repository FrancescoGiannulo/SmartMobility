import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
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

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # zona referenziata deve avere tipo='parcheggio' — verificato in ServizioMobilità
    zona_parcheggio_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("zone.id", ondelete="CASCADE"),
        nullable=False,
    )
    batteria_minima: Mapped[int | None] = mapped_column(
        Integer,
        CheckConstraint("batteria_minima BETWEEN 0 AND 100", name="batteria_minima_check"),
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
