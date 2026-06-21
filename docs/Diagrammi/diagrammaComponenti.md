# Architettura dei Componenti — SMART MOBILITY

> Descrizione testuale di `Diagramma Componenti.drawio` (fonte di verità: il file `.drawio`).
> Architettura distribuita Client-Server a livelli (MVC a tre tier). I componenti white-box
> mostrano le classi contenute; i sistemi esterni sono black-box. I componenti comunicano
> solo tramite interfacce (provided = lollipop / required = dipendenza «use»).

Il diagramma è organizzato in **due macro-componenti** `«component»` — **CLIENT** e **SERVER** —
più i **sistemi esterni**. Ogni macro-componente contiene i sotto-componenti di layer, e ogni
sotto-componente contiene le classi del rispettivo livello.

---

## 1. Macro-componente CLIENT

### 1.1 `«component» View` (Presentation) — 21 classi
`VistaLogin`, `VistaHomePageUtente`, `VistaCorsa`, `VistaStoricoCorse`, `VistaPagamenti`,
`VistaAbbonamenti`, `VistaSegnalazioneUtente`, `VistaProfiloUtente`, `CallbackOAuth`,
`PrivacyPolicy`, `VistaDefinisciZona`, `VistaMezziOperatore`, `VistaTariffe`, `VistaOfferte`,
`VistaImpostazioniRegole`, `VistaParametriSistema`, `VistaSegnalazioniOperatore`,
`VistaGestioneUtentiOperatore`, `VistaDashboardAP`, `VistaReportAP`, `VistaRecensione`.

### 1.2 `«component» ApiService` (API Service Layer) — 18 classi
`ApiService`, `AuthService`, `MapService`, `CorsaService`, `PrenotazioneService`,
`PaymentService`, `AbbonamentoService`, `OffertaService`, `FlottaService`, `TariffaService`,
`ZonaService`, `SegnalazioneService`, `ConfigurazioneService`, `RegoleFineCorsaService`,
`ReportService`, `GestioneUtentiService`, `RecensioneService`, `SuggerimentiService`.

`ApiService` è la **Facade** verso il server; i service di dominio traducono le operazioni del
proprio dominio in chiamate ad `ApiService`. Le View consumano i service tramite l'interfaccia
`ApiToView`.

---

## 2. Macro-componente SERVER

### 2.1 `«component» Controller` (MVC / FrontController) — 18 classi
`FrontController`, `AccountController`, `HomePageUtenteController`, `CorsaController`,
`PagamentoController`, `AbbonamentoController`, `MezzoOperatoreController`, `TariffaController`,
`ZoneController`, `RegoleFineCorsaController`, `OffertaController`, `ConfigurazioneController`,
`SegnalazioneUtenteController`, `SegnalazioneOPController`, `UtentiOPController`,
`AmministrazionePubblicaController`, `RecensioneController`, `SuggerimentoController`.

### 2.2 `«component» BLL` (Business Logic Layer) — 14 servizi
`ServizioMobilita`, `ServizioPrenotazione`, `ServizioPricing`, `ServizioTariffa`, `ServizioMappa`,
`ServizioAbbonamento`, `ServizioOfferta`, `ServizioSegnalazione`, `ServizioParametri`,
`ServizioRegoleFineCorsa`, `ServizioReport`, `ServizioUtenti`, `ServizioRecensione`,
`ServizioSuggerimenti`.

Espone al Controller l'interfaccia `BLLToController` (realizzazione delle `IServizio*` del
diagramma delle classi). Lo stato del `Mezzo` cambia solo tramite `ServizioMobilita`
(pattern State); il calcolo tariffa usa il pattern Strategy (IIN-4).

### 2.3 `«component» DAL` (Repository) — 18 classi
`MezzoRepository`, `CorsaRepository`, `PrenotazioneRepository`, `PagamentoRepository`,
`TariffaRepository`, `ZonaRepository`, `UtenteRepository`, `OperatoreRepository`,
`AttoreRepository`, `AbbonamentoRepository`, `OffertaRepository`, `PromozioneRepository`,
`RegoleFineCorsaRepository`, `ParametriSistemaRepository`, `SegnalazioneRepository`,
`RecensioneRepository`, `IRepository`, `SuggerimentoRepository`.

I repository sono l'unico livello che conosce le entità ORM e convertono ORM ↔ Transfer Object
verso la BLL (pattern DAO + Transfer Object). La BLL non importa mai dal Model.

### 2.4 `«component» Model` (Domain / Entity) — 20 classi
`Persona`, `Utente`, `Operatore`, `AmministrazionePubblica`, `Mezzo`, `Corsa`, `Prenotazione`,
`Pagamento`, `MetodoPagamento`, `Tariffa`, `Zona`, `Offerta`, `Promozione`, `Abbonamento`,
`AbbonamentoUtente`, `RegolaFineCorsa`, `ParametriSistema`, `Segnalazione`, `Recensione`,
`Suggerimento`.

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
| `ApiToView` | ApiService | View | `AuthService.login()`, `CorsaService.sblocca()`, `PaymentService.effettuaPagamento()`, `MapService.caricaMappa()` |
| `ClientToServer` | Controller | ApiService | REST/HTTPS: `POST /auth/login`, `GET /utente/mezzi/sbloccabili`, `POST /utente/prenotazioni`, `POST /utente/corse/{id}/termina` |
| `BLLToController` (= `IServizio*`) | BLL | Controller | `IServizioMobilita.sbloccaMezzi()`, `IServizioPricing.effettuaPagamento()`, `IServizioPrenotazione.creaPrenotazioni()`, `IServizioMappa.creaZona()` |
| `Repository` | DAL | BLL | `IRepository.save() / update() / delete() / findById()` |
| `DALtoDBMS` | DBMS | DAL | `executeQuery()`, `executeUpdate()`, `connectDB()` |
| `BLLtoGoogleMaps` | GoogleMaps | BLL (`ServizioMappa`) | `recuperaDatiMappa()`, `verificaZona()` |
| `BLLtoProviderPagamenti` | Provider Pagamenti | BLL (`ServizioPricing`) | `autorizza()`, `validaDatiPagamento()` |
| `BLLtoServizioAI` | ServizioAI | BLL (`ServizioSuggerimenti`) | `generaSuggerimenti()` |

**Flusso delle dipendenze:**
`View → ApiService → (ClientToServer, REST/HTTPS) → Controller → BLL → DAL → Model`,
con `DAL → DBMS`, `ServizioMappa → GoogleMaps`, `ServizioPricing → Provider Pagamenti`,
`ServizioSuggerimenti → ServizioAI`.

---

## 5. Note di consistenza

- **Componenti ↔ Classi:** verificato l'allineamento 1:1 per ogni layer
  (View 21, ApiService 18, Controller 18, BLL 14, DAL 18, Model 20). Le `IServizio*` del
  diagramma delle classi sono rese nel diagramma dei componenti come l'interfaccia provided
  `BLLToController`.
- **Split Tariffa/Offerta (2026-06-20):** `VistaTariffeOfferte` era troppo ampia (due flussi
  indipendenti) ed è stata separata in `VistaTariffe` + `VistaOfferte`; analogamente è stato
  estratto `TariffaService` da `FlottaService`, `TariffaController` da `MezzoOperatoreController`
  e `ServizioTariffa` da `ServizioPricing`, per simmetria con la catena già esistente
  `OffertaService → OffertaController → ServizioOfferta`. Vedi `docs/CoerenzaDiagrammaClassi.md`
  per il dettaglio dei file coinvolti.
- **Feature `Suggerimenti Intelligenti` (IF-UT.14):** aggiunta in tutti i layer del diagramma
  (`SuggerimentiService`, `SuggerimentoController`, `ServizioSuggerimenti`, `SuggerimentoRepository`,
  `Suggerimento`) più il sistema esterno `ServizioAI (Adapter)` consumato da `ServizioSuggerimenti`
  tramite l'interfaccia `BLLtoServizioAI`. La View è riusata (`VistaHomePageUtente`).
- **Feature `Recensione`:** presente in tutti i layer del diagramma (View, Service, Controller,
  BLL, DAL, Model) ma **non ancora implementata nel codice**. È una **feature pianificata**, da
  realizzare in uno sprint successivo seguendo lo slice già modellato: il disallineamento
  diagramma↔codice è quindi atteso. Da tracciare nel Product Backlog con un ID dedicato.
