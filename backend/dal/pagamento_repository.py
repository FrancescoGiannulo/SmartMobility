import uuid
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import engine
from model.pagamento import MetodoPagamento, Pagamento, StatoPagamento


class MetodoNonTrovatoException(Exception):
    pass


class PagamentoRepository:

    # [IF-UT.06] Salva Metodi di Pagamento
    def aggiungi_metodo(
        self,
        utente_id: uuid.UUID,
        tipo: str,
        token_esterno: str,
        last_four: str | None,
    ) -> MetodoPagamento:
        with Session(engine) as session:
            metodo = MetodoPagamento(
                utente_id=utente_id,
                tipo=tipo,
                token_esterno=token_esterno,
                last_four=last_four,
                predefinito=False,
            )
            session.add(metodo)
            session.commit()
            session.refresh(metodo)
            return metodo

    def lista_metodi(self, utente_id: uuid.UUID) -> list[MetodoPagamento]:
        with Session(engine) as session:
            rows = session.execute(
                text(
                    "SELECT id, tipo, last_four, predefinito "
                    "FROM metodi_pagamento WHERE utente_id = :uid "
                    "ORDER BY created_at"
                ),
                {"uid": str(utente_id)},
            ).fetchall()
            return [
                MetodoPagamento(
                    id=r.id,
                    utente_id=utente_id,
                    tipo=r.tipo,
                    token_esterno="",
                    last_four=r.last_four,
                    predefinito=r.predefinito,
                )
                for r in rows
            ]

    def trova_metodo(self, metodo_id: uuid.UUID, utente_id: uuid.UUID) -> MetodoPagamento:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT id, tipo, token_esterno, last_four, predefinito "
                    "FROM metodi_pagamento WHERE id = :mid AND utente_id = :uid"
                ),
                {"mid": str(metodo_id), "uid": str(utente_id)},
            ).fetchone()
        if not row:
            raise MetodoNonTrovatoException(f"Metodo {metodo_id} non trovato")
        return MetodoPagamento(
            id=row.id,
            utente_id=utente_id,
            tipo=row.tipo,
            token_esterno=row.token_esterno,
            last_four=row.last_four,
            predefinito=row.predefinito,
        )

    def exists_by_token(self, token_esterno: str, utente_id: uuid.UUID) -> bool:
        with Session(engine) as session:
            result = session.execute(
                text(
                    "SELECT 1 FROM metodi_pagamento WHERE token_esterno = :tok "
                    "AND utente_id = :uid LIMIT 1"
                ),
                {"tok": token_esterno, "uid": str(utente_id)},
            ).fetchone()
        return result is not None

    def exists_carta(self, last_four: str, utente_id: uuid.UUID) -> bool:
        with Session(engine) as session:
            result = session.execute(
                text(
                    "SELECT 1 FROM metodi_pagamento WHERE tipo = 'carta' "
                    "AND last_four = :lf AND utente_id = :uid LIMIT 1"
                ),
                {"lf": last_four, "uid": str(utente_id)},
            ).fetchone()
        return result is not None

    # [IF-UT.21] Imposta Metodo di Pagamento predefinito
    def imposta_predefinito(self, metodo_id: uuid.UUID, utente_id: uuid.UUID) -> None:
        with Session(engine) as session:
            session.execute(
                text(
                    "UPDATE metodi_pagamento SET predefinito = false "
                    "WHERE utente_id = :uid"
                ),
                {"uid": str(utente_id)},
            )
            session.execute(
                text(
                    "UPDATE metodi_pagamento SET predefinito = true "
                    "WHERE id = :mid AND utente_id = :uid"
                ),
                {"mid": str(metodo_id), "uid": str(utente_id)},
            )
            session.commit()

    def rimuovi_metodo(self, metodo_id: uuid.UUID, utente_id: uuid.UUID) -> None:
        with Session(engine) as session:
            session.execute(
                text(
                    "DELETE FROM metodi_pagamento WHERE id = :mid AND utente_id = :uid"
                ),
                {"mid": str(metodo_id), "uid": str(utente_id)},
            )
            session.commit()

    def trova_predefinito(self, utente_id: uuid.UUID) -> MetodoPagamento | None:
        with Session(engine) as session:
            row = session.execute(
                text(
                    "SELECT id, tipo, token_esterno, last_four "
                    "FROM metodi_pagamento WHERE utente_id = :uid AND predefinito = true"
                ),
                {"uid": str(utente_id)},
            ).fetchone()
        if not row:
            return None
        return MetodoPagamento(
            id=row.id,
            utente_id=utente_id,
            tipo=row.tipo,
            token_esterno=row.token_esterno,
            last_four=row.last_four,
            predefinito=True,
        )

    # [IF-UT.14] Trova pagamento associato a una corsa
    def trova_per_corsa(self, corsa_id: uuid.UUID) -> Pagamento | None:
        with Session(engine) as session:
            return (
                session.query(Pagamento)
                .filter(Pagamento.corsa_id == corsa_id)
                .first()
            )

    # [IF-UT.14] Lista pagamenti di un utente ordinati per data
    def trova_per_utente(self, utente_id: uuid.UUID) -> list[Pagamento]:
        with Session(engine) as session:
            return (
                session.query(Pagamento)
                .filter(Pagamento.utente_id == utente_id)
                .order_by(Pagamento.created_at.desc())
                .all()
            )

    # [CS-07] Effettua Pagamento — generico per corsa o abbonamento
    def crea_pagamento(
        self,
        utente_id: uuid.UUID,
        metodo_id: uuid.UUID | None,
        importo: Decimal,
        stato: StatoPagamento,
        corsa_id: uuid.UUID | None = None,
        abbonamento_id: uuid.UUID | None = None,
        importo_pieno: Decimal | None = None,
        offerta_applicata_id: uuid.UUID | None = None,
    ) -> Pagamento:
        with Session(engine) as session:
            pagamento = Pagamento(
                corsa_id=corsa_id,
                abbonamento_id=abbonamento_id,
                utente_id=utente_id,
                metodo_pagamento_id=metodo_id,
                importo=importo,
                importo_pieno=importo_pieno,
                offerta_applicata_id=offerta_applicata_id,
                stato=stato,
            )
            session.add(pagamento)
            session.commit()
            session.refresh(pagamento)
            return pagamento
