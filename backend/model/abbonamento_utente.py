import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class AbbonamentoUtente(Base):
    """[IF-UT.16] Abbonamento sottoscritto da un utente su un piano offerta."""

    __tablename__ = "abbonamenti_utente"
    __table_args__ = (
        CheckConstraint("data_fine > data_inizio", name="data_fine_dopo_inizio"),
        Index("idx_abbonamenti_utente_id", "utente_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("utenti.id", ondelete="CASCADE"), nullable=False
    )
    offerta_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("offerte.id", ondelete="RESTRICT"), nullable=False
    )
    data_inizio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    data_fine: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    stato: Mapped[str] = mapped_column(
        SAEnum("attivo", "scaduto", "annullato", name="stato_abbonamento", create_type=False),
        nullable=False,
        default="attivo",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
