-- 008_consenso_privacy.sql — IIN-2 / GDPR art. 7 (Condizioni per il consenso)
-- Aggiunge il timestamp del consenso esplicito al trattamento dati nella tabella utenti.
-- NULL indica che il consenso non è stato registrato (utenti creati prima di questa migrazione).

ALTER TABLE utenti
    ADD COLUMN IF NOT EXISTS consenso_privacy_at TIMESTAMPTZ;

COMMENT ON COLUMN utenti.consenso_privacy_at IS
    'Timestamp del consenso esplicito al trattamento dei dati personali (GDPR art. 7). '
    'NULL = nessun consenso registrato (utenti precedenti alla migrazione).';
