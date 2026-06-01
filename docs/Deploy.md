# Deploy — Smart Mobility

Guida completa per il deploy dell'applicazione in produzione su Vercel (frontend) e Render (backend).

---

## Architettura di produzione

```
Browser / Mobile
       │
       ▼
  Vercel (Frontend)
  https://smart-mobility-git-main-francesco-giannulo-s-projects.vercel.app
       │  VITE_API_URL
       ▼
  Render (Backend FastAPI)
  https://smartmobility-backend.onrender.com
       │
       ▼
  Supabase (PostgreSQL + Auth)
  https://whglmerfzddcatyblfgf.supabase.co
```

---

## URL di produzione

| Servizio | URL | Note |
|---|---|---|
| Frontend (stabile) | `https://smart-mobility-git-main-...vercel.app` | Si aggiorna ad ogni push su `main` |
| Frontend (temporaneo) | `https://smart-mobility-9zszmbxjs-...vercel.app` | Legato a un singolo commit — non usarlo |
| Backend | `https://smartmobility-backend.onrender.com` | Cold start ~60s dopo inattività (piano free) |
| API Docs | `https://smartmobility-backend.onrender.com/docs` | Swagger UI — utile per testare endpoint |

---

## Variabili d'ambiente

### Vercel (frontend)

Configurate su Vercel → progetto → Settings → Environment Variables.
Applicare a: **Production** e **Preview** (non Development — in locale si usa `.env.local`).

| Variabile | Valore | Note |
|---|---|---|
| `VITE_SUPABASE_URL` | `https://whglmerfzddcatyblfgf.supabase.co` | |
| `VITE_SUPABASE_ANON_KEY` | `sb_publishable_...` | Chiave pubblica — non la service_role |
| `VITE_GOOGLE_MAPS_API_KEY` | `AIzaSy...` | |
| `VITE_API_URL` | `https://smartmobility-backend.onrender.com` | Senza trailing slash — critico |

### Render (backend)

Configurate su Render → servizio → Environment.

| Variabile | Valore | Note |
|---|---|---|
| `SUPABASE_URL` | `https://whglmerfzddcatyblfgf.supabase.co` | |
| `SUPABASE_KEY` | `<service_role key>` | Chiave segreta — mai nel frontend |
| `SUPABASE_JWT_SECRET` | `<jwt secret>` | Da Supabase → Settings → API → JWT |
| `DATABASE_URL` | `postgresql://postgres...` | Transaction Pooler URI |
| `FRONTEND_URL` | `https://smart-mobility-git-main-...vercel.app` | Senza trailing slash — critico per CORS |

> **CORS critico:** `FRONTEND_URL` deve corrispondere esattamente all'`Origin` che il browser manda. Un trailing slash in più o una lettera sbagliata causa `400 Disallowed CORS origin`. Per consentire più origin separare con virgola: `https://url1.vercel.app,https://url2.vercel.app`.

---

## Come funziona il deploy automatico

### Frontend (Vercel)
Ogni push su `main` trigge un build automatico su Vercel. Il processo dura circa 30-60 secondi. Visibile su Vercel → Deployments.

```
git push origin main
        │
        ▼
Vercel rileva il push
        │
        ▼
npm install → tsc -b && vite build
        │
        ▼
Deploy su CDN globale (~30s)
        │
        ▼
URL aggiornato automaticamente
```

### Backend (Render)
Stesso meccanismo: push su `main` trigge il build su Render. Il processo dura 2-3 minuti (install + build Python).

```
git push origin main
        │
        ▼
Render rileva il push
        │
        ▼
pip install uv && uv sync
        │
        ▼
.venv/bin/uvicorn main:app --host 0.0.0.0 --port $PORT
        │
        ▼
Servizio disponibile (~2-3 min)
```

---

## Testing su mobile (rete locale)

Per testare l'app da mobile **senza** passare per il deploy:

```bash
# Avvia backend
cd backend && uv run uvicorn main:app --reload --port 8000

# Avvia frontend (host: true espone su tutta la rete locale)
cd frontend && npm run dev
```

Vite stampa l'IP della macchina:
```
  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/    ← apri questo dal mobile
```

Il proxy Vite gira sul PC — le chiamate `/api/...` vengono inoltrate automaticamente a `localhost:8000`. Non serve configurare nulla sul telefono.

> **Limitazione:** Google OAuth non funziona in locale da mobile perché l'IP locale (`192.168.x.x`) non è registrato come redirect URI su Supabase/Google. Per testare OAuth usare l'URL Vercel di produzione.

---

## Configurazione Supabase per OAuth

Per il login con Google in produzione, configurare su **Supabase → Authentication → URL Configuration**:

| Campo | Valore |
|---|---|
| Site URL | `https://smart-mobility-git-main-...vercel.app` |
| Redirect URLs | `https://smart-mobility-git-main-...vercel.app/**` |

> **Stato attuale:** il login con Google reindirizza ancora a `localhost` dopo la selezione account — issue aperta, da investigare (possibile configurazione mancante su Google Cloud Console → OAuth → Authorized redirect URIs).

---

## Configurazione Vercel (vercel.json)

Il file `vercel.json` nella root del repo configura:
- **buildCommand** / **installCommand**: comandi per buildare il frontend
- **outputDirectory**: dove Vite mette il bundle (`frontend/dist` relativo alla root, o `dist` relativo a `frontend/`)
- **rewrites**: redirige tutte le route a `index.html` — necessario per React Router (SPA)
- **rootDirectory**: NON va nel file — va impostato nell'UI di Vercel su `frontend`

> **Nota:** il campo `rootDirectory` non è supportato in `vercel.json` — genera errore `should NOT have additional property`. Impostarlo solo dall'interfaccia Vercel al momento del setup.

---

## Configurazione Render

Il file `render.yaml` nella root configura il servizio backend:

```yaml
services:
  - type: web
    name: smartmobility-backend
    runtime: python
    rootDir: backend
    buildCommand: pip install uv && uv sync
    startCommand: .venv/bin/uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars: [...]
```

> **Nota:** usare `.venv/bin/uvicorn` invece di `uv run uvicorn` — Render non rileva la porta quando uvicorn parte come subprocess di `uv run`.

---

## Diagnosi problemi comuni

### CORS: `No 'Access-Control-Allow-Origin' header`

1. Verificare `FRONTEND_URL` su Render — deve corrispondere **esattamente** all'origin del browser (niente trailing slash)
2. Testare il preflight direttamente:
```bash
curl -v -X OPTIONS \
  -H "Origin: https://il-tuo-url.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  https://smartmobility-backend.onrender.com/auth/login
```
3. Se la risposta è `400 Disallowed CORS origin` → valore `FRONTEND_URL` sbagliato
4. Se la risposta è `200` con header `access-control-allow-origin` → CORS OK, problema altrove

### Backend non risponde (ERR_CONNECTION_REFUSED o timeout)

- Piano free Render: cold start di ~60 secondi dopo 15 minuti di inattività. Aspettare e riprovare.
- Verificare i log su Render → Logs. Cercare `Application startup complete`.

### Frontend builda ma le API non funzionano

- Verificare che `VITE_API_URL` sia impostato su Vercel senza trailing slash
- Aprire DevTools → Network e controllare l'URL delle richieste XHR
- In locale senza `VITE_API_URL`, le chiamate vanno a `/api` (proxy Vite) — in produzione devono andare all'URL Render

### Vercel build fallisce con errori TypeScript

- Eseguire `npm run build` in locale prima di fare push — la build Vercel usa lo stesso comando
- Gli errori TS bloccano la build (non sono warning): vanno fixati prima del merge su `main`

---

## Costi (aggiornati maggio 2026)

| Servizio | Piano | Costo | Limiti |
|---|---|---|---|
| Vercel | Hobby | Gratis | 100GB banda/mese, uso non commerciale |
| Render | Free | Gratis | Cold start 60s, 750h istanza/mese |
| Supabase | Free | Gratis | 500MB DB, 50.000 auth users |

Per eliminare il cold start di Render: piano **Hobby a $7/mese** (always-on).
