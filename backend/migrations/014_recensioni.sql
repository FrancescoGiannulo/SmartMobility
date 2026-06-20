-- [IF-UT.15] Recensioni utenti
CREATE TABLE recensioni (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id       UUID NOT NULL,
    voto            INTEGER NOT NULL CHECK (voto BETWEEN 1 AND 5),
    commento        TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX recensioni_utente_id_idx ON recensioni (utente_id);
CREATE INDEX recensioni_created_at_idx ON recensioni (created_at DESC);
