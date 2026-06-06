import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import Text, Numeric, Integer, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Offerta(Base):
    """Classe base — campi comuni a promozione e abbonamento (STI su tabella 'offerte')."""

    __tablename__ = "offerte"
    __mapper_args__ = {
        "polymorphic_on": "tipo",
        "polymorphic_identity": None,
    }

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    tipo: Mapped[str] = mapped_column(
        SAEnum("promozione", "abbonamento", name="tipo_offerta", create_type=False),
        nullable=False,
    )
    stato: Mapped[str] = mapped_column(
        SAEnum("bozza", "attiva", "scaduta", name="stato_offerta", create_type=False),
        nullable=False,
        server_default="attiva",
    )
    descrizione: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_inizio: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    data_scadenza: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    # Campi specifici di Promozione (null per Abbonamento)
    sconto_percentuale: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True)

    # Campi specifici di Abbonamento (null per Promozione)
    prezzo: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    durata_giorni: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tipo_mezzo: Mapped[Optional[str]] = mapped_column(
        SAEnum("monopattino", "bicicletta", "automobile", name="tipo_mezzo", create_type=False),
        nullable=True,
    )

    def is_attiva(self) -> bool:
        return self.stato == "attiva"

    def get_id(self) -> uuid.UUID:
        return self.id


class Promozione(Offerta):
    """Offerta di tipo promozione: sconto percentuale con scadenza."""

    __mapper_args__ = {"polymorphic_identity": "promozione"}


class Abbonamento(Offerta):
    """Offerta di tipo abbonamento: prezzo fisso per una durata, opzionalmente per tipo mezzo."""

    __mapper_args__ = {"polymorphic_identity": "abbonamento"}
