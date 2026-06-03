-- Seed mezzi demo: distribuiti nella zona operativa di Bari (lat 41.09-41.13, lng 16.82-16.92)
-- Tipi: monopattino, bicicletta, automobile
-- Stati: Disponibile, In uso, In manutenzione

INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria) VALUES
  -- Monopattini
  ('MON-001', 'monopattino', 'Disponibile',   41.1260, 16.8620, 88),
  ('MON-002', 'monopattino', 'Disponibile',   41.1195, 16.8410, 72),
  ('MON-003', 'monopattino', 'In uso',         41.1070, 16.8750, 55),
  ('MON-004', 'monopattino', 'Disponibile',   41.0990, 16.8830, 91),
  ('MON-005', 'monopattino', 'Disponibile',   41.1310, 16.8490, 64),
  ('MON-006', 'monopattino', 'In manutenzione', 41.1150, 16.9010, 12),
  ('MON-007', 'monopattino', 'Disponibile',   41.1085, 16.8310, 79),
  ('MON-008', 'monopattino', 'In uso',         41.1230, 16.8780, 43),
  ('MON-009', 'monopattino', 'Disponibile',   41.1020, 16.8680, 95),
  ('MON-010', 'monopattino', 'Disponibile',   41.1170, 16.8560, 83),

  -- Biciclette
  ('BIC-001', 'bicicletta',  'Disponibile',   41.1140, 16.8440, 100),
  ('BIC-002', 'bicicletta',  'Disponibile',   41.1280, 16.8700, 100),
  ('BIC-003', 'bicicletta',  'In uso',         41.1050, 16.8540, 100),
  ('BIC-004', 'bicicletta',  'Disponibile',   41.1200, 16.9050, 100),
  ('BIC-005', 'bicicletta',  'Disponibile',   41.0960, 16.8620, 100),
  ('BIC-006', 'bicicletta',  'In manutenzione', 41.1320, 16.8850, 100),
  ('BIC-007', 'bicicletta',  'Disponibile',   41.1100, 16.8260, 100),
  ('BIC-008', 'bicicletta',  'Disponibile',   41.1245, 16.8510, 100),

  -- Automobili
  ('AUT-001', 'automobile',  'Disponibile',   41.1180, 16.8650, 76),
  ('AUT-002', 'automobile',  'In uso',         41.1080, 16.8420, 52),
  ('AUT-003', 'automobile',  'Disponibile',   41.1260, 16.8900, 89),
  ('AUT-004', 'automobile',  'Disponibile',   41.0970, 16.8760, 61),
  ('AUT-005', 'automobile',  'In manutenzione', 41.1340, 16.8580, 8),
  ('AUT-006', 'automobile',  'Disponibile',   41.1130, 16.8190, 94),
  ('AUT-007', 'automobile',  'Disponibile',   41.1060, 16.9000, 70)
ON CONFLICT (codice) DO NOTHING;
