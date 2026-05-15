

Nome Gruppo

[Nome System]
Versione x.y
Data di rilascio:

Ingegneria del Software a.a. 2025-2026[CdL]

Realizzato da
Cognome Nome Matricola Corso di Laurea e-mail
Cognome Nome Matricola Corso di Laurea e-mail

Indice
1.	Product Backlog	5
1.4	Introduzione	5
1.5	Contesto di business	5
1.6	Stakeholder	5
1.7	Item funzionali	5
1.7.5	IF-C1	5
1.7.6	IF-2	5
1.7.7	IF-n	5
1.8	Item funzionali	5

## 1.8.1	IF-UT.01 – Visualizza Mappa Utente	6

## 1.8.2	IF-UT.02 – Prenota mezzo	6

## 1.8.3	IF-UT.03 – Annulla Prenotazione	6

## 1.4.4 IF-UT.04 – Sblocca un mezzo	6

## 1.8.4	IF-UT.05 – Consulta tariffe	6

## 1.8.5	IF-UT.06 – Termina Corsa	6

## 1.8.6	IF-UT.07 – Visualizza Riepilogo corsa	6

## 1.8.7	IF-UT.08 – Consulta Stato Mezzo	7

1.8.8	IF-UT.09– Visualizza Zone	7

## 1.8.9	IF-UT.10 – Sospende Corsa	7

## 1.8.10	IF-UT.11 – Prenota Gruppo	7

## 1.8.11	IF-UT.12 – Salva Metodi Pagamento	7

## 1.8.12	IF-UT.13 – Visualizza Promozioni	8

## 1.8.13	IF-UT.14 – Visualizza Storico Corsa	8

## 1.8.14	IF-UT.15 – Invia Segnalazione	8

## 1.8.15	IF-UT.16 – Sottoscrive Abbonamento	8

## 1.8.16	IF-UT.17 – Registra Account	8

## 1.8.17	IF-UT.18 – Autentica Account	8

## 1.8.18	IF-UT.19 – Modifica Dati Account	8

## 1.8.19	– IF-UT.20 – Effettua pagamento	9

## 1.4.19 IF-AP.01 – Accede Report	9

## 1.8.20	IF-AP.02 - Definisce Zone Vietate	9

## 1.8.21	IF-AP.03 - Definisce Zone Parcheggio	9

## 1.8.22	IF-AP.04 – Definisce Limite Velocità	9

## 1.8.23	IF-AP.05 – Esporta Report	10

## 1.8.24	IF-AP.06 – Modifica Zona	10

## 1.8.25	IF-AP.07 – Autentica Account	10

## 1.8.26	IF-OP.01 – Visualizza Mappa Operatore	10

## 1.8.27	IF-OP.02 – Gestisce Segnalazioni	10

## 1.8.28	IF-OP.03 – Definisce Zona Operativa	10

## 1.8.29	IF-OP.04 – Modifica Stato Mezzi	11

## 1.8.30	IF-OP.05 – Sospende Account Utente	11

## 1.8.31	IF-OP.06 – Definisce Offerte Commerciali	11

## 1.8.32	IF-OP.07 – Definisce Tariffa	11

## 1.8.33	IF-OP.08 – Modifica Tariffa	11

## 1.8.34	IF-OP.09 – Configura Durata Prenotazione	11

## 1.8.35	IF-OP.10 – Configura Durata Periodo Grazia	11

## 1.8.36	IF-OP.11 – Configura Numero Massimo Mezzi	12

## 1.8.37	IF-OP.12 – Aggiunge Mezzo	12

## 1.8.38	IF-OP.13 – Dismette Mezzo	12

## 1.8.39	IF-OP.14 – Definisce Regole Fine Corsa	12

## 1.8.40	IF-OP.15 – Configura Addebito per Pausa Corsa	12

## 1.8.41	IF-OP.16 – Autentica Account Operatore	13

2.	Sprint Report	14
2.4	Sprint Backlog	14
2.5	Product Requirement Specification	16
2.5.5	Diagramma dei Casi d’uso	16
2.5.6	Specifiche dei Casi d’uso	16
Altro	43

# 2.6	System Architecture	43

2.6.5	Diagramma delle Componenti	43
2.6.6	Specifica delle componenti	43
2.6.7	Specifica delle interfacce	43

# 2.7	Detailed Product Design	44

2.7.5	Diagramma delle Classi	44
2.7.6	Specifiche delle Classi	44
2.7.7	Diagrammi di Sequenza	44

# 2.8	Data modeling and design	44

2.8.5	Modello logico del Database	44
2.8.6	Struttura fisica del Database	44

Product Backlog
Introduzione
Fornisce una descrizione testuale macroscopica del sistema, anche attraverso l’utilizzo di diagrammi di natura informale, utile a delineare i confini del sistema e ad inquadrare i vari elementi, dal funzionale al qualitativo.
Contesto di business
Stakeholder
Item funzionali
Contiene l’elenco e la specifica di tutti i requisiti funzionali espressi attraverso lo schema delle user stories:
COME <ruolo>
DEVO POTER <fare qualcosa>
PER CONSEGUIRE <un risultato >
Esempio: Come magazziniere devo poter filtrare l’archivio ordini secondo la data di ricezione per consultare gli ordini evasi.
IF-C1
Specificare la user story 1 unitamente ad una descrizione estesa della stessa
IF-2
Specificare la user story 2 unitamente ad una descrizione estesa della stessa
IF-n
Specificare la user story n unitamente ad una descrizione estesa della stessa
•	Item funzionali
Contiene l’elenco e la specifica di tutti i requisiti funzionali espressi attraverso lo schema delle user stories:

## •	IF-UT.01 – Visualizza Mappa Utente

Come utente,
Voglio visualizzare la Mappa Utente,
Così da poter scegliere un mezzo.

## •	IF-UT.02 – Prenota mezzo

Come utente,
Voglio prenotare un mezzo disponibile,
Così da trovarlo riservato al mio arrivo.

## •	IF-UT.03 – Annulla Prenotazione

Come utente,
Voglio annullare una prenotazione attiva prima di raggiungere il mezzo,
Così da liberare il mezzo se cambio programma.

## 1.4.4 IF-UT.04 – Sblocca un mezzo

Come utente,
Voglio sbloccare un mezzo,
Così da avviare fisicamente la corsa.

## IF-UT.05 – Consulta tariffe

Come utente,
Voglio consultare il tariffario per ciascuna tipologia di mezzo,
Così da confrontarne i costi

## IF-UT.06 – Termina Corsa

Come utente,
Voglio terminare la corsa
Così da liberare il mezzo.

## •	IF-UT.07 – Visualizza Riepilogo corsa

Come utente,
Voglio ricevere il riepilogo corsa,
Così da visualizzare le informazioni sulla corsa effettuata

## •	IF-UT.08 – Consulta Stato Mezzo

Come utente,
Voglio consultare lo stato di un mezzo,
Così da effettuare una scelta in base alle mie esigenze di percorso.
•	IF-UT.09– Visualizza Zone
Come utente,
Voglio visualizzare le zone soggette a restrizioni sulla mappa,
Così da pianificare il mio percorso nel rispetto delle normative vigenti.

## •	IF-UT.10 – Sospende Corsa

Come utente,
Voglio mettere in pausa la corsa,
Così da effettuare soste senza perdere il possesso del mezzo.

## •	IF-UT.11 – Prenota Gruppo

Come utente,
Voglio effettuare una prenotazione di gruppo fino al numero massimo di mezzi,
Così da gestire in un'unica operazione la mobilità condivisa con accompagnatori.

## •	IF-UT.12 – Salva Metodi Pagamento

Come utente,
Voglio salvare uno o più metodi di pagamento,
Così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati.

## •	IF-UT.13 – Visualizza Promozioni

Come utente,
Voglio accedere alle promozioni attive,
Così da ridurre i costi di utilizzo del servizio.

## •	IF-UT.14 – Visualizza Storico Corsa

Come utente,
Voglio visualizzare lo storico delle corse,
Così da tenere traccia di tutte le corse effettuate.

## •	IF-UT.15 – Invia Segnalazione

Come utente,
Voglio inviare una segnalazione,
Così da informare l'operatore affinché possa intervenire.

## •	IF-UT.16 – Sottoscrive Abbonamento

Come utente,
Voglio sottoscrivere un abbonamento,
Così da usufruire di condizioni tariffarie agevolate.

## •	IF-UT.17 – Registra Account

Come utente,
Voglio registrarmi alla piattaforma,
Così da poter accedere ai servizi di sharing.

## •	IF-UT.18 – Autentica Account

Come utente,
Voglio autenticarmi alla piattaforma,
Così da accedere ai miei dati e alle funzionalità.

## •	IF-UT.19 – Modifica Dati Account

Come utente,
Voglio modificare i dati del mio profilo,
Così da mantenere le mie informazioni aggiornate.

## IF-UT.20 – Effettua pagamento

Come Utente,
Voglio che il sistema addebiti automaticamente l'importo sul mio metodo di pagamento predefinito al termine della corsa,
Così da non dover effettuare transazioni manuali ogni volta che scendo dal mezzo.
(L’utente per poter prendere il mezzo, deve mettere una carta di credito)

## 1.4.19 IF-AP.01 – Accede Report

Come amministrazione pubblica,
Voglio accedere a report aggregati sull'utilizzo del servizio,
Così da supportare decisioni strategiche di pianificazione.

## •	IF-AP.02 - Definisce Zone Vietate

Come amministrazione pubblica,
Voglio definire i confini di una Zona Vietata,
Così da garantire il rispetto delle normative locali.

## •	IF-AP.03 - Definisce Zone Parcheggio

Come amministrazione pubblica,
Voglio definire zone di parcheggio visibili sulla Mappa Utente,
Così da ridurre il disordine dei mezzi sulla strada.

## •	IF-AP.04 – Definisce Limite Velocità

Come amministrazione pubblica,
Voglio definire il limite di velocità applicabile in ciascuna Zona Limitata,
Così da garantire il rispetto delle normative locali.

## •	IF-AP.05 – Esporta Report

Come amministrazione pubblica,
Voglio esportare i report aggregati sull'utilizzo del servizio in Formato Esportabile,
Così da utilizzarli in analisi esterne e documentazione ufficiale.

## •	IF-AP.06 – Modifica Zona

Come amministrazione pubblica,
Voglio modificare una zona pubblicata in precedenza,
Così da aggiornare la regolamentazione al variare delle condizioni urbane.

## •	IF-AP.07 – Autentica Account

Come amministrazione pubblica,
Voglio autenticarmi alla piattaforma con credenziali dedicate,
Così da accedere alle funzionalità di regolamentazione e ai report.

## •	IF-OP.01 – Visualizza Mappa Operatore

Come operatore,
Voglio visualizzare la Mappa Operatore,
Così da pianificare operazioni di redistribuzione.

## •	IF-OP.02 – Gestisce Segnalazioni

Come operatore,
Voglio leggere le segnalazioni inviate dagli utenti,
Così da pianificare gli interventi di manutenzione.

## •	IF-OP.03 – Definisce Zona Operativa

Come operatore,
Voglio definire la Zona Operativa,
Così da impedire l'allontanamento dei mezzi dall'area di servizio.

## •	IF-OP.04 – Modifica Stato Mezzi

Come operatore,
Voglio modificare lo Stato di un mezzo,
Così da nasconderlo o mostrarlo sulla Mappa Utente.

## •	IF-OP.05 – Sospende Account Utente

Come operatore,
Voglio sospendere l'account di un utente,
Così da tutelare l'integrità del servizio

## •	IF-OP.06 – Definisce Offerte Commerciali

Come operatore,
Voglio definire promozioni con condizioni e scadenza configurabili,
Così da incentivare l'utilizzo del sistema con politiche commerciali flessibili.

## •	IF-OP.07 – Definisce Tariffa

Come operatore,
Voglio definire la tariffa del servizio,
Così da permettere la configurazione del modello di costo.

## •	IF-OP.08 – Modifica Tariffa

Come operatore,
Voglio modificare una tariffa esistente per una tipologia di mezzo,
Così da aggiornare il modello di costo.

## •	IF-OP.09 – Configura Durata Prenotazione

Come operatore,
Voglio configurare la durata massima di una prenotazione,
Così da liberare i mezzi non utilizzati.

## •	IF-OP.10 – Configura Durata Periodo Grazia

Come operatore,
Voglio configurare la durata del periodo di grazia per la pausa corsa,
Così da offrire agli utenti un tempo gratuito.

## •	IF-OP.11 – Configura Numero Massimo Mezzi

Come operatore,
Voglio configurare il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente,
Così da abilitare le prenotazioni di gruppo.

## •	IF-OP.12 – Aggiunge Mezzo

Come operatore,
Voglio aggiungere un nuovo mezzo alla mappa,
Così da aumentare il numero di mezzi della flotta.

## •	IF-OP.13 – Dismette Mezzo

Come operatore,
Voglio dismettere un mezzo dalla mappa,
Così da gestire il ciclo di vita della flotta.

## •	IF-OP.14 – Definisce Regole Fine Corsa

Come Operatore
Voglio Definire regole sanzionatorie per i rilasci dei mezzi al di fuori delle aree di parcheggio consentite
Così da garantire il decoro urbano

## •	IF-OP.15 – Configura Addebito per Pausa Corsa

Come operatore,
Voglio configurare la politica di addebito durante la pausa corsa al termine del periodo di grazia,
Così da rendere trasparente e flessibile il pricing della pausa.

## •	IF-OP.16 – Autentica Account Operatore

Come operatore,
Voglio autenticarmi alla piattaforma,
Così da accedere alle funzionalità di gestione flotta, tariffe e promozioni.
Sprint Report
Sprint Backlog

Tabella di riepilogo che indica, per ognuno degli Sprint successivi allo Sprint n.0, la lista degli item del Product Backlog, evidenziando quelli che verranno implementati nell’ambito dello sprint corrente unitamente ad una descrizione esplicativa.
Per semplificare l’esposizione e salvaguardare la tracciabilità tra semilavorati si è proceduto alle seguenti assunzioni:
•	All’interno di uno Sprint sono implementati un sottoinsieme di item tra quelli specificati nel Product Backlog
•	Lo Sprint Backlog relativo allo sprint corrente contiene pertanto l’insieme degli item del Product Backlog in corso di implementazione
•	Gli Item funzionali, ovvero le User Stories dovranno essere tracciabili uno a uno, auspicabilmente seppur non necessariamente, con i casi d’uso
•	Ad ogni caso d’uso dovrà essere associato uno scenario di base più gli eventuali scenari alternativi. Lo scenario in prima istanza viene redatto a partire dalla specifica della User Story riportata nel Product Backlog
•	Ad ogni caso d’uso dovrà essere associato un diagramma di sequenza.
Ogni sprint deve necessariamente produrre in output del codice funzionante. L’unica eccezione è rappresentata dallo Sprint n°0 che deve essere utilizzato per disegnare la macroarchitettura del sistema con le sue componenti e le sue interfacce, e che sarà utilizzata come roadmap per gli sprint successivi andando a chiarire dove si colloca quanto realizzato in ciascuno di essi.

Codice Item
Numero Sprint
Note
UT.01
Sprint 1

## Visualizza Mappa utente - Camilla

UT.02
Sprint 1

## Prenota mezzo - Gabriele

UT.04
Sprint 1

## Sblocca un mezzo - Gabriele

UT.06
Sprint 1

## Termina Corsa - Flavio

UT.12
Sprint 1
Salva metodi di pagamento-Flavio
UT.17
Sprint 1

## Registra account - Camilla

UT.18
Sprint 1

## Autentica account utente - Camilla

UT.19
Sprint 1

## Modifica dati account - Camilla

UT.20
Sprint 1

## Effettua Pagamento - Gabriele

AP.07
Sprint 1

## Autentica Account ap - camilla

AP.02
Sprint 1
Definisce zone vietate- Gabriele
AP.03
Sprint 1

## Definisce zone parcheggio - Gabriele

OP.01
Sprint 1

## Visualizza Mappa Operatore - Francesco

OP.03
Sprint 1

## Definisce zone operative - Francesco

OP.07
Sprint 1

## Definisce tariffe - Flavio

OP.04
Sprint 1

## Modifica stato mezzi - Flavio

OP.08
Sprint 1

## Modifica tariffe - Flavio

OP.16
Sprint 1

## Autentica account operatore - camilla

OP.12
Sprint 1

## Aggiungi un mezzo - Francesco

OP.13
Sprint 1

## Dismetti un mezzo - Francesco

OP.14
Sprint 1

## Definisci regole fine corsa - Francesco

Product Requirement Specification
Diagramma dei Casi d’uso
Specifiche dei Casi d’uso

## Visualizza Mappa Utente - Camilla

**Nome:** Visualizza Mappa Utente
**ID:** UT.01
**Breve descrizione:** Il sistema mostra all'utente autenticato la mappa interattiva con i mezzi disponibili nelle vicinanze, le zone soggette a restrizioni e le zone di parcheggio, così da consentire la scelta di un mezzo da prenotare o sbloccare.
**Attori Primari:** Utente
**Attori Secondari:** ServizioGIS (BingMaps)
**Precondizioni:** L'utente è autenticato alla piattaforma
Sequenza principale degli eventi
•	Il caso d'uso inizia quando l'utente accede alla schermata principale della piattaforma.
•	Il sistema rileva la posizione geografica corrente dell'utente tramite il dispositivo mobile.
•	Il sistema interroga il ServizioGIS per recuperare i mezzi con stato “Disponibile” presenti nel raggio configurabile dall'operatore.
•	Il sistema recupera le zone soggette a restrizioni (zone vietate, zone limitate) e le zone di parcheggio definite dall'Amministrazione Pubblica.
•	Il sistema visualizza la mappa interattiva con:
•	i pin dei mezzi disponibili, codificati per colore e icona in base alla tipologia (monopattino, bicicletta, automobile);
•	le aree geografiche con restrizioni evidenziate cromaticamente sulla mappa;
•	il marker della posizione corrente dell'utente.
•	L'utente visualizza la mappa e può selezionare un mezzo per procedere alla prenotazione o allo sblocco.
**Post-condizioni:** La mappa è visualizzata con i dati aggiornati; l'utente può procedere con una delle azioni disponibili (prenotazione, sblocco, consultazione zone).
**Sequenza alternativa degli eventi:** •	Posizione non disponibile
– Errore di comunicazione con il ServizioGIS

**Nome:** VisualizzaMappaUtente: PosizionenNonDisponibile
**ID:** UT.01.1
**Breve descrizione:** Il sistema informa l'utente che non è possibile rilevare la sua posizione geografica.
**Attori Primari:** Utente
**Attori Secondari:** 

**Precondizioni:** Il dispositivo dell'utente non ha il GPS attivo o ha negato i permessi di geolocalizzazione.
**Post-condizioni:** La mappa viene visualizzata senza centratura automatica sulla posizione dell'utente. L'utente è informato dell'assenza della geolocalizzazione.
**Sequenza alternativa degli eventi:** •	La sequenza alternativa inizia dopo il passo 2 della sequenza principale.
•	Il sistema rileva che la geolocalizzazione non è disponibile sul dispositivo.
•	Il sistema visualizza la mappa senza centratura automatica
•	Il sistema notifica l'utente di abilitare il GPS per usufruire della funzione.

**Nome:** VisualizzaMappaUtente: ErroreServizioGIS
**ID:** UT.01.3
**Breve descrizione:** Il sistema informa l'utente che non è possibile caricare i dati della mappa a causa di un errore di comunicazione con il ServizioGIS.
**Attori Primari:** Utente
**Attori Secondari:** ServizioGIS (BingMaps)
**Precondizioni:** Il ServizioGIS non è raggiungibile o restituisce un errore durante la richiesta dei dati geografici.
**Post-condizioni:** Nessuna. La mappa non viene caricata
**Sequenza alternativa degli eventi:** •	La sequenza alternativa inizia dopo il passo 3 della sequenza principale.
•	Il sistema rileva un errore di comunicazione con il ServizioGIS.
•	Il sistema notifica l'utente dell'impossibilità di caricare i dati della mappa
•	Il sistema propone di riprovare l’operazione.

## UT.02 - Prenota Mezzo - Gabriele

**Nome:** Prenota Mezzo
**ID:** IF-UT.02
**Breve descrizione:** L'Utente prenota un mezzo disponibile nelle vicinanze; il sistema riserva il mezzo per un intervallo di tempo definito, impedendo ad altri utenti di prenotarlo.
Attori primari
Utente
Attori secondari
Nessuno
**Precondizioni:** L'Utente è autenticato nel sistema; l'Utente non ha prenotazioni attive in corso; esiste almeno un mezzo disponibile nelle vicinanze.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'Utente seleziona "Prenota" su un mezzo disponibile nella mappa.
2. Il sistema verifica che il mezzo sia ancora disponibile.
3. Il sistema crea una prenotazione associando il mezzo all'Utente.
4. punto di estensione: “Modifica Stato Mezzo”.
5. Il sistema avvia il timer di prenotazione.
6. Il sistema notifica l'Utente con la conferma della prenotazione e il tempo rimanente.
Postcondizioni
Il mezzo selezionato risulta nello stato "Prenotato" ed è associato all'Utente; il timer di prenotazione è avviato.
Sequenze alternative
MezzoNonDisponibile

**Nome:** PrenotaMezzo:MezzoNonDisponibile
**ID:** IF-UT.02.1
**Breve descrizione:** Il mezzo selezionato è stato occupato da un altro utente nell'intervallo tra la visualizzazione e la conferma della prenotazione.
**Precondizioni:** Il mezzo è passato allo stato "Prenotato" o "In Uso" prima del completamento della richiesta dell'Utente.
Postcondizioni
Lo stato del sistema rimane invariato; l'Utente non ha prenotazioni attive.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.
2. Il sistema informa l'Utente che il mezzo selezionato non è più disponibile.

3. Il sistema mostra la lista aggiornata dei mezzi disponibili nelle vicinanze.

## – Registra Account - Camilla

**Nome:** Registra Account
**ID:** UT.17
**Breve descrizione:** Il sistema registra un nuovo account utente sulla piattaforma, così da consentire l'accesso ai servizi di sharing.
**Attori Primari:** Utente
**Attori Secondari:** 

**Precondizioni:** Nessuna
Sequenza principale degli eventi
•	Il caso d'uso inizia quando l'utente seleziona "Sign Up" nella schermata di login.
•	Il sistema chiede all'utente di inserire i propri dati di registrazione.
•	L'utente inserisce i dati richiesti.
•	Fintantochè le informazioni dell’Utente non sono valide
4.1 Include (ValidaDatiAccount)
•	Il sistema crea il nuovo account utente e lo autentica automaticamente.
•	Il sistema reindirizza l'utente alla schermata principale.
**Post-condizioni:** Un nuovo account utente è stato creato e l'utente è autenticato sulla piattaforma.
**Sequenza alternativa degli eventi:** Nessuna

– ValidaDatiAccount
**Nome:** ValidaDatiAccount
**ID:** CS-02
**Breve descrizione:** Il sistema valida i dati inseriti durante le operazioni che richiedono la creazione o la modifica di un account, verificando la correttezza dell'indirizzo di posta elettronica, la conformità della password ai requisiti minimi e la completezza dei campi obbligatori.
**Attori Primari:** Sistema
**Attori Secondari:** -
**Precondizioni:** Un caso d'uso chiamante ha ricevuto i dati inseriti dall'utente e richiede la validazione.
Sequenza degli eventi principale
•	Il caso d'uso inizia quando un caso d'uso chiamante invoca la validazione dei dati inseriti.
•	Il sistema verifica che tutti i campi obbligatori siano stati compilati.
•	Il sistema verifica che l'indirizzo di posta elettronica sia sintatticamente valido.
•	Il sistema verifica che l'indirizzo di posta elettronica non sia già associato a un account esistente nella piattaforma.
•	Il sistema verifica che la password rispetti i requisiti minimi di sicurezza e coincida con la conferma password, se prevista dal caso d'uso chiamante.
•	Il sistema restituisce esito positivo al caso d'uso chiamante.
**Post-condizioni:** I dati sono stati validati con successo; il caso d'uso chiamante può proseguire con la propria sequenza principale.
**Sequenza alternativa degli eventi:** •	Se uno o più campi obbligatori sono vuoti, il sistema restituisce esito negativo al caso d'uso chiamante indicando i campi mancanti.
•	Se l'indirizzo di posta elettronica non è sintatticamente valido, il sistema restituisce esito negativo al caso d'uso chiamante indicando l'errore sul campo email.
•	Se l'indirizzo di posta elettronica è già associato a un account esistente, il sistema restituisce esito negativo al caso d'uso chiamante indicando che l'indirizzo è già in uso.
•	Se la password non rispetta i requisiti minimi o non coincide con la conferma password, il sistema restituisce esito negativo al caso d'uso chiamante indicando l'errore sul campo password.

## Modifica dati account – Camilla

**Nome:** Modifica dati account
**ID:** UT.19
**Breve descrizione:** Il sistema consente all'utente autenticato di modificare i dati del proprio profilo, così da mantenere le informazioni associate all'account aggiornate.
**Attori Primari:** Utente
**Attori Secondari:** Nessuno
**Precondizioni:** L'utente è autenticato alla piattaforma
Sequenza principale degli eventi
•	Il caso d'uso inizia quando l'utente accede alla sezione "Profilo".
•	Il sistema recupera e mostra i dati attualmente associati all'account utente.
•	L'utente modifica uno o più campi tra quelli disponibili.
•	L'utente conferma le modifiche.
•	Fintantoché le informazioni dell’Utente non sono valide
5.1 Include (ValidaDatiAccount)
•	Il sistema aggiorna i dati del profilo nel database
•	Il sistema notifica l’utente che le modifiche sono state salvate con successo.
**Post-condizioni:** I dati del profilo utente sono stati aggiornati con le nuove informazioni inserite.
**Sequenza alternativa degli eventi:** Nessuna

Autentica accout

**Nome:** Autentica Account
**ID:** CS-03 (UT.18, AP.07, OP.16)
**Breve descrizione:** L'attore accede alla piattaforma inserendo le proprie credenziali, così da ottenere accesso alle funzionalità corrispondenti al proprio ruolo.
**Attori Primari:** Utente, Amministrazione Pubblica, Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'attore dispone di un account registrato e attivo nella piattaforma.
Sequenza principale degli eventi
•	Il caso d'uso inizia quando l'attore apre la piattaforma.
•	Il sistema visualizza la schermata di login con i campi da compilare
•	L'attore inserisce le credenziali e conferma.
•	Il sistema verifica le credenziali nel database.
•	Se le credenziali sono corrette:
5.1 Il sistema reindirizza l'attore alla vista corrispondente al proprio ruolo con le relative funzionalità
•	Altrimenti
6.1 Il sistema comunica all’attore che le credenziali non sono corrette
**Post-condizioni:** L'attore è autenticato e accede alle proprie funzionalità assegnate
**Sequenza alternativa degli eventi:** 

## Sblocca Mezzo – Gabriele

**Nome:** Sblocca Mezzo
**ID:** IF-UT.04
**Breve descrizione:** L'Utente avvia la procedura di sblocco fisico del mezzo prenotato o disponibile; il sistema verifica le condizioni e abilita l'utilizzo del mezzo.
Attori primari
Utente
Attori secondari
Nessuno
**Precondizioni:** L'Utente è autenticato; l'Utente si trova in prossimità del mezzo; il mezzo è nello stato "Prenotato" dall'Utente corrente oppure nello stato "Disponibile".
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'Utente seleziona "Sblocca Mezzo" nell'applicazione.
2. Il sistema verifica che l'Utente si trovi entro la distanza massima consentita dal mezzo.
3. Il sistema invia il comando di sblocco al mezzo.
4. Il mezzo conferma l'avvenuto sblocco al sistema.
5. Il sistema aggiorna lo stato del mezzo a "In Uso" e registra l'inizio della corsa.
6. Il sistema notifica l'Utente che il mezzo è pronto all'uso.
Postcondizioni
Il mezzo è fisicamente sbloccato; lo stato del mezzo è aggiornato a "In Uso"; la corsa è registrata come avviata nel sistema.
Sequenze alternative
Comando Sblocca Fallito

**Nome:** Sblocca Mezzo: Comando Sblocca Fallito
**ID:** IF-UT.04.2
**Breve descrizione:** Il mezzo non risponde al comando di sblocco inviato dal sistema.
**Precondizioni:** Il mezzo non ha risposto allo sblocco.
Postcondizioni
Il mezzo rimane bloccato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 3 della sequenza principale.
2. Il sistema attende la conferma di sblocco dal mezzo.
3. Il sistema notifica l'Utente che non è stato possibile sbloccare il mezzo.

## Termina corsa – Flavio

**Nome:** Termina corsa
**ID:** UT.06
**Breve descrizione:** Il sistema consente all'utente autenticato di terminare la corsa in corso, verificando la posizione del mezzo e applicando le regole di fine corsa configurate dall'operatore, così da liberare il mezzo e addebitare il costo della sessione.
**Attori Primari:** Utente
**Attori Secondari:** ServizioGIS (BingMaps), ProviderPagamenti
**Precondizioni:** L'utente è autenticato alla piattaforma e ha una corsa attiva.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'utente seleziona "Termina e Paga" nella schermata Info Corsa.
2. Il sistema rileva la posizione corrente del mezzo tramite ServizioGIS.
3. Il sistema verifica che il mezzo si trovi all'interno di una Zona di Parcheggio.
4. Il sistema calcola il costo totale della corsa in base alla tariffa applicabile e alla durata della sessione.
5. Il sistema addebita l'importo calcolato tramite il metodo di pagamento associato all'account utente, tramite ProviderPagamenti.
6. Il sistema aggiorna lo stato del mezzo da "In uso" a "Disponibile".
7. Il sistema mostra all'utente il Riepilogo Corsa con durata, distanza percorsa e costo addebitato.
**Post-condizioni:** La corsa è terminata, il mezzo è liberato e reso disponibile, l'addebito è stato effettuato e il riepilogo è mostrato all'utente.
**Sequenza alternativa degli eventi:** MezzoFuoriZonaParcheggio, MezzoInZonaVietata, ErroreServizioGIS

**Nome:** Termina corsa: MezzoFuoriZonaParcheggio
**ID:** UT.06.1
**Breve descrizione:** Il sistema informa l'utente che il mezzo non si trova in una Zona di Parcheggio e applica la regola sanzionatoria configurata dall'operatore.
**Attori Primari:** Utente
**Attori Secondari:** ServizioGIS (BingMaps), ProviderPagamenti
**Precondizioni:** Il mezzo si trova fuori da qualsiasi Zona di Parcheggio al momento della richiesta di fine corsa.
Post-Condizioni
La corsa è terminata con applicazione della regola sanzionatoria (penale, divieto o avviso) configurata dall'operatore tramite OP.14.

**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 3 della sequenza principale.
2. Il sistema rileva che il mezzo non si trova in una Zona di Parcheggio.
3. Il sistema recupera la regola sanzionatoria configurata dall'operatore per i rilasci fuori zona (penale, divieto di fine corsa, o semplice avviso).
4a. Se la regola è "penale": il sistema informa l'utente dell'applicazione di una penale aggiuntiva e prosegue dal passo 4 della sequenza principale applicando la maggiorazione.
4b. Se la regola è "divieto": il sistema informa l'utente che non è possibile terminare la corsa fuori dalla Zona di Parcheggio e richiede di spostare il mezzo.
4c. Se la regola è "avviso": il sistema mostra un avviso all'utente e prosegue dal passo 4 della sequenza principale senza applicare penali.

**Nome:** Termina corsa: MezzoInZonaVietata
**ID:** UT.06.2
**Breve descrizione:** Il sistema informa l'utente che il mezzo si trova in una Zona Vietata e applica una penale obbligatoria prima di consentire la fine corsa.
**Attori Primari:** Utente
**Attori Secondari:** ServizioGIS (BingMaps), ProviderPagamenti
**Precondizioni:** Il mezzo si trova in una Zona Vietata al momento della richiesta di fine corsa.
Post-Condizioni
La corsa è terminata con applicazione della penale obbligatoria; il mezzo è liberato e l'addebito comprensivo di penale è stato effettuato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 3 della sequenza principale.
2. Il sistema rileva che il mezzo si trova in una Zona Vietata.
3. Il sistema notifica l'utente che il mezzo si trova in una Zona Vietata e che verrà applicata una penale obbligatoria.
4. Il sistema prosegue dal passo 4 della sequenza principale applicando la penale al costo totale della corsa..
**Nome:** Termina corsa: ErroreServizioGIS
**ID:** UT.06.4
**Breve descrizione:** Il sistema informa l'utente che non è possibile verificare la posizione del mezzo a causa di un errore di comunicazione con il ServizioGIS.
**Attori Primari:** Utente
**Attori Secondari:** ServizioGIS (BingMaps)
**Precondizioni:** Il ServizioGIS non è raggiungibile o restituisce un errore durante la richiesta della posizione.
Post-Condizioni
La corsa non viene terminata; l'utente è invitato a riprovare.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.
2. Il sistema rileva un errore di comunicazione con il ServizioGIS.
3. Il sistema notifica l'utente dell'impossibilità di verificare la posizione del mezzo.
4. Il sistema invita l'utente a riprovare.

Effetua Pagamento– Gabriele

**Nome:** EffettuaPagamento
**ID:** IF-UT.20
**Breve descrizione:** Al termine della corsa il sistema calcola l'importo dovuto e lo addebita automaticamente sul metodo di pagamento predefinito dell'Utente, senza richiedere alcuna azione manuale.
Attori primari
Utente
Attori secondari
Sistema di Pagamento Esterno
**Precondizioni:** Una corsa dell'Utente è appena terminata; l'Utente ha un metodo di pagamento predefinito registrato e valido.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando il sistema registra la fine della corsa.
2. Il sistema calcola la durata della corsa e l'importo dovuto in base alla tariffa applicabile.
3. Il sistema recupera il metodo di pagamento predefinito dell'Utente.
4. Il sistema trasmette la richiesta di addebito al Sistema di Pagamento Esterno.
5. Il Sistema di Pagamento Esterno autorizza e completa la transazione.
6. Il sistema genera e invia la ricevuta di pagamento all'Utente.
Postcondizioni
L'importo è addebitato; l'Utente riceve la ricevuta.
Sequenze alternative
PagamentoRifiutato

**Nome:** Effettua Pagamento: Pagamento Rifiutato
**ID:** IF-UT.20.1
**Breve descrizione:** Il Sistema di Pagamento Esterno rifiuta la transazione.
**Precondizioni:** Il Sistema di Pagamento Esterno ha restituito un esito negativo per la transazione.
Postcondizioni
Il pagamento non è andato a buon fine; l'Utente è notificato del problema.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 4 della sequenza principale.
2. Il sistema riceve l'esito negativo dal Sistema di Pagamento Esterno.
3. Il sistema notifica l'Utente del fallimento e lo invita ad aggiornare il metodo di pagamento.

## Definisce Zone vietate – Gabriele

**Nome:** DefinisciZonaVietata
**ID:** IF-AP.02
**Breve descrizione:** L'Amministrazione Pubblica definisce i confini geografici di una Zona Vietata; il sistema memorizza la zona e la applica attivamente impedendo l'utilizzo dei mezzi al suo interno.
Attori primari
Amministrazione Pubblica
Attori secondari
Nessuno
**Precondizioni:** L'Amministrazione Pubblica è autenticata con il ruolo appropriato nel sistema di back-office.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'Amministrazione Pubblica seleziona "Aggiungi Zona Vietata" nel pannello di gestione.
2. Il sistema visualizza la mappa interattiva dell'area di competenza.
3. L'Amministrazione Pubblica disegna il perimetro della zona sulla mappa definendo i vertici del poligono.
4. L'Amministrazione Pubblica conferma la creazione della zona.
5. Il sistema valida che il perimetro definito sia un poligono chiuso e non degenere.
6. Il sistema salva la Zona Vietata e la rende attiva.
7. Il sistema aggiorna la mappa visibile agli Utenti evidenziando la nuova zona.
Postcondizioni
La Zona Vietata è persistita nel sistema con il perimetro definito; il sistema la applica alla flotta.
Sequenze alternative
Perimetro Non Valido

**Nome:** Definisci Zona Vietata: Perimetro Non Valido
**ID:** IF-AP.02.1
**Breve descrizione:** Il perimetro disegnato non costituisce un poligono chiuso valido.
**Precondizioni:** Il poligono tracciato ha meno di 3 vertici oppure i lati si intersecano in modo non ammesso.
Postcondizioni
Nessuna zona è salvata; il sistema mantiene il form di creazione aperto.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 5 della sequenza principale.
2. Il sistema informa l'Amministrazione Pubblica che il perimetro definito non è valido.
3. Il sistema evidenzia sulla mappa il problema rilevato.
4. L'Amministrazione Pubblica può correggere il perimetro, tornando al passo 3 della sequenza principale.

## Definisce Zone di Parcheggio – Gabriele

**Nome:** Definisci Zona di Parcheggio
**ID:** IF-AP.03
**Breve descrizione:** L'Amministrazione Pubblica definisce una zona destinata al parcheggio dei mezzi; il sistema la rende visibile sulla mappa degli Utenti così da indirizzare il corretto rilascio dei mezzi.
Attori primari
Amministrazione Pubblica
Attori secondari
Nessuno
**Precondizioni:** L'Amministrazione Pubblica è autenticata con il ruolo appropriato.
Postcondizioni
La Zona Parcheggio è salvata e visibile sulla mappa degli Utenti; i mezzi parcheggiati al suo interno sono riconosciuti come correttamente posizionati.
Sequanza principale degli eventi
1. Il caso d'uso inizia quando l'Amministrazione Pubblica seleziona "Aggiungi Zona Parcheggio" nel pannello di gestione.
2. Il sistema visualizza la mappa interattiva dell'area di competenza con le zone esistenti.
3. L'Amministrazione Pubblica disegna il perimetro della zona parcheggio sulla mappa.
4. L'Amministrazione Pubblica conferma la creazione della zona.
5. Fintantochè la zona non è un poligono chiuso
5.1 include (Perimetro non Valido)
6. Il sistema verifica che la zona non si sovrapponga a una Zona Vietata esistente.
7. Il sistema salva la Zona Parcheggio e la pubblica sulla mappa degli Utenti.
Sequenze alternative
SovrapposizioneZonaVietata

**Nome:** Definisci Zona di Parcheggio: Sovrapposizione Zona Vietata
**ID:** IF-AP.03.1
**Breve descrizione:** Il perimetro della Zona Parcheggio si sovrappone parzialmente o totalmente a una Zona Vietata esistente.
**Precondizioni:** Il sistema ha rilevato un'intersezione tra il perimetro proposto e almeno una Zona Vietata già attiva.
Postcondizioni
Nessuna zona è salvata; il sistema mantiene il form di creazione aperto.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.
2. Il sistema evidenzia sulla mappa le aree di sovrapposizione con la Zona Vietata.
3. Il sistema informa l'Amministrazione Pubblica del conflitto rilevato.
4. L'Amministrazione Pubblica può ridefinire il perimetro per eliminare la sovrapposizione, tornando al passo 3 della sequenza principale.

## Salva Metodi di Pagamento – Flavio

**Nome:** Salva Metodi di Pagamento
**ID:** UT.12
**Breve descrizione:** Il sistema consente all'utente autenticato di salvare uno o più metodi di pagamento sul proprio account, così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati.
**Attori Primari:** Utente
**Attori Secondari:** ProviderPagamenti
**Precondizioni:** L'utente è autenticato alla piattaforma.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'utente accede alla sezione "Portafoglio" dal menu laterale.
2. Il sistema mostra i metodi di pagamento attualmente associati all'account utente e l'opzione per aggiungerne uno nuovo.
3. L'utente seleziona l'opzione per aggiungere un nuovo metodo di pagamento.
4. Il sistema mostra le tipologie di metodo di pagamento disponibili (Google Pay, Apple Pay, PayPal, carta di credito).
5. L'utente seleziona la tipologia desiderata e inserisce i dati richiesti.
6. Il sistema valida i dati inseriti tramite ProviderPagamenti.
7. Il sistema salva il nuovo metodo di pagamento sull'account utente.
8. Se l'utente non ha altri metodi di pagamento salvati, il sistema imposta automaticamente il nuovo metodo come predefinito.
9. Il sistema mostra un messaggio di conferma all'utente.

**Post-condizioni:** Il nuovo metodo di pagamento è stato salvato sull'account utente. Se era il primo metodo salvato, è stato impostato come predefinito.
**Sequenza alternativa degli eventi:** DatiNonValidi, MetodoGiàPresente, ImpostaPredefinito

**Nome:** Salva Metodi di Pagamento: DatiNonValidi
**ID:** UT.12.1
**Breve descrizione:** Il sistema informa l'utente che i dati del metodo di pagamento inseriti non sono validi.
**Attori Primari:** Utente
**Attori Secondari:** Provider di pagamento
**Precondizioni:** ProviderPagamenti ha restituito un esito negativo nella validazione dei dati inseriti.
**Post-condizioni:** Nessuna. Il metodo di pagamento non viene salvato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.
2. ProviderPagamenti restituisce un errore di validazione.
3. Il sistema informa l'utente che i dati inseriti non sono validi e richiede di correggerli. 4. Torna al passo 5 della sequenza principale.

**Nome:** Salva Metodi di Pagamento: MetodoGiàPresente
**ID:** UT.12.2
**Breve descrizione:** Il sistema informa l'utente che il metodo di pagamento inserito è già associato al proprio account.
**Attori Primari:** Utente
**Attori Secondari:** Provider di pagamento
**Precondizioni:** Il metodo di pagamento inserito dall'utente è già salvato sull'account.
**Post-condizioni:** Nessuna. Il metodo di pagamento non viene duplicato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.
2. Il sistema rileva che il metodo di pagamento è già associato all'account utente.
3. Il sistema informa l'utente che il metodo di pagamento è già presente e non viene salvato nuovamente.

**Nome:** Salva Metodi di Pagamento: ImpostaPredefinito
**ID:** UT.12.3
**Breve descrizione:** Il sistema consente all'utente di impostare un metodo di pagamento già salvato come predefinito.
**Attori Primari:** Utente
**Attori Secondari:** Nessuno
**Precondizioni:** L'utente ha già almeno un metodo di pagamento salvato sull'account e vuole cambiare quello predefinito.
**Post-condizioni:** Il metodo di pagamento selezionato è stato impostato come predefinito; il precedente predefinito non lo è più
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia al passo 2 della sequenza principale.
2. L'utente seleziona un metodo di pagamento già presente e sceglie l'opzione "Imposta come predefinito".
3. Il sistema aggiorna il metodo di pagamento predefinito e mostra un messaggio di conferma.

Definisce tariffa– Flavio
**Nome:** Definisce Tariffa
**ID:** OP.07
**Breve descrizione:** Il sistema consente all'operatore autenticato di definire una nuova tariffa per una specifica tipologia di mezzo, specificando il costo al minuto e il costo al chilometro, così da permettere la configurazione del modello di costo del servizio.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore è autenticato alla piattaforma e non esiste già una tariffa definita per la tipologia di mezzo selezionata.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'operatore accede alla sezione "Tariffe e Promozioni" dalla Dashboard Operatore.
2. Il sistema mostra le tariffe attualmente definite per ciascuna tipologia di mezzo disponibile.
3. L'operatore seleziona la tipologia di mezzo per cui intende definire una nuova tariffa (monopattino, bicicletta, automobile).
4. Il sistema mostra il form di inserimento con i campi: costo al minuto e costo al chilometro.
5. L'operatore inserisce i valori richiesti.
6. Il sistema valida i dati inseriti verificando che i valori siano numerici e maggiori di zero.
7. Il sistema salva la nuova tariffa associandola alla tipologia di mezzo selezionata.
8. Il sistema mostra un messaggio di conferma all'operatore.
**Post-condizioni:** La nuova tariffa è stata salvata nel sistema e sarà applicata alle corse successive effettuate con la tipologia di mezzo selezionata.
**Sequenza alternativa degli eventi:** DatiNonValidi, TariffaGiàEsistente, Annulla

**Nome:** Definisce Tariffa: DatiNonValidi
**ID:** OP.07.1
**Breve descrizione:** Il sistema informa l'operatore che i valori inseriti per la tariffa non sono validi.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha inserito valori non numerici o minori o uguali a zero in uno o più campi del form.
**Post-condizioni:** Nessuna. La tariffa non viene salvata.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.
2. Il sistema rileva che uno o più valori inseriti non sono numerici o sono minori o uguali a zero.
3. Il sistema informa l'operatore dell'errore specificando i campi non validi.
4. Torna al passo 5 della sequenza principale.

**Nome:** Definisce Tariffa: TariffaGiàEsistente
**ID:** OP.07.2
**Breve descrizione:** Il sistema informa l'operatore che esiste già una tariffa definita per la tipologia di mezzo selezionata.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** Esiste già una tariffa associata alla tipologia di mezzo selezionata dall'operatore.
**Post-condizioni:** Nessuna. La tariffa esistente non viene sovrascritta.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 3 della sequenza principale.
2. Il sistema rileva che esiste già una tariffa per la tipologia di mezzo selezionata.
3. Il sistema informa l'operatore che è già presente una tariffa per quel mezzo e suggerisce di utilizzare la funzione "Modifica Tariffa" (OP.08).

## Modifica stato mezzi – Flavio

**Nome:** Modifica Stato Mezzi
**ID:** OP.04
**Breve descrizione:** Il sistema consente all'operatore autenticato di modificare lo stato di un mezzo della flotta, così da nasconderlo o mostrarlo sulla Mappa Utente e gestire il ciclo operativo del veicolo.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore è autenticato alla piattaforma e il mezzo selezionato esiste nella flotta.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'operatore accede alla sezione "Gestisci Utenti" dalla Dashboard Operatore.
2. Il sistema mostra la Mappa Operatore con la lista dei mezzi della flotta e il loro stato corrente.
3. L'operatore seleziona il mezzo di cui intende modificare lo stato.
4. Il sistema mostra lo stato corrente del mezzo e le opzioni di stato selezionabili tra: Disponibile, In manutenzione, Fuori servizio.
5. L'operatore seleziona il nuovo stato desiderato.
6. Il sistema verifica che la transizione di stato richiesta sia consentita.
7. Il sistema aggiorna lo stato del mezzo.
8. Il sistema mostra un messaggio di conferma all'operatore.
**Post-condizioni:** Lo stato del mezzo è stato aggiornato. Se il nuovo stato è "In manutenzione" o "Fuori servizio" il mezzo non è più visibile sulla Mappa Utente; se il nuovo stato è "Disponibile" il mezzo è nuovamente visibile sulla Mappa Utente
**Sequenza alternativa degli eventi:** TransizioneNonConsentita, MezzoInUso, Annulla

**Nome:** Modifica Stato Mezzi: TransizioneNonConsentita
**ID:** OP.04.1
**Breve descrizione:** Il sistema informa l'operatore che la transizione di stato richiesta non è consentita.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha selezionato una transizione di stato non consentita dalle regole del sistema.
**Post-condizioni:** Nessuna. Lo stato del mezzo non viene modificato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.
2. Il sistema rileva che la transizione di stato richiesta non è consentita.
3. Il sistema informa l'operatore che la transizione non è possibile e mostra le opzioni di stato disponibili per il mezzo selezionato.
4. Torna al passo 5 della sequenza principale.

**Nome:** Modifica Stato Mezzi: MezzoInUso
**ID:** OP.04.2
**Breve descrizione:** Il sistema informa l'operatore che il mezzo selezionato è attualmente in uso da un utente e non può essere modificato.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** Il mezzo selezionato ha stato "In uso" o "Prenotato" al momento della richiesta di modifica.
**Post-condizioni:** Nessuna. Lo stato del mezzo non viene modificato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.
2. Il sistema rileva che il mezzo è attualmente in uso o prenotato da un utente.
3. Il sistema informa l'operatore che non è possibile modificare lo stato del mezzo mentre è in uso o prenotato

**Nome:** Modifica Stato Mezzi: Annulla
**ID:** OP.04.3
**Breve descrizione:** Il sistema annulla la procedura di modifica dello stato del mezzo.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha avviato la procedura di modifica dello stato ma decide di interromperla.
**Post-condizioni:** Nessuna. Lo stato del mezzo non viene modificato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa può iniziare in qualsiasi momento durante la sequenza principale.
2. L'operatore seleziona "Annulla" o abbandona la schermata di modifica.
3. Il sistema scarta le modifiche e riporta l'operatore alla Dashboard Operatore.

## Visualizza Mappa Operatore – Francesco

**Nome:** Visualizza Mappa Operatore
**ID:** OP.01
**Breve descrizione:** L'operatore visualizza la Mappa Operatore, costruita sulla base cartografica fornita dal ServizioGIS, per consultare la dislocazione di mezzi e stazioni, al fine di pianificare le operazioni di redistribuzione.
**Attori Primari:** Operatore
**Attori Secondari:** ServizioGIS (BingMaps)
**Precondizioni:** L'operatore è autenticato nel sistema e si trova nella Dashboard Operatore.
Sequenza principale degli eventi
1. L'operatore seleziona la funzione "Mappa Operatore" dalla Dashboard.
2. Il sistema richiede i dati aggiornati di mezzi e stazioni al backend e interroga il ServizioGIS per ottenere la base cartografica.
3. Il sistema riceve i dati dal backend e la base cartografica dal ServizioGIS, quindi visualizza la Mappa Operatore con la posizione dei mezzi e delle stazioni.
4. L'operatore consulta la mappa e individua le aree di interesse per la redistribuzione.
5. L'operatore può selezionare un mezzo o una stazione per visualizzarne i dettagli.
**Post-condizioni:** La Mappa Operatore è visualizzata correttamente con i dati aggiornati di mezzi e stazioni.
**Sequenza alternativa degli eventi:** ErroreCaricamento, ErroreServizioGIS

**Nome:** Visualizza Mappa Operatore: ErroreCaricamento
**ID:** OP.01.1
**Breve descrizione:** Il sistema non riesce a recuperare i dati di mezzi e stazioni dal backend.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha richiesto la visualizzazione della Mappa Operatore.
**Post-condizioni:** Nessuna. La Mappa Operatore non viene visualizzata.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.
2. Il sistema non riceve risposta dal backend o riceve un errore.
3. Il sistema informa l'operatore dell'impossibilità di caricare la Mappa Operatore e suggerisce di riprovare.

**Nome:** Visualizza Mappa Operatore: ErroreServizioGIS DA TOGLIERE
**ID:** OP.01.2
**Breve descrizione:** Il sistema non riesce a contattare il ServizioGIS o non riceve una base cartografica valida.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha richiesto la visualizzazione della Mappa Operatore.
**Post-condizioni:** Nessuna. La Mappa Operatore non viene visualizzata.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.
2. Il sistema non riceve risposta dal ServizioGIS o riceve dati cartografici non validi.
3. Il sistema informa l'operatore dell'impossibilità di caricare la base cartografica e suggerisce di riprovare più tardi.

## Definisce Zona Operativa – Francesco

**Nome:** Definisce Zona Operativa
**ID:** OP.03
**Breve descrizione:** Il sistema consente all'operatore autenticato di definire una nuova zona operativa, delimitando, tramite il ServizioGIS, l'area geografica entro cui il servizio di mobilità è attivo, così da permettere agli utenti di noleggiare e rilasciare i mezzi esclusivamente all'interno della zona.
**Attori Primari:** Operatore
**Attori Secondari:** ServizioGIS (BingMaps)
**Precondizioni:** L'operatore è autenticato alla piattaforma e si trova nella Dashboard Operatore.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'operatore accede alla sezione "Gestisci Zone" dalla Dashboard Operatore.
2. Il sistema mostra la Mappa Operatore con le zone operative attualmente definite.
3. L'operatore seleziona la funzione "Definisci Nuova Zona Operativa".
4. Il sistema interroga il ServizioGIS per caricare la base cartografica e abilita la modalità di disegno sulla mappa.
5. L'operatore traccia il perimetro della nuova zona operativa selezionando i punti sulla mappa.
6. L'operatore conferma il perimetro tracciato per la zona.
7. Il sistema valida la zona verificando che il perimetro sia chiuso e non si sovrapponga ad altre zone operative esistenti.
8. Il sistema salva la nuova zona operativa.
9. Il sistema mostra un messaggio di conferma all'operatore.
**Post-condizioni:** La nuova zona operativa è stata salvata nel sistema e gli utenti potranno noleggiare e rilasciare i mezzi esclusivamente al suo interno.
**Sequenza alternativa degli eventi:** PerimetroNonValido, ZonaSovrapposta, ErroreServizioGIS, Annulla

**Nome:** Definisce Zona Operativa: PerimetroNonValido
**ID:** OP.03.1
**Breve descrizione:** Il sistema informa l'operatore che il perimetro tracciato non è valido.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha tracciato un perimetro che non è chiuso o presenta auto-intersezioni.
**Post-condizioni:** Nessuna. La zona operativa non viene salvata.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 7 della sequenza principale.
2. Il sistema rileva che il perimetro tracciato non è chiuso o presenta auto-intersezioni.
3. Il sistema informa l'operatore dell'errore e suggerisce di correggere il perimetro.
4. Torna al passo 5 della sequenza principale.

**Nome:** Definisce Zona Operativa: ZonaSovrapposta
**ID:** OP.03.2
**Breve descrizione:** Il sistema informa l'operatore che la nuova zona si sovrappone a una zona operativa esistente.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** Il perimetro della nuova zona si sovrappone, anche parzialmente, ad almeno una zona operativa già definita.
**Post-condizioni:** Nessuna. La nuova zona operativa non viene salvata.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 7 della sequenza principale.
2. Il sistema rileva la sovrapposizione con una zona operativa esistente.
3. Il sistema informa l'operatore della sovrapposizione ed evidenzia sulla mappa la zona in conflitto.
4. Torna al passo 5 della sequenza principale.

**Nome:** Definisce Zona Operativa: Annulla
**ID:** OP.03.3
**Breve descrizione:** Il sistema annulla la procedura di definizione della zona operativa.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha avviato la procedura di definizione di una zona operativa ma decide di interromperla.
**Post-condizioni:** Nessuna. La zona operativa non viene salvata.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa può iniziare in qualsiasi momento durante la sequenza principale.
2. L'operatore seleziona "Annulla" o abbandona la modalità di disegno.
3. Il sistema scarta il perimetro tracciato e riporta l'operatore alla sezione "Gestisci Zone".

**Nome:** Definisce Zona Operativa: ErroreServizioGIS
**ID:** OP.03.4
**Breve descrizione:** Il sistema informa l'operatore che non è possibile completare la definizione della zona operativa a causa di un errore di comunicazione con il ServizioGIS.
**Attori Primari:** Operatore
**Attori Secondari:** ServizioGIS (BingMaps)
**Precondizioni:** Il ServizioGIS non è raggiungibile o restituisce un errore durante il caricamento della base cartografica o la validazione del perimetro.
**Post-condizioni:** Nessuna. La zona operativa non viene salvata.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa può iniziare dopo il passo 4 o il passo 7 della sequenza principale.
2. Il sistema rileva un errore di comunicazione con il ServizioGIS.
3. Il sistema notifica l'operatore dell'impossibilità di completare l'operazione.
4. Il sistema propone di riprovare l'operazione.

## Aggiunge Mezzo – Francesco

**Nome:** Aggiunge Mezzo
**ID:** OP.12
**Breve descrizione:** Il sistema consente all'operatore autenticato di aggiungere un nuovo mezzo alla flotta, specificando tipologia, identificativo, posizione iniziale e stato, così da renderlo disponibile per il noleggio da parte degli utenti.
**Attori Primari:** Operatore
**Attori Secondari:** ServizioGIS (BingMaps)
**Precondizioni:** L'operatore è autenticato alla piattaforma e si trova nella Dashboard Operatore.
Sequenza principale degli eventi
1. Il caso d'uso inizia quando l'operatore accede alla sezione "Gestisci Mezzi" dalla Dashboard Operatore.
2. Il sistema mostra la lista dei mezzi attualmente presenti nella flotta.
3. L'operatore seleziona la funzione "Aggiungi Nuovo Mezzo".
4. Il sistema permette di inserire i campi: tipologia (monopattino, bicicletta, automobile), identificativo, posizione iniziale e stato iniziale.
5. L'operatore inserisce i dati richiesti e seleziona la posizione iniziale sulla mappa.
6. L'operatore conferma i dati inseriti.
7. Il sistema valida i dati verificando che l'identificativo sia univoco e che la posizione ricada all'interno di una zona operativa.
8. Il sistema salva il nuovo mezzo associandolo alla flotta.
9. Il sistema mostra un messaggio di conferma all'operatore.
**Post-condizioni:** Il nuovo mezzo è stato salvato nel sistema e risulta disponibile sulla Mappa Utente in base allo stato impostato.
**Sequenza alternativa degli eventi:** DatiNonValidi, IdentificativoEsistente, Annulla

**Nome:** Aggiunge Mezzo: DatiNonValidi
**ID:** OP.12.1
**Breve descrizione:** Il sistema informa l'operatore che i dati inseriti per il nuovo mezzo non sono validi.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha inserito uno o più campi non validi (es. tipologia non riconosciuta, identificativo vuoto, posizione fuori dalle zone operative).
**Post-condizioni:** Nessuna. Il mezzo non viene salvato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 7 della sequenza principale.
2. Il sistema rileva che uno o più dati inseriti non sono validi.
3. Il sistema informa l'operatore dell'errore specificando i campi non validi.
4. Torna al passo 5 della sequenza principale.

**Nome:** Aggiunge Mezzo: IdentificativoEsistente
**ID:** OP.12.2
**Breve descrizione:** Il sistema informa l'operatore che l'identificativo inserito per il nuovo mezzo è già in uso.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** Esiste già un mezzo nella flotta con lo stesso identificativo inserito dall'operatore.
**Post-condizioni:** Nessuna. Il mezzo non viene salvato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa inizia dopo il passo 7 della sequenza principale.
2. Il sistema rileva che l'identificativo è già associato a un mezzo esistente.
3. Il sistema informa l'operatore dell'errore e suggerisce di inserire un identificativo diverso.
4. Torna al passo 5 della sequenza principale.

**Nome:** Aggiunge Mezzo: Annulla
**ID:** OP.12.3
**Breve descrizione:** Il sistema annulla la procedura di aggiunta del mezzo.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore ha avviato la procedura di aggiunta di un mezzo ma decide di interromperla.
**Post-condizioni:** Nessuna. Il mezzo non viene salvato.
**Sequenza alternativa degli eventi:** 1. La sequenza alternativa può iniziare in qualsiasi momento durante la sequenza principale.
2. L'operatore seleziona "Annulla" o abbandona il form di inserimento.
3. Il sistema scarta i dati inseriti e riporta l'operatore alla sezione "Gestisci Mezzi".

## Dismette Mezzo – Francesco

**Nome:** Dismette Mezzo
**ID:** OP.13
**Breve descrizione:** Il sistema consente all'operatore autenticato di dismettere un mezzo precedentemente censito, rimuovendone la disponibilità per l'assegnazione a nuove missioni e mantenendone lo storico ai fini di consultazione.
**Attori Primari:** Operatore
**Attori Secondari:** ServizioGIS
**Precondizioni:** L'operatore deve essere autenticato nel sistema e il mezzo da dismettere deve essere già censito e non assegnato ad alcuna missione attiva.
**Sequenza principale:** L'operatore richiede al sistema di dismettere un mezzo selezionato dall'elenco dei mezzi censiti. Il sistema, tramite il ServizioGIS, verifica che il mezzo non sia attualmente impegnato in missioni in corso e ne richiede conferma all'operatore. L'operatore conferma la dismissione. Il sistema aggiorna lo stato del mezzo a "dismesso", lo rimuove dall'elenco dei mezzi disponibili e mantiene lo storico delle informazioni associate.
**Post-condizioni:** Il mezzo è registrato come dismesso nel sistema, non risulta più disponibile per l'assegnazione a nuove missioni e i dati storici relativi al mezzo rimangono consultabili.
**Sequenza alternativa degli eventi:** MezzoInUso, MezzoNonEsistente, Annulla

**Nome:** Dismette Mezzo: MezzoInUso
**ID:** OP.13.1
**Breve descrizione:** Il sistema informa l'operatore che il mezzo selezionato è attualmente impegnato in una missione e non può essere dismesso.
**Attori Primari:** Operatore
**Attori Secondari:** ServizioGIS
**Precondizioni:** L'operatore deve essere autenticato nel sistema e il mezzo selezionato risulta assegnato a una missione attiva.
**Post-condizioni:** Lo stato del mezzo resta invariato e l'operatore rimane nella sezione di gestione dei mezzi.
**Sequenza alternativa degli eventi:** 1. Il sistema, tramite il ServizioGIS, rileva che il mezzo selezionato è impegnato in una missione in corso. 2. Il sistema notifica all'operatore l'impossibilità di dismettere il mezzo, indicandone la causa. 3. L'operatore prende visione del messaggio e ritorna alla sezione di gestione dei mezzi.

**Nome:** Dismette Mezzo: MezzoNonEsistente
**ID:** OP.13.2
**Breve descrizione:** Il sistema informa l'operatore che il mezzo selezionato non risulta più disponibile nel sistema.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore deve essere autenticato nel sistema e il mezzo selezionato risulta non più presente nell'elenco dei mezzi censiti.
**Post-condizioni:** Lo stato dei mezzi resta invariato e l'operatore rimane nella sezione di gestione dei mezzi.
**Sequenza alternativa degli eventi:** 1. Il sistema rileva che il mezzo selezionato non è più presente nell'elenco dei mezzi censiti. 2. Il sistema notifica all'operatore l'impossibilità di procedere alla dismissione, indicandone la causa. 3. L'operatore prende visione del messaggio e ritorna alla sezione di gestione dei mezzi.

**Nome:** Dismette Mezzo: Annulla
**ID:** OP.13.3
**Breve descrizione:** Il sistema annulla la procedura di dismissione del mezzo.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore deve essere autenticato nel sistema e aver avviato la procedura di dismissione di un mezzo.
**Post-condizioni:** Lo stato del mezzo resta invariato e l'operatore viene riportato alla sezione di gestione dei mezzi.
**Sequenza alternativa degli eventi:** 1. L'operatore, durante la procedura di dismissione, sceglie di annullare l'operazione. 2. Il sistema scarta le modifiche in corso e riporta l'operatore alla sezione "Gestisce Mezzi".

## Definisce Regole Fine Corsa – Francesco

**Nome:** 
**Definisce Regole Fine Corsa:** 
**ID:** OP.14
**Breve descrizione:** L'operatore definisce le regole che determinano la corretta conclusione di una corsa, specificando i vincoli relativi alla posizione di rilascio del mezzo (zona di parcheggio consentita) e alle condizioni necessarie affinché la corsa possa essere chiusa con successo.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore deve essere autenticato nel sistema e deve aver selezionato la funzione di configurazione delle regole di fine corsa.
**Sequenza principale:** 1. L'operatore accede alla sezione di configurazione delle regole di fine corsa.
2. Il sistema mostra all'operatore le zone di parcheggio disponibili e i parametri configurabili.
3. L'operatore seleziona le zone di parcheggio valide per la chiusura della corsa e imposta i vincoli aggiuntivi (es. stato del mezzo, livello batteria minimo, posizionamento corretto).
4. L'operatore conferma le regole definite.
5. Il sistema valida i parametri inseriti e salva la nuova configurazione delle regole di fine corsa.
6. Il sistema notifica all'operatore l'avvenuta definizione delle regole.

**Post-condizioni:** Le nuove regole di fine corsa sono memorizzate nel sistema e vengono applicate a tutte le corse successive.
**Sequenza alternativa degli eventi:** ZonaNonValida, ParametriNonValidi, Annulla

**Nome:** ZonaNonValida
**ID:** OP.14.1
**Breve descrizione:** L'operatore tenta di impostare come valida per la fine corsa una zona che non risulta classificata come zona di parcheggio.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore deve essere autenticato nel sistema e aver avviato la configurazione delle regole di fine corsa.
**Post-condizioni:** Le regole di fine corsa non vengono aggiornate e l'operatore viene riportato alla schermata di selezione delle zone.
**Sequenza alternativa degli eventi:** 1. L'operatore seleziona una zona non classificata come zona di parcheggio.
2. Il sistema verifica la natura della zona selezionata e rileva che non è valida come zona di fine corsa.
3. Il sistema mostra un messaggio di errore all'operatore e ripristina la selezione precedente, consentendogli di scegliere nuovamente.

**Nome:** ParametriNonValidi
**ID:** OP.14.2
**Breve descrizione:** L'operatore inserisce parametri non validi nella configurazione delle regole di fine corsa (es. livello batteria minimo negativo o fuori intervallo).
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore deve essere autenticato nel sistema e aver avviato la configurazione delle regole di fine corsa.
**Post-condizioni:** Le regole di fine corsa non vengono salvate e l'operatore viene invitato a correggere i valori inseriti.
**Sequenza alternativa degli eventi:** 1. L'operatore conferma le regole inserendo uno o più parametri non validi.
2. Il sistema rileva la presenza di valori fuori dagli intervalli ammessi.
3. Il sistema mostra un messaggio di errore evidenziando i campi con valori non validi.
4. Il sistema riporta l'operatore alla schermata di configurazione mantenendo i valori validi già inseriti.

**Nome:** Annulla
**ID:** OP.14.3
**Breve descrizione:** L'operatore annulla la procedura di definizione delle regole di fine corsa prima della conferma.
**Attori Primari:** Operatore
**Attori Secondari:** Nessuno
**Precondizioni:** L'operatore deve essere autenticato nel sistema e aver avviato la configurazione delle regole di fine corsa.
**Post-condizioni:** Le regole di fine corsa restano invariate e l'operatore viene riportato alla schermata principale di configurazione.
**Sequenza alternativa degli eventi:** 1. L'operatore, durante la procedura di definizione, sceglie di annullare l'operazione.
2. Il sistema richiede una conferma all'operatore.
3. L'operatore conferma l'annullamento.
4. Il sistema scarta le modifiche e riporta l'operatore alla schermata precedente senza salvare alcuna nuova regola.

Altro

# System Architecture

**Diagramma delle Componenti:** Riportare il diagramma delle Componenti evidenziando le interfacce utilizzate
**Specifica delle componenti:** 
**Specifica delle interfacce:** 

# Detailed Product Design

**Diagramma delle Classi:** 
**Specifiche delle Classi:** 
**Diagrammi di Sequenza:** 

# Data modeling and design

Qui va fornita la specifica di tutti i dati e le informazioni scambiate dal sistema in corso di realizzazione con l’utenza di riferimento e/o gli eventuali altri sistemi con cui esso comunica. Deve essere descritto il modello logico della base di dati e la sua struttura fisica.
**Modello logico del Database:** 
**Struttura fisica del Database:** 
