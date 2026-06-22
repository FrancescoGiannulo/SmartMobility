# CLAUDE.md — Smart Mobility

## Contesto del progetto

**Smart Mobility** è un sistema software per il Comune di Zootropolis che integra servizi di bike, car e e-scooter sharing in un'unica piattaforma.

Documenti di riferimento:
- [`docs/SprintZero.md`](docs/SprintZero.md) — architettura, glossario, mockup UI
- [`docs/Sprintn3.md`](docs/Sprintn3.md) — Product Backlog completo, Sprint 1 + Sprint 2 + Sprint 3 Backlog, casi d'uso, mockup UI (**documento primario** — sostituisce i documenti dei precedenti sprint)
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
| Mappe | Google Maps (`@vis.gl/react-google-maps`) | Mappa interattiva e geofencing |
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
- Stato attuale (giugno 2026): OAuth con Google non completamente funzionante in produzione — issue aperta

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
VITE_GOOGLE_MAPS_API_KEY=<google maps api key>
```

### Struttura del progetto

```
frontend/src/
├── views/
│   ├── auth/             → VistaLogin, CallbackOAuth
│   ├── utente/           → VistaHomePageUtente, VistaCorsa, VistaStoricoCorse, VistaPagamenti,
│   │                        VistaAbbonamenti, VistaSegnalazione, VistaProfiloUtente
│   ├── operatore/        → VistaMappaOperatore, VistaMezziOperatore, VistaTariffeOfferte,
│   │                        VistaImpostazioniRegole, VistaParametriSistema, VistaSegnalazioniOperatore
│   └── amministrazione/  → VistaDashboardAP, VistaReportAP
├── components/           → RoutaProtetta, ZonaPoligono, TooltipZona,
│                            ClusterLayerAP, HeatmapLayerAP, PopupStatsZona
└── services/
    ├── ApiService.ts           → gateway HTTP centrale + interceptor JWT
    ├── AuthService.ts          → login, registrazione, OAuth callback
    ├── MapService.ts           → mezzi e zone [IF-UT.01, IF-AP.03, IF-OP.01]
    ├── CorsaService.ts         → sblocco, pausa, termina, storico [IF-UT.03, IF-UT.04, IF-UT.09, IF-UT.11]
    ├── PrenotazioneService.ts  → prenotazioni: crea, annulla, attive, caratteristiche mezzo [IF-UT.02]
    ├── PaymentService.ts       → metodi di pagamento [IF-UT.05, IF-UT.06]
    ├── AbbonamentoService.ts   → abbonamenti [IF-UT.13]
    ├── OffertaService.ts       → offerte/promozioni [IF-OP.10]
    ├── FlottaService.ts        → gestione flotta [IF-OP.02, IF-OP.03, IF-OP.04]
    ├── ZonaService.ts          → CRUD zone [IF-OP.07]
    ├── SegnalazioneService.ts  → segnalazioni [IF-UT.12, IF-OP.08]
    ├── ConfigurazioneService.ts → parametri sistema [IF-OP.11]
    └── RegolaFinecorsaService.ts → regole fine corsa [IF-OP.06]

backend/
├── database.py       → engine SQLAlchemy, SessionLocal, Base (DeclarativeBase), get_db()
├── migrations/       → file SQL da eseguire su Supabase (001…013)
├── model/            → ORM SQLAlchemy 2.0 (Mapped + mapped_column); 17 entità; importare Base da database.py
├── controllers/      → validazione HTTP (12 controller file)
├── bll/              → logica applicativa (11 servizi)
├── dal/              → repository (15, uno per entità)
└── tests/            → test pytest (18 file); conftest.py crea fixture utente/operatore/AP con cleanup
```

**Controller backend** (12 file in `backend/controllers/`):

| File | Responsabilità |
|---|---|
| `login_controller.py` | auth: login, registrazione, OAuth callback |
| `corsa_controller.py` | prenotazioni, sblocco, corsa, pausa, storico |
| `pagamenti_controller.py` | metodi di pagamento |
| `pricing_controller.py` | tariffe e promozioni (lato utente) |
| `abbonamento_controller.py` | abbonamenti utente |
| `mezzo_operatore_controller.py` | flotta operatore (aggiungi, dismetti, modifica stato) |
| `zona_operatore_controller.py` | zone operative, vietate, limitate, parcheggio |
| `regola_fine_corsa_controller.py` | regole fine corsa |
| `offerta_controller.py` | offerte/promozioni (lato operatore) |
| `configurazione_controller.py` | parametri sistema |
| `utente_controller.py` | segnalazioni utente |
| `ap_controller.py` | report AP, mappa AP, segnalazioni OP, gestione utenti OP |

**BLL** (11 servizi in `backend/bll/`): `ServizioMobilità`, `ServizioPrenotazione`, `ServizioPricing`, `ServizioAbbonamento`, `ServizioMappa`, `ServizioReport`, `ServizioOfferta`, `ServizioRegoleFineCorsa`, `ServizioParametri`, `ServizioUtenti`, `ServizioSegnalazione`

**DAL** (15 repository in `backend/dal/`): `MezzoRepository`, `CorsaRepository`, `PrenotazioneRepository`, `PagamentoRepository`, `TariffaRepository`, `ZonaRepository`, `UtenteRepository`, `OperatoreRepository`, `AttoreRepository`, `AbbonamentoRepository`, `OffertaRepository`, `PromozioneRepository`, `RegoleFIneCorsaRepository`, `ParametriSistemaRepository`, `SegnalazioneRepository`

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
User Story (Sprintn3.md § 1.4)
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
└── API Service Layer (ApiService, AuthService, MapService, CorsaService, PaymentService,
                       AbbonamentoService, OffertaService, FlottaService, ZonaService,
                       SegnalazioneService, ConfigurazioneService, RegolaFinecorsaService)

Server
├── Controller Layer
├── Business Logic Layer (BLL)
├── Model
└── Data Access Layer (DAL) → DBMS

Servizi Esterni
├── GoogleMaps (geolocalizzazione e geofencing)
└── ProviderPagamenti (gateway pagamenti)
```

### Vincoli architetturali obbligatori

- **Controller**: solo validazione HTTP e smistamento. Zero logica di business.
- **BLL**: tutta la logica applicativa. Nessun accesso diretto al DB.
- **DAL**: solo accesso ai dati. Nessuna logica di business.
- **View/ApiService**: nessuna logica di business lato client.
- **model/**: ORM SQLAlchemy 2.0 puri — nessuna logica, nessun Pydantic. I `CheckConstraint` vanno in `__table_args__`, non come argomenti di `mapped_column`. Usare `create_type=False` su tutti i `SAEnum` (gli enum esistono già nella migrazione SQL).
- La precedenza tra tipi di zona (`vietata > limitata > operativa`) è applicata a runtime in `ServizioMappa`, non tramite vincoli DB. Le zone sono create dall'Operatore (IF-OP.07).

---

## Principi di Ingegneria del Software da rispettare

### Tracciabilità
- Ogni file, classe, metodo implementato deve essere ricondotto a un ID del Product Backlog.
- Usare commenti di tracciabilità solo nei punti architetturalmente rilevanti, nel formato: `// [IF-UT.02] Prenota mezzo`.
- Non aggiungere commenti ovunque — solo dove la connessione al requisito non è ovvia dal codice.
- **Prima di scrivere o citare un ID (`IF-UT.xx`, `IF-OP.xx`, `IF-AP.xx`) in codice, commenti, diagrammi o documentazione, verificare SEMPRE la corrispondenza nome↔ID in `docs/Sprintn3.md` (§ 1.4) — non riusare un ID visto in un commento esistente, nel nome di un file, o in un altro diagramma senza controllare il backlog. I commenti già presenti nel codice possono essere essi stessi sbagliati (es. caso reale 2026-06-20: `IF-UT.12` usato per "Salva Metodi Pagamento" invece di `IF-UT.06`, e `IF-UT.15` usato per "Invia Segnalazione" invece di `IF-UT.12`, in collisione con `IF-UT.15` reale = "Scrive una recensione"). Se un ID citato nel codice non si trova nel backlog (es. `IF-UT.21`), segnalarlo come discrepanza in `docs/CoerenzaDiagrammaClassi.md` invece di darlo per buono.

### Modularità e separazione delle responsabilità
- Un controller per entità/funzione principale (vedere lista controller sopra).
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

**Prenotazione scaduta**: il cleanup avviene su due livelli complementari:
1. **Proattivo (pg_cron)**: la funzione `cleanup_prenotazioni_scadute()` (migrazione `016_cleanup_scadenze.sql`) gira ogni 5 minuti, marca le prenotazioni scadute come `scaduta`, rilascia i mezzi a `Disponibile` e inserisce una notifica per l'utente.
2. **Lazy (fallback)**: `_sblocca_singolo` in `ServizioMobilita` rileva comunque la scadenza al momento dello sblocco, come sicurezza nel caso il job non sia ancora passato.

**Abbonamento scaduto**: la funzione `cleanup_abbonamenti_scaduti()` (stessa migrazione) gira ogni giorno a mezzanotte, marca gli abbonamenti con `data_fine < now()` come `scaduto` e notifica l'utente. Il check lazy in `ServizioAbbonamento` resta attivo come doppia sicurezza.

Entrambe le funzioni usano l'entità `Notifica` già modellata nel Diagramma Classi e implementata in `NotificaRepository.crea()`. Non introducono nuove classi o interfacce. Per abilitare pg_cron su Supabase: Dashboard → Database → Extensions → pg_cron.

### Logica pagamento a fine corsa [IF-UT.05]

Il flusso in `ServizioPricing.effettua_pagamento` segue questa precedenza:

1. **Abbonamento attivo** (`AbbonamentoUtente.data_fine > now()`) → `importo = 0`, `importo_pieno = importo_base`. Le promozioni vengono ignorate.
2. **Promozione selezionata** (solo se `importo > 0`) → `importo = importo_base * (1 - sconto%)`, `importo_pieno = importo_base`, `offerta_applicata_id` salvato.
3. **Nessuna offerta** → `importo = importo_base`.

I campi `importo_pieno` e `offerta_applicata_id` sono salvati nella tabella `pagamenti` (migrazione `011_pagamento_offerta_applicata.sql`) e usati da `CorsaRepository.find_by_utente_order_by_data` per lo storico con badge abbonamento/promozione.

**Regola**: il frontend (`VistaCorsa.tsx`) salta il modal promozioni se `getAbbonamentoCorrente()` restituisce un abbonamento con `data_fine > now()`. Il backend applica comunque la logica corretta indipendentemente da ciò che il frontend invia.

### Logica abbonamenti [IF-UT.13]

- `ServizioAbbonamento.sottoscrivi()` impedisce l'attivazione se esiste già un abbonamento con `data_fine > now()` (errore 422).
- `VistaAbbonamenti.tsx` nasconde i piani disponibili se `corrente.data_fine > new Date()`.
- `AbbonamentoRepository.get_attivo()` filtra per `stato == "attivo"` ma **non** per `data_fine > now()` — il check sulla data è responsabilità del chiamante.

### Sblocco multiplo e gruppo corsa [IF-UT.03]

Quando più mezzi vengono sbloccati insieme (batch), `ServizioMobilita.sblocca_mezzi` assegna lo stesso `gruppo_corsa_id` (UUID condiviso) a tutte le corse create. Questo permette di raggrupparle nello storico (`VistaStoricoCorse.tsx`).

Il frontend può avviare lo sblocco da tre punti:
- **Pannello mappa** (modalità `sblocca`) — selezione diretta
- **Pannello prenotazioni** (homepage) — bottone "Sblocca (N)"
- **Sidebar → Le mie prenotazioni** — bottone "Sblocca (N)" che sblocca tutte le prenotazioni attive insieme

### Pausa corsa [IF-UT.09]

La pausa accumula tempo in `pausa_durata_accumulata_sec` (migrazione `013_pausa_corsa.sql`). Il costo della pausa (`addebito_pausa` da `ParametriSistema`) viene sommato all'importo finale in `ServizioPricing`. Il mezzo resta in stato `In pausa` durante la sosta — non torna `Disponibile`.

---

## Documentazione continua

Ad ogni sprint, aggiornare:

| Documento | Contenuto |
|---|---|
| `docs/SprintZero.md` | Solo se cambiano requisiti o architettura (deliberato, non automatico) |
| `docs/Sprintn3.md` | Sprint Backlog, casi d'uso, diagrammi di sequenza, note di implementazione |
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

1. Verificare che l'item da implementare abbia un ID nel Product Backlog (`Sprintn3.md § 1.4`) e che il nome dell'item corrisponda esattamente a quell'ID — non assumere che un ID visto altrove (commento nel codice, nome file, altro diagramma) sia corretto: va sempre riverificato lì.
2. Verificare che esista o creare la specifica del caso d'uso nello sprint corrente.
3. Identificare il layer corretto in cui il codice va scritto (Controller / BLL / Model / DAL).
4. Verificare che non esista già logica simile in un altro service (evitare ridondanza).
5. Scrivere prima il test, poi l'implementazione.

## Cosa non fare mai

- Non aggiungere funzionalità non presenti nel Product Backlog senza prima aggiornarvi lo sprint backlog.
- Non mescolare logica di business nel Controller o nel DAL.
- Non accedere al DB direttamente dalla BLL (sempre tramite il repository del DAL).
- Non usare termini diversi da quelli del glossario per i concetti di dominio.
- Non committare codice non testato su un item del backlog.
- Non modificare lo stato di un mezzo al di fuori di `ServizioMobilità`.
- **Non inventare classi, interfacce o schemi Pydantic/TypeScript che non esistono nel diagramma delle classi.** La fonte di verità è `docs/Diagrammi/Diagramma Classi.drawio`; `docs/Diagrammi/DiagrammaClassi.md` ne è l'export testuale (rigenerato dal .drawio). Prima di creare una nuova classe, verificare che esista nel diagramma. Se serve qualcosa che non c'è, chiedere esplicitamente prima di procedere. I nomi devono corrispondere esattamente: es. `Corsa` non `RiepilogoCorsa` o `CorsaStorico`. I Pydantic schema del backend e le interfacce TypeScript del frontend sono serializzazioni delle classi del diagramma — usare lo stesso nome (eventualmente con suffisso tecnico `Out` solo se necessario per evitare collisioni con ORM, ma preferire il nome esatto del diagramma). Il diagramma di sequenza definisce il flusso di chiamate e i tipi di ritorno; il diagramma delle classi definisce le classi. Entrambi sono vincolanti.
