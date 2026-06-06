# CLAUDE.md — Smart Mobility

## Contesto del progetto

**Smart Mobility** è un sistema software per il Comune di Zootropolis che integra servizi di bike, car e e-scooter sharing in un'unica piattaforma.

Documenti di riferimento:
- [`docs/SprintZero.md`](docs/SprintZero.md) — architettura, glossario, mockup UI
- [`docs/Sprint1_definitivo.md`](docs/Sprint1_definitivo.md) — Sprint 1 Backlog, casi d'uso, mockup UI (**documento primario per Sprint 1** — sostituisce SprintUno.md)
- [`docs/Deploy.md`](docs/Deploy.md) — guida completa al deploy su Vercel + Render, variabili d'ambiente, diagnosi problemi

Tre ruoli utente distinti:
- **UT** — Utente finale (cittadino)
- **OP** — Operatore del Servizio (gestione flotta)
- **AP** — Amministrazione Pubblica (governance e report)

---

## Stack Tecnologico

| Layer | Tecnologia | Note |
|---|---|---|
| Frontend | React 19 + Vite + TypeScript | `frontend/` — SPA, no SSR |
| Backend | FastAPI (Python) | `backend/` — REST API |
| Database | Supabase (PostgreSQL) | Hosted, con Row Level Security |
| ORM | SQLAlchemy 2.0 | Accesso DB solo dal DAL |
| PostGIS | GeoAlchemy2 | Geometrie geografiche (zone, posizioni mezzi) |
| Driver DB | psycopg2-binary | Connessione PostgreSQL |
| Auth | Supabase Auth + PyJWT | Token JWT, blocco dopo 5 tentativi (IIN-2) |
| HTTP Client (FE) | Axios + TanStack Query | Chiamate API e cache lato client |
| Routing (FE) | React Router DOM | Navigazione SPA |
| Gestore dipendenze Python | uv | Sostituisce pip+venv; gestisce `.venv` automaticamente |

### Chiavi Supabase
- **Publishable key** (`anon`) → usata nel frontend React (`frontend/.env.local`)
- **Secret key** (`service_role`) → usata solo nel backend FastAPI (`backend/.env`) — mai esposta al client

### Workaround SSL rete universitaria
Alcuni membri del team lavorano su rete universitaria con SSL inspection che rifiuta il certificato CA di Supabase. Il workaround è già in `backend/middleware/auth_middleware.py`: il `PyJWKClient` (usato solo per token ES256) viene inizializzato con un `ssl_context` che disabilita `check_hostname` e `verify_mode`. **Non rimuovere questo workaround.** La verifica crittografica del JWT tramite PyJWT rimane attiva — viene saltato solo il chain check del certificato TLS per il JWKS endpoint. Assicurarsi che questo blocco sia presente ad ogni modifica di `auth_middleware.py`.

### Ambiente di produzione (deployato)

| Servizio | URL | Piattaforma |
|---|---|---|
| Frontend | `https://smart-mobility-git-main-francesco-giannulo-s-projects.vercel.app` | Vercel (Hobby, gratis) |
| Backend | `https://smartmobility-backend.onrender.com` | Render (Free, cold start ~60s) |

Push su `main` → deploy automatico su entrambe le piattaforme.

#### Variabili d'ambiente di produzione
- **Vercel**: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_GOOGLE_MAPS_API_KEY`, `VITE_API_URL`
- **Render**: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_JWT_SECRET`, `DATABASE_URL`, `FRONTEND_URL`

#### Problemi noti e pattern ricorrenti

**CORS (errore più frequente in produzione):**
- Sintomo: `No 'Access-Control-Allow-Origin' header` / `400 Disallowed CORS origin` nei log Render
- Causa quasi sempre: `FRONTEND_URL` su Render non matcha esattamente l'`Origin` del browser (trailing slash, http vs https, URL sbagliato)
- Diagnosi: `curl -v -X OPTIONS -H "Origin: <url-vercel>" -H "Access-Control-Request-Method: POST" https://smartmobility-backend.onrender.com/auth/login`
- Fix: correggere il valore di `FRONTEND_URL` su Render (senza trailing slash). Supporta lista CSV: `url1,url2`
- Il codice in `backend/main.py` splitta `FRONTEND_URL` per virgola — non aggiungere spazi

**Build Vercel che fallisce:**
- Causa: errori TypeScript bloccano `tsc -b && vite build`
- Diagnosi: eseguire `npm run build` in locale — stesso comando usato da Vercel
- Non fare push su `main` con build rotta — il deploy va in errore

**Backend non risponde:**
- Piano free Render: cold start di 60s dopo 15 min di inattività. Non è un bug — aspettare
- Verificare i log su Render → Logs per `Application startup complete`

**Google OAuth → reindirizza a localhost:**
- Configurare **Site URL** su Supabase → Authentication → URL Configuration con l'URL Vercel
- I Redirect URLs devono includere `https://<url-vercel>/**`
- Stato attuale (maggio 2026): OAuth con Google non completamente funzionante in produzione — issue aperta

**Avvio locale da mobile (stessa rete Wi-Fi):**
- Vite espone su `0.0.0.0` grazie a `host: true` in `vite.config.ts`
- Il proxy `/api` → `localhost:8000` è attivo solo in modalità `serve` (dev), non nella build produzione
- `ApiService.ts` usa `/api` come base URL di default in locale, `VITE_API_URL` in produzione

**SSL rete universitaria:**
- Un membro del team (SuperExcalibur10) aveva aggiunto un workaround SSL globale in `config.py` che disabilitava la verifica del certificato per tutto il processo Python — pericoloso, già revertito 3 volte
- Il workaround legittimo per PyJWKClient è in `backend/middleware/auth_middleware.py` — non rimuoverlo
- Se si vedono errori SSL dal backend verso Supabase su rete universitaria: usare hotspot mobile o VPN, non riattivare il workaround globale in `config.py`

### Avvio locale

```bash
# Backend (dalla root)
cd backend && uv run uvicorn main:app --reload
# → http://localhost:8000/docs

# Frontend (dalla root)
cd frontend && npm run dev
# → http://localhost:5173 (locale) / http://<IP>:5174 (mobile sulla stessa rete)
```

### Variabili d'ambiente

`backend/.env` (non committato — copiare da `.env.example`):
```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=<secret key>
DATABASE_URL=postgresql://postgres:<password>@db.xxxx.supabase.co:5432/postgres
```

`frontend/.env.local` (non committato — copiare da `.env.example`):
```
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=<publishable key>
```

### Struttura del progetto

```
frontend/src/
├── views/
│   ├── utente/           → VistaUtente (IF-UT.*)
│   ├── operatore/        → VistaOperatore (IF-OP.*)
│   └── amministrazione/  → VistaAmministrazionePubblica (IF-AP.*)
└── services/
    ├── ApiService.ts         → gateway HTTP centrale + interceptor JWT
    ├── AuthService.ts        → login, registrazione [IF-UT.17, IF-UT.18]
    ├── MapService.ts         → mezzi e zone [IF-UT.01, IF-AP.08, IF-OP.01]
    ├── PaymentService.ts     → metodi di pagamento, tariffe, promozioni [IF-UT.12, IF-UT.21]
    ├── CorsaService.ts       → sblocco, termina, storico [IF-UT.04, IF-UT.06, IF-UT.14]
    ├── PrenotazioneService.ts → prenotazioni [IF-UT.02]
    ├── AbbonamentoService.ts → abbonamenti [IF-UT.16]
    ├── ZonaService.ts        → CRUD zone [IF-AP.02, IF-AP.03, IF-OP.03]
    └── FlottaService.ts      → gestione flotta [IF-OP.04, IF-OP.12, IF-OP.13]

backend/
├── database.py       → engine SQLAlchemy, SessionLocal, Base (DeclarativeBase), get_db()
├── migrations/       → file SQL da eseguire su Supabase (001…011)
├── model/            → ORM SQLAlchemy 2.0 (Mapped + mapped_column); importare Base da database.py
├── controllers/      → validazione HTTP (8 controller da SprintUno.md §7.3)
├── bll/              → logica applicativa (6 servizi)
├── dal/              → repository (6, uno per entità)
└── tests/            → test pytest; conftest.py imposta DATABASE_URL dummy per unit test
```

### Git workflow

- Branch per feature: `feature/auth`, `feature/corsa`, `feature/pagamenti`, `feature/mappa-zone`, `feature/db-schema`
- Nessun commit diretto su `main` — ogni item passa da PR con review
- Un item del backlog = un PR
- Vedere `docs/GitWorkflow.md` per il tutorial completo

### Test backend

```bash
# Unit test (nessun DB richiesto)
cd backend && uv run pytest tests/ -v -m "not integration"

# Test di integrazione (richiede DATABASE_URL in backend/.env)
cd backend && uv run pytest tests/ -v -m integration

# Installa dipendenze dev prima di eseguire i test
cd backend && uv sync --extra dev
```

---

## Metodologia: Agile con Sprint

Lo sviluppo segue il paradigma **Agile Software Engineering** basato su sprint. Ogni decisione di codifica deve essere motivata da un item del Product Backlog.

### Regole fondamentali degli sprint

1. **Sprint 0** — Solo architettura e documentazione. Nessun codice applicativo.
2. **Sprint N (N ≥ 1)** — Ogni sprint deve produrre **codice funzionante** che implementa un sottoinsieme degli item del Product Backlog.
3. Ogni item implementato deve essere **tracciabile** al suo ID (`IF-UT.xx`, `IF-AP.xx`, `IF-OP.xx`).
4. Prima di scrivere codice per un item, verificare che esista la **specifica del caso d'uso** corrispondente nel documento di sprint.
5. Ogni sprint aggiorna la documentazione in `docs/`.

### Flusso per ogni item

```
User Story (SprintZero.md)
  → Caso d'uso (scenario base + alternativi)
    → Diagramma di sequenza
      → Implementazione
        → Test
          → Aggiornamento documentazione sprint
```

---

## Architettura

Il sistema segue il pattern **Client-Server + MVC** su più livelli. Rispetta sempre questa separazione — non mescolare responsabilità tra i layer.

```
Client
├── View (VistaUtente | VistaOperatore | VistaAmministrazionePubblica)
└── API Service Layer (ApiService, AuthService, MapService, PaymentService, ZonaService, FlottaService)

Server
├── Controller Layer
├── Business Logic Layer (BLL)
├── Model
└── Data Access Layer (DAL) → DBMS

Servizi Esterni
├── BingMaps (geolocalizzazione)
└── ProviderPagamenti (gateway pagamenti)
```

### Vincoli architetturali obbligatori

- **Controller**: solo validazione HTTP e smistamento. Zero logica di business.
- **BLL**: tutta la logica applicativa. Nessun accesso diretto al DB.
- **DAL**: solo accesso ai dati. Nessuna logica di business.
- **View/ApiService**: nessuna logica di business lato client.
- **model/**: ORM SQLAlchemy 2.0 puri — nessuna logica, nessun Pydantic. I `CheckConstraint` vanno in `__table_args__`, non come argomenti di `mapped_column`. Usare `create_type=False` su tutti i `SAEnum` (gli enum esistono già nella migrazione SQL).
- La precedenza tra tipi di zona (`vietata > limitata > operativa`) è applicata a runtime in `ServizioGIS`, non tramite vincoli DB. In Sprint 1 tutte le zone sono create dall'Operatore (IF-OP.02).

---

## Principi di Ingegneria del Software da rispettare

### Tracciabilità
- Ogni file, classe, metodo implementato deve essere ricondotto a un ID del Product Backlog.
- Usare commenti di tracciabilità solo nei punti architetturalmente rilevanti, nel formato: `// [IF-UT.02] Prenota mezzo`.
- Non aggiungere commenti ovunque — solo dove la connessione al requisito non è ovvia dal codice.

### Modularità e separazione delle responsabilità
- Un controller per entità/funzione principale (vedere lista in `SprintZero.md § 2.3.2`).
- Un service per dominio logico nel BLL.
- Un repository per entità nel DAL.

### Requisiti non funzionali da rispettare nel codice
- **IIN-2 Sicurezza**: tutte le comunicazioni client-server cifrate. Blocco account dopo 5 tentativi falliti. Accesso solo alle funzionalità del proprio ruolo (UT/OP/AP).
- **IIN-3 Usabilità**: UI accessibile WCAG.
- **IIN-4 Scalabilità**: l'aggiunta di una nuova tipologia di mezzo non deve richiedere modifiche strutturali — usare pattern estendibili (es. strategy, factory).
- **IIN-5 Portabilità**: il sistema deve funzionare su browser desktop e mobile senza installazione.

### Testing
- Ogni caso d'uso implementato deve avere almeno un test per lo **scenario base** e uno per ogni **scenario alternativo** documentato.
- I test devono essere indipendenti (nessun ordine di esecuzione implicito).
- Non mockare il database se il test verifica comportamento persistente — usare un DB di test reale o in-memory.

### Gestione degli stati del mezzo
Lo stato di un mezzo (`Disponibile`, `Prenotato`, `In uso`, `In pausa`, `In manutenzione`, `Fuori servizio`) è un concetto centrale. Qualsiasi operazione che modifica lo stato deve passare per `ServizioMobilità` e rispettare le transizioni valide. Non aggiornare lo stato direttamente dal Controller o dal DAL.

**Prenotazione scaduta**: non esiste un job di cleanup automatico. Se `scade_at < now()` ma il mezzo è ancora in stato `Prenotato`, `_sblocca_singolo` in `ServizioMobilita` rileva la scadenza (nessuna prenotazione attiva per qualsiasi utente) e resetta il mezzo a `Disponibile` prima di procedere con lo sblocco.

### Logica pagamento a fine corsa [IF-UT.20]

Il flusso in `ServizioPricing.effettua_pagamento` segue questa precedenza:

1. **Abbonamento attivo** (`AbbonamentoUtente.data_fine > now()`) → `importo = 0`, `importo_pieno = importo_base`. Le promozioni vengono ignorate.
2. **Promozione selezionata** (solo se `importo > 0`) → `importo = importo_base * (1 - sconto%)`, `importo_pieno = importo_base`, `offerta_applicata_id` salvato.
3. **Nessuna offerta** → `importo = importo_base`.

I campi `importo_pieno` e `offerta_applicata_id` sono salvati nella tabella `pagamenti` (migrazione `011_pagamento_offerta_applicata.sql`) e usati da `CorsaRepository.find_by_utente_order_by_data` per lo storico con badge abbonamento/promozione.

**Regola**: il frontend (`VistaCorsa.tsx`) salta il modal promozioni se `getAbbonamentoCorrente()` restituisce un abbonamento con `data_fine > now()`. Il backend applica comunque la logica corretta indipendentemente da ciò che il frontend invia.

### Logica abbonamenti [IF-UT.16]

- `ServizioAbbonamento.sottoscrivi()` impedisce l'attivazione se esiste già un abbonamento con `data_fine > now()` (errore 422).
- `VistaAbbonamenti.tsx` nasconde i piani disponibili se `corrente.data_fine > new Date()`.
- `AbbonamentoRepository.get_attivo()` filtra per `stato == "attivo"` ma **non** per `data_fine > now()` — il check sulla data è responsabilità del chiamante.

### Sblocco multiplo e gruppo corsa [IF-UT.04]

Quando più mezzi vengono sbloccati insieme (batch), `ServizioMobilita.sblocca_mezzi` assegna lo stesso `gruppo_corsa_id` (UUID condiviso) a tutte le corse create. Questo permette di raggrupparle nello storico (`VistaCorse.tsx`).

Il frontend può avviare lo sblocco da tre punti:
- **Pannello mappa** (modalità `sblocca`) — selezione diretta
- **Pannello prenotazioni** (homepage) — bottone "Sblocca (N)"
- **Sidebar → Le mie prenotazioni** — bottone "Sblocca (N)" che sblocca tutte le prenotazioni attive insieme

---

## Documentazione continua

Ad ogni sprint, aggiornare:

| Documento | Contenuto |
|---|---|
| `docs/SprintZero.md` | Solo se cambiano requisiti o architettura (deliberato, non automatico) |
| `docs/Sprint{N}.md` | Sprint Backlog, casi d'uso, diagrammi di sequenza, note di implementazione |
| `docs/README.md` | Panoramica del progetto, istruzioni per avviare il sistema |

La documentazione è parte della **Definition of Done** di ogni item. Un item non è completo se non è documentato.

---

## Glossario (termini chiave)

I termini tecnici del dominio sono definiti in `docs/SprintZero.md § 4.2`. Usare **sempre** i termini del glossario nel codice (nomi di classi, metodi, variabili):

- `Corsa` (non `Ride`, `Trip`, `Session`)
- `Mezzo` (non `Vehicle`, `Bike`)
- `Prenotazione` (non `Booking`, `Reservation`)
- `Zona` con i sottotipi: `ZonaOperativa`, `ZonaParcheggio`, `ZonaLimitata`, `ZonaVietata` — nel codice Python l'enum `TipoZona` usa valori lowercase (`"operativa"`, `"parcheggio"`, `"limitata"`, `"vietata"`) per allineamento con i tipi PostgreSQL
- `Segnalazione` (non `Report`, `Issue`, `Ticket`)
- `Flotta`, `Tariffa`, `Promozione`, `Abbonamento`, `Bonus`

---

## Cosa fare prima di scrivere codice

1. Verificare che l'item da implementare abbia un ID nel Product Backlog (`SprintZero.md § 1.4`).
2. Verificare che esista o creare la specifica del caso d'uso nello sprint corrente.
3. Identificare il layer corretto in cui il codice va scritto (Controller / BLL / Model / DAL).
4. Verificare che non esista già logica simile in un altro service (evitare ridondanza — `IIN` 12 del prompt).
5. Scrivere prima il test, poi l'implementazione.

## Cosa non fare mai

- Non aggiungere funzionalità non presenti nel Product Backlog senza prima aggiornarvi lo sprint backlog.
- Non mescolare logica di business nel Controller o nel DAL.
- Non accedere al DB direttamente dalla BLL (sempre tramite il repository del DAL).
- Non usare termini diversi da quelli del glossario per i concetti di dominio.
- Non committare codice non testato su un item del backlog.
- Non modificare lo stato di un mezzo al di fuori di `ServizioMobilità`.
- **Non inventare classi, interfacce o schemi Pydantic/TypeScript che non esistono nel diagramma delle classi** (`docs/Diagrammi/DiagrammaClassi.md`). Prima di creare una nuova classe, verificare che esista nel diagramma. Se serve qualcosa che non c'è, chiedere esplicitamente prima di procedere. I nomi devono corrispondere esattamente: es. `Corsa` non `RiepilogoCorsa` o `CorsaStorico`. I Pydantic schema del backend e le interfacce TypeScript del frontend sono serializzazioni delle classi del diagramma — usare lo stesso nome (eventualmente con suffisso tecnico `Out` solo se necessario per evitare collisioni con ORM, ma preferire il nome esatto del diagramma). Il diagramma di sequenza definisce il flusso di chiamate e i tipi di ritorno; il diagramma delle classi definisce le classi. Entrambi sono vincolanti.
