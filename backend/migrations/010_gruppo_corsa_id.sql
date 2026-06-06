-- 010_gruppo_corsa_id.sql — [IF-UT.14] Storico Corse con corsa di gruppo
-- gruppo_corsa_id: UUID condiviso tra tutte le corse avviate nello stesso
-- sblocco multiplo. NULL per corse singole.

ALTER TABLE corse ADD COLUMN IF NOT EXISTS gruppo_corsa_id UUID;

CREATE INDEX IF NOT EXISTS idx_corse_gruppo ON corse (gruppo_corsa_id)
    WHERE gruppo_corsa_id IS NOT NULL;
