# Git Workflow — Smart Mobility

Guida pratica per lavorare in team con branch separati durante lo Sprint 1.

---

## Struttura dei branch

```
main                  ← codice stabile, sempre funzionante
├── feature/auth          → P1: autenticazione e account
├── feature/corsa         → P2: prenotazione, sblocco, fine corsa
├── feature/pagamenti     → P3: pagamenti e tariffe
└── feature/mappa-zone    → P4: mappa, zone e gestione flotta
```

**Regola fondamentale:** nessuno committa direttamente su `main`. Ogni modifica passa da un branch e una Pull Request.

---

## Configurazione VS Code (una volta sola)

Il file `.vscode/settings.json` configura l'interprete Python automaticamente su **macOS/Linux**.

Su **Windows** il path del venv è diverso — dopo il clone vai su:
`Ctrl+Shift+P` → **Python: Select Interpreter** → scegli:
```
backend\.venv\Scripts\python.exe
```

---

## Setup iniziale (una volta sola dopo il clone)

```bash
# Clona il repository
git clone https://github.com/FrancescoGiannulo/SmartMobility.git
cd SmartMobility

# Scarica tutti i branch remoti
git fetch --all

# Vai sul tuo branch
git checkout feature/auth        # sostituisci con il tuo branch
```

---

## Flusso di lavoro quotidiano

### 1. Inizio giornata — aggiorna il tuo branch

Prima di iniziare a scrivere codice, sincronizza sempre il tuo branch con le ultime modifiche:

```bash
# Assicurati di essere sul tuo branch
git checkout feature/auth

# Scarica le ultime modifiche dal remote
git pull origin feature/auth

# (Opzionale ma consigliato) Incorpora anche le ultime modifiche di main
git merge main
```

Se ci sono conflitti, vedi la sezione [Gestione dei conflitti](#gestione-dei-conflitti).

---

### 2. Durante il lavoro — committa spesso

Committa ogni volta che completi una parte logica (non aspettare di finire tutto):

```bash
# Controlla cosa hai modificato
git status

# Aggiungi i file modificati (preferisci file specifici ad "add .")
git add backend/bll/servizio_auth.py backend/controllers/utente_controller.py

# Crea il commit con messaggio descrittivo
git commit -m "feat(auth): aggiunta validazione email in CS-07"
```

**Formato consigliato per i messaggi:**
```
tipo(area): descrizione breve

Esempi:
feat(auth): implementato login utente [IF-UT.18]
fix(corsa): corretto calcolo durata in ServizioMobilità
test(pagamenti): aggiunto test scenario CS-12.1 pagamento rifiutato
```

---

### 3. Fine giornata — pusha il tuo lavoro

```bash
git push origin feature/auth
```

Questo salva il tuo lavoro sul remote — i colleghi possono vederlo e tu non rischi di perderlo.

---

### 4. Aprire una Pull Request (quando un item è completo)

Quando hai finito di implementare **e testato** un item del backlog:

1. Vai su [github.com/FrancescoGiannulo/SmartMobility](https://github.com/FrancescoGiannulo/SmartMobility)
2. Clicca **"Compare & pull request"** sul tuo branch
3. Compila il titolo: `[IF-UT.18] Autentica Account`
4. Nella descrizione indica:
   - Cosa hai implementato
   - Come testarlo
   - Eventuali dipendenze da altri branch
5. Assegna un collega come reviewer
6. Clicca **"Create pull request"**

**Non fare il merge da solo** — aspetta l'approvazione di almeno un collega.

---

## Gestione dei conflitti

Un conflitto si verifica quando due persone modificano lo stesso file nelle stesse righe.

### Come risolverlo

```bash
# Git ti avvisa durante un merge
git merge main
# CONFLICT (content): Merge conflict in backend/models/mezzo.py

# Apri il file — troverai i marker di conflitto:
# <<<<<<< HEAD
# tuo codice
# =======
# codice di main
# >>>>>>> main

# Modifica il file mantenendo il codice corretto (o entrambi)
# Poi segna il conflitto come risolto
git add backend/models/mezzo.py
git commit -m "chore: risolto conflitto su Mezzo.stato"
```

### Come prevenirli

- Committa e pusha spesso — branch divergenti a lungo causano più conflitti
- Comunica con i colleghi se devi toccare file condivisi (es. `main.py`, modelli base)
- Fai `git merge main` sul tuo branch almeno una volta al giorno

---

## Comandi utili

```bash
# Vedere su quale branch sei
git branch

# Vedere tutti i branch (locali e remoti)
git branch -a

# Vedere lo storico dei commit
git log --oneline --graph --all

# Vedere cosa è cambiato prima di committare
git diff

# Annullare modifiche non ancora committate su un file
git restore backend/models/mezzo.py

# Spostare modifiche in sospeso su un altro branch (senza committare)
git stash                    # salva temporaneamente
git checkout feature/corsa   # cambia branch
git stash pop                # ripristina le modifiche
```

---

## Deploy automatico su push a main

Ogni push (o merge PR) su `main` trigge automaticamente:

1. **Vercel** — rebuilda e rideploya il frontend (~30-60s)
2. **Render** — rebuilda e rideploya il backend (~2-3 min)

Non serve fare nulla di manuale. Per verificare lo stato del deploy:
- Vercel: [vercel.com/dashboard](https://vercel.com) → progetto → Deployments
- Render: [dashboard.render.com](https://dashboard.render.com) → servizio → Logs

> **Attenzione:** se la build TypeScript fallisce (`npm run build`), Vercel non fa il deploy e mostra il build precedente. Eseguire sempre `npm run build` in locale prima di fare push su `main`.

---

## Regole del team

| Regola | Perché |
|---|---|
| Nessun commit diretto su `main` | Protegge la versione stabile + non trigga deploy accidentali |
| PR obbligatoria per il merge | Almeno un collega rivede il codice |
| Un item = un PR | Più facile da revisionare e da revertire |
| Messaggi di commit con ID backlog | Tracciabilità requisiti → codice |
| Test prima del PR | Non si merga codice non testato |
| `git pull` prima di iniziare | Evita divergenze inutili |
| `npm run build` prima del push su main | Evita build fallite su Vercel |

---

## Scenario tipico di una giornata

```bash
# Mattina: aggiorna
git checkout feature/auth
git pull origin feature/auth
git merge main

# Lavori su IF-UT.18 (login)
# ... scrivi codice ...

# A metà mattina: salva progresso
git add backend/bll/servizio_auth.py
git commit -m "feat(auth): hash password con bcrypt [IF-UT.18]"

# Hai finito l'item: pusha e apri PR
git push origin feature/auth
# → vai su GitHub e apri la Pull Request
```
