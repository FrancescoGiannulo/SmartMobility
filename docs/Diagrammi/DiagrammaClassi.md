# Specifica Architetturale e Tecnica: Diagramma delle Classi (Client-Server)

Questo documento descrive formalmente l'architettura software a livelli (N-Tier) definita nel diagramma delle classi. Il sistema è diviso in due macro-ambienti (Client e Server) che comunicano tramite interfacce esplicite. Il sistema adotta pattern architetturali consolidati come MVC, Front Controller, Facade, Singleton, e DAO (Data Access Object).

---

## 1. INTERFACCE GLOBALI E CONTRATTI DI COMUNICAZIONE

Definiscono i contratti tra i layer e verso i sistemi di terze parti, garantendo il disaccoppiamento (Loose Coupling).

### 1.1 Comunicazione di Rete
* **`«interface» ClientToServer`** (Espone i metodi che il client può chiamare sul server)
  * `+login(email: String, password: String): void`
  * `+registra(dati: Object): void`
  * `+modificaProfilo(id: int, dati: Object): void`
  * `+creaPrenotazione(idMezzo: String, idUtente: String): void`
  * `+sbloccaMezzo(idMezzo: String, idUtente: String): void`
  * `+terminaCorsa(idCorsa: int): void`
  * `+effettuaPagamento(idCorsa: int, idUtente: String): void`
  * `+salvaMetodoPagamento(metodo: MetodoPagamento, idUtente: String): void`
  * `+cercaMezzi(coordinate: Coordinate, raggio: double): List<Mezzo>`
  * `+aggiungiMezzo(dati: Object): void`
  * `+creaZona(polygon: Polygon, tipo: TipoZona): void`
  * `+generaReport(periodo: Periodo): Report`
  * `+dismettiMezzo(idMezzo): void`
  * `+modificaStatoMezzo(idMezzo, stato): void`
  * `+getTariffe(): List<Tariffa>`
  * `+creaTariffa(): Tariffa`
  * `+salvaRegoleFineCorsa(): void`
  * `+caricaMappa(): Mappa`
  * `+getCaratteristiche(): Mezzo`
  * `+prenota(idMezzo[], idUtente): List<Prenotazione>`
  * `+getMezziSbloccabili(posizione): List<Mezzo>`
  * `+getRiepilogoCorsa(idCorsa): Corsa`
  * `+recuperaStoricoCorsa(idUtente): List<Corsa>`

* **`«interface» ServerToClient`** (Gestisce le callback/risposte del server)
  * `+gestisciRisposta(response: Response)`
  * `+riceviNotifica(evento: Evento)`
  * `+mostraErroreHTTP(codice: int, msg: String)`

### 1.2 Interfacce Interne al Server
* **`«interface» BLLToController`**
  * `+registra(dati)` | `+autentica(credenziali)` | `+modificaProfilo(id, dati)` | `+creaPrenotazione(idMezzo[], idUtente)` | `+verificaDisponibilita(idMezzo)` | `+sbloccaMezzo(idMezzo, idUtente)` | `+terminaCorsa(idCorsa)` | `+aggiungiMezzo(dati)` | `+dismetti(idMezzo)` | `+calcolaImporto(idCorsa)` | `+effettuaPagamento(idCorsa)` | `+definisciTariffa(tariffa)` | `+creaZona(polygon)` | `+generaReport(periodo)` | `+esportaCSV(idReport)` | `+getStorico(idUtente)` | `+getCaratteristiche(idMezzo)` | `+getMezziSbloccabili(posizione)`

* **`«interface» ModelToBLL`**
  * `+crea(e: Entity): Entity`
  * `+aggiorna(e: Entity): Entity`

* **`«interface» DALtoModel`**
  * `+save(id: String)` | `+findVicini(coordinate, raggio)` | `+save(prenotazione)` | `+findAttiva(idUtente)` | `+findByEmail(email)` | `+findContenenti(coordinate)` | `+findById(idMezzo)` | `+findDisponibili(idMezzo[])` | `+findByUtenteOrderByData(idUtente): List<Corsa>`

### 1.3 Servizi Esterni
* **`«interface» Pagamenti`**
  * `+autorizza(metodoPagamento, importo): transactionID`
  * `+validaDatiPagamento(tipologia, dati)`
* **`«interface» GoogleMaps`**
  * `+recuperaDatiMappa(posizioneUtente): datiMappa`
  * `+verificaZona(posizione, idMezzo): Zona`

---

## 2. LATO CLIENT

Il Client separa la logica di presentazione (View) dalla logica di comunicazione di rete (API Service).

### 2.1 Package `View` (Interfacce Utente)
* **`VistaAccount`**: `-nome:String`, `-Cognome:String`, `-email: String` | `+mostraFormLogin()`, `+mostraFormRegistrazione()`, `+mostraRecuperoCredenziali()`
* **`VistaImpostazioniRegole`**: `-regoleCorrenti: RegolaFineCorsa`, `-bonusAttivo: boolean` | `+apriConfigurazioneRegoleFineCorsa()`, `+mostraConfiguratoreRegoleFineCorsa()`, `+confermaRegoleFineCorsa()`, `+mostraConfermaRegoleSalvate()`, `+mostraErrore(String)`
* **`VistaDashboardOperatore`**: `-flotta: List<Mezzo>`, `-zoneOperative: List<Zona>` | `+visualizzaDashboard()`, `+mostraDashboardReport(report)`, `+esportaCSV()`, `+esportaPDF()`, `+selezionaMappaOperatore()`, `+mostraMappaOperatore()`
* **`VistaMezziOperatore`**: `-flotta: List<Mezzo>`, `-zoneOperative: List<Zona>` | `+apriGestioneMezzi()`, `+mostraListaMezzi()`, `+selezionaMezzo()`, `+mostraFormModificaStato()`, `+confermaModificaStato()`, `+mostraConfermaModificaStato()`, `+selezionaAggiungiNuovoMezzo()`, `+mostraFormAggiuntaMezzo()`, `+confermaDatiMezzo()`, `+mostraConfermaAggiunta()`, `+richiediDismissione()`, `+mostraSuccesso()`, `+mostraErrore()`
* **`VistaDefinisciZona`**: `-tipoZona: enum` | `+avviaDefinisciZona(tipoZona)`, `+mostraEditorMappa()`, `+confermaZona()`, `+mostraZonaSalvata()`, `+tornaEditing(motivazione)`
* **`VistaAbbonamenti`**: `+sottoscrivi()`, `+mostraRiepilogo(piano: Abbonamento)`
* **`VistaCorsa`**: `-corsaInCorso: Corsa`, `-storico: List<Corsa>`, `-listaMezzi: List<Mezzo>`, `-mezzoSelezionato: Mezzo` | `+terminaEPaga()`, `+mostraAvvisoZonaVietata()`, `+mostraRiepilogoCorsa()`, `+sblocca()`, `+mostraInfoCorsa()`, `+mostraErrore()`, `+visualizzaStoricoCorsa()`, `+mostraStorico(corse)`, `+selezionaMezzi(idMezzo[])`, `+mostraConfermaprenotazione()`, `+mostraErroreDisponibilità()`, `+mostraRiepilogo()`, `+mostraConfermaSelezioneMezzo()`, `+mostraTotaleComplessivo(Corsa[])`
* **`VistaTariffePromozioni`**: `+apriSezioneTariffe()`, `+apriSezionePromozioni()`, `+mostraListaTariffe()`, `+creaTariffa()`, `+creaPromozione()`, `+creaAbbonamento()`
* **`VistaPagamento`**: `-metodiPagamento: List<MetodoPagamento>`, `-importoDaPagare: float` | `+apriPortafoglio()`, `+mostraPortafoglio(List<Pagamento>)`, `+aggiungiMetodopagamento(tipologia, dati)`, `+mostraConfermaMetodoPagamento()`, `+mostraErrorePagamento()`, `+mostraRiepilogoPagamento()`, `+terminaEPaga()`
* **`VistaDashboardAP`**: `-report: Report`, `-periodoSelezionato: date`
* **`VistaParametriSistema`**: `-parametri: ParametriSistema` | `+apriSezioneParametriSistema()`, `+inserisciNuoviValori(durataPrenotazione, durataGrazia, maxMezzi, addebitoPausa)`

### 2.2 Package `API SERVICE` (Facade e Sottoservizi)
* **`«interface» ApiToView`**: Contratto interno che espone alla View tutti i metodi orchestrati da `ApiService`.
* **`ApiService <<Facade, Singleton>>`**: `-baseUrl: String`, `-authToken: String` | `+riceviNotifica(evento: Evento)`, `+gestisciRisposta(response: Response)`, `+mostraErroreHTTP(codice: int, msg: String)`, `-inviaRichiesta(endpoint: String, body: Object): Response`, `-aggiungiHeaders(key: String, value: String)`
* **`AuthService`**: `-tokenCorrente: String`, `-utenteAutenticato: Utente` | `+login(email: String, password: String): boolean`, `+logout()`, `+registra(dati: Object): boolean`, `+modificaDatiAccount(dati: Object): boolean`, `+isAutenticato(): boolean`
* **`FlottaService`**: `-mezzi: List` | `+modificaStatoMezzo(idMezzo, nuovoStato)`, `+getMezzi(): List<Mezzo>`, `+getTariffe(): List<Tariffa>`, `+creaTariffa(tipologiaMezzo, costoMinuto, costoKm)`, `+aggiungiMezzo(tipologia, identificativo, posizione, stato)`, `+verificaDisponibilità(idMezzo): boolean`, `+dismetti(idMezzo, idOperatore)`, `+getZoneParcheggioEConfigurazione(): configurazioneAttuale`, `+salvaRegoleFineCorsa()`
* **`ZonaService`**: `-zone: List<Zona>` | `+creaZona(listaCoordinate, tipoZona): Zona`
* **`MapService`**: `-posizioneUtente: Coordinate` | `+cercaMezzi(coordinate: Coordinate, raggio: float): List<Mezzo>`, `-aggiornaPosizione()`, `+caricaMappa(posizioneUtente): Mappa`, `+recuperaDatiMappa()`
* **`PaymentService`**: `-metodiPagamento: List<Pagamento>`, `-metodoPredefinito: Pagamento` | `+salvaMetodoPagamento(metodo: MetodoPagamento)`, `+effettuaPagamento(idCorsa: int, idUtente: String)`, `+getMetodiPagamento(): List<MetodoPagamento>`, `+aggiungiMetodoPagamento(tipologia)`
* **`CorsaService`**: `-corseAttive: List<Corsa>` | `+terminaCorsa(idCorsa): riepilogoCorsa`, `+prenota(idMezzo[], idUtente): List<Prenotazione>`, `+sbloccaMezzi(idMezzo[], idUtente): Corsa`, `+getRiepilogoCorsa(idCorsa)`, `+getCaratteristiche(idMezzo)`, `+getMezziSbloccabili(posizione)`, `+recuperaStoricoCorsa(idUtente): List<Corsa>`
* **`ReportService`**: `-reportCorrente: Report` | `+recuperaReport(): report`
* **`OffertaService`**: `-offerte: List<Offerta>` | `+getOfferte(): List<Offerta>`, `+creaOfferta(tipo: String): Offerta`
* **`AbbonamentoService`**: `-offerte: List<Offerta>` | `+getPianiAbbonamento(): list<Abbonamento>`, `+sottoscriviAbbonamento(): Abbonamento`
* **`ConfigurazioneService`**: `-parametri: ParametriSistema` | `+getParametriSistema(): ParametriSistema`, `+aggiornaParametri(durataPrenotazione, durataGrazia, maxMezzi, addebitoPausa)`

---

## 3. LATO SERVER

Il backend segue l'architettura a livelli: Controller (Interfaccia esterna), Business Logic Layer (Logica applicativa), Model (Entità) e Data Access Layer (Persistenza).

### 3.1 Livello `CONTROLLER` (Pattern Front Controller)
* **`AccountController «FrontController»`**: `#basePath: String`, `#sessione: Sessione` | `+handleRequest(req: Request): Response`, `#validaAutenticazione(): boolean`, `#instrada(path: String)`, `#gestisciErrore(e: Exception): Response`
* **`HomePageUtenteController`**: `+mappaUtente()`, `+mostraMezzi()`, `+modificaProfilo()`, `+registra()`, `+login()`
* **`CorsaController`**: `+prenotazione()`, `+sblocca()`, `+terminaCorsa()`, `+getStorico()`, `+getRiepilogo()`, `+getMezzo()`
* **`PagamentoController`**: `+getMetodiPagamento(): List<MetodiPagamento>`, `+creaMetodoPagamento(): MetodoPagamento`, `+elaborapagamento(): boolean`, `+impostaPredefinito(): boolean`, `+calcolaImporto(): float`
* **`DashBoardOPController`**: `+autenticaOperatore(credenziali: Credenziali): boolean`, `+recuperaDatiMappa()`
* **`MezzoOperatoreController`**: `+getTariffe(): List<Tariffa>`, `+getMezzi(): List<Mezzo>`, `+getstatoMezzo(): stato`, `+verificaMezzo(idMezzo)`, `+dismettiMezzo(idMezzo)`, `+regolefinecorsa()`, `+aggiungiMezzo(idMezzo)`, `+modificaStatoMezzo(idMezzo, stato)`
* **`ZoneController`**: `+zoneVietate()`, `+zoneLimitate()`, `+zonaOperativa()`, `+zoneParcheggio()`
* **`AmministrazionePubblicaController`**: `+visualizzaReport(periodo: Object): Response`
* **`OffertaController`**: `+getLista(): List<Offerta>`, `+crea()`, `+eliminia()`
* **`AbbonamentoController`**: `+getAbbonamentoCorrente: Abbonamento`, `+sottoscrivi(): Abbonamento`
* **`ConfigurazioneController`**: `+getParametri(): ParametriSistema`, `+modificaParamatri()`

### 3.2 `BUSINESS LOGIC LAYER` (BLL)
* **`Servizio «Business Object»`** (Classe Base): `#logger: Logger` | `#handleBusinessException(e)`, `#validateEntity(e): Boolean`
* **`ServizioUtenti`**: `-credenzialiAttive: Utente`, `-metodiPagamento: Pagamento` | `+registraAccount(params): Utente`, `+autenticaAccount(Utente): Boolean`, `+modificaProfilo()`, `+sospendiAccount()`, `+inviaSegnalazione()`
* **`ServizioMobilità`**: `-corsaAttiva: Corsa` | `+avviaCorsa(): Corsa`, `+terminaCorsa(): RiepilogoCorsa`, `+getMezzi(): List<Mezzo>`, `+sospendiCorsa(corsa)`, `+modificaStatoMezzo(idMezzo, nuovoStato)`, `+avvisoZonaVietata(penale)`, `+aggiungeMezzo(datiMezzo)`, `+getMezzo(idMezzo): Mezzo`, `+dismettiMezzo(idmezzo)`, `+verificaPosizioneInZonaOperativa(): boolean`, `+getZonaParcheggioeRegole()`, `+salvaRegoleFineCorsa()`, `+getStorico(idUtente): List<Corsa>`, `+calcolaRiepilogoSessione(idCorsa): Corsa`, `+getMezziSbloccabili(posizione): List<Mezzo>`, `+verificaDistanza(idUtente, idMezzo): boolean`
* **`ServizioPrenotazione`**: `-durataMax`, `-maxMezziGruppo` | `+creaPrenotazione(idMezzo[], idUtente): Prenotazione`, `+applicaPromozione()`, `+annullaPrenotazione()`
* **`ServizioGIS`**: `-zoneVietate`, `-zoneOperative`, `-zoneLimitate` | `+getZoneGeografiche(): List<Zona>`, `+verificaInZona(pos): Zona`, `+calcolaPercorso()`, `+aggiornaZona()`, `+creaZona(listaCoordinate, tipoZona): Zona`, `-validaPerimetro()`, `+recuperaDatiMappa(posizioneUtente): Mappa`, `+getBaseCartografica(): BaseCartografica`
* **`ServizioPricing`**: `-tariffario: Map`, `-promozioniAttive: Promozione`, `-addebitoPausa` | `+elaboraPagamento(idCorsa, idUtente): Pagamento`, `+getTariffe(): List<Tariffa>`, `+creaTariffa(tipologiaMezzo, costoMinuto, costoKm)`, `+getMetodiPagamento(idUtente): List<MetodoPagamento>`, `+aggiungiMetodoPagamento(tipologia, dati, idUtente)`, `+validaDatiPagamento()`, `+calcolaTariffa(): Tariffa`, `+elaboraPagamento()`, `+paga_abbonamento(utente, importo, abbonamento)`
* **`ServizioReport`**: `-intervalloTemporale`, `-formatiEsportabili: File` | `+generaReport(): Report`, `+esportaCSV(params): File`, `+consultaStorico()`
* **`ServizioOfferta`**: `+listaOfferte(): List<Offerta>`, `+creaOfferta(nome, tipo, descrizione, sconto, prezzo, durata_giorni, data_inizio, data_fine, data_scadenza): Offerta`, `+modificaOfferta(id)`, `+eliminaOfferta(id)`
* **`ServizioAbbonamento`**: `+listaOfferte(): List<Offerta>`, `+get_abbonamento_attivo(utente): abbonamentoUtente`, `+sottoscrivi(utente): AbbonamentoUtente`
* **`ServizioParametri`**: `+get_parametri(): ParametriSistema`, `+aggiorna_parametro(parametro)`

### 3.3 Livello `MODEL` (Entità)
* **`Persona`**: `-id: String`, `-email: String`, `-nome: String`, `-cognome: String` | `+login(): boolean`, `+logout()`, `+crea(e: Persona): Persona`, `+aggiorna(e: Persona): Persona`
* **`Utente`**: `-nome: String`, `-cognome: String`, `-statoAccount: StatoAccount` | `+prenota(m: Mezzo): Prenotazione`, `+sblocca(m: Mezzo): Corsa`, `+terminaCorsa()`, `+modificaDatiprofilo()`
* **`Operatore`**: `-matricola: String`, `-azienda: String` | `+modificaStatoMezzo(m: Mezzo)`, `+aggiungiMezzo(m: Mezzo)`, `+dismetteMezzo(m: Mezzo)`, `+definisciTariffa(): Tariffa`, `+definisciRegolaFineCorsa()`, `+modificaTariffa(t: Tariffa)`, `+definisciZonaOperativa(): ZonaOperativa`
* **`AmministrazionePubblica`**: `-codiceEnte: String` | `+apriReport(): Report`
* **`Mezzo`**: `-tipo: TipoMezzo`, `-id: String`, `-latitudine: float`, `-longitudine: float`, `-statoMezzo: StatoMezzo` | `+sblocca(idMezzo)`, `+getPosizione(): Coordinate`, `+getStato(): StatoMezzo`, `+aggiornaStato(stato: String)`, `+getMezziDisponibili(): List<Mezzo>`, `+crea(tipo, id, latitudine, longitudine, statoMezzo): Mezzo`, `+findById(idMezzo): Mezzo`, `+findByStatoAndPosizione(posizione): List<Mezzo>`
* **`Corsa`**: `-id: String`, `-oraInizio: DateTime`, `-oraFine: DateTime`, `-costoTotale: float`, `-stato: StatoCorsa`, `-distanzaPercorsa: float`, `-gruppoCorsaID: int` | `+getDatiCorsa(): datiCorsa`, `+setStato(stato: String)`, `+creaCorsa(idMezzo, idUtente, getOra(), gruppoID): Corsa`, `-getOra(): Time`
* **`Prenotazione`**: `-id: String`, `-dataOra: DateTime`, `-stato: StatoPrenotazione`, `-isGruppo: boolean` | `+annulla()`, `+isScaduta(): boolean`, `+getDettaglio(): String`, `+creaPrenotazione(idMezzo, idUtente, scadenza): Prenotazione`, `+getId(): idPrenotazione`
* **`Zona`**: `-id: String`, `-nome: String`, `-listaCoordinate: Coordinate`, `-tipoZona: Enum` | `+crea(id, nome, tipoZona, listaCoordinate): boolean`, `+aggiorna(e: Zona): Zona`, `+getZoneAttive(): List<Zona>`
* **`MetodoPagamento`**: `-id: String`, `-tipo: TipoMetodo` | `+crea(id, tipo)`, `+elimina()`, `+impostaPredefinito(): boolean`
* **`Pagamento`**: `-id: String`, `-importo: float`, `-dataOra: DateTime`, `-stato: StatoPagamento` | `+elabora(): boolean`, `+crea(idCorsa, importo, transactionId): id`
* **`Tariffa`**: `-id: String`, `-tipoMezzo: 'monopattino'|'bicicletta'|'auto'`, `-costoPerMinuto: float`, `-costoPerKm: float`, `-aggiornata_at: DateTime` | `+creaTariffa(id, tipoMezzo): Tariffa`, `+modificaTariffa()`
* **`RegolaFineCorsa`**: `-id: String`, `-tipoPolitica: 'penale'|'divieto'|'avviso'`, `-importoPenale: float`, `-bonus_parcheggi_corretti: integer`, `-bonus_valore: decimal` | `+crea(c: Corsa): RegolaFineCorsa`
* **`Offerta`**: `-id: String`, `-descrizione: String`, `-dataCreazione: DateTime` | `+getId(): String`, `+isAttiva(): boolean`
* **`Promozione`**: `-titolo: String`, `-sconto_percentuale: Decimal`, `-data_inizio: DateTime`, `-data_fine: DateTime`, `-attiva: boolean` | `+applicaSconto(importo: Decimal): Decimal`
* **`Abbonamento`**: `-nome: String`, `-stato: Enum`, `-prezzo: Decimal`, `-durata_giorni: Integer`, `-data_scadenza: DataTime` | `+calcolaDataFine(dataInizio: dataTime): DataTime`
* **`AbbonamentoUtente`**: `-id: String`, `-idUtente: string`, `-id_offerta: string`, `-data_inizio: dateTime`, `-data_scadenza: DataTime` | `+getId(): ID`
* **`ParametriSistema`**: `-id: int`, `-durata_max_prenotazione: int`, `-durata_periodo_grazia: int`, `-max_mezzi_per_utente: int`, `-addebito_pausa: decimal` | `+getId(): ID`

### 3.4 `DATA ACCESS LAYER` (DAL) e Database
* **`Repository «Data Access Object»`** (Classe Base): `#tabella: String`, `#entityClass: Class<T>` | `+save(id: String): void`, `+update(entity: T): void`, `+delete(id: String): void`
* **`UtenteRepository`**: `+findByEmail(e: String): Utente`, `+save(u: Utente)`, `+findById(id: String): Utente`, `+update(u: Utente)`, `+delete(id: String)`
* **`MezzoRepository`**: `+findByStato(s): List<Mezzo>`, `+save(m: Mezzo)`, `+findById(idMezzo: String): Mezzo`, `+findbyStatoAndPosizione(posizione): List<Mezzo>`, `+findDisponibili(): List<Mezzo>`, `+findAll(idMezzo[]): List<Mezzo>`, `+update(m: Mezzo)`, `+delete(id: String)`
* **`CorsaRepository`**: `+findById(idCorsa): Corsa`, `+findAttiva(idMezzo): Corsa`, `+save(c: Corsa)`, `+findAll(): List<Corsa>`, `+update(c: Corsa)`, `+delete(id: String)`, `+findByUtenteOrderByData(idUtente): List<Corsa>`
* **`PrenotazioneRepository`**: `+findAttiva(idUt): Prenotazione`, `+findScadute(): List<Prenotazione>`, `+save(p: Prenotazione)`, `+update(p: Prenotazione)`, `+delete(id: String)`
* **`PagamentoRepository`**: `+findByCorsa(idCorsa): Pagamento`, `+findByUtente(idUt): List<Pagamento>`, `+save(p: Pagamento)`, `+update(p: Pagamento)`, `+delete(id: String)`
* **`ZonaRepository`**: `+findByTipo(t: Class): List<Zona>`, `+findContenenti(c: Coordinate): List`, `+save(z: Zona)`, `+findById(id: String): Zona`, `+findZonaOperativaByPosizione(posizione): Zona`, `+update(z: Zona)`, `+delete(id: String)`
* **`TariffaRepository`**: `+findAll(): List<Tariffa>`, `+existsByTipologia(tipologiaMezzo): boolean`, `+save(t: Tariffa)`, `+update(t: Tariffa)`, `+delete(id: String)`
* **`RegoleFineCorsaRepository`**: `+save(z: Regola)`, `+findById(id: String): Regola`, `+update(r: Regola)`, `+delete(id: String)`
* **`OffertaRepository`**: `+findById(s): List<Offerta>`, `+save(m: Offerta)`, `+update(m: Offerta)`, `+delete(id: Offerta)`
* **`AbbonamentoRepository`**: `+crea(id_utente): AbbonamentoUtente`
* **`ParametriSistemaRepository`**: `+save(z: ParametriSistema)`, `+findById(id: String): ParametriSistema`, `+update(r: ParamatriSistema)`, `+delete(id: String)`

* **`«interface» DBMS`** (Driver Database Basso Livello)
  * `+executeQuery(sql): ResultSet`
  * `+executeUpdate(sql): int`
  * `+connettDB()`