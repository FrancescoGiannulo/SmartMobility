import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Text, Boolean, Numeric, DateTime, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Promozione(Base):
    __tablename__ = "promozioni"
    __table_args__ = (
        CheckConstraint(
            "sconto_percentuale > 0 AND sconto_percentuale <= 100",
            name="promozione_sconto_valido",
        ),
        CheckConstraint(
            "data_fine > data_inizio",
            name="promozione_date_valide",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    titolo: Mapped[str] = mapped_column(Text, nullable=False)
    descrizione: Mapped[str | None] = mapped_column(Text, nullable=True)
    sconto_percentuale: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    data_inizio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    data_fine: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    attiva: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
