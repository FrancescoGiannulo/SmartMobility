-- 007_gdpr_cascade.sql — IIN-2 / GDPR art. 17 (Diritto all'oblio)
-- Garantisce che eliminando l'utente da auth.users si eliminino in cascata
-- i dati personali dalla tabella utenti.
-- NOTA: in Supabase la FK verso auth.users va gestita con attenzione alle policy RLS.

DO $$
BEGIN
    -- Rimuove il vecchio vincolo se esiste (senza CASCADE)
    IF EXISTS (
        SELECT 1
        FROM information_schema.table_constraints
        WHERE constraint_name = 'utenti_id_fkey'
          AND table_name = 'utenti'
    ) THEN
        ALTER TABLE utenti DROP CONSTRAINT utenti_id_fkey;
    END IF;

    -- Aggiunge il vincolo con ON DELETE CASCADE
    ALTER TABLE utenti
        ADD CONSTRAINT utenti_id_fkey
        FOREIGN KEY (id)
        REFERENCES auth.users(id)
        ON DELETE CASCADE;
END $$;
