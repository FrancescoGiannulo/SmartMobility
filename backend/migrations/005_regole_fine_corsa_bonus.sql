-- Rende zona_parcheggio_id opzionale (config globale senza zona specifica)
ALTER TABLE regole_fine_corsa
  ALTER COLUMN zona_parcheggio_id DROP NOT NULL;

-- Aggiunge campi bonus
ALTER TABLE regole_fine_corsa
  ADD COLUMN IF NOT EXISTS bonus_parcheggi_corretti INTEGER,
  ADD COLUMN IF NOT EXISTS bonus_valore NUMERIC(10, 2);

ALTER TABLE regole_fine_corsa
  ADD CONSTRAINT IF NOT EXISTS bonus_parcheggi_check
    CHECK (bonus_parcheggi_corretti IS NULL OR bonus_parcheggi_corretti > 0),
  ADD CONSTRAINT IF NOT EXISTS bonus_valore_check
    CHECK (bonus_valore IS NULL OR bonus_valore > 0);
