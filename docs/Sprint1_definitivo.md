Tecnical Report SER&Practices



**Ciclo 4**

**SMART MOBILITY**

Versione 2.0

Data di rilascio: 26/05/2026

Ingegneria del Software a. A. 2025-2026  
**Informatica e Tecnologie per la Produzione del Software**

**Realizzato da**

Cardone Flavio 829469 ITPS

f.cardone21@studenti.uniba.it

De Astis Gabriele 826243 ITPS

g.deastis1@studenti.uniba.it

Giannulo Francesco 825071 ITPS

f.giannulo@studenti.uniba.it

Lacirignola Camilla 830465 ITPS

c.lacirignola5@studenti.uniba.it

Indice

1.Product Backlog 7

1.1 Introduzione 7

1.2 Contesto di business 8

1.3 Stakeholder 10

1.4 Item funzionali 11

1.4.1IF-UT.01 – Visualizza Mappa Utente 11

1.4.2IF-UT.02 – Prenota mezzo 11

1.4.3IF-UT.03 – Annulla Prenotazione 11

1.4.4 IF-UT.04 – Sblocca un mezzo 11

1.4.5IF-UT.05 – Consulta tariffe 11

1.4.6IF-UT.06 – Termina Corsa 11

1.4.7IF-UT.07 – Visualizza Riepilogo corsa 12

1.4.8IF-UT.08 – Consulta Stato Mezzo 12

1.4.9IF-UT.09– Visualizza Zone 12

1.4.10IF-UT.10 – Sospende Corsa 12

1.4.11IF-UT.11 – Prenota Gruppo 12

1.4.12IF-UT.12 – Salva Metodi Pagamento 12

1.4.13IF-UT.13 – Visualizza Promozioni 13

1.4.14IF-UT.14 – Visualizza Storico Corsa 13

1.4.15IF-UT.15 – Invia Segnalazione 13

1.4.16IF-UT.16 – Sottoscrive Abbonamento 13

1.4.17IF-UT.17 – Effettua Pagamento 13

1.4.18 IF-AP.01 – Accede Report 13

1.4.18IF-AP.02 – Esporta Report 14

1.4.19IF-AP.03 – Visualizza Mappa Amministrazione Pubblica 14

1.4.20IF-OP.01 – Visualizza Mappa Operatore 14

1.4.21IF-OP.02 – Gestisce Segnalazioni 14

1.4.22IF-OP.03 – Definisce Confine Operativo 14

1.4.23IF-OP.04 – Modifica Stato Mezzo 14

1.4.24IF-OP.05 – Sospende Account Utente 15

1.4.25IF-OP.06 – Definisce Offerte Commerciali 15

1.4.26IF-OP.07 – Definisce Tariffa 15

1.4.27IF-OP.08 – Configura Durata Prenotazione 15

1.4.28IF-OP.09 – Configura Durata Periodo Grazia 15

1.4.29IF-OP.10 – Configura Numero Massimo Mezzi 15

1.4.30IF-OP.11 – Aggiunge Mezzo 16

1.4.31IF-OP.12 – Dismette Mezzo 16

1.4.32IF-OP.13 – Definisce Regole Fine Corsa 16

1.4.33IF-OP.14 – Configura Addebito per Pausa Corsa 16

1.4.34IF-OP.15- Definisce Zone Vietate 16

1.4.35IF-OP.16 - Definisce Zone Parcheggio 16

1.4.36IF-OP.17 – Definisce Limite Velocità 17

1.5 Item non funzionali 17

1.5.1Item Informativi 17

1.5.1.1 IIN-1 Prestazioni 17

1.5.1.2 IIN-2 Sicurezza 17

1.5.1.3 IIN-3 Usabilità 17

1.5.1.4 IIN-4 Scalabilità 18

1.5.1.5 IIN-5 Portabilità 18

1.5.1.6 Conformità 18

1.5.2Item di interfaccia 18

1.5.2.1 IUI-1 - Schermata di Login Utente 18

1.5.2.2 IUI-2 – Homepage Utente 19

1.5.2.3 IUI-3 – Menu Laterale Utente 19

1.5.2.4 IUI-4 – Corsa di Gruppo 20

1.5.2.5 IUI-5 – Prenotazione Mezzo 20

1.5.2.6 IUI-6 – Visualizzazione del Piano Tariffario 20

1.5.2.7 IUI-7 – Visualizzazione del Saldo e Metodi di Pagamento 21

1.5.2.8 IUI-8 – Schermata Info Corsa 21

1.5.2.9 IUI-9 – Visualizzazione della Cronologia Corse 22

1.5.2.10 IUI-10 – Schermata Login Operatore/Amministrazione Pubblica 22

1.5.2.11 IUI-11 – Dashboard Amministrazione Pubblica 22

1.5.2.12 IUI-12 – Definizione Zone Vietate 23

1.5.2.13 IUI-13 – Definizione Zone Limitate 23

1.5.2.14 IUI-14 – Definizione Zone di Parcheggio 24

1.5.2.15 IUI-15 – Visualizzazione dei Report 24

1.5.2.16 IUI-16 – Dashboard Operatore 24

1.5.2.17 IUI-17 – Gestione Segnalazioni 25

1.5.2.18 IUI-18 – Gestione Tariffe e Promozioni 25

1.5.2.19 IUI-19 – Schermata di Impostazione Regole 25

1.5.3Item Qualitativi 26

1.5.3.1 IQ-1 26

1.5.3.2 IQ-2 26

1.5.3.3 IQ-n 26

1.5.4Altri Item 26

2.Sprint Report 28

2.1 Sprint Backlog 28

2.2 Product Requirement Specification 30

2.2.1Diagramma dei Casi d’uso 30

2.2.2Specifiche dei Casi d’uso 30

2.2.2.1 Visualizza Mappa utente 30

2.2.2.2 Visualizza Mappa Operatore 31

2.2.2.3 Definisce Zona 32

2.2.2.4 Prenota Mezzo 33

2.2.2.5 Sblocca Mezzo 34

2.2.2.6 Termina corsa 36

2.2.2.7 Effettua Pagamento 37

2.2.2.8 Salva Metodi di Pagamento 38

2.2.2.9 Definisce tariffa 40

2.2.2.10 Modifica stato mezzo 41

2.2.2.11 Aggiunge Mezzo 42

2.2.2.12 Dismette Mezzo 43

2.2.2.13 Definisce Regole Fine Corsa 45

2.2.3Altro 46

2.3 System Architecture 47

2.3.1Diagramma delle Componenti – Diagramma Generale 47

2.3.2Specifica delle componenti 47

2.4 Detailed Product Design 47

2.4.1Diagramma delle Classi – Diagramma Generale 47

2.4.2Specifiche delle Classi 47

2.4.3Diagrammi di Sequenza 47

2.5 Data modeling and design 47

2.5.1Modello logico del Database 47

2.5.2Struttura fisica del Database 47

3.Prompt 48

3.1 Qualità dei requisiti 48

3.2 Output Prompt Requisiti 56

3.3 Definizioni 57

4.Glossario 58

4.1 Acronimi 58

4.2 Definizioni 58

Product Backlog

**CICLO 4**

**SMART MOBILITY**

Product Backlog

Introduzione 

SMART MOBILITY è un sistema software progettato per supportare il Comune di Zootropolis nell'introduzione di un servizio integrato di mobilità urbana sostenibile, che mette a fattor comune diversi servizi di sharing (bike sharing, car sharing, e-scooter sharing e altri) in un'unica piattaforma accessibile a cittadini, operatori e amministrazione pubblica.

Il Sistema si pone tre obiettivi macroscopici:

* Offrire ai cittadini un accesso rapido, sicuro e trasparente ai mezzi di sharing disponibili sul territorio
* Permettere agli operatori del servizio di gestire in modo efficiente la flotta, ridurre costi e fenomeni di vandalismo
* Consentire all'Amministrazione Pubblica di monitorare la mobilità urbana e assumere decisioni strategiche basate su dati

Tali obiettivi si traducono in un insieme di funzionalità che coprono l'intero ciclo di utilizzo del servizio per soddisfare le esigenze delle tre categorie di utenti destinatari del sistema SMART MOBILITY — Utenti finali, Operatori del Servizio e Amministrazione Pubblica.

Per quanto riguarda gli Utenti, SMART MOBILITY offre:

* Visualizzazione dei mezzi disponibili nelle vicinanze e del loro stato
* Prenotazione di uno o più mezzi e sblocco tramite dispositivo personale
* Pagamenti veloci e sicuri
* Garanzia di affidabilità del sistema, con meccanismi di prevenzione di frodi ed errori
* Promozioni, pausa della corsa e gestione del profilo di pagamento

Per quanto riguarda gli Operatori del Servizio, SMART MOBILITY offre:

* Visualizzazione della distribuzione della flotta e notifiche sulle aree con bassa disponibilità, per ottimizzare la redistribuzione dei mezzi sul territorio
* Monitoraggio di malfunzionamenti, manutenzione pianificata e posizione dei mezzi a fine corsa, per ridurre i costi operativi e contenere i fenomeni di furto e vandalismo
* Bonus per parcheggio corretto, sospensione account in caso di frode e blocco automatico dei mezzi fuori dalle zone consentite

Per quanto riguarda l'Amministrazione Pubblica, SMART MOBILITY offre:

* Monitoraggio della frequenza di utilizzo delle diverse tipologie di mezzo e dei pattern di mobilità urbana, a supporto delle decisioni strategiche di pianificazione
* Accesso a report aggregati per supportare decisioni strategiche sulla mobilità
* Analisi dello stato dei mezzi e delle tratte più utilizzate per pianificare manutenzioni e interventi urbani, contribuendo alla garanzia della sicurezza urbana
* Selezione di zone sensibili con divieto o limitazione del transito

Contesto di business

Nel panorama urbano contemporaneo, caratterizzato da un’emergenza climatica sempre più pressante, dalla necessità di decongestionare i centri storici e dalla transizione verso modelli di "Smart City", emerge con forza l'esigenza di soluzioni integrate per la mobilità dolce e condivisa. 

**SMART Mobility** nasce per rispondere a questa sfida, superando la frammentazione degli attuali servizi di sharing e offrendo una piattaforma unica che connette cittadini, operatori privati e pubblica amministrazione.

Il software è pensato per essere usato nei seguenti ambiti:

* **Contesto di mobilità per i cittadini:** in un ambiente urbano dove possedere un mezzo privato è sempre più costoso e inefficiente, i cittadini necessitano di strumenti che permettano di pianificare spostamenti intermodali in tempo reale. SMART Mobility offre un ecosistema che permette all'utente di localizzare, prenotare e pagare diversi tipi di mezzi (bici, monopattini, auto elettriche) tramite un'unica interfaccia, garantendo trasparenza sulle tariffe e sulla disponibilità, oltre a incentivare comportamenti virtuosi tramite bonus per il parcheggio corretto.
* **Contesto operativo degli operatori di flotta:** la gestione di una flotta di mezzi condivisi comporta sfide logistiche enormi, dal recupero dei mezzi scarichi alla manutenzione per atti vandalici. Gli operatori necessitano di strumenti avanzati per il monitoraggio costante della flotta, la gestione delle zone operative e l'ottimizzazione dei flussi di ridistribuzione. SMART Mobility permette ai gestori di massimizzare il tempo di attività dei mezzi, ridurre i costi di recupero e analizzare le zone a maggior rendimento.
* **Contesto di governance dell'Amministrazione Pubblica:** i comuni si trovano spesso a subire l'invasione di mezzi di sharing senza avere gli strumenti per regolarli efficacemente. SMART Mobility offre alle amministrazioni una "dashboard di controllo" per definire in tempo reale zone vietate, zone a velocità limitata e aree di parcheggio obbligatorie. Il sistema consente di raccogliere dati granulari sui flussi di traffico, permettendo di pianificare infrastrutture ciclabili e pedonali basandosi su evidenze reali anziché su stime.
* **Contesto di sostenibilità e monitoraggio ambientale:** in un'epoca di obiettivi stringenti per la riduzione della CO2, cresce il bisogno di monitorare l'impatto ambientale dei trasporti. SMART Mobility risponde a questa esigenza fornendo statistiche aggregate sui chilometri percorsi con mezzi elettrici e sul risparmio di emissioni, permettendo sia all'utente che al Comune di visualizzare il proprio contributo concreto alla transizione ecologica.

In questo scenario, **SMART Mobility** si propone come piattaforma integrata che supera i limiti dei singoli servizi proprietari, offrendo un'esperienza fluida e centralizzata che risponde alle esigenze di tutti gli attori della mobilità urbana.

Stakeholder

Il sistema SMART Mobility coinvolge diversi stakeholder che interagiscono con la piattaforma con ruoli e obiettivi specifici. Di seguito sono descritti i principali attori del sistema:

**1. Utente:**

È l'utente che usufruisce dei mezzi di mobilità condivisa. Deve essere registrato per utilizzare la mappa, per localizzare i mezzi, per noleggiare e pagare. Le tipologie di Utente sono:

* **Pendolare Urbano:** Persona che utilizza regolarmente il servizio per coprire l'ultimo miglio (es. da stazione a ufficio) e cerca affidabilità e abbonamenti convenienti.
* **Utente Occasionale:** Residente che utilizza il servizio saltuariamente per necessità impreviste o svago.
* **Turista:** Visitatore che necessita di un accesso rapido e senza frizioni (es. login social o pagamenti rapidi) per esplorare la città in modo sostenibile.

**2. Operatore del Servizio:**

Rappresenta l'azienda che immette i mezzi sulla strada. Gestisce il business e la manutenzione. Le tipologie di figure interne all'Operatore sono:

* **Manager del Servizio:** Definisce i piani tariffari, le promozioni e le zone operative per massimizzare il profitto.
* **Team Logistico e Manutentori:** Personale sul campo che si occupa della ricarica delle batterie, della riparazione dei guasti e dello spostamento fisico dei mezzi nelle zone ad alta richiesta.

**3. Amministrazione Pubblica:**

Ente che detiene la sovranità sul suolo pubblico e definisce le regole del gioco. Le figure coinvolte sono:

* **Pianificatore Urbano/Mobility Manager:** Utilizza i dati della piattaforma per studiare nuovi percorsi ciclabili e gestire le restrizioni al traffico.
* **Polizia Locale/Corpo di Vigilanza:** Monitora il rispetto delle zone vietate e la corretta gestione dei parcheggi per garantire il decoro urbano.

Item funzionali

Contiene l’elenco e la specifica di tutti i requisiti funzionali espressi attraverso lo schema delle user stories:

IF-UT.01 – Visualizza Mappa Utente

*Come* utente, 

*Voglio* visualizzare la Mappa Utente, 

*Così da* poter scegliere un mezzo.

IF-UT.02 – Prenota mezzo

*Come* utente,

*Voglio* prenotare un mezzo disponibile,

*Così da* trovarlo riservato al mio arrivo.

IF-UT.03 – Annulla Prenotazione 

*Come* utente,

*Voglio* annullare una prenotazione attiva prima di raggiungere il mezzo,

*Così* *da* liberare il mezzo se cambio programma.

* 1.4.4 IF-UT.04 – Sblocca un mezzo

*Come* utente, 

*Voglio* sbloccare un mezzo, 

*Così da* avviare fisicamente la corsa.

- IF-UT.05 – Consulta tariffe

*Come* utente, 

*Voglio* consultare il tariffario per ciascuna tipologia di mezzo,

*Così da* confrontarne i costi

- IF-UT.06 – Termina Corsa

*Come* utente,

*Voglio* terminare la corsa

*Così da* liberare il mezzo.

- IF-UT.07 – Visualizza Riepilogo corsa

*Come* utente,

*Voglio* ricevere il riepilogo corsa,

*Così* da visualizzare le informazioni sulla corsa effettuata

- IF-UT.08 – Consulta Stato Mezzo

*Come* utente,

*Voglio* consultare lo stato di un mezzo,

*Così da* effettuare una scelta in base alle mie esigenze di percorso.

- IF-UT.09– Visualizza Zone

*Come* utente,

*Voglio* visualizzare le zone soggette a restrizioni sulla mappa,

*Così da* pianificare il mio percorso nel rispetto delle normative vigenti. 

- IF-UT.10 – Sospende Corsa

*Come* utente,

*Voglio* mettere in pausa la corsa,

*Così da* effettuare soste senza perdere il possesso del mezzo.

- IF-UT.11 – Prenota Gruppo

*Come* utente,

*Voglio* effettuare una prenotazione di gruppo fino al numero massimo di mezzi,

*Così* *da* gestire in un'unica operazione la mobilità condivisa con accompagnatori.

- IF-UT.12 – Salva Metodi Pagamento

*Come* utente,

*Voglio* salvare uno o più metodi di pagamento,

*Così* *da* ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati.

- IF-UT.13 – Visualizza Promozioni

*Come* utente,

*Voglio* accedere alle promozioni attive,

*Così* da ridurre i costi di utilizzo del servizio.

- IF-UT.14 – Visualizza Storico Corsa

*Come* utente,

*Voglio* visualizzare lo storico delle corse,

*Così* *da* tenere traccia di tutte le corse effettuate.

- IF-UT.15 – Invia Segnalazione

*Come* utente,

*Voglio* inviare una segnalazione,

*Così* da informare l'operatore affinché possa intervenire.

- IF-UT.16 – Sottoscrive Abbonamento

*Come* utente,

*Voglio* sottoscrivere un abbonamento,

*Così* *da* usufruire di condizioni tariffarie agevolate.

- IF-UT.17 – Effettua Pagamento

Come utente, 

*Voglio* che il sistema addebiti automaticamente l'importo sul mio metodo di pagamento predefinito al termine della corsa, 

*Così* da non dover effettuare transazioni manuali ogni volta che scendo dal mezzo.

* 1.4.18 IF-AP.01 – Accede Report

*Come* amministrazione pubblica,

*Voglio* accedere a report aggregati sull'utilizzo del servizio,

*Così* *da* supportare decisioni strategiche di pianificazione.

IF-AP.02 – Esporta Report

*Come* amministrazione pubblica,

*Voglio* esportare i report aggregati sull'utilizzo del servizio in Formato Esportabile,

*Così* da utilizzarli in analisi esterne e documentazione ufficiale.

IF-AP.03 – Visualizza Mappa Amministrazione Pubblica

*Come* amministrazione pubblica,

*Voglio* visualizza la mappa,

*Così* *da* monitorare il servizio sulla citta.

IF-OP.01 – Visualizza Mappa Operatore

*Come* operatore,

*Voglio* visualizzare la Mappa Operatore,

*Così* *da* pianificare operazioni di redistribuzione.

IF-OP.02 – Gestisce Segnalazioni

*Come* operatore,

*Voglio* leggere le segnalazioni inviate dagli utenti,

*Così* *da* pianificare gli interventi di manutenzione.

IF-OP.03 – Definisce Confine Operativo

*Come* operatore,

*Voglio* definire il confine operativo,

*Così* *da* circoscrivere la zona percorribile dai mezzi.

IF-OP.04 – Modifica Stato Mezzo

*Come* operatore,

*Voglio* modificare lo Stato di un mezzo,

*Così* *da* nasconderlo o mostrarlo sulla Mappa Utente.

IF-OP.05 – Sospende Account Utente

*Come* operatore,

*Voglio* sospendere l'account di un utente,

*Così* *da* tutelare l'integrità del servizio

IF-OP.06 – Definisce Offerte Commerciali

*Come* operatore,

*Voglio* definire promozioni con condizioni e scadenza configurabili,

*Così* *da* incentivare l'utilizzo del sistema con politiche commerciali flessibili.

IF-OP.07 – Definisce Tariffa

*Come* operatore,

*Voglio* definire la tariffa del servizio,

*Così* *da* permettere la configurazione del modello di costo.

IF-OP.08 – Configura Durata Prenotazione

*Come* operatore,

*Voglio* configurare la durata massima di una prenotazione,

*Così* da liberare i mezzi non utilizzati.

IF-OP.09 – Configura Durata Periodo Grazia

*Come* operatore,

*Voglio* configurare la durata del periodo di grazia per la pausa corsa,

*Così* *da* offrire agli utenti un tempo gratuito.

IF-OP.10 – Configura Numero Massimo Mezzi

*Come* operatore,

*Voglio* configurare il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente,

*Così* *da* abilitare le prenotazioni di gruppo.

IF-OP.11 – Aggiunge Mezzo

*Come* operatore,

*Voglio* aggiungere un nuovo mezzo alla mappa,

*Così* *da* aumentare il numero di mezzi della flotta.

IF-OP.12 – Dismette Mezzo

*Come* operatore,

*Voglio* dismettere un mezzo dalla mappa,

*Così* *da* gestire il ciclo di vita della flotta.

IF-OP.13 – Definisce Regole Fine Corsa

*Come* Operatore 

*Voglio* Definire regole sanzionatorie per i rilasci dei mezzi al di fuori delle aree di parcheggio consentite 

**Così da** garantire il decoro urbano

IF-OP.14 – Configura Addebito per Pausa Corsa

*Come* operatore,

*Voglio* configurare la politica di addebito durante la pausa corsa al termine del periodo di grazia,

*Così* *da* rendere trasparente e flessibile il pricing della pausa.

IF-OP.15- Definisce Zone Vietate 

*Come* operatore,

*Voglio* definire i confini di una Zona Vietata,

*Così* *da* garantire il rispetto delle normative locali.

IF-OP.16 - Definisce Zone Parcheggio

*Come* operatore,

*Voglio* definire zone di parcheggio visibili sulla Mappa Utente,

*Così* *da* ridurre il disordine dei mezzi sulla strada.

IF-OP.17 – Definisce Limite Velocità

*Come* operatore,

*Voglio* definire il limite di velocità applicabile in ciascuna Zona Limitata,

*Così* *da* garantire il rispetto delle normative locali.

Item non funzionali

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali.

Item Informativi

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali di tipo informativo. 

IIN-1 Prestazioni 

* Il sistema deve aggiornare la posizione dei mezzi sulla Mappa Utente entro x secondi dall'ultimo rilevamento GPS (da testare)
* Il sistema deve completare l'operazione di prenotazione di un mezzo entro x secondi dalla richiesta dell'utente (da testare)

IIN-2 Sicurezza

* Tutte le comunicazioni tra client e server devono essere cifrate mediante protocolli di sicurezza standard
* Il sistema deve bloccare un account dopo 5 tentativi di autenticazione falliti consecutivi in un tempo configurabile dall’operatore
* I dati personali degli utenti devono essere trattati in conformità al Regolamento UE 2016/679 (GDPR)
* Ciascun ruolo (UT, OP, AP) deve poter accedere esclusivamente alle funzionalità ad esso assegnate

IIN-3 Usabilità 

* L'interfaccia deve essere accessibile secondo le linee guida WCAG (es. per utenti con disabilità visive)
* L’interfaccia deve essere facile da usare e comprensibile in meno di x minuti

IIN-4 Scalabilità 

* L'architettura deve permettere l'aggiunta di nuove tipologie di mezzo senza modifiche strutturali

IIN-5 Portabilità 

* Il sistema deve essere accessibile tramite browser web su dispositivi desktop e mobile, senza necessità di installazione

Conformità

* I report esportabili in CSV/PDF (AP.06) devono rispettare eventuali standard di formato richiesti dalla pubblica amministrazione

Item di interfaccia

Contiene i requisiti di interfaccia espressi tramite mockup.

IUI-1 - Schermata di Login Utente

Il mockup illustra l'interfaccia di autenticazione iniziale, caratterizzata da un design *clean* su sfondo bianco. La parte superiore ospita il logo del sistema, sottolineando la vocazione ecosostenibile del brand. Al centro si trova il form di accesso, con campi di input arrotondati per *Username* e *Password*, completato dal link per il recupero credenziali. Le *Call to Action* sono gestite da due grandi pulsanti in verde acqua con ombreggiature ("LOGIN" e "SIGN UP"), seguiti in basso dai collegamenti per il *social login* rapido (Google e Apple). 

IUI-2 – Homepage Utente

Questo mockup mostra l'interfaccia cartografica principale dell'app. La top bar offre l'accesso al profilo utente e al menu laterale tramite icona ad hamburger. Al centro, la mappa interattiva geolocalizza in tempo reale la flotta disponibile utilizzando pin codificati per colore e icona (monopattini in verde, bici in blu, auto in magenta). Sulla mappa è visibile un'area evidenziata in rosso (una geo-fence per zone a sosta vietata o velocità limitata) e un marker di posizione. Nella parte inferiore, due pulsanti floating permettono di avviare una "CORSA DI GRUPPO" o lo "SBLOCCA MEZZO". Chiude la schermata una bottom navigation bar per lo spostamento rapido tra le sezioni principali.

IUI-3 – Menu Laterale Utente

Il mockup illustra il *side drawer* (menu laterale a scomparsa) aperto, che scorre da destra sovrapponendosi alla mappa di sfondo, la quale risulta oscurata per mantenere il focus dell'utente. L'intestazione presenta il logotipo del brand affiancato da una chiara icona "X" per la chiusura del pannello. L'architettura dell'elenco voci allinea testo e icone vettoriali (declinate nel verde acqua aziendale) sul lato destro, favorendo una lettura rapida. Le opzioni di navigazione garantiscono l'accesso immediato alle sezioni gestionali e amministrative dell'utente, coprendo l'area personale (*Profilo*, *Impostazioni*, *Guida*) e la sfera economica/operativa (*Piano Tariffario*, *Bonus e Promozioni*, *Cronologia*, *Portafoglio*). Il layout adotta uno spazio bianco generoso per un design pulito e leggibile.

IUI-4 – Corsa di Gruppo

Il mockup presenta l'interfaccia di gestione per le corse multiple, implementata tramite un pannello a comparsa inferiore (*bottom sheet*) sovrapposto parzialmente alla mappa. L'intestazione, dotata di icona di chiusura rapida, introduce la funzione "Inizia corsa di gruppo" seguita da un contatore dinamico di stato ("Veicoli sbloccati: 3/5"). Il corpo centrale elenca i veicoli già agganciati alla sessione tramite singole *cards* arrotondate; ciascuna scheda fornisce dati in tempo reale mostrando l'icona del mezzo, il codice identificativo alfanumerico e l'indicatore visivo della batteria (con colorazione semantica verde/giallo). Nella parte inferiore è posizionata la *Call to Action* ("SBLOCCA VEICOLO"), un pulsante primario per aggiungere ulteriori mezzi prima dell'avvio definitivo della corsa.

IUI-5 – Prenotazione Mezzo

Il mockup illustra l'interfaccia per la prenotazione di un singolo veicolo, realizzata tramite un *bottom sheet* che si sovrappone alla mappa. Sulla cartina, il mezzo selezionato è enfatizzato da un *pin* verde ingrandito. Il pannello, intitolato "Prenota mezzo" con relativa icona di chiusura, riepiloga i dati cruciali: tipologia (Monopattino), codice identificativo e stato visivo della batteria. Un testo informativo avvisa chiaramente l'utente del limite temporale esatto entro cui raggiungere e sbloccare il mezzo. Il flusso si conclude con la *Call to Action* "Prenota", un pulsante primario ben delineato che attiva il blocco temporaneo del veicolo, garantendo all'utente un'interazione fluida e priva di ambiguità.

IUI-6 – Visualizzazione del Piano Tariffario

Questo mockup rappresenta la sezione informativa sui costi del servizio, strutturata con un layout minimale e ampio spazio bianco per massimizzare la leggibilità. L'header presenta il titolo della sezione affiancato da un'icona di chiusura rapida. Al centro, tre *card* dal design a pillola con morbida ombreggiatura illustrano le tariffe chilometriche per ogni categoria di veicolo (Monopattino a 0,20€/km, Bicicletta a 0,30€/km, Automobile a 0,50€/km), accostando icone stilizzate ai relativi costi per un'immediata comprensione visiva. Completa l'interfaccia il logo aziendale centrato nella parte inferiore e la *bottom navigation bar* fissa, che garantisce continuità nell'esplorazione dell'app.

IUI-7 – Visualizzazione del Saldo e Metodi di Pagamento 

Il mockup illustra l'interfaccia di gestione finanziaria ("Portafoglio"). La gerarchia visiva pone in primo piano una *card* delimitata in verde acqua che evidenzia a grandi caratteri il "Saldo" disponibile. La sezione sottostante dedicata ai "Metodi di Pagamento" è organizzata in un menu a lista provvisto di *chevron* direzionali per suggerire l'interazione. Questo blocco integra opzioni di *digital wallet* (Google Pay, Apple Pay, PayPal) e una voce per l'aggiunta di carte di credito, tutte corredate da loghi o icone di riconoscimento rapido. L'operatività è demandata alla *Call to Action* primaria "RICARICA SALDO", un pulsante *pill-shaped* ad alto contrasto per il *top-up* del conto. Lo stile mantiene il layout pulito dell'applicativo, chiudendosi con la *bottom navigation bar* di sistema.

IUI-8 – Schermata Info Corsa

Il mockup illustra il cruscotto di monitoraggio attivo durante il noleggio. L'interfaccia si apre con un'icona circolare in evidenza che identifica la tipologia di veicolo in uso (monopattino). La parte centrale espone la telemetria della sessione in tempo reale tramite un layout tabellare chiaro: riporta l'ID alfanumerico del mezzo, l'indicatore grafico della batteria, il timer del tempo trascorso e i chilometri percorsi. Nella sezione inferiore, sotto il logo aziendale, sono collocate due *Call to Action* operative tramite ampi pulsanti *pill-shaped*. Il sistema offre all'utente il pieno controllo dell'iter di viaggio, consentendo di sospendere temporaneamente la sessione ("PAUSA CORSA") o di concluderla procedendo alla fatturazione ("TERMINA E PAGA").

IUI-9 – Visualizzazione della Cronologia Corse

Il mockup illustra la sezione "Cronologia Corse", progettata per fornire all'utente lo storico dettagliato dei propri noleggi. L'interfaccia adotta un layout a lista lineare, utilizzando divisori orizzontali continui per segmentare visivamente le singole sessioni. Ogni voce (*list item*) espone sulla sinistra un'icona vettoriale identificativa del veicolo (monopattino, bicicletta o automobile), garantendo un riconoscimento visivo immediato. Sulla destra, i dati riepilogativi della corsa sono ordinatamente incolonnati: ID del mezzo, durata ("Tempo trascorso"), distanza ("Km percorsi") e data. Questa architettura dell'informazione modulare e minimalista assicura una facile leggibilità e un'ottima scansionabilità. Chiudono la schermata l'header con comando di chiusura rapida e la *bottom navigation bar* di sistema.

IUI-10 – Schermata Login Operatore/Amministrazione Pubblica

Questo mockup illustra l'adattamento landscape (orizzontale) dell'interfaccia di autenticazione, utilizzato da operatore e amministrazione pubblica. Il layout mantiene intatta la coerenza visiva, cromatica e funzionale della controparte mobile, raggruppando gli elementi in un blocco centrale ben allineato. Troviamo in sequenza: il logo, il form di input per Username e Password, i pulsanti primari di LOGIN e SIGN UP, e le opzioni per il social login rapido in basso. L'utilizzo abbondante di spazio bianco (white space) ai lati focalizza l'attenzione dell'utente sull'azione di accesso, garantendo un'esperienza utente pulita e senza distrazioni anche su schermi ampi.

IUI-11 – Dashboard Amministrazione Pubblica

Il mockup illustra la *dashboard* web dedicata all’amministrazione pubblica. Il layout *landscape* è strutturato in due macroaree funzionali: a sinistra, un ampio visualizzatore cartografico interattivo (basato su Google Maps) per il monitoraggio del territorio operativo; a destra, un pannello di controllo lineare che riporta il *branding* aziendale. Le operazioni sono demandate a quattro pulsanti *pill-shaped* ad alto contrasto che consentono la gestione visiva del *geofencing* ("DEFINISCI ZONE VIETATE", "DEFINISCI ZONE LIMITATE", "DEFINISCI ZONE PARCHEGGIO") e l'accesso alle statistiche ("VISUALIZZA REPORT"). L'affiancamento diretto tra la mappa di lavoro e i comandi operativi garantisce all'amministratore un'esperienza utente efficiente e priva di attriti durante il *setup* del servizio cittadino. 

IUI-12 – Definizione Zone Vietate

L'interfaccia illustra il flusso di *geofencing* lato amministratore per la gestione delle aree vietate. Sulla sinistra, la mappa funge da *canvas* interattivo: l'utente posiziona nodi per tracciare un poligono rosso, circoscrivendo visivamente la zona urbana soggetta a restrizione. A destra, un pannello contestuale fornisce istruzioni testuali chiare e coordinate cromaticamente. La parametrizzazione della regola avviene in basso tramite pulsanti *toggle*: l'operatore seleziona a quali veicoli applicare il divieto (es. l'opzione "Automobile" è attiva e confermata da una spunta visibile). Il layout, completato da un'icona di annullamento rapido in alto a destra, sfrutta il paradigma della manipolazione diretta per ottimizzare il *setup* del sistema e ridurre il carico cognitivo.

IUI-13 – Definizione Zone Limitate

Il mockup mostra la funzionalità amministrativa per la creazione di zone a traffico o velocità limitata. Sfruttando lo stesso paradigma di interazione del tracciamento zone vietate, la mappa permette di disegnare un poligono interattivo tramite nodi. In questo caso, il sistema utilizza semanticamente il colore **arancione** sia per l'area tracciata che per le parole chiave nel testo esplicativo, indicando una restrizione parziale. Il pannello laterale destro consente all'amministratore di selezionare tramite interruttori *toggle* a quale categoria di mezzo applicare la limitazione (nell'esempio, è spuntata "Automobile"). La coerenza visiva e procedurale con le altre schermate di *geofencing* garantisce un'elevata *learnability* del sistema.

IUI-14 – Definizione Zone di Parcheggio

L'interfaccia illustra la funzione amministrativa dedicata alla mappatura delle aree di sosta. Adottando il medesimo *pattern* d'interazione, la mappa a sinistra consente di tracciare un poligono interattivo, qui declinato semanticamente nel colore **verde** per indicare un'area consentita. A destra, il pannello laterale permette di associare il parcheggio a specifiche categorie di veicoli tramite i consueti controlli *toggle* (nell'esempio, "Automobile").

IUI-15 – Visualizzazione dei Report

L'interfaccia di reportistica offre all'amministratore una dashboard analitica sull'utilizzo della flotta. La vista si articola in due grafici principali: a sinistra, un istogramma a barre impilate analizza il volume dei noleggi su base settimanale; a destra, un grafico a torta illustra la quota di mercato (in percentuale) per tipologia di mezzo. L'operatività è garantita da due pulsanti in basso che abilitano l'esportazione dei dati in formato CSV e PDF.

IUI-16 – Dashboard Operatore

Il mockup illustra la dashboard web dell'operatore con layout split-screen landscape. A sinistra la Mappa Operatore (Google Maps) geolocalizza la flotta tramite pin cromatici per tipologia: monopattini in verde, biciclette in blu, automobili in magenta. In basso sulla mappa due pulsanti floating gestiscono "AGGIUNGI MEZZO" e "DISMETTI MEZZO". Il pannello destro espone sei pulsanti pill-shaped con icone esplicative: "GESTISCI SEGNALAZIONI", "GESTISCI UTENTI", "IMPOSTAZIONI REGOLE", "TARIFFE E PROMOZIONI", "VISUALIZZA REPORT" e "GESTISCI MEZZI". In alto a destra è presente l'icona di accesso al profilo; in basso il logo SMART MOBILITY.

IUI-17 – Gestione Segnalazioni

L'interfaccia illustra la schermata dedicata al customer care lato amministratore, strutturata tramite un rigoroso layout tabellare (data grid). Le colonne categorizzano i ticket in entrata esponendo in modo ordinato: identificativo utente, timestamp (data e ora), tipologia di problematica (espressa visivamente tramite icone semantiche per veicoli specifici o alert di sistema) e il dettaglio testuale del disservizio. L'operatività diretta è delegata al pulsante Call to Action "RISPONDI" posto in coda a ciascuna riga, che innesca il flusso di presa in carico del problema.

IUI-18 – Gestione Tariffe e Promozioni

Il mockup illustra il pannello di configurazione economica del servizio, con layout a due card affiancate e chiusura rapida tramite "X". La card sinistra mostra per ciascuna tipologia di mezzo (Monopattino, Bicicletta, Automobile) un valore numerico editabile e un selettore di unità di misura — evidenziato da un bordo squadrato — che consente all'operatore di scegliere la metrica tariffaria applicata (nell'esempio: €/km). La card destra mostra la promozione attiva tramite un blocco pill-shaped verde acqua e la Call to Action "AGGIUNGI PROMOZIONE".

IUI-19 – Schermata di Impostazione Regole

Il mockup illustra il pannello amministrativo per la configurazione delle *business rules* di sistema. L'interfaccia adotta una singola e ampia *card* strutturata a lista, dove i parametri operativi sono linearmente modificabili tramite campi di input numerici (es. durata massima della prenotazione, tolleranza della pausa, limiti di prenotazione simultanea per utente e percentuali tariffarie). L'ultima riga mostra un menu a tendina (*dropdown*), qui raffigurato nel suo stato espanso, progettato per selezionare la politica sanzionatoria in caso di sosta fuori zona (penale, divieto o semplice avviso).

Item Qualitativi

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali di tipo qualitativo. 

IQ-1

IQ-2

IQ-n

Altri Item

Sprint Report N. 1

**Ciclo 4**

**Smart Mobility**

Sprint Report

Sprint Backlog

Tabella di riepilogo che indica, per ognuno degli Sprint successivi allo Sprint n.0, la lista degli item del Product Backlog, evidenziando quelli che verranno implementati nell’ambito dello sprint corrente unitamente ad una descrizione esplicativa. 

Per semplificare l’esposizione e salvaguardare la tracciabilità tra semilavorati si è proceduto alle seguenti assunzioni:

* All’interno di uno Sprint sono implementati un sottoinsieme di item tra quelli specificati nel Product Backlog
* Lo Sprint Backlog relativo allo sprint corrente contiene pertanto l’insieme degli item del Product Backlog in corso di implementazione
* Gli Item funzionali, ovvero le User Stories dovranno essere tracciabili uno a uno, auspicabilmente seppur non necessariamente, con i casi d’uso
* Ad ogni caso d’uso dovrà essere associato uno scenario di base più gli eventuali scenari alternativi. Lo scenario in prima istanza viene redatto a partire dalla specifica della User Story riportata nel Product Backlog
* Ad ogni caso d’uso dovrà essere associato un diagramma di sequenza.

Ogni sprint deve necessariamente produrre in output del codice funzionante. L’unica eccezione è rappresentata dallo Sprint n°0 che deve essere utilizzato per disegnare la macroarchitettura del sistema con le sue componenti e le sue interfacce, e che sarà utilizzata come roadmap per gli sprint successivi andando a chiarire dove si colloca quanto realizzato in ciascuno di essi.

|  |  |  |
| --- | --- | --- |
| **Codice Item** | **Numero Sprint** | **Note** |
| UT.01 | Sprint 1 | Visualizza Mappa utente |
| UT.02 | Sprint 1 | Prenota mezzo |
| UT.04 | Sprint 1 | Sblocca un mezzo |
| UT.06 | Sprint 1 | Termina Corsa |
| UT.12 | Sprint 1 | Salva metodi di pagamento |
| UT.17 | Sprint 1 | Effettua Pagamento |
| AP.01 | Sprint 1 | Accede report |
| OP.01 | Sprint 1 | Visualizza Mappa Operatore |
| OP.03 | Sprint 1 | Definisce confine operativo |
| OP.04 | Sprint 1 | Modifica stato mezzo |
| OP.07 | Sprint 1 | Definisce tariffe |
| OP.11 | Sprint 1 | Aggiunge un mezzo |
| OP.12 | Sprint 1 | Dismette un mezzo |
| OP.13 | Sprint 1 | Definisce regole fine corsa |
| OP.15 | Sprint 1 | Definisce Zone Vietate |
| OP.16 | Sprint 1 | Definisce Zone Parcheggio |

Product Requirement Specification 

Diagramma dei Casi d’uso

Specifiche dei Casi d’uso

Visualizza Mappa utente

|  |  |
| --- | --- |
| **Nome** | **Visualizza Mappa Utente** |
| **ID** | CS-01 (UT.01) |
| **Breve descrizione** | Il sistema mostra all'Utente autenticato la mappa interattiva con i mezzi disponibili nelle vicinanze, le zone con restrizioni e le zone di parcheggio, così da poter scegliere un mezzo da prenotare o sbloccare. |
| **Attori Primari** | Utente |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L’utente è autenticato alla piattaforma |
| **Sequenza principale degli eventi** | * Il caso d'uso inizia quando l'Utente accede alla schermata principale della piattaforma. * Il sistema rileva la posizione geografica corrente dell'Utente tramite il dispositivo. * Il sistema interroga il ServizioGIS per recuperare i dati geografici. * Il sistema recupera le zone con restrizioni e le zone di parcheggio. * Il sistema visualizza la mappa con i soli mezzi disponibili per tipologia, le aree con restrizioni, le zone di parcheggio e il marker della posizione corrente. |
| **Post-condizioni** | La mappa è visualizzata con i dati aggiornati; l'Utente può procedere con la prenotazione o lo sblocco di un mezzo. |
| **Sequenza alternativa degli eventi** | Nessuna |

Visualizza Mappa Operatore

|  |  |
| --- | --- |
| **Nome** | **Visualizza Mappa Operatore** |
| **ID** | CS-02 (OP.01) |
| **Breve descrizione** | Il sistema mostra all'Operatore autenticato la mappa interattiva con l'intera flotta, incluso lo stato di ciascun mezzo (disponibile, in uso, in manutenzione, ecc.), così da poter pianificare operazioni di redistribuzione o manutenzione. |
| **Attori Primari** | Operatore |
| **Attori Secondari** | ServizioGIS |
| **Precondizioni** | L’operatore è autenticato alla piattaforma |
| **Sequenza principale degli eventi** | * Il caso d'uso inizia quando l'Operatore accede alla schermata principale della piattaforma. * Il sistema interroga il ServizioGIS per recuperare i dati geografici. * Il sistema recupera le zone con restrizioni, le zone di parcheggio e lo stato aggiornato di tutti i mezzi della flotta. * Il sistema visualizza la mappa con tutti i mezzi, lo stato di ciascuno, le aree con restrizioni e il marker della posizione corrente. |
| **Post-condizioni** | La mappa è visualizzata con i dati aggiornati sull'intera flotta; l'Operatore può procedere con la pianificazione di operazioni di redistribuzione o manutenzione. |
| **Sequenza alternativa degli eventi** | Nessuna |

Definisce Zona

|  |  |
| --- | --- |
| **Nome** | **DefinisceZona** |
| ID | CS-03 (OP.03, OP.15, OP.16) |
| Breve descrizione | L’operatore definisce i confini geografici di una Zona caratteristica (Vietata, Limitata, di Parcheggio, Confine Operativo); il sistema memorizza la zona e la applica attivamente. |
| Attori primari | Operatore |
| Attori secondari | Nessuno |
| Precondizioni | L’operatore è autenticato con il ruolo appropriato nel sistema |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l’operatore intende definire una zona caratteristica all’interno del sistema.  2. Il sistema visualizza la mappa interattiva dell'area di competenza con le zone esistenti.  3. L’operatore disegna il perimetro della zona sulla mappa definendo i vertici del poligono.  4. L’operatore conferma la creazione della zona.  5. Fintantoché il perimetro non è valido:      5.1 Il sistema notifica l’operatore del problema rilevato.      5.2 l’operatore corregge il perimetro (torna al passo 3).  6. Il sistema salva la Zona e la rende attiva.  7. Il sistema aggiorna la mappa visibile agli Utenti evidenziando la nuova zona. |
| Postcondizioni | La nuova Zona creata è persistita nel sistema con il perimetro definito; il sistema la applica alla flotta. |
| Sequenze alternative | Nessuna |



Prenota Mezzo

|  |  |
| --- | --- |
| **Nome** | **Prenota Mezzo** |
| ID | CS-04 (UT.02) |
| Breve descrizione | L'Utente prenota un mezzo disponibile nelle vicinanze; il sistema riserva il mezzo per un intervallo di tempo definito, impedendo ad altri utenti di prenotarlo. |
| Attori primari | Utente |
| Attori secondari | Nessuno |
| Precondizioni | L'Utente è autenticato nel sistema; l'Utente non ha prenotazioni attive in corso; esiste almeno un mezzo disponibile nelle vicinanze. |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l'Utente ha intenzione di prenotare un mezzo disponibile nella mappa.  2. Il sistema verifica che il mezzo sia ancora disponibile.  3. Il sistema crea una prenotazione associando il mezzo all'Utente.  4. Il sistema aggiorna lo stato del mezzo da "Disponibile" a "Prenotato".  5. Il sistema avvia il timer di prenotazione.  6. Il sistema notifica l'Utente con la conferma della prenotazione e il tempo rimanente. |
| Postcondizioni | Il mezzo selezionato risulta nello stato "Prenotato" ed è associato all'Utente; il timer di prenotazione è avviato. |
| Sequenze alternative | MezzoNonDisponibile |

|  |  |
| --- | --- |
| **Nome** | **PrenotaMezzo:MezzoNonDisponibile** |
| ID | CS-04.01 |
| Breve descrizione | Il mezzo selezionato è stato occupato da un altro utente nell'intervallo tra la visualizzazione e la conferma della prenotazione. |
| Attori primari | Utente |
| Attori secondari | nessuno |
| Precondizioni | Il mezzo è passato allo stato "Prenotato" o "In Uso" prima del completamento della richiesta dell'Utente. |
| Postcondizioni | Lo stato del sistema rimane invariato; l'Utente non ha prenotazioni attive. |
| Sequenza alternativa degli eventi | 1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.  2. Il sistema informa l'Utente che il mezzo selezionato non è più disponibile.  3. Il sistema mostra la lista aggiornata dei mezzi disponibili nelle vicinanze. |



Sblocca Mezzo

|  |  |
| --- | --- |
| **Nome** | **Sblocca Mezzo** |
| ID | CS-05 (UT.04) |
| Breve descrizione | L'Utente avvia la procedura di sblocco fisico del mezzo prenotato o disponibile; il sistema verifica le condizioni e abilita l'utilizzo del mezzo. |
| Attori primari | Utente |
| Attori secondari | Nessuno |
| Precondizioni | L'Utente è autenticato; l'Utente si trova in prossimità del mezzo; il mezzo è nello stato "Prenotato" dall'Utente corrente oppure nello stato "Disponibile". |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l'Utente vuole sbloccare un mezzo nell'applicazione.  2. Il sistema verifica che l'Utente si trovi entro la distanza massima consentita dal mezzo.  3. Il sistema invia il comando di sblocco al mezzo.  4. Il mezzo conferma l'avvenuto sblocco al sistema.  5. Il sistema aggiorna lo stato del mezzo a "In Uso" e registra l'inizio della corsa.  6. Il sistema notifica l'Utente che il mezzo è pronto all'uso. |
| Postcondizioni | Il mezzo è fisicamente sbloccato; lo stato del mezzo è aggiornato a "In Uso"; la corsa è registrata come avviata nel sistema. |
| Sequenze alternative | Comando Sblocca Fallito |

|  |  |
| --- | --- |
| **Nome** | **Sblocca Mezzo: Comando Sblocca Fallito** |
| ID | CS-05.1 |
| Breve descrizione | Il mezzo non risponde al comando di sblocco inviato dal sistema. |
| Attori Primari | Utente |
| Attori secondari | Nessuno |
| Precondizioni | Il mezzo non ha risposto allo sblocco. |
| Postcondizioni | Il mezzo rimane bloccato. |
| Sequenza alternativa degli eventi | 1. La sequenza alternativa inizia dopo il passo 3 della sequenza principale.  2. Il sistema attende la conferma di sblocco dal mezzo.  3. Il sistema notifica l'Utente che non è stato possibile sbloccare il mezzo. |

Termina corsa

|  |  |
| --- | --- |
| **Nome** | **Termina corsa** |
| ID | CS-06 (UT.06) |
| Breve descrizione | Il sistema consente all'utente autenticato di terminare la corsa in corso, verificando la posizione del mezzo e applicando le regole di fine corsa configurate dall'operatore, così da liberare il mezzo e addebitare il costo della sessione. |
| Attori Primari | Utente |
| Attori Secondari | ServizioGIS |
| Precondizioni | L'utente è autenticato alla piattaforma e ha una corsa attiva. |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l'utente vuole terminare e pagare la corsa.   2. Il sistema rileva la posizione corrente del mezzo tramite ServizioGIS.        *Punto di estensione: ErroreServizioGis*  3. include (EffettuaPagamento).   4. Il sistema aggiorna lo stato del mezzo da "In Uso" a "Disponibile".   5. Il sistema mostra all'utente il Riepilogo Corsa con le varie informazioni. |
| Post-condizioni | La corsa è terminata, il mezzo è liberato e reso disponibile, l'addebito è stato effettuato e il riepilogo è mostrato all'utente. |
| Sequenza alternativa degli eventi | MezzoInZonaVietata |

|  |  |
| --- | --- |
| **Nome** | **Termina corsa: MezzoInZonaVietata** |
| ID | CS-06.1 |
| Breve descrizione | Il sistema informa l'utente che il mezzo si trova in una Zona Vietata e applica una penale obbligatoria prima di consentire la fine corsa. |
| Attori Primari | Utente |
| Attori Secondari | ServizioGIS |
| Precondizioni | Il mezzo si trova in una Zona Vietata al momento della richiesta di fine corsa. |
| Post-Condizioni | La corsa è terminata con applicazione della penale obbligatoria; il mezzo è liberato e l'addebito comprensivo di penale è stato effettuato. |
| Sequenza alternativa degli eventi | 1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.   2. Il sistema rileva che il mezzo si trova in una Zona Vietata.   3. Il sistema notifica l'utente che il mezzo si trova in una Zona Vietata e che verrà applicata una penale obbligatoria.   4. Il sistema prosegue dal passo 3 della sequenza principale applicando la penale al costo totale della corsa. |

Effettua Pagamento

|  |  |
| --- | --- |
| **Nome** | **EffettuaPagamento** |
| ID | CS-07 (UT.17) |
| Breve descrizione | Il sistema calcola l'importo dovuto e lo addebita automaticamente sul metodo di pagamento predefinito dell'Utente, senza richiedere alcuna azione manuale. |
| Attori primari | Utente |
| Attori secondari | ProviderPagamenti |
| Precondizioni | Una corsa dell'Utente è appena terminata; l'Utente ha un metodo di pagamento predefinito registrato e valido. |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando il sistema registra la fine della corsa.  2. Il sistema calcola la durata della corsa e l'importo dovuto in base alla tariffa applicabile.  3. Il sistema recupera il metodo di pagamento predefinito dell'Utente.  4. Il sistema trasmette la richiesta di addebito al Sistema di Pagamento Esterno.  5. Il Sistema di Pagamento Esterno autorizza e completa la transazione.  6. Il sistema genera e invia la ricevuta di pagamento all'Utente. |
| Postcondizioni | L'importo è addebitato; l'Utente riceve la ricevuta. |
| Sequenze alternative | PagamentoRifiutato |

|  |  |
| --- | --- |
| **Nome** | **EffettuaPagamento: PagamentoRifiutato** |
| ID | CS-07.1 |
| Breve descrizione | Il ProviderPagamenti rifiuta la transazione. |
| Attori Primari | Utente |
| Attori secondari | ProviderPagamenti |
| Precondizioni | Il ProviderPagamenti ha restituito un esito negativo per la transazione. |
| Postcondizioni | Il pagamento non è andato a buon fine; l'Utente è notificato del problema. |
| Sequenza alternativa degli eventi | 1. La sequenza alternativa inizia dopo il passo 4 della sequenza principale.  2. Il sistema riceve l'esito negativo dal Sistema di Pagamento Esterno.  3. Il sistema notifica l'Utente del fallimento e lo invita ad aggiornare il metodo di pagamento. |

Salva Metodi di Pagamento

|  |  |
| --- | --- |
| **Nome** | **SalvaMetodiDiPagamento** |
| ID | CS-08 (UT.12) |
| Breve descrizione | Il sistema consente all'utente autenticato di salvare uno o più metodi di pagamento sul proprio account, così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati. |
| Attori Primari | Utente |
| Attori Secondari | ProviderPagamenti |
| Precondizioni | L'utente è autenticato alla piattaforma. |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l'utente accede alla sezione "Portafoglio" dal menu laterale.   2. Il sistema mostra i metodi di pagamento attualmente associati all'account utente e l'opzione per aggiungerne uno nuovo.  3. L'utente seleziona l'opzione per aggiungere un nuovo metodo di pagamento.   4. Il sistema mostra le tipologie di metodo di pagamento disponibili (Google Pay, Apple Pay, PayPal, carta di credito).   5. L'utente seleziona la tipologia desiderata e inserisce i dati richiesti.  6. Il sistema valida i dati inseriti tramite ProviderPagamenti. Se ProviderPagamenti restituisce un errore di validazione, il sistema informa l'utente che i dati inseriti non sono validi e torna al passo 5.  7. Il sistema verifica che il metodo di pagamento non sia già associato all'account. Se è già presente, il sistema informa l'utente e non procede al salvataggio.   8. Il sistema salva il nuovo metodo di pagamento sull'account utente.   9. Se il metodo appena salvato è il primo associato all'account, il sistema lo imposta automaticamente come predefinito. Altrimenti, il sistema chiede all'utente se desidera impostarlo come nuovo metodo predefinito.   10. Se l'utente conferma, il sistema aggiorna il metodo predefinito con quello appena salvato.  11. Il sistema mostra un messaggio di conferma all'utente. |
| Post-condizioni | Il nuovo metodo di pagamento è stato salvato sull'account utente. Il metodo predefinito è quello scelto dall'utente, o il primo salvato se non è stata effettuata alcuna scelta esplicita. |
| Sequenza alternativa degli eventi | Nessuna |

Definisce tariffa

|  |  |
| --- | --- |
| **Nome** | **Definisce Tariffa** |
| ID | CS-09 (OP.07) |
| Breve descrizione | Il sistema consente all'operatore autenticato di definire una nuova tariffa per una specifica tipologia di mezzo, specificando il costo al minuto e il costo al chilometro, così da permettere la configurazione del modello di costo del servizio. |
| Attori Primari | Operatore |
| Attori Secondari | Nessuno |
| Precondizioni | L'operatore è autenticato alla piattaforma e non esiste già una tariffa definita per la tipologia di mezzo selezionata. |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicate alle tariffe.   2. Il sistema mostra le tariffe attualmente definite per ciascuna tipologia di mezzo disponibile.   3. L'operatore seleziona la tipologia di mezzo per cui intende definire una nuova tariffa (monopattino, bicicletta, automobile).   4. Il sistema mostra il form di inserimento con i campi: costo al minuto e costo al chilometro.   5. L'operatore inserisce i valori richiesti.   6. Il sistema valida i dati inseriti verificando che i valori siano numerici e maggiori di zero.   7. Il sistema salva la nuova tariffa associandola alla tipologia di mezzo selezionata.   8. Il sistema mostra un messaggio di conferma all'operatore. |
| Post-condizioni | La nuova tariffa è stata salvata nel sistema e sarà applicata alle corse successive effettuate con la tipologia di mezzo selezionata. |
| Sequenza alternativa degli eventi | Nessuna |



Modifica stato mezzo

|  |  |
| --- | --- |
| **Nome** | **Modifica Stato Mezzo** |
| ID | CS-10 (OP.04) |
| Breve descrizione | Il sistema consente all'operatore autenticato di modificare lo stato di un mezzo della flotta, così da nasconderlo o mostrarlo sulla Mappa Utente e gestire il ciclo operativo del veicolo. |
| Attori Primari | Operatore |
| Attori Secondari | Nessuno |
| Precondizioni | L'operatore è autenticato alla piattaforma e il mezzo selezionato esiste nella flotta. |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata ai mezzi.   2. Il sistema mostra la Mappa Operatore con la lista dei mezzi della flotta e il loro stato corrente.   3. L'operatore seleziona il mezzo di cui intende modificare lo stato.   4. Il sistema mostra lo stato corrente del mezzo e le opzioni di stato selezionabili tra: Disponibile, In manutenzione, Fuori servizio.   5. L'operatore seleziona il nuovo stato desiderato.   6. Il sistema verifica che la transizione di stato richiesta sia consentita.   7. Il sistema aggiorna lo stato del mezzo.   8. Il sistema mostra un messaggio di conferma all'operatore. |
| Post-condizioni | Lo stato del mezzo è stato aggiornato. Se il nuovo stato è "In manutenzione" o "Fuori servizio" il mezzo non è più visibile sulla Mappa Utente; se il nuovo stato è "Disponibile" il mezzo è nuovamente visibile sulla Mappa Utente |
| Sequenza alternativa degli eventi | MezzoInUso |

|  |  |
| --- | --- |
| **Nome** | **Modifica Stato Mezzi: MezzoInUso** |
| ID | CS-10.1 |
| Breve descrizione | Il sistema informa l'operatore che il mezzo selezionato è attualmente in uso da un utente e non può essere modificato. |
| Attori Primari | Operatore |
| Attori Secondari | Nessuno |
| Precondizioni | Il mezzo selezionato ha stato "In uso" o "Prenotato" al momento della richiesta di modifica. |
| Post-condizioni | Nessuna. Lo stato del mezzo non viene modificato. |
| Sequenza alternativa degli eventi | 1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.   2. Il sistema rileva che il mezzo è attualmente in uso o prenotato da un utente.   3. Il sistema informa l'operatore che non è possibile modificare lo stato del mezzo mentre è in uso o prenotato |

Aggiunge Mezzo

|  |  |
| --- | --- |
| **Nome** | **Aggiunge Mezzo** |
| ID | CS-11 (OP.11) |
| Breve descrizione | Il sistema consente all'operatore autenticato di aggiungere un nuovo mezzo alla flotta, specificando tipologia, identificativo, posizione iniziale e stato, così da renderlo disponibile per il noleggio da parte degli utenti. |
| Attori Primari | Operatore |
| Attori Secondari | ServizioGIS |
| Precondizioni | L'operatore è autenticato alla piattaforma e si trova nella Dashboard Operatore. |
| Sequenza principale degli eventi | 1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata ai mezzi.  2. Il sistema mostra la lista dei mezzi attualmente presenti nella flotta.  3. L'operatore seleziona la funzione che permette di aggiungere un nuovo mezzo.  4. Il sistema permette di inserire i campi: tipologia (monopattino, bicicletta, automobile), identificativo, posizione iniziale e stato iniziale.  5. L'operatore inserisce i dati richiesti e seleziona la posizione iniziale sulla mappa.  6. L'operatore conferma i dati inseriti.  7. Il sistema valida i dati verificando che i campi obbligatori siano compilati e che l'identificativo sia univoco. Se uno o più campi non sono validi, il sistema informa l'operatore specificando i campi non validi e torna al passo 5.   8. Il sistema verifica tramite ServizioGIS che la posizione selezionata ricada all'interno di una zona operativa.   9. Il sistema salva il nuovo mezzo associandolo alla flotta.   10. Il sistema mostra un messaggio di conferma all'operatore. |
| Post-condizioni | Il nuovo mezzo è stato salvato nel sistema e risulta disponibile sulla Mappa Utente in base allo stato impostato. |
| Sequenza alternativa degli eventi | IdentificativoEsistente |

Dismette Mezzo

|  |  |
| --- | --- |
| **Nome** | **Dismette Mezzo** |
| ID | CS-12 (OP.12) |
| Breve descrizione | Il sistema consente all'operatore autenticato di dismettere un mezzo precedentemente censito, rimuovendone la disponibilità per l'assegnazione a nuove missioni e mantenendone lo storico ai fini di consultazione. |
| Attori Primari | Operatore |
| Attori Secondari | Nessuno |
| Precondizioni | L'operatore deve essere autenticato nel sistema e il mezzo da dismettere deve essere già censito e non assegnato ad alcuna missione attiva. |
| Sequenza principale | 1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata ai mezzi.   2. Il sistema mostra la lista dei mezzi presenti nella flotta con il loro stato corrente.   3. L'operatore seleziona il mezzo da dismettere.   4. Il sistema mostra i dettagli del mezzo selezionato e richiede conferma della dismissione.   5. L'operatore conferma la dismissione.   6. Il sistema aggiorna lo stato del mezzo a "Dismesso" e lo rimuove dall'elenco dei mezzi disponibili.   7. Il sistema mantiene lo storico delle informazioni associate al mezzo.   8. Il sistema mostra un messaggio di conferma all'operatore. |
| Post-condizioni | Il mezzo è registrato come dismesso nel sistema, non risulta più disponibile per l'assegnazione a nuove corse e i dati storici relativi al mezzo rimangono consultabili. |
| Sequenza alternativa degli eventi | MezzoInUso |

|  |  |
| --- | --- |
| **Nome** | **Dismette Mezzo: MezzoInUso** |
| ID | CS-12.1 |
| Breve descrizione | Il sistema informa l'operatore che il mezzo selezionato è attualmente impegnato in una missione e non può essere dismesso. |
| Attori Primari | Operatore |
| Attori Secondari | ServizioGIS |
| Precondizioni | L'operatore deve essere autenticato nel sistema e il mezzo selezionato risulta assegnato a una corsa attiva. |
| Post-condizioni | Lo stato del mezzo resta invariato e l'operatore rimane nella sezione di gestione dei mezzi. |
| Sequenza alternativa degli eventi | 1. Il sistema, tramite il ServizioGIS, rileva che il mezzo selezionato è impegnato in una corsa.  2. Il sistema notifica all'operatore l'impossibilità di dismettere il mezzo, indicandone la causa.   3. L'operatore prende visione del messaggio e ritorna alla sezione di gestione dei mezzi. |

Definisce Regole Fine Corsa

|  |  |
| --- | --- |
| **Nome** | **Definisce Regole Fine Corsa** |
| ID | CS-13 (OP.13) |
| Breve descrizione | L'operatore definisce le regole che determinano la corretta conclusione di una corsa, specificando i vincoli relativi alla posizione di rilascio del mezzo (zona di parcheggio consentita) e alle condizioni necessarie affinché la corsa possa essere chiusa con successo. |
| Attori Primari | Operatore |
| Attori Secondari | Nessuno |
| Precondizioni | L'operatore deve essere autenticato nel sistema e deve aver selezionato la funzione di configurazione delle regole di fine corsa. |
| Sequenza principale | 1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata alle Regole Fine Corsa   2. Il sistema mostra le zone di parcheggio disponibili e i parametri configurabili.   3. L'operatore seleziona le zone di parcheggio valide per la chiusura della corsa e imposta i vincoli aggiuntivi (stato del mezzo, livello batteria minimo, posizionamento corretto).   4. L'operatore conferma le regole definite.   5. Il sistema valida i parametri inseriti verificando che i valori rientrino negli intervalli ammessi. Se uno o più parametri non sono validi, il sistema informa l'operatore specificando i campi non validi e torna al passo 3.   6. Il sistema salva la nuova configurazione delle regole di fine corsa.   7. Il sistema notifica all'operatore l'avvenuta definizione delle regole. |
| Post-condizioni | Le nuove regole di fine corsa sono memorizzate nel sistema e vengono applicate a tutte le corse successive. |
| Sequenza alternativa degli eventi | Nessuna |

Altro

System Architecture

Diagramma delle Componenti – Diagramma Generale

Specifica delle componenti

Detailed Product Design

Diagramma delle Classi – Diagramma Generale

Specifiche delle Classi

Diagrammi di Sequenza

Data modeling and design

Qui va fornita la specifica di tutti i dati e le informazioni scambiate dal sistema in corso di realizzazione con l’utenza di riferimento e/o gli eventuali altri sistemi con cui esso comunica. Deve essere descritto il modello logico della base di dati e la sua struttura fisica.

Modello logico del Database

Struttura fisica del Database

Prompt 

Qualità dei requisiti

La seguente sezione riporta il prompt utilizzato per la convalidazione della qualità delle user story secondo le 14 caratteristiche di qualità definite nel corso. Le user story corrette a seguito di questa analisi sono riportate nel Product Backlog. 

You are a software engineer, specialized in requirements elicitation. In this phase, you need to read the User Stories. You need to read them carefully, evaluate them following the "Quality Verification Characteristics" that

are listed below.

### Context 

The municipality of Zootropolis wishes to introduce a sustainable transport system that integrates various sharing services (e.g., Bike, Car, E-scooter sharing) 

The system must operate in an urban environment involving:

- Users

- Operators

- Public authorities

## Expected Input Format

The user stories and "Quality Verification Characteristics" are written in Italian.

The user stories that will be sent to you will be in this form:

COME [ruolo] VOGLIO [fare qualcosa] COSÌ CHE [possa ottenere valore per il business]

To add more information, what follows is an example of a user story:

`COME magazziniere 

VOGLIO poter filtrare l'archivio ordini secondo la data di ricezione 

COSÌ CHE possa consultare gli ordini evasi`

## Quality Verification Characteristics

All of them are reported below:

### 1. Non Ambiguo

Deve esserci un solo modo di interpretare ogni requisito.

Le ambiguità sono create da:

\*\*Acronimi\*\*: gli acronimi devono essere scritti per intero, con l'acronimo tra parentesi.

Esempio scorretto: "Richiedere al cliente di digitare il PIN."

Esempio corretto: "Richiedere al cliente di digitare il Personal Identification Number (PIN)."

\*\*Cattivo uso dei termini\*\*: termini vaghi lasciano spazio a interpretazioni multiple.

Esempio scorretto: "Il sistema dispensa contanti fino a 500 euro a scelta del cliente." Non è chiaro se la somma e digitata liberamente, scelta tra opzioni, arrotondata o rifiutata se fuori soglia.

Esempio corretto: "Il sistema dispensa una somma a scelta del cliente tra quelle proposte: 100, 150, 200, 250, 300, 400, 500 euro."

\*\*Eccessiva sintesi\*\*: una formulazione troppo breve omette dettagli necessari.

Esempio scorretto: "Il sistema mostra 5 movimenti di Deposito o di Conto Corrente quando il cliente chiede l'estratto conto." Non è chiaro quali 5 movimenti vengano mostrati.

Esempio corretto: "Il cliente richiede l'estratto conto indicando il numero di ultimi movimenti desiderati, fino a un massimo di 20, sul conto di deposito o di conto corrente selezionato. Il sistema mostra 5 movimenti per videata. Se il cliente richiede più di 20 movimenti, il sistema riduce il numero a 20 e avverte il cliente."

### 2. Provabile o Verificabile

Deve essere possibile costruire casi di test corretti e non corretti rispetto a ogni requisito, per verificare che il sistema elabori correttamente i primi e rigetti i secondi.

Elementi che rendono un requisito non provabile:

- Aggettivi generici: robusto, sicuro, accurato, effettivo, efficiente, espandibile, flessibile, mantenibile, disponibile, amichevole, adeguato.

- Avverbi generici: velocemente, tranquillamente, tempestivamente.

- Parole ed acronimi non specifici: ecc., e/o, TBD.

- Parole generiche: gestire, manipolare.

- Espressioni generiche: che sia appropriato, come richiesto, se necessario.

- Pronomi indefiniti: pochi, molti, tanto, spesso, qualche volta, tutti, qualsiasi, alcune, qualcuno.

- Voci passive: il soggetto riceve l'azione del verbo invece di compierla.

Esempio scorretto: "Il numero di conto digitato dal cliente sarà controllato per esattezza ed esistenza nella base dati."

Esempio corretto: "Il sistema controlla che il numero di conto digitato sia corretto sintatticamente ed esista nella base di dati."

### 3. Chiaro

Il requisito deve essere conciso, laconico, semplice e preciso. Non deve contenere verbosità o informazioni non necessarie.

Esempio scorretto: "Qualche volta il cliente potrebbe chiedere l'estratto conto del deposito o del conto corrente intestato a lui; in tal caso deve dichiarare il periodo a cui si deve riferire l'estratto conto richiesto ed è necessario chiedere se vuole la stampa su carta o gli basta vederlo sul video."

Esempio corretto: "Il cliente può chiedere l'estratto conto per il periodo che dichiara. Il sistema riporta l'estratto conto, a scelta del cliente, su carta o su video."

### 4. Corretto

Se un requisito contiene fatti, questi devono essere veri.

Esempio scorretto: "Il costo dell'operazione sarà di 1 euro."

Questo requisito non è corretto per almeno due motivi: le operazioni eseguibili all'ATM non hanno tutte lo stesso prezzo, e il prezzo dipende dalla politica della banca che gestisce l'ATM e dagli accordi con la banca emittente della carta.

### 5. Comprensibile

I requisiti devono essere grammaticalmente corretti e scritti in stile consistente. Devono essere usati appositi standard terminologici. La parola "deve" deve essere utilizzata al posto di "volere", "bisogna" o "può".

### 6. Fattibile

I requisiti devono essere realizzabili entro i vincoli esistenti di tempo, denaro e risorse disponibili.

Esempio scorretto: "Il sistema userà un linguaggio naturale nell'interfaccia così che comprenda i comandi espressi in lingua italiana."

Questo requisito richiede un grande investimento di tempo e risorse, con notevole rischio di non essere realizzato con un adeguato livello di affidabilità.

### 7. Indipendente e Auto-consistente

Per comprendere un requisito non deve essere necessario conoscere nessun altro requisito.

Esempio scorretto:

- ReqI: "Il sistema elenca tutti gli importi erogabili per il cliente che ha inserito la carta di credito nell'ATM."

- ReqD: "Essi sono elencati in ordine crescente."

Il pronome "essi" si riferisce agli importi di ReqI. Se l'ordine dei requisiti nello SRS venisse modificato, ReqD diventerebbe incomprensibile.

### 8. Atomico

Ogni requisito deve contenere un solo elemento tracciabile. Le espressioni che contengono "e" o "ma" devono essere riviste e suddivise.

Esempio scorretto: "Il cliente inserisce il PIN, chiede l'erogazione di una somma e l'estratto conto."

Questo requisito ne contiene tre atomici distinti e deve essere suddiviso di conseguenza.

### 9. Necessario

Un requisito e inutile se nessuna parte interessata ne ha bisogno, oppure se la sua cancellazione non ha alcuna conseguenza sul sistema finale perché non aggiunge informazioni. I requisiti inutili sono quelli che l'analista inserisce nello SRS ritenendoli desiderati dalle parti interessate, senza che nessuna di esse li abbia esplicitamente richiesti.

Esempi di requisiti potenzialmente non necessari:

- "Tutti i requisiti specificati nello SRS devono essere testati."

- "Il sistema stampa il nome della filiale che gestisce l'ATM utilizzato dal cliente."

### 10. Astratto

I requisiti non devono contenere dettagli circa la loro implementazione, salvo che tale dettaglio costituisca un vincolo esplicitamente dichiarato dall'utente. L'implementazione e di interesse del progettista, non degli utenti del sistema.

Esempio: "Il contenuto informativo sarà memorizzato in forma strutturata."

Questo requisito specifica un dettaglio implementativo e deve essere rivisto salvo che rappresenti un vincolo esplicito.

### 11. Consistente

Tutti i requisiti devono utilizzare termini uguali per esprimere concetti uguali, e nessun requisito deve essere conflittuale con altri.

I conflitti possono essere:

\*\*Diretti\*\*: in una stessa situazione il comportamento del sistema deve essere diverso.

Esempio:

- ReqX: "L'ATM accetta tutte le carte di credito e il Bancomat emesso da qualsiasi banca."

- ReqY: "L'ATM accetta i Bancomat emessi dalle banche convenzionate con la banca gestore."

Per eliminare il conflitto e necessario cancellare uno dei due requisiti.

Esempio di terminologia inconsistente e conflitto sul formato:

- ReqX: "Le date devono essere visualizzate nella forma mm/dd/yyyy."

- ReqY: "Le date devono essere visualizzate nella forma gg/mm/aaaa."

Possibile correzione con precisazione del contesto:

- ReqX: "Le date per gli ATM in U.S. devono essere visualizzate nella forma mm/dd/yyyy."

- ReqY: "Le date per gli ATM in Italia devono essere visualizzate nella forma gg/mm/aaaa."

In alternativa, generalizzando: "Le date saranno visualizzate nel formato definito dall'utente all'installazione."

\*\*Indiretti\*\*: due requisiti non descrivono la stessa situazione ma non è possibile soddisfarli contemporaneamente.

Esempio:

- ReqX: "Il sistema deve avere l'interfaccia in linguaggio naturale."

- ReqY: "Il sistema sarà prodotto in due settimane."

Per eliminare il conflitto e necessario rilassare uno dei due requisiti.

### 12. Non Ridondante

Ogni requisito deve essere espresso una sola volta e non deve sovrapporsi a un altro.

Esempio:

- ReqX: "Il sistema mette a disposizione un calendario per aiutare a definire le date di intervallo dell'estratto conto richiesto."

- ReqY: "Il sistema mette a disposizione un calendario ogni volta che si deve digitare una data."

ReqX e un caso particolare di ReqY e deve essere cancellato.

### 13. Completo

Un requisito deve essere specificato per tutte le condizioni che possono verificarsi.

Esempio:

- ReqX: "Il sistema non visualizza la data di prelievo."

- ReqY: "Il sistema non visualizza l'anagrafica del cliente."

Il numero del conto, che non è né una data né un dato anagrafico, viene visualizzato? Il requisito e incompleto perché non copre tutti i casi possibili.

### 14. Metriche Derivate

\*\*Manutenibile\*\*: un requisito atomico e non ridondante e più facilmente modificabile.

\*\*Tracciabile\*\*: un requisito atomico dotato di identificatore univoco e tracciabile lungo il ciclo di vita del sistema.

## Output Format

Each Characteristic must be evaluated on a scale from 0 to 5, and a brief reason pointing out the errors must be specified.

What follows is the output's specific structure. Present all the data in a tabular format; each noun between the rectangular parentheses must be in a separate column. Stick with it and do not perform additional formatting or styling outside of what is being specified below:

- [Characteristic Name], [score], [reason]

At the end, add a mean score, which is the mean of all the scores.

Output Prompt Requisiti

|  |  |  |
| --- | --- | --- |
| Characteristic Name | Score | Reason |
| Non Ambiguo | 5 | Grazie all'uso del glossario e alla rimozione di avverbi vaghi, ogni requisito ha ora un'unica interpretazione possibile. |
| Provabile o Verificabile | 5 | La separazione dei requisiti e l'uso di termini precisi permettono di costruire test case binari (Pass/Fail) per ogni singola funzionalità. |
| Chiaro | 5 | Le User Story sono concise, laconiche e prive di verbosità , rispettando perfettamente il formato standard. |
| Corretto | 5 | I requisiti rappresentano fedelmente le necessità del business e i vincoli normativi espressi nel contesto di Zootropolis. |
| Comprensibile | 5 | Lo stile è consistente, grammaticalmente corretto e utilizza i termini definiti nel glossario in modo impeccabile. |
| Fattibile | 5 | Tutte le funzionalità (gestione mappe, sblocco, pagamenti) sono realizzabili con le tecnologie attuali entro i vincoli di progetto. |
| Indipendente e Auto-consistente | 5 | Ogni requisito è comprensibile senza dover fare riferimento ad altri item, garantendo la massima modularità. |
| Atomico | 5 | **Migliorato:** Ogni User Story contiene ora un solo elemento tracciabile. Abbonamenti, bonus e diverse tipologie di zone sono gestiti separatamente. |
| Necessario | 5 | La clausola "Così da" giustifica ogni funzione in base al valore reale per cittadini, operatori o amministrazione. |
| Astratto | 5 | I requisiti non contengono dettagli implementativi superflui, lasciando libertà ai progettisti (es. metodo di sblocco QR/NFC). |
| Consistente | 5 | Non vi sono conflitti tra i requisiti; le regole di precedenza tra zone AP e zone OP sono chiaramente stabilite. |
| Non Ridondante | 5 | Ogni funzionalità è espressa una sola volta e non vi sono sovrapposizioni tra i diversi ruoli utente. |
| Completo | 5 | **Migliorato:** La scomposizione dei requisiti ha permesso di coprire anche i flussi e le condizioni specifiche per ogni diversa entità del sistema. |
| Metriche Derivate | 5 | **Migliorato:** L'elevata atomicità garantisce ora una manutenibilità eccellente e una tracciabilità precisa lungo tutto il ciclo di vita. |

**Mean Score: 5.0**

Definizioni

Glossario

Acronimi

* **AP**: Amministrazione Pubblica
* **CSV**: Comma-Separated Values
* **NFC**: Near Field Communication
* **OP**: Operatore del Servizio
* **PDF**: Portable Document Format
* **QR**: Quick Response (code)
* **UT**: Utente
* **HTTP**: HyperText Transfer Protocol
* **ServizioGIS**: Geographic Information System
* **API**: Application Programming Interface
* **BLL**: Business Logic Layer
* **DAL**: Data Access Layer
* **DBMS**: Database Management System

Definizioni

* **Account utente**: Insieme di credenziali, dati anagrafici, metodi di pagamento, e-mail, password e storico associati a un utente registrato. Il profilo personale è la vista utente dell'account.
* **Addebito**: Importo economico calcolato al termine di una corsa o di un evento tariffabile e prelevato dal metodo di pagamento associato all'account utente.
* **Amministrazione Pubblica**: Ente locale (comune o equivalente) che regolamenta l'uso dello spazio urbano e definisce vincoli e agevolazioni per il servizio di sharing. Nel sistema è un ruolo distinto da Utente e Operatore.
* **Autonomia residua**: Valore numerico indicante la carica rimasta nella batteria di un mezzo elettrico (e-bike, e-scooter). Espresso in percentuale (%) o in chilometri stimati; l'unità di misura adottata è configurabile dalla piattaforma.
* **Corsa**: Sessione di utilizzo attivo di un mezzo sharing, che inizia con lo sblocco del veicolo e termina con la chiusura della sessione da parte dell'utente. Al termine viene calcolato e addebitato il costo. Sinonimo: Sessione.
* **Fine corsa**: Evento che conclude una corsa; l'esito (valido, penalizzato, rifiutato) dipende dalla posizione del mezzo rispetto a Zona Operativa e Zona di parcheggio.
* **Formato Esportabile:** Formattazione offerta dalla piattaforma per l’esportazione dei dati. Include CSV, PDF.
* **Flotta**: Insieme di tutti i mezzi gestiti da un operatore nell'ambito del servizio di sharing su un determinato territorio.
* **Mappa Operatore**: Visualizzazione cartografica accessibile agli operatori del servizio, che mostra negli ultimi x minuti la posizione e lo stato di tutti i mezzi della flotta, inclusi quelli nascosti alla Mappa Utente. Distinta dalla Mappa Utente per contenuto e permessi di accesso.
* **Mappa Utente**: Visualizzazione cartografica accessibile agli utenti, che mostra i mezzi disponibili e prenotabili nelle vicinanze entro un raggio configurabile, le zone con vincoli di circolazione o parcheggio, e le zone di parcheggio consigliate. Non mostra i mezzi rimossi dall'operatore.
* **Metodo di pagamento**: Strumento associato all'account utente (carta, wallet, ecc.) utilizzato per regolare gli addebiti.
* **Mezzo**: Qualsiasi veicolo messo a disposizione degli utenti nell'ambito del servizio: bicicletta tradizionale, bicicletta a pedalata assistita (e-bike), monopattino elettrico (e-scooter) e macchina elettrica.
* **Mezzo disponibile:** Mezzo il cui stato (definito nel glossario) è Disponibile, ossia prenotabile da un utente. Gli unici visualizzabili nella Mappa Utente.
* **Operatore del Servizio: Soggetto (azienda privata o consorzio)** responsabile della gestione operativa della flotta e della configurazione della piattaforma: definisce tariffe, promozioni, zone operative, parametri di prenotazione e pausa corsa.
* **Pausa corsa**: Stato intermedio di una sessione in cui l'utente blocca temporaneamente il mezzo senza terminare la corsa.
* **Periodo di grazia**: Durata massima configurabile dall'operatore entro cui una pausa corsa non comporta addebiti aggiuntivi o la perdita del mezzo. Se impostato a zero, la funzionalità di pausa gratuita è disabilitata.
* **Prenotazione**: Riserva temporanea di un mezzo specifico effettuata dall'utente prima di raggiungerne fisicamente la posizione. Ha una durata massima configurabile dall'operatore; alla scadenza il mezzo viene automaticamente rilasciato e reso disponibile ad altri utenti.
* **Prenotazione di gruppo**: Prenotazione effettuata da un singolo utente per un numero di mezzi fino al massimo configurato dall'operatore (può anche essere uno).
* **Promozione**: Offerta che riduce la tariffa standard o offre condizioni speciali (es. prime N corse gratis, sconto percentuale). Configurata e pubblicata dall'operatore.

+ **Abbonamento:** Contratto a tempo determinato (es. mensile, annuale) che garantisce all'utente condizioni tariffarie agevolate o un numero di corse incluse. Configurato e pubblicato dall'operatore.
+ **Bonus**: Valore monetario assegnato all'utente dall'operatore secondo certe condizioni (es. parcheggio corretto, alto numero di corse). Se impostato a zero, la funzionalità non è visualizzabile dall'utente.

* **Redistribuzione**: Operazione logistica di spostamento fisico dei mezzi da aree con eccesso di offerta verso aree con carenza, eseguita dal personale operativo sulla base dei dati della Mappa Operatore.
* **Report aggregato**: Documento che consolida statistiche anonime sull'utilizzo del servizio (corse, km, fasce orarie, zone) su un intervallo temporale configurabile. Destinato all'operatore e all'amministrazione pubblica.
* **Riepilogo corsa**: Sintesi presentata all'utente al termine di una corsa, che riporta i dati principali della sessione: durata complessiva, distanza percorsa, costo finale calcolato sulla base della tariffa applicata ed eventuali sconti o bonus. Disponibile anche nello storico corse del profilo utente.
* **Sblocco**: Operazione che disabilita il blocco fisico/elettronico del mezzo, consentendo all'utente di iniziare la corsa. Il metodo di sblocco (QR code, Bluetooth, NFC) è una scelta implementativa.
* **Segnalazione**: Comunicazione inviata dall'utente all'operatore per notificare anomalie su un mezzo (danno fisico, guasto, posizione anomala). Visibile nella Dashboard operatore.
* **Sessione**: Sinonimo di Corsa. Periodo di utilizzo attivo di un mezzo, tracciato dal sistema con marcatura temporale di inizio e fine.
* **Stato (mezzo)**: Condizione operativa corrente di un mezzo. Valori possibili: Disponibile (prenotabile), Prenotato (riservato a un utente), In uso (corsa attiva), In pausa (pausa corsa attiva), In manutenzione (rimosso dalla Mappa Utente), Fuori servizio (bloccato o irrecuperabile).
* **Storico corsa**: L’insieme delle corse effettuate da un Utente.
* **Tariffa**: Struttura di pricing applicata a una corsa. La tipologia (es. costo al minuto, alla distanza, tariffa fissa per fascia oraria) è definita e modificabile dall'operatore. La tariffa applicabile è mostrata all'utente prima dell'avvio della corsa.
* **Tariffario**: Elenco pubblicato dall'operatore delle tariffe applicate per ciascuna tipologia di mezzo e modalità di utilizzo. Distinto da Tariffa (struttura applicata alla singola corsa).
* **Utente**: Persona fisica registrata alla piattaforma che utilizza i mezzi di sharing per spostarsi nel contesto urbano. Interagisce con il sistema tramite dispositivo mobile.
* **Zona**:

+ **Zona Operativa**: Perimetro geografico definito dall'operatore entro cui i mezzi della flotta possono circolare e fermarsi. Un mezzo che esce dalla zona operativa può attivare allarmi automatici o bloccarsi. La Zona Limitata e la Zona Vietata hanno sempre la precedenza sulla Zona Operativa.
+ **Zona di parcheggio**: Area geografica designata esclusivamente dall’operatore in cui è consigliato — ma non imposto — parcheggiare il mezzo al termine della corsa. Visibile sulla Mappa Utente. L'operatore può decidere se associare a esse un Bonus economico per l'utente e configurarne il valore. Se il bonus non è configurato o è impostato a zero, la zona resta visibile come indicazione ma non genera alcun incentivo.
+ **Zona Soggetta a restrizioni:**

- **Zona Limitata**: Area geografica in cui la circolazione dei mezzi è consentita ma con restrizioni configurabili (es. velocità ridotta, orari limitati, divieto di sosta o pausa). Configurata dall’Operatore.
- **Zona Vietata**: Area geografica definita dall’Operatore in cui la circolazione dei mezzi è completamente vietata. Distinta dalla Zona Limitata (restrizioni parziali). Ha precedenza sulla Zona Operativa in caso di sovrapposizione.