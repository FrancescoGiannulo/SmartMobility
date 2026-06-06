-- ============================================================
-- 008_generalizza_pagamento.sql — CS-07 Effettua Pagamento (generalizzato)
-- corsa_id diventa nullable; aggiunto abbonamento_id opzionale
-- ============================================================

ALTER TABLE pagamenti ALTER COLUMN corsa_id DROP NOT NULL;

ALTER TABLE pagamenti
    ADD COLUMN abbonamento_id UUID REFERENCES abbonamenti_utente(id) ON DELETE SET NULL;
