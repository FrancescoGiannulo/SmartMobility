-- ============================================================
-- Seed dati di test per suggerimenti (gabriele2@gmail.com)
-- Eseguire su Supabase SQL Editor — NON committare
-- ============================================================

DO $$
DECLARE
    uid UUID;
    m1  UUID; m2 UUID; m3 UUID;
    c1  UUID; c2 UUID; c3 UUID; c4 UUID; c5 UUID; c6 UUID; c7 UUID;
    off_id UUID;
BEGIN
    -- 1. Trova l'utente
    SELECT id INTO uid FROM utenti WHERE id IN (
        SELECT id FROM auth.users WHERE email = 'gabriele2@gmail.com'
    );
    IF uid IS NULL THEN
        RAISE EXCEPTION 'Utente gabriele2@gmail.com non trovato';
    END IF;

    -- 2. Prendi 3 mezzi disponibili (uno per tipo se possibile)
    SELECT id INTO m1 FROM mezzi WHERE tipo = 'monopattino' AND stato = 'Disponibile' LIMIT 1;
    SELECT id INTO m2 FROM mezzi WHERE tipo = 'bicicletta'  AND stato = 'Disponibile' LIMIT 1;
    SELECT id INTO m3 FROM mezzi WHERE tipo = 'automobile'  AND stato = 'Disponibile' LIMIT 1;

    IF m1 IS NULL THEN SELECT id INTO m1 FROM mezzi LIMIT 1; END IF;
    IF m2 IS NULL THEN m2 := m1; END IF;
    IF m3 IS NULL THEN m3 := m1; END IF;

    -- 3. Inserisci 7 corse terminate (ultime 2 settimane, orari vari)
    c1 := gen_random_uuid();
    INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
    VALUES (c1, uid, m1, 'terminata', now() - interval '13 days' + interval '8 hours',
            now() - interval '13 days' + interval '8 hours 25 minutes', 3.2);

    c2 := gen_random_uuid();
    INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
    VALUES (c2, uid, m1, 'terminata', now() - interval '11 days' + interval '7 hours 30 minutes',
            now() - interval '11 days' + interval '7 hours 50 minutes', 2.8);

    c3 := gen_random_uuid();
    INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
    VALUES (c3, uid, m2, 'terminata', now() - interval '9 days' + interval '18 hours',
            now() - interval '9 days' + interval '18 hours 40 minutes', 5.1);

    c4 := gen_random_uuid();
    INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
    VALUES (c4, uid, m1, 'terminata', now() - interval '7 days' + interval '8 hours 15 minutes',
            now() - interval '7 days' + interval '8 hours 30 minutes', 2.5);

    c5 := gen_random_uuid();
    INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
    VALUES (c5, uid, m3, 'terminata', now() - interval '5 days' + interval '19 hours',
            now() - interval '5 days' + interval '19 hours 35 minutes', 8.7);

    c6 := gen_random_uuid();
    INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
    VALUES (c6, uid, m1, 'terminata', now() - interval '3 days' + interval '7 hours 45 minutes',
            now() - interval '3 days' + interval '8 hours 10 minutes', 3.0);

    c7 := gen_random_uuid();
    INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at, fine_at, distanza_km)
    VALUES (c7, uid, m2, 'terminata', now() - interval '1 day' + interval '17 hours 30 minutes',
            now() - interval '1 day' + interval '18 hours', 4.3);

    -- 4. Pagamenti per le corse
    INSERT INTO pagamenti (utente_id, corsa_id, importo, stato, importo_pieno)
    VALUES
        (uid, c1, 3.80, 'completato', 3.80),
        (uid, c2, 3.20, 'completato', 3.20),
        (uid, c3, 5.60, 'completato', 5.60),
        (uid, c4, 2.90, 'completato', 2.90),
        (uid, c5, 12.50, 'completato', 12.50),
        (uid, c6, 3.50, 'completato', 3.50),
        (uid, c7, 4.80, 'completato', 4.80);

    -- 5. Offerta/promozione attiva (se non esiste già)
    SELECT id INTO off_id FROM offerte WHERE stato = 'attiva' AND tipo = 'promozione' LIMIT 1;
    IF off_id IS NULL THEN
        off_id := gen_random_uuid();
        INSERT INTO offerte (id, nome, tipo, stato, descrizione, sconto_percentuale, data_inizio, data_scadenza)
        VALUES (off_id, 'Promo Estate 2026', 'promozione', 'attiva',
                'Sconto 20% su tutti i monopattini', 20.00, now(), now() + interval '30 days');
    END IF;

    RAISE NOTICE 'Seed completato per utente % — 7 corse, 7 pagamenti', uid;
END $$;
