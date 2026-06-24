import hashlib
import re
import uuid
from dataclasses import dataclass
from datetime import datetime
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
            return self._valida_carta(dati)
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, tipo))

    def _valida_carta(self, dati: dict) -> str:
        numero = (dati.get("numero") or "").replace(" ", "")
        if not re.fullmatch(r"\d{16}", numero):
            raise DatiNonValidiException("Il numero della carta deve essere di 16 cifre")

        cvc = dati.get("cvc") or ""
        if not re.fullmatch(r"\d{3,4}", cvc):
            raise DatiNonValidiException("Il CVC deve essere di 3 o 4 cifre")

        scadenza = dati.get("scadenza") or ""
        if not re.fullmatch(r"\d{2}/\d{2}", scadenza):
            raise DatiNonValidiException("La data di scadenza deve essere nel formato MM/AA")
        mese, anno = int(scadenza[:2]), int(scadenza[3:])
        if mese < 1 or mese > 12:
            raise DatiNonValidiException("Mese di scadenza non valido")
        now = datetime.now()
        anno_completo = 2000 + anno
        if anno_completo < now.year or (anno_completo == now.year and mese < now.month):
            raise DatiNonValidiException("La carta è scaduta")

        nome = (dati.get("nome_titolare") or "").strip()
        cognome = (dati.get("cognome_titolare") or "").strip()
        if not nome or not cognome:
            raise DatiNonValidiException("Nome e cognome del titolare sono obbligatori")

        return "carta-" + hashlib.sha256(numero.encode()).hexdigest()[:16]

    def autorizza(self, token_metodo: str, importo: Decimal) -> RispostaPagamento:
        """Autorizza un addebito. CS-12 passo 9-10."""
        if self.deve_fallire:
            return RispostaPagamento(autorizzato=False, transazione_id="")
        return RispostaPagamento(autorizzato=True, transazione_id=str(uuid.uuid4()))