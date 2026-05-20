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
# Apri .env e inserisci le credenziali Supabase

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

## Documentazione

| Documento | Contenuto |
|---|---|
| [SprintZero.md](SprintZero.md) | Product Backlog, architettura, glossario, mockup UI |
| [SprintUno.md](SprintUno.md) | Sprint 1 — backlog, casi d'uso, note implementazione |
