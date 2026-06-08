# Diagramma delle Classi — SmartMobility

> Esportazione completa del diagramma `Diagramma_Classi.drawio` in formato Markdown.
> Organizzato per layer architetturale (Client/Server + MVC a tre tier) per supportare progettazione e implementazione.

## Indice delle classi

Totale elementi identificati: **100**.

- **CLIENT - View (Presentation)** (16): `VistaAbbonamenti`, `VistaAccount`, `VistaCorsa`, `VistaDashboardAP`, `VistaDashboardOperatore`, `VistaDefinisciZona`, `VistaGestioneUtentiOperatore`, `VistaHomepageUtente`, `VistaImpostazioniRegole`, `VistaMezziOperatore`, `VistaPagamento`, `VistaParametriSistema`, `VistaReport`, `VistaSegnalazioneUtente`, `VistaSegnalazioniOP`, `VistaTariffePromozioni`
- **CLIENT - Service (BLL lato client)** (6): `ApiService >`, `AuthService`, `FlottaService`, `MapService`, `PaymentService`, `ZonaService`
- **SERVER - Controller (MVC / FrontController)** (16): `AbbonamentoController`, `AccountController «FrontController»`, `AmministrazionePubblicaController`, `ConfigurazioneController`, `CorsaController`, `DashBoardOPController`, `HomePageUtenteController`, `MezzoOperatoreController`, `OffertaController`, `PagamentoController`, `RegoleFineCorsaController`, `SegnalazioneOPController`, `SegnalazioneUtenteController`, `UtentiOPController`, `ZoneController`, `«interface» BLLToController`
- **SERVER - Service (Business Logic Layer)** (20): `AbbonamentoService`, `ConfigurazioneService`, `CorsaService`, `GestioneUtentiService`, `OffertaService`, `RegoleFineCorsaService`, `ReportService`, `SegnalazioneService`, `Servizio >`, `ServizioAbbonamento`, `ServizioGIS`, `ServizioMobilità`, `ServizioOfferta`, `ServizioParametri`, `ServizioPrenotazione`, `ServizioPricing`, `ServizioRegoleFineCorsa`, `ServizioReport`, `ServizioSegnalazione`, `ServizioUtenti`
- **SERVER - Model (Domain / Entity)** (18): `Abbonamento`, `AbbonamentoUtente`, `AmministrazionePubblica`, `Corsa`, `MetodoPagamento`, `Mezzo`, `Offerta`, `Operatore`, `Pagamento`, `ParametriSistema`, `Persona`, `Prenotazione`, `Promozione`, `RegolaFineCorsa`, `Segnalazione`, `Tariffa`, `Utente`, `Zona`
- **SERVER - Repository (Data Access Layer)** (14): `> DBMS`, `AbbonamentoRepository`, `CorsaRepository`, `MezzoRepository`, `OffertaRepository`, `PagamentoRepository`, `ParametriSistemaRepository`, `PrenotazioneRepository`, `RegoleFineCorsaRepository`, `Repository >`, `SegnalazioneRepository`, `TariffaRepository`, `UtenteRepository`, `ZonaRepository`
- **Interfacce / Contratti** (7): `«interface» ApiToView`, `«interface» ClientToServer`, `«interface» DALtoModel`, `«interface» GoogleMaps`, `«interface» ModelToBLL`, `«interface» Pagamenti`, `«interface» ServerToClient`
- **Sistemi esterni** (2): `GoogleMaps`, `Provider Pagamenti`


---

## CLIENT - View (Presentation)

### `VistaAbbonamenti`

**Attributi**

```
-abbonamentoAttivo: Abbonamento
-AbbonamentoAttivo: Abbonamento
```

**Metodi**

```
+accediAbbonamenti(): void
+mostraPianiAbbonamento(): List
+confermasottoscrizione(): void
+mostraRiepilogo(piano: Abbonamento): void
+mostraAbbonamentoAttivo():void
```

### `VistaAccount`

**Attributi**

```
-nome:String
-Cognome:String
-email: String
```

**Metodi**

```
+mostraFormLogin() : void
+mostraFormRegistrazione() : void
+mostraRecuperoCredenziali(): void
```

### `VistaCorsa`

**Attributi**

```
-corsaInCorso: Corsa-storico: List
-listaMezzi: List
-mezzoSelezionato: Mezzo
```

**Metodi**

```
+terminaEPaga()+mostraAvvisoZonaVietata()
+mostraRiepilogoCorsa()
+sblocca()
+mostraInfoCorsa()
+mostraErrore()
+visualizzaStoricoCorsa()
+mostraStorico(corse)
+selezionaMezzi(idMezzo[])
+mostraConfermaprenotazione()
+mostraErroreDisponibilità()
+mostraConfermaSelezioneMezzo()
+mostraTotaleComplessivo(Corsa[])
+sospendiCorsa()
+mostraAddebitoPausa()
+mostraSospensione(tempoGratuitoResiduo)
```

### `VistaDashboardAP`

**Attributi**

```
-report: Report-periodoSelezionato: date
```

**Metodi**

```
+visualizzaDashboard() : void
+mostraDashboardReport(report)
+esportaCSV() : void
+esportaPDF() : void
```

### `VistaDashboardOperatore`

**Attributi**

```
-flotta: List
-zoneOperative: List
```

**Metodi**

```
+selezionaMappaOperatore()
+mostraMappaOperatore()
```

### `VistaDefinisciZona`

**Attributi**

```
-tipoZona: enum
```

**Metodi**

```
+ avviaDefinisciZona(tipoZona)
+ mostraEditorMappa()
+confermaZona()
+mostraZonaSalvata()
+tornaEditing(motivazione)
```

### `VistaGestioneUtentiOperatore`

**Attributi**

```
- utenti: List- utenteSelezionato: Utente | null
- dialogoConfermaAperto: boolean
```

**Metodi**

```
+ apriGestioneUtenti():void+ getUtenti(): void
+ mostraElencoUtenti(listaUtenti: Utente[]): void
+ selezionaUtente(idUtente: String): void
+ getDettaglioUtente(idUtente: String): void
+ mostraDettaglioUtente(utente: Utente): void
+ avviaSospensione(idUtente: String): void
+ mostraDialogoConferma(): void
+ confermaSospensione(idUtente: String): void
+ sospendiAccount(idUtente: String): void
+ mostraConfermaSospensione(): void
```

### `VistaHomepageUtente`

**Attributi**

```
-mezziDisponibili: List
-zone:List
```

**Metodi**

```
+apriMappa()
+mostraMappa(mezzi, zone)
+mostraErrore()
+selezionaMezzoStazione(id: String): void
+apriTariffe(): void
+consultaPromozioni()
```

### `VistaImpostazioniRegole`

**Attributi**

```
-regoleCorrenti: RegolaFineCorsa
-bonusAttivo: boolean
```

**Metodi**

```
+apriConfigurazioneRegoleFineCorsa()
+mostraConfiguratoreRegoleFineCorsa()
+confermaRegoleFineCorsa()
+mostraConfermaRegoleSalvate()
+mostraErrore(String)
```

### `VistaMezziOperatore`

**Attributi**

```
-flotta: List-zoneOperative: List
```

**Metodi**

```
+apriGestioneMezzi()
+mostraListaMezzi()
+selezionaMezzo()
+mostraFormModificaStato()
+confermaModificaStato()
+mostraConfermaModificaStato()
+selezionaAggiungiNuovoMezzo()
+mostraFormAggiuntaMezzo()
+confermaDatiMezzo()
+mostraConfermaAggiunta()
+richiediDismissione()
+mostraSuccesso()
+mostraErrore()
```

### `VistaPagamento`

**Attributi**

```
-metodiPagamento:List-importoDaPagare: float
```

**Metodi**

```
+apriPortafoglio()+mostraPortafoglio(List)
+aggiungiMetodopagamento(tipologia, dati)
+mostraConfermaMetodoPagamento()
+mostraErrorePagamento()
+mostraRiepilogoPagamento()
+terminaEPaga()
```

### `VistaParametriSistema`

**Attributi**

```
-parametri: ParametriSistema
maxMezzi, addebitoPausa): void
+mostraParametriAttuali: ParametriSistema
```

**Metodi**

```
+apriSezioneParametriSistema(): void+inserisciNuoviValori(durataPrenotazione, durataGrazia,
```

### `VistaReport`

**Attributi**

```
-quotaDominante: DatoTorta
-corseTotali: number
```

**Metodi**

```
+vistaReportAP(): JSX.Element
```

### `VistaSegnalazioneUtente`

**Attributi**

```
- tipologia: string- descrizione: string
```

**Metodi**

```
+accediSegnalazione(): void+mostraformSegnalazione(): void
+selezioneTipologia(tipologia: String): void
+confermaSegnalazione(tipologia, descrizione): void
```

### `VistaSegnalazioniOP`

**Attributi**

```
-segnalazioni: List
-selezionata: Segnalazione | Null-caricamento: boolean
-azioneInCorso: boolean
-messaggio: String
```

**Metodi**

```
+ apriGestioneSegnalazioni(): void
+ selezionaSegnalazione(id: String): void
+ prendiInCarico(idSegnalazione): void
+ mostraElencoSegnalazioni(listaSegnalazioni): void
+ mostraDettaglioSegnalazione(segnalazione: Segnalazione): void
+ mostraConfermaPresaInCarico(): void
```

### `VistaTariffePromozioni`

**Attributi**

```
-listaTariffe: List
-tariffaSelezionata: Tariffa
```

**Metodi**

```
+apriSezioneTariffePromozioni()+selezionaCreaNuovaOfferta()
+confermaOfferta()
```


---

## CLIENT - Service (BLL lato client)

### `ApiService >`

**Attributi**

```
-baseUrl : String
-authToken : String
```

**Metodi**

```
+riceviNotifica(evento : Evento): void
+gestisciRisposta(response : Response): void
+mostraErroreHTTP(codice: int, msg:String): void
-inviaRichiesta(endpoint: String, body: Object): Response
-aggiungiHeaders(key: String, value: String): void
```

### `AuthService`

**Attributi**

```
-tokenCorrente : String
-utenteAutenticato: Utente
```

**Metodi**

```
+login(email : String, password : String) : boolean
+logout() : void
+registraUtente(dati : Object) : boolean
+modificaDatiAccount(dati : Object) : boolean
-isAutenticato() : boolean
```

### `FlottaService`

**Attributi**

```
-mezzi : List
```

**Metodi**

```
+modificaStatoMezzo(idMezzo, nuovoStato): void
+getMezzi(): List
+getTariffe(): List
+creaTariffa(tipologiaMezzo, costoMinuto, costoKm): void
+aggiungiMezzo(tipologia, identificativo, posizione, stato):void
+verificaDisponibilità(idMezzo): boolean
+dismetti(idMezzo, idOperatore): void
+getZoneParcheggioEConfigurazione(): configurazioneAttuale
```

### `MapService`

**Attributi**

```
-posizioneUtente : Coordinate
```

**Metodi**

```
+cercaMezzi(coordinate: Coordinate, raggio : float) : List
-aggiornaPosizione(): void
+caricaMappa(posizioneUtente): Mappa
+recuperaDatiMappa()
+renderMappa(datiFlotta: Object, baseCartografica: BaseCartografica): void
```

### `PaymentService`

**Attributi**

```
-metodiPagamento: List
-metodoPredefinito: Pagamento
+salvaMetodoPagamento
```

**Metodi**

```
(metodo : MetodoPagamento) : void
+effettuaPagamento (idCorsa: int, idUtente: String) : void
+getMetodiPagamento():List
+aggiungiMetodoPagamento(tipologia): void
```

### `ZonaService`

**Attributi**

```
-zone : List
```

**Metodi**

```
+ creaZona(listaCoordinate, tipoZona): Zona
```


---

## SERVER - Controller (MVC / FrontController)

### `AbbonamentoController`

**Attributi**

```
+getAbbonamentoCorrente: AbbonamentoUtente
```

**Metodi**

```
+sottoscrivi(): AbbonamentoUtente
```

### `AccountController «FrontController»`

**Attributi**

```
#basePath : String
#sessione : Sessione
```

**Metodi**

```
+handleRequest(req : Request) : Response
#validaAutenticazione() : boolean
#instrada(path : String) : void
#gestisciErrore(e : Exception) : Response
```

### `AmministrazionePubblicaController`

**Metodi**

```
+visualizzaReport(periodo : Object) : Response
```

### `ConfigurazioneController`

**Metodi**

```
+getParametri():ParametriSistema
+modificaParamatri():void
```

### `CorsaController`

**Metodi**

```
+prenotazione()
+sblocca()
+terminaCorsa()
+getStorico()
+getRiepilogo()
+getMezzo()
+pausaCorsa()
```

### `DashBoardOPController`

**Metodi**

```
+autenticaOperatore(credenziali: Credenziali): boolean
+recuperaDatiMappa(): void
```

### `HomePageUtenteController`

**Metodi**

```
+mappaUtente()
+mostraMezzi()
+modificaProfilo()
+registra()
+login()
```

### `MezzoOperatoreController`

**Metodi**

```
+getTariffe(): List +getMezzi():List
+getstatoMezzo(): stato
+verificaMezzo(idMezzo): void
+dismettiMezzo(idMezzo): void
+aggiungiMezzo(idMezzo):void
+modificaStatoMezzo(idMezzo, stato): void
```

### `OffertaController`

**Metodi**

```
+getLista(): List
+crea():void
+elimina(): void
+modificaOfferta():void
```

### `PagamentoController`

**Metodi**

```
+getMetodiPagamento(): List+creaMetodoPagamento(): MetodoPagamento
+elaborapagamento(): boolean
+impostaPredefinito(): boolean
+calcolaImporto(): float
+getTariffe(): List
+getPromozioniAttive(): List
```

### `RegoleFineCorsaController`

**Metodi**

```
+definisciRegoleFineCorsa(): RegolaFineCorsa
+modificaRegoleFineCorsa(): void
```

### `SegnalazioneOPController`

**Metodi**

```
+lista_segnalazioni(): List
+dettaglio_segnalazione(idsegnalazione),
+prendi_in_carico(idsegnalaizone)
```

### `SegnalazioneUtenteController`

**Metodi**

```
+mie_segnalazioni(idutente): list
+invia_segnalazione(body, idutente): segnalazione
```

### `UtentiOPController`

**Metodi**

```
+ getUtenti(): void
+ getDettaglioUtente(idUtente: String): void
+ sospendiAccount(idUtente: String): void
```

### `ZoneController`

**Metodi**

```
+zoneVietate()+zoneLimitate()
+zonaOperativa()
+zoneParcheggio()
+getDatiMappaAP(): Object
```

### `«interface» BLLToController`

**Metodi**

```
+registra(dati)+autentica(credenziali)+modificaProfilo(id, dati)+creaPrenotazione(idMezzo[],idUtente)+verificaDisponibilita(idMezzo)+sblocca(idMezzo)+terminaCorsa(idCorsa)+aggiungiMezzo(dati)+dismetti(idMezzo)+elaboraPagamento(idCorsa, idUtente)+ getTariffe()+creaTariffa(tipologiaMezzo, costoMinuto, costoKm)+getMetodiPagamento(idUtente)+aggiungiMetodoPagamento(tipologia, dati, idUtente)+validaDatiPagamento()+ calcolaTariffa()+ elaboraPagamento()+paga_abbonamento(utente, importo, abbonamento)+getPromozioniAttive()+creaZona(polygon)+generaReport(periodo)+esportaCSV(idReport)+getStorico(idUtente)
+getMezziSbloccabili(posizione)
+ getUtenti(): list+ getDettaglioUtente(idUtente: String): void+ sospendiAccount(idUtente: String): void+ notificaUtente(idUtente: String, messaggio: String): void
```


---

## SERVER - Service (Business Logic Layer)

### `AbbonamentoService`

**Attributi**

```
- offerte: List
```

**Metodi**

```
+getPianiAbbonamento():list
+sottoscriviAbbonamento(): Abbonamento
```

### `ConfigurazioneService`

**Attributi**

```
- parametri: ParametriSistema
+aggiornaParametri(durataPrenotazione,
durataGrazia, maxMezzi, addebitoPausa):void
```

**Metodi**

```
+getParametriSistema(): ParametriSistema
```

### `CorsaService`

**Attributi**

```
-corseAttive: List
```

**Metodi**

```
+terminaCorsa(idCorsa): riepilogoCorsa
+prenota(idMezzo[],idUtente):List
+sbloccaMezzi(idMezzo[], idUtente): Corsa
+getRiepilogoCorsa(idCorsa)
+getCaratteristiche(idMezzo)
+getMezziSbloccabili(posizione): List
+recuperaStoricoCorsa(idUtente):List
+sospendiCorsa(idCorsa); boolean
-getTariffe(): List
```

### `GestioneUtentiService`

**Metodi**

```
+ getUtenti(): void
+ getDettaglioUtente(idUtente: String): void
+ sospendiAccount(idUtente: String): void
```

### `OffertaService`

**Attributi**

```
- offerte: List
```

**Metodi**

```
+getOfferte(): List
+creaOfferta(nome, tipo: String): Offerta
+modificaOfferta(id):void
+eliminaOfferta(id):void
```

### `RegoleFineCorsaService`

**Attributi**

```
- regole: RegolaFineCorsa
+salvaRegoleFineCorsa(politicaSanzionatoria,
importoPenale, bonusConfig) : boolean
```

**Metodi**

```
+getConfigurazioneCorrente(): RegolaFineCorsa
```

### `ReportService`

**Attributi**

```
-reportCorrente: Report
```

**Metodi**

```
+recuperaReport(): report
```

### `SegnalazioneService`

**Attributi**

```
- segnalazioniAttuali: List
+ getSegnalazioni: List
```

**Metodi**

```
+ inviaSegnalazione(tipologia, descrizione): void
+getDettaglioSegnalazione(id): Segnalazione
+ aggiornaStatoSegnalazione(id, stato): boolean
```

### `Servizio >`

**Attributi**

```
# logger: Logger
```

**Metodi**

```
# handleBusinessException(e)
# validateEntity(e): Boolean
```

### `ServizioAbbonamento`

**Metodi**

```
+get_abbonamento_attivo(utente): abbonamentoUtente
+sottoscrivi(utente): AbbonamentoUtente
+get_piani_disponibili(): List
```

### `ServizioGIS`

**Attributi**

```
-zoneVietate
-zoneOperative
-zoneLimitate
```

**Metodi**

```
+ getZoneGeografiche(): List
+ verificaInZona(pos): Zona
+ calcolaPercorso()
+ aggiornaZona()
+ creaZona(listaCoordinate, tipoZona): Zona
- validaPerimetro()
+recuperaDatiMappa(posizioneUtente):Mappa
+getBaseCartografica():BaseCartografica
+getMissioniAttive(idMezzo: String):List
+getDatiMappaAP(): Object
```

### `ServizioMobilità`

**Attributi**

```
-corsaAttiva: Corsa
```

**Metodi**

```
+ avviaCorsa(): Corsa
+sblocca(idMezzo):boolean
+ terminaCorsa(): RiepilogoCorsa
+getMezzi(): List
+ sospendiCorsa(corsa)
+modificaStatoMezzo(idMezzo, nuovoStato):void
+avvisoZonaVietata(penale)
+aggiungeMezzo(datiMezzo):void
+getMezzo(idMezzo): Mezzo
+dismetti(idmezzo): void
+verificaPosizioneInZonaOperativa():boolean
+getZonaParcheggioeRegole(): void
+getStorico(idUtente): List
+calcolaRiepilogoSessione(idCorsa): Corsa
+getMezziSbloccabili(posizione):List
+verificaDistanza(idUtente,idMezzo): boolean
+sospendiCorsa(idCorsa): boolean
-rilevaPausaScaduta(): boolean
```

### `ServizioOfferta`

**Attributi**

```
+creaOfferta(nome, tipo, descrizione, sconto,
prezzo, durata_giorni, data_inizio, data_fine,
tipo_mezzo): Offerta
```

**Metodi**

```
+lista_offerte(): List
+modificaOfferta(id): void
+eliminaOfferta(id): void
-valida(id): boolean
```

### `ServizioParametri`

**Metodi**

```
+get_parametri():ParametriSIstema
+aggiorna_parametro(parametro):void
```

### `ServizioPrenotazione`

**Attributi**

```
-durataMax
-maxMezziGruppo
```

**Metodi**

```
+ creaPrenotazione(idMezzo[], idUtente): Prenotazione
+ applicaPromozione()
+ annullaPrenotazione()
+ verificaScadenza()
+ getCaratteristiche(idMezzo)
-rimuoviNonDisponibili(idMezzo[])
```

### `ServizioPricing`

**Attributi**

```
-tariffario: Map
-promozioniAttive: Promozione
-addebitoPausa
```

**Metodi**

```
+elaboraPagamento(idCorsa, idUtente): Pagamento
+ getTariffe(): List
+creaTariffa(tipologiaMezzo, costoMinuto, costoKm): void
+getMetodiPagamento(idUtente): List
+aggiungiMetodoPagamento(tipologia, dati, idUtente): void
+validaDatiPagamento(): void
+ calcolaTariffa(): Tariffa
+ elaboraPagamento(): void
+paga_abbonamento(utente, importo, abbonamento): void
+getPromozioniAttive(): List
```

### `ServizioRegoleFineCorsa`

**Metodi**

```
+getConfigurazioneCorrente(): RegolaFineCorsa
+salvaRegoleFineCorsa(dati): boolean
```

### `ServizioReport`

**Attributi**

```
-intervalloTemporale
-formatiEsportabili: File
```

**Metodi**

```
+ generaReport(): Report
+ esportaCSV(params): File
+ consultaStorico()
```

### `ServizioSegnalazione`

**Attributi**

```
-segnalazioni: List
```

**Metodi**

```
get_mie_segnalazioni(utente_id),
registra_segnalazione(utente_id, tipologia, descrizione): Segnalazione
get_segnalazioni(): List
get_dettaglio_segnalazione(id):Segnalazione
prendi_in_carico(id): boolean
```

### `ServizioUtenti`

**Attributi**

```
- _utente_repo: UtenteRepository
```

**Metodi**

```
+ getUtenti(): list
+ getDettaglioUtente(idUtente: String): void
+ sospendiAccount(idUtente: String): void
+ notificaUtente(idUtente: String,  messaggio: String): void
```


---

## SERVER - Model (Domain / Entity)

### `Abbonamento`

**Attributi**

```
- tipoMezzo: 'monopattino'|'bicicletta'|'automobile'
-prezzo:Decimal
-durata_giorni:Integer
```

### `AbbonamentoUtente`

**Attributi**

```
-id: String
-idUtente: string
-id_offerta: string
- data_inizio: dateTime
- data_scadenza: DataTime
```

### `AmministrazionePubblica`

**Attributi**

```
-codiceEnte : String
```

**Metodi**

```
+apriReport(): Report
```

### `Corsa`

**Attributi**

```
-id : String
-oraInizio : DateTime
-oraFine : DateTime
-costoTotale : float
-stato : StatoCorsa
-distanzaPercorsa : float
-gruppoCorsaID: int
```

**Metodi**

```
+getDatiCorsa() : datiCorsa
+setStato(stato: String): void
+creaCorsa(idMezzo, idUtente, getOra(), gruppoID): Corsa
-getOra(): Time
+registraInizioPausa(time): boolean
+applicaAddebitoPausa(): boolean
```

### `MetodoPagamento`

**Attributi**

```
-id : String
-tipo : TipoMetodo
```

**Metodi**

```
+crea(id, tipo) : void
+elimina() : void
+impostaPredefinito(): boolean
```

### `Mezzo`

**Attributi**

```
-tipo : TipoMezzo
-id : String
-latitudine : float
-longitudine : float
-statoMezzo : StatoMezzo
```

**Metodi**

```
+sblocca(idMezzo) : void
+getPosizione() : Coordinate
+getStato(): StatoMezzo
+aggiornaStato(stato: String): void
+getMezziDisponibili(): List
+crea(tipo, id, latitudine, longitudine, statoMezzo): Mezzo
+findById(idMezzo): Mezzo
+findByStatoAndPosizione(posizione): List
+bloccaMezzo():boolean
```

### `Offerta`

**Attributi**

```
-id : String
-descrizione: String
-dataCreazione: DateTime
-nome: String
- tipo: 'promozione'|'abbonamento'
-stato: 'bozza'|'attiva'|'scaduta'
-dataScadenza:DateTime
```

**Metodi**

```
+getId(): String
+isAttiva(): boolean
```

### `Operatore`

**Attributi**

```
-matricola : String
-azienda : String
```

**Metodi**

```
+modificaStatoMezzo(m : Mezzo) : void
+aggiungiMezzo(m : Mezzo) : void
+dismetteMezzo(m : Mezzo) : void
+definisciTariffa() : Tariffa
+definisciRegolaFineCorsa() : void
+modificaTariffa(t : Tariffa) : void
+definisciZonaOperativa() : ZonaOperativa
```

### `Pagamento`

**Attributi**

```
-id : String
-importo : float
-dataOra : DateTime
-stato : StatoPagamento
```

**Metodi**

```
+elabora() : boolean
+crea(idCorsa, importo, transactionId): id
```

### `ParametriSistema`

**Attributi**

```
-id: int
-durata_max_prenotazione:int
-durata_periodo_grazia:int
-max_mezzi_per_utente:int
-addebito_pausa:decimal
```

**Metodi**

```
+getId(): ID
+aggiornaValori(): boolean
```

### `Persona`

**Attributi**

```
-id : String
-email : String
-nome: String
-cognome: String
```

**Metodi**

```
+login() : boolean
+logout() : void
+crea(e : Persona) : Persona
+aggiorna(e : Persona) : Persona
```

### `Prenotazione`

**Attributi**

```
-id : String
-dataOra : DateTime
-stato : StatoPrenotazione
-isGruppo : boolean
```

**Metodi**

```
+annulla() : void
+isScaduta() : boolean
+getDettaglio() : String
+creaPrenotazione(idMezzo, idUtente, scadenza): Prenotazione
+getId(): idPrenotazione
```

### `Promozione`

**Attributi**

```
-sconto_percentuale: Decimal
```

**Metodi**

```
+ applicaSconto(importo: Decimal): Decimal
```

### `RegolaFineCorsa`

**Attributi**

```
-id : String
-tipoPolitica : 'penale'|'divieto'|'avviso'
-importoPenale : float
- bonus_parcheggi_corretti: integer
-bonus_valore: decimal
```

**Metodi**

```
+crea(c : Corsa) : RegolaFineCorsa
```

### `Segnalazione`

**Attributi**

```
+ id: String
+ utente_id: String
+ tipologia: String
+ descrizione: String
+ stato: 'aperta'|'in carico'
+ data: DateTime
```

**Metodi**

```
+getId(): ID
+aggiornaStato(stato):void
```

### `Tariffa`

**Attributi**

```
-id : String
-tipoMezzo : 'monopattino"|'bicicletta'|'auto'
-costoPerMinuto : float
-costoPerKm : float
-aggiornata_at: DateTime
```

**Metodi**

```
+creaTariffa(id, tipoMezzo): Tariffa
+modificaTariffa() : void
```

### `Utente`

**Attributi**

```
-nome : String
-cognome : String
-statoAccount : boolean
```

**Metodi**

```
+prenota(m : Mezzo) : Prenotazione
+sblocca(m : Mezzo) : Corsa
+terminaCorsa() : void
+modificaDatiprofilo() : void
+ sospendi(): void
```

### `Zona`

**Attributi**

```
-id : String
-nome : String
-listaCoordinate: Coordinate
-tipoZona: Enum
```

**Metodi**

```
+crea(id, nome, tipoZona, listaCoordinate): boolean
+aggiorna(e:Zona):Zona
+getZoneAttive(): List
```


---

## SERVER - Repository (Data Access Layer)

### `> DBMS`

**Metodi**

```
+executeQuery(sql) : ResultSet
+executeUpdate(sql) : int
+connettDB()
```

### `AbbonamentoRepository`

**Metodi**

```
+crea(id_utente): AbbonamentoUtente
+get_attivo(id): AbbonamentoUtente
```

### `CorsaRepository`

**Metodi**

```
+findById(idCorsa) : Corsa+findAttiva(idMezzo) : Corsa+save(c : Corsa) : void+findAll(): List
+update(c: Corsa) : void+delete(id : String) : void
+findByUtenteOrderByData(idUtente): List
```

### `MezzoRepository`

**Metodi**

```
+findByStato(s) : List
+save(m : Mezzo) : void
+findById(idMezzo : String) : Mezzo
+findbyStatoAndPosizione(posizione):List
+findDisponibili(): List
+lista_tutti(idMezzo[]): List
+lista_tutti(): List
+update(m: Mezzo) : void
+delete(id : String) : void
+esiste_by_codice(identificativo: String): boolean
```

### `OffertaRepository`

**Metodi**

```
+findById(s) : Offerta
+save(m : Offerta) : void
+update(m: Offerta) : void
+delete(id : Offerta) : void
```

### `PagamentoRepository`

**Metodi**

```
+findByCorsa(idCorsa) : Pagamento
+findByUtente(idUt) : List
+save(p : Pagamento) : void
+update(p: Pagamento) : void
+delete(id : String) : void
```

### `ParametriSistemaRepository`

**Metodi**

```
+save(z : ParametriSistema) : void
+findById(id : String) : ParametriSistema
+update(r: ParamatriSistema) : void
+delete(id : String) : void
```

### `PrenotazioneRepository`

**Metodi**

```
+findAttiva(idUt) : Prenotazione
+findScadute() : List
+save(p : Prenotazione) : void
+update(p: Prenotazione) : void
+delete(id : String) : void
```

### `RegoleFineCorsaRepository`

**Metodi**

```
+save(z : Regola) : void
+findById(id : String) : Regola
+update(r: Regola) : void
+delete(id : String) : void
```

### `Repository >`

**Attributi**

```
#tabella: String #entityClass: Class
```

**Metodi**

```
+save(id:String) : void
+update(entity : T) : void
+delete(id : String) : void
```

### `SegnalazioneRepository`

**Metodi**

```
crea(utente_id, tipologia, descrizione): boolean
find_by_utente(utente_id),
find_all(),
find_by_id(id), aggiorna_stato(id, stato)
```

### `TariffaRepository`

**Metodi**

```
+findAll(): List
+existsByTipologia(tipologiaMezzo): boolean
+save(t: Tariffa): void
+update(t: Tariffa) : void
+delete(id : String) : void
```

### `UtenteRepository`

**Metodi**

```
+findByEmail(e : String) : Utente
+save(u : Utente) : void
+findById(id : String) : Utente
+update(u: Utente) : void
+delete(id : String) : void
```

### `ZonaRepository`

**Metodi**

```
+findByTipo(t : Class) : List
+findContenenti(c : Coordinate) : List
+save(z : Zona) : void
+findById(id : String) : Zona
+findZonaOperativaByPosizione(posizione):Zona
+update(z: Zona) : void
+delete(id : String) : void
```


---

## Interfacce / Contratti

### `«interface» ApiToView`

**Attributi**

```
+ getSegnalazioni: List
+salvaMetodoPagamento
```

**Metodi**

```
+modificaStatoMezzo(idMezzo, nuovoStato): void
+getMezzi(): List
+getTariffe(): List
+creaTariffa(tipologiaMezzo, costoMinuto, costoKm): void
+aggiungiMezzo(tipologia, identificativo, posizione, stato):void
+verificaDisponibilità(idMezzo): boolean
+dismetti(idMezzo, idOperatore): void
+getZoneParcheggioEConfigurazione(): configurazioneAttuale
+salvaRegoleFineCorsa(politicaSanzionatoria,importoPenale, bonusConfig) : boolean
+getConfigurazioneCorrente(): RegolaFineCorsa
+login(email : String, password : String) : boolean
+logout() : void
+registraUtente(dati : Object) : boolean
+modificaDatiAccount(dati : Object) : boolean
+ inviaSegnalazione(tipologia, descrizione): void
+getDettaglioSegnalazione(id): Segnalazione
+ aggiornaStatoSegnalazione(id, stato): boolean
+getPianiAbbonamento():list
+sottoscriviAbbonamento(): Abbonamento
+ creaZona(listaCoordinate, tipoZona): Zona
+cercaMezzi(coordinate: Coordinate, raggio : float) : List
+caricaMappa(posizioneUtente): Mappa
+recuperaDatiMappa()
+renderMappa(datiFlotta: Object, baseCartografica: BaseCartografica): void
+terminaCorsa(idCorsa): riepilogoCorsa
+prenota(idMezzo[],idUtente):List
+sbloccaMezzi(idMezzo[], idUtente): Corsa
+getRiepilogoCorsa(idCorsa)
+getCaratteristiche(idMezzo)
+getMezziSbloccabili(posizione): List
+recuperaStoricoCorsa(idUtente):List
+sospendiCorsa(idCorsa); boolean
+recuperaReport(): report
(metodo : MetodoPagamento) : void
+effettuaPagamento (idCorsa: int, idUtente: String) : void
+getMetodiPagamento():List
+aggiungiMetodoPagamento(tipologia): void
+getOfferte(): List
+creaOfferta(nome, tipo: String): Offerta
+modificaOfferta(id):void
+eliminaOfferta(id):void
+ getUtenti(): void
+ getDettaglioUtente(idUtente: String): void
+ sospendiAccount(idUtente: String): void
```

### `«interface» ClientToServer`

**Attributi**

```
+ getSegnalazioni: List
+salvaMetodoPagamento
```

**Metodi**

```
+modificaStatoMezzo(idMezzo, nuovoStato): void
+getMezzi(): List
+getTariffe(): List
+creaTariffa(tipologiaMezzo, costoMinuto, costoKm): void
+aggiungiMezzo(tipologia, identificativo, posizione, stato):void
+verificaDisponibilità(idMezzo): boolean
+dismetti(idMezzo, idOperatore): void
+getZoneParcheggioEConfigurazione(): configurazioneAttuale
+salvaRegoleFineCorsa(): void
+login(email : String, password : String) : boolean
+logout() : void
+registraUtente(dati : Object) : boolean
+modificaDatiAccount(dati : Object) : boolean
+ inviaSegnalazione(tipologia, descrizione): void
+getDettaglioSegnalazione(id): Segnalazione
+ aggiornaStatoSegnalazione(id, stato): boolean
+getPianiAbbonamento():list
+sottoscriviAbbonamento(): Abbonamento
+ creaZona(listaCoordinate, tipoZona): Zona
+cercaMezzi(coordinate: Coordinate, raggio : float) : List
+caricaMappa(posizioneUtente): Mappa
+recuperaDatiMappa()
+renderMappa(datiFlotta: Object, baseCartografica: BaseCartografica): void
+terminaCorsa(idCorsa): riepilogoCorsa
+prenota(idMezzo[],idUtente):List
+sbloccaMezzi(idMezzo[], idUtente): Corsa
+getRiepilogoCorsa(idCorsa)
+getCaratteristiche(idMezzo)
+getMezziSbloccabili(posizione): List
+recuperaStoricoCorsa(idUtente):List
+sospendiCorsa(idCorsa); boolean
+recuperaReport(): report
(metodo : MetodoPagamento) : void
+effettuaPagamento (idCorsa: int, idUtente: String) : void
+getMetodiPagamento():List
+aggiungiMetodoPagamento(tipologia): void
+getOfferte(): List
+creaOfferta(nome, tipo: String): Offerta
+modificaOfferta(id):void
+eliminaOfferta(id):void
+ getUtenti(): void
+ getDettaglioUtente(idUtente: String): void
+ sospendiAccount(idUtente: String): void
```

### `«interface» DALtoModel`

**Metodi**

```
+save(entity: Entity): void
+update(entity: Entity): void
+delete(id: String): void
+findById(id: String): Entity
+findByEmail(email: String): Utente
+findByStato(stato: StatoMezzo): List
+findDisponibili(): List
+findByStatoAndPosizione(posizione): List
+findAttiva(idUtente: String): Prenotazione
+findScadute(): List
+findByCorsa(idCorsa: String): Pagamento
+findByUtente(idUtente: String): List
+findByTipo(tipo: TipoZona): List
+findContenenti(coordinate: Coordinate): List
+findByUtenteOrderByData(idUtente: String): List
```

### `«interface» GoogleMaps`

**Metodi**

```
+ recuperaDatiMappa(posizioneUtente):datiMappa+ verificaZona(posizione, idMezzo): Zona
```

### `«interface» ModelToBLL`

**Metodi**

```
+sblocca(idMezzo): void
+getPosizione(): Coordinate
+getStato(): StatoMezzo
+aggiornaStato(stato: String): void
+getDatiCorsa(): datiCorsa
+setStato(stato: String): void
+annulla(): void
+isScaduta(): boolean
+getDettaglio(): String
+getId(): idPrenotazione
+elabora(): boolean
+getId(): ID
+aggiornaStato(stato): void
+login(): boolean
+logout(): void
+ sospendi(): void
```

### `«interface» Pagamenti`

**Metodi**

```
+autorizza(metodoPagamento, importo):transactionID+validaDatiPagamento(tipologia, dati)
```

### `«interface» ServerToClient`

_Nessun membro definito nel diagramma (classe stub / segnaposto)._


---

## Sistemi esterni

### `GoogleMaps`

_Nessun membro definito nel diagramma (classe stub / segnaposto)._

### `Provider Pagamenti`

_Nessun membro definito nel diagramma (classe stub / segnaposto)._


---

## Relazioni tra classi

| Da | Tipo | A | Molteplicità / Note |
|----|------|---|---------------------|
| `AccountController «FrontController»` | dipendenza | `«interface» ServerToClient` | > |
| `Utente` | associazione | `MetodoPagamento` | 1, 0..* |
| `MetodoPagamento` | associazione | `Pagamento` | 1, 0..* |
| `Corsa` | associazione | `Pagamento` | 1, 1 |
| `Corsa` | associazione | `Mezzo` | 0..*, 1 |
| `Operatore` | associazione | `Tariffa` | 1, 0..* |
| `Utente` | associazione | `AmministrazionePubblica` |  |
| `ServizioMobilità` | dipendenza/realizzazione | `«interface» GoogleMaps` | — Use |
| `Servizio >` | dipendenza/realizzazione | `«interface» ModelToBLL` | — Use |
| `Servizio >` | dipendenza | `«interface» BLLToController` | > |
| `Persona` | dipendenza | `«interface» ModelToBLL` | Realize |
| `Zona` | dipendenza | `«interface» ModelToBLL` | Realize |
| `ZonaService` | dipendenza/realizzazione | `ApiService >` | — «usa» |
| `MapService` | dipendenza/realizzazione | `ApiService >` | — «usa» |
| `ApiService >` | dipendenza | `«interface» ApiToView` | > |
| `AuthService` | dipendenza/realizzazione | `ApiService >` | — «usa» |
| `FlottaService` | dipendenza/realizzazione | `ApiService >` | — «usa» |
| `PaymentService` | dipendenza/realizzazione | `ApiService >` | — «usa» |
| `Utente` | associazione | `Prenotazione` | 1, 0..* |
| `Prenotazione` | associazione | `Corsa` | 0..1, 0..1 |
| `MetodoPagamento` | dipendenza | `«interface» ModelToBLL` | Realize |
| `AbbonamentoUtente` | associazione | `Abbonamento` | 0..*, 1 |
| `VistaHomepageUtente` | associazione | `VistaAccount` |  |
| `VistaCorsa` | associazione | `VistaAccount` |  |
| `VistaPagamento` | associazione | `VistaAccount` |  |
| `VistaTariffePromozioni` | associazione | `VistaAccount` |  |
| `VistaMezziOperatore` | associazione | `VistaAccount` |  |
| `VistaDashboardOperatore` | associazione | `VistaAccount` |  |
| `VistaDashboardAP` | associazione | `VistaAccount` |  |
| `VistaImpostazioniRegole` | associazione | `VistaAccount` |  |
| `VistaAbbonamenti` | associazione | `VistaAccount` |  |
| `VistaParametriSistema` | associazione | `VistaAccount` |  |
| `VistaAccount` | associazione | `VistaReport` |  |

> Nota: i tipi di relazione sono dedotti dallo stile grafico degli edge draw.io (frecce, tratteggio, diamanti). Verifica composizione/aggregazione nei casi marcati come "associazione" se nel diagramma originale usavi diamanti pieni/vuoti.