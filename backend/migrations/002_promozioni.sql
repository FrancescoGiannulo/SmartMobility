-- [IF-UT.13] Tabella promozioni — Sprint 1
CREATE TABLE promozioni (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titolo              TEXT NOT NULL,
    descrizione         TEXT,
    sconto_percentuale  NUMERIC(5,2) NOT NULL
                            CONSTRAINT promozione_sconto_valido CHECK (sconto_percentuale > 0 AND sconto_percentuale <= 100),
    data_inizio         TIMESTAMPTZ NOT NULL DEFAULT now(),
    data_fine           TIMESTAMPTZ NOT NULL,
    attiva              BOOLEAN NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT promozione_date_valide CHECK (data_fine > data_inizio)
);
