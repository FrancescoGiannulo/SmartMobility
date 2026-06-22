-- 016_cleanup_scadenze.sql — Cleanup automatico prenotazioni scadute e abbonamenti scaduti
-- Tracciabilità: IF-UT.02 (Prenota mezzo), IF-UT.13 (Sottoscrive Abbonamento)
-- Usa: tabelle prenotazioni, mezzi, abbonamenti_utente, notifiche (tutte preesistenti)
-- Non introduce nuove entità — opera sulle classi già modellate nel Diagramma Classi.

-- ============================================================
-- 1. Funzione: cleanup prenotazioni scadute
-- ============================================================
-- Logica equivalente al check lazy in ServizioMobilita._sblocca_singolo,
-- ma eseguita proattivamente dal database a intervalli regolari.

CREATE OR REPLACE FUNCTION cleanup_prenotazioni_scadute()
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
BEGIN
    -- Marca come 'scaduta' tutte le prenotazioni attive oltre scade_at
    -- e notifica l'utente per ciascuna
    FOR rec IN
        SELECT p.id AS prenotazione_id,
               p.utente_id,
               p.mezzo_id,
               m.codice AS codice_mezzo
        FROM prenotazioni p
        JOIN mezzi m ON m.id = p.mezzo_id
        WHERE p.stato = 'attiva'
          AND p.scade_at < NOW()
    LOOP
        UPDATE prenotazioni SET stato = 'scaduta' WHERE id = rec.prenotazione_id;

        INSERT INTO notifiche (utente_id, messaggio)
        VALUES (
            rec.utente_id,
            'La tua prenotazione per il mezzo ' || rec.codice_mezzo || ' è scaduta.'
        );
    END LOOP;

    -- Rilascia i mezzi in stato 'Prenotato' che non hanno più prenotazioni attive
    UPDATE mezzi
    SET stato = 'Disponibile'
    WHERE stato = 'Prenotato'
      AND id NOT IN (
          SELECT mezzo_id FROM prenotazioni WHERE stato = 'attiva'
      );
END;
$$;

-- ============================================================
-- 2. Funzione: cleanup abbonamenti scaduti
-- ============================================================

CREATE OR REPLACE FUNCTION cleanup_abbonamenti_scaduti()
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN
        SELECT au.id AS abbonamento_id,
               au.utente_id,
               o.nome AS nome_piano
        FROM abbonamenti_utente au
        JOIN offerte o ON o.id = au.offerta_id
        WHERE au.stato = 'attivo'
          AND au.data_fine < NOW()
    LOOP
        UPDATE abbonamenti_utente SET stato = 'scaduto' WHERE id = rec.abbonamento_id;

        INSERT INTO notifiche (utente_id, messaggio)
        VALUES (
            rec.utente_id,
            'Il tuo abbonamento "' || rec.nome_piano || '" è scaduto.'
        );
    END LOOP;
END;
$$;

-- ============================================================
-- 3. Schedulazione pg_cron (richiede estensione abilitata su Supabase)
-- ============================================================
-- Abilitare pg_cron: Supabase Dashboard → Database → Extensions → pg_cron
-- Le righe seguenti vanno eseguite una volta dopo aver abilitato l'estensione.

-- Cleanup prenotazioni ogni 5 minuti
SELECT cron.schedule(
    'cleanup-prenotazioni-scadute',
    '*/5 * * * *',
    $$SELECT cleanup_prenotazioni_scadute()$$
);

-- Cleanup abbonamenti ogni giorno a mezzanotte
SELECT cron.schedule(
    'cleanup-abbonamenti-scaduti',
    '0 0 * * *',
    $$SELECT cleanup_abbonamenti_scaduti()$$
);