-- 020_anonimizza_account.sql — IIN-2 / GDPR art. 17 (Diritto all'oblio)
--
-- Abilita l'ANONIMIZZAZIONE dei dati storici alla cancellazione dell'account.
-- Le tabelle puramente personali (metodi_pagamento, prenotazioni, abbonamenti_utente,
-- notifiche, suggerimenti) restano in ON DELETE CASCADE e vengono eliminate.
-- I dati da conservare per i report aggregati dell'AP e per i contenuti
-- (corse, pagamenti, segnalazioni, recensioni) vengono invece SCOLLEGATI
-- dall'identità impostando utente_id = NULL prima della cancellazione.
--
-- Questa migrazione si limita a rendere nullable la colonna utente_id su quelle
-- tabelle. La FK su corse/pagamenti resta ON DELETE RESTRICT: il backend annulla
-- esplicitamente i riferimenti (ServizioUtenti.cancella_account → anonimizza_dati_utente)
-- prima di eliminare la riga utenti, così il RESTRICT è soddisfatto.
-- segnalazioni e recensioni non hanno FK verso utenti: l'anonimizzazione le rende
-- conformi all'art. 17 evitando dati personali orfani riconducibili all'utente.

ALTER TABLE corse        ALTER COLUMN utente_id DROP NOT NULL;
ALTER TABLE pagamenti    ALTER COLUMN utente_id DROP NOT NULL;
ALTER TABLE segnalazioni ALTER COLUMN utente_id DROP NOT NULL;
ALTER TABLE recensioni   ALTER COLUMN utente_id DROP NOT NULL;
