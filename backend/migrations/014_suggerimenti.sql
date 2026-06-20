-- [IF-UT.14] Suggerimenti Intelligenti

CREATE TYPE tipo_suggerimento AS ENUM (
    'risparmio',
    'percorso',
    'abbonamento',
    'orario',
    'mezzo',
    'generale'
);

CREATE TYPE stato_suggerimento AS ENUM (
    'nuovo',
    'visto'
);

CREATE TABLE suggerimenti (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id   UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
    tipo        tipo_suggerimento NOT NULL DEFAULT 'generale',
    testo       TEXT NOT NULL,
    dati_contesto JSONB DEFAULT '{}',
    stato       stato_suggerimento NOT NULL DEFAULT 'nuovo',
    creato_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_suggerimenti_utente ON suggerimenti(utente_id);
