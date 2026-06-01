-- ============================================================
-- Seed: Tariffe di default per ogni tipo di mezzo
-- Necessario per IF-UT.20 Effettua Pagamento
-- ============================================================

INSERT INTO tariffe (tipo_mezzo, costo_al_minuto, costo_al_km) VALUES
  ('monopattino', 0.0500, 0.0100),
  ('bicicletta',  0.0300, 0.0100),
  ('automobile',  0.2500, 0.1500)
ON CONFLICT (tipo_mezzo) DO NOTHING;
