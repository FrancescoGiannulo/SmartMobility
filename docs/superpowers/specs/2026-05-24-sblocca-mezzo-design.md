# Design — Sblocca Mezzo (IF-UT.04)

**Data:** 2026-05-24  
**Branch:** feature/corsa  
**Item backlog:** IF-UT.04  
**Caso d'uso:** CS-10 (SprintUno.md)  
**Diagramma di sequenza:** `docs/Diagrammi/Diagrammi di Sequenza/sequence_sblocca_mezzo.drawio`  
**Mockup:** `docs/mockup/8.png` (IUI-8)

---

## 1. Riepilogo

L'utente autenticato sblocca un mezzo dalla mappa. Il mezzo deve essere in stato `Disponibile` (sblocco diretto) oppure `Prenotato` dall'utente corrente (sblocco da prenotazione). Il sistema crea una `Corsa`, aggiorna lo stato del mezzo a `In uso` e mostra la schermata info corsa (IUI-8).

---

## 2. Backend

### 2.1 Endpoint

```
POST /utente/mezzi/{mezzo_id}/sblocca
Authorization: Bearer <JWT>
Ruolo richiesto: UT
```

**Risposta 201 Created:**
```json
{
  "id": "<uuid>",
  "mezzo_id": "<uuid>",
  "utente_id": "<uuid>",
  "stato": "in_uso",
  "inizio_at": "<ISO8601>"
}
```

**Risposta 409 Conflict:** mezzo non disponibile per l'utente  
**Risposta 404 Not Found:** mezzo inesistente

### 2.2 DAL — `MezzoRepository`

Aggiunge (se non già presenti):
- `trova_per_id(id: UUID, db: Session) -> Mezzo | None`
- `aggiorna_stato(mezzo: Mezzo, db: Session) -> None`

### 2.3 DAL — `CorsaRepository`

Implementa:
- `crea(corsa: Corsa, db: Session) -> Corsa` — persiste la corsa e ritorna l'oggetto con `id` assegnato

### 2.4 DAL — `PrenotazioneRepository`

Implementa:
- `trova_attiva_per_utente_e_mezzo(utente_id: UUID, mezzo_id: UUID, db: Session) -> Prenotazione | None`

### 2.5 BLL — `ServizioMobilita`

Metodo: `sblocca_mezzo(mezzo_id: UUID, utente_id: UUID, db: Session) -> Corsa`

Logica (fedele al diagramma di sequenza):
1. `MezzoRepository.trova_per_id(mezzo_id)` → mezzo; se `None` → `MezzoNonTrovatoException`
2. Valuta condizione `[mezzo disponibile per l'utente]`:
   - `mezzo.stato == Disponibile` → ok, sblocco diretto
   - `mezzo.stato == Prenotato` → `PrenotazioneRepository.trova_attiva_per_utente_e_mezzo(utente_id, mezzo_id)`: se trovata → ok, sblocco da prenotazione; se non trovata → `MezzoNonDisponibileException`
   - qualsiasi altro stato → `MezzoNonDisponibileException`
3. Crea `Corsa(mezzo_id=mezzo_id, utente_id=utente_id, inizio_at=now(), stato=in_uso)`
4. `CorsaRepository.crea(corsa)` → corsa persistita
5. Se sblocco da prenotazione: `prenotazione.stato = convertita` → `PrenotazioneRepository.aggiorna(prenotazione)`
6. `mezzo.stato = In uso` → `MezzoRepository.aggiorna_stato(mezzo)`
7. Ritorna `corsa`

### 2.6 Controller — `PrenotazioneUtenteController`

```python
# [IF-UT.04] Sblocca Mezzo
@router.post("/mezzi/{mezzo_id}/sblocca", status_code=201)
def sblocca_mezzo(mezzo_id: UUID, utente=Depends(verify_token(["UT"])), db=Depends(get_db)):
    ...
```

- Chiama `ServizioMobilita().sblocca_mezzo(mezzo_id, utente["id"], db)`
- `MezzoNonTrovatoException` → `404`
- `MezzoNonDisponibileException` → `409`

---

## 3. Frontend

### 3.1 `CorsaService.ts` (nuovo)

```typescript
// [IF-UT.04] Sblocca Mezzo
export const sbloccaMezzo = (mezzoId: string) =>
  api.post(`/utente/mezzi/${mezzoId}/sblocca`)
```

### 3.2 `VistaMappa.tsx` — modifica

Aggiunge `onClick` su `AdvancedMarker`: naviga a `/utente/corsa/:idMezzo` passando i dati del mezzo via `state` React Router.

### 3.3 `VistaCorsa.tsx` (nuovo, `views/utente/`)

Due stati interni (`pre_sblocco` | `attiva`):

**Stato `pre_sblocco`** (navigazione dalla mappa):
- Mostra: tipo mezzo, codice, batteria
- Pulsante **SBLOCCA** → chiama `sbloccaMezzo(idMezzo)`
  - Successo → transizione a `attiva` con dati corsa
  - Errore 409 → mostra messaggio "Mezzo non più disponibile"

**Stato `attiva`** (dopo sblocco):
- Mostra: ID mezzo, batteria, timer elapsed, km (placeholder 0)
- Pulsanti **PAUSA CORSA** e **TERMINA E PAGA** (placeholder per sprint successivi)

### 3.4 `App.tsx` — modifica

```tsx
<Route path="/utente/corsa/:idMezzo"
  element={<RoutaProtetta ruoloRichiesto="UT"><VistaCorsa /></RoutaProtetta>}
/>
```

---

## 4. Test

File: `backend/tests/test_sblocca_mezzo.py`  
Pattern: `TestClient` FastAPI + fixture `supa`/`db` su Supabase reale (stesso pattern di `test_auth.py`).

| Test | Setup | Atteso |
|------|-------|--------|
| sblocco diretto | mezzo `Disponibile` + JWT utente | `201`, corsa in DB, mezzo `In uso` |
| sblocco da prenotazione | mezzo `Prenotato` + prenotazione attiva utente | `201`, corsa in DB, prenotazione `convertita` |
| CS-10.1 mezzo non disponibile | mezzo `In uso` | `409 Conflict` |
| CS-10.1 prenotazione altrui | mezzo `Prenotato` da altro utente | `409 Conflict` |
| mezzo inesistente | UUID casuale | `404 Not Found` |

Ogni test esegue teardown: elimina corse, prenotazioni e mezzi creati durante il test.

---

## 5. Tracciabilità

| Componente | Item |
|------------|------|
| `POST /utente/mezzi/{id}/sblocca` | IF-UT.04 |
| `ServizioMobilita.sblocca_mezzo` | CS-10 scenario base |
| `MezzoNonDisponibileException` | CS-10.1 |
| `VistaCorsa` | IUI-8 |
| `VistaMappa` onClick | IF-UT.04 punto di ingresso |
