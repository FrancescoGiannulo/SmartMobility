import pytest
import unittest.mock
from unittest.mock import MagicMock, patch
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import uuid


# ── Task 2: TariffaRepository ─────────────────────────────────────────────────

class TestTariffaRepository:

    def test_findAll_multi_row_e_id_come_stringa(self):
        from dal.tariffa_repository import TariffaRepository
        from model.tariffa import Tariffa, TipoMezzo as TMezzo

        id1 = uuid.uuid4()
        id2 = uuid.uuid4()

        row1 = MagicMock(spec=Tariffa)
        row1.id = id1
        row1.tipo_mezzo = TMezzo.monopattino
        row1.costo_al_minuto = Decimal("0.05")
        row1.costo_al_km = Decimal("0.10")

        row2 = MagicMock(spec=Tariffa)
        row2.id = id2
        row2.tipo_mezzo = TMezzo.bicicletta
        row2.costo_al_minuto = Decimal("0.03")
        row2.costo_al_km = Decimal("0.08")

        db = MagicMock()
        db.query.return_value.all.return_value = [row1, row2]

        repo = TariffaRepository(db)
        result = repo.findAll()

        assert len(result) == 2
        assert result[0]["id"] == str(id1)
        assert result[1]["tipo_mezzo"] == "bicicletta"
        assert result[0]["costo_al_km"] == "0.1000"

    def test_findAll_restituisce_lista_di_dict(self):
        from dal.tariffa_repository import TariffaRepository
        from model.tariffa import Tariffa, TipoMezzo as TMezzo

        row = MagicMock(spec=Tariffa)
        row.id = uuid.uuid4()
        row.tipo_mezzo = TMezzo.monopattino
        row.costo_al_minuto = Decimal("0.05")
        row.costo_al_km = Decimal("0.10")

        db = MagicMock()
        db.query.return_value.all.return_value = [row]

        repo = TariffaRepository(db)
        result = repo.findAll()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["tipo_mezzo"] == "monopattino"
        assert result[0]["costo_al_minuto"] == "0.0500"
        assert result[0]["costo_al_km"] == "0.1000"

    def test_findAll_lista_vuota(self):
        from dal.tariffa_repository import TariffaRepository

        db = MagicMock()
        db.query.return_value.all.return_value = []

        repo = TariffaRepository(db)
        result = repo.findAll()

        assert result == []


# ── Task 3: PromozioneRepository ─────────────────────────────────────────────

class TestPromozioneRepository:

    def test_getAttive_importabile(self):
        from dal.promozione_repository import PromozioneRepository
        assert hasattr(PromozioneRepository, "getAttive")

    def test_getAttive_restituisce_lista_di_dict(self):
        from dal.promozione_repository import PromozioneRepository
        from model.promozione import Promozione

        scadenza = datetime.now(tz=timezone.utc) + timedelta(days=7)

        row = MagicMock(spec=Promozione)
        row.id = uuid.uuid4()
        row.titolo = "Prima corsa gratis"
        row.descrizione = "Solo nuovi utenti"
        row.sconto_percentuale = Decimal("100")
        row.data_fine = scadenza

        db = MagicMock()
        db.query.return_value.filter.return_value.all.return_value = [row]

        repo = PromozioneRepository(db)
        result = repo.getAttive()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["titolo"] == "Prima corsa gratis"
        assert result[0]["sconto_percentuale"] == "100.00"

    def test_getAttive_lista_vuota(self):
        from dal.promozione_repository import PromozioneRepository

        db = MagicMock()
        db.query.return_value.filter.return_value.all.return_value = []

        repo = PromozioneRepository(db)
        result = repo.getAttive()

        assert result == []


# ── Task 4: ServizioPricing ──────────────────────────────────────────────────

class TestServizioPricing:

    def test_getTariffe_delega_al_repository(self):
        from bll.servizio_pricing import ServizioPricing

        tariffa_dict = {
            "id": str(uuid.uuid4()),
            "tipo_mezzo": "monopattino",
            "costo_al_minuto": "0.0500",
            "costo_al_km": "0.1000",
        }
        db = MagicMock()

        with patch("bll.servizio_pricing.TariffaRepository") as MockRepo:
            MockRepo.return_value.findAll.return_value = [tariffa_dict]
            svc = ServizioPricing(db)
            result = svc.getTariffe()

        MockRepo.assert_called_once_with(db)
        MockRepo.return_value.findAll.assert_called_once()
        assert result == [tariffa_dict]

    def test_getTariffe_lista_vuota(self):
        from bll.servizio_pricing import ServizioPricing

        db = MagicMock()
        with patch("bll.servizio_pricing.TariffaRepository") as MockRepo:
            MockRepo.return_value.findAll.return_value = []
            result = ServizioPricing(db).getTariffe()

        assert result == []

    def test_getPromozioniAttive_delega_al_repository(self):
        from bll.servizio_pricing import ServizioPricing

        promo_dict = {
            "id": str(uuid.uuid4()),
            "titolo": "Prima corsa gratis",
            "descrizione": None,
            "sconto_percentuale": "100.00",
            "data_fine": (datetime.now(tz=timezone.utc) + timedelta(days=7)).isoformat(),
        }
        db = MagicMock()

        with patch("bll.servizio_pricing.PromozioneRepository") as MockRepo:
            MockRepo.return_value.getAttive.return_value = [promo_dict]
            svc = ServizioPricing(db)
            result = svc.getPromozioniAttive()

        MockRepo.assert_called_once_with(db)
        MockRepo.return_value.getAttive.assert_called_once()
        assert result == [promo_dict]

    def test_getPromozioniAttive_lista_vuota(self):
        from bll.servizio_pricing import ServizioPricing

        db = MagicMock()
        with patch("bll.servizio_pricing.PromozioneRepository") as MockRepo:
            MockRepo.return_value.getAttive.return_value = []
            result = ServizioPricing(db).getPromozioniAttive()

        assert result == []
