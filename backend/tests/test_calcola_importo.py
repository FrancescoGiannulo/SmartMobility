from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from bll.servizio_pricing import ServizioPricing
from bll.servizio_tariffa import TariffaNonTrovata
import pytest


def _mock_session_con_riga(riga):
    mock_session = MagicMock()
    mock_session.execute.return_value.fetchone.return_value = riga
    return mock_session


class TestCalcolaImporto:

    def test_tariffa_solo_al_minuto(self):
        riga = SimpleNamespace(costo_al_minuto=Decimal("0.05"), costo_al_km=None)
        with patch("bll.servizio_pricing.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = _mock_session_con_riga(riga)
            importo = ServizioPricing().calcola_importo("monopattino", 10.0, 999.0)

        assert importo == Decimal("0.5")

    def test_tariffa_solo_al_km(self):
        riga = SimpleNamespace(costo_al_minuto=None, costo_al_km=Decimal("0.20"))
        with patch("bll.servizio_pricing.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = _mock_session_con_riga(riga)
            importo = ServizioPricing().calcola_importo("automobile", 999.0, 3.0)

        assert importo == Decimal("0.6")

    def test_tariffa_inesistente(self):
        with patch("bll.servizio_pricing.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = _mock_session_con_riga(None)
            with pytest.raises(TariffaNonTrovata):
                ServizioPricing().calcola_importo("monopattino", 10.0, 1.0)
