
**Ciclo 4 · Versione 2.0 · Data di rilascio: 24/05/2026**

Ingegneria del Software a.A. 2025-2026 — Informatica e Tecnologie per la Produzione del Software

**Realizzato da:** Cardone Flavio (829469), De Astis Gabriele (826243), Giannulo Francesco (825071), Lacirignola Camilla (830465)

---

## Indice

- [1. PRODUCT BACKLOG](#1-product-backlog)
  - [1.1 Introduzione](#11-introduzione)
  - [1.2 Contesto di business](#12-contesto-di-business)
  - [1.3 Stakeholder](#13-stakeholder)
  - [1.4 Item funzionali](#14-item-funzionali)
  - [1.5 Item non funzionali](#15-item-non-funzionali)
- [2. SPRINT REPORT](#2-sprint-report)
  - [2.1 Sprint Backlog](#21-sprint-backlog)
  - [2.2 Product Requirement Specification](#22-product-requirement-specification)
  - [2.3 System Architecture](#23-system-architecture)
  - [2.4 Detailed Product Design](#24-detailed-product-design)
  - [2.5 Data modeling and design](#25-data-modeling-and-design)
- [3. PROMPT](#3-prompt)
  - [3.1 Qualità dei requisiti](#31-qualità-dei-requisiti)
  - [Context](#context)
- [Expected Input Format](#expected-input-format)
- [Quality Verification Characteristics](#quality-verification-characteristics)
  - [1. Non Ambiguo](#1-non-ambiguo)
  - [2. Provabile o Verificabile](#2-provabile-o-verificabile)
  - [3. Chiaro](#3-chiaro)
  - [4. Corretto](#4-corretto)
  - [5. Comprensibile](#5-comprensibile)
  - [6. Fattibile](#6-fattibile)
  - [7. Indipendente e Auto-consistente](#7-indipendente-e-auto-consistente)
  - [8. Atomico](#8-atomico)
  - [9. Necessario](#9-necessario)
  - [10. Astratto](#10-astratto)
  - [11. Consistente](#11-consistente)
  - [12. Non Ridondante](#12-non-ridondante)
  - [13. Completo](#13-completo)
  - [14. Metriche Derivate](#14-metriche-derivate)
- [Output Format](#output-format)
  - [3.2 Output Prompt Requisiti](#32-output-prompt-requisiti)
  - [3.3 Definizioni](#33-definizioni)
- [4. GLOSSARIO](#4-glossario)
  - [4.1 Acronimi](#41-acronimi)
  - [4.2 Definizioni](#42-definizioni)

---

## 1. PRODUCT BACKLOG

### 1.1 Introduzione

SMART MOBILITY è un sistema software progettato per supportare il Comune di Zootropolis nell'introduzione di un servizio integrato di mobilità urbana sostenibile, che mette a fattor comune diversi servizi di sharing (bike sharing, car sharing, e-scooter sharing e altri) in un'unica piattaforma accessibile a cittadini, operatori e amministrazione pubblica. Il Sistema si pone tre obiettivi macroscopici:
- Offrire ai cittadini un accesso rapido, sicuro e trasparente ai mezzi di sharing disponibili sul territorio
- Permettere agli operatori del servizio di gestire in modo efficiente la flotta, ridurre costi e fenomeni di vandalismo
- Consentire all'Amministrazione Pubblica di monitorare la mobilità urbana e assumere decisioni strategiche basate su dati Tali obiettivi si traducono in un insieme di funzionalità che coprono l'intero ciclo di utilizzo del servizio per soddisfare le esigenze delle tre categorie di utenti destinatari del sistema SMART MOBILITY — Utenti finali, Operatori del Servizio e Amministrazione Pubblica. Per quanto riguarda gli Utenti, SMART MOBILITY offre:
- Visualizzazione dei mezzi disponibili nelle vicinanze e del loro stato
- Prenotazione di uno o più mezzi e sblocco tramite dispositivo personale
- Pagamenti veloci e sicuri
- Garanzia di affidabilità del sistema, con meccanismi di prevenzione di frodi ed errori
- Promozioni, pausa della corsa e gestione del profilo di pagamento Per quanto riguarda gli Operatori del Servizio, SMART MOBILITY offre:
- Visualizzazione della distribuzione della flotta e notifiche sulle aree con bassa disponibilità, per ottimizzare la redistribuzione dei mezzi sul territorio

- Monitoraggio di malfunzionamenti, manutenzione pianificata e posizione dei mezzi a fine corsa, per ridurre i costi operativi e contenere i fenomeni di furto e vandalismo
- Bonus per parcheggio corretto, sospensione account in caso di frode e blocco automatico dei mezzi fuori dalle zone consentite
- Selezione di zone sensibili con divieto o limitazione del transito e definizione delle zone di parcheggio e del confine operativo Per quanto riguarda l'Amministrazione Pubblica, SMART MOBILITY offre:
- Monitoraggio della frequenza di utilizzo delle diverse tipologie di mezzo e dei pattern di mobilità urbana, a supporto delle decisioni strategiche di pianificazione
- Accesso a report aggregati per supportare decisioni strategiche sulla mobilità
- Analisi dello stato dei mezzi e delle tratte più utilizzate per pianificare manutenzioni e interventi urbani, contribuendo alla garanzia della sicurezza urbana
- Visualizzazione cartografica del territorio operativo per il monitoraggio del servizio sulla città

### 1.2 Contesto di business

Nel panorama urbano contemporaneo, caratterizzato da un'emergenza climatica sempre più pressante, dalla necessità di decongestionare i centri storici e dalla transizione verso modelli di "Smart City", emerge con forza l'esigenza di soluzioni integrate per la mobilità dolce e condivisa. SMART Mobility nasce per rispondere a questa sfida, superando la frammentazione degli attuali servizi di sharing e offrendo una piattaforma unica che connette cittadini, operatori privati e pubblica amministrazione. Il software è pensato per essere usato nei seguenti ambiti:
- Contesto di mobilità per i cittadini: in un ambiente urbano dove possedere un mezzo privato è sempre più costoso e inefficiente, i cittadini necessitano di strumenti che permettano di pianificare spostamenti intermodali in tempo reale. SMART Mobility offre un ecosistema che permette all'utente di localizzare, prenotare e pagare diversi tipi di mezzi (bici, monopattini, auto elettriche) tramite un'unica interfaccia, garantendo trasparenza sulle tariffe e sulla disponibilità, oltre a incentivare comportamenti virtuosi tramite bonus per il parcheggio corretto.

- Contesto operativo degli operatori di flotta: la gestione di una flotta di mezzi condivisi comporta sfide logistiche enormi, dal recupero dei mezzi scarichi alla manutenzione per atti vandalici. Gli operatori necessitano di strumenti avanzati per il monitoraggio costante della flotta, la gestione delle zone operative e l'ottimizzazione dei flussi di ridistribuzione. A questo scopo SMART Mobility mette a disposizione una "dashboard di controllo" che consente agli operatori di definire le zone vietate, le zone a circolazione limitata, le aree di parcheggio e il confine operativo della flotta, regolando in tempo reale la circolazione dei mezzi sul territorio. Il sistema permette inoltre ai gestori di massimizzare il tempo di attività dei mezzi, ridurre i costi di recupero e analizzare le zone a maggior rendimento.
- Contesto di governance dell'Amministrazione Pubblica: i comuni si trovano spesso a subire l'invasione di mezzi di sharing senza avere gli strumenti per monitorarli efficacemente. SMART Mobility offre alle amministrazioni una dashboard di monitoraggio che consente di osservare in tempo reale la distribuzione dei mezzi e lo stato del servizio sul territorio. Il sistema consente di raccogliere dati granulari sui flussi di traffico e di accedere a report aggregati, permettendo di pianificare infrastrutture ciclabili e pedonali basandosi su evidenze reali anziché su stime.
- Contesto di sostenibilità e monitoraggio ambientale: in un'epoca di obiettivi stringenti per la riduzione della CO2, cresce il bisogno di monitorare l'impatto ambientale dei trasporti. SMART Mobility risponde a questa esigenza fornendo statistiche aggregate sui chilometri percorsi con mezzi elettrici e sul risparmio di emissioni, permettendo sia all'utente che al Comune di visualizzare il proprio contributo concreto alla transizione ecologica. In questo scenario, SMART Mobility si propone come piattaforma integrata che supera i limiti dei singoli servizi proprietari, offrendo un'esperienza fluida e centralizzata che risponde alle esigenze di tutti gli attori della mobilità urbana.

### 1.3 Stakeholder

Il sistema SMART Mobility coinvolge diversi stakeholder che interagiscono con la piattaforma con ruoli e obiettivi specifici. Di seguito sono descritti i principali attori del sistema:
1. Utente:
È l'utente che usufruisce dei mezzi di mobilità condivisa. Deve essere registrato per utilizzare la mappa, per localizzare i mezzi, per noleggiare e pagare. Le tipologie di Utente sono:
- Pendolare Urbano: Persona che utilizza regolarmente il servizio per coprire l'ultimo miglio (es. da stazione a ufficio) e cerca affidabilità e abbonamenti convenienti.
- Utente Occasionale: Residente che utilizza il servizio saltuariamente per necessità impreviste o svago.
- Turista: Visitatore che necessita di un accesso rapido e senza frizioni per esplorare la città in modo sostenibile.
2. Operatore del Servizio:
Rappresenta l'azienda che immette i mezzi sulla strada. Gestisce il business e la manutenzione. Le tipologie di figure interne all'Operatore sono:
- Manager del Servizio: Definisce i piani tariffari, le promozioni, le zone operative e le zone soggette a restrizioni per massimizzare il profitto e regolare la circolazione dei mezzi.
- Team Logistico e Manutentori: Personale sul campo che si occupa della ricarica delle batterie, della riparazione dei guasti e dello spostamento fisico dei mezzi nelle zone ad alta richiesta.
3. Amministrazione Pubblica:
Ente che detiene la sovranità sul suolo pubblico e definisce le regole del gioco. Le figure coinvolte sono:
- Pianificatore Urbano/Mobility Manager: Utilizza i dati e i report aggregati della piattaforma per analizzare i flussi di mobilità, studiare nuovi percorsi ciclabili e supportare le decisioni strategiche di pianificazione urbana.

### 1.4 Item funzionali

Contiene l’elenco e la specifica di tutti i requisiti funzionali espressi attraverso lo schema delle user stories:

#### 1.4.1 IF-UT.01 – Visualizza Mappa Utente

Come utente, Voglio visualizzare la Mappa Utente, Così da poter scegliere un mezzo.

#### 1.4.2 IF-UT.02 – Prenota mezzo

Come utente, Voglio prenotare uno o più mezzi disponibili, Così da trovarli riservati al mio arrivo.

#### 1.4.4 IF-UT.03 – Sblocca mezzo

Come utente, Voglio sbloccare uno o più mezzi disponibili, Così da avviare fisicamente la corsa.

#### 1.4.5 IF-UT.04 – Termina Corsa

Come utente, Voglio terminare la corsa Così da liberare il mezzo.

#### 1.4.6 IF-UT.05 – Effettua Pagamento

Come utente, Voglio che il sistema addebiti automaticamente l'importo sul mio metodo di pagamento predefinito al termine della corsa, Così da non dover effettuare transazioni manuali ogni volta che scendo dal mezzo.

#### 1.4.7 IF-UT.06 – Salva Metodi Pagamento

Come utente, Voglio salvare uno o più metodi di pagamento, Così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati.

#### 1.4.8 IF-UT.07 – Consulta tariffe

Come utente, Voglio consultare il tariffario per ciascuna tipologia di mezzo, Così da confrontarne i costi

#### 1.4.9 IF-UT.08 – Visualizza Riepilogo corsa

Come utente, Voglio ricevere il riepilogo corsa, Così da visualizzare le informazioni sulla corsa effettuata

#### 1.4.10 IF-UT.09 – Sospende Corsa

Come utente, Voglio mettere in pausa la corsa, Così da effettuare soste senza perdere il possesso del mezzo.

#### 1.4.11 IF-UT.10 – Visualizza Promozioni

Come utente, Voglio accedere alle promozioni attive, Così da ridurre i costi di utilizzo del servizio.

#### 1.4.12 IF-UT.11 – Visualizza Storico Corsa

Come utente, Voglio visualizzare lo storico delle corse, Così da tenere traccia di tutte le corse effettuate.

#### 1.4.13 IF-UT.12 – Invia Segnalazione

Come utente, Voglio inviare una segnalazione, Così da informare l'operatore affinché possa intervenire.

#### 1.4.14 IF-UT.13 – Sottoscrive Abbonamento

Come utente, Voglio sottoscrivere un abbonamento, Così da usufruire di condizioni tariffarie agevolate.

#### 1.4.18 IF-AP.01 – Accede Report

Come amministrazione pubblica, Voglio accedere a report aggregati sull'utilizzo del servizio, Così da supportare decisioni strategiche di pianificazione.

#### 1.4.15 IF-AP.02 – Esporta Report

Come amministrazione pubblica, Voglio esportare i report aggregati sull'utilizzo del servizio in Formato Esportabile, Così da utilizzarli in analisi esterne e documentazione ufficiale.

#### 1.4.16 IF-AP.03 – Visualizza Mappa Amministrazione Pubblica

Come amministrazione pubblica, Voglio visualizza la mappa, Così da monitorare il servizio sulla citta.

#### 1.4.17 IF-OP.01 – Visualizza Mappa Operatore

Come operatore, Voglio visualizzare la Mappa Operatore, Così da pianificare operazioni di redistribuzione.

#### 1.4.18 IF-OP.02 – Aggiunge Mezzo

Come operatore, Voglio aggiungere un nuovo mezzo alla mappa, Così da aumentare il numero di mezzi della flotta.

#### 1.4.19 IF-OP.03 – Dismette Mezzo

Come operatore, Voglio dismettere un mezzo dalla mappa, Così da gestire il ciclo di vita della flotta.

#### 1.4.20 IF-OP.04 – Modifica Stato Mezzo

Come operatore, Voglio modificare lo Stato di un mezzo, Così da nasconderlo o mostrarlo sulla Mappa Utente.

#### 1.4.21 IF-OP.05 – Definisce Tariffa

Come operatore, Voglio definire la tariffa del servizio, Così da permettere la configurazione del modello di costo.

#### 1.4.22 IF-OP.06 – Definisce Regole Fine Corsa

Come Operatore Voglio Definire regole sanzionatorie per i rilasci dei mezzi al di fuori delle aree di parcheggio consentite Così da garantire il decoro urbano

#### 1.4.23 IF-OP.07 - Definisce Zone

Come operatore, Voglio definire i confini di una Zona, Così da garantire il rispetto delle normative locali.

#### 1.4.24 IF-OP.08 – Gestisce Segnalazioni

Come operatore, Voglio leggere le segnalazioni inviate dagli utenti, Così da pianificare gli interventi di manutenzione.

#### 1.4.25 IF-OP.09– Sospende Account Utente

Come operatore, Voglio sospendere l'account di un utente, Così da tutelare l'integrità del servizio

#### 1.4.26 IF-OP.10– Definisce Offerte

Come operatore, Voglio definire promozioni con condizioni e scadenza configurabili, Così da incentivare l'utilizzo del sistema con politiche commerciali flessibili.

#### 1.4.27 IF-OP.11 – Configura Parametri Sistema

Come operatore, Voglio configurare i parametri relativa al sistema, Così da stabilire dei limiti di utilizzo.

### 1.5 Item non funzionali

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali.

#### 1.5.1 Item Informativi

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali di tipo informativo.

##### 1.5.1.1 IIN-1 Prestazioni

- Il sistema deve aggiornare la posizione dei mezzi sulla Mappa Utente entro x secondi dall'ultimo rilevamento GPS (da testare)
- Il sistema deve completare l'operazione di prenotazione di un mezzo entro x secondi dalla richiesta dell'utente (da testare)

##### 1.5.1.2 IIN-2 Sicurezza

- Tutte le comunicazioni tra client e server devono essere cifrate mediante protocolli di sicurezza standard
- Il sistema deve bloccare un account dopo 5 tentativi di autenticazione falliti consecutivi in un tempo configurabile dall’operatore
- I dati personali degli utenti devono essere trattati in conformità al Regolamento UE 2016/679 (GDPR)
- Ciascun ruolo (UT, OP, AP) deve poter accedere esclusivamente alle funzionalità ad esso assegnate

##### 1.5.1.3 IIN-3 Usabilità

- L'interfaccia deve essere accessibile secondo le linee guida WCAG (es. per utenti con disabilità visive)
- L’interfaccia deve essere facile da usare e comprensibile in meno di x minuti

##### 1.5.1.4 IIN-4 Scalabilità

- L'architettura deve permettere l'aggiunta di nuove tipologie di mezzo senza modifiche strutturali

##### 1.5.1.5 IIN-5 Portabilità

- Il sistema deve essere accessibile tramite browser web su dispositivi desktop e mobile, senza necessità di installazione

##### 1.5.1.6 Conformità

- I report esportabili in CSV/PDF (AP.06) devono rispettare eventuali standard di formato richiesti dalla pubblica amministrazione

#### 1.5.2 Item di interfaccia

Contiene i requisiti di interfaccia espressi tramite mockup.

##### 1.5.2.1 IUI-1 - Schermata di Login Utente

Il mockup illustra l'interfaccia di autenticazione iniziale, caratterizzata da un design clean su sfondo bianco. La parte superiore ospita il logo del sistema, sottolineando la vocazione ecosostenibile del brand. Al centro si trova il form di accesso, con campi di input arrotondati per Username e Password, completato dal link per il recupero credenziali. Le Call to Action sono gestite da due grandi pulsanti in verde acqua con ombreggiature ("LOGIN" e "SIGN UP"), seguiti in basso dai collegamenti per il social login rapido (Google e Apple).

##### 1.5.2.2 IUI-2 – Homepage Utente

Questo mockup mostra l'interfaccia cartografica principale dell'app. La top bar offre l'accesso al profilo utente e al menu laterale tramite icona ad hamburger. Al centro, la mappa interattiva geolocalizza in tempo reale la flotta disponibile utilizzando pin codificati per colore e icona (monopattini in verde, bici in blu, auto in magenta). Sulla mappa è visibile un'area evidenziata in rosso (una geo-fence per zone a sosta vietata o velocità limitata) e un marker di posizione. Nella parte inferiore, due pulsanti floating permettono di avviare una "CORSA DI GRUPPO" o lo "SBLOCCA MEZZO". Chiude la schermata una bottom navigation bar per lo spostamento rapido tra le sezioni principali.

##### 1.5.2.3 IUI-3 – Menu Laterale Utente

Il mockup illustra il side drawer (menu laterale a scomparsa) aperto, che scorre da destra sovrapponendosi alla mappa di sfondo, la quale risulta oscurata per mantenere il focus dell'utente. L'intestazione presenta il logotipo del brand affiancato da una chiara icona "X" per la chiusura del pannello. L'architettura dell'elenco voci allinea testo e icone vettoriali (declinate nel verde acqua aziendale) sul lato destro, favorendo una lettura rapida. Le opzioni di navigazione garantiscono l'accesso immediato alle sezioni gestionali e amministrative dell'utente, coprendo l'area personale (Profilo,

Impostazioni, Guida) e la sfera economica/operativa (Piano Tariffario, Bonus e Promozioni, Cronologia, Portafoglio). Il layout adotta uno spazio bianco generoso per un design pulito e leggibile.

##### 1.5.2.4 IUI-4 – Corsa di Gruppo

Il mockup presenta l'interfaccia di gestione per le corse multiple, implementata tramite un pannello a comparsa inferiore (bottom sheet) sovrapposto parzialmente alla mappa. L'intestazione, dotata di icona di chiusura rapida, introduce la funzione "Inizia corsa di gruppo" seguita da un contatore dinamico di stato ("Veicoli sbloccati: 3/5"). Il corpo centrale elenca i veicoli già agganciati alla sessione tramite singole cards arrotondate; ciascuna scheda fornisce dati in tempo reale mostrando l'icona del mezzo, il codice identificativo alfanumerico e l'indicatore visivo della batteria (con colorazione semantica verde/giallo). Nella parte inferiore è posizionata la Call to Action ("SBLOCCA VEICOLO"), un pulsante primario per aggiungere ulteriori mezzi prima dell'avvio definitivo della corsa.

##### 1.5.2.5 IUI-5 – Prenotazione Mezzo

Il mockup illustra l'interfaccia per la prenotazione di un singolo veicolo, realizzata tramite un bottom sheet che si sovrappone alla mappa. Sulla cartina, il mezzo selezionato è enfatizzato da un pin verde ingrandito. Il pannello, intitolato "Prenota mezzo" con relativa icona di chiusura, riepiloga i dati cruciali: tipologia (Monopattino), codice identificativo e stato visivo della batteria. Un testo informativo avvisa chiaramente l'utente del limite temporale esatto entro cui raggiungere e sbloccare il mezzo. Il flusso si conclude con la Call to Action "Prenota", un pulsante primario ben delineato che attiva il blocco temporaneo del veicolo, garantendo all'utente un'interazione fluida e priva di ambiguità.

##### 1.5.2.6 IUI-6 – Visualizzazione del Piano Tariffario

Questo mockup rappresenta la sezione informativa sui costi del servizio, strutturata con un layout minimale e ampio spazio bianco per massimizzare la leggibilità. L'header presenta il titolo della sezione affiancato da un'icona di chiusura rapida. Al centro, tre card dal design a pillola con morbida ombreggiatura illustrano le tariffe chilometriche per ogni categoria di veicolo (Monopattino a 0,20€/km, Bicicletta a 0,30€/km, Automobile a 0,50€/km), accostando icone stilizzate ai relativi costi per un'immediata comprensione visiva. Completa l'interfaccia il logo aziendale centrato nella parte inferiore e la bottom navigation bar fissa, che garantisce continuità nell'esplorazione dell'app.

##### 1.5.2.7 IUI-7 – Visualizzazione del Saldo e Metodi di Pagamento

Il mockup illustra l'interfaccia di gestione finanziaria ("Portafoglio"). La gerarchia visiva pone in primo piano una card delimitata in verde acqua che evidenzia a grandi caratteri il "Saldo" disponibile. La sezione sottostante dedicata ai "Metodi di Pagamento" è organizzata in un menu a lista provvisto di chevron direzionali per suggerire l'interazione. Questo blocco integra opzioni di digital wallet (Google Pay, Apple Pay, PayPal) e una voce per l'aggiunta di carte di credito, tutte corredate da loghi o icone di riconoscimento rapido. L'operatività è demandata alla Call to Action primaria "RICARICA SALDO", un pulsante pill-shaped ad alto contrasto per il top-up del conto. Lo stile mantiene il layout pulito dell'applicativo, chiudendosi con la bottom navigation bar di sistema.

##### 1.5.2.8 IUI-8 – Schermata Info Corsa

Il mockup illustra il cruscotto di monitoraggio attivo durante il noleggio. L'interfaccia si apre con un'icona circolare in evidenza che identifica la tipologia di veicolo in uso (monopattino). La parte centrale espone la telemetria della sessione in tempo reale tramite un layout tabellare chiaro: riporta l'ID alfanumerico del mezzo, l'indicatore grafico della batteria, il timer del tempo trascorso e i chilometri percorsi. Nella sezione inferiore, sotto il logo aziendale, sono collocate due Call to Action operative tramite ampi pulsanti pill-shaped. Il sistema offre all'utente il pieno controllo dell'iter di viaggio, consentendo di sospendere temporaneamente la sessione ("PAUSA CORSA") o di concluderla procedendo alla fatturazione ("TERMINA E PAGA").

##### 1.5.2.9 IUI-9 – Visualizzazione della Cronologia Corse

Il mockup illustra la sezione "Cronologia Corse", progettata per fornire all'utente lo storico dettagliato dei propri noleggi. L'interfaccia adotta un layout a lista lineare, utilizzando divisori orizzontali continui per segmentare visivamente le singole sessioni. Ogni voce (list item) espone sulla sinistra un'icona vettoriale identificativa del veicolo (monopattino, bicicletta o automobile), garantendo un riconoscimento visivo immediato. Sulla destra, i dati riepilogativi della corsa sono ordinatamente incolonnati: ID del mezzo, durata ("Tempo trascorso"), distanza ("Km percorsi") e data. Questa architettura dell'informazione modulare e minimalista assicura una facile leggibilità e un'ottima scansionabilità. Chiudono la schermata l'header con comando di chiusura rapida e la bottom navigation bar di sistema.

##### 1.5.2.10 IUI-10 – Schermata Login Operatore/Amministrazione Pubblica

Questo mockup illustra l'adattamento landscape (orizzontale) dell'interfaccia di autenticazione, utilizzato da operatore e amministrazione pubblica. Il layout mantiene intatta la coerenza visiva, cromatica e funzionale della controparte mobile, raggruppando gli elementi in un blocco centrale ben allineato. Troviamo in sequenza: il logo, il form di input per Username e Password, i pulsanti primari di LOGIN e SIGN UP, e le opzioni per il social

login rapido in basso. L'utilizzo abbondante di spazio bianco (white space) ai lati focalizza l'attenzione dell'utente sull'azione di accesso, garantendo un'esperienza utente pulita e senza distrazioni anche su schermi ampi.

##### 1.5.2.11 IUI-11 – Dashboard Amministrazione Pubblica

Il mockup illustra la dashboard web dedicata all’amministrazione pubblica. Il layout landscape è strutturato in due macroaree funzionali: a sinistra, un ampio visualizzatore cartografico interattivo (basato su Google Maps) per il monitoraggio del territorio operativo; a destra, un pannello di controllo lineare che riporta il branding aziendale. Le operazioni sono demandate a quattro pulsanti pill-shaped ad alto contrasto che consentono la gestione visiva del geofencing ("DEFINISCI ZONE VIETATE", "DEFINISCI ZONE LIMITATE", "DEFINISCI ZONE PARCHEGGIO") e l'accesso alle statistiche ("VISUALIZZA REPORT"). L'affiancamento diretto tra la mappa di lavoro e i comandi operativi garantisce all'amministratore un'esperienza utente efficiente e priva di attriti durante il setup del servizio cittadino.

##### 1.5.2.12 IUI-12 – Definizione Zone Vietate

L'interfaccia illustra il flusso di geofencing lato amministratore per la gestione delle aree vietate. Sulla sinistra, la mappa funge da canvas interattivo: l'utente posiziona nodi per tracciare un poligono rosso, circoscrivendo visivamente la zona urbana soggetta a restrizione. A destra, un pannello contestuale fornisce istruzioni testuali chiare e coordinate cromaticamente. La parametrizzazione della regola avviene in basso tramite pulsanti toggle: l'operatore seleziona a quali veicoli applicare il divieto (es. l'opzione "Automobile" è attiva e confermata da una spunta visibile). Il layout, completato da un'icona di annullamento rapido in alto a destra, sfrutta il paradigma della manipolazione diretta per ottimizzare il setup del sistema e ridurre il carico cognitivo.

##### 1.5.2.13 IUI-13 – Definizione Zone Limitate

Il mockup mostra la funzionalità amministrativa per la creazione di zone a traffico o velocità limitata. Sfruttando lo stesso paradigma di interazione del tracciamento zone vietate, la mappa permette di disegnare un poligono interattivo tramite nodi. In questo caso, il sistema utilizza semanticamente il colore arancione sia per l'area tracciata che per le parole chiave nel testo esplicativo, indicando una restrizione parziale. Il pannello laterale destro consente all'amministratore di selezionare tramite interruttori toggle a quale categoria di mezzo applicare la limitazione (nell'esempio, è spuntata "Automobile"). La coerenza visiva e procedurale con le altre schermate di geofencing garantisce un'elevata learnability del sistema.

##### 1.5.2.14 IUI-14 – Definizione Zone di Parcheggio

L'interfaccia illustra la funzione amministrativa dedicata alla mappatura delle aree di sosta. Adottando il medesimo pattern d'interazione, la mappa a sinistra consente di tracciare un poligono interattivo, qui declinato semanticamente nel colore verde per indicare un'area consentita. A destra, il pannello laterale permette di associare il parcheggio a specifiche categorie di veicoli tramite i consueti controlli toggle (nell'esempio, "Automobile").

##### 1.5.2.15 IUI-15 – Visualizzazione dei Report

L'interfaccia di reportistica offre all'amministratore una dashboard analitica sull'utilizzo della flotta. La vista si articola in due grafici principali: a sinistra, un istogramma a barre impilate analizza il volume dei noleggi su base settimanale; a destra, un grafico a torta illustra la quota di mercato (in percentuale) per tipologia di mezzo. L'operatività è garantita da due pulsanti in basso che abilitano l'esportazione dei dati in formato CSV e PDF.

##### 1.5.2.16 IUI-16 – Dashboard Operatore

Il mockup illustra la dashboard web dell'operatore con layout split-screen landscape. A sinistra la Mappa Operatore (Google Maps) geolocalizza la flotta tramite pin cromatici per tipologia: monopattini in verde, biciclette in blu, automobili in magenta. In basso sulla mappa due pulsanti floating gestiscono "AGGIUNGI MEZZO" e "DISMETTI MEZZO". Il pannello destro espone sei pulsanti pill-shaped con icone esplicative: "GESTISCI SEGNALAZIONI", "GESTISCI UTENTI", "IMPOSTAZIONI REGOLE", "TARIFFE E PROMOZIONI", "VISUALIZZA REPORT" e "GESTISCI MEZZI". In alto a destra è presente l'icona di accesso al profilo; in basso il logo SMART MOBILITY.

##### 1.5.2.17 IUI-17 – Gestione Segnalazioni

L'interfaccia illustra la schermata dedicata al customer care lato amministratore, strutturata tramite un rigoroso layout tabellare (data grid). Le colonne categorizzano i ticket in entrata esponendo in modo ordinato: identificativo utente, timestamp (data e ora), tipologia di problematica (espressa visivamente tramite icone semantiche per veicoli specifici o alert di sistema) e il dettaglio testuale del disservizio. L'operatività diretta è delegata al pulsante Call to Action "RISPONDI" posto in coda a ciascuna riga, che innesca il flusso di presa in carico del problema.

##### 1.5.2.18 IUI-18 – Gestione Tariffe e Promozioni

Il mockup illustra il pannello di configurazione economica del servizio, con layout a due card affiancate e chiusura rapida tramite "X". La card sinistra mostra per ciascuna tipologia di mezzo (Monopattino, Bicicletta, Automobile) un valore numerico editabile e un selettore di unità di misura — evidenziato da un bordo squadrato — che consente all'operatore di scegliere la metrica tariffaria applicata (nell'esempio: €/km).

La card destra mostra la promozione attiva tramite un blocco pill-shaped verde acqua e la Call to Action "AGGIUNGI PROMOZIONE".

##### 1.5.2.19 IUI-19 – Schermata di Impostazione Regole

Il mockup illustra il pannello amministrativo per la configurazione delle business rules di sistema. L'interfaccia adotta una singola e ampia card strutturata a lista, dove i parametri operativi sono linearmente modificabili tramite campi di input numerici (es. durata massima della prenotazione, tolleranza della pausa, limiti di prenotazione simultanea per utente e percentuali tariffarie). L'ultima riga mostra un menu a tendina (dropdown), qui raffigurato nel suo stato espanso, progettato per selezionare la politica sanzionatoria in caso di sosta fuori zona (penale, divieto o semplice avviso).

#### 1.5.3 Item Qualitativi

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali di tipo qualitativo.

##### 1.5.3.1 IQ-1

##### 1.5.3.2 IQ-2

##### 1.5.3.3 IQ-n

#### 1.5.4 Altri Item

SPRINT REPORT N. 1 CICLO 4 SMART MOBILITY

## 2. SPRINT REPORT

### 2.1 Sprint Backlog

Tabella di riepilogo che indica, per ognuno degli Sprint successivi allo Sprint n.0, la lista degli item del Product Backlog, evidenziando quelli che verranno implementati nell’ambito dello sprint corrente unitamente ad una descrizione esplicativa. Per semplificare l’esposizione e salvaguardare la tracciabilità tra semilavorati si è proceduto alle seguenti assunzioni:
- All’interno di uno Sprint sono implementati un sottoinsieme di item tra quelli specificati nel Product Backlog
- Lo Sprint Backlog relativo allo sprint corrente contiene pertanto l’insieme degli item del Product Backlog in corso di implementazione
- Gli Item funzionali, ovvero le User Stories dovranno essere tracciabili uno a uno, auspicabilmente seppur non necessariamente, con i casi d’uso
- Ad ogni caso d’uso dovrà essere associato uno scenario di base più gli eventuali scenari alternativi. Lo scenario in prima istanza viene redatto a partire dalla specifica della User Story riportata nel Product Backlog
- Ad ogni caso d’uso dovrà essere associato un diagramma di sequenza. Ogni sprint deve necessariamente produrre in output del codice funzionante. L’unica eccezione è rappresentata dallo Sprint n°0 che deve essere utilizzato per disegnare la macroarchitettura del sistema con le sue componenti e le sue interfacce, e che sarà utilizzata come roadmap per gli sprint successivi andando a chiarire dove si colloca quanto realizzato in ciascuno di essi. Codice Item Numero Sprint Note UT.01 Sprint 1 Visualizza Mappa utente UT.02 Sprint 1 Prenota mezzo UT.03 Sprint 1 Sblocca mezzo UT.04 Sprint 1 Termina Corsa

UT.05 Sprint 1 Effettua Pagamento UT.06 Sprint 1 Salva metodo di pagamento AP.01 Sprint 1 Accede report OP.01 Sprint 1 Visualizza Mappa Operatore OP.02 Sprint 1 Aggiunge mezzo OP.03 Sprint 1 Dismette mezzo OP.04 Sprint 1 Modifica stato mezzo OP.05 Sprint 1 Definisce tariffa OP.06 Sprint 1 Definisce regole fine corsa OP.07 Sprint 1 Definisce Zona UT.07 Sprint 2 Consulta Tariffe UT.08 Sprint 2 Visualizza Riepilogo Corsa UT.09 Sprint 2 Sospende Corsa UT.10 Sprint 2 Visualizza Promozioni UT.11 Sprint 2 Visualizza Storico Corsa UT.12 Sprint 2 Invia Segnalazione UT.13 Sprint 2 Sottoscrive Abbonamento AP.02 Sprint 2 Esporta Report AP.03 Sprint 2 Visualizza Mappa Amministrazione Pubblica OP.08 Sprint 2 Gestisce Segnalazione OP.09 Sprint 2 Sospende Account Utente OP.10 Sprint 2 Definisce Offerta OP.11 Sprint 2 Configura parametri numerici di sistema

### 2.2 Product Requirement Specification

#### 2.2.1 Diagramma dei Casi d’uso

#### 2.2.2 Specifiche dei Casi d’uso

##### 2.2.2.1 UT – 01 Visualizza Mappa utente

| Campo | Valore |
|---|---|
| **Nome** | Visualizza Mappa Utente |
| **ID** | UT-01 |
| **Breve descrizione** | Il sistema mostra all'Utente autenticato la mappa interattiva<br>con i mezzi disponibili nelle vicinanze, le zone con<br>restrizioni e le zone di parcheggio, così da poter scegliere<br>un mezzo da prenotare o sbloccare. |
| **Attori Primari** | Utente |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L’utente è autenticato alla piattaforma |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Utente accede alla<br>schermata principale della piattaforma.<br>2. Il sistema rileva la posizione geografica corrente<br>dell'Utente tramite il dispositivo.<br>3. Il sistema interroga il ServizioGIS per recuperare i<br>dati geografici.<br>4. Il sistema recupera le zone con restrizioni e le zone<br>di parcheggio.<br>5. Il sistema visualizza la mappa con i soli mezzi<br>disponibili per tipologia, le aree con restrizioni, le<br>zone di parcheggio e il marker della posizione<br>corrente. |
| **Post-condizioni** | La mappa è visualizzata con i dati aggiornati; l'Utente può<br>procedere con la prenotazione o lo sblocco di un mezzo. |
| **Sequenza alternativa degli eventi** | Nessuna |

##### 2.2.2.2 UT – 02 Prenota Mezzo

| Campo | Valore |
|---|---|
| **Nome** | Prenota Mezzo |
| **ID** | UT - 02 |

| Campo | Valore |
|---|---|
| **Breve descrizione** | L'Utente seleziona uno o più mezzi sulla mappa; per ogni<br>mezzo il sistema mostra le caratteristiche e offre la<br>possibilità di aggiungere mezzi nelle vicinanze. Una volta<br>completata la selezione (1 ≤ N ≤ N_max), il sistema avvia<br>la prenotazione di tutti i mezzi scelti. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | 1.L'Utente è autenticato<br>2.Esiste almeno un mezzo disponibile nelle vicinanze;<br>3.Il numero massimo di mezzi prenotabili (N_max ≥ 1) e il<br>raggio di selezione gruppo sono stati configurati<br>dall'Operatore. |
| **Sequenza principale degli eventi** | Il caso d'uso inizia quando l'Utente vuole prenotare uno o<br>più mezzi sulla mappa.<br>L'Utente seleziona un mezzo disponibile sulla mappa.<br>Il sistema mostra le caratteristiche del mezzo selezionato.<br>Se N < N_max, il sistema offre all'Utente la possibilità di<br>aggiungere altri mezzi nelle vicinanze (entro il raggio<br>configurato dall'Operatore).<br>L'Utente sceglie se aggiungere altri mezzi (torna al passo<br>2) oppure procedere con la selezione corrente.<br>L'Utente conferma la selezione e avvia la prenotazione.<br>Il sistema verifica che tutti i mezzi selezionati siano ancora<br>disponibili.<br>Per ogni mezzo selezionato, il sistema crea una<br>prenotazione associando il mezzo all'Utente.<br>Per ogni mezzo prenotato, il sistema aggiorna lo stato da<br>"Disponibile" a "Prenotato" e avvia il timer di prenotazione.<br>Il sistema notifica l'Utente con la conferma di tutte le<br>prenotazioni e il tempo rimanente. |
| **Post-condizioni** | Tutti gli N mezzi selezionati risultano nello stato<br>"Prenotato" e associati all'Utente; N timer di prenotazione<br>sono avviati. |

| Campo | Valore |
|---|---|
| **Sequenza alternativa degli eventi** | MezzoNonDisponibile |
| **Nome** | Prenota Mezzo: MezzoNonDisponibile |
| **ID** | UT – 02.1 |
| **Breve descrizione** | Uno o più dei mezzi selezionati risultano non più<br>disponibili al momento della conferma. Il sistema rimuove<br>dalla selezione solo i mezzi non disponibili e consente<br>all'Utente di sostituirli o di procedere con i restanti. |
| **Attori primari** | Utente |
| **Attori secondari** | nessuno |
| **Precondizioni** | Almeno un mezzo del gruppo selezionato è passato allo<br>stato "Prenotato" o "In Uso" prima del completamento della<br>richiesta. |
| **Postcondizioni** | I mezzi ancora disponibili risultano nello stato "Prenotato";<br>l'Utente non ha prenotazioni attive solo se tutti i mezzi<br>selezionati erano non disponibili. |
| **Sequenza alternativa degli eventi** | Il caso d’uso inizia dopo il passo 7 della sequenza<br>principale.<br>Il sistema rimuove dalla selezione i mezzi non più<br>disponibili e informa l'Utente.<br>Il sistema mostra la lista aggiornata dei mezzi disponibili<br>nelle vicinanze.<br>L'Utente sceglie se aggiungere un mezzo sostitutivo (torna<br>al passo 2 del flusso principale) oppure procedere con i<br>mezzi rimanenti.<br>Se rimane almeno un mezzo nella selezione, il sistema<br>riprende dal passo 8 del flusso principale.<br>Se la selezione è vuota, il caso d'uso termina senza<br>prenotazioni attive. |

##### 2.2.2.3 UT – 03 Sblocca Mezzo

| Campo | Valore |
|---|---|
| **Nome** | Sblocca Mezzo |
| **ID** | UT - 03 |
| **Breve descrizione** | L'Utente avvia la procedura di sblocco fisico di uno o più<br>mezzi; il sistema verifica le condizioni per ciascun mezzo<br>e abilita l'utilizzo di quelli sbloccati con successo. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | 1. L'Utente è autenticato;<br>2.L'Utente si trova in prossimità dei mezzi da sbloccare;<br>3.Ogni mezzo selezionato è nello stato "Prenotato"<br>dall'Utente corrente oppure nello stato "Disponibile". |
| **Sequenza principale degli eventi** | Il caso d'uso inizia quando l'Utente vuole sbloccare uno o<br>più mezzi.<br>Il sistema mostra all'Utente i mezzi sbloccabili: quelli con<br>prenotazione attiva a suo nome e quelli disponibili nelle<br>vicinanze.<br>L'Utente seleziona i mezzi da sbloccare.<br>Per ogni mezzo selezionato, il sistema verifica che l'Utente<br>si trovi entro la distanza massima consentita.<br>Per ogni mezzo, il sistema invia il comando di sblocco.<br>Ogni mezzo conferma l'avvenuto sblocco al sistema.<br>Per ogni mezzo sbloccato, il sistema aggiorna lo stato a<br>"In Uso" e registra l'inizio della corsa.<br>Il sistema notifica l'Utente che tutti i mezzi selezionati<br>sono pronti all'uso. |
| **Post-condizioni** | Tutti gli N mezzi selezionati sono fisicamente sbloccati,<br>nello stato "In Uso", con la corsa registrata come avviata. |
| **Sequenza alternativa degli eventi** | SbloccoFallito |

| Campo | Valore |
|---|---|
| **Nome** | Sblocca Mezzo: SbloccoFallito |
| **ID** | UT – 03.1 |
| **Breve descrizione** | Uno o più mezzi non rispondono al comando di sblocco.<br>Solo i mezzi che non hanno risposto rimangono nel loro<br>stato precedente; gli altri vengono sbloccati regolarmente. |
| **Attori primari** | Utente |
| **Attori secondari** | nessuno |
| **Precondizioni** | Almeno un mezzo non ha risposto al comando di sblocco<br>entro il timeout. |
| **Postcondizioni** | I mezzi che hanno risposto sono in stato "In Uso"; i mezzi<br>che non hanno risposto rimangono nel loro stato<br>precedente ("Prenotato" o "Disponibile"). |
| **Sequenza alternativa degli eventi** | Il caso d’uso inizia dopo il passo 5 della sequenza<br>principale<br>Il sistema rileva il timeout per uno o più mezzi e li rimuove<br>dall'operazione di sblocco.<br>Il sistema notifica l'Utente indicando quali mezzi non è<br>stato possibile sbloccare.<br>L'Utente può riprovare lo sblocco sui mezzi falliti o<br>procedere con quelli già sbloccati. |

##### 2.2.2.4 UT – 04 Termina corsa

| Campo | Valore |
|---|---|
| **Nome** | Termina corsa |
| **ID** | UT-04 |
| **Breve descrizione** | Il sistema consente all'utente autenticato di terminare la<br>corsa in corso, verificando la posizione del mezzo e<br>applicando le regole di fine corsa configurate<br>dall'operatore, così da liberare il mezzo e addebitare il<br>costo della sessione. |
| **Attori Primari** | Utente |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L'utente è autenticato alla piattaforma e ha una corsa<br>attiva. |

| Campo | Valore |
|---|---|
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'utente vuole terminare e<br>pagare la corsa.<br>2. Il sistema rileva la posizione corrente del mezzo<br>tramite ServizioGIS.<br>Punto di estensione: ErroreServizioGis<br>3. Il sistema aggiorna lo stato del mezzo da "In Uso" a<br>"Disponibile".<br>4. Il sistema mostra all'utente il Riepilogo Corsa con le<br>varie informazioni.<br>5. punto di inclusione (Visualizza Riepilogo Fine Corsa)<br>6.include (EffettuaPagamento). |
| **Post-condizioni** | La corsa è terminata, il mezzo è liberato e reso disponibile,<br>l'addebito è stato effettuato e il riepilogo è mostrato<br>all'utente. |
| **Sequenza alternativa degli eventi** | MezzoInZonaVietata |
| **Nome** | Termina corsa: MezzoInZonaVietata |
| **ID** | UT-04.1 |
| **Breve descrizione** | Il sistema informa l'utente che il mezzo si trova in una Zona<br>Vietata e applica una penale obbligatoria prima di<br>consentire la fine corsa. |
| **Attori Primari** | Utente |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | Il mezzo si trova in una Zona Vietata al momento della<br>richiesta di fine corsa.<br>Post-Condizioni La corsa è terminata con applicazione della penale<br>obbligatoria; il mezzo è liberato e l'addebito comprensivo<br>di penale è stato effettuato. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia dopo il passo 2 della<br>sequenza principale.<br>2. Il sistema rileva che il mezzo si trova in una Zona Vietata. |

3. Il sistema notifica l'utente che il mezzo si trova in una
Zona Vietata e che verrà applicata una penale obbligatoria.
4. Il sistema prosegue dal passo 3 della sequenza
principale applicando la penale al costo totale della corsa.

##### 2.2.2.5 UT – 05 Effettua Pagamento

| Campo | Valore |
|---|---|
| **Nome** | Effettua Pagamento |
| **ID** | UT-05 |
| **Breve descrizione** | Il sistema addebita un importo definito sul metodo di<br>pagamento predefinito dell'Utente, a seguito di<br>un'operazione che prevede un costo (es.<br>sottoscrizione di abbonamento, termine di una<br>corsa). L'operazione avviene senza richiedere alcuna<br>azione manuale all'utente. |
| **Attori Primari** | Sistema |
| **Attori Secondari** | ProviderPagamenti |
| **Precondizioni** | È stata completata un'operazione soggetta a<br>pagamento |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando il sistema deve<br>procedere all'addebito per un'operazione completata.<br>2. Il sistema determina l'importo dovuto sulla base<br>delle condizioni economiche applicabili<br>all'operazione (tariffe, piano di abbonamento, ecc.).<br>3. Il sistema recupera il metodo di pagamento<br>predefinito dell'Utente.<br>4. Il sistema trasmette la richiesta di addebito al<br>ProviderPagamenti.<br>5. Il ProviderPagamenti autorizza e completa la<br>transazione.<br>6. Il sistema genera e invia la ricevuta di pagamento<br>all'Utente. |

| Campo | Valore |
|---|---|
| **Post-condizioni** | L'importo è stato addebitato; l'Utente riceve la<br>ricevuta di pagamento. |
| **Sequenza alternativa degli eventi** | PagamentoRifiutato |
| **Nome** | EffettuaPagamento: PagamentoRifiutato |
| **ID** | UT-05.1 |
| **Breve descrizione** | Il ProviderPagamenti rifiuta la transazione. |
| **Attori Primari** | Sistema |
| **Attori secondari** | ProviderPagamenti |
| **Precondizioni** | Il ProviderPagamenti ha restituito un esito negativo<br>per la transazione. |
| **Postcondizioni** | Il pagamento non è andato a buon fine; l'Utente è<br>notificato del problema. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia dopo il passo 4 della<br>sequenza principale.<br>2. Il sistema riceve l'esito negativo dal Sistema di<br>Pagamento Esterno.<br>3. Il sistema notifica l'Utente del fallimento e lo invita<br>ad aggiornare il metodo di pagamento. |

##### 2.2.2.6 UT - 06 Salva Metodo di Pagamento

| Campo | Valore |
|---|---|
| **Nome** | SalvaMetodoDiPagamento |
| **ID** | UT-06 |
| **Breve descrizione** | Il sistema consente all'utente autenticato di salvare uno o<br>più metodi di pagamento sul proprio account, così da<br>ricevere l'addebito automatico al termine di ogni corsa<br>senza reinserire i dati. |
| **Attori Primari** | Utente |
| **Attori Secondari** | ProviderPagamenti |

| Campo | Valore |
|---|---|
| **Precondizioni** | L'utente è autenticato alla piattaforma. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'utente accede alla sezione<br>"Portafoglio" dal menu laterale.<br>2. Il sistema mostra i metodi di pagamento attualmente<br>associati all'account utente e l'opzione per aggiungerne<br>uno nuovo.<br>3. L'utente seleziona l'opzione per aggiungere un nuovo<br>metodo di pagamento.<br>4. Il sistema mostra le tipologie di metodo di pagamento<br>disponibili (Google Pay, Apple Pay, PayPal, carta di<br>credito).<br>5. L'utente seleziona la tipologia desiderata e inserisce i<br>dati richiesti.<br>6. Il sistema valida i dati inseriti tramite<br>ProviderPagamenti. Se ProviderPagamenti restituisce un<br>errore di validazione, il sistema informa l'utente che i dati<br>inseriti non sono validi e torna al passo 5.<br>7. Il sistema verifica che il metodo di pagamento non sia<br>già associato all'account. Se è già presente, il sistema<br>informa l'utente e non procede al salvataggio.<br>8. Il sistema salva il nuovo metodo di pagamento<br>sull'account utente.<br>9. Se il metodo appena salvato è il primo associato<br>all'account, il sistema lo imposta automaticamente come<br>predefinito. Altrimenti, il sistema chiede all'utente se<br>desidera impostarlo come nuovo metodo predefinito.<br>10. Se l'utente conferma, il sistema aggiorna il metodo<br>predefinito con quello appena salvato.<br>11. Il sistema mostra un messaggio di conferma<br>all'utente. |
| **Post-condizioni** | Il nuovo metodo di pagamento è stato salvato sull'account<br>utente. Il metodo predefinito è quello scelto dall'utente, o<br>il primo salvato se non è stata effettuata alcuna scelta<br>esplicita. |
| **Sequenza alternativa degli eventi** | Nessuna |

##### 2.2.2.1 UT – 07 Consulta Tariffe

| Campo | Valore |
|---|---|
| **Nome** | Consulta Tariffe |
| **ID** | UT.07 |
| **Breve descrizione** | Il sistema mostra all'Utente autenticato il tariffario<br>attivo per ciascuna tipologia di mezzo disponibile<br>(Monopattino, Bicicletta, Automobile), indicando il<br>costo al minuto e il costo al chilometro, così da<br>consentirgli di confrontare i costi prima di effettuare<br>una prenotazione. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'Utente è autenticato alla piattaforma. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Utente accede alla<br>sezione "Piano Tariffario" dal menu laterale.<br>2. Il sistema recupera le tariffe attualmente definite<br>dall'Operatore per ciascuna tipologia di mezzo.<br>3. Il sistema presenta il tariffario con una card per<br>tipologia di mezzo (Monopattino, Bicicletta,<br>Automobile), indicando per ciascuna il costo al<br>minuto e il costo al chilometro.<br>4. L'Utente consulta le tariffe visualizzate. |
| **Post-condizioni** | L'Utente ha visualizzato il tariffario aggiornato e può<br>procedere con la scelta del mezzo più adatto alle<br>proprie esigenze. |
| **Sequenza alternativa degli eventi** | TariffeNonDefinite |
| **Nome** | ConsultaTariffe: TariffeNonDefinite |
| **ID** | CS-17.01 |
| **Breve descrizione** | L'Operatore non ha ancora definito le tariffe per una<br>o più tipologie di mezzo. |

| Campo | Valore |
|---|---|
| **Attori primari** | Utente |
| **Attori secondari** | Nessuno |
| **Precondizioni** | Non sono presenti tariffe definite dall'Operatore per<br>almeno una tipologia di mezzo. |
| **Postcondizioni** | Il tariffario non viene mostrato completamente;<br>l'Utente è informato che le tariffe non sono ancora<br>disponibili. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa sostituisce i passi 2 e 3<br>della sequenza principale.<br>2. Il sistema verifica che non siano presenti tariffe<br>definite per una o più tipologie di mezzo.<br>3. Il sistema notifica all'Utente che le tariffe non sono<br>al momento disponibili. |

##### 2.2.2.2 UT – 08 Visualizza Riepilogo Corsa

| Campo | Valore |
|---|---|
| **Nome** | Visualizza Riepilogo Fine Corsa |
| **ID** | UT - 08 |
| **Breve descrizione** | Al termine della procedura di chiusura corsa, il sistema<br>presenta automaticamente all'Utente il riepilogo della<br>sessione appena conclusa. In caso di corsa di gruppo, il<br>sistema mostra un riepilogo per ogni mezzo utilizzato e<br>un totale complessivo. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | La procedura Termina Corsa si è conclusa con successo<br>per almeno un mezzo; tutte le corse terminate sono nello<br>stato "Conclusa". |
| **Sequenza principale degli eventi** | Il sistema presenta all'Utente il riepilogo per ogni mezzo.<br>Se la corsa coinvolgeva più di un mezzo: |

2.1 il sistema mostra il costo totale complessivo

della sessione di gruppo. L'Utente prende visione del riepilogo e lo chiude.

| Campo | Valore |
|---|---|
| **Post-condizioni** | Il riepilogo è stato visualizzato; il riepilogo di ogni mezzo<br>è disponibile nello storico corse del profilo. |
| **Sequenza alternativa degli eventi** | Nessuna |

##### 2.2.2.3 UT – 09 Sospende Corsa

| Campo | Valore |
|---|---|
| **Nome** | Sospende corsa |
| **ID** | UT-09 |
| **Breve descrizione** | Il sistema consente all'utente autenticato con una<br>corsa attiva di mettere temporaneamente in pausa la<br>corsa, bloccando il mezzo senza terminare la<br>sessione, così da effettuare soste mantenendo il<br>possesso del mezzo. La pausa è gratuita entro il<br>periodo di grazia configurato dall'operatore; al suo<br>termine viene applicata la politica di addebito<br>configurata. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L’utente è autenticato e ha una corsa attiva |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'utente vuole mettere<br>in pausa la corsa in corso.<br>2. Il sistema invia il comando di blocco temporaneo al<br>mezzo.<br>3. Il mezzo conferma l'avvenuto blocco al sistema.<br>4. Il sistema aggiorna lo stato del mezzo da "In Uso"<br>a "In Pausa" e registra l'istante di inizio pausa.<br>5. Il sistema avvia il conteggio del periodo di grazia<br>configurato dall'operatore.<br>6. Il sistema notifica all'utente che la corsa è stata<br>sospesa, indicando il tempo di pausa gratuita residuo<br>e l'eventuale politica di addebito successiva. |

| Campo | Valore |
|---|---|
| **Post-condizioni** | La corsa non è terminata; il mezzo è bloccato e resta<br>riservato all'utente nello stato "In Pausa"; il sistema<br>mantiene attiva la sessione e traccia la durata della<br>pausa |
| **Sequenza alternativa degli eventi** | Superamento Periodo di Grazia |
| **Nome** | SospendeCorsa: Superamento Periodo di Grazia |
| **ID** | UT-09.1 |
| **Breve descrizione** | La pausa si protrae oltre il periodo di grazia e il<br>sistema applica la politica di addebito per pausa<br>configurata dall'operatore. |
| **Attori primari** | Utente |
| **Attori secondari** | Nessuno |
| **Precondizioni** | La durata della pausa ha raggiunto il periodo di grazia<br>configurato dall'operatore. |
| **Postcondizioni** | La corsa resta sospesa con applicazione dell'addebito<br>per pausa secondo la politica configurata; la sessione<br>rimane attiva |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia dopo il passo 5 della<br>sequenza principale.<br>2. Il sistema rileva che la durata della pausa ha<br>raggiunto il periodo di grazia.<br>3. Il sistema notifica all'utente la fine del periodo di<br>pausa gratuita e l'avvio dell'addebito secondo la<br>politica configurata.<br>4. Il sistema applica l'addebito per pausa al costo<br>della corsa e prosegue mantenendo il mezzo nello<br>stato "In Pausa". |

##### 2.2.2.4 UT – 10 Visualizza Promozioni

| Campo | Valore |
|---|---|
| **Nome** | Visualizza Promozioni |
| **ID** | UT.10 |
| **Breve descrizione** | Il sistema mostra all'Utente autenticato l'elenco delle<br>promozioni attive pubblicate dall'Operatore, con le<br>relative condizioni e vantaggi, così da consentirgli di<br>ridurre i costi di utilizzo del servizio. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'Utente è autenticato alla piattaforma. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Utente accede alla<br>sezione "Bonus e Promozioni" dal menu laterale.<br>2. Il sistema recupera l'elenco delle promozioni attive<br>pubblicate dall'Operatore.<br>3. Il sistema presenta l'elenco delle promozioni<br>disponibili, indicando per ciascuna: tipologia,<br>descrizione, condizioni di applicazione e data di<br>scadenza.<br>4. L'Utente consulta le promozioni disponibili. |
| **Post-condizioni** | L'Utente ha visualizzato l'elenco delle promozioni<br>attive e può scegliere di usufruirne nelle corse<br>successive. |
| **Sequenza alternativa degli eventi** | NessunPromozioneAttiva |
| **Nome** | VisualizzaPromozioni: NessunPromozioneAttiva |
| **ID** | CS-16.01 |

| Campo | Valore |
|---|---|
| **Breve descrizione** | Non vi sono promozioni attive pubblicate<br>dall'Operatore al momento della richiesta. |
| **Attori primari** | Utente |
| **Attori secondari** | Nessuno |
| **Precondizioni** | Non vi sono promozioni attive pubblicate<br>dall'Operatore. |
| **Postcondizioni** | L'elenco delle promozioni non viene mostrato;<br>l'Utente è informato dell'assenza di promozioni<br>attive. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa sostituisce i passi 2 e 3<br>della sequenza principale.<br>2. Il sistema verifica che non vi siano promozioni<br>attive.<br>3. Il sistema notifica all'Utente che non sono<br>disponibili promozioni attive al momento. |

##### 2.2.2.5 UT – 11 Visualizza Storico Corse

| Campo | Valore |
|---|---|
| **Nome** | Visualizza Storico Corse |
| **ID** | UT - 11 |
| **Breve descrizione** | L'utente consulta l'elenco cronologico delle corse<br>effettuate in passato, con le informazioni di ciascuna. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'utente è autenticato alla piattaforma. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Utente richiede la<br>visualizzazione dello storico delle corse.<br>2. Il sistema recupera l'elenco di tutte le corse effettuate<br>dall'Utente.<br>3. Il sistema presenta l'elenco delle corse effettuate in<br>ordine cronologico. |

4. L'Utente consulta le informazioni.

| Campo | Valore |
|---|---|
| **Post-condizioni** | L'utente visualizza l'elenco delle corse effettuate con le<br>relative informazioni. |
| **Sequenza alternativa degli eventi** | DatiNonDisponibili |
| **Nome** | Visualizza Storico Corse: DatiNonDisponibili |
| **ID** | UT – 11.1 |
| **Breve descrizione** | Il sistema non riesce a recuperare lo storico delle corse a<br>causa di un errore nella disponibilità dei dati. |
| **Attori primari** | Utente |
| **Attori secondari** | nessuno |
| **Precondizioni** | Il sistema non è in grado di accedere ai dati dello storico<br>dell'utente. |
| **Postcondizioni** | Lo storico non viene mostrato; l'utente è informato del<br>problema temporaneo. |
| **Sequenza alternativa degli eventi** | 1.La sequenza alternativa sostituisce i passi 3 e 4 della<br>sequenza principale.<br>2. Il sistema notifica all'Utente che lo storico delle corse<br>non è al momento disponibile e invita a riprovare. |

##### 2.2.2.6 UT – 12 Invia Segnalazione

| Campo | Valore |
|---|---|
| **Nome** | Invia segnalazione |
| **ID** | UT-12 |
| **Breve descrizione** | Il sistema consente all'Utente autenticato di inviare<br>una segnalazione relativa a un mezzo o a una<br>situazione anomala, così da informare l'Operatore<br>affinché possa intervenire tempestivamente. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |

| Campo | Valore |
|---|---|
| **Precondizioni** | L'utente è autenticato alla piattaforma. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Utente accede alla<br>sezione dedicata alle segnalazioni.<br>2. Il sistema mostra il form di segnalazione con i<br>campi richiesti.<br>3. L'Utente seleziona la tipologia di segnalazione.<br>4. L'Utente compila i campi richiesti e conferma<br>l'invio.<br>5. Il sistema registra la segnalazione e la rende<br>visibile all'Operatore.<br>6. Il sistema notifica l'Utente dell'avvenuto invio della<br>segnalazione. |
| **Post-condizioni** | La segnalazione è registrata nel sistema e resa<br>disponibile all'Operatore per la presa in carico. |
| **Sequenza alternativa degli eventi** | Nessuno |

##### 2.2.2.7 UT – 13 Sottoscrive Abbonamento

| Campo | Valore |
|---|---|
| **Nome** | Sottoscrive Abbonamento |
| **ID** | UT-13 |
| **Breve descrizione** | Il sistema consente all'Utente autenticato di scegliere<br>e sottoscrivere un piano di abbonamento attivo, così<br>da usufruire di condizioni tariffarie agevolate per un<br>periodo determinato. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | 1. L'utente è autenticato alla piattaforma; |

2. esistono piani di abbonamento attivi pubblicati
dall'operatore
3. l'utente ha un metodo di pagamento valido.

| Campo | Valore |
|---|---|
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Utente accede alla<br>sezione dedicata agli abbonamenti.<br>2. Il sistema recupera e mostra i piani di<br>abbonamento disponibili, con durata, costo e benefici<br>di ciascuno.<br>3. L'utente seleziona il piano desiderato.<br>4. Il sistema mostra il riepilogo del piano selezionato<br>e richiede conferma.<br>5. L'utente conferma la sottoscrizione.<br>6. Include (EffettuaPagamento).<br>7. Il sistema attiva l'abbonamento sull'account<br>dell'utente a partire dalla data corrente.<br>8. Il sistema notifica l'utente dell'avvenuta<br>attivazione. |
| **Post-condizioni** | L'abbonamento è attivo sull'account dell'utente; le<br>condizioni tariffarie agevolate sono applicate a<br>partire dalla data di attivazione. |
| **Sequenza alternativa degli eventi** | Nessuno |

##### 2.2.2.8 AP – 01 Accede Report

| Campo | Valore |
|---|---|
| **Nome** | Accede Report |
| **ID** | CS-14 (AP.01) |
| **Breve descrizione** | Il sistema consente all'Amministrazione Pubblica<br>autenticata di consultare la dashboard di reportistica<br>aggregata sull'utilizzo del servizio di mobilità<br>condivisa, visualizzando statistiche su corse<br>effettuate, chilometri percorsi e distribuzione per |

tipologia di mezzo, così da supportare decisioni strategiche di pianificazione urbana.

| Campo | Valore |
|---|---|
| **Attori Primari** | Amministrazione Pubblica |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'Amministrazione Pubblica è autenticata alla<br>piattaforma con il ruolo AP. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Amministrazione<br>Pubblica seleziona l'opzione "Visualizza Report" dalla<br>propria dashboard.<br>2. Il sistema recupera le statistiche aggregate<br>sull'utilizzo del servizio relative all'intervallo<br>temporale configurato.<br>3. Il sistema presenta la dashboard di reportistica con<br>un istogramma a barre impilate che analizza il volume<br>dei noleggi su base settimanale e un grafico a torta<br>che illustra la quota di mercato per tipologia di<br>mezzo.<br>4. L'Amministrazione Pubblica consulta i dati<br>visualizzati.<br>5. Punto di estensione: EsportaReport (si attiva se<br>l'Amministrazione Pubblica seleziona una delle<br>opzioni di esportazione disponibili). |
| **Post-condizioni** | La dashboard di reportistica è visualizzata con i dati<br>aggregati aggiornati; l'Amministrazione Pubblica ha<br>consultato le statistiche sull'utilizzo del servizio. |
| **Sequenza alternativa degli eventi** | DatiNonDisponibili |
| **Nome** | AccedeReport: DatiNonDisponibili |
| **ID** | CS-14.01 |

| Campo | Valore |
|---|---|
| **Breve descrizione** | Il sistema non riesce a recuperare le statistiche<br>aggregate a causa di un errore nel sistema di<br>elaborazione dati. |
| **Attori primari** | Amministrazione Pubblica |
| **Attori secondari** | Nessuno |
| **Precondizioni** | Il sistema non è in grado di accedere o elaborare i dati<br>aggregati del report. |
| **Postcondizioni** | La dashboard di reportistica non viene mostrata;<br>l'Amministrazione Pubblica è informata del problema<br>temporaneo. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa sostituisce i passi 2 e 3<br>della sequenza principale.<br>2. Il sistema rileva un errore nel recupero dei dati<br>aggregati.<br>3. Il sistema notifica all'Amministrazione Pubblica<br>che le statistiche non sono al momento disponibili e<br>la invita a riprovare. |

##### 2.2.2.9 AP - 02 Esporta Report

| Campo | Valore |
|---|---|
| **Nome** | Esporta Report |
| **ID** | CS-15 (AP.02) |
| **Breve descrizione** | Il sistema consente all'Amministrazione Pubblica di<br>esportare il report aggregato correntemente<br>visualizzato in uno dei formati disponibili (CSV o<br>PDF), così da poterlo utilizzare in analisi esterne e<br>documentazione ufficiale. Questo caso d'uso estende<br>AccedeReport. |
| **Attori Primari** | Amministrazione Pubblica |
| **Attori Secondari** | Nessuno |

| Campo | Valore |
|---|---|
| **Precondizioni** | L'Amministrazione Pubblica ha acceduto alla<br>dashboard di reportistica (CS-14).<br>I dati del report sono disponibili e visualizzati<br>correttamente. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia dal Punto di estensione<br>EsportaReport di AccedeReport, quando<br>l'Amministrazione 2. Pubblica seleziona una delle<br>opzioni di esportazione disponibili.<br>3. Il sistema presenta le opzioni di formato<br>disponibili: CSV e PDF.<br>4. L'Amministrazione Pubblica seleziona il formato<br>desiderato.<br>5. Il sistema genera il file nel formato selezionato<br>contenente i dati del report aggregato correntemente<br>visualizzato.<br>6. Il sistema avvia il download del file sul dispositivo<br>dell'Amministrazione Pubblica.<br>7. Il sistema notifica l'Amministrazione Pubblica del<br>completamento dell'esportazione. |
| **Post-condizioni** | Il file del report aggregato è stato generato e<br>scaricato nel formato selezionato; i dati esportati<br>corrispondono alle statistiche visualizzate nella<br>dashboard. |
| **Sequenza alternativa degli eventi** | ErroreGenerazioneFile |
| **Nome** | EsportaReport: ErroreGenerazioneFile |
| **ID** | CS-15.01 |
| **Breve descrizione** | Il sistema non riesce a generare il file di esportazione<br>nel formato selezionato. |
| **Attori primari** | Amministrazione Pubblica |

| Campo | Valore |
|---|---|
| **Attori secondari** | Nessuno |
| **Precondizioni** | Il sistema ha incontrato un errore durante la<br>generazione del file nel formato selezionato. |
| **Postcondizioni** | Il file non viene generato; l'Amministrazione Pubblica<br>è informata del problema e può ritentare l'operazione. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia dopo il passo 4 della<br>sequenza principale.<br>2. Il sistema rileva un errore nella generazione del<br>file.<br>3. Il sistema notifica all'Amministrazione Pubblica<br>che l'esportazione non è andata a buon fine.<br>4. Il sistema invita l'Amministrazione Pubblica a<br>riprovare o a selezionare un formato alternativo. |

##### 2.2.2.10 AP – 03 Visualizza Mappa Amministrazione Pubblica

| Campo | Valore |
|---|---|
| **Nome** | Visualizza Mappa Amministrazione Pubblica |
| **ID** | CS-18 (AP.03) |
| **Breve descrizione** | Il sistema mostra all'Amministrazione Pubblica<br>autenticata la mappa interattiva dell'area urbana di<br>competenza, arricchita da layer statistici sovrapposti<br>— tra cui la heatmap della distribuzione dei mezzi,<br>l'intensità d'uso per zona e le aree a bassa<br>disponibilità — così da supportare decisioni<br>strategiche di pianificazione e monitoraggio del<br>servizio sul territorio. |
| **Attori Primari** | Amministrazione Pubblica |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L'Amministrazione Pubblica è autenticata alla<br>piattaforma con il ruolo AP. |

| Campo | Valore |
|---|---|
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Amministrazione<br>Pubblica accede alla schermata principale della<br>propria dashboard.<br>2. Il sistema interroga il ServizioGIS per recuperare i<br>dati geografici aggiornati relativi all'area urbana di<br>competenza.<br>3. Il sistema carica la mappa interattiva e sovrappone<br>il layer predefinito: la heatmap della distribuzione dei<br>mezzi, che evidenzia con gradiente cromatico le aree<br>ad alta e bassa densità di mezzi disponibili.<br>4. Il sistema visualizza sulla mappa le zone definite<br>(Operativa, Vietata, Limitata, di Parcheggio) con la<br>rispettiva colorazione semantica.<br>5. Il sistema mostra nel pannello laterale i layer<br>statistici selezionabili: distribuzione mezzi per<br>tipologia, intensità d'uso per zona e fasce orarie di<br>picco.<br>6. L'Amministrazione Pubblica seleziona i layer<br>statistici di interesse da visualizzare sulla mappa.<br>7. Il sistema aggiorna la mappa mostrando i layer<br>selezionati.<br>8. L'Amministrazione Pubblica consulta i dati<br>territoriali visualizzati. |
| **Post-condizioni** | La mappa è visualizzata con i layer statistici<br>selezionati e aggiornati; l'Amministrazione Pubblica<br>può monitorare la distribuzione dei mezzi sul<br>territorio e procedere con decisioni strategiche di<br>pianificazione urbana. |
| **Sequenza alternativa degli eventi** | DatiGISNonDisponibili |
| **Nome** | VisualizzaMappaAP: DatiGISNonDisponibili |
| **ID** | CS-18.01 |

| Campo | Valore |
|---|---|
| **Breve descrizione** | Il ServizioGIS non riesce a fornire i dati geografici o<br>statistici necessari al caricamento della mappa. |
| **Attori primari** | Amministrazione Pubblica |
| **Attori secondari** | ServizioGIS |
| **Precondizioni** | Il ServizioGIS ha restituito un errore o non è<br>raggiungibile al momento della richiesta. |
| **Postcondizioni** | La mappa non viene caricata; l'Amministrazione<br>Pubblica è informata dell'indisponibilità temporanea<br>del servizio cartografico. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia dopo il passo 2 della<br>sequenza principale.<br>2. Il sistema rileva che il ServizioGIS non ha restituito<br>dati validi.<br>3. Il sistema notifica all'Amministrazione Pubblica<br>che la mappa non è al momento disponibile e la invita<br>a riprovare. |

##### 2.2.2.11 OP – 01 Visualizza Mappa Operatore

| Campo | Valore |
|---|---|
| **Nome** | Visualizza Mappa Operatore |
| **ID** | OP-01 |
| **Breve descrizione** | Il sistema mostra all'Operatore autenticato la mappa<br>interattiva con l'intera flotta, incluso lo stato di ciascun<br>mezzo (disponibile, in uso, in manutenzione, ecc.), così da<br>poter pianificare operazioni di redistribuzione o<br>manutenzione. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L’operatore è autenticato alla piattaforma |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Operatore accede alla<br>schermata principale della piattaforma. |

2. Il sistema interroga il ServizioGIS per recuperare i
dati geografici.
3. Il sistema recupera le zone con restrizioni, le zone
di parcheggio e lo stato aggiornato di tutti i mezzi della flotta.
4. Il sistema visualizza la mappa con tutti i mezzi, lo
stato di ciascuno, le aree con restrizioni e il marker della posizione corrente.

| Campo | Valore |
|---|---|
| **Post-condizioni** | La mappa è visualizzata con i dati aggiornati sull'intera<br>flotta; l'Operatore può procedere con la pianificazione di<br>operazioni di redistribuzione o manutenzione. |
| **Sequenza alternativa degli eventi** | Nessuna |

##### 2.2.2.12 OP – 02 Aggiunge Mezzo

| Campo | Valore |
|---|---|
| **Nome** | Aggiunge Mezzo |
| **ID** | OP – 02 |
| **Breve descrizione** | Il sistema consente all'operatore autenticato di aggiungere<br>un nuovo mezzo alla flotta, specificando tipologia,<br>identificativo, posizione iniziale e stato, così da renderlo<br>disponibile per il noleggio da parte degli utenti. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L'operatore è autenticato alla piattaforma e si trova nella<br>Dashboard Operatore. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'operatore accede alla<br>sezione dedicata ai mezzi.<br>2. Il sistema mostra la lista dei mezzi attualmente presenti<br>nella flotta.<br>3. L'operatore seleziona la funzione che permette di<br>aggiungere un nuovo mezzo. |

4. Il sistema permette di inserire i campi: tipologia
(monopattino, bicicletta, automobile), identificativo, posizione iniziale e stato iniziale.
5. L'operatore inserisce i dati richiesti e seleziona la
posizione iniziale sulla mappa.
6. L'operatore conferma i dati inseriti.
7. Il sistema valida i dati verificando che i campi obbligatori
siano compilati e che l'identificativo sia univoco. Se uno o più campi non sono validi, il sistema informa l'operatore specificando i campi non validi e torna al passo 5.
8. Il sistema verifica tramite ServizioGIS che la posizione
selezionata ricada all'interno di una zona operativa.
9. Il sistema salva il nuovo mezzo associandolo alla flotta.
10. Il sistema mostra un messaggio di conferma
all'operatore.

| Campo | Valore |
|---|---|
| **Post-condizioni** | Il nuovo mezzo è stato salvato nel sistema e risulta<br>disponibile sulla Mappa Utente in base allo stato<br>impostato. |
| **Sequenza alternativa degli eventi** | IdentificativoEsistente<br>PosizioneNonOperativa |

| Campo | Valore |
|---|---|
| **Nome** | Aggiunge Mezzo: IdentificativoEsistente |
| **ID** | OP-02.01 |
| **Breve descrizione** | Il sistema rileva che l'identificativo inserito è già<br>associato ad un altro mezzo e solleva<br>IdentificativoEsistenteException, impedendo il salvataggio. |
| **Attori primari** | Operatore |
| **Attori secondari** | Nessuno |
| **Precondizioni** | L'identificativo inserito dall'operatore esiste già nel<br>MezzoRepository. |
| **Postcondizioni** | Il nuovo mezzo non viene salvato; l'operatore rimane sulla<br>schermata di inserimento per correggere i dati. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia al passo 7 della sequenza<br>principale.<br>2. Il sistema verifica l'unicità dell'identificativo tramite<br>MezzoRepository.<br>3. Il sistema rileva che l'identificativo è già presente e<br>solleva IdentificativoEsistenteException.<br>4. Il sistema informa l'operatore dell'errore e torna<br>al passo 5. |

| Campo | Valore |
|---|---|
| **Nome** | Aggiunge Mezzo: PosizioneNonOperativa |
| **ID** | OP-02.02 |
| **Breve descrizione** | Il ServizioGIS rileva che la posizione iniziale non ricade in<br>alcuna zona operativa; il sistema solleva<br>PosizioneNonOperativaException e impedisce il salvataggio. |
| **Attori primari** | Operatore |
| **Attori secondari** | ServizioGIS |
| **Precondizioni** | La posizione iniziale del mezzo selezionata sulla mappa non<br>ricade in alcuna zona operativa. |
| **Postcondizioni** | Il nuovo mezzo non viene salvato; l'operatore rimane sulla<br>schermata di inserimento per selezionare una posizione<br>valida. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia dopo il passo 8 della<br>sequenza principale.<br>2. Il ServizioGIS rileva che la posizione iniziale non ricade<br>in alcuna zona operativa e solleva<br>PosizioneNonOperativaException.<br>3. Il sistema informa l'operatore dell'errore di posizione<br>e torna al passo 5. |

##### 2.2.2.13 OP – 03 Dismette Mezzo

| Campo | Valore |
|---|---|
| **Nome** | Dismette Mezzo |
| **ID** | OP – 03 |
| **Breve descrizione** | Il sistema consente all'operatore autenticato di<br>dismettere un mezzo precedentemente censito,<br>rimuovendone la disponibilità per l'assegnazione a<br>nuove missioni e mantenendone lo storico ai fini di<br>consultazione. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |

| Campo | Valore |
|---|---|
| **Precondizioni** | L'operatore deve essere autenticato nel sistema e il<br>mezzo da dismettere deve essere già censito e non<br>assegnato ad alcuna missione attiva.<br>Sequenza<br>principale<br>1. Il caso d'uso inizia quando l'operatore accede alla<br>sezione dedicata ai mezzi.<br>2. Il sistema mostra la lista dei mezzi presenti nella<br>flotta con il loro stato corrente.<br>3. L'operatore seleziona il mezzo da dismettere.<br>4. Il sistema mostra i dettagli del mezzo selezionato e<br>richiede conferma della dismissione.<br>5. L'operatore conferma la dismissione.<br>6. Il sistema aggiorna lo stato del mezzo a "Dismesso"<br>e lo rimuove dall'elenco dei mezzi disponibili.<br>7. Il sistema mantiene lo storico delle informazioni<br>associate al mezzo.<br>8. Il sistema mostra un messaggio di conferma<br>all'operatore. |
| **Post-condizioni** | Il mezzo è registrato come dismesso nel sistema, non<br>risulta più disponibile per l'assegnazione a nuove<br>corse e i dati storici relativi al mezzo rimangono<br>consultabili. |
| **Sequenza alternativa degli eventi** | MezzoInUso |
| **Nome** | Dismette Mezzo: MezzoInUso |
| **ID** | OP-03.1 |
| **Breve descrizione** | Il sistema informa l'operatore che il mezzo selezionato<br>è attualmente impegnato in una missione e non può<br>essere dismesso. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | ServizioGIS |

| Campo | Valore |
|---|---|
| **Precondizioni** | L'operatore deve essere autenticato nel sistema e il<br>mezzo selezionato risulta assegnato a una corsa<br>attiva. |
| **Post-condizioni** | Lo stato del mezzo resta invariato e l'operatore rimane<br>nella sezione di gestione dei mezzi. |
| **Sequenza alternativa degli eventi** | 1. Il sistema, tramite il ServizioGIS, rileva che il mezzo<br>selezionato è impegnato in una corsa.<br>2. Il sistema notifica all'operatore l'impossibilità di<br>dismettere il mezzo, indicandone la causa.<br>3. L'operatore prende visione del messaggio e ritorna<br>alla sezione di gestione dei mezzi. |

##### 2.2.2.14 OP – 04 Modifica stato mezzo

| Campo | Valore |
|---|---|
| **Nome** | Modifica Stato Mezzo |
| **ID** | OP-04 |
| **Breve descrizione** | Il sistema consente all'operatore autenticato di modificare<br>lo stato di un mezzo della flotta, così da nasconderlo o<br>mostrarlo sulla Mappa Utente e gestire il ciclo operativo del<br>veicolo. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'operatore è autenticato alla piattaforma e il mezzo<br>selezionato esiste nella flotta. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'operatore accede alla<br>sezione dedicata ai mezzi.<br>2. Il sistema mostra la Mappa Operatore con la lista dei<br>mezzi della flotta e il loro stato corrente.<br>3. L'operatore seleziona il mezzo di cui intende<br>modificare lo stato.<br>4. Il sistema mostra lo stato corrente del mezzo e le<br>opzioni di stato selezionabili tra: Disponibile, In<br>manutenzione, Fuori servizio.<br>5. L'operatore seleziona il nuovo stato desiderato. |

6. Il sistema verifica che la transizione di stato richiesta
sia consentita.
7. Il sistema aggiorna lo stato del mezzo.
8. Il sistema mostra un messaggio di conferma
all'operatore.

| Campo | Valore |
|---|---|
| **Post-condizioni** | Lo stato del mezzo è stato aggiornato. Se il nuovo stato è<br>"In manutenzione" o "Fuori servizio" il mezzo non è più<br>visibile sulla Mappa Utente; se il nuovo stato è "Disponibile"<br>il mezzo è nuovamente visibile sulla Mappa Utente |
| **Sequenza alternativa degli eventi** | MezzoInUso |
| **Nome** | Modifica Stato Mezzo: MezzoInUso |
| **ID** | OP-04.1 |
| **Breve descrizione** | Il sistema informa l'operatore che il mezzo selezionato è<br>attualmente in uso da un utente e non può essere<br>modificato. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | Il mezzo selezionato ha stato "In uso" o "Prenotato" al<br>momento della richiesta di modifica. |
| **Post-condizioni** | Nessuna. Lo stato del mezzo non viene modificato. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa inizia dopo il passo 6 della<br>sequenza principale.<br>2. Il sistema rileva che il mezzo è attualmente in uso o<br>prenotato da un utente.<br>3. Il sistema informa l'operatore che non è possibile<br>modificare lo stato del mezzo mentre è in uso o prenotato |

##### 2.2.2.15 OP – 05 Definisce tariffa

| Campo | Valore |
|---|---|
| **Nome** | Definisce Tariffa |
| **ID** | OP-05 |

| Campo | Valore |
|---|---|
| **Breve descrizione** | Il sistema consente all'operatore autenticato di definire una<br>nuova tariffa per una specifica tipologia di mezzo,<br>specificando il costo al minuto e il costo al chilometro, così<br>da permettere la configurazione del modello di costo del<br>servizio. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'operatore è autenticato alla piattaforma e non esiste già<br>una tariffa definita per la tipologia di mezzo selezionata. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'operatore accede alla<br>sezione dedicate alle tariffe.<br>2. Il sistema mostra le tariffe attualmente definite per<br>ciascuna tipologia di mezzo disponibile.<br>3. L'operatore seleziona la tipologia di mezzo per cui<br>intende definire una nuova tariffa (monopattino,<br>bicicletta, automobile).<br>4. Il sistema mostra il form di inserimento con i campi:<br>costo al minuto e costo al chilometro.<br>5. L'operatore inserisce i valori richiesti.<br>6. Il sistema valida i dati inseriti verificando che i valori<br>siano numerici e maggiori di zero.<br>7. Il sistema salva la nuova tariffa associandola alla<br>tipologia di mezzo selezionata.<br>8. Il sistema mostra un messaggio di conferma<br>all'operatore. |
| **Post-condizioni** | La nuova tariffa è stata salvata nel sistema e sarà applicata<br>alle corse successive effettuate con la tipologia di mezzo<br>selezionata. |
| **Sequenza alternativa degli eventi** | Nessuna |

##### 2.2.2.16 OP-06 Definisce Regole Fine Corsa

| Campo | Valore |
|---|---|
| **Nome** | Definisce Regole Fine Corsa |

| Campo | Valore |
|---|---|
| **ID** | OP-06 |
| **Breve descrizione** | L'operatore definisce le regole sanzionatorie e<br>incentivanti che governano la corretta conclusione<br>di una corsa, specificando la politica sanzionatoria<br>applicata al rilascio del mezzo al di fuori delle zone<br>di parcheggio e un eventuale bonus riconosciuto<br>all'utente al raggiungimento di un numero<br>prestabilito di parcheggi corretti, così da garantire<br>il decoro urbano. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'operatore è autenticato nel sistema ed esiste almeno<br>una zona di parcheggio già definita. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'operatore accede<br>alla sezione dedicata alle Regole Fine Corsa.<br>2. Il sistema mostra i parametri configurabili<br>correnti.<br>3. L'operatore configura le regole: |

3.1 stabilisce la politica sanzionatoria applicata

al rilascio del mezzo fuori dalle zone di parcheggio (penale, blocco fine corsa o avviso);

3.1.2 se la politica prevede una penale,

inserisce l'importo da addebitare in aggiunta al costo della corsa;

3.2 se intende attivare un incentivo, configura il

bonus indicando il numero di parcheggi corretti necessari e il valore del bonus.
4. L'operatore conferma le regole definite.
5. Se i parametri non rientrano negli intervalli
ammessi, il sistema informa l'operatore

specificando i campi non validi e torna al passo 3.
6. Il sistema salva la nuova configurazione.
7. Il sistema notifica all'operatore l'avvenuta
definizione delle regole.

| Campo | Valore |
|---|---|
| **Post-condizioni** | Le nuove regole di fine corsa sono memorizzate nel<br>sistema e vengono applicate a tutte le corse successive. |
| **Sequenza alternativa degli eventi** | Nessuna |

##### 2.2.2.17 OP-07 Definisce Zona

| Campo | Valore |
|---|---|
| **Nome** | DefinisceZona |
| **ID** | OP - 07 |
| **Breve descrizione** | L’operatore definisce i confini geografici di una Zona<br>caratteristica (Vietata, Limitata, di Parcheggio, Confine<br>Operativo); il sistema memorizza la zona e la applica<br>attivamente. |
| **Attori primari** | Operatore |
| **Attori secondari** | Nessuno |
| **Precondizioni** | L’operatore è autenticato con il ruolo appropriato nel<br>sistema |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l’operatore intende definire<br>una zona caratteristica all’interno del sistema.<br>2. Il sistema visualizza la mappa interattiva dell'area<br>di competenza con le zone esistenti.<br>3. L’operatore disegna il perimetro della zona sulla mappa<br>definendo i vertici del poligono.<br>4. L’operatore conferma la creazione della zona.<br>5. Fintantoché il perimetro non è valido: |

5.1 Il sistema notifica l’operatore del problema rilevato.

5.2 l’operatore corregge il perimetro (torna al passo 3).

6. Il sistema salva la Zona e la rende attiva.
7. Il sistema aggiorna la mappa visibile agli Utenti
evidenziando la nuova zona.

| Campo | Valore |
|---|---|
| **Postcondizioni** | La nuova Zona creata è persistita nel sistema con il<br>perimetro definito; il sistema la applica alla flotta. |
| **Sequenze alternative** | Nessuna |

##### 2.2.2.18 OP-08 Gestisce Segnalazione

| Campo | Valore |
|---|---|
| **Nome** | Gestisce segnalazione |
| **ID** | OP-08 |
| **Breve descrizione** | Il sistema consente all'Operatore autenticato di<br>consultare le segnalazioni inviate dagli Utenti così da<br>pianificare gli opportuni interventi a fronte delle<br>problematiche riscontrate (relative ai mezzi, alle zone<br>di parcheggio o ad altri aspetti del servizio) |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'operatore è autenticato alla piattaforma. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Operatore accede alla<br>sezione dedicata alle segnalazioni.<br>2. Il sistema recupera l'elenco delle segnalazioni<br>inviate dagli Utenti.<br>3. Il sistema presenta l'elenco delle segnalazioni in<br>ordine cronologico, indicando per ciascuna: tipologia,<br>descrizione e data di invio.<br>4. L'Operatore consulta le segnalazioni visualizzate.<br>5. L'Operatore seleziona una segnalazione per<br>visualizzarne il dettaglio. |

6. Il sistema mostra il dettaglio completo della
segnalazione selezionata.
7. L'Operatore prende in carico la segnalazione.
8. Il sistema aggiorna lo stato della segnalazione e
notifica l'Utente della presa in carico.

| Campo | Valore |
|---|---|
| **Post-condizioni** | La segnalazione è stata presa in carico dall'Operatore;<br>l'Utente è informato dell'aggiornamento di stato. |
| **Sequenza alternativa degli eventi** | Nessuno |

##### 2.2.2.19 OP-09 Sospende Account Utente

| Campo | Valore |
|---|---|
| **Nome** | Sospende account utente |
| **ID** | OP-09 |
| **Breve descrizione** | Il sistema consente all'Operatore autenticato di<br>sospendere l'account di un Utente, così da tutelare<br>l'integrità del servizio in caso di comportamenti<br>scorretti o violazioni delle condizioni d'uso. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | 1. L'Operatore è autenticato alla piattaforma.<br>2. L'account dell'Utente da sospendere è attivo. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Operatore accede alla<br>sezione per la gestione degli utenti.<br>2. Il sistema presenta l'elenco degli utenti registrati.<br>3. L'Operatore seleziona l'Utente di cui intende<br>sospendere l'account.<br>4. Il sistema mostra il dettaglio del profilo dell'Utente<br>selezionato.<br>5. L’operatore aggiunge una descrizione sulla<br>motivazione della sospensione dell’account |

5. L'Operatore seleziona l'opzione per sospendere
Account.
6. Il sistema richiede conferma dell'operazione.
7. L'Operatore conferma la sospensione.
8. Il sistema sospende l'account dell'Utente e gli
impedisce l'accesso alla piattaforma.
9. Il sistema notifica l'Utente dell'avvenuta
sospensione del proprio account.

| Campo | Valore |
|---|---|
| **Post-condizioni** | La segnalazione è stata presa in carico dall'Operatore;<br>l'Utente è informato dell'aggiornamento di stato. |
| **Sequenza alternativa degli eventi** | Nessuno |

##### 2.2.2.20 OP-10 Definisce Offerta

| Campo | Valore |
|---|---|
| **Nome** | Definisce Offerta |
| **ID** | OP-10 |
| **Breve descrizione** | Il sistema consente all'Operatore autenticato di<br>creare e pubblicare offerte commerciali<br>(promozioni e piani di abbonamento) con<br>condizioni e scadenza configurabili, così da<br>incentivare l'utilizzo del servizio con politiche<br>commerciali flessibili. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L'operatore è autenticato alla piattaforma. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Operatore accede<br>alla sezione delle Tariffe e Promozioni.<br>2. Il sistema mostra le offerte attualmente definite<br>(promozioni e piani di abbonamento) con il<br>rispettivo stato (attiva, scaduta, in bozza). |

3. L'Operatore seleziona l'opzione per creare una
nuova offerta.
4. Il sistema chiede all'Operatore di scegliere la
tipologia di offerta da creare: Promozione o Abbonamento.
5. L'Operatore seleziona la tipologia desiderata.
6. Il sistema mostra il form di configurazione
specifico per la tipologia scelta.
7. L'Operatore compila i campi richiesti e
conferma.
8. l sistema valida i dati inseriti verificando che i
valori siano coerenti e completi (importi numerici e maggiori di zero, date di scadenza nel futuro, nome non duplicato). Se non sono corretti, il sistema invita l’operatore a riprovare e si torna al passo 7.
9. Il sistema salva l'offerta e la pubblica
rendendola disponibile agli utenti.
10. Il sistema mostra un messaggio di conferma
all'Operatore.

| Campo | Valore |
|---|---|
| **Post-condizioni** | L'offerta è salvata nel sistema e resa visibile agli<br>utenti nelle sezioni dedicate |
| **Sequenza alternativa degli eventi** | Nessuno |

##### 2.2.2.21 OP-11 Configura parametri di sistema

| Campo | Valore |
|---|---|
| **Nome** | Configura Parametri Numerici di Sistema |
| **ID** | OP-11 |
| **Breve descrizione** | L'operatore configura i parametri numerici operativi<br>del sistema come la durata massima di una |

prenotazione, la durata del periodo di grazia per la pausa corsa, il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente e l'importo di addebito al minuto applicato durante la pausa corsa al termine del periodo di grazia.

| Campo | Valore |
|---|---|
| **Attori Primari** | Operatore |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | L’operatore è autenticato nel sistema |
| **Sequenza principale degli eventi** | 1. Il caso d’uso inizia quando l’operatore accede<br>alla sezione di configurazione dei parametri di<br>sistema.<br>2. Il sistema recupera e mostra i valori correnti dei<br>quattro parametri: durata massima prenotazione<br>(minuti), durata periodo di grazia (minuti), numero<br>massimo di mezzi prenotabili per utente e importo<br>di addebito al minuto durante la pausa corsa (euro).<br>3. L’operatore inserisce i nuovi valori dei parametri<br>che intende modificare:<br>• 3.1 Se modifica la durata prenotazione,<br>inserisce il nuovo valore in minuti per la<br>durata massima di una prenotazione.<br>• 3.2 Se modifica la durata periodo di grazia,<br>inserisce il nuovo valore in minuti; se<br>impostato a zero, la pausa gratuita è<br>disabilitata.<br>• 3.3 Se modifica il numero massimo mezzi,<br>inserisce il numero massimo di mezzi<br>prenotabili contemporaneamente da un<br>singolo utente.<br>• 3.4 Se modifica l'addebito pausa corsa,<br>inserisce l'importo in euro addebitato per |

ogni minuto di pausa al termine del periodo di grazia; se impostato a zero, la pausa non comporta alcun addebito aggiuntivo.
4. L’operatore conferma le modifiche.
5. Se il sistema rileva che uno o più valori non
rispettano i vincoli di validazione (non numerici, negativi, oppure numero massimo mezzi non intero positivo), viene restituito un errore e il caso d’uso riprende al passo 3
6. Altrimenti Il sistema salva i nuovi parametri.
7. Il sistema mostra un messaggio di conferma
all’operatore.

| Campo | Valore |
|---|---|
| **Post-condizioni** | I nuovi parametri numerici sono salvati nel sistema<br>e applicati a tutte le operazioni successive:<br>1. le prenotazioni scadranno secondo la nuova<br>durata massima;<br>2. le pause corsa applicheranno il nuovo periodo di<br>grazia e il nuovo importo di addebito al minuto<br>3. le prenotazioni di gruppo rispetteranno il nuovo<br>limite massimo di mezzi. |
| **Sequenza alternativa degli eventi** | Nessuna |

### 2.3 System Architecture

#### 2.3.1 Diagramma delle Componenti – Diagramma Generale

##### 2.3.1.1 Client

##### 2.3.1.2 Server

#### 2.3.2 Specifica delle componenti

L’architettura portante del sistema segue il modello Client-Server, arricchito dall'integrazione del pattern logico MVC (Model-View-Controller), da un'estensione su più livelli e dalla comunicazione con servizi esterni.

##### 2.3.2.1 Specifica delle componenti client

Il blocco Client gestisce l'interfaccia utente (Frontend) e la comunicazione iniziale con il server tramite le API. VIEW: Gestisce l'interfaccia grafica e l'interazione con le diverse tipologie di utenti del sistema
- VistaAuth: Gestisce l'autenticazione. Contiene la classe:
  - VistaLogin: Schermata per l'inserimento delle credenziali (username e password) e l'accesso al sistema.
- VistaUtente: Interfaccia per il cliente finale. Contiene le classi:

  - VistaHomePageUtente: Schermata principale per l'utente, mostra la mappa geografica con la posizione in tempo reale dei mezzi disponibili.
  - VistaCorsa: Schermata attiva durante il noleggio, mostra i dati in tempo reale (tempo trascorso, costo stimato, pulsante per terminare la corsa).
  - VistaSegnalazioneUtente: Schermata che permette all’utente di inviare una segnalazione.
  - VistaPagamento: Schermata dedicata ai pagamenti.
  - VistaAbbonamenti: Schermata che permette di mostrare all’utente gli abbonamenti offerti dalla piattaforma.
- VistaOperatore: Interfaccia per il personale di gestione sul campo. Contiene le classi:
  - VistaDashBoardOperatore: È la schermata principale di controllo per l'operatore. Fornisce una panoramica dello stato del servizio, notifiche in tempo reale su eventuali anomalie dei mezzi, segnalazioni degli utenti o task di manutenzione da completare.
  - VistaDefinisciZona: Interfaccia grafica che permette all'operatore di tracciare e definire nuove aree operative sulla mappa o di modificare quelle esistenti. Viene utilizzata per impostare aree di geofencing, come zone di parcheggio obbligatorio, zone in cui è vietata la sosta o aree a velocità limitata.
  - VistaTariffeOfferte: Schermata per la gestione e la configurazione economica del servizio. Permette all'operatore di inserire nuovi piani tariffari (es. costo di sblocco e costo al minuto) o di creare e attivare codici promozionali e sconti per gli utenti.
  - VistaMezziOperatore: Pannello tecnico focalizzato sulla gestione fisica della flotta. Consente di visualizzare l'elenco completo dei veicoli, filtrandoli per stato (es. carica bassa, in manutenzione, disponibile), e include le funzionalità per registrare un nuovo mezzo nel sistema o forzare la chiusura di una corsa.
  - VistaImpostazioniRegole: Schermata di configurazione aziendale e sistemistica in cui l'operatore definisce i parametri generali di funzionamento e le regole di fine corsa (ad esempio, l'obbligo

per l'utente di scattare una foto al mezzo parcheggiato prima di poter chiudere il noleggio).
  - VistaSegnalazioneOP: Schermata per la gestione e le risposte alle segnalazioni utente. L’operatore può prendere in carico la segnalazione.
  - VistaParametriSistema: Schermata di configurazione dei parametri di sistema tra cui: il numero massimo di mezzi prenotabili da un utente, i minuti del periodo di pausa e il relativo addebito e i minuti massimi per la prenotazione di un mezzo.
- VistaAmministrazionePubblica: Interfaccia dedicata agli enti pubblici per il monitoraggio. Contiene la classe
  - VistaDashboardAP: Interfaccia di monitoraggio riservata alla Pubblica Amministrazione per visionare dati aggregati sul traffico e sull'uso del servizio. API SERVICE LAYER: Funge da intermediario tra le Viste (interfaccia) e il Server, esponendo o consumando i servizi di rete tramite l'interfaccia APIToView. Le classi incluse:
- ApiService: Classe di base per la gestione delle richieste HTTP (GET, POST, ecc.) e per la cattura e visualizzazione degli errori di rete.
- AuthService: Gestisce le chiamate API relative ai token di accesso, login e logout.
- PaymentService: Invia le richieste di transazione finanziaria e salvataggio dei metodi di pagamento.
- ReportService: Richiede al server i dati analitici per la generazione dei report.
- MapService: Interroga il server per ottenere le coordinate dei mezzi da mostrare sulla mappa.
- ZonaService: Gestisce il recupero delle informazioni sulle aree operative.
- FlottaService: Invia i comandi di aggiornamento dello stato della flotta
- CorsaService: Invia le richieste di blocco temporaneo o sblocco del veicolo.
- ConfigurazioneService: Richiede al server i parametri di sistema

- RegoleFineCorsaService: Richiede al server quali sono le regole fine corsa e eventuali modifiche.
- SegnalazioneService: Richiede al server la lista delle segnalazioni
- AbbonamentoService: Richiede al server gli abbonamenti disponibili
- OffertaService: richiede al server le offerte del sistema

##### 2.3.2.2 Specifica delle componenti server

Il Server elabora la logica di business, coordina i dati e interagisce con il database. È diviso in 4 strati principali staccati e comunicanti tramite interfacce dedicate. CONTROLLER: Riceve le richieste dal Client tramite l'interfaccia ClientToServer e coordina il flusso applicativo verso la Business Logic.
- AuthController: Gestisce la sicurezza e l'accesso
  - LoginController: Riceve le credenziali dal client e avvia la procedura di controllo dell'identità.
- UtenteController: Coordina le azioni degli utenti standard
  - CorsaController: Riceve le richieste di prenotazione o sblocco del mezzo fatte dall'utente.
  - PagamentoController: Intercetta le richieste di pagamento a fine corsa o all'aggiunta di una carta.
  - HomePageUtenteController: Smista le richieste iniziali dell'utente all'apertura dell'app.
  - AbbonamentoController: Riceve le richieste di sottoscrivere un nuovo abbonamento
  - SegnalazioneUtController: riceve e gestisce le segnalazioni
- OperatoreController: Gestisce le operazioni sui mezzi e il territorio
  - MezzoOperatoreController: Gestisce i flussi di inserimento o modifica dello stato dei veicoli inviati dal personale sul campo.
  - ZonaOperatoreController: Gestisce le richieste di creazione e modifica delle zone geografiche e delle relative tariffe/regole.
  - OffertaController: gestisce le richieste di creazione e modifica di offerte e tariffe.

  - DashBoardOPController: gestisce le richieste di estrazione dei dati riguardanti la dashboard
  - ConfigurazioneController: gestisce la richiesta di modifica dei parametri di sistema
  - segnalazioneOPController: gestisce il flusso di visualizzazione e presa in carico delle segnalazioni
  - RegoleFineCorsaController: gestisce le richiesta di modifica delle regole fine corsa
- AmministrazionePubblicaController: Gestisce la reportistica istituzionale
  - APController: Gestisce le richieste di estrazione dati e statistiche da parte dei sistemi dell'Amministrazione Pubblica. BUSINESS LOGIC LAYER: Rappresenta il cuore del sistema, dove risiedono le regole di business del software. Comunica con i controller tramite l'interfaccia BLLToController.
- ServizioMobilità: Applica le regole per l'avvio e la terminazione di una corsa, lo sblocco fisico del mezzo e il cambio di stato del veicolo.
- ServizioGIS: Elabora i calcoli geografici, verifica se un mezzo si trova all'interno di una determinata area e definisce i confini dei perimetri operativi.
- ServizioUtenti: Contiene la logica per validare le registrazioni, verificare i documenti di guida e modificare i profili.
- ServizioPricing: Calcola la tariffa finale del noleggio in base al tempo, alla distanza e ad eventuali promozioni attive.
- ServizioReport: Aggrega i dati di utilizzo del sistema e genera i file (es. CSV) per il monitoraggio.
- ServizioPrenotazione: Verifica se un mezzo è effettivamente opzionabile e ne gestisce il timer di scadenza della prenotazione.
- ServizioSegnalazione: Contiene la logica per inviare e gestire le segnalazioni
- ServizioOfferta: contiene la logica per la creazione e modifica delle offerte

- ServizioAbbonamento: contiene la logica per la creazione e modifica degli abboanmenti
- ServizioParametri: contiene la logica per impostare i parametri
- ServizioRegoleFineCorsa: contiene la logica per impostare regole fine corsa MODEL: Rappresenta le entità di business del dominio "Smart Mobility". Comunica con la BLL tramite l'interfaccia ModelToBLL.
- Utente: Rappresenta il cliente finale.
- Operatore: Rappresenta il dipendente aziendale con privilegi di gestione flotta.
- RegoleFineCorsa: Contiene i vincoli normativi o aziendali da rispettare per poter chiudere un noleggio (es. foto del parcheggio, zone consentite).
- Mezzo: Rappresenta il singolo veicolo (monopattino, bici, scooter) con targa, ID hardware, livello batteria e coordinate.
- Corsa: Rappresenta la transazione del noleggio (ora inizio, ora fine, mezzo usato, utente, percorso effettuato).
- Zona: Rappresenta un'area geografica poligonale sulla mappa dotata di specifiche regole (es. zona a velocità ridotta, zona di sosta vietata).
- Prenotazione: Rappresenta il blocco temporaneo di un mezzo da parte di un utente prima di iniziare la corsa.
- AmministrazionePubblica: Rappresenta l'ente esterno abilitato alla consultazione dei dati aggregati.
- Pagamento: Rappresenta la ricevuta della transazione economica associata a una corsa o a una penale.
- Tariffa: Modella i costi del servizio (costo al minuto, costo di sblocco, tariffe orarie).
- Promozione: sconto percentuale applicabile a una corsa, con data di scadenza. È un tipo di Offerta — l'utente la seleziona prima del pagamento e riduce l'importo finale.
- Abbonamento: piano a prezzo fisso con durata in giorni (es. mensile), opzionalmente limitato a un tipo di mezzo. Se attivo, azzera il costo di ogni corsa. È anch'esso un tipo di Offerta, sottoscritto dall'utente tramite AbbonamentoUtente.

- ParametriSistema: contiene i valori operativi configurabili del sistema: durata massima prenotazione, periodo di grazia, numero massimo di mezzi per utente, e addebito al minuto durante la pausa corsa. DATA ACCESS LAYER: Fornisce un'astrazione per l'accesso ai dati persistenti, isolando i modelli dal database reale. Comunica con i Modelli tramite l'interfaccia DALToModel. Implementa il pattern Repository
- AttoriRepository: Interroga e salva i dati di Utenti e Operatori.
- MezzoRepository: Gestisce la persistenza e l'aggiornamento dei dati fisici e di stato dei veicoli.
- CorsaRepository: Salva e recupera i dati storici e attivi dei noleggi.
- PrenotazioneRepository: Gestisce il salvataggio sul database delle prenotazioni attive o scadute.
- PagamentoRepository: Registra nel database lo stato delle transazioni (es. pagato, fallito).
- ZonaRepository: Mantiene persistenti le coordinate poligonali delle zone operative.
- TariffaRepository: Gestisce il salvataggio e la storicizzazione dei piani tariffari.
- RegoleFineCorsaRepository: Mantiene persistenti le regole e i vincoli di chiusura corsa nel database.

##### 2.3.2.3 Specifica delle componenti Servizi Esterni

SERVIZI ESTERNI: Sottosistema che raggruppa le API di terze parti, connesse tramite l'interfaccia ServiziEsterni.
- ProviderPagamenti: Gestisce la transazione monetaria in sicurezza
- GoogleMaps: Fornisce i servizi di geolocalizzazione, mappe e geofencing

##### 2.3.2.4 Specifica delle componenti Persistenza

Il livello finale di persistenza dei dati, collegato alla DAL tramite l'interfaccia DALtoDBMS.
- DBMS: Il sistema di gestione del database che esegue materialmente i comandi.

### 2.4 Detailed Product Design

#### 2.4.1 Diagramma delle Classi – Diagramma Generale

##### 2.4.1.1 Diagramma delle Classi – Client

##### 2.4.1.2 Diagramma delle Classi – Server

##### 2.4.1.3 Diagramma delle Classi – View

##### 2.4.1.4 Diagramma delle Classi – APIService

##### 2.4.1.5 Diagramma delle Classi – interfacce Client/Server

##### 2.4.1.6 Diagramma delle Classi – Controller

##### 2.4.1.7 Diagramma delle Classi – Business Logic Layer

##### 2.4.1.8 Diagramma delle Classi – Model

##### 2.4.1.9 Diagramma delle Classi – Data Access Layer

#### 2.4.2 Specifiche delle Classi

##### 2.4.2.1 Specifica delle Classi – Client

L'architettura è articolata in tre macro-aree:
- View — gestisce la presentazione e l'interazione con l'utente.
- API Service — gestisce la logica applicativa lato client e la comunicazione con il backend remoto.
- Interfacce — definiscono i contratti di comunicazione tra i livelli interni e con il server. Il Client è esposto come componente unico, suddiviso internamente nei sotto-componenti View e API Service. Le interfacce ApiToView e ServerToClient definiscono rispettivamente il contratto tra View e API Service e tra Client e backend.

###### 2.4.2.1.1 PANORAMICA ARCHITETTURALE

Le classi View comunicano con il livello API Service esclusivamente tramite l'interfaccia ApiToView, realizzata dalla classe ApiService. Quest'ultima agisce come façade verso un insieme di service specializzati per dominio (autenticazione, mappa, zone, pagamenti, flotta, reportistica, prenotazioni) e instrada le richieste verso il backend realizzando l'interfaccia ServerToClient. Questa organizzazione garantisce che:
- le viste non abbiano alcuna conoscenza diretta dei service applicativi né dei dettagli di comunicazione di rete;
- ogni service abbia un perimetro di responsabilità ben definito sul proprio dominio;
- il backend interagisca con il Client tramite un contratto unico e indipendente dalle viste.

###### 2.4.2.1.2 INTERFACCE

1 Interfaccia ClientToServer
- Stereotipo: «interface»

- Ruolo: definisce il contratto delle operazioni che il Server espone verso il Client. È realizzata da ApiService lato Client e dal Server lato backend.
- Ambito funzionale: autenticazione e gestione del profilo utente, ciclo di vita della corsa (prenotazione, sblocco, terminazione), gestione dei pagamenti, ricerca dei mezzi e caricamento mappa, gestione della flotta, definizione di zone e regole di fine corsa, tariffazione e reportistica.
2 Interfaccia ApiToView
- Stereotipo: «interface»
- Ruolo: definisce il contratto tra View e API Service. È realizzata da ApiService e costituisce il punto di ingresso unico utilizzato dalle viste per richiedere operazioni applicative o aggiornamenti di stato.
- Ambito funzionale: autenticazione, prenotazione e gestione della corsa, pagamenti, gestione operativa e amministrativa di mezzi, zone e tariffe, presentazione dei form di accesso e caricamento della mappa.

###### 2.4.2.1.3 LIVELLO API SERVICE

- Classe ApiService (Stereotipi: «Facade», «Singleton»): punto di ingresso unico del livello API Service. Realizza l'interfaccia ApiToView orchestrando le chiamate verso i service specializzati e instrada le richieste verso il Server realizzando l'interfaccia ServerToClient. Si occupa inoltre dell'invio delle richieste HTTP, della gestione delle risposte e della propagazione degli errori alle viste, oltre che della ricezione di notifiche asincrone dal server. Essendo Singleton, garantisce un'unica istanza condivisa tra tutte le viste per l'intera sessione utente.
- Classe AuthService: gestisce l'autenticazione dell'utente, la registrazione, la modifica dei dati di account e il mantenimento dello stato di sessione. Espone inoltre la verifica della presenza di una sessione attiva.
- Classe MapService: gestisce il caricamento della mappa, l'aggiornamento periodico della posizione dell'utente e la ricerca dei mezzi disponibili nelle vicinanze a partire dalle coordinate correnti.

- Classe ZonaService: gestisce la creazione delle zone (operative, vietate, parcheggio) e ne mantiene una cache locale a supporto delle viste cartografiche.
- Classe PaymentService: gestisce il portafoglio dell'utente, i metodi di pagamento salvati (incluso il metodo predefinito) e l'esecuzione delle transazioni di pagamento associate alle corse.
- Classe FlottaService: gestisce la flotta di mezzi sul lato operatore e amministratore. Si occupa dell'aggiunta di nuovi mezzi, della modifica del loro stato operativo, della dismissione, della verifica di disponibilità, oltre che della gestione delle tariffe e delle regole di fine corsa e del recupero della configurazione corrente di parcheggi e zone.
- Classe ReportService: recupera dal backend i dati statistici e i report aggregati a supporto della dashboard dell'amministratore di piattaforma.
- Classe CorsaService: gestisce l'intero ciclo di vita della prenotazione, dalla creazione della stessa allo sblocco del mezzo con conseguente avvio della corsa, fino alla terminazione e produzione del riepilogo finale.
- SegnalazioneService: Gestione dell'invio delle segnalazioni di anomalia su un mezzo da parte dell'utente (lato utente). Recupero e gestione dell'elenco delle segnalazioni ricevute a supporto della dashboard operatore (lato operatore).
- AbbonamentoService: Recupero dei piani di abbonamento disponibili pubblicati dall'operatore. Gestione della sottoscrizione di un abbonamento da parte dell'utente e verifica dello stato di sottoscrizione attiva.
- Offerta Service: Recupero delle promozioni/offerte attive a supporto delle viste utente (visualizza promozioni). Gestione della creazione e configurazione di offerte commerciali con condizioni e scadenza (lato operatore).
- ConfigurazoneService: Recupero e impostazione dei parametri numerici di sistema configurabili dall'operatore (durata prenotazione, durata periodo di grazia, numero massimo mezzi per prenotazione di gruppo, addebito pausa corsa, importo bonus).

###### 2.4.2.1.4 LIVELLO VIEW

Le classi View rappresentano le schermate dell'applicazione. Tutte dialogano con il livello API tramite l'interfaccia ApiToView e sono raggruppate per profilo utente: Utente finale, Operatore e Amministratore pubblica.

###### 2.4.2.1.4.1 UTENTE

- VistaAccount: gestisce login, registrazione e recupero credenziali. Costituisce la vista radice dell'applicazione, da cui dipendono funzionalmente tutte le altre viste.
- VistaHomepageUtente: rappresenta la schermata principale dell'utente e visualizza la mappa con i mezzi disponibili nelle vicinanze e le zone definite sul territorio.
- VistaCorsa: gestisce la corsa attiva, dallo sblocco del mezzo alla terminazione. Visualizza informazioni quali durata, distanza e costo, segnala l'ingresso in zone vietate e mostra il riepilogo finale al termine della corsa.
- VistaPrenotazioneMezzo: gestisce la selezione e la prenotazione di un mezzo dalla mappa, mostrando le conferme di prenotazione e segnalando eventuali errori di disponibilità.
- VistaPagamento: gestisce il portafoglio dell'utente, l'aggiunta di nuovi metodi di pagamento e l'esecuzione del pagamento al termine della corsa, mostrando i relativi riepiloghi e conferme.
- VistaSegnalazione: invio di una segnalazione su un mezzo (selezione tipo anomalia, descrizione) con conferma di invio.
- VistaAbbonamenti: consultazione dei piani disponibili e sottoscrizione di un abbonamento, con riepilogo e conferma.
- VistaPromozioni: consultazione delle promozioni/offerte attive applicabili

###### 2.4.2.1.4.2 Amministratore Pubblica

- VistaDashboardAP: fornisce la dashboard di reportistica e analisi statistica per l'amministratore, con la possibilità di esportare i dati in formato CSV e PDF.

###### 2.4.2.1.4.3 Operatore

- VistaDashboardOperatore: rappresenta la dashboard principale dell'operatore e costituisce il punto di accesso alla mappa operativa con i mezzi gestiti.
- VistaMezziOperatore: consente la gestione completa dei mezzi della flotta, comprendendo la visualizzazione della lista, la modifica dello stato di un mezzo, l'aggiunta di nuovi mezzi e la richiesta di dismissione, con relative conferme e notifiche di esito.
- VistaDefinisciZona: fornisce un editor cartografico per la definizione di nuove zone (parcheggio, operative, vietate), con conferma del perimetro disegnato e possibilità di ritornare in editing in caso di errore.
- VistaImpostazioniRegole: consente la configurazione delle regole di fine corsa, come ad esempio l'obbligo di sosta in determinate zone parcheggio, con relativa conferma di salvataggio.
- VistaTariffeOfferte: gestisce le tariffe e le promozioni applicate ai mezzi, consentendone la visualizzazione e la creazione di nuove tariffe.
- VistaGestioneSegnalazioni: lista delle segnalazioni ricevute, consultazione del dettaglio e pianificazione interventi (integrata o accessibile dalla VistaDashboardOperatore).
- VistaConfigurazioneParametri: configurazione dei parametri numerici di sistema (durata prenotazione, periodo di grazia, numero massimo mezzi, addebito pausa, bonus), con validazione e conferma di salvataggio.
- VistaGestioneUtenti (Operatore): consultazione della lista utenti e sospensione/riattivazione di un account, con conferma e notifica di esito.

###### 2.4.2.1.5 RELAZIONI TRA LE CLASSI

- Realizzazioni di interfaccia:
  - ApiService realizza ApiToView (verso il livello View).
  - ApiService realizza ServerToClient lato Client; il Server la usa lato backend.
- Dipendenze «use»:

  - AuthService, MapService, ZonaService, PaymentService, FlottaService, ReportService e PrenotazioneService utilizzano ApiService.
  - Tutte le classi Vista* utilizzano ApiToView.
- Associazioni tra viste:
  - VistaAccount è la vista radice; sono ad essa associate VistaHomepageUtente, VistaCorsa, VistaPrenotazioneMezzo, VistaPagamento, VistaMezziOperatore, VistaDashboardOperatore, VistaDashboardAP, VistaDefinisciZona, VistaTariffeOfferte e VistaImpostazioniRegole.

##### 2.4.2.2 Specifica delle Classi – Server

L'architettura server è articolata in quattro macro-aree:
- Controller — gestisce la ricezione delle richieste HTTP e la restituzione delle risposte al client.
- Business Logic Layer (BLL) — contiene la logica applicativa e di dominio.
- Model — rappresenta le entità di dominio del sistema e incapsula lo stato e il comportamento degli oggetti di business.
- Data Access Layer (DAL) — gestisce la persistenza e l'accesso ai dati tramite repository. Il Server è esposto come componente unico, suddiviso internamente nei sotto-componenti Controller, BLL e Model. Le interfacce BLLToController e ModelToBLL definiscono rispettivamente il contratto tra Controller e BLL e tra BLL e Model. L'interfaccia DALtoModel definisce il contratto tra Model e Data Access Layer.

###### 2.4.2.2.1 PANORAMICA ARCHITETTURALE

I Controller ricevono le richieste HTTP dal Client e delegano l'elaborazione al livello BLL esclusivamente tramite l'interfaccia BLLToController, realizzata dai service del Business Logic Layer. I service della BLL operano sui modelli di dominio tramite l'interfaccia ModelToBLL e accedono alla persistenza tramite i Repository del Data Access Layer, che realizzano l'interfaccia DALtoModel.

Questa organizzazione garantisce che:
- i Controller non abbiano alcuna conoscenza diretta della logica di business né dei dettagli di accesso ai dati;
- ogni service BLL abbia un perimetro di responsabilità ben definito sul proprio dominio applicativo;
- i Repository costituiscano l'unico punto di accesso al database, isolando il resto del sistema dai dettagli di persistenza.

###### 2.4.2.2.2 INTERFACCE

- Interfaccia ServerToClient
  - Stereotipo: «interface»
  - Ruolo: Definisce il contratto per l'invio delle richieste dal Client verso il Server. È invocata dall'API Service Layer del client e implementata dai Controller del backend per gestire i dati di input.
  - Ambito funzionale: Inoltro credenziali di accesso, invio comandi del ciclo di corsa (prenotazione, sblocchi, chiusure), trasmissione dati di pagamento, richieste di coordinate per mappe/mezzi, e invio di comandi gestionali dell'operatore (modifica flotta, tariffe, regole e geofencing).
- Interfaccia BLLToController
  - Stereotipo: «interface»
  - Ruolo: definisce il contratto delle operazioni che il livello BLL espone verso i Controller. È realizzata da ServizioMobilità e dagli altri service della BLL.
  - Ambito funzionale: autenticazione e gestione del profilo utente, ciclo di vita della prenotazione e della corsa, gestione dei pagamenti, gestione della flotta di mezzi, definizione di zone e regole di fine corsa, tariffazione e reportistica.
- Interfaccia ModelToBLL
  - Stereotipo: «interface»

  - Ruolo: definisce il contratto tra le entità del Model e il livello BLL. È realizzata dalle classi del Model (Utente, Corsa, Mezzo, Prenotazione, Pagamento, Tariffa, Zona, RegolaFineCorsa).
  - Ambito funzionale: creazione e aggiornamento delle entità di dominio, accesso agli attributi e alle operazioni di business delle singole entità.
- Interfaccia DALtoModel
  - Stereotipo: «interface»
  - Ruolo: definisce il contratto che i Repository devono rispettare per l'accesso al database. È realizzata da tutti i Repository del Data Access Layer.
  - Ambito funzionale: esecuzione di query, aggiornamenti, ricerca per identificatore, ricerca per coordinate e per email.
- Interfaccia DBMS
  - Stereotipo: «interface»
  - Ruolo: definisce il contratto di accesso al database relazionale. Espone executeQuery(sql): ResultSet, executeUpdate(sql): int e connettDB().

###### 2.4.2.2.3 LIVELLO CONTROLLER

- AccountController: Stereotipi: «FrontController»: è il punto di ingresso unico delle richieste HTTP in ingresso. Gestisce il routing verso i controller specializzati, la gestione centralizzata delle eccezioni e il reindirizzamento in caso di errore.
- HomePageUtenteController: gestisce le richieste relative alla homepage dell'utente, tra cui il caricamento della mappa e la visualizzazione dei mezzi disponibili nelle vicinanze.
- CorsaController: gestisce il ciclo di vita della prenotazione lato server, dalla creazione della prenotazione allo sblocco del mezzo fino alla terminazione della corsa.
- PagamentoController: gestisce le operazioni relative ai metodi di pagamento, tra cui il recupero dei metodi salvati, la creazione di nuovi metodi, la validazione del profilo di pagamento e il calcolo dell'importo finale.

- DashboardOPController: gestisce le richieste della dashboard dell'amministratore di piattaforma, fornendo i dati statistici aggregati e la risposta con le informazioni di mappa e reportistica.
- TariffeController: gestisce le operazioni CRUD sulle tariffe applicate ai mezzi, esponendo gli endpoint per la creazione, il recupero e la modifica delle tariffe.
- MezziOperatoreController: gestisce le operazioni sulla flotta di mezzi lato operatore, tra cui l'aggiunta di nuovi mezzi, la modifica dello stato operativo, la dismissione e la modifica dello stato di un mezzo.
- ZoneController: gestisce la creazione, la modifica e il recupero delle zone geografiche (operative, vietate, parcheggio) e delle relative configurazioni cartografiche.
- AmministrazionePubblicaController: gestisce le richieste provenienti dall'amministrazione pubblica, in particolare il recupero dei report periodici aggregati.
- SegnalazioneController — gestione delle richieste relative alle segnalazioni: ricezione di una nuova segnalazione (lato utente) e recupero dell'elenco delle segnalazioni (lato operatore).
- AbbonamentoController — gestione delle richieste relative agli abbonamenti: recupero dei piani disponibili, sottoscrizione di un abbonamento e creazione/modifica dei piani (lato operatore).
- OffertaController — operazioni CRUD sulle offerte/promozioni (creazione, recupero, modifica) con condizioni e scadenza configurabili.
- ConfigurazioneController — gestione delle richieste di lettura e aggiornamento dei parametri numerici di sistema.
- AccountUtenteController (Operatore): gestione delle richieste di sospensione e riattivazione dell'account di un utente.

###### 2.4.2.2.4 LIVELLO BUSINESS LOGIC LAYER

- ServizioMobilità: orchestratore principale della BLL. Gestisce l'intero ciclo di vita della corsa, la verifica della disponibilità dei mezzi, lo sblocco, la terminazione, il calcolo dell'importo e la gestione delle zone geografiche. Coordina le interazioni tra ServizioGIS, ServizioPagamenti, ServizioPrenotazione e i Repository.

- ServizioGIS: gestisce le operazioni geografiche e cartografiche. Si occupa del recupero delle zone attive, della verifica della posizione del mezzo rispetto alle zone consentite e vietate, della validazione della posizione di fine corsa e del caricamento della mappa cartografica.
- ServizioPagamenti: gestisce l'autorizzazione dei pagamenti tramite il ProviderPagamenti, la creazione dei record di pagamento, la validazione dei metodi di pagamento e la gestione delle transazioni associate alle corse. Espone inoltre le operazioni di amministrazione degli account di pagamento.
- ServizioPrenotazione: gestisce la logica di creazione delle prenotazioni, l'applicazione delle promozioni disponibili e la verifica della scalabilità in termini di disponibilità dei mezzi.
- ServizioTariffe: gestisce la logica di tariffazione. Si occupa del recupero delle tariffe applicabili per tipologia di mezzo, della validazione delle tariffe e della promozione delle promozioni attive.
- ServizioReport: genera i report statistici aggregati per l'amministratore di piattaforma e per l'amministrazione pubblica, esportando i dati in formato CSV e fornendo le metriche di utilizzo della flotta e dei pagamenti.
- ServizioSegnalazioni — logica di registrazione e recupero delle segnalazioni; associazione della segnalazione al mezzo e all'utente segnalante.
- ServizioOfferte — logica di gestione di promozioni e abbonamenti: validazione delle condizioni e delle scadenze, applicazione delle promozioni attive in fase di tariffazione, gestione della sottoscrizione e del calcolo del bonus.
- ServizioConfigurazione — logica di gestione dei parametri di sistema: validazione dei valori rispetto agli intervalli ammessi e persistenza della configurazione corrente.
- ServizioGestioneUtenti: logica di sospensione e riattivazione dell'account utente, con verifica delle precondizioni e aggiornamento dello stato. Coordinato da Servizio Mobilità.

###### 2.4.2.2.5 LIVELLO MODEL

- Persona: classe base astratta per tutti gli attori del sistema. Contiene gli attributi comuni di anagrafica (id, nome, cognome, email) e il metodo di login.
- Utente: rappresenta l'utente finale del sistema. Estende Persona e mantiene le associazioni con le prenotazioni, i metodi di pagamento e le corse effettuate. Espone le operazioni di modifica del profilo.
- Operatore: rappresenta l'operatore di flotta. Estende Persona e ha responsabilità sulla gestione dei mezzi assegnati, sulla modifica dello stato operativo e sulla gestione delle tariffe.
- AmministrazionePubblica: rappresenta l'ente pubblico che accede ai report aggregati del sistema. Estende Persona ed espone il metodo di recupero dei report periodici.
- Mezzo: rappresenta un mezzo della flotta. Mantiene lo stato operativo (StatoMezzo), le coordinate geografiche correnti, la lunghezza e la StatoDisponibilità. Espone le operazioni di blocco/sblocco e aggiornamento della posizione.
- Prenotazione: rappresenta la prenotazione di un mezzo da parte di un utente. Mantiene lo stato della prenotazione (StatoPrenotazione), l'associazione con il mezzo, l'utente e la corsa. Espone il metodo getBiglietto().
- Corsa: rappresenta una corsa effettuata da un utente. Mantiene lo stato (StatoCorsa), le date di inizio e fine, il costo calcolato e il percorso. Espone le operazioni getDatiCorsa(), setStato() e creaCorsa(), oltre al metodo di calcolo del costo finale.
- Pagamento: rappresenta una transazione di pagamento associata a una corsa. Mantiene l'importo, la data, lo stato (StatoPagamento) e il transactionId. Espone il metodo valida() e crea().
- MetodoPagamento: rappresenta un metodo di pagamento salvato dall'utente. Mantiene il tipo (TipoMetodo), il token_esterno e il flag risposta Predefinita. Ha molteplicità 0..* rispetto all'utente.
- Tariffa: rappresenta la struttura tariffaria applicata a un mezzo. Mantiene il tipo di tariffa (TipoTariffa), il costo al minuto, il costo al km e lo stato (StatoTariffa). Espone le operazioni calcolaTariffe() e modificaTariffa().

- Zona: rappresenta una zona geografica del sistema (operativa, vietata, parcheggio). Mantiene le coordinate del perimetro, il nome e il tipo (TipoZona). Espone le operazioni di creazione e recupero delle zone figlie.
- RegolaFineCorsa: rappresenta una regola che vincola la terminazione della corsa (es. obbligo di sosta in una zona parcheggio). Mantiene l'associazione con la tariffa e la policy applicata. Espone il metodo crea().
- Segnalazione: rappresenta una comunicazione inviata dall'utente all'operatore per notificare un'anomalia su un mezzo (danno, guasto, posizione anomala). Mantiene il tipo di anomalia (TipoAnomalia), la descrizione, la data e lo stato (StatoSegnalazione), ed è associata al mezzo segnalato e all'utente segnalante. Espone il metodo crea().
- Offerta: classe base che rappresenta una politica commerciale configurata e pubblicata dall'operatore. Mantiene nome, descrizione, condizioni, data di scadenza e stato (StatoOfferta). Espone i metodi crea() e verificaValidità().
- Promozione: estende Offerta e rappresenta un'offerta che riduce la tariffa standard (es. sconto percentuale, prime N corse gratis). Mantiene il tipo e il valore dello sconto e viene applicata in fase di tariffazione.
- Abbonamento: estende Offerta e rappresenta un contratto a tempo determinato che garantisce all'utente condizioni tariffarie agevolate o un numero di corse incluse. Mantiene la durata, le corse incluse e la tariffa agevolata, ed è associato agli utenti sottoscrittori.
- ParametriSistema: rappresenta l'insieme dei parametri numerici di configurazione del sistema impostati dall'operatore (durata massima prenotazione, durata periodo di grazia, numero massimo mezzi, addebito pausa, valore bonus). Espone le operazioni di validazione e aggiornamento ed è estendibile con ulteriori parametri.

###### 2.4.2.2.6 LIVELLO DATA ACCESS LAYER

- Repository (Stereotipo: «Data Access Object») classe base per tutti i repository. Espone le operazioni comuni save(id) e delete(id).

- UtenteRepository: gestisce la persistenza degli utenti. Espone le operazioni di ricerca per email, per id e per coordinate, oltre alle operazioni di aggiornamento e cancellazione.
- MezzoRepository: gestisce la persistenza dei mezzi. Espone le operazioni di ricerca per tipologia, per stato, per identificativo e per operatore, oltre alle operazioni di aggiornamento e cancellazione.
- CorsaRepository: gestisce la persistenza delle corse. Espone le operazioni findById(), findByCorsaId(), update() e delete().
- PrenotazioneRepository: gestisce la persistenza delle prenotazioni. Espone le operazioni di ricerca per utente, per mezzo e per stato, oltre alle operazioni di aggiornamento.
- PagamentoRepository: gestisce la persistenza dei pagamenti. Espone le operazioni findByCorsaCorsa(), findByElencoId(), update(), save() e delete().
- TariffeRepository: gestisce la persistenza delle tariffe. Espone le operazioni di ricerca per tipologia, validazione della configurazione e aggiornamento.
- ZoneRepository: gestisce la persistenza delle zone geografiche. Espone le operazioni di ricerca per tipo, per coordinate, per nome e per zona padre, oltre all'aggiornamento.
- RegolaFineCorsa Repository: gestisce la persistenza delle regole di fine corsa. Espone le operazioni save(), find(), update() e delete().
- SegnalazioneRepository: gestisce la persistenza delle segnalazioni. Espone le operazioni di ricerca per mezzo, per utente e per stato, oltre alle operazioni di aggiornamento.
- OffertaRepository: gestisce la persistenza delle offerte commerciali (promozioni e abbonamenti). Espone le operazioni di ricerca per tipo, per stato e per scadenza, la validazione della configurazione e l'aggiornamento.
- BonusRepository: gestisce la persistenza dei bonus assegnati agli utenti. Espone le operazioni di ricerca per utente, oltre a save(), update() e delete().

- ParametriSistemaRepository: gestisce la persistenza dei parametri numerici di configurazione del sistema. Espone le operazioni di recupero della configurazione corrente e di aggiornamento.

###### 2.4.2.2.7 RELAZIONI TRA LE CLASSI

Realizzazioni di interfaccia:
- ServizioMobilità e i service BLL realizzano BLLToController (verso il livello Controller).
- Le classi del Model realizzano ModelToBLL (verso il livello BLL).
- Tutti i Repository realizzano DALtoModel (verso il Model). Dipendenze «use»:
- Tutti i Controller utilizzano BLLToController.
- ServizioMobilità utilizza ServizioGIS, ServizioPagamenti, ServizioPrenotazione, ServizioTariffe e ServizioReport.
- Tutti i service BLL utilizzano i rispettivi Repository del DAL. Associazioni tra classi del Model:
- Utente ha associazione 0..* con Prenotazione, MetodoPagamento e Corsa.
- Prenotazione ha associazione 1 con Mezzo e 0..1 con Corsa.
- Corsa ha associazione 1 con Pagamento e 0..1 con RegolaFineCorsa.
- Tariffa ha associazione 0..* con Mezzo e 1 con RegolaFineCorsa.
- Zona ha associazione 0..* con Mezzo tramite la verifica della posizione.

#### 2.4.3 Diagrammi di Sequenza

##### 2.4.3.1 UT - 01 Visualizza Mappa Utente

##### 2.4.3.2 UT - 02 Prenota Mezzo

##### 2.4.3.3 UT – 03 Sblocca Mezzo

##### 2.4.3.4 UT – 04 Termina Corsa

##### 2.4.3.5 UT – 05 Effettua Pagamento

##### 2.4.3.6 UT – 06 Salva Metodo di Pagamento

##### 2.4.3.7 UT – 07 Consulta Tariffe

##### 2.4.3.8 UT – 08 Visualizza Riepilogo Corsa

##### 2.4.3.9 UT - 09 Sospende Corsa

##### 2.4.3.10 UT – 10 Visualizza Promozioni

##### 2.4.3.11 UT – 11 Visualizza Storico Corsa

##### 2.4.3.12 UT – 12 Invia Segnalazione

##### 2.4.3.13 UT – 13 Sottoscrive Abbonamento

##### 2.4.3.14 AP – 01 Accede Report

##### 2.4.3.15 AP – 02 Esporta Report

##### 2.4.3.16 AP – 03 Visualizza Mappa Amministrazione Pubblica

##### 2.4.3.17 OP-01 Visualizza Mappa Operatore

##### 2.4.3.18 OP – 02 Aggiunge Mezzo

##### 2.4.3.19 OP – 03 Dismette Mezzo

##### 2.4.3.20 OP – 04 Modifica Stato Mezzo

##### 2.4.3.21 OP – 05 Definisce Tariffa

##### 2.4.3.22 OP – 06 Definisce Regole fine corsa

##### 2.4.3.23 OP – 07 Definisce Zona

##### 2.4.3.24 OP – 08 Gestisce Segnalazione

##### 2.4.3.25 OP – 09 Sospende account utente

##### 2.4.3.26 OP – 10 Definisce Offerta

##### 2.4.3.27 OP – 11 Configura parametri numerici di sistema

### 2.5 Data modeling and design

Qui va fornita la specifica di tutti i dati e le informazioni scambiate dal sistema in corso di realizzazione con l’utenza di riferimento e/o gli eventuali altri sistemi con cui esso comunica. Deve essere descritto il modello logico della base di dati e la sua struttura fisica.

#### 2.5.1 Modello logico del Database

#### 2.5.2 Struttura fisica del Database

## 3. PROMPT

### 3.1 Qualità dei requisiti

La seguente sezione riporta il prompt utilizzato per la convalidazione della qualità delle user story secondo le 14 caratteristiche di qualità definite nel corso. Le user story corrette a seguito di questa analisi sono riportate nel Product Backlog. You are a software engineer, specialized in requirements elicitation. In this phase, you need to read the User Stories. You need to read them carefully, evaluate them following the "Quality Verification Characteristics" that are listed below.
### Context
The municipality of Zootropolis wishes to introduce a sustainable transport system that integrates various sharing services (e.g., Bike, Car, E-scooter sharing) The system must operate in an urban environment involving:
- Users
- Operators
- Public authorities
## Expected Input Format
The user stories and "Quality Verification Characteristics" are written in Italian. The user stories that will be sent to you will be in this form: COME [ruolo] VOGLIO [fare qualcosa] COSÌ CHE [possa ottenere valore per il business]

To add more information, what follows is an example of a user story: `COME magazziniere VOGLIO poter filtrare l'archivio ordini secondo la data di ricezione COSÌ CHE possa consultare gli ordini evasi`
## Quality Verification Characteristics
All of them are reported below:
### 1. Non Ambiguo
Deve esserci un solo modo di interpretare ogni requisito. Le ambiguità sono create da: **Acronimi**: gli acronimi devono essere scritti per intero, con l'acronimo tra parentesi. Esempio scorretto: "Richiedere al cliente di digitare il PIN." Esempio corretto: "Richiedere al cliente di digitare il Personal Identification Number (PIN)." **Cattivo uso dei termini**: termini vaghi lasciano spazio a interpretazioni multiple. Esempio scorretto: "Il sistema dispensa contanti fino a 500 euro a scelta del cliente." Non è chiaro se la somma e digitata liberamente, scelta tra opzioni, arrotondata o rifiutata se fuori soglia. Esempio corretto: "Il sistema dispensa una somma a scelta del cliente tra quelle proposte: 100, 150, 200, 250, 300, 400, 500 euro." **Eccessiva sintesi**: una formulazione troppo breve omette dettagli necessari. Esempio scorretto: "Il sistema mostra 5 movimenti di Deposito o di Conto Corrente quando il cliente chiede l'estratto conto." Non è chiaro quali 5 movimenti vengano mostrati.

Esempio corretto: "Il cliente richiede l'estratto conto indicando il numero di ultimi movimenti desiderati, fino a un massimo di 20, sul conto di deposito o di conto corrente selezionato. Il sistema mostra 5 movimenti per videata. Se il cliente richiede più di 20 movimenti, il sistema riduce il numero a 20 e avverte il cliente."
### 2. Provabile o Verificabile
Deve essere possibile costruire casi di test corretti e non corretti rispetto a ogni requisito, per verificare che il sistema elabori correttamente i primi e rigetti i secondi. Elementi che rendono un requisito non provabile:
- Aggettivi generici: robusto, sicuro, accurato, effettivo, efficiente, espandibile, flessibile, mantenibile, disponibile, amichevole, adeguato.
- Avverbi generici: velocemente, tranquillamente, tempestivamente.
- Parole ed acronimi non specifici: ecc., e/o, TBD.
- Parole generiche: gestire, manipolare.
- Espressioni generiche: che sia appropriato, come richiesto, se necessario.
- Pronomi indefiniti: pochi, molti, tanto, spesso, qualche volta, tutti, qualsiasi, alcune, qualcuno.
- Voci passive: il soggetto riceve l'azione del verbo invece di compierla. Esempio scorretto: "Il numero di conto digitato dal cliente sarà controllato per esattezza ed esistenza nella base dati." Esempio corretto: "Il sistema controlla che il numero di conto digitato sia corretto sintatticamente ed esista nella base di dati."

### 3. Chiaro
Il requisito deve essere conciso, laconico, semplice e preciso. Non deve contenere verbosità o informazioni non necessarie. Esempio scorretto: "Qualche volta il cliente potrebbe chiedere l'estratto conto del deposito o del conto corrente intestato a lui; in tal caso deve dichiarare il periodo a cui si deve riferire l'estratto conto richiesto ed è necessario chiedere se vuole la stampa su carta o gli basta vederlo sul video." Esempio corretto: "Il cliente può chiedere l'estratto conto per il periodo che dichiara. Il sistema riporta l'estratto conto, a scelta del cliente, su carta o su video."
### 4. Corretto
Se un requisito contiene fatti, questi devono essere veri. Esempio scorretto: "Il costo dell'operazione sarà di 1 euro." Questo requisito non è corretto per almeno due motivi: le operazioni eseguibili all'ATM non hanno tutte lo stesso prezzo, e il prezzo dipende dalla politica della banca che gestisce l'ATM e dagli accordi con la banca emittente della carta.
### 5. Comprensibile
I requisiti devono essere grammaticalmente corretti e scritti in stile consistente. Devono essere usati appositi standard terminologici. La parola "deve" deve essere utilizzata al posto di "volere", "bisogna" o "può".

### 6. Fattibile
I requisiti devono essere realizzabili entro i vincoli esistenti di tempo, denaro e risorse disponibili. Esempio scorretto: "Il sistema userà un linguaggio naturale nell'interfaccia così che comprenda i comandi espressi in lingua italiana." Questo requisito richiede un grande investimento di tempo e risorse, con notevole rischio di non essere realizzato con un adeguato livello di affidabilità.
### 7. Indipendente e Auto-consistente
Per comprendere un requisito non deve essere necessario conoscere nessun altro requisito. Esempio scorretto:
- ReqI: "Il sistema elenca tutti gli importi erogabili per il cliente che ha inserito la carta di credito nell'ATM."
- ReqD: "Essi sono elencati in ordine crescente." Il pronome "essi" si riferisce agli importi di ReqI. Se l'ordine dei requisiti nello SRS venisse modificato, ReqD diventerebbe incomprensibile.
### 8. Atomico
Ogni requisito deve contenere un solo elemento tracciabile. Le espressioni che contengono "e" o "ma" devono essere riviste e suddivise.

Esempio scorretto: "Il cliente inserisce il PIN, chiede l'erogazione di una somma e l'estratto conto." Questo requisito ne contiene tre atomici distinti e deve essere suddiviso di conseguenza.
### 9. Necessario
Un requisito e inutile se nessuna parte interessata ne ha bisogno, oppure se la sua cancellazione non ha alcuna conseguenza sul sistema finale perché non aggiunge informazioni. I requisiti inutili sono quelli che l'analista inserisce nello SRS ritenendoli desiderati dalle parti interessate, senza che nessuna di esse li abbia esplicitamente richiesti. Esempi di requisiti potenzialmente non necessari:
- "Tutti i requisiti specificati nello SRS devono essere testati."
- "Il sistema stampa il nome della filiale che gestisce l'ATM utilizzato dal cliente."
### 10. Astratto
I requisiti non devono contenere dettagli circa la loro implementazione, salvo che tale dettaglio costituisca un vincolo esplicitamente dichiarato dall'utente. L'implementazione e di interesse del progettista, non degli utenti del sistema. Esempio: "Il contenuto informativo sarà memorizzato in forma strutturata." Questo requisito specifica un dettaglio implementativo e deve essere rivisto salvo che rappresenti un vincolo esplicito.
### 11. Consistente

Tutti i requisiti devono utilizzare termini uguali per esprimere concetti uguali, e nessun requisito deve essere conflittuale con altri. I conflitti possono essere: **Diretti**: in una stessa situazione il comportamento del sistema deve essere diverso. Esempio:
- ReqX: "L'ATM accetta tutte le carte di credito e il Bancomat emesso da qualsiasi banca."
- ReqY: "L'ATM accetta i Bancomat emessi dalle banche convenzionate con la banca gestore." Per eliminare il conflitto e necessario cancellare uno dei due requisiti. Esempio di terminologia inconsistente e conflitto sul formato:
- ReqX: "Le date devono essere visualizzate nella forma mm/dd/yyyy."
- ReqY: "Le date devono essere visualizzate nella forma gg/mm/aaaa." Possibile correzione con precisazione del contesto:
- ReqX: "Le date per gli ATM in U.S. devono essere visualizzate nella forma mm/dd/yyyy."
- ReqY: "Le date per gli ATM in Italia devono essere visualizzate nella forma gg/mm/aaaa." In alternativa, generalizzando: "Le date saranno visualizzate nel formato definito dall'utente all'installazione." **Indiretti**: due requisiti non descrivono la stessa situazione ma non è possibile soddisfarli contemporaneamente. Esempio:
- ReqX: "Il sistema deve avere l'interfaccia in linguaggio naturale."
- ReqY: "Il sistema sarà prodotto in due settimane." Per eliminare il conflitto e necessario rilassare uno dei due requisiti.

### 12. Non Ridondante
Ogni requisito deve essere espresso una sola volta e non deve sovrapporsi a un altro. Esempio:
- ReqX: "Il sistema mette a disposizione un calendario per aiutare a definire le date di intervallo dell'estratto conto richiesto."
- ReqY: "Il sistema mette a disposizione un calendario ogni volta che si deve digitare una data." ReqX e un caso particolare di ReqY e deve essere cancellato.
### 13. Completo
Un requisito deve essere specificato per tutte le condizioni che possono verificarsi. Esempio:
- ReqX: "Il sistema non visualizza la data di prelievo."
- ReqY: "Il sistema non visualizza l'anagrafica del cliente." Il numero del conto, che non è né una data né un dato anagrafico, viene visualizzato? Il requisito e incompleto perché non copre tutti i casi possibili.
### 14. Metriche Derivate
**Manutenibile**: un requisito atomico e non ridondante e più facilmente modificabile. **Tracciabile**: un requisito atomico dotato di identificatore univoco e tracciabile lungo il ciclo di vita del sistema.

## Output Format
Each Characteristic must be evaluated on a scale from 0 to 5, and a brief reason pointing out the errors must be specified. What follows is the output's specific structure. Present all the data in a tabular format; each noun between the rectangular parentheses must be in a separate column. Stick with it and do not perform additional formatting or styling outside of what is being specified below:
- [Characteristic Name], [score], [reason] At the end, add a mean score, which is the mean of all the scores.

### 3.2 Output Prompt Requisiti

Characteristic Name Score Reason Non Ambiguo 5 Grazie all'uso del glossario e alla rimozione di avverbi vaghi, ogni requisito ha ora un'unica interpretazione possibile. Provabile o Verificabile
5 La separazione dei requisiti e l'uso di termini precisi
permettono di costruire test case binari (Pass/Fail) per ogni singola funzionalità. Chiaro 5 Le User Story sono concise, laconiche e prive di verbosità , rispettando perfettamente il formato standard. Corretto 5 I requisiti rappresentano fedelmente le necessità del business e i vincoli normativi espressi nel contesto di Zootropolis. Comprensibile 5 Lo stile è consistente, grammaticalmente corretto e utilizza i termini definiti nel glossario in modo impeccabile. Fattibile 5 Tutte le funzionalità (gestione mappe, sblocco, pagamenti) sono realizzabili con le tecnologie attuali entro i vincoli di progetto. Indipendente e Auto-consistente
5 Ogni requisito è comprensibile senza dover fare riferimento
ad altri item, garantendo la massima modularità. Atomico 5 Migliorato: Ogni User Story contiene ora un solo elemento tracciabile. Abbonamenti, bonus e diverse tipologie di zone sono gestiti separatamente.

Necessario 5 La clausola "Così da" giustifica ogni funzione in base al valore reale per cittadini, operatori o amministrazione. Astratto 5 I requisiti non contengono dettagli implementativi superflui, lasciando libertà ai progettisti (es. metodo di sblocco QR/NFC). Consistente 5 Non vi sono conflitti tra i requisiti; le regole di precedenza tra zone AP e zone OP sono chiaramente stabilite. Non Ridondante 5 Ogni funzionalità è espressa una sola volta e non vi sono sovrapposizioni tra i diversi ruoli utente. Completo 5 Migliorato: La scomposizione dei requisiti ha permesso di coprire anche i flussi e le condizioni specifiche per ogni diversa entità del sistema. Metriche Derivate 5 Migliorato: L'elevata atomicità garantisce ora una manutenibilità eccellente e una tracciabilità precisa lungo tutto il ciclo di vita. Mean Score: 5.0

### 3.3 Definizioni

## 4. GLOSSARIO

### 4.1 Acronimi

- AP: Amministrazione Pubblica
- CSV: Comma-Separated Values
- NFC: Near Field Communication
- OP: Operatore del Servizio
- PDF: Portable Document Format
- QR: Quick Response (code)
- UT: Utente
- HTTP: HyperText Transfer Protocol
- ServizioGIS: Geographic Information System
- API: Application Programming Interface
- BLL: Business Logic Layer
- DAL: Data Access Layer
- DBMS: Database Management System

### 4.2 Definizioni

- Account utente: Insieme di credenziali, dati anagrafici, metodi di pagamento, e-mail, password e storico associati a un utente registrato. Il profilo personale è la vista utente dell'account.
- Addebito: Importo economico calcolato al termine di una corsa o di un evento tariffabile e prelevato dal metodo di pagamento associato all'account utente.
- Amministrazione Pubblica: Ente locale (comune o equivalente) che monitora l'andamento del servizio di sharing sul territorio e ne analizza i dati aggregati a supporto delle decisioni di pianificazione urbana. Nel sistema è un ruolo distinto da Utente e Operatore, privo di poteri di configurazione diretta della flotta o delle zone.
- Autonomia residua: Valore numerico indicante la carica rimasta nella batteria di un mezzo elettrico (e-bike, e-scooter). Espresso in

percentuale (%) o in chilometri stimati; l'unità di misura adottata è configurabile dalla piattaforma.
- Corsa: Sessione di utilizzo attivo di un mezzo sharing, che inizia con lo sblocco del veicolo e termina con la chiusura della sessione da parte dell'utente. Al termine viene calcolato e addebitato il costo. Sinonimo: Sessione.
- Fine corsa: Evento che conclude una corsa; l'esito (valido, penalizzato, rifiutato) dipende dalla posizione del mezzo rispetto a Zona Operativa e Zona di parcheggio.
- Formato Esportabile: Formattazione offerta dalla piattaforma per l’esportazione dei dati. Include CSV, PDF.
- Flotta: Insieme di tutti i mezzi gestiti da un operatore nell'ambito del servizio di sharing su un determinato territorio.
- Mappa Operatore: Visualizzazione cartografica accessibile agli operatori del servizio, che mostra negli ultimi x minuti la posizione e lo stato di tutti i mezzi della flotta, inclusi quelli nascosti alla Mappa Utente. Distinta dalla Mappa Utente per contenuto e permessi di accesso.
- Mappa Utente: Visualizzazione cartografica accessibile agli utenti, che mostra i mezzi disponibili con il relativo stato, le varie zone: vietata, limitata, parcheggio e confine operativo. Non mostra i mezzi rimossi dall'operatore.
- Metodo di pagamento: Strumento associato all'account utente (carta, wallet, ecc.) utilizzato per regolare gli addebiti.
- Mezzo: Qualsiasi veicolo messo a disposizione degli utenti nell'ambito del servizio: bicicletta tradizionale, bicicletta a pedalata assistita (e-bike), monopattino elettrico (e-scooter) e macchina elettrica.
- Mezzo disponibile: Mezzo il cui stato (definito nel glossario) è Disponibile, ossia prenotabile da un utente. Gli unici visualizzabili nella Mappa Utente.
- Operatore del Servizio: Soggetto (azienda privata o consorzio) responsabile della gestione operativa della flotta e della configurazione della piattaforma: definisce tariffe, promozioni,

zone operative, zone soggette a restrizioni e zone di parcheggio parametri di prenotazione e pausa corsa.
- Parametri di sistema: Insieme dei valori numerici configurabili che regolano il funzionamento operativo della piattaforma. Comprendono la durata massima di una prenotazione, la durata del periodo di grazia per la pausa corsa, il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente e l'importo di addebito al minuto applicato durante la pausa corsa al termine del periodo di grazia. Tali parametri sono modificabili dall'Operatore tramite l'apposita sezione di configurazione) e si applicano a tutte le operazioni successive alla modifica. L'insieme dei parametri è aperto a future estensioni: nuovi parametri numerici operativi potranno essere aggiunti senza alterare la struttura del caso d'uso, in quanto condividono la stessa logica di configurazione, validazione e salvataggio.
- Pausa corsa: Stato intermedio di una sessione in cui l'utente blocca temporaneamente il mezzo senza terminare la corsa.
- Periodo di grazia: Durata massima configurabile dall'operatore entro cui una pausa corsa non comporta addebiti aggiuntivi o la perdita del mezzo. Se impostato a zero, la funzionalità di pausa gratuita è disabilitata.
- Prenotazione: Riserva temporanea di un mezzo specifico effettuata dall'utente prima di raggiungerne fisicamente la posizione. Ha una durata massima configurabile dall'operatore; alla scadenza il mezzo viene automaticamente rilasciato e reso disponibile ad altri utenti.
- Prenotazione di gruppo: Prenotazione effettuata da un singolo utente per un numero di mezzi fino al massimo configurato dall'operatore (può anche essere uno).
- Offerta: Politica commerciale definita e pubblicata dall'Operatore allo scopo di incentivare l'utilizzo del servizio. È caratterizzata da una denominazione, una data di scadenza, uno stato (attiva, scaduta o in bozza) e da un insieme di condizioni di applicazione. Si specializza nelle seguenti tipologie:
  - Promozione: riduce la tariffa standard o introduce condizioni agevolate (ad esempio le prime N corse gratuite o uno sconto percentuale).

  - Abbonamento: contratto a tempo determinato (mensile o annuale) che garantisce all'utente condizioni tariffarie agevolate o un numero di corse incluse.
- Regole Fine Corsa: Insieme di condizioni configurate dall'operatore che determinano l'esito del Fine Corsa. Comprendono: la penale applicata in caso di parcheggio fuori zona, il tipo di vincolo (penale, divieto, avviso) e l'eventuale Bonus riconosciuto all'utente per il parcheggio corretto. La definizione delle regole è separata dalla definizione geografica della Zona di parcheggio.
- Redistribuzione: Operazione logistica di spostamento fisico dei mezzi da aree con eccesso di offerta verso aree con carenza, eseguita dal personale operativo sulla base dei dati della Mappa Operatore.
- Report aggregato: Documento che consolida statistiche anonime sull'utilizzo del servizio (corse, km, fasce orarie, zone) su un intervallo temporale configurabile. Destinato all'operatore e all'amministrazione pubblica.
- Riepilogo corsa: Sintesi presentata all'utente al termine di una corsa, che riporta i dati principali della sessione: durata complessiva, distanza percorsa, costo finale calcolato sulla base della tariffa applicata ed eventuali sconti o bonus. Disponibile anche nello storico corse del profilo utente.
- Sblocco: Operazione che disabilita il blocco fisico/elettronico del mezzo, consentendo all'utente di iniziare la corsa. Il metodo di sblocco (QR code, Bluetooth, NFC) è una scelta implementativa.
- Segnalazione: Comunicazione inviata dall'utente all'operatore per notificare anomalie su un mezzo (danno fisico, guasto, posizione anomala). Visibile nella Dashboard operatore.
- Sessione: Sinonimo di Corsa. Periodo di utilizzo attivo di un mezzo, tracciato dal sistema con marcatura temporale di inizio e fine.
- Stato (mezzo): Condizione operativa corrente di un mezzo. Valori possibili: Disponibile (prenotabile), Prenotato (riservato a un utente), In uso (corsa attiva), In pausa (pausa corsa attiva), In manutenzione (rimosso dalla Mappa Utente), Fuori servizio (bloccato o irrecuperabile).

- Storico corsa: L’insieme delle corse effettuate da un Utente.
- Tariffa: Struttura di pricing applicata a una corsa. La tipologia (es. costo al minuto, alla distanza, tariffa fissa per fascia oraria) è definita e modificabile dall'operatore. La tariffa applicabile è mostrata all'utente prima dell'avvio della corsa.
- Tariffario: Elenco pubblicato dall'operatore delle tariffe applicate per ciascuna tipologia di mezzo e modalità di utilizzo. Distinto da Tariffa (struttura applicata alla singola corsa).
- Utente: Persona fisica registrata alla piattaforma che utilizza i mezzi di sharing per spostarsi nel contesto urbano. Interagisce con il sistema tramite dispositivo mobile.
- Zona:
  - Zona Operativa: Perimetro geografico definito dall'operatore entro cui i mezzi della flotta possono circolare e fermarsi. Un mezzo che esce dalla zona operativa può attivare allarmi automatici o bloccarsi. La Zona Limitata e la Zona Vietata hanno sempre la precedenza sulla Zona Operativa.
  - Zona di parcheggio: Area geografica designata esclusivamente dall'operatore in cui è consigliato — ma non imposto — parcheggiare il mezzo al termine della corsa. Visibile sulla Mappa Utente. La definizione della zona riguarda esclusivamente il suo perimetro geografico; gli eventuali incentivi associati al parcheggio corretto sono configurati separatamente tramite le Regole Fine Corsa.
  - Zona Soggetta a restrizioni:
    - Zona Limitata: Area geografica in cui la circolazione dei mezzi è consentita ma con restrizioni configurabili (es. velocità ridotta, orari limitati, divieto di sosta o pausa). Configurata dall’Operatore.
    - Zona Vietata: Area geografica definita dall’Operatore in cui la circolazione dei mezzi è completamente vietata. Distinta dalla Zona Limitata (restrizioni parziali). Ha precedenza sulla Zona Operativa in caso di sovrapposizione.