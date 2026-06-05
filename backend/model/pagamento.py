import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, Boolean, Numeric, DateTime, text, ForeignKey, CheckConstraint, Index
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from database import Base


class TipoMetodoPagamento(str, Enum):
    google_pay = "google_pay"
    apple_pay = "apple_pay"
    paypal = "paypal"
    carta = "carta"


class StatoPagamento(str, Enum):
    completato = "completato"
    rifiutato = "rifiutato"
    in_attesa = "in_attesa"


class MetodoPagamento(Base):
    __tablename__ = "metodi_pagamento"
    __table_args__ = (
        Index(
            "metodi_pagamento_predefinito_unico",
            "utente_id",
            unique=True,
            postgresql_where=text("predefinito = true"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=False,
    )
    tipo: Mapped[TipoMetodoPagamento] = mapped_column(
        SAEnum(TipoMetodoPagamento, name="tipo_metodo_pagamento", create_type=False),
        nullable=False,
    )
    token_esterno: Mapped[str] = mapped_column(String, nullable=False)
    last_four: Mapped[str | None] = mapped_column(String(4), nullable=True)
    predefinito: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )


class Pagamento(Base):
    __tablename__ = "pagamenti"
    __table_args__ = (CheckConstraint("importo >= 0", name="pagamenti_importo_non_negativo"),)

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # [CS-07] nullable: il pagamento può essere per una corsa o un abbonamento
    corsa_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=True,
    )
    abbonamento_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=True,
    )
    utente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=False,
    )
    # [IF-UT.20] nullable: CS-12.1 il metodo potrebbe essere rimosso dopo un pagamento rifiutato
    metodo_pagamento_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("metodi_pagamento.id", ondelete="SET NULL"),
        nullable=True,
    )
    importo: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    # prezzo ante-sconto; None se non è stato applicato nessuno sconto
    importo_pieno: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    # promozione applicata sulla corsa (None se abbonamento o nessuno sconto)
    offerta_applicata_id: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("offerte.id", ondelete="SET NULL"),
        nullable=True,
    )
    stato: Mapped[StatoPagamento] = mapped_column(
        SAEnum(StatoPagamento, name="stato_pagamento", create_type=False),
        nullable=False,
        default=StatoPagamento.in_attesa,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
