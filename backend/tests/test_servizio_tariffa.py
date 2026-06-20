import uuid
from unittest.mock import MagicMock, patch
from decimal import Decimal


# [IF-OP.07 / IF-OP.08] Definisce Tariffa / Modifica Tariffa
class TestServizioTariffa:

    def test_get_tariffe_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        riga = MagicMock()
        riga.id = uuid.uuid4()
        riga.tipo_mezzo = "monopattino"
        riga.costo_al_minuto = Decimal("0.05")
        riga.costo_al_km = Decimal("0.10")

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.find_all.return_value = [riga]
            result = ServizioTariffa().get_tariffe()

        assert result == [{
            "id": str(riga.id),
            "tipo_mezzo": "monopattino",
            "costo_al_minuto": 0.05,
            "costo_al_km": 0.10,
        }]

    def test_get_tariffe_lista_vuota(self):
        from bll.servizio_tariffa import ServizioTariffa

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.find_all.return_value = []
            result = ServizioTariffa().get_tariffe()

        assert result == []

    def test_crea_tariffa_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        tariffa = MagicMock()
        tariffa.id = uuid.uuid4()
        tariffa.tipo_mezzo = "bicicletta"
        tariffa.costo_al_minuto = Decimal("0.03")
        tariffa.costo_al_km = Decimal("0.08")

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.exists_by_tipologia.return_value = False
            MockRepo.return_value.crea.return_value = tariffa
            result = ServizioTariffa().crea_tariffa("bicicletta", 0.03, 0.08)

        MockRepo.return_value.crea.assert_called_once_with("bicicletta", Decimal("0.03"), Decimal("0.08"))
        assert result["tipo_mezzo"] == "bicicletta"

    def test_crea_tariffa_gia_esistente(self):
        from bll.servizio_tariffa import ServizioTariffa, TariffaGiaEsistente

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.exists_by_tipologia.return_value = True
            try:
                ServizioTariffa().crea_tariffa("bicicletta", 0.03, 0.08)
                assert False, "doveva lanciare TariffaGiaEsistente"
            except TariffaGiaEsistente:
                pass
        MockRepo.return_value.crea.assert_not_called()

    def test_aggiorna_tariffa_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        tariffa = MagicMock()
        tariffa.id = uuid.uuid4()
        tariffa.tipo_mezzo = "monopattino"
        tariffa.costo_al_minuto = Decimal("0.07")
        tariffa.costo_al_km = Decimal("0.12")

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.aggiorna.return_value = tariffa
            result = ServizioTariffa().aggiorna_tariffa("monopattino", 0.07, 0.12)

        assert result["costo_al_minuto"] == 0.07

    def test_aggiorna_tariffa_non_trovata(self):
        from bll.servizio_tariffa import ServizioTariffa, TariffaNonTrovata

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.aggiorna.return_value = None
            try:
                ServizioTariffa().aggiorna_tariffa("monopattino", 0.07, 0.12)
                assert False, "doveva lanciare TariffaNonTrovata"
            except TariffaNonTrovata:
                pass
