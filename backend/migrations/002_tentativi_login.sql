-- 002_tentativi_login.sql — IIN-2 lockout dopo 5 tentativi falliti
CREATE TABLE IF NOT EXISTS tentativi_login (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email        TEXT NOT NULL,
  tentativo_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  riuscito     BOOLEAN NOT NULL
);

CREATE INDEX IF NOT EXISTS tentativi_login_email_idx
  ON tentativi_login (email, tentativo_at);
