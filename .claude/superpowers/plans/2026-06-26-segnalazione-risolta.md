# Gestisci segnalazione — stato "risolta" [IF-OP.08] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Far comparire lo stato "risolta" sulle segnalazioni: l'operatore può chiudere una segnalazione presa in carico, e l'utente la vede "Risolta" nel proprio storico.

**Architecture:** Nuovo valore enum `risolta` in `StatoSegnalazione`, aggiunto al tipo Postgres via migrazione. Nuovo metodo `ServizioSegnalazione.risolvi()` (BLL) che valida la transizione `in_carico → risolta` e riusa `SegnalazioneRepository.aggiorna_stato` già esistente. Nuovo endpoint `PATCH /operatore/segnalazioni/{id}/risolvi`. Frontend: nuova funzione service + bottone lato operatore + badge lato utente.

**Tech Stack:** FastAPI, SQLAlchemy 2.0 (raw `text()` nel repository esistente), pytest + `TestClient`, React 19 + TypeScript, Axios.

## Global Constraints

- Transizione valida solo `in_carico → risolta` (non da `aperta`). Tentativo non valido → 422.
- Nessuna notifica push; solo badge nello storico utente (`VistaSegnalazione.tsx`), già ricaricato da `caricaStorico()`.
- Seguire il glossario: `Segnalazione`, non altri termini.
- Layer: Controller solo validazione HTTP, logica di transizione in `ServizioSegnalazione` (BLL), accesso dati in `SegnalazioneRepository` (DAL) — non aggiungere logica di business nel controller o nel DAL.

---

### Task 1: Migrazione SQL — nuovo valore enum

**Files:**
- Create: `backend/migrations/020_segnalazione_risolta.sql`

**Interfaces:**
- Produces: valore `'risolta'` disponibile nel tipo Postgres `stato_segnalazione`, usato da Task 2 in poi.

- [ ] **Step 1: Creare il file di migrazione**

```sql
-- [IF-OP.08] Aggiunge lo stato "risolta" alle segnalazioni
ALTER TYPE stato_segnalazione ADD VALUE 'risolta';
```

- [ ] **Step 2: Eseguire la migrazione su Supabase**

Apri Supabase Dashboard → SQL Editor, esegui il contenuto di `backend/migrations/020_segnalazione_risolta.sql` sul database del progetto (lo stesso usato da `DATABASE_URL` in `backend/.env`). Questo passo è manuale, come le migrazioni precedenti in questo progetto — non esiste uno script di migrazione automatico.

Verifica:
```sql
SELECT unnest(enum_range(NULL::stato_segnalazione));
```
Expected: la riga `risolta` compare nel risultato insieme a `aperta` e `in_carico`.

- [ ] **Step 3: Commit**

```bash
git add backend/migrations/020_segnalazione_risolta.sql
git commit -m "feat(db): aggiunge stato 'risolta' a stato_segnalazione [IF-OP.08]"
```

---

### Task 2: Model — nuovo valore enum Python

**Files:**
- Modify: `backend/model/segnalazione.py:11-14`

**Interfaces:**
- Consumes: nessuno (dipende solo dal tipo Postgres aggiornato in Task 1, ma SQLAlchemy con `create_type=False` legge solo i valori Python — il file deve combaciare).
- Produces: `StatoSegnalazione.risolta`, usato da Task 3 (BLL).

- [ ] **Step 1: Aggiungere il valore all'enum**

In `backend/model/segnalazione.py`, sostituire:

```python
class StatoSegnalazione(str, Enum):
    aperta = "aperta"
    in_carico = "in_carico"
```

con:

```python
class StatoSegnalazione(str, Enum):
    aperta = "aperta"
    in_carico = "in_carico"
    risolta = "risolta"
```

- [ ] **Step 2: Verifica rapida d'importazione**

Run: `cd backend && uv run python -c "from model.segnalazione import StatoSegnalazione; print(StatoSegnalazione.risolta.value)"`
Expected: stampa `risolta` senza errori.

- [ ] **Step 3: Commit**

```bash
git add backend/model/segnalazione.py
git commit -m "feat(model): aggiunge StatoSegnalazione.risolta [IF-OP.08]"
```

---

### Task 3: BLL — metodo `risolvi` con validazione transizione

**Files:**
- Modify: `backend/bll/servizio_segnalazione.py`
- Test: `backend/tests/test_segnalazione_risolta.py` (nuovo)

**Interfaces:**
- Consumes: `SegnalazioneRepository.aggiorna_stato(segnalazione_id, StatoSegnalazione) -> bool` (già esistente, `backend/dal/segnalazione_repository.py:93-104`); `ServizioSegnalazione.get_dettaglio_segnalazione(segnalazione_id) -> dict` (già esistente, righe 57-69).
- Produces: `ServizioSegnalazione.risolvi(segnalazione_id: UUID) -> dict` (stessa forma di `get_dettaglio_segnalazione`); eccezione `TransizioneNonValida(Exception)`, usata da Task 4 (controller).

Il test in questo task usa `TestClient` end-to-end (come `backend/tests/test_recensione.py`) per evitare di duplicare logica di setup HTTP — non serve un test BLL isolato separato perché `ServizioSegnalazione` non ha dipendenze mockabili interessanti oltre al repository reale.

- [ ] **Step 1: Scrivere i test che useranno l'endpoint (falliranno per 404 — endpoint non esiste ancora)**

Creare `backend/tests/test_segnalazione_risolta.py`:

```python
"""[IF-OP.08] Test Gestisce Segnalazione — transizione a stato 'risolta'."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session
from main import app

http = TestClient(app)


def _login(email: str, password: str) -> str:
    resp = http.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login fallito: {resp.text}"
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _crea_segnalazione(db, utente_id) -> str:
    with Session(db) as s:
        row = s.execute(
            text(
                "INSERT INTO segnalazioni (utente_id, tipologia, descrizione) "
                "VALUES (:uid, 'Altro', 'Test segnalazione') RETURNING id"
            ),
            {"uid": str(utente_id)},
        ).fetchone()
        s.commit()
    return str(row.id)


def _elimina_segnalazione(db, segnalazione_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM segnalazioni WHERE id = :id"), {"id": segnalazione_id})
        s.commit()


@pytest.mark.integration
def test_risolvi_segnalazione_scenario_base(db, utente_test, operatore_test):
    """[IF-OP.08] Segnalazione in_carico -> risolvi -> stato 'risolta', visibile nello storico utente."""
    segnalazione_id = _crea_segnalazione(db, utente_test["id"])
    try:
        token_op = _login(operatore_test["email"], operatore_test["password"])
        resp = http.patch(
            f"/operatore/segnalazioni/{segnalazione_id}/prendi-in-carico",
            headers=_auth(token_op),
        )
        assert resp.status_code == 200, resp.text

        resp = http.patch(
            f"/operatore/segnalazioni/{segnalazione_id}/risolvi",
            headers=_auth(token_op),
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["stato"] == "risolta"

        token_ut = _login(utente_test["email"], utente_test["password"])
        storico = http.get("/utente/segnalazioni", headers=_auth(token_ut))
        assert storico.status_code == 200
        assert any(s["id"] == segnalazione_id and s["stato"] == "risolta" for s in storico.json())
    finally:
        _elimina_segnalazione(db, segnalazione_id)


@pytest.mark.integration
def test_risolvi_segnalazione_aperta_422(db, utente_test, operatore_test):
    """[IF-OP.08] Tentativo di risolvere una segnalazione ancora 'aperta' -> 422."""
    segnalazione_id = _crea_segnalazione(db, utente_test["id"])
    try:
        token_op = _login(operatore_test["email"], operatore_test["password"])
        resp = http.patch(
            f"/operatore/segnalazioni/{segnalazione_id}/risolvi",
            headers=_auth(token_op),
        )
        assert resp.status_code == 422
    finally:
        _elimina_segnalazione(db, segnalazione_id)


@pytest.mark.integration
def test_risolvi_segnalazione_non_trovata_404(operatore_test):
    """[IF-OP.08] Id inesistente -> 404."""
    import uuid
    token_op = _login(operatore_test["email"], operatore_test["password"])
    resp = http.patch(
        f"/operatore/segnalazioni/{uuid.uuid4()}/risolvi",
        headers=_auth(token_op),
    )
    assert resp.status_code == 404
```

- [ ] **Step 2: Eseguire i test per verificare che falliscano**

Run: `cd backend && uv run pytest tests/test_segnalazione_risolta.py -v -m integration`
Expected: FAIL — `404 Not Found` sulle chiamate a `/risolvi` (endpoint non esiste ancora) e la prima asserzione fallisce.

- [ ] **Step 3: Implementare `risolvi` nel BLL**

In `backend/bll/servizio_segnalazione.py`, aggiungere dopo `class SegnalazioneNonTrovata(Exception): pass`:

```python
class TransizioneNonValida(Exception):
    pass
```

E aggiungere, alla fine della classe `ServizioSegnalazione` (dopo `prendi_in_carico`):

```python
    # [IF-OP.08] Segna come risolta
    def risolvi(self, segnalazione_id: UUID) -> dict:
        dettaglio = self.get_dettaglio_segnalazione(segnalazione_id)
        if dettaglio["stato"] != StatoSegnalazione.in_carico.value:
            raise TransizioneNonValida(
                f"Impossibile risolvere una segnalazione con stato '{dettaglio['stato']}'"
            )
        self._repo.aggiorna_stato(segnalazione_id, StatoSegnalazione.risolta)
        return self.get_dettaglio_segnalazione(segnalazione_id)
```

- [ ] **Step 4: Aggiungere l'endpoint nel controller (necessario perché i test passino)**

Vedi Task 4 — i due task sono testati insieme dagli stessi test HTTP. Procedere subito a Task 4 prima di rieseguire i test.

- [ ] **Step 5: Commit (dopo Task 4)**

Il commit di questo task è incluso nel commit di Task 4, perché i test coprono entrambi i livelli (BLL + controller) in un'unica suite HTTP.

---

### Task 4: Controller — endpoint `PATCH /operatore/segnalazioni/{id}/risolvi`

**Files:**
- Modify: `backend/controllers/segnalazione_op_controller.py`

**Interfaces:**
- Consumes: `ServizioSegnalazione.risolvi(segnalazione_id) -> dict` e `TransizioneNonValida` (Task 3).
- Produces: route HTTP `PATCH /operatore/segnalazioni/{segnalazione_id}/risolvi`, response_model `SegnalazioneOut`.

- [ ] **Step 1: Aggiungere l'import dell'eccezione**

In `backend/controllers/segnalazione_op_controller.py`, modificare la riga di import:

```python
from bll.servizio_segnalazione import ServizioSegnalazione, SegnalazioneNonTrovata
```

in:

```python
from bll.servizio_segnalazione import ServizioSegnalazione, SegnalazioneNonTrovata, TransizioneNonValida
```

- [ ] **Step 2: Aggiungere l'endpoint**

Aggiungere alla fine del file:

```python
@router.patch("/segnalazioni/{segnalazione_id}/risolvi", response_model=SegnalazioneOut)
def risolvi_segnalazione(
    segnalazione_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    """[IF-OP.08] Segna una segnalazione come risolta."""
    try:
        return ServizioSegnalazione(db).risolvi(segnalazione_id)
    except SegnalazioneNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TransizioneNonValida as e:
        raise HTTPException(status_code=422, detail=str(e))
```

- [ ] **Step 3: Eseguire i test di Task 3 per verificare che passino**

Run: `cd backend && uv run pytest tests/test_segnalazione_risolta.py -v -m integration`
Expected: PASS su tutti e 3 i test.

- [ ] **Step 4: Eseguire la suite completa dei test segnalazione esistenti (no regressioni)**

Run: `cd backend && uv run pytest tests/ -v -m integration -k segnalazione`
Expected: PASS (nessun test di segnalazione esistente si rompe; se non esistono altri test di segnalazione, questo comando non troverà nulla da eseguire oltre al nuovo file — va bene).

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_segnalazione.py backend/controllers/segnalazione_op_controller.py backend/tests/test_segnalazione_risolta.py
git commit -m "feat(api): endpoint PATCH /operatore/segnalazioni/{id}/risolvi [IF-OP.08]"
```

---

### Task 5: Frontend service — tipo e funzione `risolviSegnalazione`

**Files:**
- Modify: `frontend/src/services/SegnalazioneService.ts:3-11,40-41`

**Interfaces:**
- Produces: `risolviSegnalazione(id: string): Promise<{ data: Segnalazione }>`, usato da Task 6. Tipo `Segnalazione.stato` estende a `'aperta' | 'in_carico' | 'risolta'`, usato da Task 6 e 7.

- [ ] **Step 1: Estendere il tipo `Segnalazione`**

In `frontend/src/services/SegnalazioneService.ts`, sostituire:

```typescript
export interface Segnalazione {
  id: string
  utente_id?: string
  tipologia: string
  descrizione: string
  stato: 'aperta' | 'in_carico'
  created_at: string
  nome_utente?: string
}
```

con:

```typescript
export interface Segnalazione {
  id: string
  utente_id?: string
  tipologia: string
  descrizione: string
  stato: 'aperta' | 'in_carico' | 'risolta'
  created_at: string
  nome_utente?: string
}
```

- [ ] **Step 2: Aggiungere la funzione `risolviSegnalazione`**

Dopo la funzione `aggiornaStatoSegnalazione`, aggiungere:

```typescript
export const risolviSegnalazione = (id: string): Promise<{ data: Segnalazione }> =>
  api.patch(`/operatore/segnalazioni/${id}/risolvi`, {})
```

- [ ] **Step 3: Verifica tipo**

Run: `cd frontend && npx tsc --noEmit -p .`
Expected: nessun nuovo errore relativo a `SegnalazioneService.ts`.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/services/SegnalazioneService.ts
git commit -m "feat(fe): aggiunge risolviSegnalazione e stato 'risolta' [IF-OP.08]"
```

---

### Task 6: Frontend operatore — bottone "Segna come risolta"

**Files:**
- Modify: `frontend/src/views/operatore/VistaSegnalazioniOperatore.tsx`
- Modify: `frontend/src/views/operatore/VistaSegnalazioniOperatore.css` (nuova classe badge)

**Interfaces:**
- Consumes: `risolviSegnalazione(id)` da Task 5; `STATO_LABEL`/`STATO_CLASS` (locali al file).

- [ ] **Step 1: Importare la nuova funzione**

In `frontend/src/views/operatore/VistaSegnalazioniOperatore.tsx`, modificare l'import:

```typescript
import {
  getSegnalazioni,
  getDettaglioSegnalazione,
  aggiornaStatoSegnalazione,
  type Segnalazione,
} from '../../services/SegnalazioneService'
```

in:

```typescript
import {
  getSegnalazioni,
  getDettaglioSegnalazione,
  aggiornaStatoSegnalazione,
  risolviSegnalazione,
  type Segnalazione,
} from '../../services/SegnalazioneService'
```

- [ ] **Step 2: Estendere `STATO_LABEL` e `STATO_CLASS`**

Sostituire:

```typescript
const STATO_LABEL: Record<string, string> = {
  aperta: 'Aperta',
  in_carico: 'In carico',
}

const STATO_CLASS: Record<string, string> = {
  aperta: 'badge-aperta',
  in_carico: 'badge-in-carico',
}
```

con:

```typescript
const STATO_LABEL: Record<string, string> = {
  aperta: 'Aperta',
  in_carico: 'In carico',
  risolta: 'Risolta',
}

const STATO_CLASS: Record<string, string> = {
  aperta: 'badge-aperta',
  in_carico: 'badge-in-carico',
  risolta: 'badge-risolta',
}
```

- [ ] **Step 3: Aggiungere lo state handler `risolviSegnalazioneLocale`**

Dopo la funzione `prendiInCarico`, aggiungere:

```typescript
  const risolviSegnalazioneLocale = async () => {
    if (!selezionata) return
    setAzioneInCorso(true)
    try {
      const res = await risolviSegnalazione(selezionata.id)
      setSelezionata(res.data)
      setSegnalazioni(prev =>
        prev.map(s => s.id === res.data.id ? res.data : s)
      )
      setMessaggio('Segnalazione segnata come risolta.')
      setTimeout(() => setMessaggio(''), 3000)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 404) {
        setErrore('Segnalazione non trovata.')
      } else if (axios.isAxiosError(err) && err.response?.status === 422) {
        setErrore('La segnalazione deve essere prima presa in carico.')
      } else {
        setErrore('Errore durante l\'operazione.')
      }
    } finally {
      setAzioneInCorso(false)
    }
  }
```

- [ ] **Step 4: Aggiornare il blocco JSX del dettaglio**

Sostituire:

```typescript
            {selezionata.stato === 'aperta' && (
              <button
                type="button"
                className="btn-segn-op-primario"
                onClick={prendiInCarico}
                disabled={azioneInCorso}
              >
                {azioneInCorso ? 'Aggiornamento...' : 'PRENDI IN CARICO'}
              </button>
            )}
            {selezionata.stato === 'in_carico' && (
              <p className="segn-op-in-carico-msg">✅ Già presa in carico</p>
            )}
```

con:

```typescript
            {selezionata.stato === 'aperta' && (
              <button
                type="button"
                className="btn-segn-op-primario"
                onClick={prendiInCarico}
                disabled={azioneInCorso}
              >
                {azioneInCorso ? 'Aggiornamento...' : 'PRENDI IN CARICO'}
              </button>
            )}
            {selezionata.stato === 'in_carico' && (
              <button
                type="button"
                className="btn-segn-op-primario"
                onClick={risolviSegnalazioneLocale}
                disabled={azioneInCorso}
              >
                {azioneInCorso ? 'Aggiornamento...' : 'SEGNA COME RISOLTA'}
              </button>
            )}
            {selezionata.stato === 'risolta' && (
              <p className="segn-op-in-carico-msg">✅ Segnalazione risolta</p>
            )}
```

- [ ] **Step 5: Aggiungere lo stile del badge "risolta"**

In `frontend/src/views/operatore/VistaSegnalazioniOperatore.css`, individuare la regola `.badge-in-carico` (o `.badge-aperta`) e aggiungere una regola analoga subito dopo:

```css
.badge-risolta {
  background-color: #dcfce7;
  color: #15803d;
}
```

(Usare gli stessi nomi di proprietà già presenti nelle regole `.badge-aperta`/`.badge-in-carico` per restare consistenti — copiare la struttura esistente e cambiare solo i valori di colore.)

- [ ] **Step 6: Verifica manuale**

Run: `cd frontend && npm run dev`, poi nel browser: login come operatore → Segnalazioni → seleziona una segnalazione `aperta` → "PRENDI IN CARICO" → bottone diventa "SEGNA COME RISOLTA" → click → badge passa a "Risolta" e il messaggio di conferma appare.

- [ ] **Step 7: Commit**

```bash
git add frontend/src/views/operatore/VistaSegnalazioniOperatore.tsx frontend/src/views/operatore/VistaSegnalazioniOperatore.css
git commit -m "feat(fe): bottone 'segna come risolta' lato operatore [IF-OP.08]"
```

---

### Task 7: Frontend utente — badge "Risolta" nello storico

**Files:**
- Modify: `frontend/src/views/utente/VistaSegnalazione.tsx:7-15`
- Modify: `frontend/src/views/utente/VistaSegnalazione.css` (nuova classe badge)

**Interfaces:**
- Consumes: tipo `Segnalazione.stato` estesa (Task 5); nessuna nuova funzione richiamata (lo storico già esistente in `caricaStorico()` riceve il campo `stato` aggiornato dal backend).

- [ ] **Step 1: Estendere `STATO_LABEL` e `STATO_CLASS`**

In `frontend/src/views/utente/VistaSegnalazione.tsx`, sostituire:

```typescript
const STATO_LABEL: Record<string, string> = {
  aperta: 'Aperta',
  in_carico: 'In carico',
}

const STATO_CLASS: Record<string, string> = {
  aperta: 'segn-badge--aperta',
  in_carico: 'segn-badge--in-carico',
}
```

con:

```typescript
const STATO_LABEL: Record<string, string> = {
  aperta: 'Aperta',
  in_carico: 'In carico',
  risolta: 'Risolta',
}

const STATO_CLASS: Record<string, string> = {
  aperta: 'segn-badge--aperta',
  in_carico: 'segn-badge--in-carico',
  risolta: 'segn-badge--risolta',
}
```

- [ ] **Step 2: Aggiungere lo stile del badge**

In `frontend/src/views/utente/VistaSegnalazione.css`, individuare la regola `.segn-badge--in-carico` e aggiungere subito dopo, replicando la stessa struttura di proprietà con colori diversi:

```css
.segn-badge--risolta {
  background-color: #dcfce7;
  color: #15803d;
}
```

- [ ] **Step 3: Verifica manuale**

Run: `cd frontend && npm run dev` (se non già avviato dal Task 6). Nel browser: login come l'utente che ha la segnalazione risolta nel Task 6 → vai su "Le mie segnalazioni" → il badge della segnalazione mostra "Risolta".

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/utente/VistaSegnalazione.tsx frontend/src/views/utente/VistaSegnalazione.css
git commit -m "feat(fe): badge 'Risolta' nello storico segnalazioni utente [IF-OP.08]"
```

---

### Task 8: Aggiornamento documentazione sprint

**Files:**
- Modify: `docs/Sprintn3.md` (sezione caso d'uso IF-OP.08 — Gestisce Segnalazione)

**Interfaces:** nessuna (solo documentazione).

- [ ] **Step 1: Localizzare la sezione IF-OP.08 in `docs/Sprintn3.md`**

Cercare il caso d'uso "Gestisce Segnalazione" / IF-OP.08.

- [ ] **Step 2: Aggiungere lo scenario alternativo "Segna come risolta"**

Aggiungere, nella stessa struttura degli altri scenari già documentati per questo caso d'uso (scenario base "Prendi in carico"), un nuovo paragrafo:

```markdown
**Scenario alternativo — Segna come risolta:**
Precondizione: la segnalazione è nello stato `in_carico`.
1. L'operatore apre il dettaglio di una segnalazione presa in carico.
2. L'operatore preme "SEGNA COME RISOLTA".
3. Il sistema aggiorna lo stato a `risolta`.
4. L'utente, accedendo al proprio storico segnalazioni, vede lo stato "Risolta".

Eccezione: se la segnalazione non è nello stato `in_carico` (es. è ancora `aperta`), il sistema rifiuta la transizione (HTTP 422).
```

- [ ] **Step 3: Commit**

```bash
git add docs/Sprintn3.md
git commit -m "docs: aggiorna caso d'uso IF-OP.08 con scenario 'risolvi segnalazione'"
```

---

## Note finali per chi esegue il piano

Dopo il Task 8, segnalare all'utente che il **Diagramma delle Classi** e i **diagrammi di sequenza** in `docs/Diagrammi/` vanno aggiornati a mano (non generabili automaticamente da questo plan):
- Diagramma Classi: nessuna nuova classe/attributo — `StatoSegnalazione` è un enum di valore, non sempre rappresentato esplicitamente nei diagrammi UML a meno che non lo sia già per `aperta`/`in_carico`. Verificare se il diagramma elenca i valori dell'enum per `Segnalazione.stato` e, se sì, aggiungere `risolta`.
- Diagramma di sequenza IF-OP.08: aggiungere un nuovo riquadro/alt per il flusso "Operatore segna come risolta" (Operatore → SegnalazioneOPController → ServizioSegnalazione → SegnalazioneRepository → DB), analogo a quello già presente per "Prendi in carico".
