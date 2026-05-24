# Architettura dei Componenti - SMART MOBILITY SYSTEM

Questo documento descrive l'architettura a componenti del sistema "Smart Mobility System". Il diagramma illustra un'architettura distribuita basata su livelli (Client, Server, Database, Servizi Esterni) e definisce chiaramente i raggruppamenti logici dei moduli e le interfacce di comunicazione tra di essi.

---

## 1. Livello CLIENT (Frontend)
Il componente Client racchiude l'intera applicazione lato utente/operatore ed è strutturato internamente in due sottolivelli principali: la UI (View) e i servizi di integrazione (API Service Layer).

### 1.1 Sottocomponente: View
Contiene i moduli visivi (interfacce grafiche) suddivisi per tipologia di attore:
* **VistaAuth:** Contiene `VistaLogin`.
* **VistaUtente:** Contiene `VistaHomePageUtente`, `VistaPrenotazioneMezzo`, `VistaCronologiaCorse`, `VistaCorsa`.
* **VistaOperatore:** Contiene `VistaDashboardOperatore`, `VistaTariffePromozioni`, `VistaMezziOperatore`, `VistaImpostazioniRegole`, `VistaDefinisciZona`.
* **VistaAmministrazionePubblica:** Contiene `VistaDashboardAP`.

### 1.2 Sottocomponente: API Service Layer (Frontend)
Gestisce la logica lato client e le chiamate di rete verso il backend.
* **Moduli Servizio Client:** `ApiService`, `AuthService`, `MapService`, `PaymentService`, `ZonaService`, `FlottaService`, `ReportService`, `PrenotazioneService`.

---

## 2. Livello SERVER (Backend)
Il Server è suddiviso rigidamente in quattro livelli logico-architetturali, che gestiscono il ciclo di vita della richiesta dalla ricezione fino alla persistenza.

### 2.1 Sottocomponente: CONTROLLER
Gestisce l'instradamento delle richieste HTTP in ingresso e raggruppa i controller per area di competenza:
* **AuthController:** Contiene `LoginController`.
* **UtenteController:** Contiene `PrenotazioneUtenteController`, `PagamentoController`, `HomePageUtenteController`.
* **OperatoreController:** Contiene `MezzoOperatoreController`, `ZonaOperatoreController`.
* **AmministrazionePubblicaController:** Contiene `ReportAPController`.

### 2.2 Sottocomponente: BUSINESS LOGIC LAYER (BLL)
Contiene i servizi core che implementano le regole di business del dominio.
* **Moduli BLL:** `ServizioMobilità`, `ServizioGIS`, `ServizioUtenti`, `ServizioReport`, `ServizioPricing`, `ServizioPrenotazione`.

### 2.3 Sottocomponente: MODEL
Rappresenta le entità di dominio (Business Objects) manipolate dal sistema.
* **Entità:** `Utente`, `Operatore`, `AmministrazionePubblica`, `Mezzo`, `Corsa`, `Prenotazione`, `Pagamento`, `Tariffa`, `Zona`, `RegoleFineCorsa`.

### 2.4 Sottocomponente: DATA ACCESS LAYER (DAL)
Gestisce l'astrazione per l'accesso ai dati (pattern Repository).
* **Moduli Repository:** `AttoreRepository`, `MezzoRepository`, `CorsaRepository`, `PagamentoRepository`, `ZonaRepository`, `PrenotazioneRepository`, `TariffaRepository`, `RegoleFineCorsaRepository`.

---

## 3. Infrastruttura e Servizi Esterni

### 3.1 DATABASE
* **DBMS:** Il sistema di gestione del database relazionale/non relazionale, che comunica direttamente con il DAL.

### 3.2 SERVIZI ESTERNI
Sistemi di terze parti integrati nel flusso del Server:
* **ProviderPagamenti:** Gestisce l'autorizzazione e la validazione dei pagamenti.
* **GoogleMaps:** Fornisce i dati cartografici e i servizi di geocoding/geofencing.

---

## 4. Interfacce e Porte (Contratti di Comunicazione)
I componenti comunicano esclusivamente tramite interfacce ben definite (porte fornite/richieste):

* **`APIToView`**: Collega internamente le View del Client ai propri servizi Frontend (API Service Layer).
* **`ClientToServer`** & **`ServerToClient`**: Rete/Contratti API. Permettono all'API Service Layer del Client di comunicare con i Controller del Server (e viceversa per le risposte/notifiche).
* **`BLLToController`**: Interfaccia esposta dal Business Logic Layer e consumata dal Controller.
* **`ModelToBLL`**: Interfaccia che permette al BLL di istanziare, validare e manipolare le entità del Model.
* **`DALToModel`**: Interfaccia utilizzata dal DAL per idratare le entità del Model recuperate dal database.
* **`DALtoDBMS`**: Interfaccia di basso livello per l'esecuzione di query e connessioni al Database.

---

## 5. Mappatura Operazioni (Dettaglio Metodi per Livello)
Il diagramma associa a vari livelli specifici set di operazioni:

### 5.1 Metodi Client (API Service Layer)
* *AuthService:* `.login()`, `.registraUtente()`, `.logout()`
* *MapService:* `.caricaMappa()`, `.cercaMezzi()`
* *PrenotazioneService:* `.prenotaMezzo()`, `.terminaCorsa()`, `.sbloccaMezzo()`
* *PaymentService:* `.effettuaPagamento()`, `.salvaMetodoPagamento()`
* *FlottaService:* `.aggiungiMezzo()`, `.dismetti()`, `.modificaStato()`
* *ZonaService:* `.creaZona()`
* *Gestione Rete Base:* `ApiService.gestisciRisposta()`, `.riceviNotifica()`, `.mostraErroreHTTP()`

### 5.2 Metodi Server (Controller)
* *HomePageUtenteController:* `.login()`, `.registra()`, `.modificaProfilo()`
* *PrenotazioneUtenteController:* `.Prenotazione()`, `.sblocca()`, `.terminaCorsa()`
* *PagamentiController:* `.effettuaPagamento()`
* *MezzoOperatoreController:* `.aggiungiMezzo()`, `.dismetti()`, `.modificaStatoMezzo()`, `.getTariffe()`, `.creatariffa()`, `.salvaRegoleFineCorsa()`
* *ZonaOperatoreController:* `.creaZona()`
* *DashboardOPController:* `.CaricaMappa()`

### 5.3 Metodi Server (Business Logic Layer)
* *ServizioUtenti:* `.registra()`, `.autentica()`, `.modificaProfilo()`
* *ServizioPrenotazione:* `.creaPrenotazione()`, `.verificaDisponibilita()`
* *ServizioMobilità:* `.sbloccaMezzo()`, `.terminaCorsa()`, `.aggiungiMezzo()`, `.dismetti()`, `.modificaStatoMezzo()`, `.verificaPosizione()`, `.getZonaParcheggioeRegole()`, `.salvaRegoleFineCorsa()`
* *ServizioPricing:* `.calcolaImporto()`, `.effettuaPagamento()`, `.definisciTariffa()`
* *ServizioGIS:* `.creaZona()`
* *ServizioReport:* `.generaReport()`, `.esportaCSV()`

### 5.4 Metodi Server (Model)
* *Entity:* `.crea()`, `.aggiorna()`

### 5.5 Metodi Server (DAL & Repository)
* *Generic Repository:* `.save()`, `.update()`, `.delete()`
* *MezzoRepository:* `.findVicini(coordinate, raggio)`
* *PrenotazioneRepository:* `.findAttiva(idUtente)`
* *UtenteRepository:* `.findByEmail(email)`
* *ZonaRepository:* `.findContenenti(coordinate)`

### 5.6 Metodi Database (DBMS)
* *DataSource:* `.connettDB()`, `.executeQuery()`, `.executeUpdate()`

### 5.7 Metodi Servizi Esterni
* *ProviderPagamenti:* `.autorizza()`, `.validaDatiPagamento()`
* *GoogleMaps:* `.recuperaDatiMappa()`, `.verificaZona()`