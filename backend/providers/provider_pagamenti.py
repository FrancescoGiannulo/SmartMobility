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
        if tipo == "carta":
            # Token deterministico su last_four: è l'unico dato disponibile per
            # rilevare duplicati nello stub (in produzione il provider userebbe
            # il numero completo della carta).
            last_four = dati.get("last_four") or ""
            return f"carta-{last_four}" if last_four else f"carta-{uuid.uuid4()}"
        # Per wallet digitali (paypal, google_pay, apple_pay) un utente ha un solo account:
        # token deterministico per tipo → rileva duplicati correttamente.
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, tipo))

    def autorizza(self, token_metodo: str, importo: Decimal) -> RispostaPagamento:
        """Autorizza un addebito. CS-12 passo 9-10."""
        if self.deve_fallire:
            return RispostaPagamento(autorizzato=False, transazione_id="")
        return RispostaPagamento(autorizzato=True, transazione_id=str(uuid.uuid4()))