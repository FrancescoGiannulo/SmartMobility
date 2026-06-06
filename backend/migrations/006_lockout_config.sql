-- 006_lockout_config.sql — IIN-2 finestra di lockout configurabile dall'operatore
-- Sostituisce il valore hardcoded di 15 minuti in attore_repository.py
CREATE TABLE IF NOT EXISTS configurazione_sicurezza (
    id                  SERIAL PRIMARY KEY,
    lockout_window_min  INT NOT NULL DEFAULT 15
        CONSTRAINT lockout_window_min_positivo CHECK (lockout_window_min > 0),
    max_tentativi       INT NOT NULL DEFAULT 5
        CONSTRAINT max_tentativi_positivo CHECK (max_tentativi > 0),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Garantisce un'unica riga (configurazione globale di sistema)
CREATE UNIQUE INDEX IF NOT EXISTS configurazione_sicurezza_singleton
    ON configurazione_sicurezza ((TRUE));

-- Inserisce la riga di default se non esiste
INSERT INTO configurazione_sicurezza (lockout_window_min, max_tentativi)
SELECT 15, 5
WHERE NOT EXISTS (SELECT 1 FROM configurazione_sicurezza);
