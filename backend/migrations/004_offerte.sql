DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_offerta') THEN
    CREATE TYPE tipo_offerta AS ENUM ('promozione', 'abbonamento');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'stato_offerta') THEN
    CREATE TYPE stato_offerta AS ENUM ('bozza', 'attiva', 'scaduta');
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS offerte (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome            TEXT NOT NULL,
    tipo            tipo_offerta NOT NULL,
    stato           stato_offerta NOT NULL DEFAULT 'attiva',
    descrizione     TEXT,
    sconto_percentuale NUMERIC(5,2),
    prezzo          NUMERIC(10,2),
    durata_giorni   INTEGER,
    data_inizio     TIMESTAMPTZ,
    data_scadenza   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT offerte_nome_unico UNIQUE (nome),
    CONSTRAINT sconto_valido CHECK (sconto_percentuale IS NULL OR (sconto_percentuale > 0 AND sconto_percentuale <= 100)),
    CONSTRAINT prezzo_valido CHECK (prezzo IS NULL OR prezzo > 0),
    CONSTRAINT durata_valida CHECK (durata_giorni IS NULL OR durata_giorni > 0)
);
