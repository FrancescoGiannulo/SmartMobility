import uuid
from decimal import Decimal
from unittest.mock import MagicMock, patch


class TestTariffaRepositoryFindAll:

    def test_find_all_propaga_costo_km_none(self):
        from dal.tariffa_repository import TariffaRepository

        riga = MagicMock()
        riga.id = uuid.uuid4()
        riga.tipo_mezzo = "monopattino"
        riga.costo_al_minuto = Decimal("0.05")
        riga.costo_al_km = None

        mock_session = MagicMock()
        mock_session.execute.return_value.fetchall.return_value = [riga]

        with patch("dal.tariffa_repository.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = mock_session
            result = TariffaRepository().find_all()

        assert len(result) == 1
        assert result[0].costo_al_minuto == Decimal("0.05")
        assert result[0].costo_al_km is None

    def test_crea_con_solo_costo_al_km(self):
        from dal.tariffa_repository import TariffaRepository

        mock_session = MagicMock()

        with patch("dal.tariffa_repository.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = mock_session
            TariffaRepository().crea("automobile", None, Decimal("0.20"))

        added = mock_session.add.call_args[0][0]
        assert added.tipo_mezzo == "automobile"
        assert added.costo_al_minuto is None
        assert added.costo_al_km == Decimal("0.20")
