import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, Float, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class TipoMezzo(str, Enum):
    monopattino = "monopattino"
    bicicletta = "bicicletta"
    automobile = "automobile"


class StatoMezzo(str, Enum):
    disponibile = "Disponibile"
    prenotato = "Prenotato"
    in_uso = "In uso"
    in_pausa = "In pausa"
    in_manutenzione = "In manutenzione"
    fuori_servizio = "Fuori servizio"
    dismesso = "Dismesso"


class Mezzo(Base):
    __tablename__ = "mezzi"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    codice: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    tipo: Mapped[TipoMezzo] = mapped_column(
        SAEnum(TipoMezzo, name="tipo_mezzo", create_type=False), nullable=False
    )
    stato: Mapped[StatoMezzo] = mapped_column(
        SAEnum(StatoMezzo, name="stato_mezzo", create_type=False),
        nullable=False,
        default=StatoMezzo.disponibile,
    )
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    batteria: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
