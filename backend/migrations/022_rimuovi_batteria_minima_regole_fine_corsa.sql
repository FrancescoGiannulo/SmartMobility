-- [IF-OP.06] Rimuove la soglia "batteria minima" configurabile dall'Operatore nelle regole di
-- fine corsa: la transizione "In manutenzione" per batteria scarica resta attiva ma usa una
-- soglia fissa lato applicazione (ServizioMobilita.BATTERIA_MINIMA_MANUTENZIONE), non più
-- configurabile a runtime.
ALTER TABLE regole_fine_corsa DROP CONSTRAINT IF EXISTS batteria_minima_check;
ALTER TABLE regole_fine_corsa DROP COLUMN IF EXISTS batteria_minima;
