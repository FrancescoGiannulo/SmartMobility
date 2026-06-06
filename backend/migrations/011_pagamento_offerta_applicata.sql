-- 011_pagamento_offerta_applicata.sql
-- Traccia il prezzo originale e la promozione applicata sul pagamento di una corsa
ALTER TABLE pagamenti
    ADD COLUMN IF NOT EXISTS importo_pieno     NUMERIC(10, 2),
    ADD COLUMN IF NOT EXISTS offerta_applicata_id UUID REFERENCES offerte(id) ON DELETE SET NULL;
