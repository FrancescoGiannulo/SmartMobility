import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Text, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class TipoSuggerimento(str, Enum):
    risparmio = "risparmio"
    percorso = "percorso"
    abbonamento = "abbonamento"
    orario = "orario"
    mezzo = "mezzo"
    generale = "generale"


class StatoSuggerimento(str, Enum):
    nuovo = "nuovo"
    visto = "visto"


class Suggerimento(Base):
    __tablename__ = "suggerimenti"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    tipo: Mapped[TipoSuggerimento] = mapped_column(
        SAEnum(TipoSuggerimento, name="tipo_suggerimento", create_type=False),
        nullable=False,
        default=TipoSuggerimento.generale,
    )
    testo: Mapped[str] = mapped_column(Text, nullable=False)
    dati_contesto: Mapped[dict] = mapped_column(JSONB, default=dict)
    stato: Mapped[StatoSuggerimento] = mapped_column(
        SAEnum(StatoSuggerimento, name="stato_suggerimento", create_type=False),
        nullable=False,
        default=StatoSuggerimento.nuovo,
    )
    creato_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
