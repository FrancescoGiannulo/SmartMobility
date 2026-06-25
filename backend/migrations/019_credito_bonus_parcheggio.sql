-- [IF-OP.06] Contatore parcheggi corretti consecutivi e credito bonus accumulato dall'utente.
ALTER TABLE utenti
  ADD COLUMN IF NOT EXISTS contatore_parcheggi_corretti INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS credito_bonus NUMERIC(10, 2) NOT NULL DEFAULT 0.00;

-- Config regole_fine_corsa diventa una riga globale unica (zona_parcheggio_id sempre NULL).
-- Rimuove eventuali righe duplicate per-zona create prima di questa fix, mantenendo la più recente.
DELETE FROM regole_fine_corsa
WHERE id NOT IN (
  SELECT id FROM regole_fine_corsa ORDER BY created_at DESC LIMIT 1
);

UPDATE regole_fine_corsa SET zona_parcheggio_id = NULL;

-- [IF-OP.06] Esito della verifica parcheggio a fine corsa, persistito sulla corsa così che
-- il pagamento (endpoint separato) applichi la penale indipendentemente da cosa invia il client.
ALTER TABLE corse
  ADD COLUMN IF NOT EXISTS penale_parcheggio_applicata BOOLEAN NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS avviso_parcheggio TEXT;
