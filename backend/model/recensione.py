import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, Text, DateTime, Integer, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class Recensione(Base):
    __tablename__ = "recensioni"
    __table_args__ = (
        CheckConstraint("voto BETWEEN 1 AND 5", name="recensioni_voto_check"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    voto: Mapped[int] = mapped_column(Integer, nullable=False)
    commento: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
