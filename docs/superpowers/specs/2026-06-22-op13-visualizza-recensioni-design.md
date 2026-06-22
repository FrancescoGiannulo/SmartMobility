# Design — OP-13 Visualizza Recensioni

**ID Product Backlog:** IF-OP.13 (Sprint 3)
**Data:** 2026-06-22
**Autore:** Francesco

## Obiettivo

Consentire all'Operatore autenticato (ruolo OP) di consultare l'elenco delle
recensioni lasciate dagli utenti (voto 1–5, commento, data) insieme al voto
medio aggregato. Read-side complementare a IF-UT.15 (Scrive Recensione), già
implementato.

## Fonti di verità (aderenza stretta)

- **Use case:** `docs/Sprintn3.md` § OP-13 (scenario base) + OP-13.01
  (NessunaRecensione).
- **Diagramma classi:** `docs/Diagrammi/Diagramma Classi.drawio` →
  `VistaRecensioniOperatore`, `RecensioneService.getRecensioni()`,
  `RecensioneController.getRecensioni()`, `IServizioRecensione`/
  `ServizioRecensione.getRecensioni()`, `RecensioneRepository.findAll()`.
- **Diagramma di sequenza:**
  `docs/Diagrammi/Diagrammi di Sequenza/francesco/Sprint3/visualizza_recensioni.drawio`.

## Stato attuale del codice

Già presente (write-side IF-UT.15):
- `backend/model/recensione.py` — entità `Recensione`.
- `backend/dal/recensione_repository.py` — include già `find_all()`.
- `backend/bll/servizio_recensione.py` — metodi di scrittura.
- `backend/controllers/recensione_controller.py` — router `prefix="/utente"`.
- `backend/controllers/schemas.py` — `RecensioneOut`.
- `backend/migrations/014_recensioni.sql` — tabella `recensioni`.
- `frontend/src/services/RecensioneService.ts` — `scriviRecensione`, `getMieRecensioni`.

Da implementare per OP-13: vedi sotto.

## Decisione architetturale

`GET /operatore/recensioni` viene esposto da un **secondo `APIRouter(prefix="/operatore")`
nello stesso file** `recensione_controller.py`. Mantiene un solo `RecensioneController`
(coerente col diagramma classi, che assegna sia i metodi UT sia `getRecensioni`
alla stessa classe) e riusa il pattern di prefisso già adottato da
`mezzo_operatore_controller.py`.

## Componenti

### Backend

1. **Schema** (`schemas.py`):
   ```python
   class RecensioniOperatoreOut(BaseModel):
       recensioni: list[RecensioneOut]
       voto_medio: float
   ```
   Serializza l'`Object {recensioni, votoMedio}` del diagramma. Si usa
   `voto_medio` (snake_case) per coerenza con tutti gli altri schemi del
   progetto; il frontend lo mappa.

2. **`ServizioRecensione.get_recensioni()`** → `dict`:
   - chiama `self._repo.find_all()`;
   - calcola la media con helper privato `_calcola_voto_medio(lista)`
     (arrotondata a 1 decimale; `0.0` se lista vuota);
   - ritorna `{"recensioni": [...], "voto_medio": x}`.
   - Nessuna eccezione: la lista vuota è il caso OP-13.01, gestito dalla View.
   - `_calcola_voto_medio` è privato perché non compare nel diagramma classi
     (compare solo come self-call `calcolaVotoMedio` nel diagramma di sequenza);
     i metodi privati non sono vincolati dal diagramma classi.

3. **`RecensioneController`** — nuovo router operatore nello stesso file:
   ```python
   router_operatore = APIRouter(prefix="/operatore", tags=["Recensioni"])

   @router_operatore.get("/recensioni", response_model=RecensioniOperatoreOut)
   def get_recensioni(_=Depends(verify_token(["OP"]))):
       # [IF-OP.13] Visualizza Recensioni
       return _servizio.get_recensioni()
   ```

4. **`main.py`**: `app.include_router(recensione_operatore_router)`.

### Frontend

5. **`RecensioneService.ts`**:
   ```ts
   export interface RecensioniOperatore {
     recensioni: Recensione[]
     voto_medio: number
   }
   // [IF-OP.13] Visualizza Recensioni
   export const getRecensioni = (): Promise<{ data: RecensioniOperatore }> =>
     api.get('/operatore/recensioni')
   ```

6. **`VistaRecensioniOperatore.tsx`** (+ `.css`):
   - `apriRecensioni()` — carica i dati al mount (effetto).
   - `mostraRecensioni(recensioni, votoMedio)` — rendering.
   - **alt** (dal diagramma): se `recensioni.length > 0` mostra voto medio +
     lista (voto/stelle, commento, data); altrimenti messaggio "Nessuna
     recensione presente" (OP-13.01).
   - Bottone "Indietro" e stile coerenti con `VistaSegnalazioniOperatore`.

7. **`App.tsx`**: rotta `/operatore/recensioni` protetta `ruoloRichiesto="OP"`.

8. **`VistaMappaOperatore.tsx`**: bottone "Recensioni" nel pannello laterale →
   `navigate('/operatore/recensioni')`.

## Flusso (dal diagramma di sequenza)

```
Operatore → VistaRecensioniOperatore.apriRecensioni()
  → RecensioneService.getRecensioni()
    → ApiService GET /operatore/recensioni (HTTPS + JWT)
      → FrontController.validaAutenticazione(["OP"])  [verify_token]
        → RecensioneController.getRecensioni()
          → ServizioRecensione.getRecensioni()
            → RecensioneRepository.findAll()  → listaRecensioni
            → _calcola_voto_medio(listaRecensioni)
          ← {recensioni, votoMedio}
      ← 200 OK + {recensioni, votoMedio}
  ← mostraRecensioni(...)  |  mostraInfo("Nessuna recensione presente")
```

## Test (`backend/tests/`)

File `test_recensioni_operatore.py`:
- **Base OP-13**: OP autenticato, recensioni in DB → 200, `recensioni` non
  vuoto, `voto_medio` calcolato correttamente.
- **OP-13.01 NessunaRecensione**: nessuna recensione → 200, `recensioni` vuoto,
  `voto_medio == 0.0`.
- **Guardia ruolo (IIN-2)**: utente non-OP → 403.

Test indipendenti, con cleanup delle recensioni inserite (pattern già usato in
`test_recensione.py`).

## Tracciabilità

Tutti i nuovi punti architetturalmente rilevanti commentati `# [IF-OP.13]`.

## Fuori scope

- Paginazione/filtri sulle recensioni (non richiesti dal backlog).
- Modifica del diagramma classi/sequenza (già allineati a questa feature).
- Modifica della migration (tabella `recensioni` già esistente).
