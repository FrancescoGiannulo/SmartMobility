# Specifica Architetturale Dettagliata - Sistema di Mobilità Smart

Questo documento fornisce un'analisi profonda dell'architettura del sistema estratta dal diagramma delle classi. Il sistema utilizza un'architettura a livelli (N-Tier) e il pattern MVC (Model-View-Controller) esteso.

---

## 1. Livello PRESENTATION (Client / Viste)
Le viste rappresentano le interfacce utente del frontend (App/Web), suddivise per tipologia di attore.

### 1.1 Viste Utente (End-User)
* **VistaAccount:** Gestisce l'accesso. 
    * *Attributi:* `-nome`, `-cognome`, `-email`. 
    * *Metodi:* `+mostraFormLogin()`, `+mostraFormRegistrazione()`, `+mostraRecuperoCredenziali()`.
* **VistaHomepageUtente:** La mappa principale.
    * *Metodi:* `+apriMappa()`, `+mostraMappa(mezzi, zone)`, `+mostraErrore()`.
* **VistaPrenotazioneMezzo:** Flusso di prenotazione.
    * *Metodi:* `+selezionaMezzo()`, `+mostraConfermaprenotazione()`, `+mostraErroreDisponibilità()`.
* **VistaCorsa:** Gestione della corsa attiva.
    * *Metodi:* `+sblocca()`, `+mostraInfoCorsa()`, `+mostraAvvisoZonaVietata()`, `+terminaEPaga()`, `+mostraRiepilogoCorsa()`.
* **VistaPagamento:** Wallet e checkout.
    * *Metodi:* `+apriPortafoglio()`, `+mostraPortafoglio()`, `+aggiungiMetodopagamento()`, `+mostraRiepilogoPagamento()`, `+terminaEPaga()`.

### 1.2 Viste Operatore (Backend Management)
* **VistaDashboardOperatore:** Entry point per gli operatori della flotta.
    * *Metodi:* `+selezionaMappaOperatore()`, `+mostraMappaOperatore()`.
* **VistaMezziOperatore:** Gestione stato dei mezzi.
    * *Metodi:* `+apriGestioneMezzi()`, `+mostraListaMezzi()`, `+mostraFormModificaStato()`, `+confermaModificaStato()`, `+mostraFormAggiuntaMezzo()`, `+richiediDismissione()`.
* **VistaDefinisciZona:** Disegno del geofencing.
    * *Attributi:* `-tipoZona`.
    * *Metodi:* `+avviaDefinisciZona()`, `+mostraEditorMappa()`, `+confermaZona()`.
* **VistaImpostazioniRegole:** Definizione regole di fine corsa.
    * *Metodi:* `+apriConfigurazioneRegoleFineCorsa()`, `+mostraConfiguratoreRegoleFineCorsa()`, `+confermaRegoleFineCorsa()`.

### 1.3 Viste Amministrazione Pubblica (AP)
* **VistaDashboardAP:** Analisi e reportistica.
    * *Metodi:* `+visualizzaDashboard()`, `+mostraDashboardReport()`, `+esportaCSV()`, `+esportaPDF()`.
* **VistaTariffePromozioni:** Controllo prezzi.
    * *Metodi:* `+apriSezioneTariffe()`, `+mostraFormNuovaTariffa()`, `+confermaNuovaTariffa()`.

---

## 2. INTERFACCE DI COMUNICAZIONE (Contratti)
Il sistema usa interfacce esplicite per disaccoppiare i layer.
* **`ApiToView`**: Contratto che il frontend utilizza per invocare operazioni logiche sul backend (es. `+login()`, `+prenotaMezzo()`, `+creaZona()`, `+caricaMappa()`).
* **`ClientToServer` / `ServerToClient`**: Gestiscono i wrapper di rete HTTP (es. `+gestisciRisposta(Response)`, `+riceviNotifica(Evento)`).
* **`BLLToController`**: Espone la logica core ai Controller (es. `+creaPrenotazione(mezzoId, utenteId)`, `+calcolaImporto()`, `+definisciTariffa()`).
* **`ModelToBLL` & `DALtoModel`**: Interfacce per la serializzazione/idratazione degli oggetti dal DB alla memoria (es. `+crea(Entity)`, `+save(id)`).

---

## 3. Livello APPLICATION (Controller)
Implementa il pattern **Front Controller** tramite `AccountController`, che smista le richieste (Routing) e valida l'autenticazione.
* **AccountController:** `#basePath`, `#sessione`, `+handleRequest(Request)`, `#validaAutenticazione()`, `#instrada(path)`.
* **PrenotazioneUtenteController:** `+prenotazione()`, `+sblocca()`, `+terminaCorsa()`.
* **PagamentoController:** `+getMetodiPagamento()`, `+elaborapagamento()`, `+calcolaImporto()`.
* **ZoneController:** Restituisce `+zoneVietate()`, `+zoneLimitate()`, `+zonaOperativa()`, `+zoneParcheggio()`.

---

## 4. BUSINESS LOGIC LAYER (BLL)
Diviso architetturalmente in due sottonivelli: Facade (Servizi esposti via API) e Business Object Interni.

### 4.1 Livello Facade (Servizi API)
Tutti raggruppati dietro il Singleton `ApiService`.
* **AuthService:** `+login()`, `+registra()`, `+isAutenticato()`.
* **FlottaService:** `+getMezzi()`, `+aggiungiMezzo()`, `+dismetti()`, `+verificaDisponibilità()`.
* **MapService:** `-posizioneUtente`. `+cercaMezzi()`, `+caricaMappa()`.
* **PaymentService:** `-metodiPagamento`, `-metodoPredefinito`.
* **PrenotazioneService:** `+prenota()`, `+sblocca()`, `+terminaCorsa()`.
* **ZonaService / ReportService:** Coordinano i confini e le estrazioni dati.

### 4.2 Livello Core (Business Objects)
Ereditano dalla superclasse `Servizio` (`#logger`, `#handleBusinessException()`, `#validateEntity()`).
* **ServizioMobilità:** Gestisce lo stato fisico. `-corsaAttiva: Corsa`. Metodi: `+avviaCorsa()`, `+terminaCorsa()`, `+sbloccaMezzo()`, `+verificaPosizioneInZonaOperativa()`.
* **ServizioPrenotazione:** Logica asincrona. `-durataMax`, `-maxMezziGruppo`. Metodi: `+creaPrenotazione()`, `+verificaScadenza()`.
* **ServizioGIS:** Controllo geografico. `-zoneVietate`, `-zoneOperative`, `-zoneLimitate`. Metodi: `+verificaInZona()`, `+calcolaPercorso()`, `-validaPerimetro()`.
* **ServizioPricing:** Calcolo dinamico. `-tariffario`, `-promozioniAttive`, `-addebitoPausa`. Metodi: `+calcolaTariffa()`, `+elaboraPagamento()`.
* **ServizioUtenti & ServizioReport:** Gestione domini specifici (segnalazioni, sospensione account, generazione CSV/Report).

### 4.3 Servizi Esterni (Integrazioni)
* **`«interface» Pagamenti`**: Implementato dal provider esterno. Espone `+autorizza(metodoPagamento, importo)` e `+validaDatiPagamento()`.
* **`«interface» GoogleMaps`**: Espone `+recuperaDatiMappa()` e `+verificaZona()`.

---

## 5. DATA MODEL LAYER (Entità di Dominio e Relazioni)
Le classi contengono lo stato. Le relazioni indicano le regole di business del DB.

### Gerarchia Utenti
* **`Persona` (Superclasse):** `-id`, `-email`, `-nome`, `-cognome`.
    * **`Utente`:** `-statoAccount`.
    * **`Operatore`:** `-matricola`, `-azienda`.
    * **`AmministrazionePubblica`:** `-codiceEnte`.

### Entità Core e Molteplicità (Relazioni)
* **Mezzo:** `-tipo`, `-id`, `-latitudine`, `-longitudine`, `-statoMezzo`.
* **Corsa:** `-id`, `-oraInizio`, `-oraFine`, `-costoTotale`, `-stato`, `-distanzaPercorsa`.
* **Prenotazione:** `-id`, `-dataOra`, `-stato`, `-isGruppo`.
* **Pagamento:** `-id`, `-importo`, `-dataOra`, `-stato`.
* **MetodoPagamento:** `-id`, `-tipo`.
* **Tariffa:** `-id`, `-tipoMezzo`, `-costoPerMinuto`, `-costoPerKm`.
* **Zona:** `-id`, `-nome`, `-listaCoordinate`, `-tipoZona`.
* **RegolaFineCorsa:** `-id`, `-tipoPolitica`, `-importoPenale`.

**Relazioni Esplicite nel Diagramma:**
* **Utente (1) $\rightarrow$ MetodoPagamento (0..*):** Un utente ha zero o più metodi di pagamento salvati.
* **MetodoPagamento (1) $\rightarrow$ Pagamento (0..*):** Un metodo di pagamento può generare molti pagamenti storici.
* **Utente (1) $\rightarrow$ Prenotazione (0..*):** Un utente può avere uno storico di molte prenotazioni.
* **Prenotazione (0..1) $\rightarrow$ Corsa (0..1):** Una prenotazione si evolve (o meno) in una corsa. Rapporto 1 a 1 opzionale.
* **Corsa (0..*) $\rightarrow$ Mezzo (1):** Un singolo mezzo ha uno storico di molte corse associate.
* **Corsa (1) $\rightarrow$ Pagamento (1):** Ogni corsa genera esattamente un pagamento (ricevuta).
* **Operatore (1) $\rightarrow$ Tariffa (0..*):** L'operatore definisce listini tariffari multipli.
* **Operatore (1) $\rightarrow$ RegolaFineCorsa (0..*):** L'operatore definisce penali o incentivi per il rilascio in base alle zone.

---

## 6. DATA ACCESS LAYER (Persistenza / DAO)
Tutti i componenti di accesso ai dati (Repository) comunicano tramite l'interfaccia `DBMS` che espone i comandi base: `+executeQuery(sql)`, `+executeUpdate(sql)`, `+connettDB()`.

Tutti i repository ereditano dall'interfaccia base **`Repository <<DAO>>`** che garantisce metodi CRUD standard: `+save()`, `+update()`, `+delete()`.

* **UtenteRepository:** `+findByEmail(email)`, `+findById(id)`.
* **MezzoRepository:** `+findByStato(s)`, `+findDisponibili()`, `+findAll()`.
* **CorsaRepository:** `+findAttiva(idMezzo)`. Cruciale per ricollegarsi alle corse in corso in caso di disconnessione.
* **PrenotazioneRepository:** `+findAttiva(idUt)`, `+findScadute()`. (Usato dal CRON job per rilasciare i mezzi prenotati ma non sbloccati in tempo).
* **PagamentoRepository:** `+findByCorsa(idCorsa)`, `+findByUtente(idUt)`.
* **ZonaRepository:** `+findByTipo(t)`, `+findContenenti(Coordinate)`, `+findZonaOperativaByPosizione(posizione)`. Vitale per il ServizioGIS.
* **TariffaRepository:** `+existsByTipologia(tipologiaMezzo)`.
* **RegoleFineCorsaRepository:** Gestisce le politiche applicate (es. sconti parcheggio hub, penali fuori area).