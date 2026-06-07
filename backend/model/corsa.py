import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import DateTime, Integer, Numeric, Float, text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class StatoCorsa(str, Enum):
    in_uso = "in_uso"
    in_pausa = "in_pausa"
    terminata = "terminata"


class Corsa(Base):
    __tablename__ = "corse"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("utenti.id", ondelete="RESTRICT"),
        nullable=False,
    )
    mezzo_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("mezzi.id", ondelete="RESTRICT"),
        nullable=False,
    )
    # [IF-UT.04] nullable: CS-10 permette sblocco diretto senza prenotazione
    prenotazione_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("prenotazioni.id", ondelete="SET NULL"),
        nullable=True,
    )
    gruppo_corsa_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True), nullable=True
    )
    stato: Mapped[StatoCorsa] = mapped_column(
        SAEnum(StatoCorsa, name="stato_corsa", create_type=False),
        nullable=False,
        default=StatoCorsa.in_uso,
    )
    inizio_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fine_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    distanza_km: Mapped[Decimal | None] = mapped_column(Numeric(10, 3), nullable=True)
    inizio_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    inizio_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    fine_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    fine_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    pausa_inizio_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    pausa_durata_accumulata_sec: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
