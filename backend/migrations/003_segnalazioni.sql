-- [IF-UT.15 / IF-OP.08] Segnalazioni utenti
CREATE TYPE stato_segnalazione AS ENUM ('aperta', 'in_carico');

CREATE TABLE segnalazioni (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id       UUID NOT NULL,
    tipologia       TEXT NOT NULL,
    descrizione     TEXT NOT NULL,
    stato           stato_segnalazione NOT NULL DEFAULT 'aperta',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX segnalazioni_stato_idx ON segnalazioni (stato);
CREATE INDEX segnalazioni_created_at_idx ON segnalazioni (created_at DESC);
