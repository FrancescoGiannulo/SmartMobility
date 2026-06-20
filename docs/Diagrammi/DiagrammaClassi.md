# Diagramma delle Classi - SmartMobility

> Export testuale di `Diagramma Classi.drawio` (fonte di verita).
> Rigenerato automaticamente da `docs/Diagrammi/_gen_diagramma_md.py`.
> Organizzato per layer architetturale (Client/Server + MVC a tre tier).

## Indice delle classi

Totale elementi identificati: **136**.

- **CLIENT - View (Presentation)** (21): `VistaLogin`, `VistaProfiloUtente`, `CallbackOAuth`, `PrivacyPolicy`, `VistaGestioneUtentiOperatore`, `VistaRecensione`, `VistaSegnalazioneUtente`, `VistaSegnalazioniOperatore`, `VistaDashboardAP`, `VistaReportAP`, `VistaParametriSistema`, `VistaImpostazioniRegole`, `VistaAbbonamenti`, `VistaTariffe`, `VistaOfferte`, `VistaCorsa`, `VistaStoricoCorse`, `VistaMezziOperatore`, `VistaPagamenti`, `VistaHomePageUtente`, `VistaDefinisciZona`
- **CLIENT - Service (API Service Layer)** (18): `AuthService`, `GestioneUtentiService`, `RecensioneService`, `SegnalazioneService`, `ReportService`, `SuggerimentiService`, `RegoleFineCorsaService`, `ConfigurazioneService`, `ApiService`, `AbbonamentoService`, `OffertaService`, `TariffaService`, `CorsaService`, `PrenotazioneService`, `FlottaService`, `PaymentService`, `ZonaService`, `MapService`
- **SERVER - Controller (MVC / FrontController)** (18): `AccountController`, `UtentiOPController`, `RecensioneController`, `SegnalazioneUtenteController`, `SegnalazioneOPController`, `AmministrazionePubblicaController`, `SuggerimentoController`, `ConfigurazioneController`, `RegoleFineCorsaController`, `FrontController (router FastAPI + auth middleware)`, `AbbonamentoController`, `OffertaController`, `CorsaController`, `MezzoOperatoreController`, `PagamentoController`, `ZoneController`, `TariffaController`, `HomePageUtenteController`
- **Contratti Controller -> BLL (interfacce)** (14): `IServizioUtenti`, `IServizioRecensione`, `IServizioSegnalazione`, `IServizioReport`, `IServizioSuggerimenti`, `IServizioRegoleFineCorsa`, `IServizioParametri`, `IServizioAbbonamento`, `IServizioOfferta`, `IServizioTariffa`, `IServizioPrenotazione`, `IServizioMobilita`, `IServizioPricing`, `IServizioGIS`
- **SERVER - Service (Business Logic Layer)** (14): `ServizioUtenti`, `ServizioRecensione`, `ServizioSegnalazione`, `ServizioReport`, `ServizioSuggerimenti`, `ServizioParametri`, `ServizioRegoleFineCorsa`, `ServizioAbbonamento`, `ServizioOfferta`, `ServizioTariffa`, `ServizioPrenotazione`, `ServizioMobilita`, `ServizioPricing`, `ServizioGIS`
- **SERVER - Repository (Data Access Layer)** (18): `UtenteRepository`, `AttoreRepository`, `OperatoreRepository`, `RecensioneRepository`, `SegnalazioneRepository`, `IRepository`, `SuggerimentoRepository`, `RegoleFineCorsaRepository`, `ParametriSistemaRepository`, `AbbonamentoRepository`, `OffertaRepository`, `PromozioneRepository`, `CorsaRepository`, `PrenotazioneRepository`, `MezzoRepository`, `PagamentoRepository`, `TariffaRepository`, `ZonaRepository`
- **SERVER - Model (Domain / Entity)** (20): `Persona`, `Utente`, `Operatore`, `AmministrazionePubblica`, `Recensione`, `Segnalazione`, `ParametriSistema`, `RegolaFineCorsa`, `AbbonamentoUtente`, `Abbonamento`, `Offerta`, `Promozione`, `Prenotazione`, `Corsa`, `Mezzo`, `Tariffa`, `Pagamento`, `MetodoPagamento`, `Zona`, `Suggerimento`
- **Sistemi esterni, Adapter & Note** (13): `Nota 1 — Client`, `Nota 2 — BLL`, `Nota 3 — DAL`, `GoogleMaps`, `Pagamenti`, `ProviderPagamentiAdapter`, `IServizioAI`, `GoogleMapsAdapter`, `DBMS — Supabase PostgreSQL`, `Provider Pagamenti`, `Google Maps`, `ServizioAIAdapter`, `ServizioAI`

---

## CLIENT - View (Presentation)

### `VistaLogin`

**Attributi**

```
- email: String
- password: String
```

**Metodi**

```
+ mostraFormLogin(): void
+ mostraFormRegistrazione(): void
+ mostraRecuperoCredenziali(): void
+ mostraErrore(msg: String): void
```

### `VistaProfiloUtente`

**Attributi**

```
- nome: String
- cognome: String
- email: String
```

**Metodi**

```
+ mostraDatiAccount(): void
+ modificaDatiAccount(dati: Object): void
+ mostraConferma(): void
```

### `CallbackOAuth`

**Metodi**

```
+ gestisciCallback(): void
```

### `PrivacyPolicy`

**Metodi**

```
+ mostraPolicy(): void
```

### `VistaGestioneUtentiOperatore`

**Attributi**

```
- utenti: List
- utenteSelezionato: Utente
- dialogoConfermaAperto: boolean
```

**Metodi**

```
+ apriGestioneUtenti(): void
+ mostraElencoUtenti(lista: List): void
+ selezionaUtente(idUtente: String): void
+ mostraDettaglioUtente(u: Utente): void
+ avviaSospensione(idUtente: String): void
+ mostraDialogoConferma(): void
+ confermaSospensione(idUtente: String): void
+ mostraConfermaSospensione(): void
```

### `VistaRecensione`

**Attributi**

```
- voto: int
- commento: String
```

**Metodi**

```
+ apriFormRecensione(): void
+ mostraFormRecensione(): void
+ confermaScrivi(voto: int, commento: String): void
+ mostraConfermaRecensione(): void+ mostraStoricoRecensioni(recensioni: List): void
+ mostraErrore(msg: String): void
```

### `VistaSegnalazioneUtente`

**Attributi**

```
- tipologia: String
- descrizione: String
```

**Metodi**

```
+ accediSegnalazione(): void
+ mostraFormSegnalazione(): void
+ selezionaTipologia(tipologia: String): void
+ confermaSegnalazione(tipologia: String, descrizione: String): void
+ mostraConfermaInvio(): void
```

### `VistaSegnalazioniOperatore`

**Attributi**

```
- segnalazioni: List
- selezionata: Segnalazione
- caricamento: boolean
- azioneInCorso: boolean
```

**Metodi**

```
+ apriGestioneSegnalazioni(): void
+ mostraElencoSegnalazioni(lista: List): void
+ selezionaSegnalazione(id: String): void
+ mostraDettaglioSegnalazione(s: Segnalazione): void
+ prendiInCarico(idSegnalazione: String): void
+ mostraConfermaPresaInCarico(): void
```

### `VistaDashboardAP`

**Attributi**

```
- report: Report
- periodoSelezionato: Date
```

**Metodi**

```
+ visualizzaDashboard(): void
+ mostraDashboardReport(report: Report): void
+ esportaCSV(): void
+ esportaPDF(): void
```

### `VistaReportAP`

**Attributi**

```
- quotaDominante: DatoTorta
- corseTotali: int
```

**Metodi**

```
+ mostraReport(): void
```

### `VistaParametriSistema`

**Attributi**

```
- parametri: ParametriSistema
```

**Metodi**

```
+ apriSezioneParametriSistema(): void
+ mostraParametriAttuali(): void
+ inserisciNuoviValori(parametri: ParametriSistema): void
```

### `VistaImpostazioniRegole`

**Attributi**

```
- regoleCorrenti: RegolaFineCorsa
- bonusAttivo: boolean
```

**Metodi**

```
+ apriConfigurazioneRegoleFineCorsa(): void
+ mostraConfiguratoreRegoleFineCorsa(): void
+ confermaRegoleFineCorsa(): void
+ mostraConfermaRegoleSalvate(): void
+ mostraErrore(msg: String): void
```

### `VistaAbbonamenti`

**Attributi**

```
- abbonamentoAttivo: Abbonamento
```

**Metodi**

```
+ accediAbbonamenti(): void
+ mostraPianiAbbonamento(): List+selezionaPiano(id): boolean
+ mostraRiepilogo(piano: Abbonamento): void
+ confermaSottoscrizione(): void
+ mostraAbbonamentoAttivo(): void
```

### `VistaTariffe`

**Attributi**

```
- listaTariffe: List
- tariffaSelezionata: Tariffa
```

**Metodi**

```
+ apriTariffe(): void
+ mostraListaTariffe(listaTariffe: List): void
+ selezionaCreaNuovaTariffa(): void
+ confermaNuovaTariffa(tipoMezzo: TipoMezzo, costoMinuto: float, costoKm: float): void
+ mostraConfermaTariffa(): void
```

### `VistaOfferte`

**Attributi**

```
- listaOfferte: List
```

**Metodi**

```
+ apriOfferte(): void
+ mostraListaOfferte(listaOfferte: List): void
+ selezionaCreaNuovaOfferta(): void
+ mostraSceltaTipologia(): void
+ selezionaTipologia(tipo: String): void
+ mostraFormPromozione(): void
+ mostraFormAbbonamento(): void
+ confermaOfferta(dati: Object): void
+ mostraConferma(): void
+ mostraErrore(motivazione: String): void
```

### `VistaCorsa`

**Attributi**

```
- corsaInCorso: Corsa
- listaMezzi: List
- mezzoSelezionato: Mezzo
```

**Metodi**

```
+ sblocca(): void
+ selezionaMezzi(idMezzo: String[]): void
+ mostraConfermaSelezioneMezzo(): void
+ mostraConfermaPrenotazione(): void
+ mostraErroreDisponibilita(): void
+ mostraInfoCorsa(): void
+ sospendiCorsa(): void
+ mostraSospensione(tempoGratuitoResiduo: int): void
+ mostraAddebitoPausa(): void
+ terminaEPaga(): void
+ mostraRiepilogoCorsa(): void
+ mostraAvvisoZonaVietata(): void
+ mostraErrore(msg: String): void
```

### `VistaStoricoCorse`

**Attributi**

```
- storico: List
```

**Metodi**

```
+ visualizzaStoricoCorse(): void
+ mostraStorico(corse: List): void
+ mostraTotaleComplessivo(corse: List): void
```

### `VistaMezziOperatore`

**Attributi**

```
- flotta: List
- zoneOperative: List
```

**Metodi**

```
+ apriGestioneMezzi(): void
+ mostraListaMezzi(): void
+ selezionaMezzo(): void
+ mostraFormModificaStato(): void
+ confermaModificaStato(): void
+ mostraConfermaModificaStato(): void
+ selezionaAggiungiNuovoMezzo(): void
+ mostraFormAggiuntaMezzo(): void
+ confermaDatiMezzo(): void
+ mostraConfermaAggiunta(): void
+ richiediDismissione(): void
+ mostraSuccesso(): void
+ mostraErrore(msg: String): void
```

### `VistaPagamenti`

**Attributi**

```
- metodiPagamento: List
- importoDaPagare: float
```

**Metodi**

```
+ apriPortafoglio(): void
+ mostraPortafoglio(metodi: List): void
+ aggiungiMetodoPagamento(tipologia: String, dati: Object): void
+ mostraConfermaMetodoPagamento(): void
+ mostraRiepilogoPagamento(): void
+ mostraErrorePagamento(): void
```

### `VistaHomePageUtente`

**Attributi**

```
- mezziDisponibili: List
- zone: List
- suggerimenti: List
```

**Metodi**

```
+ apriMappa(): void
+ mostraMappa(mezzi: List, zone: List): void
+ selezionaMezzoStazione(idMezzo: String): void
+ apriTariffe(): void
+ consultaPromozioni(): void
+ mostraSuggerimenti(suggerimenti: List): void
+ segnaSuggerimentoVisto(id: String): void
+ mostraNessunSuggerimento(): void
+ mostraErrore(msg: String): void
```

### `VistaDefinisciZona`

**Attributi**

```
- tipoZona: TipoZona
```

**Metodi**

```
+ avviaDefinisciZona(tipoZona: TipoZona): void
+ mostraEditorMappa(): void
+ confermaZona(): void
+ mostraZonaSalvata(): void
+ tornaEditing(motivazione: String): void
```

---

## CLIENT - Service (API Service Layer)

### `AuthService`

**Attributi**

```
- tokenCorrente: String
- utenteAutenticato: Utente
```

**Metodi**

```
+ login(email: String, password: String): boolean
+ logout(): void
+ registraUtente(dati: Object): boolean
+ modificaDatiAccount(dati: Object): boolean
+ isAutenticato(): boolean
```

### `GestioneUtentiService`

**Metodi**

```
+ getUtenti(): List
+ getDettaglioUtente(idUtente: String): Utente
+ sospendiAccount(idUtente: String): void
```

### `RecensioneService`

**Metodi**

```
+ scriviRecensione(voto: int, commento: String): Recensione+getMieRecensioni(): List
```

### `SegnalazioneService`

**Metodi**

```
+ inviaSegnalazione(tipologia: String, descrizione: String): void
+ getMieSegnalazioni(): List
+ getSegnalazioni(): List
+ getDettaglioSegnalazione(id: String): Segnalazione
+ prendiInCarico(id: String): boolean
```

### `ReportService`

**Metodi**

```
+ recuperaReport(periodo: Object): Report
+ esportaCSV(idReport: String): File
```

### `SuggerimentiService`

**Metodi**

```
+ getSuggerimenti(): List
+ segnaVisto(id: String): void
```

### `RegoleFineCorsaService`

**Metodi**

```
+ getConfigurazioneCorrente(): RegolaFineCorsa
+ salvaRegoleFineCorsa(politica: String, importoPenale: float, bonusConfig: Object): boolean
```

### `ConfigurazioneService`

**Metodi**

```
+ getParametri(): ParametriSistema
+ aggiornaParametri(parametri: ParametriSistema): void
```

### `ApiService`

**Attributi**

```
- baseUrl: String
```

**Metodi**

```
- authToken: String (JWT)
+ inviaRichiesta(endpoint: String, body: Object): Response
+ gestisciRisposta(response: Response): void
+ mostraErroreHTTP(codice: int, msg: String): void
- aggiungiHeaders(key: String, value: String): void
```

### `AbbonamentoService`

**Metodi**

```
+ getPianiAbbonamento(): List
+ sottoscriviAbbonamento(id: String): AbbonamentoUtente
+ getAbbonamentoCorrente(): AbbonamentoUtente
```

### `OffertaService`

**Metodi**

```
+ getOfferte(): List
+ creaOfferta(dati: Object): Offerta
+ modificaOfferta(id: String, dati: Object): void
+ eliminaOfferta(id: String): void
```

### `TariffaService`

**Metodi**

```
+ getTariffe(): List
+ creaTariffa(tipoMezzo: TipoMezzo, costoMinuto: float, costoKm: float): void
```

### `CorsaService`

**Metodi**

```
+ sbloccaMezzi(idMezzo: String[], idUtente: String): Corsa
+ terminaCorsa(idCorsa: String): Corsa
+ sospendiCorsa(idCorsa: String): boolean
+ getRiepilogoCorsa(idCorsa: String): Corsa
+ getStorico(idUtente: String): List
+ getMezziSbloccabili(posizione: Coordinate): List
```

### `PrenotazioneService`

**Metodi**

```
+ creaPrenotazione(idMezzo: String[], idUtente: String): Prenotazione
+ annullaPrenotazione(idPrenotazione: String): void
+ getPrenotazioniAttive(idUtente: String): List
```

### `FlottaService`

**Attributi**

```
- mezzi: List
```

**Metodi**

```
+ getMezzi(): List
+ aggiungiMezzo(tipologia: String, identificativo: String, posizione: Coordinate): void
+ modificaStatoMezzo(idMezzo: String, nuovoStato: StatoMezzo): void
+ dismetti(idMezzo: String, idOperatore: String): void
+ verificaDisponibilita(idMezzo: String): boolean
+ getZoneParcheggioEConfigurazione(): Object
```

### `PaymentService`

**Attributi**

```
- metodiPagamento: List
- metodoPredefinito: MetodoPagamento
```

**Metodi**

```
+ getMetodiPagamento(): List
+ aggiungiMetodoPagamento(tipologia: String, dati: Object): void
+ salvaMetodoPagamento(metodo: MetodoPagamento): void
+ impostaPredefinito(idMetodo: String): boolean
+ effettuaPagamento(idCorsa: String, idUtente: String): void
+ getTariffe(): List
+ getPromozioniAttive(): List
```

### `ZonaService`

**Metodi**

```
+ creaZona(nome: String, tipo: TipoZona, coordinate: Coordinate[], limiteVelocita: int): Zona
+ eliminaZona(idZona: String): void
```

### `MapService`

**Metodi**

```
+ getMezziUtente(): List
+ getZoneUtente(): List
+ getMezziOperatore(): List
+ getZoneOperatore(): List
+ getMezziAP(): List
+ getZoneAP(): List
```

---

## SERVER - Controller (MVC / FrontController)

### `AccountController`

**Metodi**

```
+ login(credenziali: Credenziali): Response
+ registra(dati: Object): Response
+ modificaProfilo(idUtente: String, dati: Object): Response
+ logout(): Response
```

### `UtentiOPController`

**Metodi**

```
+ getUtenti(): Response
+ getDettaglioUtente(idUtente: String): Response
+ sospendiAccount(idUtente: String): Response
```

### `RecensioneController`

**Metodi**

```
+ scriviRecensione(idUtente: String, voto: int, commento: String): Response+ mieRecensioni(idUtente: String): Response
```

### `SegnalazioneUtenteController`

**Metodi**

```
+ mieSegnalazioni(idUtente: String): Response
+ inviaSegnalazione(body: SegnalazioneIn, idUtente: String): Response
```

### `SegnalazioneOPController`

**Metodi**

```
+ listaSegnalazioni(): Response
+ dettaglioSegnalazione(idSegnalazione: String): Response
+ prendiInCarico(idSegnalazione: String): Response
```

### `AmministrazionePubblicaController`

**Metodi**

```
+ visualizzaReport(periodo: Object): Response
+ esportaCSV(idReport: String): Response
```

### `SuggerimentoController`

**Metodi**

```
+ getSuggerimenti(): Response
+ segnaVisto(id: String): Response
```

### `ConfigurazioneController`

**Metodi**

```
+ getParametri(): Response
+ modificaParametri(body: ParametriIn): Response
```

### `RegoleFineCorsaController`

**Metodi**

```
+ getRegoleFineCorsa(): Response
+ definisciRegoleFineCorsa(body: RegoleIn): Response
```

### `FrontController (router FastAPI + auth middleware)`

**Metodi**

```
# basePath: String
+ handleRequest(req: Request): Response
# validaAutenticazione(): boolean
# instrada(path: String): void
# gestisciErrore(e: Exception): Response
```

### `AbbonamentoController`

**Metodi**

```
+ getPiani(): Response
+ getAbbonamentoCorrente(idUtente: String): Response
+ sottoscrivi(body: SottoscrizioneIn): Response
```

### `OffertaController`

**Metodi**

```
+ getLista(): Response
+ crea(body: OffertaIn): Response
+ modificaOfferta(id: String, body: OffertaIn): Response
+ elimina(id: String): Response
```

### `CorsaController`

**Metodi**

```
+ prenotazione(body: PrenotazioneIn): Response
+ sblocca(body: SbloccoIn): Response
+ terminaCorsa(idCorsa: String): Response
+ pausaCorsa(idCorsa: String): Response
+ getStorico(idUtente: String): Response
+ getRiepilogo(idCorsa: String): Response
+ getMezzo(idMezzo: String): Response
```

### `MezzoOperatoreController`

**Metodi**

```
+ getMezzi(): Response
+ getStatoMezzo(idMezzo: String): Response
+ aggiungiMezzo(body: MezzoIn): Response
+ modificaStatoMezzo(idMezzo: String, stato: StatoMezzo): Response
+ dismettiMezzo(idMezzo: String): Response
+ verificaMezzo(idMezzo: String): Response
```

### `PagamentoController`

**Metodi**

```
+ getMetodiPagamento(idUtente: String): Response
+ creaMetodoPagamento(body: MetodoPagamentoIn): Response
+ impostaPredefinito(idMetodo: String): Response
+ elaboraPagamento(idCorsa: String, idUtente: String): Response
+ calcolaImporto(idCorsa: String): Response
+ getTariffe(): Response
+ getPromozioniAttive(): Response
```

### `ZoneController`

**Metodi**

```
+ creaZona(body: ZonaIn): Response
+ zoneOperative(): Response
+ zoneParcheggio(): Response
+ zoneLimitate(): Response
+ zoneVietate(): Response
+ getDatiMappaAP(): Response
```

### `TariffaController`

**Metodi**

```
+ getTariffe(): Response
+ creaTariffa(body: TariffaIn): Response
+ aggiornaTariffa(idTariffa: String, body: TariffaIn): Response
```

### `HomePageUtenteController`

**Metodi**

```
+ mappaUtente()+mostraMezzi()
```

---

## Contratti Controller -> BLL (interfacce)

### `IServizioUtenti`

**Metodi**

```
+ registraAccount(email, password, nome, cognome): Utente
+ autenticaAccount(email, password): Token
+ accediOAuth(token, idUtente, email): Token
+ profiloCorrente(idUtente, email): Utente
+ esportaDati(idUtente, email): File
+ cancellaAccount(idUtente): void
+ getUtenti(): List
+ getDettaglioUtente(idUtente): Utente
+ sospendiAccount(idUtente): void
```

### `IServizioRecensione`

**Metodi**

```
+ scriviRecensione(idUtente: String, voto: int, commento: String): Recensione+ validaVoto(voto: int): boolean
+ haCorsaConclusa(idUtente: String): boolean
+ getMieRecensioni(idUtente: String): List
```

### `IServizioSegnalazione`

**Metodi**

```
+ getMieSegnalazioni(idUtente): List
+ registraSegnalazione(idUtente, tipologia, descrizione): Segnalazione
+ getSegnalazioni(): List
+ getDettaglioSegnalazione(id): Segnalazione
+ prendiInCarico(id): boolean
```

### `IServizioReport`

**Metodi**

```
+ generaReport(periodo): Report
+ esportaCSV(idReport): File
+ consultaStorico(periodo): List
```

### `IServizioSuggerimenti`

**Metodi**

```
+ getSuggerimenti(idUtente): List
+ generaSuggerimenti(idUtente): List
+ segnaVisto(idSuggerimento, idUtente): void
```

### `IServizioRegoleFineCorsa`

**Metodi**

```
+ getCorrente(): RegolaFineCorsa
+ salva(tipoVincolo, penaleFuoriZona, batteriaMinima, bonusParcheggi, bonusValore): RegolaFineCorsa
```

### `IServizioParametri`

**Metodi**

```
+ getParametri(): ParametriSistema
+ aggiornaParametri(p): ParametriSistema
```

### `IServizioAbbonamento`

**Metodi**

```
+ getPianiDisponibili(): List
+ getAbbonamentoAttivo(idUtente): AbbonamentoUtente
+ sottoscrivi(idUtente, idOfferta): AbbonamentoUtente
```

### `IServizioOfferta`

**Metodi**

```
+ listaOfferte(): List
+ creaOfferta(dati): Offerta
+ modificaOfferta(id, dati): Offerta
+ eliminaOfferta(id): void
```

### `IServizioTariffa`

**Metodi**

```
+ getTariffe(): List
+ creaTariffa(tipoMezzo, costoMin, costoKm): Tariffa
+ aggiornaTariffa(tipoMezzo, costoMin, costoKm): Tariffa
```

### `IServizioPrenotazione`

**Metodi**

```
+ creaPrenotazioni(idMezzo[], idUtente): List
+ annullaPrenotazione(idPrenotazione, idUtente): void
+ getPrenotazioniAttive(idUtente): List
+ getCaratteristiche(idMezzo): Mezzo
```

### `IServizioMobilita`

**Metodi**

```
+ sbloccaMezzi(idMezzo[], idUtente, pos): List
+ terminaCorsa(idCorsa, idUtente): void
+ mettiInPausa(idCorsa, idUtente): void
+ riprendiCorsa(idCorsa, idUtente): void
+ getMezziSbloccabili(idUtente, pos): List
+ getMezziFlotta(): List
+ aggiungiMezzo(tipo, codice, pos, stato): Mezzo
+ verificaDismissione(idMezzo): boolean
+ dismettiMezzo(idMezzo): void
+ modificaStatoMezzo(idMezzo, stato): void
+ getStorico(idUtente): List
+ calcolaRiepilogoSessione(idCorsa, idUtente): Corsa
+ getZonaParcheggioERegole(idOperatore): Object
```

### `IServizioPricing`

**Metodi**

```
+ effettuaPagamento(idCorsa, idUtente, tipoMezzo, durata, distanza, idOfferta): Pagamento
+ pagaImporto(idUtente, importo, idCorsa, idAbbonamento): Pagamento
+ calcolaImporto(tipoMezzo, durataMin, distanzaKm): Decimal
+ getTariffe(): List
+ listaMetodi(idUtente): List
+ aggiungiMetodo(idUtente, tipo, dati): MetodoPagamento
+ impostaPredefinito(idMetodo, idUtente): void
+ rimuoviMetodo(idMetodo, idUtente): void
+ getPromozioniAttive(): List
```

### `IServizioGIS`

**Metodi**

```
+ ottieniZone(): List
+ ottieniMezziUtente(): List
+ ottieniMezziOperatore(): List
+ creaZona(nome, tipo, coordinate[], limiteVelocita): Zona
+ eliminaZona(idZona): void
+ verificaPosizioneInZonaOperativa(lat, lng): boolean
```

---

## SERVER - Service (Business Logic Layer)

### `ServizioUtenti`

**Attributi**

```
- attoreRepo: IAttoreRepository
- utenteRepo: IUtenteRepository
```

**Metodi**

```
+ registraAccount(email: String, password: String, nome: String, cognome: String): Utente
+ autenticaAccount(email: String, password: String): Token
+ accediOAuth(token: String, idUtente: String, email: String, consensoPrivacy: boolean): Token
+ profiloCorrente(idUtente: String, email: String): Utente
+ esportaDati(idUtente: String, email: String): File
+ cancellaAccount(idUtente: String): void
+ getUtenti(): List
+ getDettaglioUtente(idUtente: String): Utente
+ sospendiAccount(idUtente: String): void
- buildProfilo(profilo: Object, ruolo: String, email: String): Utente
```

### `ServizioRecensione`

**Attributi**

```
- recensioneRepo: IRecensioneRepository- corsaRepo: ICorsaRepository
```

**Metodi**

```
+ scriviRecensione(idUtente: String, voto: int, commento: String): Recensione+ validaVoto(voto: int): boolean
+ haCorsaConclusa(idUtente: String): boolean
+ getMieRecensioni(idUtente: String): List
```

### `ServizioSegnalazione`

**Attributi**

```
- segnalazioneRepo: ISegnalazioneRepository
```

**Metodi**

```
+ getMieSegnalazioni(idUtente: String): List
+ registraSegnalazione(idUtente, tipologia, descrizione): Segnalazione
+ getSegnalazioni(): List
+ getDettaglioSegnalazione(id: String): Segnalazione
+ prendiInCarico(id: String): boolean
```

### `ServizioReport`

**Attributi**

```
- intervalloTemporale: Periodo
```

**Metodi**

```
+ generaReport(periodo: Periodo): Report
+ esportaCSV(idReport: String): File
+ consultaStorico(periodo: Periodo): List
```

### `ServizioSuggerimenti`

**Attributi**

```
- suggerimentoRepo: ISuggerimentoRepository
- corsaRepo: ICorsaRepository
- abbonamentoRepo: IAbbonamentoRepository
- pagamentoRepo: IPagamentoRepository
- servizioAI: IServizioAI
```

**Metodi**

```
+ getSuggerimenti(idUtente): List
+ generaSuggerimenti(idUtente): List
+ segnaVisto(idSuggerimento, idUtente): void
- raccogliDati(idUtente): Object
- ordinaPerRilevanza(suggerimenti): List
```

### `ServizioParametri`

**Attributi**

```
- parametriRepo: IParametriSistemaRepository
```

**Metodi**

```
+ getParametri(): ParametriSistema
+ aggiornaParametri(p: ParametriSistema): ParametriSistema
```

### `ServizioRegoleFineCorsa`

**Attributi**

```
- regoleRepo: IRegoleFineCorsaRepository
```

**Metodi**

```
+ getCorrente(): RegolaFineCorsa
+ salva(tipoVincolo: String, penaleFuoriZona: Decimal, batteriaMinima: int, bonusParcheggiCorretti: int, bonusValore: Decimal): RegolaFineCorsa
```

### `ServizioAbbonamento`

**Attributi**

```
- abbonamentoRepo: IAbbonamentoRepository
- offertaRepo: IOffertaRepository
```

**Metodi**

```
+ getPianiDisponibili(): List
+ getAbbonamentoAttivo(idUtente: String): AbbonamentoUtente
+ sottoscrivi(idUtente: String, idOfferta: String): AbbonamentoUtente
```

### `ServizioOfferta`

**Attributi**

```
- offertaRepo: IOffertaRepository
- promozioneRepo: IPromozioneRepository
```

**Metodi**

```
+ listaOfferte(): List
+ creaOfferta(dati: Object): Offerta
+ modificaOfferta(id: String, dati: Object): Offerta
+ eliminaOfferta(id: String): void
- valida(dati: Object): boolean
```

### `ServizioTariffa`

**Attributi**

```
- tariffaRepo: ITariffaRepository
```

**Metodi**

```
+ getTariffe(): List
+ creaTariffa(tipoMezzo: TipoMezzo, costoMinuto: float, costoKm: float): Tariffa
+ aggiornaTariffa(tipoMezzo: TipoMezzo, costoMinuto: float, costoKm: float): Tariffa
```

### `ServizioPrenotazione`

**Attributi**

```
- mezzoRepo: IMezzoRepository
- prenotazioneRepo: IPrenotazioneRepository
- parametriRepo: IParametriSistemaRepository
```

**Metodi**

```
+ creaPrenotazioni(idMezzo: String[], idUtente: String): List
+ annullaPrenotazione(idPrenotazione: String, idUtente: String): void
+ getPrenotazioniAttive(idUtente: String): List
+ getCaratteristiche(idMezzo: String): Mezzo
```

### `ServizioMobilita`

**Attributi**

```
- mezzoRepo: IMezzoRepository
- corsaRepo: ICorsaRepository
- prenotazioneRepo: IPrenotazioneRepository
- zonaRepo: IZonaRepository
- operatoreRepo: IOperatoreRepository
- parametriRepo: IParametriSistemaRepository
```

**Metodi**

```
+ sbloccaMezzi(idMezzo: String[], idUtente: String, pos: Coordinate): List
+ terminaCorsa(idCorsa: String, idUtente: String): void
+ mettiInPausa(idCorsa: String, idUtente: String): void
+ riprendiCorsa(idCorsa: String, idUtente: String): void
+ getMezziSbloccabili(idUtente: String, pos: Coordinate): List
+ getMezziFlotta(): List
+ aggiungiMezzo(tipo: TipoMezzo, codice: String, pos: Coordinate, stato: StatoMezzo): Mezzo
+ verificaDismissione(idMezzo: String): boolean
+ dismettiMezzo(idMezzo: String): void
+ modificaStatoMezzo(idMezzo: String, stato: StatoMezzo): void
+ getStorico(idUtente: String): List
+ calcolaRiepilogoSessione(idCorsa: String, idUtente: String): Corsa
+ getZonaParcheggioERegole(idOperatore: String): Object
- sbloccaSingolo(idUtente: String, idMezzo: String, gruppoCorsaId: String): Corsa
```

### `ServizioPricing`

**Attributi**

```
- strategie: Map
- provider: ProviderPagamentiAdapter
- pagamentoRepo: IPagamentoRepository
- tariffaRepo: ITariffaRepository
- promozioneRepo: IPromozioneRepository
- abbonamentoRepo: IAbbonamentoRepository
```

**Metodi**

```
+elaboraPagamento(idCorsa, idUtente):boolean
+ calcolaImporto(tipoMezzo: TipoMezzo, durataMin: float, distanzaKm: float): Decimal
+ getTariffe(): List
+ listaMetodi(idUtente: String): List
+ aggiungiMetodo(idUtente: String, tipo: TipoMetodo, dati: Object): MetodoPagamento
+ impostaPredefinito(idMetodo: String, idUtente: String): void
+ rimuoviMetodo(idMetodo: String, idUtente: String): void
+ getPromozioniAttive(): List
```

### `ServizioGIS`

**Attributi**

```
- zonaRepo: IZonaRepository
- mezzoRepo: IMezzoRepository
```

**Metodi**

```
+ ottieniZone(): List
+ ottieniMezziUtente(): List
+ ottieniMezziOperatore(): List
+ creaZona(nome: String, tipo: TipoZona, coordinate: Coordinate[], limiteVelocita: int): Zona
+ eliminaZona(idZona: String): void
+ verificaPosizioneInZonaOperativa(lat: float, lng: float): boolean
- applicaPrecedenzaZone(zone: List): List
```

---

## SERVER - Repository (Data Access Layer)

### `UtenteRepository`

**Metodi**

```
+ findByEmail(email: String): Utente
+ findById(id: String): Utente
+ save(u: Utente): Utente
+ update(u: Utente): Utente
+ delete(id: String): void
```

### `AttoreRepository`

**Metodi**

```
+ findById(id: String): Persona
+ findByRuolo(ruolo: String): List
+ sospendi(id: String): void
```

### `OperatoreRepository`

**Metodi**

```
+ findById(id: String): Operatore
+ findByMatricola(matricola: String): Operatore
```

### `RecensioneRepository`

**Metodi**

```
+ save(r: Recensione): Recensione
+ findByUtenteId(idUtente: String): List
+ findAll(): List
```

### `SegnalazioneRepository`

**Metodi**

```
+ crea(idUtente, tipologia, descrizione): Segnalazione
+ findByUtente(idUtente: String): List
+ findAll(): List
+ findById(id: String): Segnalazione
+ aggiornaStato(id: String, stato: StatoSegnalazione): boolean
```

### `IRepository`

**Metodi**

```
+ save(entity: T): T
+ update(entity: T): T
+ delete(id: String): void
+ findById(id: String): T
```

### `SuggerimentoRepository`

**Metodi**

```
+ findByUtente(idUtente: String): List
+ save(s: Suggerimento): Suggerimento
+ findRecenti(idUtente: String, da: DateTime): List
+ aggiornaStato(id: String, stato: StatoSuggerimento): void
```

### `RegoleFineCorsaRepository`

**Metodi**

```
+ findCorrente(): RegolaFineCorsa
+ save(r: RegolaFineCorsa): RegolaFineCorsa
+ update(r: RegolaFineCorsa): RegolaFineCorsa
```

### `ParametriSistemaRepository`

**Metodi**

```
+ findCorrente(): ParametriSistema
+ save(p: ParametriSistema): ParametriSistema
+ update(p: ParametriSistema): ParametriSistema
```

### `AbbonamentoRepository`

**Metodi**

```
+ crea(idUtente: String, idOfferta: String): AbbonamentoUtente
+ getAttivo(idUtente: String): AbbonamentoUtente
+ getPianiDisponibili(): List
```

### `OffertaRepository`

**Metodi**

```
+ findById(id: String): Offerta
+ findAll(): List
+ save(o: Offerta): Offerta
+ update(o: Offerta): Offerta
+ delete(id: String): void
```

### `PromozioneRepository`

**Metodi**

```
+ findAttive(): List
+ findById(id: String): Promozione
```

### `CorsaRepository`

**Metodi**

```
+ findById(idCorsa: String): Corsa
+ findAttiva(idMezzo: String): Corsa
+ findByUtenteOrderByData(idUtente: String): List
+ findByPeriodo(periodo: Periodo): List
+ save(c: Corsa): Corsa
+ update(c: Corsa): Corsa
```

### `PrenotazioneRepository`

**Metodi**

```
+ findAttiva(idUtente: String): Prenotazione
+ findScadute(): List
+ save(p: Prenotazione): Prenotazione
+ update(p: Prenotazione): Prenotazione
+ delete(id: String): void
```

### `MezzoRepository`

**Metodi**

```
+ findById(idMezzo: String): Mezzo
+ findByStato(stato: StatoMezzo): List
+ findByStatoAndPosizione(pos: Coordinate): List
+ findDisponibili(): List
+ listaTutti(): List
+ esisteByCodice(identificativo: String): boolean
+ save(m: Mezzo): Mezzo
+ update(m: Mezzo): Mezzo
+ delete(id: String): void
```

### `PagamentoRepository`

**Metodi**

```
+ findByCorsa(idCorsa: String): Pagamento
+ findByUtente(idUtente: String): List
+ save(p: Pagamento): Pagamento
+ getMetodiByUtente(idUtente: String): List
+ salvaMetodo(m: MetodoPagamento): MetodoPagamento
```

### `TariffaRepository`

**Metodi**

```
+ findAll(): List
+ existsByTipologia(tipoMezzo: TipoMezzo): boolean
+ save(t: Tariffa): Tariffa
+ update(t: Tariffa): Tariffa
```

### `ZonaRepository`

**Metodi**

```
+ findByTipo(tipo: TipoZona): List
+ findContenenti(c: Coordinate): List
+ findZonaOperativaByPosizione(pos: Coordinate): Zona
+ findById(id: String): Zona
+ save(z: Zona): Zona
+ update(z: Zona): Zona
+ delete(id: String): void
```

---

## SERVER - Model (Domain / Entity)

### `Persona`

**Attributi**

```
- id: String
- email: String
- nome: String
- cognome: String
```

### `Utente`

**Attributi**

```
- statoAccount: StatoAccount
```

### `Operatore`

**Attributi**

```
- matricola: String
- azienda: String
```

### `AmministrazionePubblica`

**Attributi**

```
- codiceEnte: String
```

### `Recensione`

**Attributi**

```
- id: String
- idUtente: String
- voto: int
- commento: String
- dataCreazione: DateTime
```

### `Segnalazione`

**Attributi**

```
- id: String
- idUtente: String
- tipologia: String
- descrizione: String
- stato: StatoSegnalazione
- data: DateTime
```

### `ParametriSistema`

**Attributi**

```
- id: int
- durataMaxPrenotazione: int
- durataPeriodoGrazia: int
- maxMezziPerUtente: int
- addebitoPausa: Decimal
```

### `RegolaFineCorsa`

**Attributi**

```
- id: String
- tipoPolitica: TipoVincolo
- importoPenale: float
- bonusParcheggiCorretti: int
- bonusValore: Decimal
```

### `AbbonamentoUtente`

**Attributi**

```
- id: String
- idUtente: String
- idOfferta: String
- dataInizio: DateTime
- dataFine: DateTime
```

### `Abbonamento`

**Attributi**

```
- tipoMezzo: TipoMezzo
- prezzo: Decimal
- durataGiorni: int
```

### `Offerta`

**Attributi**

```
- id: String
- nome: String
- descrizione: String
- tipo: TipoOfferta
- stato: StatoOfferta
- dataCreazione: DateTime
- dataScadenza: DateTime
```

### `Promozione`

**Attributi**

```
- scontoPercentuale: Decimal
```

### `Prenotazione`

**Attributi**

```
- id: String
- dataOra: DateTime
- scadeAt: DateTime
- stato: StatoPrenotazione
- isGruppo: boolean
```

### `Corsa`

**Attributi**

```
- id: String
- oraInizio: DateTime
- oraFine: DateTime
- costoTotale: float
- stato: StatoCorsa
- distanzaPercorsa: float
- gruppoCorsaId: String
```

### `Mezzo`

**Attributi**

```
- id: String
- tipo: TipoMezzo
- latitudine: float
- longitudine: float
- statoMezzo: StatoMezzo
```

### `Tariffa`

**Attributi**

```
- id: String
- tipoMezzo: TipoMezzo
- costoPerMinuto: float
- costoPerKm: float
- aggiornataAt: DateTime
```

### `Pagamento`

**Attributi**

```
- id: String
- importo: float
- importoPieno: float
- dataOra: DateTime
- stato: StatoPagamento
- offertaApplicataId: String
```

### `MetodoPagamento`

**Attributi**

```
- id: String
- tipo: TipoMetodo
- predefinito: boolean
```

### `Zona`

**Attributi**

```
- id: String
- nome: String
- perimetro: Coordinate[]
- tipoZona: TipoZona
```

### `Suggerimento`

**Attributi**

```
- id: String
- utenteId: String
- tipo: TipoSuggerimento
- testo: String
- datiContesto: Object
- stato: StatoSuggerimento
- creatoAt: DateTime
```

---

## Sistemi esterni, Adapter & Note

### `Nota 1 — Client`

**Metodi**

```
Nessuna vista dipende da un'altra vista: lo stato di autenticazione si chiede ad AuthService («Singleton»). Le viste osservano i service tramite TanStack Query (pattern Observer). La Facade verso il server e' ApiService: i service di dominio traducono le operazioni del proprio dominio in chiamate ad ApiService.
```

### `Nota 2 — BLL`

**Metodi**

```
Lo stato del Mezzo cambia solo tramite ServizioMobilita (pattern State, transizioni valide esplicite). Il calcolo tariffa varia per tipologia di mezzo con il pattern Strategy (IIN-4: nuove tipologie senza modifiche strutturali).
```

### `Nota 3 — DAL`

**Metodi**

```
I repository sono l'unico livello che conosce le entita' ORM: convertono ORM ↔ Transfer Object verso la BLL (pattern DAO + Transfer Object). La BLL non importa mai dal Model.
```

### `GoogleMaps`

**Metodi**

```
+ recuperaDatiMappa(pos: Coordinate): DatiMappa
+ verificaZona(pos: Coordinate, idMezzo: String): Zona
```

### `Pagamenti`

**Metodi**

```
+ autorizza(metodo: MetodoPagamento, importo: float): TransactionId
+ validaDatiPagamento(tipologia: String, dati: Object): boolean
```

### `ProviderPagamentiAdapter`

**Metodi**

```
+ autorizza(metodo: MetodoPagamento, importo: float): TransactionId
+ validaDatiPagamento(tipologia: String, dati: Object): boolean
- chiamaGateway(req: Request): Response
```

### `IServizioAI`

**Metodi**

```
+ generaSuggerimenti(dati: Object): List
```

### `GoogleMapsAdapter`

**Metodi**

```
+ recuperaDatiMappa(pos: Coordinate): DatiMappa
+ verificaZona(pos: Coordinate, idMezzo: String): Zona
- chiamaApiGoogle(req: Request): Response
```

### `DBMS — Supabase PostgreSQL`

**Attributi**

```
- engine: Engine
- sessionLocal: SessionFactory
```

**Metodi**

```
+ executeQuery(sql: String): ResultSet
+ executeUpdate(sql: String): int
+ connectDB(): Session
```

### `Provider Pagamenti`

### `Google Maps`

### `ServizioAIAdapter`

**Metodi**

```
+ generaSuggerimenti(dati: Object): List
- chiamaModelloIA(prompt: String): Response
- valutaSufficienzaDati(dati: Object): boolean
```

### `ServizioAI`

---

## Relazioni tra layer

Il diagramma contiene **176** relazioni (in prevalenza dipendenze d'uso `Use`).
Riepilogo delle dipendenze direzionali tra layer (origine -> destinazione):

| Da (layer) | A (layer) | N. dipendenze |
|---|---|---|
| SERVER - Service (Business Logic Layer) | SERVER - Repository (Data Access Layer) | 29 |
| CLIENT - View (Presentation) | CLIENT - Service (API Service Layer) | 20 |
| SERVER - Model (Domain / Entity) | SERVER - Model (Domain / Entity) | 19 |
| SERVER - Controller (MVC / FrontController) | Contratti Controller -> BLL (interfacce) | 17 |
| CLIENT - Service (API Service Layer) | CLIENT - Service (API Service Layer) | 16 |
| SERVER - Repository (Data Access Layer) | SERVER - Repository (Data Access Layer) | 16 |
| SERVER - Repository (Data Access Layer) | SERVER - Model (Domain / Entity) | 16 |
| SERVER - Controller (MVC / FrontController) | SERVER - Controller (MVC / FrontController) | 14 |
| SERVER - Service (Business Logic Layer) | Contratti Controller -> BLL (interfacce) | 13 |
| Sistemi esterni, Adapter & Note | Sistemi esterni, Adapter & Note | 6 |
| SERVER - Service (Business Logic Layer) | Sistemi esterni, Adapter & Note | 3 |
| CLIENT - Service (API Service Layer) | SERVER - Controller (MVC / FrontController) | 1 |
| SERVER - Repository (Data Access Layer) | Sistemi esterni, Adapter & Note | 1 |
