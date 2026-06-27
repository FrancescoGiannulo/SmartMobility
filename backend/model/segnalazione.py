import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Text, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class StatoSegnalazione(str, Enum):
    aperta = "aperta"
    in_carico = "in_carico"
    risolta = "risolta"


class Segnalazione(Base):
    __tablename__ = "segnalazioni"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    tipologia: Mapped[str] = mapped_column(String, nullable=False)
    descrizione: Mapped[str] = mapped_column(Text, nullable=False)
    stato: Mapped[StatoSegnalazione] = mapped_column(
        SAEnum(StatoSegnalazione, name="stato_segnalazione", create_type=False),
        nullable=False,
        default=StatoSegnalazione.aperta,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
