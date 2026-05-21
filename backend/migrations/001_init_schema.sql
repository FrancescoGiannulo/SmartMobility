-- ============================================================
-- 001_init_schema.sql — Smart Mobility Sprint 1
-- Eseguire su Supabase SQL Editor (o psql)
-- ============================================================

-- 1. Estensione PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- ============================================================
-- 2. Enum Types
-- ============================================================

CREATE TYPE tipo_mezzo AS ENUM ('monopattino', 'bicicletta', 'automobile');

CREATE TYPE stato_mezzo AS ENUM (
    'Disponibile', 'Prenotato', 'In uso', 'In pausa',
    'In manutenzione', 'Fuori servizio', 'Dismesso'
);

CREATE TYPE tipo_zona AS ENUM ('operativa', 'parcheggio', 'limitata', 'vietata');

CREATE TYPE stato_prenotazione AS ENUM ('attiva', 'scaduta', 'annullata', 'convertita');

CREATE TYPE stato_corsa AS ENUM ('in_uso', 'in_pausa', 'terminata');

CREATE TYPE stato_pagamento AS ENUM ('completato', 'rifiutato', 'in_attesa');

CREATE TYPE tipo_metodo_pagamento AS ENUM ('google_pay', 'apple_pay', 'paypal', 'carta');

CREATE TYPE tipo_vincolo_fine_corsa AS ENUM ('penale', 'divieto', 'avviso');

-- ============================================================
-- 3. Tabelle — Profili Utente (FK → auth.users)
-- ============================================================

CREATE TABLE utenti (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome        TEXT NOT NULL,
    cognome     TEXT NOT NULL,
    telefono    TEXT,
    sospeso     BOOLEAN NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE operatori (
    id                              UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome                            TEXT NOT NULL,
    durata_max_prenotazione_min     INTEGER NOT NULL DEFAULT 15,
    durata_periodo_grazia_min       INTEGER NOT NULL DEFAULT 5,
    max_mezzi_per_utente            INTEGER NOT NULL DEFAULT 1,
    created_at                      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE amministratori (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 4. Flotta
-- ============================================================

CREATE TABLE mezzi (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codice      TEXT NOT NULL UNIQUE,
    tipo        tipo_mezzo NOT NULL,
    stato       stato_mezzo NOT NULL DEFAULT 'Disponibile',
    lat         DOUBLE PRECISION,
    lng         DOUBLE PRECISION,
    batteria    INTEGER CHECK (batteria BETWEEN 0 AND 100),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 5. Zone Geografiche
-- ============================================================

CREATE TABLE zone (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome             TEXT NOT NULL,
    tipo             tipo_zona NOT NULL,
    perimetro        GEOMETRY(POLYGON, 4326) NOT NULL,
    limite_velocita  INTEGER,
    attiva           BOOLEAN NOT NULL DEFAULT true,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indice spaziale obbligatorio per ST_Contains / ST_Intersects
CREATE INDEX zone_perimetro_gist ON zone USING GIST (perimetro);

-- ============================================================
-- 6. Tariffe
-- ============================================================

CREATE TABLE tariffe (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo_mezzo       tipo_mezzo NOT NULL UNIQUE,
    costo_al_minuto  NUMERIC(10, 4) NOT NULL CHECK (costo_al_minuto > 0),
    costo_al_km      NUMERIC(10, 4) NOT NULL CHECK (costo_al_km > 0),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    aggiornata_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 7. Metodi di Pagamento
-- ============================================================

CREATE TABLE metodi_pagamento (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id       UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
    tipo            tipo_metodo_pagamento NOT NULL,
    token_esterno   TEXT NOT NULL,
    last_four       TEXT,
    predefinito     BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Al massimo un metodo predefinito per utente (invariante IF-UT.21)
CREATE UNIQUE INDEX metodi_pagamento_predefinito_unico
    ON metodi_pagamento (utente_id)
    WHERE predefinito = true;

-- ============================================================
-- 8. Prenotazioni
-- ============================================================

CREATE TABLE prenotazioni (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id   UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
    mezzo_id    UUID NOT NULL REFERENCES mezzi(id) ON DELETE RESTRICT,
    stato       stato_prenotazione NOT NULL DEFAULT 'attiva',
    scade_at    TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 9. Regole Fine Corsa
-- ============================================================

CREATE TABLE regole_fine_corsa (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    zona_parcheggio_id  UUID NOT NULL REFERENCES zone(id) ON DELETE CASCADE,
    batteria_minima     INTEGER CHECK (batteria_minima BETWEEN 0 AND 100),
    penale_fuori_zona   NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    tipo_vincolo        tipo_vincolo_fine_corsa NOT NULL DEFAULT 'avviso',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 10. Corse
-- ============================================================

CREATE TABLE corse (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utente_id        UUID NOT NULL REFERENCES utenti(id) ON DELETE RESTRICT,
    mezzo_id         UUID NOT NULL REFERENCES mezzi(id) ON DELETE RESTRICT,
    prenotazione_id  UUID REFERENCES prenotazioni(id) ON DELETE SET NULL,
    stato            stato_corsa NOT NULL DEFAULT 'in_uso',
    inizio_at        TIMESTAMPTZ NOT NULL,
    fine_at          TIMESTAMPTZ,
    distanza_km      NUMERIC(10, 3),
    inizio_lat       DOUBLE PRECISION,
    inizio_lng       DOUBLE PRECISION,
    fine_lat         DOUBLE PRECISION,
    fine_lng         DOUBLE PRECISION,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 11. Pagamenti
-- ============================================================

CREATE TABLE pagamenti (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    corsa_id              UUID NOT NULL REFERENCES corse(id) ON DELETE RESTRICT,
    utente_id             UUID NOT NULL REFERENCES utenti(id) ON DELETE RESTRICT,
    metodo_pagamento_id   UUID REFERENCES metodi_pagamento(id) ON DELETE SET NULL,
    importo               NUMERIC(10, 2) NOT NULL CHECK (importo >= 0),
    stato                 stato_pagamento NOT NULL DEFAULT 'in_attesa',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);
