# Smart Mobility

Sistema software per il Comune di Zootropolis che integra bike, car e e-scooter sharing in un'unica piattaforma.

---

## Stack tecnologico

| Layer | Tecnologia |
|---|---|
| Frontend | React 19 + Vite + TypeScript |
| Backend | FastAPI (Python) |
| Database | Supabase (PostgreSQL) |

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
# Apri .env e inserisci le credenziali Supabase:
#   SUPABASE_URL      → Settings → API → Project URL
#   SUPABASE_KEY      → Settings → API → service_role secret key
#   SUPABASE_JWT_SECRET → Settings → API → JWT Settings → JWT Secret
#   DATABASE_URL      → Settings → Database → Transaction Pooler → URI
#                       (formato: postgresql://postgres.<ref>:<password>@aws-0-*.pooler.supabase.com:6543/postgres)

# 4. Frontend — installa dipendenze Node
cd ../frontend
npm install

# 5. Configura le variabili d'ambiente del frontend
cp .env.example .env.local
# Apri .env.local e inserisci le credenziali Supabase
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
| **Frontend** | `https://smart-mobility-git-main-francesco-giannulo-s-projects.vercel.app` |
| **Backend API** | `https://smartmobility-backend.onrender.com` |
| **API Docs** | `https://smartmobility-backend.onrender.com/docs` |

> Il piano free di Render ha un cold start di ~60 secondi dopo periodi di inattività. Il frontend su Vercel è sempre istantaneo.

Ogni push su `main` aggiorna automaticamente sia frontend che backend. Per la guida completa al deploy: [Deploy.md](Deploy.md).

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
| [SprintZero.md](SprintZero.md) | Product Backlog, architettura, glossario, mockup UI |
| [Sprint1_definitivo.md](Sprint1_definitivo.md) | Sprint 1 — backlog, casi d'uso, note implementazione |
| [Deploy.md](Deploy.md) | Guida completa al deploy su Vercel e Render |
| [GitWorkflow.md](GitWorkflow.md) | Flusso di lavoro Git per il team |
