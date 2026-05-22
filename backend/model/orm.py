"""
ORM SQLAlchemy 2.0 — modelli per utenti, operatori e amministratori.
Usato da test_schema.py e dal DAL per query tipizzate.
"""
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Utente(Base):
    """[IF-UT.17] Profilo dell'utente finale."""

    __tablename__ = "utenti"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    cognome: Mapped[str] = mapped_column(Text, nullable=False)
    telefono: Mapped[str | None] = mapped_column(Text, nullable=True)
    sospeso: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Operatore(Base):
    """Profilo dell'operatore del servizio."""

    __tablename__ = "operatori"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    durata_max_prenotazione_min: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    durata_periodo_grazia_min: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    max_mezzi_per_utente: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AmministrazionePubblica(Base):
    """Profilo dell'amministratore pubblico."""

    __tablename__ = "amministratori"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
