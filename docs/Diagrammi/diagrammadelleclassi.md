# Documentazione del Diagramma delle Classi

Questo documento descrive la struttura del sistema derivata dal diagramma delle classi caricato. L'architettura segue un pattern **Multi-Tier** distribuito tra **Client** e **Server**, strutturato con pattern MVC (Model-View-Controller) ed entità di persistenza.

---

## ARCHITETTURA DEL CLIENT

Il lato Client è suddiviso in tre macro-livelli: **View** (Interfaccia Utente), **API Service Layer** (Servizi di supporto locali) e le **Interfacce di Comunicazione**.

### 1. View (Interfaccia Utente)

Tutte le viste del sistema ereditano o fanno riferimento a una vista base comune.

#### BaseView `«Abstract»`
* **Metodi:**
    * `+ mostra() : void`
    * `+ nascondi() : void`
    * `+ aggiorna() : void`

#### Area Autenticazione (Login)
* **VistaLogin**
    * `+ mostraFormLogin() : void`
    * `+ mostraFormRegistrazione() : void`
    * `+ mostraRecuperoCredenziali() : void`

#### Area Utente standard (Cittadino / Fruitore del servizio)
* **VistaUtente `«Abstract»`**
    * `+ navigaA(vista : String) : void`
* **VistaHomepageUtente** (Eredita da `VistaUtente`)
    * *Nota: Mostra la mappa principale, i pin e consente lo sblocco.*
    * `+ mostraPin(mezzi : List) : void`
    * `+ mostraZone(zone : List) : void`
    * `+ evidenziaGeofence(zone : List) : void`
    * `+ sbloccaMezzo() : void`
    * `+ avviaCorsaGruppo() : void`
* **VistaCorsaDiGruppo**
    * `+ mostraContatore(att : int, max : int) : void`
    * `+ mostraVeicoli(mezzi : List) : void`
    * `+ aggiungiVeicolo() : void`
* **VistaInfoCorsa**
    * `+ mostraTimer(s : int) : void`
    * `+ mostraDistanza(km : float) : void`
    * `+ pausaCorsa() : void`
    * `+ terminaEPaga() : void`
    * `+ mostraRiepilogo(d : int, km : float, c : float) : void`
* **VistaPrenotazioneMezzo**
    * `+ mostraDettagliMezzo(mezzo : Object) : void`
    * `+ prenota() : void`
    * `+ mostraTempoLimite(min : int) : void`
* **VistaPortafoglio**
    * `+ mostraSaldo(saldo : float) : void`
    * `+ mostraMetodi(metodi : List) : void`
    * `+ aggiungiMetodo() : void`
    * `+ ricaricaSaldo() : void`
* **VistaPianoTariffario**
    * `+ mostraTariffe(tariffe : List) : void`
    * `+ mostraPromozioni(promozioni : List) : void`
* **VistaCronologiaCorse**
    * `+ mostraStorico(corse : List) : void`
* **VistaProfiloUtente**
    * `+ mostraDati(utente : Object) : void`
    * `+ modificaDati() : void`

#### Area Operatore (Gestione Flotta e Manutenzione)
* **VistaOperatore `«Abstract»`**
    * `+ navigaA(sezione : String) : void`
* **VistaDashboardOperatore**
    * `+ mostraMappa(flotta : List) : void`
    * `+ apriGestioneSegnalazioni() : void`
    * `+ apriGestioneUtenti() : void`
    * `+ apriGestioneZoneOperative() : void`
    * `+ apriTariffePromozioni() : void`
    * `+ apriImpostazioniRegole() : void`
    * `+ apriReport() : void`
* **VistaSegnalazioni**
    * `+ mostraSegnalazioni(lista : List) : void`
    * `+ prendiInCarico(id : String) : void`
* **VistaGestioneUtenti**
    * `+ mostraUtenti(lista : List) : void`
    * `+ sospendiAccount(id : String) : void`
* **VistaTariffePromozioni**
    * `+ mostraTariffe(tariffe : List) : void`
    * `+ modificaTariffa(id : String) : void`
    * `+ aggiungiPromozione() : void`
* **VistaImpostazioniRegole**
    * `+ mostraParametri(regole : Object) : void`
    * `+ salvaParametri() : void`

#### Area Amministrazione Pubblica (Regolamentazione del Territorio)
* **VistaAmministrazionePubblica `«Abstract»`**
    * `+ navigaA(sezione : String) : void`
* **VistaDashboardAP**
    * `+ mostraMappaInterattiva() : void`
    * `+ apriZonaVietata() : void`
    * `+ apriZonaLimitata() : void`
    * `+ apriZonaParcheggio() : void`
    * `+ apriReport() : void`
    * `+ mostraGraficoNoleggi(dati : Object) : void`
    * `+ mostraQuoteMercato(dati : Object) : void`
    * `+ esportaCSV() : void`
    * `+ esportaPDF() : void`
* **VistaDefinisciZona `«Abstract»`**
    * `+ mostraEditorMappa() : void`
    * `+ tracciaPoligono(coord : List) : void`
    * `+ confermaZona() : void`
    * `+ tornaEditing(msg : String) : void`
* **VistaDefinisciZonaVietata** (Eredita da `VistaDefinisciZona`)
    * `+ selezionaTipiMezzo(tipi : List) : void`
* **VistaDefinisciZonaLimitata** (Eredita da `VistaDefinisciZona`)
    * `+ impostaLimiteVelocita(kmh : int) : void`
    * `+ selezionaTipiMezzo(tipi : List) : void`
* **VistaDefinisciZonaParcheggio** (Eredita da `VistaDefinisciZona`)
    * `+ associaCatMezzo(tipi : List) : void`

---

### 2. API Service Layer (Client-Side)

Insieme di servizi locali sul client che incapsulano la logica di comunicazione remota.

#### ApiService `«Facade, Singleton»`
* **Attributi:**
    * `- baseUrl : String`
    * `- authToken : String`
* **Metodi:**
    * `+ riceviNotifica(evento : Evento): void`
    * `+ gestisciRisposta(response : Response): void`
    * `+ mostraErroreHTTP(codice: int, msg: String): void`
    * `- inviaRichiesta(endpoint: String, body: Object): Response`
    * `- aggiungiHeaders(key: String, value: String): void`

#### Servizi Specifici delegati (Pattern Facade)
* **AuthService:** Gestisce token e sessione utente (`- tokenCorrente`, `- utenteAutenticato`).
* **FlottaService:** Gestisce lo stato locale dei mezzi (`- mezzi : List`).
* **ZonaService:** Mantiene l'elenco locale delle zone geografiche (`- zone : List<Zona>`).
* **MapService:** Gestisce la geolocalizzazione dell'hardware (`- posizioneCorrente : Coordinate`).
* **PaymentService:** Gestisce i metodi di pagamento del client.

---

## ARCHITETTURA DEL SERVER

Il Server è strutturato secondo una rigorosa architettura a tre livelli (**3-Tier**): Controller, Business Logic Layer (BLL), e Data Access Layer (DAL).

### 1. Controller Layer

Riceve le richieste HTTP/API dal client, valida l'autenticazione ed esegue il routing verso la logica di business.

#### BaseController `«FrontController, Abstract»`
* **Attributi:**
    * `# basePath : String`
    * `# sessione : Sessione`
* **Metodi:**
    * `+ handleRequest(req : Request) : Response`
    * `# validaAutenticazione() : boolean`
    * `# instrada(path : String) : void`
    * `# gestisciErrore(e : Exception) : Response`

#### Controller Specifici (Implementazioni)
* **LoginController:** `+ login(email, password)`, `- validaCredenziali(credenziali)`
* **UtenteController:** `+ modificaProfilo(id, dati)`, `- validaDatiAccount(dati)`, `+ registra(dati)`
* **PrenotazioneUtenteController:** `+ creaPrenotazione(idMezzo, idUtente)`, `+ sbloccaMezzo(idMezzo)`, `+ terminaCorsa(idCorsa)`
* **PagamentiController:** `+ effettuaPagamento(idCorsa)`, `+ salvaMetodoPagamento(idUt, metodo)`, `- calcolaImporto(corsa)`
* **OperatoreController:** `- autenticaOperatore(credenziali)`
* **MezzoOperatoreController:** `+ aggiungiMezzo(dati)`, `+ dismetti(idMezzo)`, `+ modificaStato(idMezzo, stato)`, `+ visualizzaFlotta()`
* **ZonaOperatoreController:** `+ definisciZonaOperativa(p : Polygon)`, `+ modificaZona(id, d)`, `+ listaZoneOperative()`
* **AmministrazionePubblicaController:** `+ visualizzaReport(periodo)`
* **ZonaAPController:** `+ creaZonaVietata(p)`, `+ creaZonaParcheggio(p)`, `+ creaZonaLimitata(p, kmh)`, `+ modificaZona(id, d)`, `+ validaPerimetro(p)`
* **ReportAPController:** `+ generaReport(periodo)`, `+ esportaCSV(idReport)`, `+ esportaPDF(idReport)`

---

### 2. Business Logic Layer (BLL) & Domain Model

Questo livello contiene il motore logico dell'applicazione (i Servizi) e il Modello ad Oggetti del dominio.

#### Servizi di Business (BLL)
* **Servizio `«Abstract»`:** Fornisce funzioni di utilità trasversali come `# logger`, `# handleBusinessException(e)` e `# validateEntity(e)`.
* **ServizioMobilità:** Coordina lo stato delle corse in tempo reale (`+ avviaCorsa()`, `+ sospendiCorsa()`, `+ terminaCorsa()`, `+ sbloccaMezzo()`).
* **ServizioGIS:** Esegue computazioni geometriche spaziali (`+ getZoneGeografiche()`, `+ verificaInZona(pos)`, `+ calcolaPercorso()`).
* **ServizioPricing:** Determina costi e tariffe applicate (`+ calcolaTariffa(corsa)`, `+ applicaPromozione(promo)`, `+ definisciTariffa()`).
* **ServizioReport:** Elabora le aggregazioni di dati (`+ generaReportCorse()`, `+ esportaCSV()`).
* **ServizioPrenotazione:** Controlla i vincoli di prenotazione temporanea (`+ creaPrenotazione()`, `+ annullaPrenotazione()`, `+ verificaScadenza()`).
* **ServizioUtenti:** Gestisce il ciclo di vita degli account (`+ registraAccount()`, `+ autenticaAccount()`, `+ sospendiAccount()`, `+ inviaSegnalazione()`).

#### Classi del Modello di Dominio (Model)
* **Persona `«Abstract»`:** Classe base per l'anagrafica (`- id`, `- email`, `- password`).
    * **Utente:** (Eredita da `Persona`). Gestisce lo stato dell'account e le relazioni con i pagamenti.
    * **Operatore:** (Eredita da `Persona`). Identificato da `- matricola` e `- azienda`.
    * **AmministrazionePubblica:** (Eredita da `Persona`). Identificata da `- codiceEnte`.
* **Mezzo:** Il veicolo fisico per il noleggio (`- id`, `- tipo`, `- targa`, `- latitudine`, `- longitudine`, `- statoMezzo`).
* **Corsa:** Rappresenta un noleggio attivo o concluso (`- id`, `- oraInizio`, `- oraFine`, `- costoTotale`, `- distanzaPercorsa`).
* **Prenotazione:** Prenotazione temporanea del mezzo prima dello sblocco (`- id`, `- dataOra`, `- stato`, `- isGruppo`).
* **MetodoPagamento:** Carta o portafoglio elettronico associato all'utente.
* **Pagamento:** La transazione economica legata a una corsa o ricarica (`- importo`, `- dataOra`, `- stato`).
* **Tariffa:** Modello di costo orario/chilometrico applicato a un veicolo.
* **RegoleFineCorsa:** Criteri e penali applicate al termine del noleggio.
* **Zona `«Abstract»`:** Porzione geografica di territorio (`- id`, `- nome`, `- confini: Poligono`).
    * **ZonaVietata:** (Eredita da `Zona`). Impedisce la circolazione o il parcheggio.
    * **ZonaParcheggio:** (Eredita da `Zona`). Definisce aree di sosta dedicate con `- capienza` e `- bonusImporto`.
    * **ZonaOperativa:** (Eredita da `Zona`). Delimita il perimetro massimo di funzionamento del servizio.

---

### 3. Data Access Layer (DAL)

Responsabile della persistenza dei dati sul Database Relazionale (DBMS).

#### Struttura Repository Pattern
* **Repository<T> `«Interface, Abstract»`:** Interfaccia generica per le operazioni CRUD comuni.
    * `+ save(entity: T) : void`
    * `+ update(entity: T) : void`
    * `+ delete(id: String) : void`
* **UtenteRepository:** `+ findByEmail(e)`, `+ findById(id)`
* **MezzoRepository:** `+ findVicini(coordinate, raggio)`, `+ findByStato(stato)`
* **CorsaRepository:** `+ findByUtente(idUtente)`, `+ findAttiva(idMezzo)`
* **PrenotazioneRepository:** `+ findAttiva(idUtente)`, `+ findScadute()`
* **PagamentoRepository:** `+ findByCorsa(idCorsa)`, `+ findByUtente(idUtente)`
* **ZonaRepository:** `+ findByTipo(tipoClass)`, `+ findContenenti(coordinate)`

#### Livello Driver di Basso Livello
* **DBMS `«Interface»`**
    * `+ executeQuery(sql : String) : ResultSet`
    * `+ executeUpdate(sql : String) : int`
    * `+ connettDB() : void`

---

## INTERFACCE DI DISACCOPPIAMENTO (CONTRATTI)

Per garantire l'indipendenza tra i livelli e consentire il mock/testing, sono state inserite quattro interfacce architetturali di disaccoppiamento:

1.  **ApiToView:** Esposta dall'API Service Layer verso le View del Client.
2.  **ClientToServer / ServerToClient:** Definisce il contratto di rete (es. REST API / WebSocket) per il passaggio dei dati tra Client e Server.
3.  **ControllerToBLL:** Interfaccia esposta dal Business Logic Layer per isolare i Controller della rete dalla logica pura di business.
4.  **ModelToDAL:** Esposta dai Repository verso il Modello per isolare le entità di business dalle query SQL dirette sul database.