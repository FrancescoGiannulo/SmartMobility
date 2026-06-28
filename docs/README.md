# Smart Mobility

Sistema software per il Comune di Zootropolis che integra bike, car e e-scooter sharing in un'unica piattaforma.

---

## Stack tecnologico

| Layer | Tecnologia |
|---|---|
| Frontend | React 19 + Vite + TypeScript |
| Backend | FastAPI (Python) |
| Database | Supabase (PostgreSQL + PostGIS) |
| ORM | SQLAlchemy 2.0 + GeoAlchemy2 |
| Auth | Supabase Auth + PyJWT |
| Mappe | Google Maps (`@vis.gl/react-google-maps`) |
| AI | Groq + Llama 3.3 (suggerimenti intelligenti) |
| HTTP Client (FE) | Axios + TanStack Query |
| Routing (FE) | React Router DOM |
| Gestore dipendenze Python | uv |

---

## Prerequisiti

### macOS / Linux

**Node.js** (include npm):
```bash
# Con Homebrew
brew install node

# Oppure scarica da https://nodejs.org
```

**uv** (gestore Python + ambienti virtuali):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Riavvia il terminale dopo l'installazione di `uv`.

---

### Windows

**Node.js** (include npm):

Verifica se è già installato:
```powershell
node --version
npm --version
```

Se i comandi non vengono riconosciuti, scarica e installa da [nodejs.org](https://nodejs.org) (versione LTS).

**uv**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Riavvia il terminale dopo l'installazione di `uv`.

---

## Setup iniziale (solo al primo clone)

```bash
# 1. Clona il repository
git clone https://github.com/FrancescoGiannulo/SmartMobility.git
cd SmartMobility

# 2. Backend — installa dipendenze Python
cd backend
uv sync

# 3. Configura le variabili d'ambiente del backend
cp .env.example .env
# Apri .env e compila i valori:
#   SUPABASE_URL        → Settings → API → Project URL
#   SUPABASE_KEY        → Settings → API → service_role secret key
#   SUPABASE_JWT_SECRET → Settings → API → JWT Settings → JWT Secret
#   DATABASE_URL        → Settings → Database → Transaction Pooler → URI
#                         (formato: postgresql://postgres.<ref>:<password>@aws-0-*.pooler.supabase.com:6543/postgres)
#   DEMO_ACCOUNT_EMAIL  → email dell'account demo (opzionale, abilita il movimento simulato)
#   GROQ_API_KEY        → opzionale, abilita i suggerimenti AI (groq.com)

# 4. Frontend — installa dipendenze Node
cd ../frontend
npm install

# 5. Configura le variabili d'ambiente del frontend
cp .env.example .env.local
# Apri .env.local e compila i valori:
#   VITE_SUPABASE_URL      → Settings → API → Project URL
#   VITE_SUPABASE_ANON_KEY → Settings → API → anon/public key
#   VITE_GOOGLE_MAPS_API_KEY → Google Cloud Console → Maps JavaScript API
#   VITE_DEMO_EMAIL        → stessa email di DEMO_ACCOUNT_EMAIL (opzionale)
```

Le credenziali Supabase si trovano su [supabase.com](https://supabase.com) → progetto → Settings → API.

---

## Avvio

Apri due terminali separati:

**Terminale 1 — Backend:**
```bash
cd backend
uv run uvicorn main:app --reload
```
API disponibile su [http://localhost:8000](http://localhost:8000)
Documentazione interattiva su [http://localhost:8000/docs](http://localhost:8000/docs)

**Terminale 2 — Frontend:**
```bash
cd frontend
npm run dev
```
App disponibile su [http://localhost:5173](http://localhost:5173)

---

## Aggiornare le dipendenze

Quando un collega aggiunge nuove dipendenze Python o npm, esegui:

```bash
# Backend
cd backend && uv sync

# Frontend
cd frontend && npm install
```

---

## Struttura del progetto

```
SmartMobility/
├── backend/
│   ├── controllers/     # validazione HTTP e routing
│   ├── bll/             # logica applicativa (Business Logic Layer)
│   ├── dal/             # accesso ai dati (repository)
│   ├── model/           # entità di dominio
│   ├── main.py          # entrypoint FastAPI
│   ├── pyproject.toml   # dipendenze Python
│   └── .env.example     # template variabili d'ambiente
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env.example     # template variabili d'ambiente
└── docs/                # documentazione di progetto
```

---

## Ambiente di produzione

L'applicazione è deployata e accessibile senza avviare nulla in locale:

| Servizio | URL |
|---|---|
| **Frontend** | https://smart-mobility-git-main-francesco-giannulo-s-projects.vercel.app |
| **Backend API** | `https://smartmobility-backend.onrender.com` |
| **API Docs** | `https://smartmobility-backend.onrender.com/docs` |

> Il piano free di Render ha un cold start di ~60 secondi dopo periodi di inattività. Il frontend su Vercel è sempre istantaneo.

Ogni push su `main` aggiorna automaticamente sia frontend che backend. Per la guida completa al deploy: [Deploy.md](Deploy.md).

### Come usarlo

1. Apri [smart-mobility-git-main-francesco-giannulo-s-projects.vercel.app](https://smart-mobility-git-main-francesco-giannulo-s-projects.vercel.app)
2. Registrati con email e password, oppure accedi con uno dei tre account predefiniti:

| Ruolo | Email | Password |
|---|---|---|
| Utente (demo) | `demo@smartmobility.it` | `DemoEsame2026!` |
| Operatore | `operatore@smartmobility.test` | `Operatore123!` |
| Amministrazione Pubblica | `admin@smartmobility.test` | `Admin123!` |

3. Da **Utente**: esplora la mappa, prenota un mezzo, avvia una corsa e usa il pulsante **"Avvia demo movimento"** per simulare lo spostamento sulla mappa.
4. Da **Operatore**: monitora la flotta in tempo reale sulla mappa, gestisci mezzi, tariffe, zone e segnalazioni.
5. Da **Amministrazione Pubblica**: visualizza la dashboard con heatmap degli utilizzi ed esporta report CSV.

---

## Testing su mobile (rete locale)

Per testare da smartphone sulla stessa rete Wi-Fi, avvia i server localmente:

```bash
# Terminale 1 — Backend
cd backend && uv run uvicorn main:app --reload

# Terminale 2 — Frontend
cd frontend && npm run dev
```

Vite mostra l'IP della macchina nella riga `Network:` — aprilo dal browser del telefono. Il proxy Vite gestisce automaticamente le chiamate API senza configurazioni aggiuntive.

> Per testare il login con Google usare l'URL Vercel di produzione, non l'IP locale.

---

## Documentazione

| Documento | Contenuto |
|---|---|
| [Sprintn3.md](Sprintn3.md) | Product Backlog completo, Sprint 1-3, casi d'uso, diagrammi, note implementazione |
| [Deploy.md](Deploy.md) | Guida completa al deploy su Vercel e Render |
| [GitWorkflow.md](GitWorkflow.md) | Flusso di lavoro Git per il team |
| [pattern.md](pattern.md) | Pattern architetturali adottati |
