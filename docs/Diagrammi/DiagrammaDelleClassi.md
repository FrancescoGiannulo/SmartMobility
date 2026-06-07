# Diagramma delle Classi - Specifica dei Layer

Questo documento descrive in dettaglio tutte le classi presenti all'interno del sistema, organizzate secondo l'architettura a layer (Client, Controller, Business Logic Layer, Model, Data Access Layer) ed evidenziando attributi e metodi per ciascuna di esse.

---

## 1. CLIENT LAYER

Il Client gestisce l'interfaccia utente (View) e l'interazione iniziale con i servizi.

### VistaHomepageUtente
* **Descrizione**: Gestisce la schermata principale dell'applicazione utente.
* **Metodi**:
  * `+apriMappa()`
  * `+mostraMappa(mezzi, zone)`
  * `+mostraErrore()`

### VistaDefinisciZona
* **Descrizione**: Interfaccia dedicata alla configurazione e creazione di perimetri e aree geografiche.
* **Attributi**:
  * `-tipoZona: enum`
* **Metodi**:
  * `+avviaDefinisciZona(tipoZona)`
  * `+mostraEditorMappa()`
  * `+confermaZona()`
  * `+mostraZonaSalvata()`
  * `+tornaEditing(motivazione)`

### VistaImpostazioniRegole
* **Descrizione**: Permette la configurazione delle regole e politiche di fine corsa.
* **Attributi**:
  * `-regoleCorrenti: RegolaFineCorsa`
  * `-bonusAttivo: boolean`
* **Metodi**:
  * `+apriConfigurazioneRegoleFineCorsa()`
  * `+mostraConfiguratoreRegoleFineCorsa()`
  * `+confermaRegoleFineCorsa()`
  * `+mostraConfermaRegoleSalvate()`
  * `+mostraErrore(String)`

### VistaDashboardOperatore
* **Descrizione**: Dashboard riepilogativa per gli operatori di sistema per consultare report e flotta.
* **Attributi**:
  * `-flotta: List<Mezzo>`
  * `-zoneOperative: List<Zona>`
  * `-report: Report`
  * `-periodoSelezionato: date`
* **Metodi**:
  * `+visualizzaDashboard() : void`
  * `+mostraDashboardReport(report)`
  * `+esportaCSV() : void`
  * `+esportaPDF() : void`
  * `+selezionaMappaOperatore()`
  * `+mostraMappaOperatore()`

### VistaMezziOperatore
* **Descrizione**: Schermata per la gestione dello stato della flotta da parte degli operatori.
* **Attributi**:
  * `-flotta: List<Mezzo>`
  * `-zoneOperative: List<Zona>`
* **Metodi**:
  * `+apriGestioneMezzi()`
  * `+mostraListaMezzi()`
  * `+selezionaMezzo()`
  * `+mostraFormModificaStato()`
  * `+confermaModificaStato()`
  * `+mostraConfermaModificaStato()`
  * `+selezionaAggiungiNuovoMezzo()`
  * `+mostraFormAggiuntaMezzo()`
  * `+confermaDatiMezzo()`
  * `+mostraConfermaAggiunta()`
  * `+richiediDismissione()`
  * `+mostraSuccesso()`
  * `+mostraErrore()`

### VistaTariffePromozioni
* **Descrizione**: Consente la gestione e visualizzazione dei piani tariffari e promozioni.
* **Attributi**:
  * `-listaTariffe: List<Tariffa>`
  * `-tariffaSelezionata: Tariffa`
* **Metodi**:
  * `+apriSezioneTariffePromozioni()`
  * `+selezionaCreaNuovaOfferta()`
  * `+confermaOfferta()`

### VistaSegnalazioneUtente
* **Descrizione**: Form per l'invio di segnalazioni di guasti o problematiche da parte dell'utente.
* **Attributi**:
  * `-tipologia: string`
  * `-descrizione: string`
* **Metodi**:
  * `+accediSegnalazione(): void`
  * `+mostraformSegnalazione(): void`
  * `+selezioneTipologia(tipologia: String): void`
  * `+confermaSegnalazione(tipologia, descrizione): void`

### ApiService
* **Descrizione**: Componente Facade/Singleton sul client per l'interfacciamento con il server.
* **Metodi**:
  * `+riceviNotifica(evento : Evento): void`
  * `+gestisciRisposta(response : Response): void`
  * `+mostraErroreHTTP(codice: int, msg:String): void`
  * `-inviaRichiesta(endpoint: String, body: Object): Response`
  * `-aggiungiHeaders(key: String, value: String): void`

### Interfaccia: ServerToClient
* **Metodi**:
  * `+gestisciRisposta(response : Response)`
  * `+riceviNotifica(evento : Evento)`
  * `+mostraErroreHTTP(codice : int, msg : String)`

---

## 2. CONTROLLER LAYER

I controller orchestrano il flusso applicativo e instradano le richieste verso la business logic.

### AccountController (FrontController)
* **Attributi**:
  * `#basePath : String`
  * `#sessione : Sessione`
* **Metodi**:
  * `+handleRequest(req : Request) : Response`
  * `#validaAutenticazione() : boolean`
  * `#instrada(path : String) : void`
  * `#gestisciErrore(e : Exception) : Response`

### HomePageUtenteController
* **Metodi**: *(Eredita la struttura di gestione del FrontController)*

### CorsaController
* **Metodi**:
  * `+prenotazione()`
  * `+sblocca()`
  * `+terminaCorsa()`
  * `+getStorico()`
  * `+getRiepilogo()`
  * `+getMezzo()`

### PagamentoController
* **Metodi**:
  * `+getMetodiPagamento(): List<MetodiPagamento>`
  * `+creaMetodoPagamento(): MetodoPagamento`
  * `+elaborapagamento(): boolean`
  * `+impostaPredefinito(): boolean`
  * `+calcolaImporto(): float`

### DashBoardOPController
* **Metodi**:
  * `+autenticaOperatore(credenziali: Credenziali): boolean`
  * `+recuperaDatiMappa(): void`

### MezzoOperatoreController
* **Metodi**: *(Gestisce le richieste di modifica stato, inserimento e dismissione flotta)*

### ZoneController
* **Metodi**:
  * `+zoneVietate()`
  * `+zoneLimitate()`
  * `+zonaOperativa()`
  * `+zoneParcheggio()`

### AmministrazionePubblicaController
* **Metodi**:
  * `+visualizzaReport(periodo : Object) : Response`

### Interfaccia: ClientToServer
* **Metodi**:
  * `+login(email:String, password: String): void`
  * `+registra(dati:Object): void`
  * `+modificaProfilo(id: int, dati: Object):void`
  * `+creaPrenotazione(idMezzo: String, idUtente:String): void`
  * `+sbloccaMezzo(idMezzo: String, idUtente: String): void`
  * `+terminaCorsa(idCorsa: int): void`
  * `+effettuaPagamento(idCorsa: int, idUtente:String): void`
  * `+salvaMetodoPagamento(metodo:MetodoPagamento, idUtente: String):void`
  * `+cercaMezzi(coordinate:Coordinate,raggio:double): List<Mezzo>`
  * `+aggiungiMezzo(dati:Object):void`
  * `+creaZona(polygon:Polygon, tipo: TipoZona):void`
  * `+generaReport(periodo:Periodo): Report`
  * `+dismettiMezzo(idMezzo):void`
  * `+modificaStatoMezzo(idMezzo, stato): void`
  * `+getTariffe(): List<Tariffa>`
  * `+creaTariffa(): Tariffa`
  * `+salvaRegoleFineCorsa(): void`
  * `+caricaMappa():Mappa`
  * `+getCaratteristiche(): Mezzo`
  * `+prenota(idMezzo[],idUtente): List<Prenotazione>`
  * `+getMezziSbloccabili(posizione): List<Mezzo>`
  * `+getRiepilogoCorsa(idCorsa): Corsa`
  * `+recuperaStoricoCorsa(idUtente): List<Corsa>`

---

## 3. BUSINESS LOGIC LAYER (BLL)

I servizi incapsulano la logica di business e le regole applicative del dominio.

### Servizio (Business Object)
* **Attributi**:
  * `#logger: Logger`
* **Metodi**:
  * `#handleBusinessException(e)`
  * `#validateEntity(e): Boolean`

### ServizioMobilità
* **Attributi**:
  * `-corsaAttiva: Corsa`
* **Metodi**:
  * `+avviaCorsa(): Corsa`
  * `+terminaCorsa(): RiepilogoCorsa`
  * `+getMezzi(): List<Mezzo>`
  * `+sospendiCorsa(corsa)`
  * `+modificaStatoMezzo(idMezzo, nuovoStato):void`
  * `+avvisoZonaVietata(penale)`
  * `+aggiungeMezzo(datiMezzo):void`
  * `+getMezzo(idMezzo): Mezzo`
  * `+dismettiMezzo(idmezzo): void`
  * `+verificaPosizioneInZonaOperativa():boolean`
  * `+getZonaParcheggioeRegole(): void`
  * `+salvaRegoleFineCorsa(): void`
  * `+getStorico(idUtente): List<Corsa>`
  * `+calcolaRiepilogoSessione(idCorsa): Corsa`
  * `+getMezziSbloccabili(posizione):List<Mezzo>`
  * `+verificaDistanza(idUtente,idMezzo): boolean`

### ServizioGIS
* **Attributi**:
  * `-zoneVietate`
  * `-zoneOperative`
  * `-zoneLimitate`
* **Metodi**:
  * `+getZoneGeografiche(): List<Zona>`
  * `+verificaInZona(pos): Zona`
  * `+calcolaPercorso()`
  * `+aggiornaZona()`
  * `+creaZona(listaCoordinate, tipoZona): Zona`
  * `-validaPerimetro()`
  * `+recuperaDatiMappa(posizioneUtente):Mappa`
  * `+getBaseCartografica():BaseCartografica`

### ServizioUtenti
* **Attributi**:
  * `-credenzialiAttive: Utente`
  * `-metodiPagamento: Pagamento`
* **Metodi**:
  * `+registraAccount(params): Utente`
  * `+autenticaAccount(Utente): Boolean`
  * `+modificaProfilo()`
  * `+sospendiAccount()`
  * `+inviaSegnalazione()`

### ServizioPricing
* **Attributi**:
  * `-tariffario: Map`
  * `-promozioniAttive: Promozione`
  * `-addebitoPausa`
* **Metodi**:
  * `+elaboraPagamento(idCorsa, idUtente): Pagamento`
  * `+getTariffe(): List<Tariffa>`
  * `+creaTariffa(tipologiaMezzo, costoMinuto, costoKm): void`
  * `+getMetodiPagamento(idUtente): List<MetodoPagamento>`
  * `+aggiungiMetodoPagamento(tipologia, dati, idUtente): void`
  * `+validaDatiPagamento(): void`
  * `+calcolaTariffa(): Tariffa`
  * `+elaboraPagamento(): void`
  * `+paga_abbonamento(utente, importo, abbonamento): void`

### ServizioPrenotazione
* **Attributi**:
  * `-durataMax`
  * `-maxMezziGruppo`
* **Metodi**:
  * `+creaPrenotazione(idMezzo[], idUtente): Prenotazione`
  * `+applicaPromozione()`
  * `+annullaPrenotazione()`
  * `+verificaScadenza()`
  * `+getCaratteristiche(idMezzo)`
  * `-rimuoviNonDisponibili(idMezzo[])`

### ServizioReport
* **Attributi**:
  * `-intervalloTemporale`
  * `-formatiEsportabili: File`
* **Metodi**:
  * `+generaReport(): Report`
  * `+esportaCSV(params): File`
  * `+consultaStorico()`

### ServizioAbbonamento
* **Metodi**:
  * `+get_abbonamento_attivo(utente): abbonamentoUtente`
  * `+sottoscrivi(utente): AbbonamentoUtente`
  * `+get_piani_disponibili(): List<Abbonamento>`

### ServizioOfferta
* **Metodi**:
  * `+creaOfferta(nome, tipo, descrizione, sconto, prezzo, durata_giorni, data_inizio, data_fine, tipo_mezzo): Offerta`
  * `+lista_offerte(): List<Offerta>`
  * `+modificaOfferta(id): void`
  * `+eliminaOfferta(id): void`
  * `-valida(id): boolean`

### ServizioParametri
* **Metodi**:
  * `+get_parametri():ParametriSistema`
  * `+aggiorna_parametro(parametro):void`

### ServizioSegnalazione
* **Metodi**:
  * `+get_mie_segnalazioni(utente_id)`
  * `+registra_segnalazione(utente_id, tipologia, descrizione): Segnalazione`
  * `+get_segnalazioni(): List<Segnalazione>`
  * `+get_dettaglio_segnalazione(id):Segnalazione`
  * `+prendi_in_carico(id): boolean`

### Interfaccia: BLLToController
* **Metodi**:
  * `+registra(dati)`
  * `+autentica(credenziali)`
  * `+modificaProfilo(id, dati)`
  * `+creaPrenotazione(idMezzo[],idUtente)`
  * `+verificaDisponibilita(idMezzo)`
  * `+sbloccaMezzo(idMezzo, idUtente)`
  * `+terminaCorsa(idCorsa)`
  * `+aggiungiMezzo(dati)`
  * `+dismetti(idMezzo)`
  * `+calcolaImporto(idCorsa)`
  * `+effettuaPagamento(idCorsa)`
  * `+definisciTariffa(tariffa)`
  * `+creaZona(polygon)`
  * `+generaReport(periodo)`
  * `+esportaCSV(idReport)`
  * `+getStorico(idUtente)`
  * `+getCaratteristiche(idMezzo)`
  * `+getMezziSbloccabili(posizione)`

---

## 4. MODEL LAYER (ENTITIES)

Rappresenta le entità di dominio persistenti e le strutture dati principali.

### Persona (Classe Astratta)
* **Attributi**:
  * `-id : String`
  * `-email : String`
  * `-nome: String`
  * `-cognome: String`
* **Metodi**:
  * `+login() : boolean`
  * `+logout() : void`
  * `+crea(e : Persona) : Persona`
  * `+aggiorna(e : Persona) : Persona`

### Utente (Estende Persona)
* **Attributi**:
  * `-nome : String`
  * `-cognome : String`
  * `-statoAccount : StatoAccount`
* **Metodi**:
  * `+prenota(m : Mezzo) : Prenotazione`
  * `+sblocca(m : Mezzo) : Corsa`
  * `+terminaCorsa() : void`
  * `+modificaDatiprofilo() : void`

### Operatore (Estende Persona)
* **Attributi**:
  * `-matricola : String`
  * `-azienda : String`
* **Metodi**:
  * `+modificaStatoMezzo(m : Mezzo) : void`
  * `+aggiungiMezzo(m : Mezzo) : void`
  * `+dismetteMezzo(m : Mezzo) : void`
  * `+definisciTariffa() : Tariffa`
  * `+definisciRegolaFineCorsa() : void`
  * `+modificaTariffa(t : Tariffa) : void`
  * `+definisciZonaOperativa() : ZonaOperativa`

### AmministrazionePubblica (Estende Persona)
* **Attributi**:
  * `-codiceEnte : String`
* **Metodi**:
  * `+apriReport(): Report`

### Mezzo
* **Attributi**:
  * `-tipo : TipoMezzo`
  * `-id : String`
  * `-latitudine : float`
  * `-longitudine : float`
  * `-statoMezzo : StatoMezzo`
* **Metodi**:
  * `+sblocca(idMezzo) : void`
  * `+getPosizione() : Coordinate`
  * `+getStato(): StatoMezzo`
  * `+aggiornaStato(stato: String): void`
  * `+getMezziDisponibili(): List<Mezzo>`
  * `+crea(tipo, id, latitudine, longitudine, statoMezzo): Mezzo`
  * `+findById(idMezzo): Mezzo`
  * `+findByStatoAndPosizione(posizione): List<Mezzo>`

### Corsa
* **Attributi**:
  * `-id : String`
  * `-oraInizio : DateTime`
  * `-oraFine : DateTime`
  * `-costoTotale : float`
  * `-stato : StatoCorsa`
  * `-distanzaPercorsa : float`
  * `-gruppoCorsaID: int`
* **Metodi**:
  * `+getDatiCorsa() : datiCorsa`
  * `+setStato(stato: String): void`
  * `+creaCorsa(idMezzo, idUtente, getOra(), gruppoID): Corsa`
  * `-getOra(): Time`

### Prenotazione
* **Attributi**:
  * `-id : String`
  * `-dataOra : DateTime`
  * `-stato : StatoPrenotazione`
  * `-isGruppo : boolean`
* **Metodi**:
  * `+annulla() : void`
  * `+isScaduta() : boolean`
  * `+getDettaglio() : String`
  * `+creaPrenotazione(idMezzo, idUtente, scadenza): Prenotazione`
  * `+getId(): idPrenotazione`

### Pagamento
* **Attributi**:
  * `-id : String`
  * `-importo : float`
  * `-dataOra : DateTime`
  * `-stato : StatoPagamento`
* **Metodi**:
  * `+elabora() : boolean`
  * `+crea(idCorsa, importo, transactionId): id`

### MetodoPagamento
* **Attributi**:
  * `-id : String`
  * `-tipo : TipoMetodo`
* **Metodi**:
  * `+crea(id, tipo) : void`
  * `+elimina() : void`
  * `+impostaPredefinito(): boolean`

### Tariffa
* **Attributi**:
  * `-id : String`
  * `-tipoMezzo : 'monopattino'|'bicicletta'|'auto'`
  * `-costoPerMinuto : float`
  * `-costoPerKm : float`
  * `-aggiornata_at: DateTime`
* **Metodi**:
  * `+creaTariffa(id, tipoMezzo): Tariffa`
  * `+modificaTariffa() : void`

### RegolaFineCorsa
* **Attributi**:
  * `-id : String`
  * `-tipoPolitica : 'penale'|'divieto'|'avviso'`
  * `-importoPenale : float`
  * `-bonus_parcheggi_corretti: integer`
  * `-bonus_valore: decimal`
* **Metodi**:
  * `+crea(c : Corsa) : RegolaFineCorsa`

### Zona
* **Attributi**:
  * `-id : String`
  * `-nome : String`
  * `-listaCoordinate: Coordinate`
  * `-tipoZona: Enum`
* **Metodi**:
  * `+crea(id, nome, tipoZona, listaCoordinate): boolean`
  * `+aggiorna(e:Zona):Zona`
  * `+getZoneAttive(): List<Zona>`

### Segnalazione
* **Attributi**:
  * `+id: String`
  * `+utente_id: String`
  * `+tipologia: String`
  * `+descrizione: String`
  * `+stato: 'aperta'|'in carico'`
  * `+data: DateTime`
* **Metodi**:
  * `+getId(): ID`
  * `+aggiornaStato(stato):void`

### Interfaccia: ModelToBLL
* **Metodi**:
  * `+crea(e : Entity) : Entity`
  * `+aggiorna(e : Entity) : Entity`

---

## 5. DATA ACCESS LAYER (DAL)

Gestisce la persistenza e le query verso la base di dati (DBMS).

### Repository (Data Access Object - DAO Generale)
* **Attributi**:
  * `#tabella: String`
  * `#entityClass: Class<T>`
* **Metodi**:
  * `+save(id:String) : void`
  * `+update(entity : T) : void`
  * `+delete(id : String) : void`

### UtenteRepository
* **Metodi**:
  * `+findByEmail(e : String) : Utente`
  * `+save(u : Utente) : void`
  * `+findById(id : String) : Utente`
  * `+update(u: Utente) : void`
  * `+delete(id : String) : void`

### MezzoRepository
* **Metodi**:
  * `+findByStato(s) : List<Mezzo>`
  * `+save(m : Mezzo) : void`
  * `+findById(idMezzo : String) : Mezzo`
  * `+findbyStatoAndPosizione(posizione):List<Mezzo>`
  * `+findDisponibili(): List<Mezzo>`
  * `+findAll(idMezzo[]): List<Mezzo>`
  * `+update(m: Mezzo) : void`
  * `+delete(id : String) : void`

### CorsaRepository
* **Metodi**:
  * `+findById(idCorsa) : Corsa`
  * `+findAttiva(idMezzo) : Corsa`
  * `+save(c : Corsa) : void`
  * `+findAll(): List<Corsa>`
  * `+update(c: Corsa) : void`
  * `+delete(id : String) : void`
  * `+findByUtenteOrderByData(idUtente): List<Corsa>`

### PrenotazioneRepository
* **Metodi**:
  * `+findAttiva(idUt) : Prenotazione`
  * `+findScadute() : List<Prenotazione>`
  * `+save(p : Prenotazione) : void`
  * `+update(p: Prenotazione) : void`
  * `+delete(id : String) : void`

### PagamentoRepository
* **Metodi**:
  * `+findByCorsa(idCorsa) : Pagamento`
  * `+findByUtente(idUt) : List<Pagamento>`
  * `+save(p : Pagamento) : void`
  * `+update(p: Pagamento) : void`
  * `+delete(id : String) : void`

### ZonaRepository
* **Metodi**:
  * `+findByTipo(t : Class) : List<Zona>`
  * `+findContenenti(c : Coordinate) : List`
  * `+save(z : Zona) : void`
  * `+findById(id : String) : Zona`
  * `+findZonaOperativaByPosizione(posizione):Zona`
  * `+update(z: Zona) : void`
  * `+delete(id : String) : void`

### Interfaccia: DALtoModel
* **Metodi**:
  * `+save(id:String)`
  * `+findVicini(coordinate, raggio)`
  * `+save(prenotazione)`
  * `+findAttiva(idUtente)`
  * `+findByEmail(email)`
  * `+findContenenti(coordinate)`
  * `+findById(idMezzo)`
  * `+findDisponibili(idMezzo[])`
  * `+findByUtenteOrderByData(idUtente): List<Corsa>`

### Interfaccia Esterna: DBMS
* **Metodi**:
  * `+executeQuery(sql) : ResultSet`
  * `+executeUpdate(sql) : int`
  * `+connettDB()`

