# Coerenza Diagramma delle Classi ↔ Codice

Documento di tracciamento delle discrepanze tra `docs/Diagrammi/DiagrammaClassi.md` e il codice sorgente.
Aggiornare questo file ad ogni fix fino a raggiungere piena coerenza.

**Ultima revisione:** 2026-06-08

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
| `VistaGestioneUtentiOperatore` | non trovata | ❌ | Vista prevista dal diagramma non implementata |
| `VistaHomepageUtente` | `views/utente/VistaMappa.tsx` | ⚠️ | Nome diverso |
| `VistaImpostazioniRegole` | `views/operatore/VistaImpostazioniRegole.tsx` | ✅ | |
| `VistaMezziOperatore` | `views/operatore/VistaMezziOperatore.tsx` | ✅ | |
| `VistaPagamento` | `views/utente/VistaPagamenti.tsx` | ⚠️ | Singolare vs plurale |
| `VistaParametriSistema` | `views/operatore/VistaParametriSistema.tsx` | ✅ | |
| `VistaReport` | `views/amministrazione/VistaReportAP.tsx` | ⚠️ | Nome diverso |
| `VistaSegnalazioneUtente` | `views/utente/VistaSegnalazione.tsx` | ⚠️ | Nome abbreviato |
| `VistaSegnalazioniOP` | `views/operatore/VistaSegnalazioniOperatore.tsx` | ⚠️ | Nome diverso |
| `VistaTariffeOfferte` | `views/operatore/VistaTariffeOfferte.tsx` | ✅ | |
| *(non previsto)* | `views/utente/VistaCorse.tsx` | ⚠️ | Extra: storico corse — aggiungere al diagramma |
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
| `ServizioGIS` | `bll/servizio_gis.py` | ✅ | |
| `ServizioMobilità` | `bll/servizio_mobilita.py` (`ServizioMobilita`) | ✅ | Nome senza accento — accettabile |
| `ServizioOfferta` | `bll/servizio_offerte.py` (`ServizioOfferta`) | ⚠️ | Nome file al plurale (`offerte`) vs singolare nel diagramma |
| `ServizioParametri` | `bll/servizio_parametri.py` | ✅ | |
| `ServizioPrenotazione` | `bll/servizio_prenotazione.py` | ✅ | |
| `ServizioPricing` | `bll/servizio_pricing.py` | ✅ | |
| `ServizioRegoleFineCorsa` | `bll/servizio_regole_fine_corsa.py` (`ServizioRegolaFinecorsa`) | ⚠️ | `Finecorsa` vs `FineCorsa` — maiuscola 'C' diverge |
| `ServizioReport` | `bll/servizio_report.py` | ✅ | |
| `ServizioSegnalazione` | `bll/servizio_segnalazione.py` | ✅ | Creato il 2026-06-08 |
| `ServizioUtenti` | `bll/servizio_utenti.py` | ✅ | |
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
| `Corsa` | `model/corsa.py` | ✅ | |
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
| `OffertaController` | `controllers/offerta_controller.py` | ✅ | |
| `PagamentoController` | `controllers/pagamenti_controller.py` + `controllers/pricing_controller.py` | ⚠️ | Spezzato in due file |
| `RegoleFineCorsaController` | `controllers/regola_fine_corsa_controller.py` | ✅ | |
| `SegnalazioneOPController` | `controllers/segnalazione_op_controller.py` | ✅ | Creato il 2026-06-08 |
| `SegnalazioneUtenteController` | `controllers/segnalazione_utente_controller.py` | ✅ | Creato il 2026-06-08 |
| `UtentiOPController` | non trovato | ❌ | Da verificare se esiste logica di gestione utenti OP |
| `ZoneController` | `controllers/zona_operatore_controller.py` | ✅ | |

---

## Riepilogo discrepanze aperte

### ❌ Critiche (da risolvere)

| # | Problema | Azione necessaria |
|---|----------|-------------------|
| 1 | `Abbonamento` ORM mancante | Decidere: creare modello separato O aggiornare diagramma per riflettere la fusione con `Offerta` |
| 2 | `UtenteRepository` vuoto (`pass`) | Implementare i metodi previsti dal diagramma |
| 3 | `VistaDefinisciZona` mancante | Creare la view O integrare funzionalità in `VistaMappaOperatore` e aggiornare diagramma |
| 4 | `VistaGestioneUtentiOperatore` mancante | Creare la view |
| 5 | `DashBoardOPController` mancante | Creare controller dedicato O aggiornare diagramma |
| 6 | `HomePageUtenteController` mancante | Estrarre da `utente_controller.py` O aggiornare diagramma |
| 7 | `UtentiOPController` mancante | Creare controller dedicato O aggiornare diagramma |

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

**Frontend views:** `VistaCorse`, `VistaLogin`, `VistaProfiloUtente`, `CallbackOAuth`, `PrivacyPolicy`

**DAL:** `AttoreRepository`, `OperatoreRepository`, `PromozioneRepository`, `RegoleFineCorsaRawRepository`

### ⚠️ Duplicati nel diagramma da rimuovere

Le seguenti classi BLL compaiono due volte nel diagramma (una volta con nome italiano `Servizio*`, una volta con nome inglese `*Service`). Rimuovere le versioni inglesi:
`AbbonamentoService`, `CorsaService`, `ConfigurazioneService`, `GestioneUtentiService`, `OffertaService`, `RegoleFineCorsaService`, `ReportService`, `SegnalazioneService`

---

## Cronologia fix

| Data | Fix | File coinvolti |
|------|-----|----------------|
| 2026-06-08 | Creato `ServizioSegnalazione` BLL separato da `ServizioMobilita` | `bll/servizio_segnalazione.py` (nuovo) |
| 2026-06-08 | Creato `SegnalazioneUtenteController` per IF-UT.15 | `controllers/segnalazione_utente_controller.py` (nuovo) |
| 2026-06-08 | Creato `SegnalazioneOPController` per IF-OP.08 | `controllers/segnalazione_op_controller.py` (nuovo) |
| 2026-06-08 | Rimossi metodi segnalazione da `ServizioMobilita` | `bll/servizio_mobilita.py` |
| 2026-06-08 | Rimosso `segnalazione_router` da `utente_controller.py` | `controllers/utente_controller.py` |
| 2026-06-08 | Aggiornato `main.py` con nuovi router segnalazione | `main.py` |
