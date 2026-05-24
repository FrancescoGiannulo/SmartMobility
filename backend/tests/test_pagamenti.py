from decimal import Decimal
from providers.provider_pagamenti import ProviderPagamentiStub, RispostaPagamento, DatiNonValidiException


def test_provider_autorizza_ok():
    provider = ProviderPagamentiStub(deve_fallire=False)
    risposta = provider.autorizza("tok-abc", Decimal("5.00"))
    assert risposta.autorizzato is True
    assert risposta.transazione_id != ""


def test_provider_rifiuta():
    provider = ProviderPagamentiStub(deve_fallire=True)
    risposta = provider.autorizza("tok-abc", Decimal("5.00"))
    assert risposta.autorizzato is False
    assert risposta.transazione_id == ""


def test_provider_valida_dati_ok():
    provider = ProviderPagamentiStub(deve_fallire=False)
    token = provider.valida_dati_pagamento("carta", {"last_four": "1234"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_provider_valida_dati_non_validi():
    import pytest
    provider = ProviderPagamentiStub(deve_fallire=True)
    with pytest.raises(DatiNonValidiException):
        provider.valida_dati_pagamento("carta", {"last_four": "9999"})