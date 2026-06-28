# Design: Suggerimenti Personalizzati basati su IA (IF-UT.22)

**Data:** 2026-06-15
**Stato:** Proposta — in attesa di revisione
**Ambito:** Sprint 2 (nuova feature, non presente nel Product Backlog corrente)

---

## 1. Contesto e motivazione

Durante una sessione di brainstorming sulle prossime funzionalità è emersa l'idea di
usare l'Intelligenza Artificiale (IA) per fornire all'Utente suggerimenti sulle proprie
corse e sull'utilizzo generale del servizio.

Per rispettare i vincoli del progetto (requisiti **Provabili/Verificabili**, **Fattibili**
entro i tempi dello sprint, nessuna dipendenza esterna che renda i test non
deterministici) si è scartata l'ipotesi di un assistente conversazionale aperto
(chatbot) a favore di un **motore di suggerimenti contestuali proattivi**:

- la decisione su *quale* suggerimento mostrare è presa da **regole deterministiche**
  nel BLL, basate sui dati già presenti (`Corsa`, `Pagamento`, `AbbonamentoUtente`);
- l'IA (LLM esterno) viene usata **solo** per formulare il *testo* del suggerimento in
  linguaggio naturale a partire da dati già calcolati — non per decidere la logica di
  business;
- se il servizio IA esterno non è configurato o non risponde, il sistema usa un
  **template testuale statico** equivalente, così la feature resta completamente
  testabile senza dipendenze esterne.

---

## 2. User Story

### IF-UT.22 – Visualizza Suggerimenti Personalizzati

> Come utente, voglio visualizzare nella mia Homepage suggerimenti calcolati dal
> sistema sulla base delle mie ultime 30 corse e del mio abbonamento corrente, così da
> individuare opportunità di risparmio economico e informazioni utili sulle mie
> abitudini di mobilità.

Note di qualità (rif. § "Qualità dei requisiti" di `Sprint2_SMART_Mobility.md`):

- **Non ambiguo**: l'intervallo di analisi è fissato a "ultime 30 corse" (non "alcune
  corse").
- **Atomico**: la US descrive la sola visualizzazione dei suggerimenti; le singole
  tipologie di suggerimento (regole) sono specificate nel caso d'uso come scenari
  distinti, non come requisiti separati.
- **Astratto**: non menziona l'uso di un LLM — è un dettaglio implementativo,
  descritto in questo documento di design ma non nella US.

---

## 3. Architettura

### 3.1 Nuovi elementi (seguono le convenzioni di `DiagrammaClassi_Corretto.drawio`)

| Elemento | Tipo | Layer | Note |
|---|---|---|---|
| `Suggerimento` | «entity» | Model | Nuova entità |
| `ISuggerimentoRepository` | «interface» | DAL (contratto) | |
| `SuggerimentoRepository` | «DAO» | DAL | |
| `IServizioSuggerimenti` | «interface» | Contratto Controller→BLL | |
| `ServizioSuggerimenti` | «Business Object» | BLL | |
| `AssistenteIA` | «interface» | Contratto verso sistema esterno | |
| `AssistenteIAAdapter` | «Adapter» | Integrazione esterna | |
| `Provider IA` | «sistema esterno» | — | es. Anthropic Claude API |
| `SuggerimentoController` | «Controller» | Controller | |
| `SuggerimentiService` | Service (BLL client) | Frontend | |

Il pattern **Adapter** per `AssistenteIAAdapter` è coerente con
`GoogleMapsAdapter` e `ProviderPagamentiAdapter` già presenti nel diagramma:
isola il BLL dal formato specifico dell'API del provider IA e rende il componente
mockabile nei test.

### 3.2 Flusso (scenario base)

1. Il frontend (`VistaHomepageUtente`) richiede i suggerimenti correnti tramite
   `SuggerimentiService.getSuggerimenti()` → `SuggerimentoController.getSuggerimenti`.
2. `ServizioSuggerimenti.getSuggerimenti(idUtente)`:
   - se esistono suggerimenti con `stato = 'nuovo'` generati nelle ultime 24 ore,
     li restituisce;
   - altrimenti invoca `generaSuggerimenti(idUtente)`.
3. `generaSuggerimenti(idUtente)`:
   a. recupera le ultime 30 corse (`ICorsaRepository.findByUtenteOrderByData`,
      limitate a 30), l'abbonamento attivo (`IAbbonamentoRepository.getAttivo`) e i
      pagamenti correlati (`IPagamentoRepository.findByUtente`);
   b. applica le **regole** (§ 3.3) ai dati raccolti, producendo 0..N "candidati"
      (struttura interna con `tipo` e `datiContesto`, non ancora testo);
   c. per ciascun candidato chiama `AssistenteIAAdapter.generaTesto(tipo, datiContesto)`
      per ottenere il testo in linguaggio naturale; in caso di errore/assenza
      configurazione, usa `formattaTestoStatico(tipo, datiContesto)` (template Python);
   d. persiste i `Suggerimento` tramite `ISuggerimentoRepository.save` e li restituisce.
4. L'utente può segnare un suggerimento come letto/ignorato:
   `SuggerimentiService.segnaVisto(idSuggerimento)` →
   `ServizioSuggerimenti.segnaVisto(idSuggerimento, idUtente)`.

### 3.3 Regole iniziali (Sprint 2)

Per mantenere lo scope fattibile in uno sprint, si propongono **due** regole iniziali,
ciascuna corrispondente a uno scenario del caso d'uso:

- **R1 — Abbonamento conveniente**: se l'utente non ha un abbonamento attivo
  (`AbbonamentoUtente.dataFine <= now()` o assente) e la somma di
  `Pagamento.importoPieno` delle corse degli ultimi 30 giorni per una tipologia di
  mezzo supera il `prezzo` dell'abbonamento mensile per quella tipologia, viene
  generato un suggerimento di tipo `abbonamento_consigliato`.
- **R2 — Mezzo preferito per fascia orario**: se l'utente ha effettuato almeno 5 corse
  con la stessa `TipoMezzo` nella stessa fascia orario (mattina 6-12, pomeriggio
  12-18, sera 18-24, notte 0-6) nelle ultime 30 corse, viene generato un suggerimento
  di tipo `mezzo_preferito`.

Altre regole (es. impatto ambientale, opzione G "Riepilogo impatto personale"
discussa in brainstorming) potranno essere aggiunte in sprint successivi senza
modifiche strutturali: `ServizioSuggerimenti` applica le regole come lista di
funzioni, pattern **Strategy** già usato in `ServizioPricing` per le tariffe.

### 3.4 Nuova entità `Suggerimento`

| Campo | Tipo | Note |
|---|---|---|
| `id` | UUID | PK |
| `utente_id` | UUID | FK → `utenti.id` |
| `tipo` | enum `tipo_suggerimento` | `abbonamento_consigliato`, `mezzo_preferito` |
| `testo` | TEXT | Testo mostrato all'utente (da IA o template statico) |
| `dati_contesto` | JSONB | Dati usati per generare il suggerimento (per audit/test) |
| `stato` | enum `stato_suggerimento` | `nuovo`, `visto`, `ignorato` |
| `creato_at` | TIMESTAMPTZ | DEFAULT now() |

Migrazione proposta: `backend/migrations/014_suggerimenti.sql`.

### 3.5 `AssistenteIAAdapter`

```
«Adapter»
AssistenteIAAdapter
---
+ generaTesto(tipo: TipoSuggerimento, contesto: Object): String
- chiamaModelloIA(prompt: String): Response
```

- Configurazione tramite variabile d'ambiente (es. `ANTHROPIC_API_KEY`), letta in
  `backend/.env` — **non** committata, come le altre chiavi di servizio.
- Se la variabile non è impostata o la chiamata fallisce/va in timeout,
  `ServizioSuggerimenti` usa `formattaTestoStatico`, un dizionario di template per
  `tipo` con placeholder sostituiti dai valori di `datiContesto` (es.
  `"Negli ultimi 30 giorni hai speso {importo}€ in corse {tipo_mezzo}: con
  l'abbonamento mensile risparmieresti {risparmio}€."`).
- Questo isola completamente la logica di business dal servizio esterno: i test
  unitari di `ServizioSuggerimenti` non richiedono mai una chiamata IA reale.

---

## 4. Impatto sul Diagramma delle Classi

Il diagramma `docs/Diagrammi/DiagrammaClassi_Corretto.drawio` (revisione 10/06/2026)
va aggiornato aggiungendo i seguenti elementi, seguendo le convenzioni esistenti
(stessa notazione di `ServizioOfferta`/`OffertaRepository`/`IServizioOfferta` per il
pattern Business Object + DAO + interfaccia):

1. **BLL**: nuovo box «Business Object» `ServizioSuggerimenti`
   - attributi: `- suggerimentoRepo: ISuggerimentoRepository`,
     `- corsaRepo: ICorsaRepository`, `- abbonamentoRepo: IAbbonamentoRepository`,
     `- pagamentoRepo: IPagamentoRepository`, `- assistenteIA: AssistenteIAAdapter`
   - metodi: `+ getSuggerimenti(idUtente): List<Suggerimento>`,
     `+ generaSuggerimenti(idUtente): List<Suggerimento>`,
     `+ segnaVisto(idSuggerimento, idUtente): void`,
     `- applicaRegole(corse, abbonamento, pagamenti): List<CandidatoSuggerimento>`,
     `- formattaTestoStatico(tipo, contesto): String`
2. **Interfacce Controller→BLL**: nuovo box «interface» `IServizioSuggerimenti` con la
   stessa firma pubblica di cui sopra.
3. **DAL**: nuovo box «DAO» `SuggerimentoRepository` e «interface»
   `ISuggerimentoRepository` con `findByUtente(idUtente)`, `save(s)`,
   `findRecenti(idUtente, da: DateTime)`, `aggiornaStato(id, stato)`.
4. **Model**: nuova «entity» `Suggerimento` con i campi di § 3.4.
5. **Sistemi esterni & Adapter**: nuovo box «Adapter» `AssistenteIAAdapter` e
   «interface» `AssistenteIA` (accanto a `ProviderPagamentiAdapter`), nuovo box
   «sistema esterno» `Provider IA`, collegato con relazione «chiama API» come
   `Google Maps`/`Provider Pagamenti`.
6. **Client**: nuovo `SuggerimentiService` nel Client API Service Layer (stesso
   livello di `AbbonamentoService`, `CorsaService`), che traduce le chiamate verso
   `ApiService` («Facade»).
7. **Controller**: nuovo `SuggerimentoController` con rotte `GET /suggerimenti` e
   `PATCH /suggerimenti/{id}`.

`docs/CoerenzaDiagrammaClassi.md` andrà aggiornato in una fase successiva
(implementazione), aggiungendo righe per ciascuno dei nuovi elementi una volta
creati i file corrispondenti — coerentemente con il resto del documento che traccia
lo stato "✅/⚠️/❌" diagramma↔codice.

---

## 5. Abbozzo Specifica Caso d'Uso — UT-22 Visualizza Suggerimenti Personalizzati

| Campo | Valore |
|---|---|
| **Nome** | Visualizza Suggerimenti Personalizzati |
| **ID** | UT-22 (IF-UT.22) |
| **Breve descrizione** | Il sistema analizza lo storico delle ultime 30 corse e<br>l'abbonamento corrente dell'Utente per generare suggerimenti<br>personalizzati, mostrati nella Homepage, così da segnalare<br>opportunità di risparmio o abitudini di mobilità ricorrenti. |
| **Attori Primari** | Utente |
| **Attori Secondari** | Nessuno |
| **Precondizioni** | 1. L'utente è autenticato alla piattaforma.<br>2. L'utente ha effettuato almeno una corsa. |
| **Sequenza principale degli eventi** | 1. Il caso d'uso inizia quando l'Utente accede alla<br>Homepage.<br>2. Il sistema verifica se esistono suggerimenti generati<br>nelle ultime 24 ore con stato "nuovo" per l'utente.<br>3. Se non esistono, il sistema recupera le ultime 30 corse,<br>l'abbonamento attivo e i pagamenti correlati dell'utente.<br>4. Il sistema applica le regole R1 (Abbonamento conveniente)<br>e R2 (Mezzo preferito per fascia orario) ai dati recuperati.<br>5. Per ciascuna regola soddisfatta, il sistema genera il<br>testo del suggerimento tramite il servizio di Intelligenza<br>Artificiale (IA) esterno e lo salva con stato "nuovo".<br>6. Il sistema mostra nella Homepage l'elenco dei<br>suggerimenti con stato "nuovo" o "visto" generati nelle<br>ultime 24 ore.<br>7. L'Utente seleziona un suggerimento per segnarlo come<br>letto.<br>8. Il sistema aggiorna lo stato del suggerimento a "visto". |
| **Post-condizioni** | I suggerimenti applicabili sono mostrati nella Homepage<br>dell'utente; lo stato dei suggerimenti letti è aggiornato a<br>"visto". |
| **Sequenza alternativa degli eventi** | NessunaRegolaSoddisfatta, ServizioIANonDisponibile |

### UT-22.01 — NessunaRegolaSoddisfatta

| Campo | Valore |
|---|---|
| **Breve descrizione** | Nessuna delle regole R1/R2 è soddisfatta dai dati<br>dell'utente. |
| **Precondizioni** | Il sistema ha applicato le regole al passo 4 della<br>sequenza principale senza produrre candidati. |
| **Post-condizioni** | La sezione suggerimenti della Homepage non mostra alcun<br>elemento. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa sostituisce i passi 5-6 della<br>sequenza principale.<br>2. Il sistema non genera alcun `Suggerimento`.<br>3. Il sistema non mostra la sezione suggerimenti nella<br>Homepage. |

### UT-22.02 — ServizioIANonDisponibile

| Campo | Valore |
|---|---|
| **Breve descrizione** | Il servizio esterno di Intelligenza Artificiale non è<br>configurato o non risponde durante la generazione del<br>testo di un suggerimento. |
| **Precondizioni** | Al passo 5 della sequenza principale, la chiamata al<br>servizio IA esterno fallisce o va in timeout. |
| **Post-condizioni** | Il suggerimento è generato e mostrato con un testo<br>equivalente prodotto da un template predefinito, senza<br>interruzioni percepibili dall'Utente. |
| **Sequenza alternativa degli eventi** | 1. La sequenza alternativa sostituisce il passo 5 della<br>sequenza principale.<br>2. Il sistema rileva l'errore o l'assenza di<br>configurazione del servizio IA.<br>3. Il sistema genera il testo del suggerimento tramite un<br>template testuale statico associato al tipo di regola<br>soddisfatta.<br>4. Il sistema salva il `Suggerimento` con stato "nuovo" e<br>prosegue al passo 6 della sequenza principale. |

---

## 6. Test plan

- `ServizioSuggerimenti.genera_suggerimenti`:
  - R1 soddisfatta (no abbonamento attivo, spesa > prezzo abbonamento) → genera
    suggerimento `abbonamento_consigliato`;
  - R1 non soddisfatta (abbonamento attivo) → nessun suggerimento `abbonamento_consigliato`;
  - R2 soddisfatta (≥5 corse stesso mezzo/fascia) → genera `mezzo_preferito`;
  - nessuna regola soddisfatta (scenario UT-22.01) → lista vuota;
  - `AssistenteIAAdapter` mockato per restituire un errore → testo da template
    statico (scenario UT-22.02), nessuna eccezione propagata.
- `ServizioSuggerimenti.segna_visto`: aggiorna lo stato solo per suggerimenti
  appartenenti all'utente richiedente (no accesso cross-utente).
- `SuggerimentoController`: test di integrazione su `GET /suggerimenti` e
  `PATCH /suggerimenti/{id}` con autenticazione.

---

## 7. Domande aperte / decisioni da confermare prima dell'implementazione

1. **Provider IA**: quale servizio usare (es. Anthropic Claude API) e dove
   configurare la relativa chiave in `backend/.env` / variabili Render.
2. **Frequenza di generazione**: la rigenerazione "on-demand" (al massimo ogni 24h
   per utente, al primo accesso alla Homepage) è accettabile per Sprint 2, oppure si
   preferisce un trigger diverso (es. al termine di ogni corsa)?
3. **Visibilità**: i suggerimenti vanno mostrati solo nella Homepage
   (`VistaHomepageUtente`) o anche in altre viste (es. `VistaCorsa` a fine corsa)?

Queste decisioni non bloccano la stesura del piano di implementazione, ma vanno
chiarite prima di iniziare lo sviluppo.
