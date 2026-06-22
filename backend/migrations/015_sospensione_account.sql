-- 015_sospensione_account.sql — IF-OP.09 Sospende Account Utente
ALTER TABLE utenti ADD COLUMN IF NOT EXISTS motivazione_sospensione TEXT;
ALTER TABLE utenti ADD COLUMN IF NOT EXISTS sospeso_at TIMESTAMPTZ;

CREATE TABLE IF NOT EXISTS notifiche (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utente_id   UUID NOT NULL REFERENCES utenti(id) ON DELETE CASCADE,
  messaggio   TEXT NOT NULL,
  letta       BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS notifiche_utente_idx ON notifiche (utente_id, created_at);
