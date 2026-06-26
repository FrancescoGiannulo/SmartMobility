import pytest
from pydantic import ValidationError
from controllers.schemas import CreaTariffaRequest


class TestCreaTariffaRequestXor:

    def test_solo_costo_al_minuto_valido(self):
        req = CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=0.15, costo_al_km=None)
        assert req.costo_al_minuto == 0.15
        assert req.costo_al_km is None

    def test_solo_costo_al_km_valido(self):
        req = CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=None, costo_al_km=0.20)
        assert req.costo_al_km == 0.20
        assert req.costo_al_minuto is None

    def test_entrambi_popolati_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=0.15, costo_al_km=0.20)

    def test_nessuno_popolato_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=None, costo_al_km=None)

    def test_valore_zero_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=0, costo_al_km=None)

    def test_valore_negativo_rifiutato(self):
        with pytest.raises(ValidationError):
            CreaTariffaRequest(tipo_mezzo="monopattino", costo_al_minuto=-0.05, costo_al_km=None)
