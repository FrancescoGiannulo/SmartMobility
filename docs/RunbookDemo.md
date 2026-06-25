# Runbook Demo Esame — Movimento mezzi e geofencing

## Prerequisiti
- Backend e frontend avviati (o ambiente di produzione raggiungibile).
- Env: `DEMO_ACCOUNT_EMAIL=demo@smartmobility.it` (backend), `VITE_DEMO_EMAIL=demo@smartmobility.it` (frontend).
- Account demo UT: `demo@smartmobility.it` / `DemoEsame2026!` (creato con `backend/scripts/seed_demo_account.py`).
- Account operatore: `operatore@smartmobility.test` / `Operatore123!`.

## Passi
1. Finestra A (browser): login come `demo@smartmobility.it`. Finestra B: login come operatore, apri la mappa.
2. Finestra A: dalla home prenota e **sblocca i mezzi** desiderati (es. 3) → corsa di gruppo, si apre Info Corsa.
3. In Info Corsa premi **▶ Avvia demo movimento**.
4. Racconta mentre il convoglio attraversa:
   - **Campus universitario** → banner giallo "Zona a velocità limitata — max 15 km/h";
   - **Politecnico** (dentro Campus) → banner rosso "Zona vietata" → spiega la **precedenza** vietata>limitata;
   - **uscita zona operativa** → banner ⚠️ "Fuori dalla zona operativa".
   In finestra B i mezzi si muovono in fila sulla mappa operatore.
5. Termina la corsa per mostrare la **penale** zona vietata a fine corsa (caso d'uso UT-04).

## Note
- La demo gira finché la tab demo resta aperta.
- Se i banner non cambiano: verifica che le zone "Campus universitario"/"Politecnico" esistano e siano attive nel DB.
