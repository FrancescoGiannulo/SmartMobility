# Coerenza Diagramma delle Classi ↔ Codice

Documento di tracciamento delle discrepanze tra `docs/Diagrammi/DiagrammaClassi.md` e il codice sorgente.
Aggiornare questo file ad ogni fix fino a raggiungere piena coerenza.

**Ultima revisione:** 2026-06-21

**Legenda:** ✅ Coerente | ⚠️ Nome/struttura diverge | ❌ Mancante o problema critico

---

## FRONTEND — Views

| Diagramma | File nel codice | Stato | Note |
|-----------|----------------|-------|------|
| `VistaAbbonamenti` | `views/utente/VistaAbbonamenti.tsx` | ✅ | |
| `VistaAccount` | `views/auth/VistaLogin.tsx` + `views/utente/VistaProfiloUtente.tsx` | ⚠️ | Rinominata e spezzata in due file |
| `VistaCorsa` | `views/utente/VistaCorsa.tsx` | ✅ | |
| `VistaDashboardAP` | `views/amministrazione/VistaDashboardAP.tsx` | ✅ | |
| `VistaDashboardOperatore` | `views/operatore/VistaMappaOperatore.tsx` | ⚠️ | Nome diverso |
| `VistaDefinisciZona` | non trovata | ❌ | Probabilmente da creare o da integrare in `VistaMappaOperatore` |
| `VistaGestioneUtentiOperatore` | `views/operatore/VistaGestioneUtentiOperatore.tsx` | ✅ | Implementata 2026-06-21 (IF-OP.09) |
| `VistaHomepageUtente` | `views/utente/VistaMappa.tsx` | ⚠️ | Nome diverso |
| `VistaImpostazioniRegole` | `views/operatore/VistaImpostazioniRegole.tsx` | ✅ | |
| `VistaMezziOperatore` | `views/operatore/VistaMezziOperatore.tsx` | ✅ | |
| `VistaPagamento` | `views/utente/VistaPagamenti.tsx` | ⚠️ | Singolare vs plurale |
| `VistaParametriSistema` | `views/operatore/VistaParametriSistema.tsx` | ✅ | |
| `VistaReport` | `views/amministrazione/VistaReportAP.tsx` | ⚠️ | Nome diverso |
| `VistaSegnalazioneUtente` | `views/utente/VistaSegnalazione.tsx` | ⚠️ | Nome abbreviato |
| `VistaSegnalazioniOP` | `views/operatore/VistaSegnalazioniOperatore.tsx` | ⚠️ | Nome diverso |
| `VistaTariffe` | `views/operatore/VistaTariffe.tsx` | ✅ | Sprint successivo: separata da `VistaTariffeOfferte` (2026-06-20) |
| `VistaOfferte` | `views/operatore/VistaOfferte.tsx` | ✅ | Sprint successivo: separata da `VistaTariffeOfferte` (2026-06-20) |
| `VistaStoricoCorse` | `views/utente/VistaStoricoCorse.tsx` | ✅ | |
| *(non previsto)* | `views/auth/VistaLogin.tsx` | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `views/utente/VistaProfiloUtente.tsx` | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `views/auth/CallbackOAuth.tsx` | ⚠️ | Extra tecnico OAuth |
| *(non previsto)* | `views/PrivacyPolicy.tsx` | ⚠️ | Extra — aggiungere al diagramma |

---

## FRONTEND — Services

| Diagramma | File nel codice | Stato | Note |
|-----------|----------------|-------|------|
| `ApiService` | `services/ApiService.ts` | ✅ | |
| `AuthService` | `services/AuthService.ts` | ✅ | |
| `FlottaService` | `services/FlottaService.ts` | ✅ | |
| `TariffaService` | `services/TariffaService.ts` | ✅ | Creato 2026-06-20, estratto da `FlottaService` |
| `MapService` | `services/MapService.ts` | ✅ | |
| `PaymentService` | `services/PaymentService.ts` | ✅ | |
| `ZonaService` | `services/ZonaService.ts` | ✅ | |
| *(non previsto)* | `services/AbbonamentoService.ts` | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `services/CorsaService.ts` | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `services/ConfigurazioneService.ts` | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `services/OffertaService.ts` | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `services/RegolaFinecorsaService.ts` | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `services/SegnalazioneService.ts` | ⚠️ | Extra — aggiungere al diagramma |

---

## BACKEND — BLL (Servizi)

| Diagramma | File / Classe nel codice | Stato | Note |
|-----------|--------------------------|-------|------|
| `ServizioAbbonamento` | `bll/servizio_abbonamento.py` | ✅ | |
| `ServizioMappa` | `bll/servizio_mappa.py` | ✅ | |
| `ServizioMobilità` | `bll/servizio_mobilita.py` (`ServizioMobilita`) | ✅ | Nome senza accento — accettabile |
| `ServizioOfferta` | `bll/servizio_offerte.py` (`ServizioOfferta`) | ⚠️ | Nome file al plurale (`offerte`) vs singolare nel diagramma |
| `ServizioParametri` | `bll/servizio_parametri.py` | ✅ | |
| `ServizioPrenotazione` | `bll/servizio_prenotazione.py` | ✅ | |
| `ServizioPricing` | `bll/servizio_pricing.py` | ✅ | |
| `ServizioTariffa` | `bll/servizio_tariffa.py` | ✅ | Creato 2026-06-20, estratto da `ServizioPricing` (creaTariffa/aggiornaTariffa/get_tariffe) per simmetria con `ServizioOfferta` |
| `ServizioRegoleFineCorsa` | `bll/servizio_regole_fine_corsa.py` (`ServizioRegolaFinecorsa`) | ⚠️ | `Finecorsa` vs `FineCorsa` — maiuscola 'C' diverge |
| `ServizioReport` | `bll/servizio_report.py` | ✅ | |
| `ServizioSegnalazione` | `bll/servizio_segnalazione.py` | ✅ | Creato il 2026-06-08 |
| `ServizioUtenti` | `bll/servizio_utenti.py` | ✅ | |
| `NotificaService` | `bll/notifica_service.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) — solo persistenza, nessuna UI di lettura |
| `AbbonamentoService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di `ServizioAbbonamento` — rimuovere dal diagramma |
| `CorsaService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di parte di `ServizioMobilità` — rimuovere dal diagramma |
| `ConfigurazioneService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di `ServizioParametri` — rimuovere dal diagramma |
| `GestioneUtentiService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di `ServizioUtenti` — rimuovere dal diagramma |
| `OffertaService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di `ServizioOfferta` — rimuovere dal diagramma |
| `RegoleFineCorsaService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di `ServizioRegoleFineCorsa` — rimuovere dal diagramma |
| `ReportService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di `ServizioReport` — rimuovere dal diagramma |
| `SegnalazioneService` | *(duplicato nel diagramma)* | ⚠️ | Duplicato di `ServizioSegnalazione` — rimuovere dal diagramma |

---

## BACKEND — Model (Entità ORM)

| Diagramma | File / Classe nel codice | Stato | Note |
|-----------|--------------------------|-------|------|
| `Abbonamento` | non presente come ORM separato | ❌ | Modellato dentro `Offerta` con `tipo='abbonamento'` — decidere se allineare diagramma o creare modello separato |
| `AbbonamentoUtente` | `model/abbonamento_utente.py` | ✅ | |
| `AmministrazionePubblica` | `model/amministrazione_pubblica.py` (dataclass) | ⚠️ | Solo dataclass, non ORM SQLAlchemy |
| `Corsa` | `model/corsa.py` | ✅ | Aggiunto `pausaDurataAccumulataSec` al diagramma (2026-06-20), già presente nel DB (`013_pausa_corsa.sql`) ma mancante nel diagramma classi |
| `MetodoPagamento` | `model/pagamento.py` | ✅ | |
| `Mezzo` | `model/mezzo.py` | ✅ | |
| `Offerta` | `model/offerta.py` | ✅ | |
| `Operatore` | `model/orm.py` + `model/operatore.py` (dataclass) | ✅ | |
| `Pagamento` | `model/pagamento.py` | ✅ | |
| `ParametriSistema` | `model/parametri_sistema.py` | ✅ | |
| `Persona` | `model/persona.py` (dataclass) | ✅ | |
| `Prenotazione` | `model/prenotazione.py` | ✅ | |
| `Promozione` | `model/promozione.py` | ✅ | |
| `RegolaFineCorsa` | `model/regola_fine_corsa.py` (`RegolaFinecorsa`) | ⚠️ | `Finecorsa` vs `FineCorsa` — maiuscola 'C' diverge |
| `Segnalazione` | `model/segnalazione.py` | ✅ | |
| `Tariffa` | `model/tariffa.py` | ✅ | |
| `Utente` | `model/orm.py` + `model/utente.py` (dataclass) | ✅ | |
| `Zona` | `model/zona.py` | ✅ | |
| `Notifica` | `model/notifica.py` + `model/orm.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) |

---

## BACKEND — DAL (Repository)

| Diagramma | File nel codice | Stato | Note |
|-----------|----------------|-------|------|
| `AbbonamentoRepository` | `dal/abbonamento_repository.py` | ✅ | |
| `CorsaRepository` | `dal/corsa_repository.py` | ✅ | |
| `MezzoRepository` | `dal/mezzo_repository.py` | ✅ | |
| `OffertaRepository` | `dal/offerta_repository.py` | ✅ | |
| `PagamentoRepository` | `dal/pagamento_repository.py` | ✅ | |
| `ParametriSistemaRepository` | `dal/parametri_sistema_repository.py` | ✅ | |
| `PrenotazioneRepository` | `dal/prenotazione_repository.py` | ✅ | |
| `RegoleFineCorsaRepository` | `dal/regola_fine_corsa_repository.py` | ✅ | Presente anche `RegoleFineCorsaRawRepository` (non nel diagramma) |
| `SegnalazioneRepository` | `dal/segnalazione_repository.py` | ✅ | |
| `TariffaRepository` | `dal/tariffa_repository.py` | ✅ | |
| `UtenteRepository` | `dal/utente_repository.py` | ❌ | File esiste ma la classe è vuota (`pass`) — implementazione assente |
| `ZonaRepository` | `dal/zona_repository.py` | ✅ | |
| `NotificaRepository` | `dal/notifica_repository.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) |
| *(non previsto)* | `dal/attore_repository.py` (`AttoreRepository`) | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `dal/operatore_repository.py` (`OperatoreRepository`) | ⚠️ | Extra — aggiungere al diagramma |
| *(non previsto)* | `dal/promozione_repository.py` (`PromozioneRepository`) | ⚠️ | Extra — aggiungere al diagramma |

---

## BACKEND — Controllers

| Diagramma | File nel codice | Stato | Note |
|-----------|----------------|-------|------|
| `AbbonamentoController` | `controllers/abbonamento_controller.py` | ✅ | |
| `AccountController «FrontController»` | `controllers/login_controller.py` | ⚠️ | Nome diverso |
| `AmministrazionePubblicaController` | `controllers/ap_controller.py` | ✅ | Nome abbreviato accettabile |
| `ConfigurazioneController` | `controllers/configurazione_controller.py` | ✅ | |
| `CorsaController` | `controllers/corsa_controller.py` | ✅ | |
| `DashBoardOPController` | non trovato | ❌ | Funzionalità probabilmente dentro `mezzo_operatore_controller.py` |
| `HomePageUtenteController` | non trovato | ❌ | Funzionalità inside `utente_controller.py` (mappa_router) |
| `MezzoOperatoreController` | `controllers/mezzo_operatore_controller.py` | ✅ | |
| `TariffaController` | `controllers/tariffa_controller.py` | ✅ | Creato 2026-06-20, estratto da `mezzo_operatore_controller.py` |
| `OffertaController` | `controllers/offerta_controller.py` | ✅ | |
| `PagamentoController` | `controllers/pagamenti_controller.py` + `controllers/pricing_controller.py` | ⚠️ | Spezzato in due file |
| `RegoleFineCorsaController` | `controllers/regola_fine_corsa_controller.py` | ✅ | |
| `SegnalazioneOPController` | `controllers/segnalazione_op_controller.py` | ✅ | Creato il 2026-06-08 |
| `SegnalazioneUtenteController` | `controllers/segnalazione_utente_controller.py` | ✅ | Creato il 2026-06-08 |
| `UtentiOPController` | `controllers/utenti_op_controller.py` | ✅ | Implementata 2026-06-21 (IF-OP.09) |
| `ZoneController` | `controllers/zona_operatore_controller.py` | ✅ | |

---

## Riepilogo discrepanze aperte

### ❌ Critiche (da risolvere)

| # | Problema | Azione necessaria |
|---|----------|-------------------|
| 1 | `Abbonamento` ORM mancante | Decidere: creare modello separato O aggiornare diagramma per riflettere la fusione con `Offerta` |
| 2 | `UtenteRepository` vuoto (`pass`) | Implementare i metodi previsti dal diagramma |
| 3 | `VistaDefinisciZona` mancante | Creare la view O integrare funzionalità in `VistaMappaOperatore` e aggiornare diagramma |
| 4 | `DashBoardOPController` mancante | Creare controller dedicato O aggiornare diagramma |
| 5 | `HomePageUtenteController` mancante | Estrarre da `utente_controller.py` O aggiornare diagramma |

### ⚠️ Nomi divergenti (da allineare — codice O diagramma)

| # | Diagramma | Codice | Dove allineare |
|---|-----------|--------|----------------|
| 1 | `RegolaFineCorsa` | `RegolaFinecorsa` (model + BLL) | Scegliere una forma e uniformare |
| 2 | `ServizioRegoleFineCorsa` | `ServizioRegolaFinecorsa` | Idem |
| 3 | `VistaPagamento` | `VistaPagamenti` | Aggiornare diagramma |
| 4 | `VistaHomepageUtente` | `VistaMappa` | Aggiornare diagramma |
| 5 | `VistaDashboardOperatore` | `VistaMappaOperatore` | Aggiornare diagramma |
| 6 | `VistaReport` | `VistaReportAP` | Aggiornare diagramma |
| 7 | `VistaSegnalazioneUtente` | `VistaSegnalazione` | Aggiornare diagramma |
| 8 | `VistaSegnalazioniOP` | `VistaSegnalazioniOperatore` | Aggiornare diagramma |
| 9 | `VistaAccount` | `VistaLogin` + `VistaProfiloUtente` | Aggiornare diagramma |
| 10 | `PagamentoController` | `pagamenti_controller` + `pricing_controller` | Aggiornare diagramma |
| 11 | `AccountController` | `login_controller` | Aggiornare diagramma |

### ⚠️ Extra nel codice non nel diagramma (da aggiungere al diagramma)

**Frontend services:** `AbbonamentoService`, `CorsaService`, `ConfigurazioneService`, `OffertaService`, `RegolaFinecorsaService`, `SegnalazioneService`

**Frontend views:** `VistaStoricoCorse`, `VistaLogin`, `VistaProfiloUtente`, `CallbackOAuth`, `PrivacyPolicy`

**DAL:** `AttoreRepository`, `OperatoreRepository`, `PromozioneRepository`, `RegoleFineCorsaRawRepository`

### ⚠️ Duplicati nel diagramma da rimuovere

Le seguenti classi BLL compaiono due volte nel diagramma (una volta con nome italiano `Servizio*`, una volta con nome inglese `*Service`). Rimuovere le versioni inglesi:
`AbbonamentoService`, `CorsaService`, `ConfigurazioneService`, `GestioneUtentiService`, `OffertaService`, `RegoleFineCorsaService`, `ReportService`, `SegnalazioneService`

---

## Cronologia fix

| Data | Fix | File coinvolti |
|------|-----|----------------|
| 2026-06-20 | Corretto ID errato in `sequence_sospende_corsa.drawio`: era `IF-UT.10` (= Visualizza Promozioni, tutt'altra feature), corretto in **IF-UT.09** (verificato in `Sprint3_SMART_Mobility.md`). Rimossi self-message inventati su entità pure (`corsa.registraInizioPausa()`, `mezzo.bloccaMezzo()`, `corsa.applicaAddebitoPausa()`); corretto `sospendiCorsa→pausaCorsa` per `CorsaController` (nome reale); rimosso il branch "periodo di grazia scaduto" come round-trip client-server fittizio (nessun metodo/endpoint reale lo supporta) — sostituito con nota che rimanda al meccanismo reale (`pausaDurataAccumulataSec` calcolato in `ServizioPricing.effettuaPagamento` a fine corsa). Aggiunto `pausaDurataAccumulataSec: int` a `Corsa` nel diagramma classi | `Diagramma Classi.drawio`, `sequence_sospende_corsa.drawio` (ricostruito) |
| 2026-06-20 | Identificato e corretto ID errato: "Sospende Account Utente" è **IF-OP.09** (verificato in `Sprint3_SMART_Mobility.md`), non un generico "CS-21" usato nel titolo del vecchio diagramma di sequenza. Aggiunti i gap reali del caso d'uso: parametro `motivazione` mancante in tutta la catena (`VistaGestioneUtentiOperatore.confermaSospensione`, `IServizioUtenti`/`ServizioUtenti.sospendiAccount`, `UtentiOPController.sospendiAccount`, `GestioneUtentiService.sospendiAccount`, `AttoreRepository.sospendi`); creato `Notifica`/`NotificaRepository`/`NotificaService` (richiesti sia da IF-OP.09 passo 9 sia da IF-OP.08, mai modellati prima) e collegati a `ServizioUtenti`/`ServizioSegnalazione`. Solo diagrammi, nessun file di codice creato/modificato — feature pianificata, non implementata (come `Recensione`) | `Diagramma Classi.drawio`, `sequence_sospende_account_utente.drawio` (ricostruito), `sequence_gestisce_segnalazione.drawio` (aggiunta chiamata NotificaService) |
| 2026-06-20 | Estratto `ServizioTariffa`/`IServizioTariffa` da `ServizioPricing` (creaTariffa/aggiornaTariffa/getTariffe, pattern "engine") per simmetria con `ServizioOfferta`; `ServizioPricing` mantiene solo `getTariffe()` (pattern "db injection", IF-UT.05) e `calcolaImporto` | `bll/servizio_tariffa.py` (nuovo), `bll/servizio_pricing.py`, `controllers/tariffa_controller.py`, `tests/test_servizio_tariffa.py` (nuovo), `Diagramma Classi.drawio`, `sequence_definisce_tariffa.drawio` |
| 2026-06-20 | Separata `VistaTariffeOfferte` (troppo ampia, due flussi indipendenti) in `VistaTariffe` + `VistaOfferte`; estratto `TariffaService` da `FlottaService`; estratto `TariffaController` da `mezzo_operatore_controller.py` con relativi test di integrazione | `views/operatore/VistaTariffe.tsx` (nuovo), `views/operatore/VistaOfferte.tsx` (nuovo, ex `VistaTariffeOfferte.tsx`), `services/TariffaService.ts` (nuovo), `services/FlottaService.ts`, `controllers/tariffa_controller.py` (nuovo), `controllers/mezzo_operatore_controller.py`, `main.py`, `tests/test_tariffa_http.py` (nuovo), `App.tsx`, `views/operatore/VistaMappaOperatore.tsx` |
| 2026-06-08 | Creato `ServizioSegnalazione` BLL separato da `ServizioMobilita` | `bll/servizio_segnalazione.py` (nuovo) |
| 2026-06-08 | Creato `SegnalazioneUtenteController` per IF-UT.12 | `controllers/segnalazione_utente_controller.py` (nuovo) |
| 2026-06-20 | Corretti ID backlog errati nei commenti di tracciabilità: pagamenti taggati `IF-UT.12` → `IF-UT.06` (Salva Metodi Pagamento); segnalazioni taggate `IF-UT.15` → `IF-UT.12` (Invia Segnalazione) — `IF-UT.15` è in realtà "Scrive una recensione" e collideva col codice di `Recensione`, che la usa correttamente. Solo commenti, nessuna logica toccata. Verificato anche `IF-UT.21` ("Imposta Metodo Predefinito"): non risulta in `docs/Sprint3_SMART_Mobility.md` — da chiarire in una sessione futura, non corretto qui. | `bll/servizio_pricing.py`, `bll/servizio_mobilita.py`, `bll/servizio_segnalazione.py`, `controllers/pagamenti_controller.py`, `controllers/schemas.py`, `controllers/segnalazione_utente_controller.py`, `dal/pagamento_repository.py`, `dal/segnalazione_repository.py`, `frontend/src/services/PaymentService.ts`, `frontend/src/services/SegnalazioneService.ts`, `frontend/src/views/utente/VistaPagamenti.tsx`, `frontend/src/views/utente/VistaSegnalazione.tsx` |
| 2026-06-08 | Creato `SegnalazioneOPController` per IF-OP.08 | `controllers/segnalazione_op_controller.py` (nuovo) |
| 2026-06-08 | Rimossi metodi segnalazione da `ServizioMobilita` | `bll/servizio_mobilita.py` |
| 2026-06-08 | Rimosso `segnalazione_router` da `utente_controller.py` | `controllers/utente_controller.py` |
| 2026-06-08 | Aggiornato `main.py` con nuovi router segnalazione | `main.py` |
| 2026-06-21 | Implementato IF-OP.09 (Sospende Account Utente): `model/notifica.py`+`model/orm.py::Notifica`, `dal/notifica_repository.py`, `bll/notifica_service.py`, `AttoreRepository.lista_utenti/trova_utente_per_id/sospendi`, `ServizioUtenti.get_utenti/get_dettaglio_utente/sospendi_account`, `controllers/utenti_op_controller.py`, `GestioneUtentiService.ts`, `VistaGestioneUtentiOperatore.tsx`. Riattivazione e invalidazione sessione attiva escluse dallo scope (vedi spec). Corrette anche le post-condizioni errate di OP-09 in `Sprintn3.md` (testo copiato dal caso d'uso Segnalazione) | `backend/migrations/015_sospensione_account.sql`, `backend/model/notifica.py`, `backend/model/orm.py`, `backend/dal/notifica_repository.py`, `backend/bll/notifica_service.py`, `backend/dal/attore_repository.py`, `backend/bll/servizio_utenti.py`, `backend/controllers/utenti_op_controller.py`, `backend/controllers/schemas.py`, `backend/main.py`, `frontend/src/services/GestioneUtentiService.ts`, `frontend/src/views/operatore/VistaGestioneUtentiOperatore.tsx`, `App.tsx`, `VistaMappaOperatore.tsx`, `Sprintn3.md` |
