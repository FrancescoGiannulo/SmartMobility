import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Boolean, Integer, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from geoalchemy2 import Geometry
from database import Base


class TipoZona(str, Enum):
    operativa = "operativa"
    parcheggio = "parcheggio"
    limitata = "limitata"
    vietata = "vietata"


class Zona(Base):
    __tablename__ = "zone"

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    tipo: Mapped[TipoZona] = mapped_column(
        SAEnum(TipoZona, name="tipo_zona", create_type=False), nullable=False
    )
    perimetro: Mapped[bytes] = mapped_column(
        Geometry("POLYGON", srid=4326), nullable=False
    )
    limite_velocita: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attiva: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
