-- ============================================================
-- 006_parametri_sistema.sql — CS-15 Configura Parametri Numerici di Sistema
-- IF-OP.08, IF-OP.09, IF-OP.10, IF-OP.14
-- Tabella singleton (una sola riga con id = 1)
-- ============================================================

CREATE TABLE parametri_sistema (
    id                          INTEGER PRIMARY KEY DEFAULT 1,
    durata_max_prenotazione_min INTEGER NOT NULL DEFAULT 15
        CONSTRAINT durata_max_prenotazione_non_negativa CHECK (durata_max_prenotazione_min >= 0),
    durata_periodo_grazia_min   INTEGER NOT NULL DEFAULT 5
        CONSTRAINT durata_grazia_non_negativa CHECK (durata_periodo_grazia_min >= 0),
    max_mezzi_per_utente        INTEGER NOT NULL DEFAULT 1
        CONSTRAINT max_mezzi_positivo CHECK (max_mezzi_per_utente >= 1),
    addebito_pausa_min          NUMERIC(10, 4) NOT NULL DEFAULT 0.0000
        CONSTRAINT addebito_non_negativo CHECK (addebito_pausa_min >= 0),
    CONSTRAINT singleton CHECK (id = 1)
);

-- Riga di default: il sistema parte sempre con valori configurati
INSERT INTO parametri_sistema (id, durata_max_prenotazione_min, durata_periodo_grazia_min, max_mezzi_per_utente, addebito_pausa_min)
VALUES (1, 15, 5, 1, 0.0000)
ON CONFLICT DO NOTHING;
