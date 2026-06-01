import uuid
from dataclasses import dataclass
from decimal import Decimal


class DatiNonValidiException(Exception):
    pass


@dataclass
class RispostaPagamento:
    autorizzato: bool
    transazione_id: str


class ProviderPagamentiStub:

    def __init__(self, deve_fallire: bool = False):
        self.deve_fallire = deve_fallire

    def valida_dati_pagamento(self, tipo: str, dati: dict) -> str:
        """Valida i dati del metodo e restituisce un token. CS-13 passo 15-16."""
        if self.deve_fallire:
            raise DatiNonValidiException("Dati di pagamento non validi")
        return f"{tipo}-{uuid.uuid4()}"

    def autorizza(self, token_metodo: str, importo: Decimal) -> RispostaPagamento:
        """Autorizza un addebito. CS-12 passo 9-10."""
        if self.deve_fallire:
            return RispostaPagamento(autorizzato=False, transazione_id="")
        return RispostaPagamento(autorizzato=True, transazione_id=str(uuid.uuid4()))