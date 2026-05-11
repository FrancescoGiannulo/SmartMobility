# CLAUDE.md — Smart Mobility

## Contesto del progetto

**Smart Mobility** è un sistema software per il Comune di Zootropolis che integra servizi di bike, car e e-scooter sharing in un'unica piattaforma. Il documento di riferimento primario è [`docs/SprintZero.md`](docs/SprintZero.md), che contiene Product Backlog, architettura, glossario e mockup UI.

Tre ruoli utente distinti:
- **UT** — Utente finale (cittadino)
- **OP** — Operatore del Servizio (gestione flotta)
- **AP** — Amministrazione Pubblica (governance e report)

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
- Le **zone AP** (Vietate, Limitate) hanno sempre la precedenza sulle zone OP. Questa regola deve riflettersi in `ServizioGIS` e `ServizioMobilità`.

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
- `Zona` con i sottotipi: `ZonaOperativa`, `ZonaParcheggio`, `ZonaLimitata`, `ZonaVietata`
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
