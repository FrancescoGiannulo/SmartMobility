# Architettura dei Componenti — SMART MOBILITY

> Descrizione testuale di `Diagramma Componenti.drawio` (fonte di verita: il file `.drawio`).
> Architettura distribuita Client-Server a livelli (MVC a tre tier). I componenti white-box
> mostrano le classi contenute; i sistemi esterni sono black-box. I componenti comunicano
> solo tramite interfacce (provided = lollipop / required = dipendenza «use»).

Il diagramma e organizzato in **due macro-componenti** `«component»` — **CLIENT** e **SERVER** —
piu i **sistemi esterni**. Ogni macro-componente contiene i sotto-componenti di layer, e ogni
sotto-componente contiene le classi del rispettivo livello.

---

## 1. Macro-componente CLIENT

### 1.1 `«component» View` (Presentation) — 24 classi
`VistaLogin`, `VistaHomePageUtente`, `VistaCorsa`, `VistaStoricoCorse`, `VistaPagamenti`,
`VistaAbbonamenti`, `VistaSegnalazioneUtente`, `VistaProfiloUtente`, `CallbackOAuth`,
`PrivacyPolicy`, `VistaDefinisciZona`, `VistaMezziOperatore`, `VistaTariffe`,
`VistaImpostazioniRegole`, `VistaParametriSistema`, `VistaSegnalazioniOperatore`,
`VistaGestioneUtentiOperatore`, `VistaDashboardAP`, `VistaReportAP`, `VistaRecensione`,
`VistaOfferte`, `VistaStoricoModifiche`, `VistaRecensioniOperatore`, `VistaDashBoardOperatore`.

### 1.2 `«component» ApiService` (API Service Layer) — 19 classi
`ApiService`, `AuthService`, `MapService`, `CorsaService`, `PrenotazioneService`,
`PaymentService`, `AbbonamentoService`, `OffertaService`, `FlottaService`, `TariffaService`,
`ZonaService`, `SegnalazioneService`, `ConfigurazioneService`, `RegoleFineCorsaService`,
`ReportService`, `GestioneUtentiService`, `RecensioneService`, `SuggerimentiService`,
`StoricoModificheService`.

`ApiService` e la **Facade** verso il server; i service di dominio traducono le operazioni del
proprio dominio in chiamate ad `ApiService`. Le View consumano i service tramite l'interfaccia
`ApiToView`.

---

## 2. Macro-componente SERVER

### 2.1 `«component» Controller` (MVC / FrontController) — 19 classi
`FrontController`, `AccountController`, `HomePageUtenteController`, `CorsaController`,
`PagamentoController`, `AbbonamentoController`, `MezzoOperatoreController`, `ZoneController`,
`RegoleFineCorsaController`, `OffertaController`, `ConfigurazioneController`,
`SegnalazioneUtenteController`, `SegnalazioneOPController`, `UtentiOPController`,
`AmministrazionePubblicaController`, `RecensioneController`, `SuggerimentoController`,
`TariffaController`, `StoricoModificheController`.

### 2.2 `«component» BLL` (Business Logic Layer) — 16 servizi
`ServizioMobilita`, `ServizioPrenotazione`, `ServizioPricing`, `ServizioMappa`,
`ServizioAbbonamento`, `ServizioOfferta`, `ServizioSegnalazione`, `ServizioParametri`,
`ServizioRegoleFineCorsa`, `ServizioReport`, `ServizioUtenti`, `ServizioRecensione`,
`ServizioSuggerimenti`, `ServizioTariffa`, `ServizioNotifica`, `ServizioStoricoModifiche`.

Espone al Controller l'interfaccia `BLLToController` (realizzazione delle `IServizio*` del
diagramma delle classi). Lo stato del `Mezzo` cambia solo tramite `ServizioMobilita`
(pattern State); il calcolo tariffa usa il pattern Strategy (IIN-4).

### 2.3 `«component» DAL` (Repository) — 20 classi
`MezzoRepository`, `CorsaRepository`, `PrenotazioneRepository`, `PagamentoRepository`,
`TariffaRepository`, `ZonaRepository`, `UtenteRepository`, `OperatoreRepository`,
`AttoreRepository`, `AbbonamentoRepository`, `OffertaRepository`, `PromozioneRepository`,
`RegoleFineCorsaRepository`, `ParametriSistemaRepository`, `SegnalazioneRepository`,
`IRepository`, `RecensioneRepository`, `SuggerimentoRepository`, `NotificaRepository`,
`StoricoModificheRepository`.

I repository sono l'unico livello che conosce le entita ORM e convertono ORM <-> Transfer Object
verso la BLL (pattern DAO + Transfer Object). La BLL non importa mai dal Model.

### 2.4 `«component» Model` (Domain / Entity) — 22 classi
`Persona`, `Utente`, `Operatore`, `AmministrazionePubblica`, `Mezzo`, `Corsa`, `Prenotazione`,
`Pagamento`, `MetodoPagamento`, `Tariffa`, `Zona`, `Offerta`, `Promozione`, `Abbonamento`,
`AbbonamentoUtente`, `RegolaFineCorsa`, `ParametriSistema`, `Segnalazione`, `Recensione`,
`Suggerimento`, `Notifica`, `StoricoModifiche`.

---

## 3. Sistemi esterni (black-box)

- `«component» DBMS — Supabase PostgreSQL` — persistenza relazionale (PostgreSQL + PostGIS).
- `«component» GoogleMaps (Adapter)` — dati cartografici, geocoding/geofencing.
- `«component» Provider Pagamenti (Adapter)` — autorizzazione e validazione pagamenti.
- `«component» ServizioAI (Adapter)` — generazione dei suggerimenti intelligenti (IF-UT.14).

Non se ne mostra il contenuto (componenti black-box/grey-box).

---

## 4. Interfacce (provided = lollipop · required = dipendenza «use»)

| Interfaccia | Fornita da (provided) | Richiesta da (required) | Operazioni esposte (annotazioni) |
|---|---|---|---|
| `ApiToView` | ApiService | View | `AuthService.login()`, `CorsaService.sblocca()`, `PaymentService.effettuaPagamento()`, `MapService.caricaMappa()`, `PrenotazioneService.creaPrenotazione()`, `AbbonamentoService.sottoscrivi()`, `ZonaService.creaZona()`, `FlottaService.aggiungiMezzo()`, `SegnalazioneService.inviaSegnalazione()`, `OffertaService.creaOfferta()` |
| `ClientToServer` | Controller | ApiService | REST/HTTPS: `POST /auth/login`, `GET /utente/mezzi/sbloccabili`, `POST /utente/prenotazioni`, `POST /utente/corse/{id}/termina`, `POST /utente/abbonamenti/{offerta_id}`, `POST /operatore/zone`, `POST /operatore/mezzi`, `POST /utente/segnalazioni`, `POST /operatore/offerte` |
| `BLLToController` (= `IServizio*`) | BLL | Controller | `IServizioMobilita.sbloccaMezzi()`, `IServizioPricing.effettuaPagamento()`, `IServizioPrenotazione.creaPrenotazioni()`, `IServizioMappa.creaZona()`, `IServizioAbbonamento.sottoscrivi()`, `IServizioSegnalazione.creaSegnalazione()`, `IServizioOfferta.creaOfferta()`, `IServizioMobilita.aggiungiMezzo()` |
| `Repository` | DAL | BLL | `IRepository.save() / update() / delete() / findById()` |
| `DALtoDBMS` | DBMS | DAL | `executeQuery()`, `executeUpdate()`, `connectDB()` |
| `BLLtoGoogleMaps` | GoogleMaps | BLL (`ServizioMappa`) | `recuperaDatiMappa()`, `verificaZona()` |
| `BLLtoProviderPagamenti` | Provider Pagamenti | BLL (`ServizioPricing`) | `autorizza()`, `validaDatiPagamento()` |
| `BLLtoServizioAI` | ServizioAI | BLL (`ServizioSuggerimenti`) | `generaSuggerimenti()` |

**Flusso delle dipendenze:**
`View -> ApiService -> (ClientToServer, REST/HTTPS) -> Controller -> BLL -> DAL -> Model`,
con `DAL -> DBMS`, `ServizioMappa -> GoogleMaps`, `ServizioPricing -> Provider Pagamenti`,
`ServizioSuggerimenti -> ServizioAI`.

---

## 5. Note di consistenza

- **Componenti <-> Classi:** verificato l'allineamento per ogni layer
  (View 24, ApiService 19, Controller 19, BLL 16, DAL 20, Model 22). Le `IServizio*` del
  diagramma delle classi sono rese nel diagramma dei componenti come l'interfaccia provided
  `BLLToController`.
- **Meccanismo di notifica (2026-06-21):** `ServizioNotifica` (BLL), `NotificaRepository` (DAL) e
  `Notifica` (Model) erano gia presenti nel diagramma delle classi (usati da `ServizioSegnalazione`
  e `ServizioUtenti` per notificare l'Utente) ma non erano ancora stati riportati nel diagramma dei
  componenti — aggiunti ora per coerenza.
- **Split Tariffa/Offerta (2026-06-20):** `VistaTariffeOfferte` era troppo ampia (due flussi
  indipendenti) ed e stata separata in `VistaTariffe` + `VistaOfferte`; analogamente e stato
  estratto `TariffaService` da `FlottaService`, `TariffaController` da `MezzoOperatoreController`
  e `ServizioTariffa` da `ServizioPricing`, per simmetria con la catena gia esistente
  `OffertaService -> OffertaController -> ServizioOfferta`. Vedi `docs/CoerenzaDiagrammaClassi.md`
  per il dettaglio dei file coinvolti.
- **Feature `Suggerimenti Intelligenti` (IF-UT.14):** aggiunta in tutti i layer del diagramma
  (`SuggerimentiService`, `SuggerimentoController`, `ServizioSuggerimenti`, `SuggerimentoRepository`,
  `Suggerimento`) piu il sistema esterno `ServizioAI (Adapter)` consumato da `ServizioSuggerimenti`
  tramite l'interfaccia `BLLtoServizioAI`. La View e riusata (`VistaHomePageUtente`).
- **Feature `Recensione` (IF-UT.15, implementata 2026-06-21):** presente in tutti i layer del
  diagramma (View, Service, Controller, BLL, DAL, Model) ed **ora implementata nel codice**
  seguendo esattamente lo slice gia modellato qui (`VistaRecensione`, `RecensioneService`,
  `RecensioneController`, `ServizioRecensione`, `RecensioneRepository`, `Recensione`). Diagramma e
  codice sono allineati.
- **Feature `Mostra Storico Modifiche` (IF-OP.13, 2026-06-22):** aggiunta in tutti i layer del
  diagramma dei componenti (`VistaStoricoModifiche`, `StoricoModificheService`,
  `StoricoModificheController`, `ServizioStoricoModifiche`, `StoricoModificheRepository`,
  `StoricoModifiche`), in linea con lo slice gia presente nel diagramma delle classi
  (`IServizioStoricoModifiche` realizzata da `ServizioStoricoModifiche`).
- **Viste Operatore aggiunte (2026-06-24):** `VistaRecensioniOperatore` e `VistaDashBoardOperatore`
  aggiunte al componente View nel `.drawio`, portando il totale a 24 classi.
