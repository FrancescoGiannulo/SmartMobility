import uuid
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import pytest
from providers.provider_pagamenti import ProviderPagamentiStub, DatiNonValidiException
from bll.servizio_pricing import (
    ServizioPricing,
    MetodoNonTrovato,
    MetodoDuplicato,
    DatiNonValidi,
    NessunMetodoPredefinito,
    PagamentoRifiutato,
)
from dal.pagamento_repository import MetodoNonTrovatoException
from model.pagamento import StatoPagamento


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
    provider = ProviderPagamentiStub(deve_fallire=True)
    with pytest.raises(DatiNonValidiException):
        provider.valida_dati_pagamento("carta", {"last_four": "9999"})


# ── ServizioPricing unit tests (repo e provider completamente mockati) ──────


def _make_metodo(**kwargs) -> SimpleNamespace:
    defaults = dict(
        id=uuid.uuid4(),
        utente_id=uuid.uuid4(),
        tipo="carta",
        token_esterno="carta-tok-1",
        last_four="1234",
        predefinito=False,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _make_pagamento(**kwargs) -> SimpleNamespace:
    defaults = dict(
        id=uuid.uuid4(),
        corsa_id=uuid.uuid4(),
        utente_id=uuid.uuid4(),
        metodo_pagamento_id=uuid.uuid4(),
        importo=Decimal("5.00"),
        stato=StatoPagamento.completato,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _servizio(repo=None, provider=None) -> ServizioPricing:
    return ServizioPricing(repo=repo or MagicMock(), provider=provider or ProviderPagamentiStub())


# CS-13 — scenario base: aggiungi metodo OK
def test_aggiungi_metodo_ok():
    repo = MagicMock()
    repo.exists_by_token.return_value = False
    uid = uuid.uuid4()
    metodo = _make_metodo(utente_id=uid)
    repo.aggiungi_metodo.return_value = metodo

    svc = _servizio(repo=repo)
    result = svc.aggiungi_metodo(uid, "carta", {"last_four": "1234"})

    assert result["tipo"] == "carta"
    assert result["last_four"] == "1234"
    repo.aggiungi_metodo.assert_called_once()


# CS-13 — alternativo: dati non validi dal provider
def test_aggiungi_metodo_dati_non_validi():
    repo = MagicMock()
    svc = ServizioPricing(repo=repo, provider=ProviderPagamentiStub(deve_fallire=True))
    with pytest.raises(DatiNonValidi):
        svc.aggiungi_metodo(uuid.uuid4(), "carta", {"last_four": "9999"})
    repo.aggiungi_metodo.assert_not_called()


# CS-13 — alternativo: token già presente (duplicato)
def test_aggiungi_metodo_duplicato():
    repo = MagicMock()
    repo.exists_by_token.return_value = True
    svc = _servizio(repo=repo)
    with pytest.raises(MetodoDuplicato):
        svc.aggiungi_metodo(uuid.uuid4(), "carta", {"last_four": "1234"})
    repo.aggiungi_metodo.assert_not_called()


# IF-UT.21 — scenario base: imposta predefinito OK
def test_imposta_predefinito_ok():
    repo = MagicMock()
    uid = uuid.uuid4()
    mid = uuid.uuid4()
    repo.trova_metodo.return_value = _make_metodo(id=mid, utente_id=uid)

    svc = _servizio(repo=repo)
    svc.imposta_predefinito(mid, uid)

    repo.imposta_predefinito.assert_called_once_with(mid, uid)


# IF-UT.21 — alternativo: metodo non trovato
def test_imposta_predefinito_non_trovato():
    repo = MagicMock()
    repo.trova_metodo.side_effect = MetodoNonTrovatoException("non trovato")
    svc = _servizio(repo=repo)
    with pytest.raises(MetodoNonTrovato):
        svc.imposta_predefinito(uuid.uuid4(), uuid.uuid4())
    repo.imposta_predefinito.assert_not_called()


def _mock_pausa_e_parametri():
    """Patch per isolare effettua_pagamento dal DB per i test unitari."""
    mock_corsa_repo = MagicMock()
    mock_corsa_repo.return_value.get_pausa_accumulata_sec.return_value = 0

    mock_parametri = SimpleNamespace(
        durata_periodo_grazia_min=5,
        addebito_pausa_min=Decimal("0.00"),
    )
    mock_parametri_repo = MagicMock()
    mock_parametri_repo.return_value.get.return_value = mock_parametri

    return mock_corsa_repo, mock_parametri_repo


# CS-12 — scenario base: effettua pagamento OK
def test_effettua_pagamento_ok():
    repo = MagicMock()
    uid = uuid.uuid4()
    corsa_id = uuid.uuid4()
    metodo = _make_metodo(utente_id=uid, predefinito=True, token_esterno="carta-tok-1")
    pagamento = _make_pagamento(corsa_id=corsa_id, utente_id=uid, stato=StatoPagamento.completato)
    repo.trova_predefinito.return_value = metodo
    repo.crea_pagamento.return_value = pagamento

    mock_cr, mock_pr = _mock_pausa_e_parametri()
    with patch("bll.servizio_pricing.CorsaRepository", mock_cr), \
         patch("bll.servizio_pricing.ParametriSistemaRepository", mock_pr):
        svc = _servizio(repo=repo)
        svc.calcola_importo = MagicMock(return_value=Decimal("5.00"))
        result = svc.effettua_pagamento(corsa_id, uid, "bicicletta", 10.0, 2.0)

    assert result["stato"] == StatoPagamento.completato
    assert "transazione_id" in result
    repo.crea_pagamento.assert_called_once()


# CS-12 — alternativo: nessun metodo predefinito
def test_effettua_pagamento_nessun_predefinito():
    repo = MagicMock()
    repo.lista_metodi.return_value = []
    mock_cr, mock_pr = _mock_pausa_e_parametri()
    with patch("bll.servizio_pricing.CorsaRepository", mock_cr), \
         patch("bll.servizio_pricing.ParametriSistemaRepository", mock_pr):
        svc = _servizio(repo=repo)
        with pytest.raises(NessunMetodoPredefinito):
            svc.effettua_pagamento(uuid.uuid4(), uuid.uuid4(), "bicicletta", 10.0, 2.0)
    repo.crea_pagamento.assert_not_called()


# CS-12 — alternativo: provider rifiuta il pagamento
def test_effettua_pagamento_rifiutato():
    repo = MagicMock()
    uid = uuid.uuid4()
    corsa_id = uuid.uuid4()
    metodo = _make_metodo(utente_id=uid, predefinito=True)
    pagamento = _make_pagamento(corsa_id=corsa_id, utente_id=uid, stato=StatoPagamento.rifiutato)
    repo.trova_predefinito.return_value = metodo
    repo.crea_pagamento.return_value = pagamento

    provider = ProviderPagamentiStub(deve_fallire=True)
    mock_cr, mock_pr = _mock_pausa_e_parametri()
    with patch("bll.servizio_pricing.CorsaRepository", mock_cr), \
         patch("bll.servizio_pricing.ParametriSistemaRepository", mock_pr):
        svc = ServizioPricing(repo=repo, provider=provider)
        svc.calcola_importo = MagicMock(return_value=Decimal("5.00"))
        with pytest.raises(PagamentoRifiutato):
            svc.effettua_pagamento(corsa_id, uid, "bicicletta", 10.0, 2.0)

    # il pagamento viene comunque registrato come rifiutato
    repo.crea_pagamento.assert_called_once()
    args = repo.crea_pagamento.call_args
    assert args.kwargs.get("stato") == StatoPagamento.rifiutato or args.args[-1] == StatoPagamento.rifiutato


# lista metodi — scenario base
def test_lista_metodi():
    repo = MagicMock()
    uid = uuid.uuid4()
    repo.lista_metodi.return_value = [
        _make_metodo(utente_id=uid, tipo="carta", last_four="1234"),
        _make_metodo(utente_id=uid, tipo="paypal", last_four=None),
    ]
    svc = _servizio(repo=repo)
    result = svc.lista_metodi(uid)
    assert len(result) == 2
    assert result[0]["tipo"] == "carta"
    assert result[1]["last_four"] is None


# rimuovi metodo — metodo non trovato
def test_rimuovi_metodo_non_trovato():
    repo = MagicMock()
    repo.trova_metodo.side_effect = MetodoNonTrovatoException("non trovato")
    svc = _servizio(repo=repo)
    with pytest.raises(MetodoNonTrovato):
        svc.rimuovi_metodo(uuid.uuid4(), uuid.uuid4())
    repo.rimuovi_metodo.assert_not_called()