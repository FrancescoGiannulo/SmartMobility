# Demo movimento mezzi — Design

**Data:** 2026-06-25
**Scopo:** Funzione di presentazione per l'esame. Durante una corsa attiva, l'account demo
avvia con un pulsante il movimento simulato del/i mezzo/i lungo un percorso che attraversa
una zona **limitata**, una zona **vietata** (annidata nella limitata) e infine esce dalla
**zona operativa**. Il movimento è visibile in tempo reale sia dalla **mappa Operatore** sia
dalla schermata **info corsa Utente**, dimostrando geofencing e regola di precedenza
(`vietata > limitata > operativa`).

La funzione è un **helper di presentazione**, ristretto a un singolo account demo; non è una
feature di prodotto per gli utenti finali.

---

## 1. Vincoli e scelte già decise

- **Backend-integrato**: la posizione "vive" nel DB (`mezzi.lat/lng`); le due viste, sessioni
  separate, leggono la stessa verità via polling. Niente sincronizzazione client-side.
- **Driver nel frontend dell'account demo** (non task in background sul backend, fragile su
  Render free): il pulsante avvia un `setInterval` (~2s) che cammina lungo una polilinea e ad
  ogni tick chiama un endpoint che aggiorna la posizione e ritorna lo stato geofencing.
- **Gating via env var**: `DEMO_ACCOUNT_EMAIL` (backend) / `VITE_DEMO_EMAIL` (frontend).
  Nessuna migrazione, nessuna colonna `is_demo`.
- **Account demo**: `demo@smartmobility.it` (UT), già registrato.
- **Zone**: si usano le 21 zone reali già presenti nel DB. Nessun seed di zone.

## 2. Flusso demo (per il presentatore)

1. Login **account demo (UT)** in finestra A; login **OP** in finestra B (mappa operatore).
2. Finestra A: **prenota + sblocca** il/i mezzo/i specifici noti — flusso reale, invariato.
3. A corsa attiva compare il pulsante **▶ "Avvia demo movimento"** (solo per l'account demo).
4. Click → il/i mezzo/i partono lungo la polilinea (~1 punto/2s).
5. Banner nella finestra A e marker in movimento nella finestra B reagiscono in sequenza:
   - ingresso in **"Campus universitario"** (limitata, vmax 15) → banner giallo "Zona a
     velocità limitata — max 15 km/h";
   - ingresso in **"Politecnico"** (vietata, dentro Campus) → banner rosso "Zona vietata"
     (dimostra la **precedenza**: nell'area sovrapposta vince vietata);
   - uscita dalla **zona operativa** → banner ⚠️ "Fuori dalla zona operativa" (già esistente).
6. Fine percorso: termina la corsa → si vede la **penale obbligatoria** zona vietata
   (comportamento già documentato in caso d'uso UT-04).

## 3. Architettura (rispetta i layer)

```
Frontend demo (VistaCorsa)                    Frontend OP (VistaMappaOperatore)
  setInterval ~2s                               polling ~2s su /mappa/mezzi
      │ PATCH posizione {lat,lng}                     │ GET mezzi
      ▼                                               ▼
  Controller (corsa_controller)  ───────────► ServizioMappa (BLL)
      │ valida HTTP + gating demo                 aggiorna posizione
      ▼                                           calcola zona (precedenza) + limite
  ServizioMappa.aggiorna_posizione_demo ──► MezzoRepository.aggiorna_posizione (DAL)
      │                                      ZonaRepository.tipo_zona_del_punto (DAL)
      │                                      NotificaRepository.crea (su vietata / fuori)
      ▼
  ritorna {lat, lng, zona, limite_velocita}  ──► banner finestra A
```

Vincoli architetturali: il Controller fa solo validazione/smistamento; la logica geofencing
sta in `ServizioMappa`; l'accesso DB solo nel DAL. La posizione **non** è uno "stato" del
mezzo (`Disponibile`/`In uso`/...), quindi passa per `ServizioMappa` e **non** per
`ServizioMobilità`.

## 4. Componenti net-new

### DAL
- `MezzoRepository.aggiorna_posizione(mezzo_id, lat, lng) -> None`
  `UPDATE mezzi SET lat=:lat, lng=:lng WHERE id=:id`.
- `ZonaRepository.tipo_zona_del_punto(lat, lng) -> dict | None`
  Una query PostGIS `ST_Within` che ritorna la zona **più restrittiva** che contiene il punto,
  con ordinamento di precedenza `vietata(0) < limitata(1) < operativa(2)`; ritorna
  `{tipo, limite_velocita}` oppure `None` se il punto non è in nessuna zona (= fuori operativa).
  Riusa il pattern di `punto_in_zona_operativa` già presente.

### BLL — `ServizioMappa`
- `aggiorna_posizione_demo(mezzo_id, lat, lng, id_utente, notifica) -> dict`
  1. `mezzo_repo.aggiorna_posizione(...)`;
  2. `zona = zona_repo.tipo_zona_del_punto(lat, lng)`;
  3. determina `stato_zona ∈ {operativa, limitata, vietata, fuori}` (`None` → `fuori`);
  4. se `notifica == True` e `stato_zona ∈ {vietata, fuori}`:
     `NotificaRepository.crea(id_utente, msg)` (vedi §6);
  5. ritorna `{lat, lng, zona: stato_zona, limite_velocita}`.

### Controller — `corsa_controller.py`
- `PATCH /corse/{corsa_id}/demo/posizione`, body `{lat: float, lng: float, notifica: bool}`.
  (`notifica` è `true` solo nel tick di transizione di zona — vedi §6.)
  - **Gating**: l'utente autenticato deve avere email == `DEMO_ACCOUNT_EMAIL` ed essere il
    proprietario della corsa attiva indicata; altrimenti `403`. Per ogni altro utente
    l'endpoint non opera.
  - Ricava il `mezzo_id` dalla corsa, delega a `ServizioMappa.aggiorna_posizione_demo`,
    risponde con lo schema geofencing.
- Schema Pydantic `PosizioneDemoOut { lat, lng, zona, limite_velocita }` in `schemas.py`.

### Frontend
- **`CorsaService.ts`**: `aggiornaPosizioneDemo(corsaId, lat, lng) -> Promise<StatoZona>`.
- **`VistaCorsa.tsx`**:
  - Mostra il pulsante **▶ "Avvia demo movimento"** solo se l'utente corrente è l'account demo
    (`VITE_DEMO_EMAIL`) e c'è una corsa attiva.
  - Al click: costruisce la polilinea (vedi §5) dalla posizione attuale del mezzo, poi
    `setInterval(~2s)` che avanza un waypoint per tick e chiama `aggiornaPosizioneDemo`.
  - Aggiorna i banner dallo `zona` ritornato: nuovo banner **limitata** (giallo, con
    `limite_velocita`), nuovo banner **vietata** (rosso); il banner **fuori operativa** già
    esiste e viene pilotato dallo stesso stato (sostituendo il watch GPS durante la demo).
  - A fine polilinea: ferma l'intervallo.
- **`VistaMappaOperatore.tsx`**: aggiunge `setInterval(ricaricaDati, 2000)` (con cleanup) così
  il marker del mezzo si anima. Nessun'altra modifica.

### Config
- `backend/.env(.example)`: `DEMO_ACCOUNT_EMAIL=demo@smartmobility.it`.
- `frontend/.env.local(.example)`: `VITE_DEMO_EMAIL=demo@smartmobility.it`.

## 5. Costruzione della polilinea

Calcolata a runtime lato frontend, indipendente dal mezzo specifico:
`posizione_attuale_mezzo` → waypoint centro **"Campus universitario"** (41.1095, 16.8806) →
waypoint centro **"Politecnico"** (41.1093, 16.8791) → punto **fuori** dalla zona operativa
(verso il bordo esterno, calibrato in implementazione leggendo i vertici reali del poligono
operativo). Tra waypoint si interpolano punti intermedi (~5–10) per un movimento fluido.
I centroidi reali vanno riletti dal DB in fase di implementazione per calibrare i waypoint.

## 6. Note di robustezza

- **Notifica solo al cambio stato (decisione)**: l'endpoint è stateless, quindi il confronto
  con il tick precedente lo fa il **frontend** (conosce lo stato ritornato dal tick precedente)
  e invia `notifica: true` solo sul tick di **transizione** verso `vietata`/`fuori`. Il BLL
  crea la `Notifica` solo se `notifica == true`. Così si riusa l'entità `Notifica` (coerente
  con il pattern del progetto) senza generare decine di notifiche duplicate.
- La demo gira finché la tab dell'account demo è aperta: accettabile per l'esame.

## 7. Tracciabilità

- `IF-OP.01` Visualizza Mappa Operatore (mappa real-time, polling).
- `IF-UT.01` Visualizza Mappa Utente / `IF-UT.08` Visualizza Riepilogo corsa (info corsa).
- Semantica zone: glossario `docs/Sprintn3.md §4.2` (Zona Operativa/Limitata/Vietata) e caso
  d'uso UT-04 (penale zona vietata a fine corsa).
- L'endpoint demo è marcato come helper di presentazione, gated all'account demo.

## 8. Testing

- `ZonaRepository.tipo_zona_del_punto`: punto in operativa pura, in limitata, in vietata
  (annidata → deve vincere vietata), fuori da tutto (→ None). Test di integrazione (PostGIS).
- `ServizioMappa.aggiorna_posizione_demo`: ritorna lo stato corretto per ciascun caso e
  aggiorna la posizione.
- Controller: gating — utente non demo → 403; utente demo non proprietario della corsa → 403.

## 9. Fuori scope (YAGNI)

- Nessuna reazione "fisica" (blocco motore, rallentamento reale): solo segnalazione/banner.
- Nessun task di simulazione lato backend.
- Nessuna nuova classe nel diagramma: si riusano `Mezzo`, `Zona`, `Corsa`, `Notifica`.
- Nessuna modifica al calcolo penale a fine corsa (già esistente).
