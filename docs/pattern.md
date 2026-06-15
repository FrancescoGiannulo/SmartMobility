# I Pattern Software
*Ingegneria del Software — Vita Santa Barletta, Danilo Caivano, Antonio Piccinno*

---

## Indice

1. [Definizione di Pattern](#definizione-di-pattern)
2. [Definizione Formale](#definizione-formale)
3. [Caratteristiche Comuni](#caratteristiche-comuni)
4. [Categorie di Pattern](#categorie-di-pattern)
5. [Design Pattern — Classificazione Completa](#design-pattern--classificazione-completa)
6. [Pattern Creazionali](#pattern-creazionali)
   - [Singleton](#singleton)
   - [Abstract Factory](#abstract-factory)
7. [Pattern Strutturali](#pattern-strutturali)
   - [Facade](#facade)
   - [Adapter](#adapter)
8. [Pattern Comportamentali](#pattern-comportamentali)
   - [Observer](#observer)
9. [Pattern J2EE / Web](#pattern-j2ee--web)
   - [Front Controller](#front-controller)
   - [Business Object](#business-object)
   - [Transfer Object](#transfer-object)
   - [Data Access Object](#data-access-object)
10. [Riferimenti](#riferimenti)

---

## Definizione di Pattern

> *"Un pattern è un'idea che si è rivelata utile in un contesto pratico e probabilmente sarà utile in altri."*
> — Martin Fowler

> *"Ogni pattern è una regola che esprime una relazione tra: un Contesto, un Problema Ricorrente e una Soluzione."*
> — Christopher Alexander

### I tre elementi di un pattern

| Elemento | Descrizione |
|----------|-------------|
| **Contesto** | Ambiente, circostanze o condizioni in relazione tra loro che caratterizzano un problema |
| **Problema** | Situazione che necessita uno studio e una soluzione; può essere specificato da un insieme di coppie causa/effetto |
| **Soluzione** | Modalità per superare il problema nello specifico contesto |

```
      Contesto
     /        \
    /          \
Problema ---- Soluzione
```

---

## Definizione Formale

Un **pattern software** è:
- La descrizione strutturata di una soluzione esemplare ad un problema (software) ricorrente
- Descritto in forma standard, in modo che possa essere facilmente condiviso e riusato

### Struttura standard di un pattern

```
Nome
├── Contesto
├── Problema
├── Soluzione
└── Conseguenze
```

---

## Caratteristiche Comuni

- Si basano sull'**esperienza**
- Sono scritti in maniera **strutturata**
- Esistono a **diversi livelli di astrazione**
- Si prestano a **continui miglioramenti**
- Sono **artefatti riusabili**
- Esprimono **best-practices**
- Possono essere **usati insieme** per risolvere problemi più grandi
- **Evitano di reinventare la ruota**

---

## Categorie di Pattern

### Cluster

I pattern possono essere raggruppati in **macro-categorie** (dette *cluster*), ciascuna contenente pattern orientati a risolvere problematiche similari. I cluster possono essere ulteriormente suddivisi in sottocategorie.

### Categorie per livello di astrazione (sviluppo software)

```
Pattern Software
├── Pattern Architetturali (Stili Architetturali)   ← alto livello
├── Pattern di Progetto (Design Pattern)             ← medio livello
└── Pattern di Implementazione (Idiomi)              ← basso livello
```

#### Pattern Architetturali (Stili Architetturali)
- Descrivono lo **schema organizzativo della struttura** di un sistema software
- Individuano le parti del sistema a cui sono associate responsabilità omogenee
- Descrivono le **relazioni** tra i diversi sottosistemi
- Esprimono un particolare problema e presentano uno schema generico per la soluzione
- Descrivono una **classe di architetture**
- *Esempi*: Layers, Client/Server, MVC, ...

#### Pattern di Progetto (Design Pattern)
- Si riferiscono alle problematiche legate al **progetto object-oriented** (scomposizione del sistema in oggetti)
- Agevolano il **riuso di soluzioni architetturali** note
- Rendono accessibili tecniche di progettazione universalmente riconosciute come valide
- Aiutano i progettisti a operare **scelte consapevoli** tra le varie alternative
- *Esempi*: Singleton, Adapter, Proxy, Observer, Facade, ...

**4 elementi fondamentali di un design pattern:**

| Elemento | Descrizione |
|----------|-------------|
| **Nome** | Descrive sinteticamente le funzionalità; permette di identificare il pattern e condividere idee ad alto livello di astrazione |
| **Problema** | Descrive la situazione a cui applicare il pattern e le condizioni necessarie al suo utilizzo |
| **Soluzione** | Descrive in modo astratto come il pattern risolve il problema (elementi, responsabilità, collaborazioni) |
| **Conseguenze** | Descrive risultati e vincoli dell'applicazione del pattern (fondamentali per valutare vantaggi e svantaggi) |

#### Pattern di Implementazione (Idiomi)
- Pattern di **basso livello**, specifico di un linguaggio di programmazione
- Descrive come implementare aspetti particolari usando caratteristiche specifiche di un certo linguaggio

### Pattern Language (Linguaggio di Pattern)

I pattern **non sono tra loro indipendenti**:
- Alcuni sono **alternativi** — "ne uso uno oppure l'altro"
- Alcuni sono **sinergici** — "se ne uso uno è utile usare anche l'altro"
- Alcuni possono essere usati in **gruppi più complessi**

Un **pattern language** è una famiglia di pattern correlati con una discussione sulle loro correlazioni.  
*Esempi*: linguaggio di pattern per la sicurezza, per sistemi distribuiti.

### Ruolo dei pattern software

| Ruolo | Descrizione |
|-------|-------------|
| Deposito di conoscenza | Raccolgono esperienza collettiva |
| Best-practices | Esempi di buone pratiche |
| Linguaggio comune | Per discutere problemi di progettazione |
| Standardizzazione | Aiuto alla standardizzazione |
| Miglioramento continuo | Sorgente di miglioramento iterativo |
| Generalità | Incoraggiamento alla generalità |

**Ruolo principale** nell'ambito delle architetture software:
- **Riduzione del rischio**
- **Incremento della produttività**, della standardizzazione e della qualità

---

## Design Pattern — Classificazione Completa

### Pattern Creazionali
> Risolvono problemi inerenti il **processo di creazione di oggetti**

| Design Pattern | Aspetto variabile |
|----------------|------------------|
| **Factory Method** | Quale sotto-classe viene istanziata |
| **Abstract Factory** | Famiglie di oggetti |
| **Builder** | Modo in cui un oggetto composito viene creato |
| **Prototype** | Quale classe di un oggetto viene istanziata |
| **Singleton** | Unica istanza di una classe |

### Pattern Strutturali
> Risolvono problemi inerenti la **composizione di classi o di oggetti**

| Design Pattern | Aspetto variabile |
|----------------|------------------|
| **Adapter** | Interfaccia di un oggetto |
| **Bridge** | Implementazione di un oggetto |
| **Composite** | Struttura e composizione di un oggetto |
| **Decorator** | Responsabilità di un oggetto senza sotto-classi |
| **Façade** | Interfaccia a un sotto-sistema |
| **Flyweight** | Risorse impiegate per la memorizzazione di oggetti |
| **Proxy** | Come accedere a un oggetto; localizzazione di un oggetto |

### Pattern Comportamentali
> Risolvono problemi inerenti le **modalità di interazione e distribuzione delle responsabilità** tra classi o oggetti

| Design Pattern | Aspetto variabile |
|----------------|------------------|
| **Chain of Responsibility** | Oggetto che può esaudire una richiesta |
| **Command** | Quando e come una richiesta viene esaudita |
| **Interpreter** | Grammatica e interpretazione di un linguaggio |
| **Iterator** | Accesso e modalità di scansione degli elementi di un insieme di oggetti |
| **Mediator** | Come e quali oggetti interagiscono tra loro |
| **Memento** | Quali informazioni private vengono memorizzate esternamente a un oggetto e quando |
| **Observer** | Oggetti che dipendono da un altro oggetto; come gli oggetti dipendenti vengono aggiornati |
| **State** | Stati di un oggetto |
| **Strategy** | Un algoritmo |
| **Template Method** | Passi di un algoritmo |
| **Visitor** | Operazioni applicabili senza cambiare le classi degli oggetti |

---

## Pattern Creazionali

---

### Singleton

**Categoria**: Creazionale

#### Scopo
Assicurare che una classe abbia **una sola istanza** e fornire un **punto d'accesso globale** a tale istanza.  
L'unica istanza deve poter essere estesa attraverso la definizione di sotto-classi, e i client devono essere in grado di utilizzare le istanze estese senza dover modificare il proprio codice.

#### Problema
È importante poter assicurare che per alcune classi esista una sola istanza.

> **Esempio**: in un sistema potrebbero esistere più stampanti, ma potrebbe essere presente soltanto **una coda di stampa**.

#### Soluzione
- Fare in modo che la **classe stessa** abbia la responsabilità di creare le proprie istanze
- La classe assicura che nessun'altra istanza possa essere creata (intercettando le richieste di creazione)
- Fornisce un modo semplice per accedere all'istanza tramite l'operazione `Instance()`

#### Struttura

```
┌─────────────────────────────────────┐
│            Singleton                │
├─────────────────────────────────────┤
│  - instance: Singleton              │
├─────────────────────────────────────┤
│  + Instance(): Singleton            │
│  + SingletonOperation()             │
│  + GetSingletonData()               │
└─────────────────────────────────────┘
   I Client accedono a Singleton
   SOLO attraverso Instance()
```

#### Esempio di implementazione (Java)

```java
public class Singleton {
    // Unica istanza privata e statica
    private static Singleton instance;

    // Costruttore privato: impedisce la creazione dall'esterno
    private Singleton() { }

    // Metodo statico di accesso globale
    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }

    public void singletonOperation() {
        // logica specifica
    }
}

// Utilizzo:
Singleton s1 = Singleton.getInstance();
Singleton s2 = Singleton.getInstance();
// s1 == s2  →  true (stessa istanza)
```

#### Thread-safe (doppio controllo)

```java
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() { }

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

#### Conseguenze

**Vantaggi:**
- **Accesso controllato** ad un'unica istanza
- **Risoluzione dello spazio dei nomi**: miglioramento rispetto all'uso di variabili globali
- **Numero variabile di istanze**: permette di gestire un numero variabile di istanze (generalizzazione)

---

### Abstract Factory

**Categoria**: Creazionale

#### Scopo
Fornire un'**interfaccia per la creazione di famiglie di oggetti** correlati o dipendenti senza specificare quali siano le loro classi concrete. Nascondere come vengono creati e collegati oggetti complessi.

#### Quando usarlo
Il pattern Abstract Factory può essere utilizzato quando:
- Un sistema deve essere **indipendente** dalle modalità di creazione, composizione, rappresentazione dei suoi prodotti
- Un sistema deve poter essere **configurato** scegliendo tra più famiglie di prodotti
- Esistono **famiglie di oggetti correlati** progettati per essere utilizzati insieme e occorre garantire che questo vincolo sia rispettato
- Si vuole fornire una **libreria di classi** rivelando soltanto le interfacce e non le implementazioni

#### Problema
Permettere che un sistema sia indipendente dall'implementazione degli oggetti concreti e che il client, attraverso l'interfaccia, utilizzi **diverse famiglie di prodotti**.

#### Soluzione

```
    ┌──────────────────┐         crea          ┌──────────────────┐
    │  AbstractFactory │ ─────────────────────► │  AbstractProductA│
    │──────────────────│                        └──────────────────┘
    │+createProductA() │                                 △
    │+createProductB() │                        ┌────────┴──────────┐
    └──────────────────┘                        │ConcreteProductA1  │
             △                                  │ConcreteProductA2  │
    ┌────────┴──────────┐                       └───────────────────┘
    │ConcreteFactory1   │ ─────────────────────► crea ConcreteProductA1
    │ConcreteFactory2   │ ─────────────────────► crea ConcreteProductA2
    └───────────────────┘
             △
       ┌─────┴─────┐
       │  Client   │  ← usa solo classi astratte
       └───────────┘
```

#### Partecipanti

| Partecipante | Ruolo |
|---|---|
| **AbstractFactory** | Definisce l'interfaccia di riferimento per gli oggetti che creano le istanze |
| **ConcreteFactory** | Implementa concretamente l'interfaccia di AbstractFactory; crea una tipologia specifica di oggetti di una famiglia |
| **AbstractProduct** | Definisce l'interfaccia per una famiglia di oggetti da creare tramite il factory |
| **ConcreteProduct** | Implementa concretamente l'oggetto della famiglia; viene creato dal ConcreteFactory corrispondente |
| **Client** | Utilizza unicamente le classi astratte del factory e dell'oggetto da creare, senza conoscerne gli aspetti implementativi |

#### Esempio di implementazione (Java)

```java
// Prodotti astratti
interface Button { void render(); }
interface Checkbox { void render(); }

// Prodotti concreti — Famiglia Windows
class WindowsButton implements Button {
    public void render() { System.out.println("Windows Button"); }
}
class WindowsCheckbox implements Checkbox {
    public void render() { System.out.println("Windows Checkbox"); }
}

// Prodotti concreti — Famiglia macOS
class MacButton implements Button {
    public void render() { System.out.println("Mac Button"); }
}
class MacCheckbox implements Checkbox {
    public void render() { System.out.println("Mac Checkbox"); }
}

// AbstractFactory
interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// ConcreteFactory per Windows
class WindowsFactory implements GUIFactory {
    public Button createButton()   { return new WindowsButton(); }
    public Checkbox createCheckbox(){ return new WindowsCheckbox(); }
}

// ConcreteFactory per macOS
class MacFactory implements GUIFactory {
    public Button createButton()   { return new MacButton(); }
    public Checkbox createCheckbox(){ return new MacCheckbox(); }
}

// Client — usa solo interfacce astratte
class Application {
    private Button button;
    private Checkbox checkbox;

    Application(GUIFactory factory) {
        button   = factory.createButton();
        checkbox = factory.createCheckbox();
    }

    void render() {
        button.render();
        checkbox.render();
    }
}

// Configurazione
GUIFactory factory = new WindowsFactory(); // oppure new MacFactory()
Application app = new Application(factory);
app.render();
```

#### Conseguenze

**Vantaggi:**
- Aiuta a **controllare le classi** di oggetti creati da un'applicazione
- Consente di **cambiare in modo semplice** la famiglia di prodotti utilizzata
- **Promuove la coerenza** nell'utilizzo di prodotti (si usano sempre prodotti della stessa famiglia)

**Svantaggi:**
- L'**aggiunta del supporto per nuove tipologie di prodotti è difficile**: consentire la creazione di nuove tipologie richiede l'estensione dell'interfaccia e la conseguente modifica di AbstractFactory e di tutte le sue sottoclassi

---

## Pattern Strutturali

---

### Facade

**Categoria**: Strutturale

#### Scopo
Fornire un'**interfaccia unificata** per un insieme di interfacce presenti in un sottosistema.  
Facade definisce un'interfaccia di livello più alto, che rende il sottosistema **più semplice da utilizzare**.

Un obiettivo comune di progettazione è la **minimizzazione delle comunicazioni e delle dipendenze** fra i diversi sottosistemi.

#### Uso nelle architetture software
Il pattern Facade può essere utilizzato per definire un **punto d'accesso a un elemento architetturale**. Supporta le seguenti tattiche architetturali per la modificabilità:
- **Encapsulate**: nasconde i dettagli implementativi del sottosistema
- Definisce l'**interfaccia di un sottosistema**
- **Abstract common services**: astrae servizi comuni accessibili da più client

#### Problema
Un client deve realizzare una singola operazione accedendo a classi molto **differenti tra loro** — alta complessità esposta al client.

```
         ┌──────────┐
         │  Client  │
         └──────────┘
          /   |    \
         ▼    ▼     ▼
      Class1 Class2 Class3   ← accoppiamento diretto: fragile!
```

#### Soluzione
La classe Facade **nasconde la complessità** dell'operazione. Il client chiama soltanto `metodoUnico()` che internamente coordina le classi del sottosistema.

```
         ┌──────────┐
         │  Client  │
         └──────────┘
               │
               ▼
         ┌──────────┐
         │  Facade  │        ← unico punto d'accesso
         └──────────┘
          /   |    \
         ▼    ▼     ▼
      Class1 Class2 Class3   ← il client non li conosce
```

#### Partecipanti

| Partecipante | Ruolo |
|---|---|
| **Facade** | Conoscitore del sottosistema; responsabile dell'invocazione delle classi interne |
| **Subsystem classes** | Implementano le funzionalità del sottosistema; eseguono il lavoro assegnato dalla Facade; **non conoscono** il Facade e non mantengono alcuna referenza ad esso |

#### Esempio di implementazione (Java)

```java
// Classi del sottosistema (complesse)
class SubsystemA {
    public void operationA1() { System.out.println("A1"); }
    public void operationA2() { System.out.println("A2"); }
}

class SubsystemB {
    public void operationB1() { System.out.println("B1"); }
}

class SubsystemC {
    public void operationC1() { System.out.println("C1"); }
    public void operationC2() { System.out.println("C2"); }
}

// Facade: semplifica l'accesso
class Facade {
    private SubsystemA a = new SubsystemA();
    private SubsystemB b = new SubsystemB();
    private SubsystemC c = new SubsystemC();

    // Un'unica operazione che coordina i sottosistemi
    public void metodoUnico() {
        a.operationA1();
        b.operationB1();
        c.operationC1();
        c.operationC2();
        a.operationA2();
    }
}

// Client: usa solo la Facade
class Client {
    public static void main(String[] args) {
        Facade facade = new Facade();
        facade.metodoUnico();  // semplice!
    }
}
```

#### Esempio nel progetto Smart Mobility
Nel progetto, il layer **Controller** agisce come Facade verso i layer BLL e DAL: il client HTTP invia una richiesta a un unico endpoint (es. `POST /corse/sblocca`) e il controller coordina internamente `ServizioMobilita` e i DAL relativi.

#### Conseguenze

**Vantaggi:**
- **Indipendenza** dell'implementazione della classe Client dall'implementazione delle classi interne
- **Riusabilità** delle classi nascoste dal facade

**Svantaggi:**
- **Overhead di manutenzione**: la classe facade deve essere mantenuta aggiornata al variare del sottosistema

---

### Adapter

**Categoria**: Strutturale

#### Scopo
Adattare l'interfaccia di un elemento di un sistema ad una forma richiesta da uno dei suoi client.  
**Convertire l'interfaccia di una classe in un'altra interfaccia richiesta dal client.**  
Adapter consente a classi diverse di operare insieme quando ciò non sarebbe altrimenti possibile a causa di interfacce incompatibili.

#### Problema
Un elemento **(client)** potrebbe usare i servizi offerti da un altro elemento **(adaptee)**, ma l'interfaccia dell'adaptee **non è adatta** al client:
- *Esempio*: il client è .NET mentre l'adaptee è Java

Il client **potrebbe usare direttamente l'adaptee**, ma il conseguente accoppiamento stretto è indesiderato:
- Cambiamenti nell'adaptee richiedono cambiamenti nel client
- Client diversi devono cambiare in modo diverso

**Soluzione preferibile**: uso di un **intermediario (adattatore)** che fornisce soltanto un servizio di adattamento e traduzione.

```
Prima (senza Adapter):
  Client ─── [interfaccia incompatibile!] ──► Adaptee

Dopo (con Adapter):
  Client ──► Adapter ──► Adaptee
  (Target)  (traduce)   (originale)
```

#### Soluzione
Si definisce una classe intermedia, detta **Adapter**, che serve ad accoppiare l'interfaccia con la classe facendo da tramite:
- Quando il client vuole comunicare con l'adaptee → il client comunica con l'adattatore e l'adattatore comunica con l'adaptee
- L'adattatore **interpreta** le richieste del client, le trasforma in richieste all'adaptee, ottiene risposte dall'adaptee, e le ritrasforma in risposte al client
- L'adattatore ha un'**interfaccia (target)** diversa da quella dell'adaptee — scelta in modo che sia "gradita" al client

#### Struttura

```
  ┌──────────┐    usa    ┌──────────┐   implementa  ┌────────────────┐
  │  Client  │ ─────────► │  Target  │ ◄─────────────│    Adapter     │
  └──────────┘           │ request()│               │ request() {    │
                         └──────────┘               │  adaptee.      │
                                                    │  specificReq() │
                                                    │ }              │
                                                    └───────┬────────┘
                                                            │ delega a
                                                            ▼
                                                    ┌──────────────┐
                                                    │   Adaptee    │
                                                    │specificReq() │
                                                    └──────────────┘
```

| Ruolo | Classe | Descrizione |
|-------|--------|-------------|
| **Target** | Interfaccia | L'interfaccia da implementare (quella che il client conosce) |
| **Adaptee** | Classe esistente | Fornisce l'implementazione (non modificabile) |
| **Adapter** | Classe intermedia | Implementa Target e richiama Adaptee |

#### Esempio di implementazione (Java)

```java
// Interfaccia target (quella che il client conosce)
interface MediaPlayer {
    void play(String fileName);
}

// Adaptee (vecchia libreria con interfaccia diversa)
class LegacyAudioPlayer {
    public void playOldFormat(String file) {
        System.out.println("Playing (old format): " + file);
    }
}

// Adapter: traduce MediaPlayer → LegacyAudioPlayer
class AudioAdapter implements MediaPlayer {
    private LegacyAudioPlayer legacy;

    AudioAdapter(LegacyAudioPlayer legacy) {
        this.legacy = legacy;
    }

    @Override
    public void play(String fileName) {
        // traduce la chiamata
        legacy.playOldFormat(fileName);
    }
}

// Client: usa solo MediaPlayer (non conosce LegacyAudioPlayer)
class MusicApp {
    public static void main(String[] args) {
        LegacyAudioPlayer old = new LegacyAudioPlayer();
        MediaPlayer player = new AudioAdapter(old);
        player.play("song.mp3");
    }
}
```

#### Conseguenze

**Vantaggi:**
- **Disaccoppiamento** delle implementazioni di client e adaptee — l'implementazione di ciascun elemento può variare senza ripercussioni sull'altro
- L'**adaptee può essere usato da diversi tipi di client**, ciascuno col suo adattatore

**Svantaggi:**
- La **direzione addizionale** potrebbe ridurre l'efficienza
- **Overhead di manutenzione**: se cambia il servizio offerto dall'adaptee, deve cambiare anche l'adattatore

---

## Pattern Comportamentali

---

### Observer

**Categoria**: Comportamentale  
**Alias**: Publish-Subscribe

#### Scopo
Definire una **dipendenza uno a molti** fra oggetti, in modo tale che se un oggetto cambia il suo stato interno, ciascuno degli oggetti dipendenti da esso viene **notificato e aggiornato automaticamente**.

#### Problema
Mantenere un alto livello di **consistenza** fra classi correlate, senza produrre situazioni di **forte accoppiamento**.

#### Quando usarlo
- Quando un'astrazione presenta **due diversi aspetti tra loro dipendenti** — è possibile definire due classi in cui incapsulare questi aspetti in modo da poterli utilizzare in maniera indipendente
- Quando una **modifica a un oggetto richiede modifiche ad altri oggetti** che dipendono da questo
- Quando un oggetto ha bisogno di **notificare ad altri oggetti** senza conoscerne l'identità principale

#### Soluzione
Gli oggetti fondamentali sono il **soggetto** (Subject) e l'**osservatore** (Observer):
1. Un soggetto può avere un numero imprecisato di osservatori dipendenti
2. Tutti gli osservatori verranno notificati quando il soggetto cambia il suo stato
3. In risposta alla notifica, ogni osservatore richiede le informazioni necessarie per sincronizzarsi con il nuovo stato del soggetto

#### Struttura

```
  ┌────────────────────────────┐         ┌─────────────────┐
  │         Subject            │         │    Observer     │
  │────────────────────────────│         │─────────────────│
  │ +attach(Observer)          │──────►  │ +update()       │
  │ +detach(Observer)          │         └────────┬────────┘
  │ +notify()                  │                  △
  └────────────┬───────────────┘                  │
               △                        ┌─────────┴────────┐
               │                        │ ConcreteObserver  │
  ┌────────────┴──────────────┐         │─────────────────  │
  │    ConcreteSubject         │         │ observerState     │
  │────────────────────────────│         │────────────────── │
  │ subjectState               │◄────── │ +update()         │
  │ +getState()                │         └──────────────────┘
  │ +setState()                │
  └────────────────────────────┘
```

#### Partecipanti

| Partecipante | Responsabilità |
|---|---|
| **Subject** | Conosce i suoi Observer; fornisce l'interfaccia per associare e rimuovere oggetti Observer |
| **Observer** | Fornisce l'interfaccia di notifica per gli oggetti a cui devono essere segnalati i cambiamenti di stato di Subject |
| **ConcreteSubject** | Contiene lo stato monitorato dagli Observer; invia la notifica quando lo stato cambia |
| **ConcreteObserver** | Mantiene un riferimento a ConcreteSubject; contiene le informazioni da mantenere sincronizzate; implementa il metodo di gestione della notifica |

#### Collaborazioni
1. **ConcreteSubject notifica** ai propri Observer quando il suo stato cambia
2. Dopo la notifica, un **ConcreteObserver può richiedere ulteriori informazioni** al Subject concreto
3. **ConcreteObserver usa** le informazioni ottenute dal Subject per **sincronizzare il proprio stato**

#### Esempio di implementazione (Java)

```java
import java.util.ArrayList;
import java.util.List;

// Observer interface
interface Observer {
    void update(String event, Object data);
}

// Subject
class EventBus {
    private List<Observer> observers = new ArrayList<>();

    public void attach(Observer o) { observers.add(o); }
    public void detach(Observer o) { observers.remove(o); }

    protected void notifyObservers(String event, Object data) {
        for (Observer o : observers) {
            o.update(event, data);
        }
    }
}

// ConcreteSubject
class StockMarket extends EventBus {
    private double price;

    public void setPrice(double price) {
        this.price = price;
        notifyObservers("PRICE_CHANGE", price);
    }
}

// ConcreteObserver 1
class PriceDisplay implements Observer {
    @Override
    public void update(String event, Object data) {
        System.out.println("Display: prezzo aggiornato → " + data);
    }
}

// ConcreteObserver 2
class AlertSystem implements Observer {
    private double threshold;

    AlertSystem(double threshold) { this.threshold = threshold; }

    @Override
    public void update(String event, Object data) {
        double price = (Double) data;
        if (price > threshold) {
            System.out.println("ALERT: prezzo supera la soglia! → " + price);
        }
    }
}

// Utilizzo
StockMarket market = new StockMarket();
market.attach(new PriceDisplay());
market.attach(new AlertSystem(150.0));

market.setPrice(120.0);   // → Display aggiornato
market.setPrice(160.0);   // → Display aggiornato + ALERT
```

#### Esempio nel progetto Smart Mobility
Il pattern Observer può essere usato nel contesto delle **Segnalazioni**: quando un operatore aggiorna lo stato di un mezzo (es. `In manutenzione`), gli observer registrati (es. il servizio notifiche, il pannello amministrativo) vengono automaticamente notificati.

#### Conseguenze

**Vantaggi:**
- **Accoppiamento astratto** fra Subject e Observer: il soggetto non conosce le classi concrete degli osservatori
- **Numero libero di osservatori**: è possibile aggiungere e togliere osservatori in qualsiasi momento senza modificare il soggetto

**Svantaggi:**
- **Aggiornamenti inattesi**: gli Observer non hanno conoscenza della presenza l'uno dell'altro; possono essere del tutto all'oscuro del costo effettivo di richiedere una modifica al Subject

---

## Pattern J2EE / Web

I seguenti pattern sono specifici per applicazioni web multi-tier (J2EE), ma i principi si applicano a qualsiasi architettura a livelli.

---

### Front Controller

**Categoria**: Presentation Tier

#### Contesto
Applicazioni WEB J2EE, **Presentation Tier**

#### Problema
Necessità di **centralizzare il punto di accesso** per la gestione delle richieste.  
Senza un accesso centralizzato, il codice di controllo per gestire le richieste sarebbe **replicato** in differenti parti del sistema → sistema meno modulare, meno coeso, meno manutenibile.

#### Soluzione
Usare il **Front Controller come punto di contatto iniziale** per la gestione di ogni richiesta.

Obiettivi:
- Evitare un sistema meno modulare e meno coeso
- **Adottare una logica comune** a tutte le richieste
- **Separare logica di elaborazione** dalle view
- **Centralizzare l'accesso** al sistema

#### Gestione di una Richiesta — 4 fasi

```
  Richiesta HTTP
       │
       ▼
  ┌─────────────────────────────────────┐
  │  1. Gestione del Protocollo         │  ← gestisce protocolli specifici,
  │     e Trasformazione del Contesto   │    trasforma stato in forma generale
  ├─────────────────────────────────────┤
  │  2. Navigazione e Instradamento     │  ← sceglie oggetti per elaborazione
  │                                     │    e view per visualizzazione
  ├─────────────────────────────────────┤
  │  3. Elaborazione "Core"             │  ← servizio principale della richiesta
  ├─────────────────────────────────────┤
  │  4. Dispatch                        │  ← passa il controllo ai componenti
  │                                     │    per l'elaborazione della view
  └─────────────────────────────────────┘
```

#### Struttura

```
Browser ──► FrontController ──► Command/Handler ──► View
                 │
                 └──► gestisce: autenticazione, logging, routing
```

#### Esempio nel progetto Smart Mobility
In FastAPI, ogni **controller** (`utente_controller.py`, `mezzo_operatore_controller.py`, ecc.) riceve tutte le richieste HTTP per il proprio dominio. Il router FastAPI in `main.py` agisce come Front Controller che smista le richieste ai controller appropriati.

#### Conseguenze
- **Centralizza il controllo**
- **Migliora la gestibilità**
- **Migliora la riusabilità**
- **Migliora la separazione dei ruoli**

---

### Business Object

**Categoria**: Business Tier

#### Contesto
Applicazioni WEB J2EE, **Business Tier**

#### Problema
- Il modello concettuale del sistema ha la logica di business e relazioni
- Un accesso diretto dei client ai dati di business contenuti in un data store porterebbe a:
  - **Duplicazione** della logica di business
  - **Bassa riusabilità** e manutenibilità

#### Soluzione
Usare i **Business Object** per implementare un object model che rappresenti il modello concettuale del sistema.

Quando adottarlo:
- Modello concettuale con **oggetti strutturati e interrelati**
- Modello concettuale con **logica sofisticata**, validazioni e regole di business
- Necessità di **separare lo stato e i comportamenti** di business dal resto del sistema
- Necessità di **maggiore riusabilità** della logica di business e minore duplicazione di codice

#### Identificare i Business Object (BO) candidati

I candidati sono le **entità del modello concettuale**:
- Oggetti che gli utenti creano/accedono/manipolano nei casi d'uso
- Rappresentano dati di business di un sistema stateful e persistenti
- Sono riusati in differenti casi d'uso
- Sono identificati con **nomi di tipo sostantivo**

> **Esempio** — sistema "Elaborazione Ordini": `Ordine`, `Articolo`, `Fattura`, `Conto`

> **Nel progetto Smart Mobility**: `Mezzo`, `Corsa`, `Prenotazione`, `Zona`, `Segnalazione`, `Abbonamento`

Tipicamente ad ogni BO vi è una corrispondenza con un **elemento persistente di un datastore**.

#### Struttura

```
  ┌──────────┐         ┌─────────────────┐         ┌──────────────┐
  │  Client  │──────►  │  Business Object │──────►  │  DataStore   │
  └──────────┘         │  (logica + stato)│         │  (DB, file)  │
                       └─────────────────┘         └──────────────┘
```

#### Esempio nel progetto Smart Mobility (BLL)

```python
# backend/bll/servizio_mobilita.py — Business Object "Corsa"
class ServizioMobilita:
    def sblocca_mezzi(self, utente_id, mezzo_ids, metodo_pagamento_id):
        # logica business: validazione, creazione corsa, aggiornamento stato
        gruppo_corsa_id = str(uuid.uuid4())
        for mezzo_id in mezzo_ids:
            self._sblocca_singolo(utente_id, mezzo_id, gruppo_corsa_id)
        return gruppo_corsa_id
```

#### Conseguenze

**Vantaggi:**
- Promuove approccio **OO** nell'implementazione del business model
- **Centralizza** il comportamento e lo stato del business
- **Favorisce il riuso**
- Evita duplicazioni e favorisce **manutenibilità** del codice
- **Separa** logica di persistenza dalla logica di business
- Promuove la **Service Oriented Architecture**

**Svantaggi:**
- Implementazioni POJO suscettibili ai **dati vecchi**
- Delega parte del comportamento ad un **ulteriore livello**
- Può indurre BO di **dimensioni eccessive**

---

### Transfer Object

**Categoria**: Business Tier  
**Alias**: Value Object, DTO (Data Transfer Object)

#### Contesto
Applicazioni WEB J2EE, **Business Tier**

#### Problema
La necessità di **trasferire dati tra livelli differenti**.  
I client devono accedere ad altri livelli per raccogliere o aggiornare i dati → necessità di ridurre le richieste remote ed evitare la degradazione delle performance di rete.

#### Soluzione
Usare un **Transfer Object** per trasportare dati multipli attraverso la rete con una singola chiamata.

#### Strategie

**1. Strategia base**: oggetto TO separato dall'entità

```
  Business Object ──────────────────► Transfer Object (DTO)
  (entità con logica)                  (solo dati, serializzabile)
```

**2. Entity Inherits Transfer Object Strategy**

```
  TransferObject (base)
        △
        │
  BusinessObject (entità + logica BO)
```

#### Struttura

```
  ┌──────────┐   richiesta   ┌─────────────┐   getTO()   ┌──────────────────┐
  │  Client  │ ────────────► │BusinessTier │ ──────────► │ Transfer Object  │
  │          │ ◄──────────── │             │             │ (bundle di dati) │
  └──────────┘   risposta TO └─────────────┘             └──────────────────┘
```

#### Esempio nel progetto Smart Mobility (Pydantic schemas)

```python
# backend/controllers/schema.py — Transfer Object (schema Pydantic)
from pydantic import BaseModel
from datetime import datetime

class CorsaOut(BaseModel):
    id: int
    mezzo_id: int
    utente_id: int
    data_inizio: datetime
    data_fine: datetime | None
    importo: float | None
    gruppo_corsa_id: str | None

    class Config:
        from_attributes = True

# Il controller usa CorsaOut come TO tra BLL e frontend
# Invece di esporre direttamente l'ORM, si trasferisce solo ciò che serve
```

#### Conseguenze

**Vantaggi:**
- **Riduce il traffico di rete**
- Trasferimento di una **maggior mole di dati** con un numero inferiore di chiamate
- **Riduce la duplicazione** del codice

**Svantaggi:**
- Introduce **TO "vecchi"** (dati non aggiornati tra una chiamata e l'altra)
- Incrementa la complessità per gestire **sincronizzazioni e controllo di versioni**

---

### Data Access Object

**Categoria**: Integration Tier  
**Alias**: DAO, Repository

#### Contesto
Applicazioni WEB J2EE, **Integration Tier**

#### Problema
- Necessità di **incapsulare in un tier separato** l'accesso e la manipolazione dei dati
- Un sistema gestisce i dati persistenti in diversi modi (DB relazionale, file, servizi remoti, ecc.)
- Il codice dipendente dalle regole specifiche di ogni supporto è sparso nel sistema

#### Soluzione
Usare un **Data Access Object** per astrarre e incapsulare gli accessi ai datasource.  
Un DAO gestisce la connessione con i datasource e **recupera/memorizza i dati**.

Obiettivi:
- **Disaccoppiare** la logica di persistenza dal resto del sistema
- Fornire un accesso ai dati mediante **API indipendenti** dai data source
- **Incapsulare** i dettagli relativi a dispositivi "proprietari"

#### Struttura

```
  ┌─────────────────┐      usa      ┌─────────────────────┐
  │  Business Layer  │ ────────────► │        DAO          │
  │  (BLL/Service)   │              │  (interfaccia pura) │
  └─────────────────┘              └──────────┬──────────┘
                                              △
                                   ┌──────────┴──────────┐
                                   │   ConcreteDAO        │
                                   │ (implementazione DB) │
                                   └──────────┬──────────┘
                                              │ accede a
                                              ▼
                                   ┌──────────────────────┐
                                   │   DataSource         │
                                   │ (DB, file, API, ...)  │
                                   └──────────────────────┘
```

#### Partecipanti

| Partecipante | Ruolo |
|---|---|
| **BusinessObject** | Usa il DAO per accedere ai dati; non conosce i dettagli di persistenza |
| **DataAccessObject** | Interfaccia astratta che definisce le operazioni sui dati |
| **ConcreteDataAccessObject** | Implementa le operazioni di accesso ai dati per un datasource specifico |
| **TransferObject** | Veicola i dati tra DAO e Business Layer |
| **DataSource** | La sorgente dei dati (database, file, servizio remoto) |

#### Esempio nel progetto Smart Mobility (DAL)

```python
# backend/dal/corsa_repository.py — Data Access Object
from sqlalchemy.orm import Session
from backend.model.corsa import Corsa

class CorsaRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, corsa_id: int) -> Corsa | None:
        return self.db.query(Corsa).filter(Corsa.id == corsa_id).first()

    def find_attiva_by_utente(self, utente_id: int) -> list[Corsa]:
        return (
            self.db.query(Corsa)
            .filter(Corsa.utente_id == utente_id, Corsa.data_fine == None)
            .all()
        )

    def save(self, corsa: Corsa) -> Corsa:
        self.db.add(corsa)
        self.db.commit()
        self.db.refresh(corsa)
        return corsa

    def find_by_utente_order_by_data(self, utente_id: int) -> list[Corsa]:
        return (
            self.db.query(Corsa)
            .filter(Corsa.utente_id == utente_id)
            .order_by(Corsa.data_inizio.desc())
            .all()
        )
```

```python
# backend/bll/servizio_mobilita.py — usa il DAO
class ServizioMobilita:
    def __init__(self, db: Session):
        self.corsa_repo = CorsaRepository(db)    # usa il DAO
        self.mezzo_repo = MezzoRepository(db)    # usa il DAO

    def termina_corsa(self, corsa_id: int) -> Corsa:
        corsa = self.corsa_repo.find_by_id(corsa_id)  # non accede direttamente al DB
        # ... logica business ...
        return self.corsa_repo.save(corsa)
```

#### Conseguenze

**Vantaggi:**
- **Centralizza il controllo** con gestori con accoppiamento basso
- Consente la **"trasparenza"** (il client non sa se i dati vengono da DB, file, ecc.)
- Fornisce una **vista OO** e incapsula i database schema
- Consente **migrazioni più agevoli** (cambiare DB senza toccare la BLL)
- **Riduce la complessità** del codice nei client
- **Organizza** tutti gli accessi ai dati in un livello separato

**Svantaggi:**
- **Aggiunge un livello extra**
- Richiede un **design gerarchico** delle classi
- **Maggiore complessità** per poter consentire un design OO

---

## Riepilogo: Pattern nel progetto Smart Mobility

| Pattern | Dove viene usato nel progetto |
|---------|------------------------------|
| **Facade** | Controller HTTP che nasconde la complessità di BLL + DAL |
| **Business Object** | Classi BLL (`ServizioMobilita`, `ServizioPricing`, `ServizioAbbonamento`, ...) |
| **DAO / Repository** | Layer DAL (`CorsaRepository`, `MezzoRepository`, `ZonaRepository`, ...) |
| **Transfer Object** | Schema Pydantic `Out` (es. `CorsaOut`, `MezzoOut`) tra backend e frontend |
| **Front Controller** | Router FastAPI in `main.py` + singoli controller per dominio |
| **Observer** | (applicabile a notifiche di stato mezzo, segnalazioni) |
| **Abstract Factory** | (applicabile a creazione famiglie di mezzi: bike, car, e-scooter) |
| **Singleton** | Database session, configurazione applicazione |

---

## Riferimenti

- **J2EE Core Patterns** — Alur, Malks, Crupi
- **Design Pattern in Java** — Steven John Metsker, "Design pattern in Java: manuale pratico". Pearson: Addison Wesley, 2003
- **Core J2EE Patterns** — http://www.corej2eepatterns.com/PatternRelationships.htm
- **Design Patterns: Elements of Reusable Object-Oriented Software** — Gang of Four (Gamma, Helm, Johnson, Vlissides)
