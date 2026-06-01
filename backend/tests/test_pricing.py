import pytest
import unittest.mock
from unittest.mock import MagicMock, patch
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import uuid


# ── Task 2: TariffaRepository ─────────────────────────────────────────────────

class TestTariffaRepository:

    def test_findAll_importabile(self):
        from dal.tariffa_repository import TariffaRepository
        assert hasattr(TariffaRepository, "findAll")

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

    def test_findAll_lista_vuota(self):
        from dal.tariffa_repository import TariffaRepository

        db = MagicMock()
        db.query.return_value.all.return_value = []

        repo = TariffaRepository(db)
        result = repo.findAll()

        assert result == []
