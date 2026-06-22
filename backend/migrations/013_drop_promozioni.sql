-- 013_drop_promozioni.sql
-- Rimuove la tabella promozioni, sostituita da offerte (STI) con 004_offerte.sql.
-- Nessuna FK la referenzia e non ha mai contenuto dati in produzione.
DROP TABLE IF EXISTS promozioni;
