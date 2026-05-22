"""SQLAlchemy ORM models for database tables."""
import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, DateTime, text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Utente(Base):
    __tablename__ = "utenti"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    cognome: Mapped[str] = mapped_column(String, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    sospeso: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )


class Operatore(Base):
    __tablename__ = "operatori"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    durata_max_prenotazione_min: Mapped[int] = mapped_column(
        Integer, nullable=False, default=15
    )
    durata_periodo_grazia_min: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5
    )
    max_mezzi_per_utente: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )


class AmministrazionePubblica(Base):
    __tablename__ = "amministratori"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
