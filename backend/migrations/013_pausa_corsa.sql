-- ============================================================
-- 013_pausa_corsa.sql — Tracciamento pausa corsa
-- Aggiunge pausa_inizio_at e pausa_durata_accumulata_sec a corse
-- per supportare addebito_pausa_min e durata_periodo_grazia_min
-- di ParametriSistema (IF-OP.09 / IF-OP.14)
-- ============================================================

ALTER TABLE corse
    ADD COLUMN IF NOT EXISTS pausa_inizio_at           TIMESTAMPTZ  DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS pausa_durata_accumulata_sec INTEGER NOT NULL DEFAULT 0;
