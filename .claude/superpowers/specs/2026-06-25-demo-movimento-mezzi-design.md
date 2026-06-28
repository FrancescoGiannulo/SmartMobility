# Demo movimento mezzi — Design

**Data:** 2026-06-25
**Scopo:** Funzione di presentazione per l'esame. Durante una corsa di gruppo attiva, l'account
demo avvia con un pulsante il movimento simulato dei mezzi sbloccati, che si muovono **in
convoglio** (uno dietro l'altro) lungo un percorso che attraversa una zona **limitata**, una
zona **vietata** (annidata nella limitata) e infine esce dalla **zona operativa**. Il movimento
è visibile in tempo reale sia dalla **mappa Operatore** sia dalla schermata **info corsa
Utente**, dimostrando geofencing e regola di precedenza (`vietata > limitata > operativa`).

La funzione è un **helper di presentazione**, ristretto a un singolo account demo; non è una
feature di prodotto per gli utenti finali.

---

## 1. Vincoli e scelte già decise

- **Backend-integrato sulla posizione**: la posizione "vive" nel DB (`mezzi.lat/lng`,
  `Mezzo.latitudine/longitudine` nel diagramma); le due viste, sessioni separate, leggono la
  stessa verità via polling.
- **Driver nel frontend dell'account demo** (non task in background sul backend, fragile su
  Render free): il pulsante avvia un `setInterval` (~2s) che, per ogni mezzo del gruppo, avanza
  lungo la polilinea e chiama l'endpoint che aggiorna la posizione nel DB.
- **Geofencing calcolato lato client**, riusando gli helper già esistenti in
  `frontend/src/utils/geoUtils.ts` (`puntoInPoligono`, `distanzaDaPoligono`) e le zone già
  caricate dalla VistaCorsa (`getZoneUtente`). Il backend **non** calcola la zona: si limita ad
  aggiornare la posizione. Questo è coerente con ciò che la VistaCorsa già fa oggi per la zona
  operativa.
- **Avviso minimale**: in info corsa compare **solo un piccolo banner** che cambia in base alla
  zona. **Niente** sistema di notifiche frontend, **niente** persistenza di `Notifica` per la
  demo.
- **Gating via env var**: `DEMO_ACCOUNT_EMAIL` (backend) / `VITE_DEMO_EMAIL` (frontend).
  Nessuna migrazione, nessuna colonna `is_demo`.
- **Account demo**: `demo@smartmobility.it` (UT), già registrato.
- **Zone**: si usano le 21 zone reali già presenti nel DB. Nessun seed di zone.

## 2. Flusso demo (per il presentatore)

1. Login **account demo (UT)** in finestra A; login **OP** in finestra B (mappa operatore).
2. Finestra A: **prenota + sblocca N mezzi** (corsa di gruppo) — flusso reale, invariato.
3. A corsa attiva compare il pulsante **▶ "Avvia demo movimento"** (solo per l'account demo).
4. Click → gli N mezzi partono lungo la **stessa polilinea in convoglio**, ognuno sfasato di
   alcuni waypoint rispetto al precedente (~1 punto/2s). Quanti mezzi in fila = quanti sbloccati.
5. Piccolo banner in info corsa (finestra A) e marker in fila in movimento (finestra B)
   reagiscono man mano che il convoglio attraversa le zone:
   - ingresso in **"Campus universitario"** (limitata, vmax 15) → banner giallo "Zona a velocità
     limitata — max 15 km/h";
   - ingresso in **"Politecnico"** (vietata, dentro Campus) → banner rosso "Zona vietata"
     (dimostra la **precedenza**: nell'area sovrapposta vince vietata);
   - uscita dalla **zona operativa** → banner ⚠️ "Fuori dalla zona operativa" (già esistente).
6. Fine percorso: termina la corsa → penale obbligatoria zona vietata (comportamento già
   documentato in caso d'uso UT-04, invariato).

## 3. Architettura (rispetta i layer)

```
Frontend demo (VistaCorsa)                      Frontend OP (VistaMappaOperatore)
  setInterval ~2s, per ogni mezzo:                polling ~2s su /mappa/mezzi
    - calcola waypoint (offset convoglio)              │ GET mezzi
    - calcola zona client-side (geoUtils)              ▼
    - PATCH posizione {lat,lng} ──┐             (marker in fila si muovono)
    - aggiorna piccolo banner     │
                                  ▼
                          Controller (corsa_controller)
                            valida HTTP + gating account demo
                                  ▼
                          ServizioMappa.aggiornaPosizioneMezzo (BLL)
                                  ▼
                          MezzoRepository.aggiorna_posizione (DAL) ──► DB
```

Vincoli: Controller solo validazione/smistamento; aggiornamento posizione in `ServizioMappa`
(servizio geografico, già responsabile di "zone, posizioni, validazione perimetri"); accesso DB
solo nel DAL. La posizione **non** è uno "stato" del mezzo (`Disponibile`/`In uso`/...): non
passa per `ServizioMobilità`.

## 4. Componenti net-new

### DAL — `MezzoRepository`
- `aggiorna_posizione(mezzo_id, lat, lng) -> None`
  `UPDATE mezzi SET lat=:lat, lng=:lng WHERE id=:id`.

### BLL — `ServizioMappa` (+ interfaccia `IServizioMappa`)
- `aggiornaPosizioneMezzo(idMezzo, lat, lng) -> None` (impl. Python `aggiorna_posizione_mezzo`)
  Delega a `MezzoRepository.aggiorna_posizione`. **Nuovo metodo da aggiungere anche al diagramma
  delle classi** (vedi §7).

### Controller — `corsa_controller.py`
- `PATCH /corse/{corsa_id}/demo/posizione`, body `{lat: float, lng: float}`.
  - **Gating**: l'utente autenticato deve avere email == `DEMO_ACCOUNT_EMAIL` ed essere il
    proprietario della corsa indicata; altrimenti `403`. Per ogni altro utente non opera.
  - Ricava il `mezzo_id` dalla corsa, delega a `ServizioMappa.aggiornaPosizioneMezzo`.
    Risponde `204 No Content`.

### Frontend
- **`geoUtils.ts`**: aggiunge una funzione pura
  `zonaCorrente(lat, lng, zone) -> { tipo: 'vietata'|'limitata'|'operativa'|'fuori', limiteVelocita?: number }`
  che applica la precedenza `vietata > limitata > operativa` con `puntoInPoligono` (e
  `distanzaDaPoligono` + margine per "fuori operativa"). Funzione util, non una classe di dominio.
- **`CorsaService.ts`**: `aggiornaPosizioneDemo(corsaId, lat, lng) -> Promise<void>`.
- **`VistaCorsa.tsx`** (dentro `mostraInfoCorsa`, niente nuovi metodi di dominio):
  - Pulsante **▶ "Avvia demo movimento"** mostrato solo se l'utente corrente è l'account demo
    (`VITE_DEMO_EMAIL`) e c'è una corsa di gruppo attiva.
  - Al click costruisce **una** polilinea condivisa (§5). Ad ogni tick, per ogni corsa/mezzo del
    gruppo `i`: indice = `tick - i*LAG` (clamp a 0, fermo a fine percorso), calcola il waypoint,
    chiama `aggiornaPosizioneDemo(corse[i].corsa_id, lat, lng)`.
  - Calcola lo **stato zona aggregato** = zona più restrittiva occupata da un qualsiasi mezzo
    (via `zonaCorrente` client-side) e aggiorna il **piccolo banner**: limitata (giallo, con
    `limiteVelocita`), vietata (rosso), fuori operativa (già esistente). Durante la demo il
    banner è pilotato da questo stato, non dal watch GPS.
  - A fine polilinea (tutti i mezzi arrivati) ferma l'intervallo.
- **`VistaMappaOperatore.tsx`**: aggiunge `setInterval(ricaricaDati, 2000)` (con cleanup) così i
  marker dei mezzi si animano in fila. Nessun'altra modifica.

### Config
- `backend/.env(.example)`: `DEMO_ACCOUNT_EMAIL=demo@smartmobility.it`.
- `frontend/.env.local(.example)`: `VITE_DEMO_EMAIL=demo@smartmobility.it`.

## 5. Costruzione della polilinea

**Una sola** polilinea condivisa dal convoglio, calcolata a runtime lato frontend:
`posizione_capofila` → waypoint centro **"Campus universitario"** (41.1095, 16.8806) → waypoint
centro **"Politecnico"** (41.1093, 16.8791) → punto **fuori** dalla zona operativa (verso il
bordo esterno, calibrato in implementazione leggendo i vertici reali del poligono operativo).
Tra waypoint si interpolano punti intermedi (~5–10) per un movimento fluido. I mezzi seguono la
**stessa** sequenza, ciascuno sfasato di `LAG` waypoint (default 2) rispetto al precedente, così
restano in fila. La posizione di partenza è quella del mezzo capofila; i centroidi reali vanno
riletti dal DB in implementazione per calibrare i waypoint.

## 6. Coerenza con il Diagramma delle Classi

- **Nessuna nuova classe/entità.** Si riusano `Mezzo`, `Zona`, `Corsa`, `ServizioMappa`,
  `MezzoRepository`, e la View `VistaCorsa` (il banner è parte di `mostraInfoCorsa`).
- **Una sola aggiunta di dominio**: il metodo `aggiornaPosizioneMezzo(idMezzo, lat, lng)` su
  `IServizioMappa`/`ServizioMappa`. Va riflesso nel diagramma sorgente
  `docs/Diagrammi/Diagramma Classi.drawio` e nel suo export `docs/Diagrammi/DiagrammaClassi.md`
  (Definition of Done).
- `MezzoRepository.aggiorna_posizione` rientra nel contratto repository esistente (CRUD su
  `Mezzo`), in analogia a `aggiorna_stato`: non introduce nuove interfacce.
- La funzione `zonaCorrente` in `geoUtils.ts` è una utility di presentazione (come gli helper
  già presenti), non una classe del diagramma.
- Il pulsante/driver demo in `VistaCorsa` è un helper di presentazione interno: non aggiunge
  metodi di dominio alla View nel diagramma.

## 7. Tracciabilità

- `IF-OP.01` Visualizza Mappa Operatore (mappa real-time, polling).
- `IF-UT.01` Visualizza Mappa Utente / `IF-UT.08` Visualizza Riepilogo corsa (info corsa).
- Semantica zone: glossario `docs/Sprintn3.md §4.2` (Zona Operativa/Limitata/Vietata) e caso
  d'uso UT-04 (penale zona vietata a fine corsa).
- L'endpoint demo è marcato come helper di presentazione, gated all'account demo.

## 8. Testing

- `ServizioMappa.aggiornaPosizioneMezzo`: aggiorna effettivamente `lat/lng` del mezzo
  (integrazione su DB).
- Controller `PATCH /corse/{corsa_id}/demo/posizione`: utente non demo → 403; utente demo non
  proprietario della corsa → 403; utente demo proprietario → 204 e posizione aggiornata.
- `geoUtils.zonaCorrente` (unit, frontend): punto in operativa pura → `operativa`; in limitata →
  `limitata` con `limiteVelocita`; in vietata annidata → `vietata` (precedenza); fuori da tutto
  → `fuori`.

## 9. Fuori scope (YAGNI)

- Nessuna reazione "fisica" (blocco motore, rallentamento reale): solo il piccolo banner.
- Nessun task di simulazione lato backend.
- Nessuna notifica frontend e nessuna persistenza di `Notifica` per la demo.
- Nessuna modifica al calcolo penale a fine corsa (già esistente).
