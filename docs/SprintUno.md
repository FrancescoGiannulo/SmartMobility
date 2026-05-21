# SMART MOBILITY — Contesto di Progetto per Agente AI
> **Documento**: Sprint Report N.1 — Ciclo 4  
> **Versione**: 2.0 | **Data di rilascio**: 26/05/2026  
> **Corso**: Ingegneria del Software a.a. 2025-2026 — Informatica e Tecnologie per la Produzione del Software (ITPS)  
> **Team**: Cardone Flavio (829469), De Astis Gabriele (826243), Giannulo Francesco (825071), Lacirignola Camilla (830465)

---

## 1. INTRODUZIONE AL SISTEMA

**SMART MOBILITY** è un sistema software progettato per il Comune di **Zootropolis** per introdurre un servizio integrato di mobilità urbana sostenibile. Unifica in un'unica piattaforma diversi servizi di sharing: bike sharing, car sharing, e-scooter sharing e altri.

### Obiettivi macroscopici

1. Offrire ai **cittadini (Utenti)** un accesso rapido, sicuro e trasparente ai mezzi di sharing disponibili sul territorio.
2. Permettere agli **Operatori del Servizio** di gestire in modo efficiente la flotta, ridurre costi e fenomeni di vandalismo.
3. Consentire all'**Amministrazione Pubblica (AP)** di monitorare la mobilità urbana e assumere decisioni strategiche basate su dati.

### Funzionalità per categoria di utente

**Per gli Utenti:**
- Visualizzazione dei mezzi disponibili nelle vicinanze e del loro stato
- Prenotazione di uno o più mezzi e sblocco tramite dispositivo personale
- Pagamenti veloci e sicuri con addebito automatico
- Promozioni, pausa della corsa e gestione del profilo di pagamento

**Per gli Operatori:**
- Visualizzazione della distribuzione della flotta con notifiche su aree a bassa disponibilità
- Monitoraggio di malfunzionamenti, manutenzione e posizione dei mezzi a fine corsa
- Bonus per parcheggio corretto, sospensione account in caso di frode, blocco automatico dei mezzi fuori zone consentite

**Per l'Amministrazione Pubblica:**
- Monitoraggio della frequenza di utilizzo e dei pattern di mobilità urbana
- Accesso a report aggregati per decisioni strategiche
- Analisi dello stato dei mezzi e delle tratte più utilizzate
- Selezione di zone sensibili con divieto o limitazione del transito

---

## 2. CONTESTO DI BUSINESS

Il sistema opera nei seguenti ambiti:

- **Mobilità cittadini**: piattaforma unificata per localizzare, prenotare e pagare diversi tipi di mezzi (bici, monopattini, auto elettriche) tramite un'unica interfaccia, con incentivi per comportamenti virtuosi.
- **Gestione operativa della flotta**: monitoraggio costante, gestione zone operative, ottimizzazione flussi di ridistribuzione, riduzione costi di recupero.
- **Governance pubblica**: dashboard per definire zone vietate, zone a velocità limitata e aree di parcheggio; raccolta dati granulari sui flussi di traffico.
- **Sostenibilità ambientale**: statistiche aggregate sui km percorsi con mezzi elettrici e sul risparmio di emissioni CO2.

---

## 3. STAKEHOLDER

### 3.1 Utente
Persona fisica registrata che usa i mezzi di sharing. Deve essere registrata per usare la mappa, localizzare mezzi, noleggiare e pagare.

- **Pendolare Urbano**: usa regolarmente il servizio per l'ultimo miglio; cerca affidabilità e abbonamenti convenienti.
- **Utente Occasionale**: usa il servizio saltuariamente per necessità impreviste o svago.
- **Turista**: necessita di accesso rapido senza frizioni (social login, pagamenti rapidi).

### 3.2 Operatore del Servizio
Azienda che immette i mezzi in strada, gestisce il business e la manutenzione.

- **Manager del Servizio**: definisce piani tariffari, promozioni e zone operative.
- **Team Logistico e Manutentori**: personale sul campo per ricarica, riparazione e redistribuzione fisica dei mezzi.

### 3.3 Amministrazione Pubblica
Ente con sovranità sul suolo pubblico che definisce le regole del servizio.

- **Pianificatore Urbano / Mobility Manager**: usa i dati per pianificare percorsi ciclabili e gestire restrizioni al traffico.
- **Polizia Locale / Corpo di Vigilanza**: monitora rispetto delle zone vietate e correttezza dei parcheggi.

---

## 4. PRODUCT BACKLOG — ITEM FUNZIONALI

### 4.1 Item Funzionali Utente (IF-UT)

| Codice | Nome | User Story |
|--------|------|------------|
| IF-UT.01 | Visualizza Mappa Utente | Come utente, voglio visualizzare la Mappa Utente, così da poter scegliere un mezzo. |
| IF-UT.02 | Prenota mezzo | Come utente, voglio prenotare un mezzo disponibile, così da trovarlo riservato al mio arrivo. |
| IF-UT.03 | Annulla Prenotazione | Come utente, voglio annullare una prenotazione attiva prima di raggiungere il mezzo, così da liberare il mezzo se cambio programma. |
| IF-UT.04 | Sblocca un mezzo | Come utente, voglio sbloccare un mezzo, così da avviare fisicamente la corsa. |
| IF-UT.05 | Consulta tariffe | Come utente, voglio consultare il tariffario per ciascuna tipologia di mezzo, così da confrontarne i costi. |
| IF-UT.06 | Termina Corsa | Come utente, voglio terminare la corsa, così da liberare il mezzo. |
| IF-UT.07 | Visualizza Riepilogo corsa | Come utente, voglio ricevere il riepilogo corsa, così da visualizzare le informazioni sulla corsa effettuata. |
| IF-UT.08 | Consulta Stato Mezzo | Come utente, voglio consultare lo stato di un mezzo, così da effettuare una scelta in base alle mie esigenze di percorso. |
| IF-UT.09 | Visualizza Zone | Come utente, voglio visualizzare le zone soggette a restrizioni sulla mappa, così da pianificare il mio percorso nel rispetto delle normative vigenti. |
| IF-UT.10 | Sospende Corsa | Come utente, voglio mettere in pausa la corsa, così da effettuare soste senza perdere il possesso del mezzo. |
| IF-UT.11 | Prenota Gruppo | Come utente, voglio effettuare una prenotazione di gruppo fino al numero massimo di mezzi, così da gestire in un'unica operazione la mobilità condivisa con accompagnatori. |
| IF-UT.12 | Salva Metodi Pagamento | Come utente, voglio salvare uno o più metodi di pagamento, così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati. |
| IF-UT.13 | Visualizza Promozioni | Come utente, voglio accedere alle promozioni attive, così da ridurre i costi di utilizzo del servizio. |
| IF-UT.14 | Visualizza Storico Corsa | Come utente, voglio visualizzare lo storico delle corse, così da tenere traccia di tutte le corse effettuate. |
| IF-UT.15 | Invia Segnalazione | Come utente, voglio inviare una segnalazione, così da informare l'operatore affinché possa intervenire. |
| IF-UT.16 | Sottoscrive Abbonamento | Come utente, voglio sottoscrivere un abbonamento, così da usufruire di condizioni tariffarie agevolate. |
| IF-UT.17 | Registra Account | (user story implicita dal backlog) |
| IF-UT.18 | Autentica Account | (user story implicita dal backlog) |
| IF-UT.19 | Modifica Dati Account | (user story implicita dal backlog) |
| IF-UT.20 | Effettua Pagamento | Come utente, voglio che il sistema addebiti automaticamente l'importo sul mio metodo di pagamento predefinito al termine della corsa, così da non dover effettuare transazioni manuali ogni volta che scendo dal mezzo. |
| IF-UT.21 | Imposta Metodo di Pagamento predefinito | (user story implicita dal backlog) |

### 4.2 Item Funzionali Amministrazione Pubblica (IF-AP)

| Codice | Nome | User Story |
|--------|------|------------|
| IF-AP.01 | Accede Report | Come amministrazione pubblica, voglio accedere a report aggregati sull'utilizzo del servizio, così da supportare decisioni strategiche di pianificazione. |
| IF-AP.02 | Esporta Report | Come amministrazione pubblica, voglio esportare i report aggregati in Formato Esportabile, così da utilizzarli in analisi esterne e documentazione ufficiale. |
| IF-AP.03 | Visualizza Mappa Amministrazione Pubblica | Come amministrazione pubblica, voglio visualizzare la mappa, così da monitorare il servizio sulla città. |
| IF-AP.04 | Definisce Limite Velocità | Come operatore, voglio definire il limite di velocità applicabile in ciascuna Zona Limitata, così da garantire il rispetto delle normative locali. |
| IF-AP.07 | Autentica Account AP | (user story implicita dal backlog) |
| IF-AP.08 | Visualizza Mappa Amministrazione Pubblica | (user story implicita dal backlog) |

### 4.3 Item Funzionali Operatore (IF-OP)

| Codice | Nome | User Story |
|--------|------|------------|
| IF-OP.01 | Visualizza Mappa Operatore | Come operatore, voglio visualizzare la Mappa Operatore, così da pianificare operazioni di redistribuzione. |
| IF-OP.02 | Gestisce Segnalazioni | Come operatore, voglio leggere le segnalazioni inviate dagli utenti, così da pianificare gli interventi di manutenzione. |
| IF-OP.02b | Definisce Zone Vietate | Come operatore, voglio definire i confini di una Zona Vietata, così da garantire il rispetto delle normative locali. |
| IF-OP.03 | Definisce Confine Operativo | Come operatore, voglio definire il confine operativo, così da circoscrivere la zona percorribile dai mezzi. |
| IF-OP.03b | Definisce Zone Parcheggio | Come operatore, voglio definire zone di parcheggio visibili sulla Mappa Utente, così da ridurre il disordine dei mezzi sulla strada. |
| IF-OP.04 | Modifica Stato Mezzo | Come operatore, voglio modificare lo Stato di un mezzo, così da nasconderlo o mostrarlo sulla Mappa Utente. |
| IF-OP.05 | Sospende Account Utente | Come operatore, voglio sospendere l'account di un utente, così da tutelare l'integrità del servizio. |
| IF-OP.06 | Definisce Offerte Commerciali | Come operatore, voglio definire promozioni con condizioni e scadenza configurabili, così da incentivare l'utilizzo del sistema con politiche commerciali flessibili. |
| IF-OP.07 | Definisce Tariffa | Come operatore, voglio definire la tariffa del servizio, così da permettere la configurazione del modello di costo. |
| IF-OP.08 | Modifica Tariffa | (user story implicita dal backlog) |
| IF-OP.09 | Configura Durata Prenotazione | Come operatore, voglio configurare la durata massima di una prenotazione, così da liberare i mezzi non utilizzati. |
| IF-OP.10 | Configura Durata Periodo Grazia | Come operatore, voglio configurare la durata del periodo di grazia per la pausa corsa, così da offrire agli utenti un tempo gratuito. |
| IF-OP.11 | Configura Numero Massimo Mezzi | Come operatore, voglio configurare il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente, così da abilitare le prenotazioni di gruppo. |
| IF-OP.12 | Aggiunge Mezzo | Come operatore, voglio aggiungere un nuovo mezzo alla mappa, così da aumentare il numero di mezzi della flotta. |
| IF-OP.13 | Dismette Mezzo | Come operatore, voglio dismettere un mezzo dalla mappa, così da gestire il ciclo di vita della flotta. |
| IF-OP.14 | Definisce Regole Fine Corsa | Come operatore, voglio definire regole sanzionatorie per i rilasci dei mezzi al di fuori delle aree di parcheggio consentite, così da garantire il decoro urbano. |
| IF-OP.15 | Configura Addebito per Pausa Corsa | Come operatore, voglio configurare la politica di addebito durante la pausa corsa al termine del periodo di grazia, così da rendere trasparente e flessibile il pricing della pausa. |
| IF-OP.16 | Autentica Account Operatore | (user story implicita dal backlog) |

---

## 5. PRODUCT BACKLOG — ITEM NON FUNZIONALI

### 5.1 Item Informativi

**IIN-1 Prestazioni**
- Il sistema deve aggiornare la posizione dei mezzi sulla Mappa Utente entro x secondi dall'ultimo rilevamento GPS (da testare).
- Il sistema deve completare l'operazione di prenotazione di un mezzo entro x secondi dalla richiesta dell'utente (da testare).

**IIN-2 Sicurezza**
- Tutte le comunicazioni tra client e server devono essere cifrate mediante protocolli di sicurezza standard.
- Il sistema deve bloccare un account dopo 5 tentativi di autenticazione falliti consecutivi in un tempo configurabile dall'operatore.
- I dati personali degli utenti devono essere trattati in conformità al Regolamento UE 2016/679 (GDPR).
- Ciascun ruolo (UT, OP, AP) deve poter accedere esclusivamente alle funzionalità ad esso assegnate.

**IIN-3 Usabilità**
- L'interfaccia deve essere accessibile secondo le linee guida WCAG (es. per utenti con disabilità visive).
- L'interfaccia deve essere facile da usare e comprensibile in meno di x minuti.

**IIN-4 Scalabilità**
- L'architettura deve permettere l'aggiunta di nuove tipologie di mezzo senza modifiche strutturali.

**IIN-5 Portabilità**
- Il sistema deve essere accessibile tramite browser web su dispositivi desktop e mobile, senza necessità di installazione.

**Conformità**
- I report esportabili in CSV/PDF devono rispettare eventuali standard di formato richiesti dalla pubblica amministrazione.

### 5.2 Item di Interfaccia (Mockup)

| Codice | Nome | Descrizione |
|--------|------|-------------|
| IUI-1 | Schermata di Login Utente | Design clean su sfondo bianco. Logo del sistema in alto. Form con campi Username e Password arrotondati, link recupero credenziali. CTA: pulsanti "LOGIN" e "SIGN UP" in verde acqua. Social login rapido (Google e Apple) in basso. |
| IUI-2 | Homepage Utente | Interfaccia cartografica principale. Top bar con accesso profilo e menu hamburger. Mappa interattiva con pin codificati per colore/icona (monopattini verde, bici blu, auto magenta). Geo-fence per zone in rosso. Pulsanti floating "CORSA DI GRUPPO" e "SBLOCCA MEZZO". Bottom navigation bar. |
| IUI-3 | Menu Laterale Utente | Side drawer a scomparsa da destra. Logo + icona "X" di chiusura. Voci: Profilo, Impostazioni, Guida, Piano Tariffario, Bonus e Promozioni, Cronologia, Portafoglio. Icone vettoriali in verde acqua aziendale. |
| IUI-4 | Corsa di Gruppo | Bottom sheet sovrapposto alla mappa. Intestazione "Inizia corsa di gruppo" con contatore dinamico (es. "Veicoli sbloccati: 3/5"). Cards per ogni veicolo con icona, codice ID e indicatore batteria. CTA "SBLOCCA VEICOLO". |
| IUI-5 | Prenotazione Mezzo | Bottom sheet con pin verde ingrandito sulla mappa. Dati: tipologia, codice ID, batteria. Avviso limite temporale per raggiungere il mezzo. CTA "Prenota". |
| IUI-6 | Visualizzazione Piano Tariffario | Layout minimale con 3 card a pillola. Tariffe indicative: Monopattino 0,20€/km, Bicicletta 0,30€/km, Automobile 0,50€/km. Bottom navigation bar. |
| IUI-7 | Saldo e Metodi di Pagamento | Card in verde acqua con saldo disponibile. Lista metodi di pagamento (Google Pay, Apple Pay, PayPal, carte di credito) con chevron. CTA "RICARICA SALDO". |
| IUI-8 | Schermata Info Corsa | Cruscotto di monitoraggio durante il noleggio. Icona veicolo in uso. Tabella: ID mezzo, batteria, timer, km percorsi. CTA "PAUSA CORSA" e "TERMINA E PAGA". |
| IUI-9 | Cronologia Corse | Lista lineare con divisori orizzontali. Per ogni corsa: icona veicolo, ID mezzo, durata, distanza, data. |
| IUI-10 | Login Operatore/AP | Layout landscape (orizzontale). Stessa struttura del login utente: logo, form Username/Password, pulsanti LOGIN e SIGN UP, social login. |
| IUI-11 | Dashboard Amministrazione Pubblica | Layout landscape split-screen. Sinistra: mappa interattiva (Google Maps). Destra: pulsanti "DEFINISCI ZONE VIETATE", "DEFINISCI ZONE LIMITATE", "DEFINISCI ZONE PARCHEGGIO", "VISUALIZZA REPORT". |
| IUI-12 | Definizione Zone Vietate | Mappa come canvas interattivo per tracciare poligoni rossi. Pannello laterale con istruzioni. Toggle per selezionare a quali veicoli applicare il divieto. |
| IUI-13 | Definizione Zone Limitate | Stessa interazione di IUI-12. Colore arancione per restrizione parziale. Toggle per categoria di mezzo. |
| IUI-14 | Definizione Zone di Parcheggio | Stessa interazione di IUI-12. Colore verde per area consentita. Toggle per categoria di mezzo. |
| IUI-15 | Visualizzazione dei Report | Dashboard analitica. Istogramma a barre impilate (noleggi settimanali) + grafico a torta (quota per tipologia mezzo). Pulsanti esportazione CSV e PDF. |
| IUI-16 | Dashboard Operatore | Layout split-screen landscape. Sinistra: Mappa Operatore con pin cromatici flotta. Floating buttons: "AGGIUNGI MEZZO" e "DISMETTI MEZZO". Destra: pulsanti "GESTISCI SEGNALAZIONI", "GESTISCI UTENTI", "IMPOSTAZIONI REGOLE", "TARIFFE E PROMOZIONI", "VISUALIZZA REPORT", "GESTISCI MEZZI". |
| IUI-17 | Gestione Segnalazioni | Layout tabellare (data grid). Colonne: ID utente, timestamp, tipologia problematica (icone semantiche), dettaglio testuale. CTA "RISPONDI" per ogni riga. |
| IUI-18 | Gestione Tariffe e Promozioni | Due card affiancate. Sinistra: tariffe per tipologia mezzo con campo editabile e selettore unità (es. €/km). Destra: promozione attiva in pillola verde acqua + CTA "AGGIUNGI PROMOZIONE". |
| IUI-19 | Impostazione Regole | Card a lista con parametri configurabili: durata massima prenotazione, tolleranza pausa, limite prenotazioni simultanee per utente, percentuali tariffarie. Dropdown per politica sanzionatoria sosta fuori zona (penale / divieto / avviso). |

---

## 6. SPRINT BACKLOG — SPRINT N.1

Gli item implementati nel presente sprint sono i seguenti:

| Codice Item | Nome | Note |
|-------------|------|------|
| UT.01 | Visualizza Mappa Utente | Sprint 1 |
| UT.02 | Prenota mezzo | Sprint 1 |
| UT.04 | Sblocca un mezzo | Sprint 1 |
| UT.06 | Termina Corsa | Sprint 1 |
| UT.12 | Salva metodi di pagamento | Sprint 1 |
| UT.17 | Registra account | Sprint 1 |
| UT.18 | Autentica account utente | Sprint 1 |
| UT.19 | Modifica dati account | Sprint 1 |
| UT.20 | Effettua Pagamento | Sprint 1 |
| UT.21 | Imposta Metodo di Pagamento Predefinito | Sprint 1 |
| AP.07 | Autentica Account AP | Sprint 1 |
| AP.02 | Definisce zone vietate | Sprint 1 |
| AP.03 | Definisce zone parcheggio | Sprint 1 |
| AP.08 | Visualizza mappa Amministrazione Pubblica | Sprint 1 |
| OP.01 | Visualizza Mappa Operatore | Sprint 1 |
| OP.03 | Definisce zone operative | Sprint 1 |
| OP.07 | Definisce tariffe | Sprint 1 |
| OP.04 | Modifica stato mezzo | Sprint 1 |
| OP.08 | Modifica tariffe | Sprint 1 |
| OP.16 | Autentica account operatore | Sprint 1 |
| OP.12 | Aggiungi un mezzo | Sprint 1 |
| OP.13 | Dismetti un mezzo | Sprint 1 |
| OP.14 | Definisci regole fine corsa | Sprint 1 |

---

## 7. SPECIFICHE DEI CASI D'USO

### CS-01 — Visualizza Mappa Utente (UT.01)

- **Attori Primari**: Utente
- **Attori Secondari**: ServizioGIS
- **Precondizioni**: L'utente è autenticato alla piattaforma.
- **Sequenza principale**:
  1. L'utente accede alla schermata principale.
  2. Il sistema rileva la posizione geografica corrente tramite il dispositivo.
  3. Il sistema interroga il ServizioGIS per recuperare i dati geografici.
  4. Il sistema recupera le zone con restrizioni e le zone di parcheggio.
  5. Il sistema visualizza la mappa con i soli mezzi disponibili per tipologia, le aree con restrizioni, le zone di parcheggio e il marker della posizione corrente.
- **Post-condizioni**: La mappa è visualizzata con dati aggiornati; l'utente può procedere con prenotazione o sblocco di un mezzo.
- **Sequenze alternative**: Nessuna.

---

### CS-02 — Visualizza Mappa Operatore (OP.01)

- **Attori Primari**: Operatore
- **Attori Secondari**: ServizioGIS
- **Precondizioni**: L'operatore è autenticato alla piattaforma.
- **Sequenza principale**:
  1. L'operatore accede alla schermata principale.
  2. Il sistema rileva la posizione geografica corrente tramite il dispositivo.
  3. Il sistema interroga il ServizioGIS per recuperare i dati geografici.
  4. Il sistema recupera le zone con restrizioni, le zone di parcheggio e lo stato aggiornato di tutti i mezzi della flotta.
  5. Il sistema visualizza la mappa con tutti i mezzi (indipendentemente dallo stato), lo stato di ciascuno, le aree con restrizioni e il marker della posizione corrente.
- **Post-condizioni**: La mappa è visualizzata con dati aggiornati sull'intera flotta; l'operatore può pianificare operazioni di redistribuzione o manutenzione.
- **Sequenze alternative**: Nessuna.

---

### CS-03 — Definisci Zona (AP.02, AP.03, OP.03)

- **Attori Primari**: Operatore (o AP con ruolo appropriato)
- **Attori Secondari**: Nessuno
- **Precondizioni**: L'attore è autenticato con il ruolo appropriato nel sistema.
- **Sequenza principale**:
  1. L'attore intende definire una zona caratteristica.
  2. Il sistema visualizza la mappa interattiva con le zone esistenti.
  3. L'attore disegna il perimetro della zona sulla mappa definendo i vertici del poligono.
  4. L'attore conferma la creazione della zona.
  5. Fintantoché il perimetro non è valido: il sistema notifica il problema; l'attore corregge il perimetro (torna al passo 3).
  6. Il sistema salva la Zona e la rende attiva.
  7. Il sistema aggiorna la mappa visibile agli utenti evidenziando la nuova zona.
- **Post-condizioni**: La nuova Zona è persistita nel sistema con il perimetro definito; il sistema la applica alla flotta.
- **Sequenze alternative**: Nessuna.

---

### CS-05 — Prenota Mezzo (UT.02)

- **Attori Primari**: Utente
- **Attori Secondari**: Nessuno
- **Precondizioni**: L'utente è autenticato; non ha prenotazioni attive in corso; esiste almeno un mezzo disponibile nelle vicinanze.
- **Sequenza principale**:
  1. L'utente intende prenotare un mezzo disponibile nella mappa.
  2. Il sistema verifica che il mezzo sia ancora disponibile.
  3. Il sistema crea una prenotazione associando il mezzo all'utente.
  4. Il sistema aggiorna lo stato del mezzo da "Disponibile" a "Prenotato".
  5. Il sistema avvia il timer di prenotazione.
  6. Il sistema notifica l'utente con la conferma della prenotazione e il tempo rimanente.
- **Post-condizioni**: Il mezzo è nello stato "Prenotato" ed è associato all'utente; il timer di prenotazione è avviato.
- **Sequenze alternative**:
  - **CS-05.01 MezzoNonDisponibile**: Il mezzo è stato occupato da un altro utente. Il sistema informa l'utente e mostra la lista aggiornata dei mezzi disponibili.

---

### CS-10 — Sblocca Mezzo (UT.04)

- **Attori Primari**: Utente
- **Attori Secondari**: Nessuno
- **Precondizioni**: L'utente è autenticato; si trova in prossimità del mezzo; il mezzo è nello stato "Prenotato" dall'utente corrente oppure "Disponibile".
- **Sequenza principale**:
  1. L'utente vuole sbloccare un mezzo nell'applicazione.
  2. Il sistema verifica che l'utente si trovi entro la distanza massima consentita dal mezzo.
  3. Il sistema invia il comando di sblocco al mezzo.
  4. Il mezzo conferma l'avvenuto sblocco al sistema.
  5. Il sistema aggiorna lo stato del mezzo a "In Uso" e registra l'inizio della corsa.
  6. Il sistema notifica l'utente che il mezzo è pronto all'uso.
- **Post-condizioni**: Il mezzo è fisicamente sbloccato; lo stato è "In Uso"; la corsa è registrata come avviata.
- **Sequenze alternative**:
  - **CS-10.1 Comando Sblocca Fallito**: Il mezzo non risponde. Il sistema attende la conferma e notifica l'utente dell'impossibilità di sbloccare.

---

### CS-11 — Termina Corsa (UT.06)

- **Attori Primari**: Utente
- **Attori Secondari**: ServizioGIS
- **Precondizioni**: L'utente è autenticato e ha una corsa attiva.
- **Sequenza principale**:
  1. L'utente vuole terminare e pagare la corsa.
  2. Il sistema rileva la posizione corrente del mezzo tramite ServizioGIS. *(Punto di estensione: ErroreServizioGis)*
  3. Include (EffettuaPagamento) — CS-12.
  4. Il sistema aggiorna lo stato del mezzo da "In Uso" a "Disponibile".
  5. Il sistema mostra all'utente il Riepilogo Corsa.
- **Post-condizioni**: La corsa è terminata, il mezzo è disponibile, l'addebito è stato effettuato, il riepilogo è mostrato.
- **Sequenze alternative**:
  - **CS-11.1 MezzoInZonaVietata**: Il sistema rileva la Zona Vietata, notifica l'utente dell'applicazione di una penale obbligatoria e prosegue con il pagamento comprensivo di penale.

---

### CS-12 — Effettua Pagamento (UT.20)

- **Attori Primari**: Utente
- **Attori Secondari**: ProviderPagamenti
- **Precondizioni**: Una corsa è appena terminata; l'utente ha un metodo di pagamento predefinito valido.
- **Sequenza principale**:
  1. Il sistema registra la fine della corsa.
  2. Il sistema calcola la durata e l'importo dovuto in base alla tariffa applicabile.
  3. Il sistema recupera il metodo di pagamento predefinito dell'utente.
  4. Il sistema trasmette la richiesta di addebito al Sistema di Pagamento Esterno.
  5. Il Sistema di Pagamento Esterno autorizza e completa la transazione.
  6. Il sistema genera e invia la ricevuta di pagamento all'utente.
- **Post-condizioni**: L'importo è addebitato; l'utente riceve la ricevuta.
- **Sequenze alternative**:
  - **CS-12.1 PagamentoRifiutato**: Il ProviderPagamenti rifiuta la transazione. Il sistema notifica l'utente e lo invita ad aggiornare il metodo di pagamento.

---

### CS-13 — Salva Metodi di Pagamento (UT.12)

- **Attori Primari**: Utente
- **Attori Secondari**: ProviderPagamenti
- **Precondizioni**: L'utente è autenticato alla piattaforma.
- **Sequenza principale**:
  1. L'utente accede alla sezione "Portafoglio" dal menu laterale.
  2. Il sistema mostra i metodi di pagamento attuali e l'opzione per aggiungerne uno nuovo.
  3. L'utente seleziona l'opzione per aggiungere un nuovo metodo.
  4. Il sistema mostra le tipologie disponibili: Google Pay, Apple Pay, PayPal, carta di credito.
  5. L'utente seleziona la tipologia e inserisce i dati richiesti.
  6. Il sistema valida i dati tramite ProviderPagamenti. Se errore: informa l'utente e torna al passo 5.
  7. Il sistema verifica che il metodo non sia già associato all'account. Se presente: informa l'utente e non procede.
  8. Il sistema salva il nuovo metodo di pagamento.
  9. Se è il primo metodo, lo imposta automaticamente come predefinito. Altrimenti chiede se impostarlo come nuovo predefinito.
  10. Se l'utente conferma: aggiorna il metodo predefinito.
  11. Il sistema mostra un messaggio di conferma.
- **Post-condizioni**: Il nuovo metodo è salvato. Il metodo predefinito è quello scelto dall'utente, o il primo salvato se non c'è stata scelta esplicita.
- **Sequenze alternative**: Nessuna.

---

### CS-14 — Definisce Tariffa (OP.07)

- **Attori Primari**: Operatore
- **Attori Secondari**: Nessuno
- **Precondizioni**: L'operatore è autenticato; non esiste già una tariffa definita per la tipologia di mezzo selezionata.
- **Sequenza principale**:
  1. L'operatore accede alla sezione dedicata alle tariffe.
  2. Il sistema mostra le tariffe attualmente definite per ciascuna tipologia di mezzo.
  3. L'operatore seleziona la tipologia di mezzo (monopattino, bicicletta, automobile).
  4. Il sistema mostra il form con i campi: costo al minuto e costo al chilometro.
  5. L'operatore inserisce i valori richiesti.
  6. Il sistema valida che i valori siano numerici e maggiori di zero.
  7. Il sistema salva la nuova tariffa associandola alla tipologia di mezzo selezionata.
  8. Il sistema mostra un messaggio di conferma.
- **Post-condizioni**: La nuova tariffa è salvata e sarà applicata alle corse successive.
- **Sequenze alternative**: Nessuna.

---

### CS-16 — Modifica Stato Mezzo (OP.04)

- **Attori Primari**: Operatore
- **Attori Secondari**: Nessuno
- **Precondizioni**: L'operatore è autenticato; il mezzo selezionato esiste nella flotta.
- **Sequenza principale**:
  1. L'operatore accede alla sezione dedicata ai mezzi.
  2. Il sistema mostra la Mappa Operatore con la lista dei mezzi e il loro stato corrente.
  3. L'operatore seleziona il mezzo di cui intende modificare lo stato.
  4. Il sistema mostra lo stato corrente e le opzioni selezionabili: Disponibile, In manutenzione, Fuori servizio.
  5. L'operatore seleziona il nuovo stato desiderato.
  6. Il sistema verifica che la transizione di stato sia consentita.
  7. Il sistema aggiorna lo stato del mezzo.
  8. Il sistema mostra un messaggio di conferma.
- **Post-condizioni**: Lo stato del mezzo è aggiornato. Se "In manutenzione" o "Fuori servizio": non più visibile sulla Mappa Utente. Se "Disponibile": nuovamente visibile.
- **Sequenze alternative**:
  - **CS-16.1 MezzoInUso**: Il mezzo è in uso o prenotato. Il sistema informa l'operatore che la modifica non è possibile.

---

### CS-17 — Aggiunge Mezzo (OP.12)

- **Attori Primari**: Operatore
- **Attori Secondari**: ServizioGIS
- **Precondizioni**: L'operatore è autenticato e si trova nella Dashboard Operatore.
- **Sequenza principale**:
  1. L'operatore accede alla sezione dedicata ai mezzi.
  2. Il sistema mostra la lista dei mezzi attualmente presenti nella flotta.
  3. L'operatore seleziona la funzione per aggiungere un nuovo mezzo.
  4. Il sistema permette di inserire: tipologia (monopattino, bicicletta, automobile), identificativo, posizione iniziale, stato iniziale.
  5. L'operatore inserisce i dati e seleziona la posizione iniziale sulla mappa.
  6. L'operatore conferma i dati inseriti.
  7. Il sistema valida: campi obbligatori compilati, identificativo univoco. Se non validi: informa l'operatore e torna al passo 5.
  8. Il sistema verifica tramite ServizioGIS che la posizione ricada all'interno di una zona operativa.
  9. Il sistema salva il nuovo mezzo nella flotta.
  10. Il sistema mostra un messaggio di conferma.
- **Post-condizioni**: Il nuovo mezzo è salvato e disponibile sulla Mappa Utente in base allo stato impostato.
- **Sequenze alternative**:
  - **IdentificativoEsistente**: L'identificativo è già presente nel sistema. Il sistema informa l'operatore.

---

### CS-18 — Dismette Mezzo (OP.13)

- **Attori Primari**: Operatore
- **Attori Secondari**: Nessuno (CS-18.1: ServizioGIS)
- **Precondizioni**: L'operatore è autenticato; il mezzo è censito e non assegnato a missioni attive.
- **Sequenza principale**:
  1. L'operatore accede alla sezione dedicata ai mezzi.
  2. Il sistema mostra la lista dei mezzi con il loro stato corrente.
  3. L'operatore seleziona il mezzo da dismettere.
  4. Il sistema mostra i dettagli e richiede conferma della dismissione.
  5. L'operatore conferma la dismissione.
  6. Il sistema aggiorna lo stato del mezzo a "Dismesso" e lo rimuove dall'elenco dei mezzi disponibili.
  7. Il sistema mantiene lo storico delle informazioni associate al mezzo.
  8. Il sistema mostra un messaggio di conferma.
- **Post-condizioni**: Il mezzo è registrato come dismesso; non disponibile per nuove corse; i dati storici rimangono consultabili.
- **Sequenze alternative**:
  - **CS-18.1 MezzoInUso**: Il sistema rileva che il mezzo è impegnato in una corsa (tramite ServizioGIS), notifica l'impossibilità di dismettere e l'operatore ritorna alla sezione gestione mezzi.

---

### CS-19 — Definisce Regole Fine Corsa (OP.14)

- **Attori Primari**: Operatore
- **Attori Secondari**: Nessuno
- **Precondizioni**: L'operatore è autenticato e ha selezionato la funzione di configurazione delle regole di fine corsa.
- **Sequenza principale**:
  1. L'operatore accede alla sezione dedicata alle Regole Fine Corsa.
  2. Il sistema mostra le zone di parcheggio disponibili e i parametri configurabili.
  3. L'operatore seleziona le zone di parcheggio valide per la chiusura della corsa e imposta i vincoli aggiuntivi (stato del mezzo, livello batteria minimo, posizionamento corretto).
  4. L'operatore conferma le regole definite.
  5. Il sistema valida che i valori rientrino negli intervalli ammessi. Se non validi: informa l'operatore e torna al passo 3.
  6. Il sistema salva la nuova configurazione delle regole di fine corsa.
  7. Il sistema notifica all'operatore l'avvenuta definizione delle regole.
- **Post-condizioni**: Le nuove regole di fine corsa sono memorizzate e vengono applicate a tutte le corse successive.
- **Sequenze alternative**: Nessuna.

---

## 8. ARCHITETTURA DI SISTEMA (Struttura)

Il documento prevede i seguenti diagrammi (da completare in sprint successivi):

- **Diagramma Generale delle Componenti**: componenti Client, Server, Servizi Esterni, Database.
- **Componente Client**: interfaccia utente, operatore, amministrazione pubblica.
- **Componente Server**: BLL (Business Logic Layer), DAL (Data Access Layer).
- **Servizi Esterni**: ServizioGIS, ProviderPagamenti.
- **Database**: modello logico e struttura fisica.
- **Diagramma delle Classi**: da completare.
- **Diagrammi di Sequenza**: uno per ciascun caso d'uso.

---

## 9. GLOSSARIO

### 9.1 Acronimi

| Acronimo | Significato |
|----------|-------------|
| AP | Amministrazione Pubblica |
| API | Application Programming Interface |
| BLL | Business Logic Layer |
| CSV | Comma-Separated Values |
| DAL | Data Access Layer |
| DBMS | Database Management System |
| GIS / ServizioGIS | Geographic Information System |
| HTTP | HyperText Transfer Protocol |
| NFC | Near Field Communication |
| OP | Operatore del Servizio |
| PDF | Portable Document Format |
| QR | Quick Response (code) |
| UT | Utente |

### 9.2 Definizioni

| Termine | Definizione |
|---------|-------------|
| **Account utente** | Insieme di credenziali, dati anagrafici, metodi di pagamento, e-mail, password e storico associati a un utente registrato. |
| **Addebito** | Importo economico calcolato al termine di una corsa o di un evento tariffabile e prelevato dal metodo di pagamento associato all'account. |
| **Amministrazione Pubblica** | Ente locale (comune o equivalente) che regolamenta l'uso dello spazio urbano. Nel sistema è un ruolo distinto da Utente e Operatore. |
| **Autonomia residua** | Valore numerico della carica rimasta nella batteria di un mezzo elettrico. Espresso in % o km stimati; l'unità di misura è configurabile dalla piattaforma. |
| **Corsa / Sessione** | Sessione di utilizzo attivo di un mezzo sharing, dall'sblocco del veicolo alla chiusura della sessione. Al termine viene calcolato e addebitato il costo. |
| **Fine corsa** | Evento che conclude una corsa; l'esito (valido, penalizzato, rifiutato) dipende dalla posizione del mezzo rispetto a Zona Operativa e Zona di Parcheggio. |
| **Flotta** | Insieme di tutti i mezzi gestiti da un operatore nell'ambito del servizio di sharing su un determinato territorio. |
| **Formato Esportabile** | Formattazione offerta dalla piattaforma per l'esportazione dei dati. Include CSV e PDF. |
| **Mappa Operatore** | Visualizzazione cartografica per gli operatori. Mostra posizione e stato di tutti i mezzi della flotta (inclusi quelli nascosti alla Mappa Utente). |
| **Mappa Utente** | Visualizzazione cartografica per gli utenti. Mostra solo i mezzi disponibili/prenotabili entro un raggio configurabile, le zone con vincoli e le zone di parcheggio consigliate. |
| **Metodo di pagamento** | Strumento associato all'account utente (carta, wallet, ecc.) usato per regolare gli addebiti. |
| **Mezzo** | Qualsiasi veicolo messo a disposizione: bicicletta tradizionale, e-bike, monopattino elettrico (e-scooter), macchina elettrica. |
| **Mezzo disponibile** | Mezzo il cui stato è "Disponibile", quindi prenotabile. Unico tipo visualizzato sulla Mappa Utente. |
| **Operatore del Servizio** | Soggetto (azienda privata o consorzio) responsabile della gestione operativa della flotta e della configurazione della piattaforma. |
| **Pausa corsa** | Stato intermedio in cui l'utente blocca temporaneamente il mezzo senza terminare la corsa. |
| **Periodo di grazia** | Durata massima configurabile dall'operatore entro cui una pausa corsa non comporta addebiti aggiuntivi o la perdita del mezzo. Se zero, la pausa gratuita è disabilitata. |
| **Prenotazione** | Riserva temporanea di un mezzo effettuata dall'utente prima di raggiungerlo fisicamente. Ha una durata massima configurabile; alla scadenza il mezzo viene rilasciato automaticamente. |
| **Prenotazione di gruppo** | Prenotazione effettuata da un singolo utente per un numero di mezzi fino al massimo configurato dall'operatore. |
| **Promozione** | Offerta che riduce la tariffa standard o offre condizioni speciali. Configurata e pubblicata dall'operatore. |
| **Abbonamento** | Contratto a tempo determinato (es. mensile, annuale) con condizioni tariffarie agevolate o corse incluse. Configurato dall'operatore. |
| **Bonus** | Valore monetario assegnato all'utente dall'operatore secondo condizioni definite (es. parcheggio corretto). Se zero, non è visualizzabile dall'utente. |
| **Redistribuzione** | Operazione logistica di spostamento fisico dei mezzi da aree con eccesso di offerta verso aree con carenza. |
| **Report aggregato** | Documento con statistiche anonime sull'utilizzo del servizio su un intervallo temporale configurabile. Destinato a operatore e AP. |
| **Riepilogo corsa** | Sintesi presentata all'utente al termine di una corsa: durata, distanza percorsa, costo finale, sconti o bonus applicati. |
| **Sblocco** | Operazione che disabilita il blocco fisico/elettronico del mezzo. Il metodo (QR code, Bluetooth, NFC) è una scelta implementativa. |
| **Segnalazione** | Comunicazione inviata dall'utente all'operatore per notificare anomalie su un mezzo (danno, guasto, posizione anomala). |
| **Stato (mezzo)** | Condizione operativa corrente. Valori possibili: **Disponibile** (prenotabile), **Prenotato** (riservato a un utente), **In uso** (corsa attiva), **In pausa** (pausa corsa attiva), **In manutenzione** (rimosso dalla Mappa Utente), **Fuori servizio** (bloccato o irrecuperabile). |
| **Storico corsa** | L'insieme delle corse effettuate da un utente. |
| **Tariffa** | Struttura di pricing applicata a una corsa (es. costo al minuto, alla distanza, tariffa fissa). Definita e modificabile dall'operatore. |
| **Tariffario** | Elenco pubblicato dall'operatore delle tariffe applicate per ciascuna tipologia di mezzo. |
| **Utente** | Persona fisica registrata alla piattaforma che utilizza i mezzi di sharing. Interagisce tramite dispositivo mobile. |
| **Zona Operativa** | Perimetro geografico definito dall'operatore entro cui i mezzi possono circolare e fermarsi. Zona Limitata e Zona Vietata hanno sempre precedenza sulla Zona Operativa. |
| **Zona di parcheggio** | Area geografica designata dall'operatore in cui è consigliato parcheggiare al termine della corsa. Visibile sulla Mappa Utente. Può essere associata a un Bonus configurabile. |
| **Zona Limitata** | Area geografica con restrizioni configurabili (es. velocità ridotta, orari limitati, divieto di sosta). Configurata dall'operatore. |
| **Zona Vietata** | Area geografica in cui la circolazione dei mezzi è completamente vietata. Ha precedenza sulla Zona Operativa in caso di sovrapposizione. |

---

## 10. NOTE METODOLOGICHE

### Regole dello Sprint
- Ogni sprint produce codice funzionante (unica eccezione: Sprint n°0, destinato alla macroarchitettura).
- Lo Sprint n°0 disegna la macroarchitettura con componenti e interfacce, usata come roadmap per gli sprint successivi.
- Gli item funzionali (User Stories) sono tracciabili 1:1 con i casi d'uso.
- Ogni caso d'uso include uno scenario di base e gli scenari alternativi.
- Ad ogni caso d'uso è associato un diagramma di sequenza.

### Qualità dei Requisiti
Le user story sono state validate secondo 14 caratteristiche di qualità. Il sistema di valutazione adottato prevede un punteggio da 0 a 5 per ciascuna caratteristica. Il documento riporta un **Mean Score: 5.0** per tutte le caratteristiche:

| Caratteristica | Score |
|----------------|-------|
| Non Ambiguo | 5 |
| Provabile o Verificabile | 5 |
| Chiaro | 5 |
| Corretto | 5 |
| Comprensibile | 5 |
| Fattibile | 5 |
| Indipendente e Auto-consistente | 5 |
| Atomico | 5 |
| Necessario | 5 |
| Astratto | 5 |
| Consistente | 5 |
| Non Ridondante | 5 |
| Completo | 5 |
| Metriche Derivate (Manutenibilità e Tracciabilità) | 5 |
