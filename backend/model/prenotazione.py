import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class StatoPrenotazione(str, Enum):
    attiva = "attiva"
    scaduta = "scaduta"
    annullata = "annullata"
    convertita = "convertita"


class Prenotazione(Base):
    __tablename__ = "prenotazioni"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("utenti.id", ondelete="CASCADE"),
        nullable=False,
    )
    mezzo_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("mezzi.id", ondelete="RESTRICT"),
        nullable=False,
    )
    stato: Mapped[StatoPrenotazione] = mapped_column(
        SAEnum(StatoPrenotazione, name="stato_prenotazione", create_type=False),
        nullable=False,
        default=StatoPrenotazione.attiva,
    )
    scade_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
