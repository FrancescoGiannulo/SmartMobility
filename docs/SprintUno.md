# SMART MOBILITY – Contesto di Sistema per Agente IA

> **Documento:** Ciclo 4, Versione 2.0 – rilasciato il 10/05/2026  
> **Progetto accademico:** Ingegneria del Software a.a. 2025-2026  
> **Università:** Dipartimento di Informatica, Università degli Studi di Bari (SERLAB)  
> **Team:** Cardone Flavio (829469), De Astis Gabriele (826243), Giannulo Francesco (825071), Lacirignola Camilla (830465)

---

## 1. Descrizione del Sistema

**SMART MOBILITY** è una piattaforma software integrata per la mobilità urbana sostenibile del Comune di **Zootropolis**. Unifica diversi servizi di sharing (bike sharing, car sharing, e-scooter sharing) in un'unica interfaccia accessibile a tre categorie di utenti: cittadini, operatori di servizio e amministrazione pubblica.

### Obiettivi principali

1. Offrire ai cittadini un accesso rapido, sicuro e trasparente ai mezzi di sharing disponibili sul territorio.
2. Permettere agli operatori di gestire in modo efficiente la flotta, ridurre costi e fenomeni di vandalismo.
3. Consentire all'Amministrazione Pubblica di monitorare la mobilità urbana e assumere decisioni strategiche basate su dati.

---

## 2. Stakeholder e Ruoli

### 2.1 Utente (UT)
Persona fisica registrata che utilizza i mezzi di sharing. Deve essere autenticata per accedere alle funzionalità.

**Sottotipi:**
- **Pendolare Urbano** – usa il servizio regolarmente per l'ultimo miglio, cerca affidabilità e abbonamenti.
- **Utente Occasionale** – residente che usa il servizio saltuariamente.
- **Turista** – necessita di accesso rapido e senza frizioni (social login, pagamenti rapidi).

### 2.2 Operatore del Servizio (OP)
Azienda privata o consorzio che immette i mezzi sulla strada e gestisce il business.

**Figure interne:**
- **Manager del Servizio** – definisce tariffe, promozioni, zone operative.
- **Team Logistico e Manutentori** – gestione fisica della flotta sul campo (ricarica, riparazione, redistribuzione).

### 2.3 Amministrazione Pubblica (AP)
Ente locale che detiene la sovranità sul suolo pubblico e definisce le regole del servizio.

**Figure coinvolte:**
- **Pianificatore Urbano / Mobility Manager** – usa i dati per pianificare percorsi ciclabili e gestire restrizioni.
- **Polizia Locale / Corpo di Vigilanza** – monitora il rispetto delle zone vietate e la gestione dei parcheggi.

---

## 3. Product Backlog – Requisiti Funzionali

### 3.1 Funzionalità Utente (IF-UT)

| ID | Nome | Descrizione (User Story) |
|----|------|--------------------------|
| IF-UT.01 | Visualizza Mappa Utente | Come utente, voglio visualizzare la Mappa Utente, così da poter scegliere un mezzo. |
| IF-UT.02 | Prenota mezzo | Come utente, voglio prenotare un mezzo disponibile, così da trovarlo riservato al mio arrivo. |
| IF-UT.03 | Annulla Prenotazione | Come utente, voglio annullare una prenotazione attiva prima di raggiungere il mezzo, così da liberarlo se cambio programma. |
| IF-UT.04 | Sblocca un mezzo | Come utente, voglio sbloccare un mezzo, così da avviare fisicamente la corsa. |
| IF-UT.05 | Consulta tariffe | Come utente, voglio consultare il tariffario per ciascuna tipologia di mezzo, così da confrontarne i costi. |
| IF-UT.06 | Termina Corsa | Come utente, voglio terminare la corsa, così da liberare il mezzo. |
| IF-UT.07 | Visualizza Riepilogo corsa | Come utente, voglio ricevere il riepilogo corsa, così da visualizzare le informazioni sulla corsa effettuata. |
| IF-UT.08 | Consulta Stato Mezzo | Come utente, voglio consultare lo stato di un mezzo, così da effettuare una scelta in base alle mie esigenze di percorso. |
| IF-UT.09 | Visualizza Zone | Come utente, voglio visualizzare le zone soggette a restrizioni sulla mappa, così da pianificare il mio percorso. |
| IF-UT.10 | Sospende Corsa | Come utente, voglio mettere in pausa la corsa, così da effettuare soste senza perdere il possesso del mezzo. |
| IF-UT.11 | Prenota Gruppo | Come utente, voglio effettuare una prenotazione di gruppo fino al numero massimo di mezzi, così da gestire in un'unica operazione la mobilità condivisa con accompagnatori. |
| IF-UT.12 | Salva Metodi Pagamento | Come utente, voglio salvare uno o più metodi di pagamento, così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati. |
| IF-UT.13 | Visualizza Promozioni | Come utente, voglio accedere alle promozioni attive, così da ridurre i costi di utilizzo del servizio. |
| IF-UT.14 | Visualizza Storico Corsa | Come utente, voglio visualizzare lo storico delle corse, così da tenere traccia di tutte le corse effettuate. |
| IF-UT.15 | Invia Segnalazione | Come utente, voglio inviare una segnalazione, così da informare l'operatore affinché possa intervenire. |
| IF-UT.16 | Sottoscrive Abbonamento | Come utente, voglio sottoscrivere un abbonamento, così da usufruire di condizioni tariffarie agevolate. |
| IF-UT.17 | Registra Account | Come utente, voglio registrarmi alla piattaforma, così da poter accedere ai servizi di sharing. |
| IF-UT.18 | Autentica Account | Come utente, voglio autenticarmi alla piattaforma, così da accedere ai miei dati e alle funzionalità. |
| IF-UT.19 | Modifica Dati Account | Come utente, voglio modificare i dati del mio profilo, così da mantenere le mie informazioni aggiornate. |
| IF-UT.20 | Effettua Pagamento | Come utente, voglio che il sistema addebiti automaticamente l'importo sul mio metodo di pagamento predefinito al termine della corsa, così da non dover effettuare transazioni manuali. |
| IF-UT.21 | Imposta Metodo di Pagamento predefinito | Come utente, voglio impostare un metodo di pagamento predefinito, così da utilizzarlo automaticamente per gli addebiti. |

### 3.2 Funzionalità Amministrazione Pubblica (IF-AP)

| ID | Nome | Descrizione (User Story) |
|----|------|--------------------------|
| IF-AP.01 | Accede Report | Come AP, voglio accedere a report aggregati sull'utilizzo del servizio, così da supportare decisioni strategiche di pianificazione. |
| IF-AP.02 | Definisce Zone Vietate | Come AP, voglio definire i confini di una Zona Vietata, così da garantire il rispetto delle normative locali. |
| IF-AP.03 | Definisce Zone Parcheggio | Come AP, voglio definire zone di parcheggio visibili sulla Mappa Utente, così da ridurre il disordine dei mezzi sulla strada. |
| IF-AP.04 | Definisce Limite Velocità | Come AP, voglio definire il limite di velocità applicabile in ciascuna Zona Limitata, così da garantire il rispetto delle normative locali. |
| IF-AP.05 | Esporta Report | Come AP, voglio esportare i report aggregati in Formato Esportabile (CSV/PDF), così da utilizzarli in analisi esterne e documentazione ufficiale. |
| IF-AP.06 | Modifica Zona | Come AP, voglio modificare una zona pubblicata in precedenza, così da aggiornare la regolamentazione al variare delle condizioni urbane. |
| IF-AP.07 | Autentica Account | Come AP, voglio autenticarmi alla piattaforma con credenziali dedicate, così da accedere alle funzionalità di regolamentazione e ai report. |
| IF-AP.08 | Visualizza Mappa AP | Come AP, voglio visualizzare la mappa, così da monitorare il servizio sulla città. |

### 3.3 Funzionalità Operatore (IF-OP)

| ID | Nome | Descrizione (User Story) |
|----|------|--------------------------|
| IF-OP.01 | Visualizza Mappa Operatore | Come operatore, voglio visualizzare la Mappa Operatore, così da pianificare operazioni di redistribuzione. |
| IF-OP.02 | Gestisce Segnalazioni | Come operatore, voglio leggere le segnalazioni inviate dagli utenti, così da pianificare gli interventi di manutenzione. |
| IF-OP.03 | Definisce Zona Operativa | Come operatore, voglio definire la Zona Operativa, così da impedire l'allontanamento dei mezzi dall'area di servizio. |
| IF-OP.04 | Modifica Stato Mezzo | Come operatore, voglio modificare lo Stato di un mezzo, così da nasconderlo o mostrarlo sulla Mappa Utente. |
| IF-OP.05 | Sospende Account Utente | Come operatore, voglio sospendere l'account di un utente, così da tutelare l'integrità del servizio. |
| IF-OP.06 | Definisce Offerte Commerciali | Come operatore, voglio definire promozioni con condizioni e scadenza configurabili, così da incentivare l'utilizzo del sistema. |
| IF-OP.07 | Definisce Tariffa | Come operatore, voglio definire la tariffa del servizio, così da permettere la configurazione del modello di costo. |
| IF-OP.08 | Modifica Tariffa | Come operatore, voglio modificare una tariffa esistente per una tipologia di mezzo, così da aggiornare il modello di costo. |
| IF-OP.09 | Configura Durata Prenotazione | Come operatore, voglio configurare la durata massima di una prenotazione, così da liberare i mezzi non utilizzati. |
| IF-OP.10 | Configura Durata Periodo Grazia | Come operatore, voglio configurare la durata del periodo di grazia per la pausa corsa, così da offrire agli utenti un tempo gratuito. |
| IF-OP.11 | Configura Numero Massimo Mezzi | Come operatore, voglio configurare il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente, così da abilitare le prenotazioni di gruppo. |
| IF-OP.12 | Aggiunge Mezzo | Come operatore, voglio aggiungere un nuovo mezzo alla mappa, così da aumentare il numero di mezzi della flotta. |
| IF-OP.13 | Dismette Mezzo | Come operatore, voglio dismettere un mezzo dalla mappa, così da gestire il ciclo di vita della flotta. |
| IF-OP.14 | Definisce Regole Fine Corsa | Come operatore, voglio definire regole sanzionatorie per i rilasci dei mezzi al di fuori delle aree di parcheggio consentite, così da garantire il decoro urbano. |
| IF-OP.15 | Configura Addebito per Pausa Corsa | Come operatore, voglio configurare la politica di addebito durante la pausa corsa al termine del periodo di grazia, così da rendere trasparente e flessibile il pricing della pausa. |
| IF-OP.16 | Autentica Account Operatore | Come operatore, voglio autenticarmi alla piattaforma, così da accedere alle funzionalità di gestione flotta, tariffe e promozioni. |

---

## 4. Requisiti Non Funzionali

### 4.1 Prestazioni (IIN-1)
- Il sistema deve aggiornare la posizione dei mezzi sulla Mappa Utente entro x secondi dall'ultimo rilevamento GPS (da definire con test).
- Il sistema deve completare l'operazione di prenotazione di un mezzo entro x secondi dalla richiesta dell'utente (da definire con test).

### 4.2 Sicurezza (IIN-2)
- Tutte le comunicazioni tra client e server devono essere cifrate mediante protocolli di sicurezza standard.
- Il sistema deve bloccare un account dopo 5 tentativi di autenticazione falliti consecutivi in un tempo configurabile dall'operatore.
- I dati personali degli utenti devono essere trattati in conformità al **Regolamento UE 2016/679 (GDPR)**.
- Ciascun ruolo (UT, OP, AP) deve poter accedere esclusivamente alle funzionalità ad esso assegnate.

### 4.3 Usabilità (IIN-3)
- L'interfaccia deve essere accessibile secondo le linee guida **WCAG** (es. per utenti con disabilità visive).
- L'interfaccia deve essere facile da usare e comprensibile in meno di x minuti (da definire con test).

### 4.4 Scalabilità (IIN-4)
- L'architettura deve permettere l'aggiunta di nuove tipologie di mezzo senza modifiche strutturali.

### 4.5 Portabilità (IIN-5)
- Il sistema deve essere accessibile tramite browser web su dispositivi desktop e mobile, senza necessità di installazione.

### 4.6 Conformità
- I report esportabili in CSV/PDF devono rispettare eventuali standard di formato richiesti dalla pubblica amministrazione.

---

## 5. Sprint 1 – Backlog

Gli item implementati nello Sprint 1 sono:

| Codice Item | Funzionalità |
|-------------|--------------|
| UT.01 | Visualizza Mappa utente |
| UT.02 | Prenota mezzo |
| UT.04 | Sblocca un mezzo |
| UT.06 | Termina Corsa |
| UT.12 | Salva metodi di pagamento |
| UT.17 | Registra account |
| UT.18 | Autentica account utente |
| UT.19 | Modifica dati account |
| UT.20 | Effettua Pagamento |
| UT.21 | Imposta Metodo di Pagamento Predefinito |
| AP.07 | Autentica Account AP |
| AP.02 | Definisce zone vietate |
| AP.03 | Definisce zone parcheggio |
| AP.08 | Visualizza mappa Amministrazione Pubblica |
| OP.01 | Visualizza Mappa Operatore |
| OP.03 | Definisce zone operative |
| OP.07 | Definisce tariffe |
| OP.04 | Modifica stato mezzo |
| OP.08 | Modifica tariffe |
| OP.16 | Autentica account operatore |
| OP.12 | Aggiungi un mezzo |
| OP.13 | Dismetti un mezzo |
| OP.14 | Definisci regole fine corsa |

---

## 6. Casi d'Uso – Specifiche (Sprint 1)

### CS-01 – Visualizza Mappa
- **Attori primari:** Utente, Operatore, Amministrazione Pubblica
- **Attori secondari:** ServizioGIS
- **Precondizioni:** L'attore è autenticato
- **Flusso principale:**
  1. L'attore accede alla schermata principale.
  2. Il sistema rileva la posizione geografica corrente tramite il dispositivo.
  3. Il sistema interroga il ServizioGIS per recuperare i dati geografici.
  4. Punto di estensione: `ErroreServizioGIS` (CS-02)
  5. Il sistema recupera le zone soggette a restrizioni e le zone di parcheggio.
  6. Il sistema visualizza la mappa con i mezzi per tipologia, le aree con restrizioni e il marker della posizione corrente.
- **Post-condizioni:** La mappa è visualizzata con i dati aggiornati.
- **Contenuto per ruolo:** Utente vede mezzi disponibili e zone; Operatore vede intera flotta con stati; AP vede distribuzione zone regolamentate.

### CS-02 – Segnala Errore Servizio GIS
- **Attori primari:** Sistema
- **Attori secondari:** ServizioGIS
- **Precondizioni:** Il ServizioGIS non è raggiungibile o restituisce un errore.
- **Flusso:** Il sistema notifica l'attore dell'impossibilità di completare l'operazione e propone di riprovare.

### CS-03 – Definisci Zona
- **Attori primari:** Amministrazione Pubblica, Operatore
- **Precondizioni:** L'attore è autenticato con il ruolo appropriato.
- **Flusso principale:**
  1. Il sistema visualizza la mappa interattiva con le zone esistenti.
  2. L'attore disegna il perimetro della zona definendo i vertici del poligono.
  3. L'attore conferma la creazione della zona.
  4. Loop: include `ValidaPerimetro` (CS-04); se non valido il sistema notifica e chiede correzione.
  5. Il sistema salva la Zona e la rende attiva.
  6. Il sistema aggiorna la mappa visibile agli Utenti.
- **Post-condizioni:** La nuova Zona è persistita nel sistema e applicata alla flotta.

### CS-04 – Valida Perimetro
- **Attori primari:** Sistema
- **Verifiche eseguite:**
  1. Il poligono è chiuso.
  2. Assenza di auto-intersezioni tra i lati.
  3. Numero di vertici ≥ 3.
  4. La zona non è sovrapposta ad una già esistente.
- **Esito:** positivo se tutte le verifiche passano, negativo con indicazione del problema altrimenti.

### CS-05 – Prenota Mezzo
- **Attori primari:** Utente
- **Precondizioni:** Utente autenticato, nessuna prenotazione attiva, almeno un mezzo disponibile nelle vicinanze.
- **Flusso principale:**
  1. L'utente seleziona un mezzo disponibile sulla mappa.
  2. Il sistema verifica che il mezzo sia ancora disponibile.
  3. Il sistema crea la prenotazione associando il mezzo all'utente.
  4. Il sistema aggiorna lo stato del mezzo da "Disponibile" a "Prenotato".
  5. Il sistema avvia il timer di prenotazione.
  6. Il sistema notifica l'utente con conferma e tempo rimanente.
- **Post-condizioni:** Mezzo nello stato "Prenotato" e timer avviato.
- **Alternativa CS-05.01 – MezzoNonDisponibile:** Il mezzo è stato occupato nel frattempo. Il sistema informa l'utente e mostra la lista aggiornata dei mezzi disponibili.

### CS-06 – Registra Account
- **Attori primari:** Utente
- **Precondizioni:** Nessuna.
- **Flusso principale:**
  1. Il sistema presenta il modulo di registrazione.
  2. L'utente inserisce i propri dati.
  3. Include `ValidaDatiAccount` (CS-07); se negativo, mostra errori e richiede correzione.
  4. Il sistema crea il nuovo account e autentica automaticamente l'utente.
  5. Il sistema reindirizza l'utente alla schermata principale.
- **Post-condizioni:** Nuovo account creato, utente autenticato.

### CS-07 – ValidaDatiAccount
- **Attori primari:** Sistema
- **Verifiche eseguite in parallelo:**
  - Tutti i campi obbligatori compilati.
  - Indirizzo email sintatticamente valido.
  - Email non già associata a un account esistente.
  - Password rispetta i requisiti minimi; coincide con la conferma password (se prevista).
- **Esito:** positivo se tutto ok, negativo con lista completa degli errori.

### CS-08 – Modifica Dati Account
- **Attori primari:** Utente
- **Precondizioni:** Utente autenticato.
- **Flusso:** L'utente modifica i campi nel profilo, include `ValidaDatiAccount`; se valido il sistema aggiorna e notifica il successo.

### CS-09 – Autentica Account
- **Attori primari:** Utente, Amministrazione Pubblica, Operatore
- **Precondizioni:** L'attore ha un account registrato e attivo.
- **Flusso:** Inserimento credenziali → verifica → redirect alla vista corrispondente al ruolo. Se credenziali errate, il sistema comunica l'errore e ripropone il form.

### CS-10 – Sblocca Mezzo
- **Attori primari:** Utente
- **Precondizioni:** Utente autenticato, in prossimità del mezzo; mezzo in stato "Prenotato" dall'utente corrente oppure "Disponibile".
- **Flusso:**
  1. Il sistema verifica che l'utente sia entro la distanza massima consentita.
  2. Il sistema invia il comando di sblocco al mezzo.
  3. Il mezzo conferma l'avvenuto sblocco.
  4. Il sistema aggiorna lo stato a "In Uso" e registra l'inizio della corsa.
  5. Il sistema notifica l'utente che il mezzo è pronto all'uso.
- **Post-condizioni:** Mezzo fisicamente sbloccato, stato "In Uso", corsa avviata.
- **Alternativa CS-10.1 – Comando Sblocca Fallito:** Il mezzo non risponde; il sistema notifica l'utente che non è stato possibile sbloccare il mezzo.

### CS-11 – Termina Corsa
- **Attori primari:** Utente
- **Attori secondari:** ServizioGIS
- **Precondizioni:** Utente autenticato con una corsa attiva.
- **Flusso:**
  1. Il sistema rileva la posizione corrente del mezzo tramite ServizioGIS. (Punto di estensione: `ErroreServizioGIS`)
  2. Include `EffettuaPagamento` (CS-12).
  3. Il sistema aggiorna lo stato del mezzo da "In Uso" a "Disponibile".
  4. Il sistema mostra all'utente il Riepilogo Corsa.
- **Post-condizioni:** Corsa terminata, mezzo disponibile, addebito effettuato, riepilogo mostrato.
- **Alternativa CS-11.1 – MezzoInZonaVietata:** Il sistema informa l'utente della Zona Vietata e applica una penale obbligatoria al costo totale prima di procedere.

### CS-12 – Effettua Pagamento
- **Attori primari:** Utente
- **Attori secondari:** ProviderPagamenti
- **Precondizioni:** Corsa appena terminata; utente ha un metodo di pagamento predefinito registrato e valido.
- **Flusso:**
  1. Il sistema calcola la durata della corsa e l'importo dovuto in base alla tariffa applicabile.
  2. Il sistema recupera il metodo di pagamento predefinito dell'utente.
  3. Il sistema trasmette la richiesta di addebito al ProviderPagamenti.
  4. Il ProviderPagamenti autorizza e completa la transazione.
  5. Il sistema genera e invia la ricevuta di pagamento all'utente.
- **Post-condizioni:** Importo addebitato, ricevuta inviata.
- **Alternativa CS-12.1 – PagamentoRifiutato:** Il ProviderPagamenti rifiuta la transazione. Il sistema notifica l'utente del fallimento e lo invita ad aggiornare il metodo di pagamento.

### CS-13 – Salva Metodi di Pagamento
- **Attori primari:** Utente
- **Attori secondari:** ProviderPagamenti
- **Precondizioni:** Utente autenticato.
- **Flusso:**
  1. L'utente accede alla sezione "Portafoglio".
  2. Il sistema mostra i metodi di pagamento associati e l'opzione per aggiungerne uno nuovo.
  3. L'utente seleziona la tipologia (Google Pay, Apple Pay, PayPal, carta di credito) e inserisce i dati.
  4. Il sistema valida i dati tramite ProviderPagamenti; se errore, informa l'utente e ripropone il form.
  5. Il sistema verifica che il metodo non sia già associato all'account; se duplicato, informa l'utente.
  6. Il sistema salva il metodo di pagamento.
  7. Se è il primo metodo salvato, viene impostato automaticamente come predefinito. Altrimenti chiede all'utente se desidera impostarlo come predefinito.
  8. Il sistema mostra conferma.
- **Post-condizioni:** Nuovo metodo di pagamento salvato; metodo predefinito aggiornato se richiesto.

### CS-14 – Definisce Tariffa
- **Attori primari:** Operatore
- **Precondizioni:** Operatore autenticato; NON esiste già una tariffa per la tipologia di mezzo selezionata.
- **Flusso:**
  1. L'operatore accede alla sezione tariffe.
  2. Seleziona la tipologia di mezzo (monopattino, bicicletta, automobile).
  3. Inserisce costo al minuto e costo al chilometro.
  4. Il sistema valida (valori numerici e > 0) e salva.
- **Post-condizioni:** Nuova tariffa salvata, applicata alle corse successive di quella tipologia.

### CS-15 – Modifica Tariffa
- **Attori primari:** Operatore
- **Precondizioni:** Operatore autenticato; almeno una tariffa precedentemente definita.
- **Flusso:** L'operatore seleziona la tariffa, modifica i parametri (tipologia mezzo, struttura pricing, valore), conferma; il sistema valida e aggiorna.
- **Post-condizioni:** Tariffa aggiornata; le nuove corse saranno addebitate con la tariffa aggiornata.

### CS-16 – Modifica Stato Mezzo
- **Attori primari:** Operatore
- **Precondizioni:** Operatore autenticato; mezzo esistente nella flotta.
- **Stati selezionabili:** Disponibile, In manutenzione, Fuori servizio.
- **Flusso:** L'operatore seleziona il mezzo, sceglie il nuovo stato; il sistema verifica che la transizione sia consentita e aggiorna.
- **Post-condizioni:** Se nuovo stato è "In manutenzione" o "Fuori servizio", il mezzo non è visibile sulla Mappa Utente. Se "Disponibile", torna visibile.
- **Alternativa CS-16.1 – MezzoInUso:** Il mezzo è in uso o prenotato; la modifica viene bloccata e l'operatore viene informato.

### CS-17 – Aggiunge Mezzo
- **Attori primari:** Operatore
- **Attori secondari:** ServizioGIS
- **Precondizioni:** Operatore autenticato nella Dashboard Operatore.
- **Flusso:**
  1. L'operatore seleziona la funzione "aggiungi mezzo".
  2. Inserisce tipologia, identificativo, posizione iniziale (sulla mappa) e stato iniziale.
  3. Il sistema valida (campi obbligatori compilati, identificativo univoco).
  4. Il sistema verifica tramite ServizioGIS che la posizione ricada in una zona operativa.
  5. Il sistema salva il mezzo.
- **Post-condizioni:** Mezzo salvato e disponibile sulla Mappa Utente in base allo stato impostato.
- **Alternativa:** IdentificativoEsistente.

### CS-18 – Dismette Mezzo
- **Attori primari:** Operatore
- **Precondizioni:** Operatore autenticato; mezzo censito e non assegnato a corsa attiva.
- **Flusso:** L'operatore seleziona il mezzo, conferma la dismissione; il sistema aggiorna lo stato a "Dismesso", rimuove dalla disponibilità e mantiene lo storico.
- **Post-condizioni:** Mezzo registrato come dismesso; dati storici consultabili.
- **Alternativa CS-18.1 – MezzoInUso:** Il sistema rileva (tramite ServizioGIS) che il mezzo è in una corsa attiva e blocca la dismissione.

### CS-19 – Definisce Regole Fine Corsa
- **Attori primari:** Operatore
- **Precondizioni:** Operatore autenticato, funzione di configurazione selezionata.
- **Flusso:**
  1. Il sistema mostra le zone di parcheggio disponibili e i parametri configurabili.
  2. L'operatore seleziona le zone di parcheggio valide per la chiusura della corsa e imposta i vincoli aggiuntivi (stato del mezzo, livello batteria minimo, posizionamento corretto).
  3. Il sistema valida i parametri (valori negli intervalli ammessi); se non valido, informa l'operatore.
  4. Il sistema salva la configurazione.
- **Post-condizioni:** Le nuove regole di fine corsa sono applicate a tutte le corse successive.

---

## 7. Architettura di Sistema

### 7.1 Pattern Architetturale
Il sistema segue un modello **Client-Server** con pattern **MVC** (Model-View-Controller) su più livelli.

### 7.2 Componente Client

**View (interfacce utente):**
- `VistaUtente` – per gli utenti finali
- `VistaOperatore` – per gli operatori
- `VistaAmministrazionePubblica` – per gli enti pubblici

**API Service Layer (comunicazione con il server):**
- `ApiService` – Gateway centrale HTTP (GET/POST/PUT/DELETE)
- `AuthService` – login, logout, registrazione
- `MapService` – dati geografici, bridge verso ServizioGIS
- `PaymentService` – metodi di pagamento e transazioni
- `ZonaService` – definizioni zone geografiche
- `FlottaService` – stato dei mezzi della flotta

### 7.3 Componente Server

**Controller Layer:**
- `UtenteController`
  - `PrenotazioneUtenteController`
  - `PagamentiController`
- `OperatoreController`
  - `MezzoOperatoreController`
  - `ZonaOperatoreController`
  - `PrenotazioneOperatoreController`
- `AmministrazionePubblicaController`
  - `ZonaAPController`
  - `ReportAPController`

**Business Logic Layer (BLL):**
- `ServizioMobilità` – orchestrazione principale
- `ServizioGIS` – funzionalità geografiche e mappatura
- `ServizioUtenti` – registrazione, profilo utenti
- `ServizioPricing` – calcolo tariffe e promozioni
- `ServizioReport` – generazione report e statistiche
- `ServizioPrenotazione` – ciclo di vita delle prenotazioni

**Model (entità del dominio):**
- `Utente`, `Operatore`, `AmministrazionePubblica`
- `Mezzo`, `Corsa`, `Prenotazione`, `Zona`
- `Segnalazione`, `Pagamento`, `Promozione`

**Data Access Layer (DAL):**
- `UtenteRepository`, `MezzoRepository`, `CorsaRepository`
- `PagamentoRepository`, `ZonaRepository`, `PrenotazioneRepository`

### 7.4 Servizi Esterni
- **BingMaps** – fornitore di mappe e geolocalizzazione (usato da `MapService`)
- **ProviderPagamenti** – gateway di pagamento esterno (usato da `PaymentService`)

### 7.5 Database
- Componente `DBMS` accessibile tramite interfaccia `DALToDBMS`

### 7.6 Interfacce di Sistema

| Interfaccia | Descrizione |
|-------------|-------------|
| `ClientToServer` | Invio richieste dal client verso l'API layer |
| `ServerToClient` | Invio dati dal server verso il client |
| `ApiToView` | Permette alle viste di invocare funzionalità server senza dettagli HTTP |
| `ControllerToBLL` | Controller invocano i servizi della Business Logic |
| `BLLToController` | Restituzione risultati dalla BLL verso il Controller |
| `BLLToModel` | BLL crea, legge o aggiorna le entità del dominio |
| `ModelToBLL` | Model fornisce dati strutturati ai servizi BLL |
| `ModelToDAL` | Passaggio oggetti di dominio allo strato di persistenza |
| `DALToDBMS` | Esecuzione query e transazioni sul database |
| `ServiziEsterni` | Interazione con ProviderPagamenti e BingMaps |

---

## 8. Mockup delle Interfacce (IUI)

| ID | Schermata | Descrizione sintetica |
|----|-----------|----------------------|
| IUI-1 | Login Utente | Design clean, form con Username/Password, pulsanti LOGIN e SIGN UP in verde acqua, social login Google e Apple. |
| IUI-2 | Homepage Utente | Mappa interattiva con pin per tipologia mezzo (monopattini verde, bici blu, auto magenta), geo-fence zone in rosso, pulsanti floating "CORSA DI GRUPPO" e "SBLOCCA MEZZO", bottom navigation bar. |
| IUI-3 | Menu Laterale Utente | Side drawer da destra con: Profilo, Piano Tariffario, Bonus e Promozioni, Cronologia, Impostazioni, Portafoglio, Guida. |
| IUI-4 | Corsa di Gruppo | Bottom sheet con contatore "Veicoli sbloccati: N/max", cards per ogni veicolo (codice + batteria), pulsante "SBLOCCA VEICOLO". |
| IUI-5 | Prenotazione Mezzo | Bottom sheet con dati mezzo (tipologia, codice, batteria), avviso del limite temporale per sblocco, pulsante "Prenota". |
| IUI-6 | Piano Tariffario | Cards con tariffe chilometriche: Monopattino 0,20€/km, Bicicletta 0,30€/km, Automobile 0,50€/km. |
| IUI-7 | Portafoglio | Card saldo in verde acqua, lista metodi di pagamento (Google Pay, Apple Pay, PayPal, carta di credito), pulsante "RICARICA SALDO". |
| IUI-8 | Info Corsa (attiva) | Dashboard con ID mezzo, batteria, timer tempo trascorso, km percorsi; pulsanti "TERMINA E PAGA" e "PAUSA CORSA". |
| IUI-9 | Cronologia Corse | Lista con icona mezzo, ID, tempo trascorso, km percorsi, data. |
| IUI-10 | Login Operatore/AP | Layout landscape, stessa struttura del login utente. |
| IUI-11 | Dashboard AP | Split-screen: mappa a sinistra, pannello con pulsanti "DEFINISCI ZONE VIETATE", "DEFINISCI ZONE LIMITATE", "DEFINISCI ZONE PARCHEGGIO", "VISUALIZZA REPORT". |
| IUI-12 | Definizione Zone Vietate | Mappa con poligono rosso disegnato dall'utente, pannello con istruzioni e toggle per selezionare tipologie di mezzo a cui applicare il divieto. |
| IUI-13 | Definizione Zone Limitate | Come zone vietate ma con colore arancione (restrizione parziale). |
| IUI-14 | Definizione Zone Parcheggio | Come zone vietate ma con colore verde (area consentita). |
| IUI-15 | Report AP | Istogramma noleggi settimanali + grafico a torta per tipologia mezzo; pulsanti "ESPORTA CSV" e "ESPORTA PDF". |
| IUI-16 | Dashboard Operatore | Split-screen: Mappa Operatore con pin colorati per tipologia, pulsanti floating "AGGIUNGI MEZZO" / "DISMETTI MEZZO"; pannello con "GESTISCI SEGNALAZIONI", "GESTISCI UTENTI", "IMPOSTAZIONI REGOLE", "TARIFFE E PROMOZIONI", "VISUALIZZA REPORT", "GESTISCI MEZZI". |
| IUI-17 | Gestione Segnalazioni | Tabella (utente, data, ora, tipo problema, dettaglio), pulsante "RISPONDI" per ogni riga. |
| IUI-18 | Gestione Tariffe e Promozioni | Due card: sinistra con tariffe per tipologia mezzo (valore numerico editabile + selettore unità es. €/km); destra con promozione attiva e pulsante "AGGIUNGI PROMOZIONE". |
| IUI-19 | Impostazione Regole | Card con parametri numerici configurabili: durata max prenotazione, durata periodo di grazia, numero max prenotazioni simultanee per utente, percentuale tariffa durante pausa corsa, regola di business (dropdown: penale / divieto / avviso). |

---

## 9. Glossario

### Acronimi

| Acronimo | Significato |
|----------|-------------|
| AP | Amministrazione Pubblica |
| API | Application Programming Interface |
| BLL | Business Logic Layer |
| CSV | Comma-Separated Values |
| DAL | Data Access Layer |
| DBMS | Database Management System |
| HTTP | HyperText Transfer Protocol |
| NFC | Near Field Communication |
| OP | Operatore del Servizio |
| PDF | Portable Document Format |
| QR | Quick Response (code) |
| ServizioGIS | Geographic Information System |
| UT | Utente |

### Definizioni Chiave

| Termine | Definizione |
|---------|-------------|
| **Account utente** | Insieme di credenziali, dati anagrafici, metodi di pagamento, e-mail, password e storico associati a un utente registrato. |
| **Addebito** | Importo economico calcolato al termine di una corsa e prelevato dal metodo di pagamento predefinito dell'utente. |
| **Autonomia residua** | Carica rimasta nella batteria di un mezzo elettrico, espressa in % o km stimati (unità configurabile). |
| **Corsa** (= Sessione) | Sessione di utilizzo attivo di un mezzo: inizia con lo sblocco e termina con la chiusura della sessione da parte dell'utente. |
| **Fine corsa** | Evento che conclude una corsa; l'esito (valido, penalizzato, rifiutato) dipende dalla posizione del mezzo rispetto a Zona Operativa e Zona di parcheggio. |
| **Flotta** | Insieme di tutti i mezzi gestiti da un operatore nell'ambito del servizio di sharing. |
| **Formato Esportabile** | CSV o PDF. |
| **Mappa Operatore** | Vista cartografica per operatori: mostra posizione e stato di tutti i mezzi della flotta (inclusi quelli nascosti alla Mappa Utente). |
| **Mappa Utente** | Vista cartografica per utenti: mostra solo i mezzi disponibili/prenotabili nelle vicinanze, le zone con vincoli e le zone parcheggio. |
| **Mezzo** | Bicicletta tradizionale, e-bike, monopattino elettrico (e-scooter), macchina elettrica. |
| **Mezzo disponibile** | Mezzo il cui stato è "Disponibile": unici visualizzabili sulla Mappa Utente. |
| **Pausa corsa** | Stato intermedio di una sessione in cui l'utente blocca temporaneamente il mezzo senza terminare la corsa. |
| **Periodo di grazia** | Durata massima configurabile dall'operatore entro cui la pausa corsa non comporta addebiti aggiuntivi. Se 0, la pausa gratuita è disabilitata. |
| **Prenotazione** | Riserva temporanea di un mezzo. Ha durata massima configurabile dall'operatore; alla scadenza il mezzo viene rilasciato automaticamente. |
| **Prenotazione di gruppo** | Prenotazione per un numero di mezzi fino al massimo configurato dall'operatore (può essere anche 1). |
| **Promozione** | Offerta che riduce la tariffa standard o offre condizioni speciali. |
| **Abbonamento** | Contratto a tempo determinato (es. mensile/annuale) con condizioni tariffarie agevolate. Sottotipo di Promozione. |
| **Bonus** | Valore monetario assegnato all'utente dall'operatore (es. per parcheggio corretto). Se 0, la funzionalità non è visibile all'utente. |
| **Redistribuzione** | Spostamento fisico dei mezzi da aree con eccesso di offerta verso aree con carenza, eseguito dal personale operativo. |
| **Report aggregato** | Documento con statistiche anonime sull'utilizzo (corse, km, fasce orarie, zone) su un intervallo configurabile. |
| **Riepilogo corsa** | Sintesi mostrata all'utente al termine della corsa: durata, distanza percorsa, costo finale, eventuali sconti/bonus. Disponibile anche nello storico corse. |
| **Sblocco** | Operazione che disabilita il blocco fisico/elettronico del mezzo. Metodo (QR, Bluetooth, NFC) è una scelta implementativa. |
| **Segnalazione** | Comunicazione inviata dall'utente all'operatore per anomalie su un mezzo (danno fisico, guasto, posizione anomala). |
| **Stato (mezzo)** | Valori possibili: `Disponibile`, `Prenotato`, `In uso`, `In pausa`, `In manutenzione`, `Fuori servizio`, `Dismesso`. |
| **Storico corsa** | L'insieme delle corse effettuate da un utente. |
| **Tariffa** | Struttura di pricing applicata a una corsa (costo al minuto, alla distanza, tariffa fissa per fascia oraria). Definita e modificabile dall'operatore. |
| **Tariffario** | Elenco delle tariffe per ciascuna tipologia di mezzo e modalità di utilizzo. |
| **Zona Operativa** | Perimetro definito dall'operatore entro cui i mezzi possono circolare e fermarsi. Le zone AP hanno sempre la precedenza in caso di sovrapposizione. |
| **Zona di parcheggio** | Area designata dall'AP in cui è consigliato (non obbligatorio) parcheggiare. L'operatore può associare un Bonus. |
| **Zona Limitata** | Area definita dall'AP con restrizioni parziali (es. velocità ridotta, orari limitati, divieto di sosta o pausa). Visualizzata sulla Mappa Utente. |
| **Zona Vietata** | Area definita dall'AP in cui la circolazione dei mezzi è completamente vietata. Ha precedenza sulla Zona Operativa in caso di sovrapposizione. |

---

## 10. Note per l'Agente IA

- **Lingua del dominio:** italiano. Tutti i nomi di entità, ruoli, stati e zone sono in italiano.
- **Tre ruoli distinti:** UT (Utente), OP (Operatore), AP (Amministrazione Pubblica). Ognuno accede esclusivamente alle funzionalità assegnate.
- **Priorità delle zone:** le zone dell'AP (Vietata, Limitata) hanno sempre la precedenza sulle zone dell'OP. Le sovrapposizioni si risolvono sempre a favore delle restrizioni AP.
- **Stati del mezzo:** il ciclo di vita è `Disponibile → Prenotato → In uso → (In pausa) → Disponibile`. Uno stato `In manutenzione` o `Fuori servizio` rimuove il mezzo dalla Mappa Utente. `Dismesso` è uno stato finale irreversibile.
- **Pagamento automatico:** il sistema addebita automaticamente al termine della corsa sul metodo di pagamento predefinito; non è richiesta alcuna azione manuale da parte dell'utente.
- **Sprint corrente (Sprint 1):** 23 item in sviluppo, copertura ampia delle funzionalità core per tutti e tre i ruoli.
- **Sezioni ancora da completare nel documento:** Diagramma dei Casi d'uso (2.2.1), Diagramma delle Classi (2.4.1), Specifiche delle Classi (2.4.2), Diagrammi di Sequenza (2.4.3), Modello logico del Database (2.5.1), Struttura fisica del Database (2.5.2), Definizioni prompt (3.3), Item Qualitativi (1.5.3) e Altri Item (1.5.4) sono sezioni vuote o da sviluppare.
- **Servizi esterni integrati:** BingMaps (mappe/geolocalizzazione) e ProviderPagamenti (transazioni).
- **Conformità normativa:** GDPR (Regolamento UE 2016/679), accessibilità WCAG.