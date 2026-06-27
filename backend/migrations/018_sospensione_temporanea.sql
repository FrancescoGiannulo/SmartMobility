-- 018_sospensione_temporanea.sql — IF-OP.09 Sospensione temporanea con riattivazione automatica
-- Aggiunge la colonna sospensione_fine per la scadenza della sospensione
-- e un job pg_cron per la riattivazione automatica degli account sospesi scaduti.

ALTER TABLE utenti ADD COLUMN IF NOT EXISTS sospensione_fine TIMESTAMPTZ;

-- ============================================================
-- Funzione: riattivazione automatica account sospesi scaduti
-- ============================================================

CREATE OR REPLACE FUNCTION cleanup_sospensioni_scadute()
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN
        SELECT id, nome, cognome
        FROM utenti
        WHERE sospeso = true
          AND sospensione_fine IS NOT NULL
          AND sospensione_fine < NOW()
    LOOP
        UPDATE utenti
        SET sospeso = false,
            motivazione_sospensione = NULL,
            sospeso_at = NULL,
            sospensione_fine = NULL
        WHERE id = rec.id;

        INSERT INTO notifiche (utente_id, messaggio)
        VALUES (
            rec.id,
            'Il tuo account è stato riattivato. La sospensione è terminata.'
        );
    END LOOP;
END;
$$;

-- Cleanup sospensioni ogni 15 minuti
SELECT cron.schedule(
    'cleanup-sospensioni-scadute',
    '*/15 * * * *',
    $$SELECT cleanup_sospensioni_scadute()$$
);
