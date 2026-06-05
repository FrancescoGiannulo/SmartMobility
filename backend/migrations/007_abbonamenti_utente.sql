-- ============================================================
-- 007_abbonamenti_utente.sql — IF-UT.16 Sottoscrive Abbonamento
-- ============================================================

CREATE TYPE stato_abbonamento AS ENUM ('attivo', 'scaduto', 'annullato');

CREATE TABLE abbonamenti_utente (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id   UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
    offerta_id  UUID NOT NULL REFERENCES offerte(id) ON DELETE RESTRICT,
    data_inizio TIMESTAMPTZ NOT NULL DEFAULT now(),
    data_fine   TIMESTAMPTZ NOT NULL,
    stato       stato_abbonamento NOT NULL DEFAULT 'attivo',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT data_fine_dopo_inizio CHECK (data_fine > data_inizio)
);

CREATE INDEX idx_abbonamenti_utente_id ON abbonamenti_utente(utente_id);
