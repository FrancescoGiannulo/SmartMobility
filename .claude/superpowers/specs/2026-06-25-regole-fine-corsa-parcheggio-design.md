# Regole Fine Corsa — enforcement parcheggio + bonus [IF-OP.06]

## Problema
`RegolaFinecorsa` (tipo_vincolo, penale_fuori_zona, bonus_parcheggi_corretti, bonus_valore) viene salvata dall'operatore ma non è mai applicata: nessuno verifica se il mezzo è parcheggiato in una `ZonaParcheggio` a fine corsa. La penale "fuori zona" già applicata in `ServizioPricing` riguarda un'altra regola (IF-OP.06, transito in zona vietata/operativa durante la corsa). Inoltre `salva_regole_fine_corsa` duplica la stessa riga di config per ogni zona di parcheggio invece di salvarla una volta.

## Decisioni
- Config globale: una sola riga in `regole_fine_corsa` con `zona_parcheggio_id = NULL`. Rimossa la duplicazione per-zona.
- Bonus erogato come **credito in €** su `Utente.credito_bonus`, scalato dal prossimo pagamento (no nuova entità Bonus/Promozione).
- Contatore `Utente.contatore_parcheggi_corretti`: serie **consecutiva**, si azzera a ogni parcheggio scorretto.
- `tipo_vincolo` a fine corsa, se esistono zone di parcheggio attive:
  - `avviso`: corsa termina, messaggio informativo nel riepilogo.
  - `penale`: corsa termina, `penale_fuori_zona` si **somma** alla penale IF-OP.06 esistente nello stesso pagamento.
  - `divieto`: corsa **non termina** (HTTP 409), mezzo resta "In uso".
- Se nessuna `ZonaParcheggio` attiva è configurata: nessuna verifica, nessuna regressione sul comportamento attuale.
- Bonus (contatore + credito) si applica indipendentemente da `tipo_vincolo`, solo se `bonus_parcheggi_corretti`/`bonus_valore` sono configurati.

## Modifiche

**Migrazione** (`backend/migrations/0NN_credito_bonus_utente.sql`): `utenti.contatore_parcheggi_corretti INTEGER DEFAULT 0`, `utenti.credito_bonus NUMERIC(10,2) DEFAULT 0.00`.

**Model**: `model/utente.py` + due campi; aggiornare `docs/Diagrammi/DiagrammaClassi.md` (sezione Utente).

**DAL**:
- `ZonaRepository.punto_in_zona_parcheggio(lat, lng) -> bool` (stesso pattern ST_Within di `punto_in_zona_operativa`).
- `UtenteRepository`: metodi per leggere/incrementare/azzerare contatore e credito.

**BLL `ServizioMobilita`**:
- `salva_regole_fine_corsa`: salva una riga unica (no loop sulle zone parcheggio).
- `termina_corsa`: dopo aver verificato lo stato corsa, se esistono zone parcheggio attive, controlla posizione mezzo → applica logica sopra. Nuova eccezione `ParcheggioVietatoException`.
- Ritorna anche eventuale `avviso_parcheggio` e `penale_parcheggio_applicata` da passare a `ServizioPricing`.

**BLL `ServizioPricing.effettua_pagamento`**: somma `penale_fuori_zona` (parcheggio) alla penale esistente; poi scala `credito_bonus` disponibile dall'importo finale (mai sotto zero), decrementa il credito.

**Controller**: `termina_corsa` cattura `ParcheggioVietatoException` → 409.

**Frontend `VistaCorsa.tsx`**: nuova fase per il 409 (blocco, niente chiusura), banner avviso nel riepilogo, riga "Credito bonus applicato" se presente.

## Test
Unit: `punto_in_zona_parcheggio`, contatore (reset/incremento/soglia+credito), blocco `divieto`, somma penali, scalo credito. Niente test E2E frontend per velocità — solo verifica manuale del flusso divieto/penale/avviso.

## Scope escluso (per velocità)
- Aggiornamento esteso di `Sprintn3.md` (caso d'uso completo + diagramma di sequenza) — rimando a dopo, segnalo solo la discrepanza minima.
- Promozione/Bonus come entità dedicata (scartata in fase di brainstorming).
