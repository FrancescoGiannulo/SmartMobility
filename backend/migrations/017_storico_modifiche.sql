-- 017_storico_modifiche.sql — IF-OP.12 Mostra Storico Modifiche
CREATE TABLE IF NOT EXISTS storico_modifiche (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tipo_configurazione   TEXT NOT NULL,
  descrizione           TEXT NOT NULL,
  valore_precedente     TEXT,
  valore_nuovo          TEXT,
  operatore_id          UUID NOT NULL,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS storico_modifiche_created_at_idx ON storico_modifiche (created_at DESC);
