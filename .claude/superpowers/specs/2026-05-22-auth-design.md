# Spec: Registrazione e Login — Smart Mobility

**Data:** 2026-05-22
**Items:** IF-UT.17, IF-UT.18, IF-AP.07, IF-OP.16
**Branch:** `feature/auth`

---

## 1. Scope

Implementazione completa del flusso di autenticazione e registrazione per la piattaforma Smart Mobility, con distinzione tra:
- **Utente (UT):** interfaccia mobile (portrait), registrazione self-service + Google OAuth
- **Operatore (OP) e Amministrazione Pubblica (AP):** interfaccia desktop (landscape), solo login email/password, account creati da admin

Items fuori scope: recupero password, modifica profilo (IF-UT.19), social login Apple.

---

## 2. Approccio scelto

**Supabase Auth come motore principale.** Supabase gestisce hashing password, JWT, sessioni, Google OAuth. Il backend FastAPI valida il JWT con PyJWT senza reimplementare logica di sicurezza. I ruoli (UT/OP/AP) sono determinati dalla presenza dell'UUID nelle tabelle `utenti`, `operatori`, `amministratori`.

---

## 3. Database

### Schema esistente (nessuna modifica)

```
auth.users (Supabase)       → id, email, password_hash, provider
utenti      (nostro DB)     → id (FK auth.users), nome, cognome, telefono, sospeso
operatori   (nostro DB)     → id (FK auth.users), nome, config operativa
amministratori (nostro DB)  → id (FK auth.users), nome
```

### Aggiunta: migration `002_tentativi_login.sql`

```sql
CREATE TABLE tentativi_login (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email        TEXT NOT NULL,
  tentativo_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  riuscito     BOOLEAN NOT NULL
);
CREATE INDEX tentativi_login_email_idx ON tentativi_login (email, tentativo_at);
```

Usata da `ServizioUtenti` per implementare il lockout a 5 tentativi (IIN-2).

### Determinazione ruolo

Dopo login, `AttoreRepository.trova_per_id(uuid)` cerca in ordine:
1. `utenti` → ruolo `"UT"`
2. `operatori` → ruolo `"OP"`
3. `amministratori` → ruolo `"AP"`
4. Non trovato → `AttoreNonTrovatoException`

---

## 4. Backend

### Struttura file

```
backend/
├── controllers/
│   ├── login_controller.py        # LoginController: POST /auth/login, GET /auth/me
│   └── utente_controller.py       # UtenteController: POST /auth/registra
├── bll/
│   └── servizio_utenti.py         # ServizioUtenti
├── model/
│   ├── persona.py                 # Persona abstract (id, email, nome, cognome — NO password)
│   ├── utente.py                  # Utente(Persona): sospeso
│   ├── operatore.py               # Operatore(Persona): config operativa
│   └── amministrazione_pubblica.py
├── dal/
│   └── attore_repository.py       # AttoreRepository
├── middleware/
│   └── auth_middleware.py         # verify_token
└── main.py                        # mounting router /auth
```

### Controller Layer

**`LoginController`**
- `POST /auth/login` — valida presenza `email` e `password`, delega a `ServizioUtenti.autentica_account()`
- `GET /auth/me` — route protetta da middleware, delega a `ServizioUtenti.profilo_corrente(utente_id)`

**`UtenteController`**
- `POST /auth/registra` — valida formato email, password ≥ 8 caratteri, `nome` e `cognome` non vuoti; delega a `ServizioUtenti.registra_account()`

**Middleware `verify_token`**
- Estrae JWT da `Authorization: Bearer <token>`
- Verifica firma con chiave pubblica Supabase (PyJWT + JWKS endpoint)
- Inietta `utente_corrente: { id: UUID, ruolo: str }` nella request
- 401 se token mancante o scaduto
- 403 se ruolo non autorizzato per la route

### Business Logic Layer — `ServizioUtenti`

**`registra_account(email, password, nome, cognome)`**
1. Chiama Supabase Auth Admin API → crea `auth.users`
2. `AttoreRepository.crea_utente(id, nome, cognome)`
3. Restituisce `{ access_token, ruolo: "UT", profilo }`

**`autentica_account(email, password)`**
1. `AttoreRepository.conta_tentativi_falliti(email, ultimi 15 min)` → se ≥ 5: `AccountBloccatoException` (423)
2. Chiama Supabase Auth `signInWithPassword(email, password)` → se fallisce: registra tentativo fallito, solleva `CredenzialNonValideException` (401)
3. `AttoreRepository.trova_per_id(supabase_user.id)` → determina ruolo
4. `AttoreRepository.registra_tentativo(email, riuscito=True)`
5. Restituisce `{ access_token, ruolo, profilo }`

**`profilo_corrente(utente_id)`**
1. `AttoreRepository.trova_per_id(utente_id)`
2. Restituisce profilo con ruolo

### Data Access Layer — `AttoreRepository`

| Metodo | Operazione |
|---|---|
| `trova_per_id(id)` | Cerca in `utenti` → `operatori` → `amministratori`, restituisce `(profilo, ruolo)` |
| `trova_per_email(email)` | Risolve email → id via Supabase Auth Admin API, poi `trova_per_id` |
| `crea_utente(id, nome, cognome)` | `INSERT INTO utenti` |
| `conta_tentativi_falliti(email, da)` | `SELECT COUNT(*) FROM tentativi_login WHERE riuscito=false AND tentativo_at > NOW() - INTERVAL '15 minutes'` |
| `registra_tentativo(email, riuscito)` | `INSERT INTO tentativi_login` |

---

## 5. Frontend

### Struttura file

```
frontend/src/
├── views/
│   └── auth/
│       ├── VistaLogin.tsx         # componente unico mobile + desktop
│       └── VistaLogin.css         # layout responsivo (media query 768px)
├── services/
│   └── AuthService.ts             # aggiornamento file esistente
└── App.tsx                        # routing con RoutaProtetta
```

### `VistaLogin` — layout responsivo

| | Mobile (< 768px) — IUI-1 | Desktop (≥ 768px) — IUI-10 |
|---|---|---|
| Orientamento | Portrait, verticale | Landscape, card centrata |
| SIGN UP | Visibile | Nascosto |
| Google OAuth | Pulsante visibile | Pulsante visibile |
| Post-login redirect | `/utente/home` | `/operatore/dashboard` o `/ap/dashboard` |

Palette: sfondo bianco, bottoni verde acqua (`#4CAF9A` indicativo), bordi arrotondati (mockup IUI-1 / IUI-10).

### `AuthService` — metodi

```typescript
registra(dati: { email, password, nome, cognome }): Promise<{ ruolo, profilo }>
autentica(credenziali: { email, password }): Promise<{ ruolo, profilo }>
autenticaGoogle(): Promise<void>           // solo UT
logout(): void
utenteCorrente(): { ruolo, profilo } | null
```

Tutti i metodi salvano/rimuovono il JWT in `localStorage`. `autenticaGoogle()` usa `supabase.auth.signInWithOAuth`, poi chiama `GET /auth/me` per ottenere ruolo e profilo.

### Routing in `App.tsx`

```
/                   → VistaLogin (redirect a home se già autenticato)
/utente/*           → RoutaProtetta ruolo="UT" → VistaUtente
/operatore/*        → RoutaProtetta ruolo="OP" → VistaOperatore
/ap/*               → RoutaProtetta ruolo="AP" → VistaAP
/non-autorizzato    → pagina errore
```

`RoutaProtetta`: se non autenticato → redirect `/`; se ruolo errato → redirect `/non-autorizzato`.

---

## 6. Error handling

### Backend

| Eccezione BLL | HTTP | Messaggio |
|---|---|---|
| `CredenzialNonValideException` | 401 | "Credenziali non valide" |
| `AccountBloccatoException` | 423 | "Account bloccato. Riprova tra X minuti" |
| `AccountSospesoException` | 403 | "Account sospeso" |
| `EmailGiaRegistrataException` | 409 | "Email già registrata" |
| `AttoreNonTrovatoException` | 404 | "Utente non trovato" |
| `ServizioAuthException` | 502 | "Servizio auth non disponibile" |
| Token mancante/scaduto (middleware) | 401 | "Token non valido o scaduto" |
| Ruolo non autorizzato (middleware) | 403 | "Accesso non autorizzato" |

### Frontend

| Codice HTTP | Messaggio UI |
|---|---|
| 401 | "Email o password non corretti" |
| 423 | "Account bloccato. Riprova tra X minuti" |
| 403 | "Account sospeso. Contatta il supporto" |
| 409 | "Email già registrata" |
| 502 / rete | "Servizio temporaneamente non disponibile" |

---

## 7. Testing (pytest)

| Test | Scenario | Item |
|---|---|---|
| `test_login_successo_ut` | Login UT valido → JWT + ruolo UT | IF-UT.18 |
| `test_login_successo_op` | Login OP valido → JWT + ruolo OP | IF-OP.16 |
| `test_login_successo_ap` | Login AP valido → JWT + ruolo AP | IF-AP.07 |
| `test_login_credenziali_errate` | Password sbagliata → 401 | IF-UT.18 alt |
| `test_login_lockout` | 5 tentativi falliti → 423 al 6° | IIN-2 |
| `test_login_account_sospeso` | UT sospeso → 403 | IF-OP.05 |
| `test_registra_successo` | Nuova registrazione → profilo in DB | IF-UT.17 |
| `test_registra_email_duplicata` | Email già presente → 409 | IF-UT.17 alt |
| `test_me_token_valido` | GET /auth/me con JWT → profilo + ruolo | IF-UT.18 |
| `test_me_senza_token` | GET /auth/me senza JWT → 401 | IIN-2 |

I test usano DB Supabase di test reale (no mock del database).

---

## 8. Vincoli rispettati

- **IIN-2:** lockout dopo 5 tentativi falliti via `tentativi_login`; JWT cifrato in transito (HTTPS)
- **IIN-2:** ruoli isolati — ogni route protetta verifica il ruolo nel middleware
- **IIN-4:** modello `Persona` estendibile senza modifiche strutturali
- **Glossario:** `Corsa`, `Mezzo`, `Prenotazione`, `Zona` nei nomi — nessun termine anglofono nei layer di dominio
- **Architettura:** nessuna logica di business nel Controller; nessun accesso DB diretto dalla BLL
