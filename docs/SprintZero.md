# Smart Mobility — Sprint Zero

**Versione:** 2.0  
**Data di rilascio:** 10/05/2026  
**Corso:** Ingegneria del Software a.a. 2025-2026 — Informatica e Tecnologie per la Produzione del Software

**Realizzato da:**

| Nome | Matricola | Email |
|---|---|---|
| Cardone Flavio | 829469 | f.cardone21@studenti.uniba.it |
| De Astis Gabriele | 826243 | g.deastis1@studenti.uniba.it |
| Giannulo Francesco | 825071 | f.giannulo@studenti.uniba.it |
| Lacirignola Camilla | 830465 | c.lacirignola5@studenti.uniba.it |

---

## Indice

1. [Product Backlog](#1-product-backlog)
   - 1.1 [Introduzione](#11-introduzione)
   - 1.2 [Contesto di business](#12-contesto-di-business)
   - 1.3 [Stakeholder](#13-stakeholder)
   - 1.4 [Item funzionali](#14-item-funzionali)
   - 1.5 [Item non funzionali](#15-item-non-funzionali)
2. [Sprint Report](#2-sprint-report)
   - 2.1 [Sprint Backlog](#21-sprint-backlog)
   - 2.2 [Product Requirement Specification](#22-product-requirement-specification)
   - 2.3 [System Architecture](#23-system-architecture)
   - 2.4 [Detailed Product Design](#24-detailed-product-design)
   - 2.5 [Data Modeling and Design](#25-data-modeling-and-design)
3. [Prompt](#3-prompt)
   - 3.1 [Qualità dei requisiti](#31-qualità-dei-requisiti)
   - 3.2 [Output Prompt](#32-output-prompt)
   - 3.3 [Definizioni](#33-definizioni)
4. [Glossario](#4-glossario)
   - 4.1 [Acronimi](#41-acronimi)
   - 4.2 [Definizioni](#42-definizioni)

---

## 1. Product Backlog

### 1.1 Introduzione

**SMART MOBILITY** è un sistema software progettato per supportare il Comune di Zootropolis nell'introduzione di un servizio integrato di mobilità urbana sostenibile, che mette a fattor comune diversi servizi di sharing (bike sharing, car sharing, e-scooter sharing e altri) in un'unica piattaforma accessibile a cittadini, operatori e amministrazione pubblica.

Il sistema si pone tre obiettivi macroscopici:

1. Offrire ai cittadini un accesso rapido, sicuro e trasparente ai mezzi di sharing disponibili sul territorio.
2. Permettere agli operatori del servizio di gestire in modo efficiente la flotta, ridurre costi e fenomeni di vandalismo.
3. Consentire all'Amministrazione Pubblica di monitorare la mobilità urbana e assumere decisioni strategiche basate su dati.

**Per gli Utenti**, SMART MOBILITY offre:
- Visualizzazione dei mezzi disponibili nelle vicinanze e del loro stato
- Prenotazione di uno o più mezzi e sblocco tramite dispositivo personale
- Pagamenti veloci e sicuri
- Garanzia di affidabilità del sistema, con meccanismi di prevenzione di frodi ed errori
- Promozioni, pausa della corsa e gestione del profilo di pagamento

**Per gli Operatori del Servizio**, SMART MOBILITY offre:
- Visualizzazione della distribuzione della flotta e notifiche sulle aree con bassa disponibilità
- Monitoraggio di malfunzionamenti, manutenzione pianificata e posizione dei mezzi a fine corsa
- Bonus per parcheggio corretto, sospensione account in caso di frode e blocco automatico dei mezzi fuori dalle zone consentite

**Per l'Amministrazione Pubblica**, SMART MOBILITY offre:
- Monitoraggio della frequenza di utilizzo delle diverse tipologie di mezzo e dei pattern di mobilità urbana
- Accesso a report aggregati per supportare decisioni strategiche sulla mobilità
- Analisi dello stato dei mezzi e delle tratte più utilizzate per pianificare manutenzioni e interventi urbani
- Selezione di zone sensibili con divieto o limitazione del transito

---

### 1.2 Contesto di business

Nel panorama urbano contemporaneo, caratterizzato da un'emergenza climatica sempre più pressante, dalla necessità di decongestionare i centri storici e dalla transizione verso modelli di "Smart City", emerge con forza l'esigenza di soluzioni integrate per la mobilità dolce e condivisa.

SMART Mobility nasce per rispondere a questa sfida, superando la frammentazione degli attuali servizi di sharing e offrendo una piattaforma unica che connette cittadini, operatori privati e pubblica amministrazione.

Il software è pensato per essere usato nei seguenti ambiti:

**Mobilità per i cittadini**
In un ambiente urbano dove possedere un mezzo privato è sempre più costoso e inefficiente, i cittadini necessitano di strumenti che permettano di pianificare spostamenti intermodali in tempo reale. SMART Mobility offre un ecosistema che permette all'utente di localizzare, prenotare e pagare diversi tipi di mezzi (bici, monopattini, auto elettriche) tramite un'unica interfaccia, garantendo trasparenza sulle tariffe e sulla disponibilità, oltre a incentivare comportamenti virtuosi tramite bonus per il parcheggio corretto.

**Contesto operativo degli operatori di flotta**
La gestione di una flotta di mezzi condivisi comporta sfide logistiche enormi, dal recupero dei mezzi scarichi alla manutenzione per atti vandalici. Gli operatori necessitano di strumenti avanzati per il monitoraggio costante della flotta, la gestione delle zone operative e l'ottimizzazione dei flussi di ridistribuzione. SMART Mobility permette ai gestori di massimizzare il tempo di attività dei mezzi, ridurre i costi di recupero e analizzare le zone a maggior rendimento.

**Contesto di governance dell'Amministrazione Pubblica**
I comuni si trovano spesso a subire l'invasione di mezzi di sharing senza avere gli strumenti per regolarli efficacemente. SMART Mobility offre alle amministrazioni una "dashboard di controllo" per definire in tempo reale zone vietate, zone a velocità limitata e aree di parcheggio obbligatorie. Il sistema consente di raccogliere dati granulari sui flussi di traffico, permettendo di pianificare infrastrutture ciclabili e pedonali basandosi su evidenze reali anziché su stime.

**Contesto di sostenibilità e monitoraggio ambientale**
In un'epoca di obiettivi stringenti per la riduzione della CO₂, cresce il bisogno di monitorare l'impatto ambientale dei trasporti. SMART Mobility risponde a questa esigenza fornendo statistiche aggregate sui chilometri percorsi con mezzi elettrici e sul risparmio di emissioni, permettendo sia all'utente che al Comune di visualizzare il proprio contributo concreto alla transizione ecologica.

---

### 1.3 Stakeholder

Il sistema SMART Mobility coinvolge diversi stakeholder che interagiscono con la piattaforma con ruoli e obiettivi specifici:

#### 1. Utente
È l'utente che usufruisce dei mezzi di mobilità condivisa. Deve essere registrato per utilizzare la mappa, per localizzare i mezzi, per noleggiare e pagare.

| Tipologia | Descrizione |
|---|---|
| **Pendolare Urbano** | Utilizza regolarmente il servizio per coprire l'ultimo miglio (es. da stazione a ufficio). Cerca affidabilità e abbonamenti convenienti. |
| **Utente Occasionale** | Residente che utilizza il servizio saltuariamente per necessità impreviste o svago. |
| **Turista** | Visitatore che necessita di un accesso rapido e senza frizioni (es. login social o pagamenti rapidi) per esplorare la città in modo sostenibile. |

#### 2. Operatore del Servizio
Rappresenta l'azienda che immette i mezzi sulla strada. Gestisce il business e la manutenzione.

| Tipologia | Descrizione |
|---|---|
| **Manager del Servizio** | Definisce i piani tariffari, le promozioni e le zone operative per massimizzare il profitto. |
| **Team Logistico e Manutentori** | Personale sul campo che si occupa della ricarica delle batterie, della riparazione dei guasti e dello spostamento fisico dei mezzi nelle zone ad alta richiesta. |

#### 3. Amministrazione Pubblica
Ente che detiene la sovranità sul suolo pubblico e definisce le regole del gioco.

| Tipologia | Descrizione |
|---|---|
| **Pianificatore Urbano / Mobility Manager** | Utilizza i dati della piattaforma per studiare nuovi percorsi ciclabili e gestire le restrizioni al traffico. |
| **Polizia Locale / Corpo di Vigilanza** | Monitora il rispetto delle zone vietate e la corretta gestione dei parcheggi per garantire il decoro urbano. |

---

### 1.4 Item funzionali

Elenco e specifica di tutti i requisiti funzionali espressi attraverso lo schema delle user stories.

#### Utente (UT)

| ID | Titolo | User Story |
|---|---|---|
| **IF-UT.01** | Visualizza Mappa Utente | Come utente, voglio visualizzare la Mappa Utente, così da poter scegliere un mezzo. |
| **IF-UT.02** | Prenota mezzo | Come utente, voglio prenotare un mezzo disponibile, così da trovarlo riservato al mio arrivo. |
| **IF-UT.03** | Annulla Prenotazione | Come utente, voglio annullare una prenotazione attiva prima di raggiungere il mezzo, così da liberare il mezzo se cambio programma. |
| **IF-UT.04** | Sblocca un mezzo | Come utente, voglio sbloccare un mezzo, così da avviare fisicamente la corsa. |
| **IF-UT.05** | Consulta tariffe | Come utente, voglio consultare il tariffario per ciascuna tipologia di mezzo, così da confrontarne i costi. |
| **IF-UT.06** | Termina Corsa | Come utente, voglio terminare la corsa, così da liberare il mezzo. |
| **IF-UT.07** | Visualizza Riepilogo corsa | Come utente, voglio ricevere il riepilogo corsa, così da visualizzare le informazioni sulla corsa effettuata. |
| **IF-UT.08** | Consulta Stato Mezzo | Come utente, voglio consultare lo stato di un mezzo, così da effettuare una scelta in base alle mie esigenze di percorso. |
| **IF-UT.09** | Visualizza Zone | Come utente, voglio visualizzare le zone soggette a restrizioni sulla mappa, così da pianificare il mio percorso nel rispetto delle normative vigenti. |
| **IF-UT.10** | Sospende Corsa | Come utente, voglio mettere in pausa la corsa, così da effettuare soste senza perdere il possesso del mezzo. |
| **IF-UT.11** | Prenota Gruppo | Come utente, voglio effettuare una prenotazione di gruppo fino al numero massimo di mezzi, così da gestire in un'unica operazione la mobilità condivisa con accompagnatori. |
| **IF-UT.12** | Salva Metodi Pagamento | Come utente, voglio salvare uno o più metodi di pagamento, così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati. |
| **IF-UT.13** | Visualizza Promozioni | Come utente, voglio accedere alle promozioni attive, così da ridurre i costi di utilizzo del servizio. |
| **IF-UT.14** | Visualizza Storico Corsa | Come utente, voglio visualizzare lo storico delle corse, così da tenere traccia di tutte le corse effettuate. |
| **IF-UT.15** | Invia Segnalazione | Come utente, voglio inviare una segnalazione, così da informare l'operatore affinché possa intervenire. |
| **IF-UT.16** | Sottoscrive Abbonamento | Come utente, voglio sottoscrivere un abbonamento, così da usufruire di condizioni tariffarie agevolate. |
| **IF-UT.17** | Registra Account | Come utente, voglio registrarmi alla piattaforma, così da poter accedere ai servizi di sharing. |
| **IF-UT.18** | Autentica Account | Come utente, voglio autenticarmi alla piattaforma, così da accedere ai miei dati e alle funzionalità. |
| **IF-UT.19** | Modifica Dati Account | Come utente, voglio modificare i dati del mio profilo, così da mantenere le mie informazioni aggiornate. |

#### Amministrazione Pubblica (AP)

| ID | Titolo | User Story |
|---|---|---|
| **IF-AP.01** | Accede Report | Come amministrazione pubblica, voglio accedere a report aggregati sull'utilizzo del servizio, così da supportare decisioni strategiche di pianificazione. |
| **IF-AP.02** | Definisce Zone Vietate | Come amministrazione pubblica, voglio definire i confini di una Zona Vietata, così da garantire il rispetto delle normative locali. |
| **IF-AP.03** | Definisce Zone Parcheggio | Come amministrazione pubblica, voglio definire zone di parcheggio visibili sulla Mappa Utente, così da ridurre il disordine dei mezzi sulla strada. |
| **IF-AP.04** | Definisce Limite Velocità | Come amministrazione pubblica, voglio definire il limite di velocità applicabile in ciascuna Zona Limitata, così da garantire il rispetto delle normative locali. |
| **IF-AP.05** | Esporta Report | Come amministrazione pubblica, voglio esportare i report aggregati sull'utilizzo del servizio in Formato Esportabile, così da utilizzarli in analisi esterne e documentazione ufficiale. |
| **IF-AP.06** | Modifica Zona | Come amministrazione pubblica, voglio modificare una zona pubblicata in precedenza, così da aggiornare la regolamentazione al variare delle condizioni urbane. |
| **IF-AP.07** | Autentica Account | Come amministrazione pubblica, voglio autenticarmi alla piattaforma con credenziali dedicate, così da accedere alle funzionalità di regolamentazione e ai report. |

#### Operatore (OP)

| ID | Titolo | User Story |
|---|---|---|
| **IF-OP.01** | Visualizza Mappa Operatore | Come operatore, voglio visualizzare la Mappa Operatore, così da pianificare operazioni di redistribuzione. |
| **IF-OP.02** | Gestisce Segnalazioni | Come operatore, voglio leggere le segnalazioni inviate dagli utenti, così da pianificare gli interventi di manutenzione. |
| **IF-OP.03** | Definisce Zona Operativa | Come operatore, voglio definire la Zona Operativa, così da impedire l'allontanamento dei mezzi dall'area di servizio. |
| **IF-OP.04** | Modifica Stato Mezzi | Come operatore, voglio modificare lo Stato di un mezzo, così da nasconderlo o mostrarlo sulla Mappa Utente. |
| **IF-OP.05** | Sospende Account Utente | Come operatore, voglio sospendere l'account di un utente, così da tutelare l'integrità del servizio. |
| **IF-OP.06** | Definisce Offerte Commerciali | Come operatore, voglio definire promozioni con condizioni e scadenza configurabili, così da incentivare l'utilizzo del sistema con politiche commerciali flessibili. |
| **IF-OP.07** | Definisce Tariffa | Come operatore, voglio definire la tariffa del servizio, così da permettere la configurazione del modello di costo. |
| **IF-OP.08** | Modifica Tariffa | Come operatore, voglio modificare una tariffa esistente per una tipologia di mezzo, così da aggiornare il modello di costo. |
| **IF-OP.09** | Configura Durata Prenotazione | Come operatore, voglio configurare la durata massima di una prenotazione, così da liberare i mezzi non utilizzati. |
| **IF-OP.10** | Configura Durata Periodo Grazia | Come operatore, voglio configurare la durata del periodo di grazia per la pausa corsa, così da offrire agli utenti un tempo gratuito. |
| **IF-OP.11** | Configura Numero Massimo Mezzi | Come operatore, voglio configurare il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente, così da abilitare le prenotazioni di gruppo. |
| **IF-OP.12** | Aggiunge Mezzo | Come operatore, voglio aggiungere un nuovo mezzo alla mappa, così da aumentare il numero di mezzi della flotta. |
| **IF-OP.13** | Dismette Mezzo | Come operatore, voglio dismettere un mezzo dalla mappa, così da gestire il ciclo di vita della flotta. |
| **IF-OP.14** | Definisce Regole Fine Corsa | Come operatore, voglio definire regole sanzionatorie per i rilasci dei mezzi al di fuori delle aree di parcheggio consentite, così da garantire il decoro urbano. |
| **IF-OP.15** | Configura Addebito per Pausa Corsa | Come operatore, voglio configurare la politica di addebito durante la pausa corsa al termine del periodo di grazia, così da rendere trasparente e flessibile il pricing della pausa. |
| **IF-OP.16** | Autentica Account Operatore | Come operatore, voglio autenticarmi alla piattaforma, così da accedere alle funzionalità di gestione flotta, tariffe e promozioni. |

---

### 1.5 Item non funzionali

#### 1.5.1 Item Informativi

**IIN-1 — Prestazioni**
- Il sistema deve aggiornare la posizione dei mezzi sulla Mappa Utente entro x secondi dall'ultimo rilevamento GPS *(da testare)*.
- Il sistema deve completare l'operazione di prenotazione di un mezzo entro x secondi dalla richiesta dell'utente *(da testare)*.

**IIN-2 — Sicurezza**
- Tutte le comunicazioni tra client e server devono essere cifrate mediante protocolli di sicurezza standard.
- Il sistema deve bloccare un account dopo 5 tentativi di autenticazione falliti consecutivi in un tempo configurabile dall'operatore.
- I dati personali degli utenti devono essere trattati in conformità al Regolamento UE 2016/679 (GDPR).
- Ciascun ruolo (UT, OP, AP) deve poter accedere esclusivamente alle funzionalità ad esso assegnate.

**IIN-3 — Usabilità**
- L'interfaccia deve essere accessibile secondo le linee guida WCAG (es. per utenti con disabilità visive).
- L'interfaccia deve essere facile da usare e comprensibile in meno di x minuti.

**IIN-4 — Scalabilità**
- L'architettura deve permettere l'aggiunta di nuove tipologie di mezzo senza modifiche strutturali.

**IIN-5 — Portabilità**
- Il sistema deve essere accessibile tramite browser web su dispositivi desktop e mobile, senza necessità di installazione.

**Conformità**
- I report esportabili in CSV/PDF (AP.05) devono rispettare eventuali standard di formato richiesti dalla pubblica amministrazione.

---

#### 1.5.2 Item di interfaccia

**IUI-1 — Schermata di Login Utente**
Design clean su sfondo bianco con logo aziendale in evidenza. Form di accesso con campi arrotondati per Username e Password, link per il recupero credenziali. Due pulsanti principali in verde acqua ("LOGIN" e "SIGN UP") e opzioni di social login rapido (Google e Apple).

**IUI-2 — Homepage Utente**
Interfaccia cartografica principale con top bar per accesso al profilo e menu hamburger. Mappa interattiva con pin codificati per tipologia (monopattini in verde, bici in blu, auto in magenta) e geo-fence evidenziate in rosso. Due pulsanti floating per "CORSA DI GRUPPO" e "SBLOCCA MEZZO". Bottom navigation bar per navigazione rapida.

**IUI-3 — Menu Laterale Utente**
Side drawer a scomparsa da destra con sfondo oscurato. Intestazione con logo e icona di chiusura. Voci di navigazione con icone in verde acqua: Profilo, Impostazioni, Guida, Piano Tariffario, Bonus e Promozioni, Cronologia, Portafoglio.

**IUI-4 — Corsa di Gruppo**
Bottom sheet sovrapposto parzialmente alla mappa. Intestazione con contatore dinamico ("Veicoli sbloccati: 3/5"). Cards per ogni veicolo agganciato con icona, codice identificativo e indicatore batteria. Pulsante "SBLOCCA VEICOLO" per aggiungere ulteriori mezzi.

**IUI-5 — Prenotazione Mezzo**
Bottom sheet con mezzo selezionato evidenziato sulla mappa. Riepilogo dati: tipologia, codice identificativo, stato batteria e avviso sul limite temporale per raggiungere il mezzo. Pulsante "Prenota" per attivare il blocco temporaneo del veicolo.

**IUI-6 — Visualizzazione del Piano Tariffario**
Layout minimale con tre card a pillola per le tariffe chilometriche:
- Monopattino: 0,20 €/km
- Bicicletta: 0,30 €/km
- Automobile: 0,50 €/km

**IUI-7 — Visualizzazione del Saldo e Metodi di Pagamento**
Schermata "Portafoglio" con card in verde acqua per il saldo disponibile. Lista metodi di pagamento: Google Pay, Apple Pay, PayPal, carta di credito. Pulsante "RICARICA SALDO" per il top-up del conto.

**IUI-8 — Schermata Info Corsa**
Cruscotto di monitoraggio attivo con icona del veicolo in uso. Layout tabellare con: ID mezzo, indicatore batteria, timer del tempo trascorso, chilometri percorsi. Pulsanti "PAUSA CORSA" e "TERMINA E PAGA".

**IUI-9 — Visualizzazione della Cronologia Corse**
Lista lineare delle corse con divisori orizzontali. Per ogni corsa: icona del veicolo, ID mezzo, durata, distanza e data.

**IUI-10 — Schermata Login Operatore/Amministrazione Pubblica**
Layout landscape con stessa coerenza visiva del login utente. Form centrato con logo, Username, Password, pulsanti LOGIN/SIGN UP e social login.

**IUI-11 — Dashboard Amministrazione Pubblica**
Layout split-screen: mappa interattiva a sinistra, pannello di controllo a destra. Quattro pulsanti principali: "DEFINISCI ZONE VIETATE", "DEFINISCI ZONE LIMITATE", "DEFINISCI ZONE PARCHEGGIO", "VISUALIZZA REPORT".

**IUI-12 — Definizione Zone Vietate**
Mappa come canvas interattivo: poligono rosso tracciabile tramite nodi. Pannello laterale con istruzioni e toggle per selezionare i tipi di veicolo soggetti al divieto.

**IUI-13 — Definizione Zone Limitate**
Stesso paradigma delle zone vietate, con colore arancione per indicare restrizione parziale. Toggle per selezionare la categoria di mezzo soggetta alla limitazione.

**IUI-14 — Definizione Zone di Parcheggio**
Poligono in verde per indicare area consentita. Toggle per associare il parcheggio a specifiche categorie di veicoli.

**IUI-15 — Visualizzazione dei Report**
Dashboard analitica con:
- Istogramma a barre impilate per i noleggi su base settimanale
- Grafico a torta per la quota di mercato per tipologia di mezzo
- Pulsanti per esportazione in CSV e PDF

**IUI-16 — Dashboard Operatore**
Layout split-screen: mappa con flotta geolocalizzata e controlli per aggiungere/dismettere mezzi a sinistra. Menu verticale a destra con: "Gestisci Segnalazioni", "Gestisci Utenti", "Impostazioni Regole", "Tariffe e Promozioni", "Visualizza Report".

**IUI-17 — Gestione Segnalazioni**
Tabella con colonne: ID utente, timestamp, tipologia di problematica (con icone semantiche), dettaglio testuale. Pulsante "RISPONDI" per la presa in carico di ogni ticket.

**IUI-18 — Gestione Tariffe e Promozioni**
Due card affiancate: a sinistra il pricing con campi di input per le tariffe al chilometro per ogni veicolo; a destra le promozioni attive con pulsante "AGGIUNGI PROMOZIONE".

**IUI-19 — Schermata di Impostazione Regole**
Card con lista di parametri configurabili tramite input numerici: durata massima prenotazione, tolleranza pausa, limite mezzi simultanei per utente, percentuali tariffarie. Dropdown per selezionare la politica sanzionatoria per sosta fuori zona.

---

#### 1.5.3 Item Qualitativi

| ID | Specifica |
|---|---|
| IQ-1 | *(da definire)* |
| IQ-2 | *(da definire)* |
| IQ-n | *(da definire)* |

---

## 2. Sprint Report

### 2.1 Sprint Backlog

Tabella di riepilogo degli item del Product Backlog implementati in ciascuno sprint.

**Assunzioni:**
- All'interno di uno sprint sono implementati un sottoinsieme di item tra quelli specificati nel Product Backlog.
- Gli item funzionali (User Stories) sono tracciabili uno a uno con i casi d'uso.
- Ad ogni caso d'uso è associato uno scenario di base più gli eventuali scenari alternativi.
- Ad ogni caso d'uso è associato un diagramma di sequenza.
- Ogni sprint produce in output codice funzionante. L'unica eccezione è lo Sprint 0, dedicato alla macro-architettura del sistema.

| Codice Item | Numero Sprint | Note |
|---|---|---|
| IF 1 | Sprint 1 | … |

---

### 2.2 Product Requirement Specification

- Diagramma dei Casi d'uso
- Specifiche dei Casi d'uso
- Altro

---

### 2.3 System Architecture

#### 2.3.1 Diagramma delle Componenti

- Diagramma Generale
- Componente Client
- Componente Server
- Servizi Esterni
- Database

#### 2.3.2 Specifica delle componenti

L'architettura portante del sistema segue il modello **Client-Server**, arricchito dall'integrazione del pattern logico **MVC** (Model-View-Controller), da un'estensione su più livelli e dalla comunicazione con servizi esterni.

---

##### Specifica della Componente Client

La componente client è responsabile dell'interfaccia utente. Si occupa di visualizzare i dati e gestire l'interazione con il server.

**View** — Interfacce per le tre tipologie di utenti:
- `VistaUtente`: interfaccia per gli utenti finali.
- `VistaOperatore`: interfaccia per gli operatori che gestiscono la flotta e le zone.
- `VistaAmministrazionePubblica`: interfaccia per gli enti pubblici per supervisione e reporting.

**API Service Layer** — Moduli responsabili della comunicazione con il server:

| Servizio | Responsabilità |
|---|---|
| `ApiService` | Gateway centrale: configura header HTTP, gestisce errori di rete, fornisce metodi GET/POST/PUT/DELETE. |
| `AuthService` | Gestisce login, logout, registrazione. |
| `MapService` | Recupera dati geografici: posizione mezzi, zone, percorsi. Bridge tra client e ServizioGIS. |
| `PaymentService` | Gestisce le chiamate relative a metodi di pagamento e avvio transazioni. |
| `ZonaService` | Recupera e aggiorna le definizioni delle zone geografiche (vietate, limitate, parcheggio). |
| `FlottaService` | Recupera e aggiorna lo stato dei mezzi della flotta. |

---

##### Specifica della Componente Server

La componente server riceve e invia i comandi tramite `ApiService` ed è organizzata su più livelli.

**Controller** — Gestisce il flusso delle richieste HTTP:

| Controller | Responsabilità |
|---|---|
| `UtenteController` | Gestisce le operazioni sull'entità utente. |
| `PrenotazioneUtenteController` | Gestisce le prenotazioni effettuate dagli utenti. |
| `PagamentiController` | Gestisce i pagamenti effettuati dagli utenti. |
| `OperatoreController` | Gestisce le operazioni sull'entità operatore. |
| `MezzoOperatoreController` | Gestisce le operazioni dei mezzi. |
| `ZonaOperatoreController` | Gestisce le operazioni sulle zone geografiche. |
| `PrenotazioneOperatoreController` | Gestisce la visualizzazione delle prenotazioni da parte degli utenti. |
| `AmministrazionePubblicaController` | Gestisce le operazioni dell'ente pubblico. |
| `ZonaAPController` | Gestisce la visualizzazione e supervisione delle zone da parte dell'ente pubblico. |
| `ReportAPController` | Gestisce la generazione e visualizzazione dei report per l'amministrazione pubblica. |

**Business Logic Layer (BLL)** — Logica applicativa del sistema:

| Servizio | Responsabilità |
|---|---|
| `ServizioMobilità` | Orchestrazione principale del servizio di mobilità condivisa. |
| `ServizioGIS` | Gestisce tutte le funzionalità geografiche e di mappatura. |
| `ServizioUtenti` | Gestisce la logica di business relativa agli utenti (registrazione, profilo, ecc.). |
| `ServizioPricing` | Gestisce il calcolo delle tariffe e l'applicazione di promozioni. |
| `ServizioReport` | Gestisce la generazione di report e statistiche. |
| `ServizioPrenotazione` | Gestisce l'intero ciclo di vita di una prenotazione. |

**Model** — Entità del dominio:

| Entità | Descrizione |
|---|---|
| `Utente` | Utente finale del sistema. |
| `Operatore` | Operatore del servizio. |
| `AmministrazionePubblica` | Ente pubblico. |
| `Mezzo` | Veicolo della flotta. |
| `Corsa` | Sessione di utilizzo attivo di un mezzo. |
| `Prenotazione` | Prenotazione di un mezzo. |
| `Zona` | Area geografica del servizio. |
| `Segnalazione` | Segnalazione di problema o anomalia. |
| `Pagamento` | Transazione di pagamento. |
| `Promozione` | Sconto o offerta applicabile. |

**Data Access Layer (DAL)** — Accesso ai dati persistenti:

| Repository | Responsabilità |
|---|---|
| `UtenteRepository` | Accesso ai dati degli utenti. |
| `MezzoRepository` | Accesso ai dati dei mezzi. |
| `CorsaRepository` | Accesso ai dati delle corse. |
| `PagamentoRepository` | Accesso ai dati dei pagamenti. |
| `ZonaRepository` | Accesso ai dati delle zone. |
| `PrenotazioneRepository` | Accesso ai dati delle prenotazioni. |

---

##### Specifica della Componente Servizi Esterni

Il sistema si integra con due servizi esterni:

| Servizio | Utilizzo |
|---|---|
| **BingMaps** | Fornitore di mappe e servizi di geolocalizzazione, utilizzato dal `MapService`. |
| **ProviderPagamenti** | Gateway di pagamento esterno, utilizzato dal `PaymentService`. |

---

#### 2.3.3 Specifica delle interfacce

| Interfaccia | Descrizione |
|---|---|
| `ClientToServer` | Espone le operazioni per l'invio delle richieste dal client verso l'API layer. |
| `ServerToClient` | Espone le operazioni per l'invio dei dati dal server verso il client. |
| `ApiToView` | Permette alle viste di invocare le funzionalità del server in modo astratto, senza occuparsi dei dettagli HTTP. |
| `ControllerToBLL` | Permette ai Controller di invocare i servizi della Business Logic. |
| `BLLToController` | Gestisce la restituzione dei risultati della Business Logic verso il Controller. |
| `BLLToModel` | Utilizzata dalla Business Logic per creare, leggere o aggiornare lo stato delle entità di dominio. |
| `ModelToBLL` | Il Model fornisce i dati strutturati necessari ai servizi della Business Logic. |
| `ModelToDAL` | Passaggio degli oggetti di dominio al Data Access Layer per le operazioni di persistenza. |
| `DALToDBMS` | Interfaccia di basso livello per l'esecuzione di query e transazioni sul database. |
| `ServiziEsterni` | Espone le interfacce per l'interazione con fornitori terzi (pagamenti e servizi cartografici). |

---

### 2.4 Detailed Product Design

- Diagramma delle Classi
- Specifiche delle Classi
- Diagrammi di Sequenza

---

### 2.5 Data Modeling and Design

- Modello logico del Database
- Struttura fisica del Database

---

## 3. Prompt

### 3.1 Qualità dei requisiti

La seguente sezione riporta il prompt utilizzato per la convalidazione della qualità delle user story secondo le 14 caratteristiche di qualità definite nel corso.

---

**Prompt utilizzato:**

> You are a software engineer, specialized in requirements elicitation. In this phase, you need to read the User Stories. You need to read them carefully, evaluate them following the "Quality Verification Characteristics" listed below.
>
> **Context:** The municipality of Zootropolis wishes to introduce a sustainable transport system that integrates various sharing services (e.g., Bike, Car, E-scooter sharing). The system must operate in an urban environment involving Users, Operators, and Public authorities.
>
> **Expected Input Format:** The user stories are in the form:
> `COME [ruolo] VOGLIO [fare qualcosa] COSÌ CHE [possa ottenere valore per il business]`

Le 14 caratteristiche di qualità valutate:

| # | Caratteristica | Descrizione |
|---|---|---|
| 1 | **Non Ambiguo** | Deve esserci un solo modo di interpretare ogni requisito. Evitare acronimi non espansi, termini vaghi ed eccessiva sintesi. |
| 2 | **Provabile o Verificabile** | Deve essere possibile costruire casi di test corretti e non corretti. Evitare aggettivi/avverbi generici, pronomi indefiniti e voci passive. |
| 3 | **Chiaro** | Il requisito deve essere conciso, laconico, semplice e preciso. Nessuna verbosità o informazione non necessaria. |
| 4 | **Corretto** | Se un requisito contiene fatti, questi devono essere veri. |
| 5 | **Comprensibile** | Grammaticalmente corretto, stile consistente, con standard terminologici. Usare "deve" al posto di "volere", "bisogna" o "può". |
| 6 | **Fattibile** | I requisiti devono essere realizzabili entro i vincoli esistenti di tempo, denaro e risorse. |
| 7 | **Indipendente e Auto-consistente** | Per comprendere un requisito non deve essere necessario conoscere nessun altro requisito. |
| 8 | **Atomico** | Ogni requisito deve contenere un solo elemento tracciabile. Le espressioni con "e" o "ma" devono essere suddivise. |
| 9 | **Necessario** | Un requisito è inutile se nessuna parte interessata ne ha bisogno o se la sua cancellazione non ha conseguenze sul sistema finale. |
| 10 | **Astratto** | I requisiti non devono contenere dettagli circa la loro implementazione, salvo vincoli espliciti dell'utente. |
| 11 | **Consistente** | Tutti i requisiti devono utilizzare termini uguali per concetti uguali, e nessun requisito deve essere conflittuale con altri. |
| 12 | **Non Ridondante** | Ogni requisito deve essere espresso una sola volta e non deve sovrapporsi a un altro. |
| 13 | **Completo** | Un requisito deve essere specificato per tutte le condizioni che possono verificarsi. |
| 14 | **Metriche Derivate** | Manutenibilità e tracciabilità garantite dall'atomicità e dall'identificatore univoco di ciascun requisito. |

---

### 3.2 Output Prompt

| Caratteristica | Score | Motivazione |
|---|---|---|
| Non Ambiguo | 5 | Grazie all'uso del glossario e alla rimozione di avverbi vaghi, ogni requisito ha un'unica interpretazione possibile. |
| Provabile o Verificabile | 5 | La separazione dei requisiti e l'uso di termini precisi permettono di costruire test case binari (Pass/Fail) per ogni singola funzionalità. |
| Chiaro | 5 | Le User Story sono concise, laconiche e prive di verbosità, rispettando perfettamente il formato standard. |
| Corretto | 5 | I requisiti rappresentano fedelmente le necessità del business e i vincoli normativi espressi nel contesto di Zootropolis. |
| Comprensibile | 5 | Lo stile è consistente, grammaticalmente corretto e utilizza i termini definiti nel glossario in modo impeccabile. |
| Fattibile | 5 | Tutte le funzionalità (gestione mappe, sblocco, pagamenti) sono realizzabili con le tecnologie attuali entro i vincoli di progetto. |
| Indipendente e Auto-consistente | 5 | Ogni requisito è comprensibile senza dover fare riferimento ad altri item, garantendo la massima modularità. |
| Atomico | 5 | Ogni User Story contiene ora un solo elemento tracciabile. Abbonamenti, bonus e diverse tipologie di zone sono gestiti separatamente. |
| Necessario | 5 | La clausola "Così da" giustifica ogni funzione in base al valore reale per cittadini, operatori o amministrazione. |
| Astratto | 5 | I requisiti non contengono dettagli implementativi superflui, lasciando libertà ai progettisti (es. metodo di sblocco QR/NFC). |
| Consistente | 5 | Non vi sono conflitti tra i requisiti; le regole di precedenza tra zone AP e zone OP sono chiaramente stabilite. |
| Non Ridondante | 5 | Ogni funzionalità è espressa una sola volta e non vi sono sovrapposizioni tra i diversi ruoli utente. |
| Completo | 5 | La scomposizione dei requisiti ha permesso di coprire anche i flussi e le condizioni specifiche per ogni diversa entità del sistema. |
| Metriche Derivate | 5 | L'elevata atomicità garantisce una manutenibilità eccellente e una tracciabilità precisa lungo tutto il ciclo di vita. |
| **Media** | **5.0** | |

---

### 3.3 Definizioni

Vedere la sezione [Glossario](#4-glossario).

---

## 4. Glossario

### 4.1 Acronimi

| Acronimo | Espansione |
|---|---|
| AP | Amministrazione Pubblica |
| API | Application Programming Interface |
| BLL | Business Logic Layer |
| CSV | Comma-Separated Values |
| DAL | Data Access Layer |
| DBMS | Database Management System |
| GIS | Geographic Information System |
| HTTP | HyperText Transfer Protocol |
| NFC | Near Field Communication |
| OP | Operatore del Servizio |
| PDF | Portable Document Format |
| QR | Quick Response (code) |
| UT | Utente |

---

### 4.2 Definizioni

**Account utente**
Insieme di credenziali, dati anagrafici, metodi di pagamento, e-mail, password e storico associati a un utente registrato. Il profilo personale è la vista utente dell'account.

**Addebito**
Importo economico calcolato al termine di una corsa o di un evento tariffabile e prelevato dal metodo di pagamento associato all'account utente.

**Amministrazione Pubblica**
Ente locale (comune o equivalente) che regolamenta l'uso dello spazio urbano e definisce vincoli e agevolazioni per il servizio di sharing. Nel sistema è un ruolo distinto da Utente e Operatore.

**Autonomia residua**
Valore numerico indicante la carica rimasta nella batteria di un mezzo elettrico (e-bike, e-scooter). Espresso in percentuale (%) o in chilometri stimati; l'unità di misura adottata è configurabile dalla piattaforma.

**Corsa / Sessione**
Sessione di utilizzo attivo di un mezzo sharing, che inizia con lo sblocco del veicolo e termina con la chiusura della sessione da parte dell'utente. Al termine viene calcolato e addebitato il costo.

**Fine corsa**
Evento che conclude una corsa; l'esito (valido, penalizzato, rifiutato) dipende dalla posizione del mezzo rispetto alla Zona Operativa e alla Zona di parcheggio.

**Formato Esportabile**
Formattazione offerta dalla piattaforma per l'esportazione dei dati. Include CSV e PDF.

**Flotta**
Insieme di tutti i mezzi gestiti da un operatore nell'ambito del servizio di sharing su un determinato territorio.

**Mappa Operatore**
Visualizzazione cartografica accessibile agli operatori, che mostra la posizione e lo stato di tutti i mezzi della flotta negli ultimi x minuti, inclusi quelli nascosti alla Mappa Utente.

**Mappa Utente**
Visualizzazione cartografica accessibile agli utenti, che mostra i mezzi disponibili e prenotabili nelle vicinanze, le zone con vincoli di circolazione o parcheggio. Non mostra i mezzi rimossi dall'operatore.

**Metodo di pagamento**
Strumento associato all'account utente (carta, wallet, ecc.) utilizzato per regolare gli addebiti.

**Mezzo**
Qualsiasi veicolo messo a disposizione degli utenti: bicicletta tradizionale, bicicletta a pedalata assistita (e-bike), monopattino elettrico (e-scooter) e macchina elettrica.

**Mezzo disponibile**
Mezzo il cui stato è *Disponibile*, ossia prenotabile da un utente. Gli unici visualizzabili nella Mappa Utente.

**Operatore del Servizio**
Soggetto (azienda privata o consorzio) responsabile della gestione operativa della flotta e della configurazione della piattaforma.

**Pausa corsa**
Stato intermedio di una sessione in cui l'utente blocca temporaneamente il mezzo senza terminare la corsa.

**Periodo di grazia**
Durata massima configurabile dall'operatore entro cui una pausa corsa non comporta addebiti aggiuntivi o la perdita del mezzo. Se impostato a zero, la funzionalità di pausa gratuita è disabilitata.

**Prenotazione**
Riserva temporanea di un mezzo specifico effettuata dall'utente prima di raggiungerne fisicamente la posizione. Ha una durata massima configurabile dall'operatore; alla scadenza il mezzo viene automaticamente rilasciato.

**Prenotazione di gruppo**
Prenotazione effettuata da un singolo utente per un numero di mezzi fino al massimo configurato dall'operatore.

**Promozione**
Offerta che riduce la tariffa standard o offre condizioni speciali (es. prime N corse gratis, sconto percentuale). Configurata e pubblicata dall'operatore.

**Abbonamento**
Contratto a tempo determinato (es. mensile, annuale) che garantisce all'utente condizioni tariffarie agevolate o un numero di corse incluse. Configurato e pubblicato dall'operatore.

**Bonus**
Valore monetario assegnato all'utente dall'operatore secondo certe condizioni (es. parcheggio corretto, alto numero di corse). Se impostato a zero, la funzionalità non è visualizzabile dall'utente.

**Redistribuzione**
Operazione logistica di spostamento fisico dei mezzi da aree con eccesso di offerta verso aree con carenza, eseguita dal personale operativo.

**Report aggregato**
Documento che consolida statistiche anonime sull'utilizzo del servizio su un intervallo temporale configurabile. Destinato all'operatore e all'amministrazione pubblica.

**Riepilogo corsa**
Sintesi presentata all'utente al termine di una corsa: durata complessiva, distanza percorsa, costo finale ed eventuali sconti o bonus. Disponibile anche nello storico corse.

**Sblocco**
Operazione che disabilita il blocco fisico/elettronico del mezzo, consentendo all'utente di iniziare la corsa. Il metodo di sblocco (QR code, Bluetooth, NFC) è una scelta implementativa.

**Segnalazione**
Comunicazione inviata dall'utente all'operatore per notificare anomalie su un mezzo (danno fisico, guasto, posizione anomala). Visibile nella dashboard operatore.

**Stato (mezzo)**
Condizione operativa corrente di un mezzo.

| Stato | Descrizione |
|---|---|
| Disponibile | Prenotabile da un utente. |
| Prenotato | Riservato a un utente. |
| In uso | Corsa attiva. |
| In pausa | Pausa corsa attiva. |
| In manutenzione | Rimosso dalla Mappa Utente. |
| Fuori servizio | Bloccato o irrecuperabile. |

**Storico corsa**
L'insieme delle corse effettuate da un utente.

**Tariffa**
Struttura di pricing applicata a una corsa. La tipologia (es. costo al minuto, alla distanza, tariffa fissa per fascia oraria) è definita e modificabile dall'operatore.

**Tariffario**
Elenco pubblicato dall'operatore delle tariffe applicate per ciascuna tipologia di mezzo e modalità di utilizzo.

**Utente**
Persona fisica registrata alla piattaforma che utilizza i mezzi di sharing per spostarsi nel contesto urbano. Interagisce con il sistema tramite dispositivo mobile.

**Zone**

| Zona | Descrizione |
|---|---|
| **Zona Operativa** | Perimetro geografico definito dall'operatore entro cui i mezzi possono circolare. Le zone AP hanno sempre la precedenza. |
| **Zona di parcheggio** | Area designata dall'amministrazione pubblica in cui è consigliato parcheggiare il mezzo. L'operatore può associarvi un bonus economico. |
| **Zona Limitata** | Area in cui la circolazione è consentita ma con restrizioni configurabili (es. velocità ridotta). Configurata dall'AP. |
| **Zona Vietata** | Area in cui la circolazione è completamente vietata. Definita dall'AP, ha precedenza sulla Zona Operativa dell'operatore. |
