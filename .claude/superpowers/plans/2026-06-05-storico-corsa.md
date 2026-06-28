# Visualizza Storico Corse — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare IF-UT.14 CS-11 — l'utente visualizza la cronologia delle corse, con le corse di gruppo raggruppate e un popup di dettaglio per ogni mezzo.

**Architecture:** Segue il diagramma `sequence_storico_corsa.drawio`: VistaCorse → CorsaService → GET /utente/corse/storico → CorsaController (prenotazione_utente_controller) → ServizioMobilita.get_storico() → CorsaRepository.find_by_utente_order_by_data(). Le corse di gruppo sono identificate da un `gruppo_corsa_id` UUID generato al momento dello sblocco di più mezzi insieme.

**Tech Stack:** FastAPI + SQLAlchemy (backend), React + TypeScript + Axios (frontend), PostgreSQL, pytest per test di integrazione.

---

## File Map

| File | Azione | Responsabilità |
|---|---|---|
| `backend/migrations/010_gruppo_corsa_id.sql` | CREATE | Aggiunge colonna `gruppo_corsa_id UUID` alla tabella `corse` |
| `backend/dal/corsa_repository.py` | MODIFY | Aggiorna `crea()` + aggiunge `find_by_utente_order_by_data()` |
| `backend/bll/servizio_mobilita.py` | MODIFY | Aggiorna `sblocca_mezzi()` + aggiunge `get_storico()` |
| `backend/controllers/schemas.py` | MODIFY | Aggiunge `CorsaStoricoOut` |
| `backend/controllers/prenotazione_utente_controller.py` | MODIFY | Aggiunge `GET /utente/corse/storico` |
| `backend/tests/test_storico_corsa.py` | CREATE | Test integrazione repository, BLL, endpoint |
| `frontend/src/services/CorsaService.ts` | MODIFY | Aggiunge `getStoricoCorsa()` e interfaccia `CorsaStorico` |
| `frontend/src/views/utente/VistaCorse.tsx` | CREATE | Vista lista storico con raggruppamento gruppo |
| `frontend/src/views/utente/VistaCorse.css` | CREATE | Stili lista, riga, badge gruppo, popup |
| `frontend/src/App.tsx` | MODIFY | Aggiunge route `/utente/storico` |
| `frontend/src/views/utente/VistaMappa.tsx` | MODIFY | Aggiunge voce "Cronologia" nella sidebar |

---

## Task 1: Migrazione DB — `gruppo_corsa_id`

**Files:**
- Create: `backend/migrations/010_gruppo_corsa_id.sql`

- [ ] **Step 1: Crea il file di migrazione**

```sql
-- 010_gruppo_corsa_id.sql — [IF-UT.14] Storico Corse con corsa di gruppo
-- gruppo_corsa_id: UUID condiviso tra tutte le corse avviate nello stesso
-- sblocco multiplo. NULL per corse singole.

ALTER TABLE corse ADD COLUMN gruppo_corsa_id UUID;

CREATE INDEX idx_corse_gruppo ON corse (gruppo_corsa_id)
    WHERE gruppo_corsa_id IS NOT NULL;
```

- [ ] **Step 2: Applica la migrazione al DB**

```bash
cd backend
uv run python -c "
from config import engine
from sqlalchemy import text

with open('migrations/010_gruppo_corsa_id.sql') as f:
    sql = f.read()
with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()
print('OK')
"
```

Output atteso: `OK`

- [ ] **Step 3: Verifica che la colonna esista**

```bash
uv run python -c "
from config import engine
from sqlalchemy import text
with engine.connect() as conn:
    row = conn.execute(text(
        \"SELECT column_name FROM information_schema.columns \"
        \"WHERE table_name='corse' AND column_name='gruppo_corsa_id'\"
    )).fetchone()
    print('Colonna trovata:', row)
"
```

Output atteso: `Colonna trovata: ('gruppo_corsa_id',)`

- [ ] **Step 4: Commit**

```bash
git add backend/migrations/010_gruppo_corsa_id.sql
git commit -m "feat(db): aggiungi gruppo_corsa_id a corse [IF-UT.14]"
```

---

## Task 2: CorsaRepository — `crea()` aggiornato + `find_by_utente_order_by_data()`

**Files:**
- Modify: `backend/dal/corsa_repository.py`

- [ ] **Step 1: Scrivi il test che fallisce**

Crea `backend/tests/test_storico_corsa.py`:

```python
import pytest
import uuid as _uuid
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session


LAT_TEST = 41.11
LNG_TEST = 16.85


def _inserisci_mezzo(db, codice: str) -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', 'Disponibile', :lat, :lng, 80)
        """), {"codice": codice, "lat": LAT_TEST, "lng": LNG_TEST})
        s.commit()
        row = s.execute(
            text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}
        ).fetchone()
    return str(row.id)


def _inserisci_corsa(db, utente_id, mezzo_id, stato="terminata",
                     gruppo_corsa_id=None, minuti_fa=0) -> str:
    from datetime import timedelta
    now = datetime.now(timezone.utc) - timedelta(minutes=minuti_fa)
    fine = now + timedelta(minutes=30)
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO corse
                (id, utente_id, mezzo_id, stato, inizio_at, fine_at,
                 distanza_km, gruppo_corsa_id)
            VALUES
                (:id, :uid, :mid, :stato, :inizio, :fine,
                 3.5, :gruppo)
        """), {
            "id": str(_uuid.uuid4()),
            "uid": str(utente_id),
            "mid": mezzo_id,
            "stato": stato,
            "inizio": now,
            "fine": fine,
            "gruppo": str(gruppo_corsa_id) if gruppo_corsa_id else None,
        })
        s.commit()
        row = s.execute(
            text("SELECT id FROM corse WHERE utente_id = :uid ORDER BY inizio_at DESC LIMIT 1"),
            {"uid": str(utente_id)}
        ).fetchone()
    return str(row.id)


def _cleanup(db, utente_id, mezzo_ids):
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE utente_id = :uid"),
                  {"uid": str(utente_id)})
        for mid in mezzo_ids:
            s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mid})
        s.commit()


class TestCorsaRepository:

    @pytest.mark.integration
    def test_crea_con_gruppo_corsa_id(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice = f"TEST-GRP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        gruppo_id = _uuid.uuid4()
        try:
            repo = CorsaRepository(db)
            corsa = repo.crea(utente_test["id"], _uuid.UUID(mezzo_id),
                              None, gruppo_id)
            assert corsa["gruppo_corsa_id"] == str(gruppo_id)
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_find_by_utente_restituisce_solo_terminate(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice = f"TEST-ST-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo_id, stato="terminata")
            _inserisci_corsa(db, utente_test["id"], mezzo_id, stato="in_uso")
            repo = CorsaRepository(db)
            risultato = repo.find_by_utente_order_by_data(utente_test["id"])
            stati = [r["stato"] if "stato" in r else "terminata" for r in risultato]
            assert all(s == "terminata" for s in stati) or len(risultato) >= 1
            # verifica che la corsa in_uso non sia inclusa
            assert len(risultato) == 1
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_find_by_utente_ordina_per_data_decrescente(self, db, utente_test):
        from dal.corsa_repository import CorsaRepository
        codice1 = f"TEST-ORD1-{_uuid.uuid4().hex[:6]}"
        codice2 = f"TEST-ORD2-{_uuid.uuid4().hex[:6]}"
        mezzo1 = _inserisci_mezzo(db, codice1)
        mezzo2 = _inserisci_mezzo(db, codice2)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo1, minuti_fa=60)   # più vecchia
            _inserisci_corsa(db, utente_test["id"], mezzo2, minuti_fa=10)   # più recente
            repo = CorsaRepository(db)
            risultato = repo.find_by_utente_order_by_data(utente_test["id"])
            assert len(risultato) == 2
            # la più recente viene prima
            assert risultato[0]["codice_mezzo"] == codice2
            assert risultato[1]["codice_mezzo"] == codice1
        finally:
            _cleanup(db, utente_test["id"], [mezzo1, mezzo2])
```

- [ ] **Step 2: Esegui i test — devono fallire**

```bash
cd backend
uv run pytest tests/test_storico_corsa.py -v -m integration 2>&1 | head -30
```

Output atteso: `FAILED` — `AttributeError: 'CorsaRepository' object has no attribute 'find_by_utente_order_by_data'`

- [ ] **Step 3: Implementa le modifiche a `CorsaRepository`**

In `backend/dal/corsa_repository.py`, sostituisci il metodo `crea` esistente e aggiungi `find_by_utente_order_by_data`:

```python
    # [IF-UT.04] CS-05 — crea corsa all'avvio del mezzo
    def crea(
        self,
        utente_id: UUID,
        mezzo_id: UUID,
        prenotazione_id: UUID | None,
        gruppo_corsa_id: UUID | None = None,
    ) -> dict:
        sql = text("""
            INSERT INTO corse
                (id, utente_id, mezzo_id, prenotazione_id, stato,
                 inizio_at, gruppo_corsa_id)
            VALUES
                (:id, :utente_id, :mezzo_id, :prenotazione_id, 'in_uso',
                 :inizio_at, :gruppo_corsa_id)
            RETURNING id, utente_id, mezzo_id, prenotazione_id, stato,
                      inizio_at, gruppo_corsa_id
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "id": str(_uuid.uuid4()),
                "utente_id": str(utente_id),
                "mezzo_id": str(mezzo_id),
                "prenotazione_id": str(prenotazione_id) if prenotazione_id else None,
                "inizio_at": datetime.now(timezone.utc),
                "gruppo_corsa_id": str(gruppo_corsa_id) if gruppo_corsa_id else None,
            }).fetchone()
            s.commit()
        return {
            "id": str(row.id),
            "utente_id": str(row.utente_id),
            "mezzo_id": str(row.mezzo_id),
            "prenotazione_id": str(row.prenotazione_id) if row.prenotazione_id else None,
            "stato": row.stato,
            "inizio_at": row.inizio_at.isoformat(),
            "gruppo_corsa_id": str(row.gruppo_corsa_id) if row.gruppo_corsa_id else None,
        }

    # [IF-UT.14] CS-11 — storico corse per utente, ordinate per data decrescente
    def find_by_utente_order_by_data(self, utente_id: UUID) -> list[dict]:
        sql = text("""
            SELECT
                c.id,
                c.inizio_at,
                c.fine_at,
                c.distanza_km,
                c.gruppo_corsa_id,
                m.tipo  AS tipo_mezzo,
                m.codice AS codice_mezzo,
                EXTRACT(EPOCH FROM (c.fine_at - c.inizio_at)) / 60 AS durata_min
            FROM corse c
            JOIN mezzi m ON c.mezzo_id = m.id
            WHERE c.utente_id = :utente_id
              AND c.stato = 'terminata'
            ORDER BY c.inizio_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql, {"utente_id": str(utente_id)}).fetchall()
        return [
            {
                "id": str(r.id),
                "tipo_mezzo": r.tipo_mezzo,
                "codice_mezzo": r.codice_mezzo,
                "inizio_at": r.inizio_at.isoformat(),
                "fine_at": r.fine_at.isoformat() if r.fine_at else None,
                "durata_min": float(r.durata_min) if r.durata_min is not None else None,
                "distanza_km": float(r.distanza_km) if r.distanza_km is not None else None,
                "gruppo_corsa_id": str(r.gruppo_corsa_id) if r.gruppo_corsa_id else None,
            }
            for r in rows
        ]
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend
uv run pytest tests/test_storico_corsa.py::TestCorsaRepository -v -m integration
```

Output atteso: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/dal/corsa_repository.py backend/tests/test_storico_corsa.py
git commit -m "feat(dal): aggiorna crea() con gruppo_corsa_id + find_by_utente_order_by_data [IF-UT.14]"
```

---

## Task 3: ServizioMobilita — `sblocca_mezzi()` + `get_storico()`

**Files:**
- Modify: `backend/bll/servizio_mobilita.py`

- [ ] **Step 1: Scrivi i test che falliscono** — aggiungi a `backend/tests/test_storico_corsa.py`:

```python
class TestServizioMobilita:

    @pytest.mark.integration
    def test_sblocca_gruppo_assegna_gruppo_corsa_id(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice1 = f"TEST-SG1-{_uuid.uuid4().hex[:6]}"
        codice2 = f"TEST-SG2-{_uuid.uuid4().hex[:6]}"
        mezzo1 = _inserisci_mezzo(db, codice1)
        mezzo2 = _inserisci_mezzo(db, codice2)
        try:
            from sqlalchemy.orm import Session as OrmSession
            with OrmSession(db) as s:
                svc = ServizioMobilita(s)
                ris = svc.sblocca_mezzi(
                    [_uuid.UUID(mezzo1), _uuid.UUID(mezzo2)],
                    utente_test["id"]
                )
            assert len(ris["sbloccati"]) == 2
            # entrambe le corse devono avere lo stesso gruppo_corsa_id (non None)
            with Session(db) as s:
                corse = s.execute(
                    text("SELECT gruppo_corsa_id FROM corse WHERE utente_id = :uid"),
                    {"uid": str(utente_test["id"])}
                ).fetchall()
            gruppi = [str(c.gruppo_corsa_id) for c in corse if c.gruppo_corsa_id]
            assert len(gruppi) == 2
            assert gruppi[0] == gruppi[1]
        finally:
            _cleanup(db, utente_test["id"], [mezzo1, mezzo2])

    @pytest.mark.integration
    def test_sblocca_singolo_nessun_gruppo_corsa_id(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-SS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            from sqlalchemy.orm import Session as OrmSession
            with OrmSession(db) as s:
                svc = ServizioMobilita(s)
                svc.sblocca_mezzi([_uuid.UUID(mezzo_id)], utente_test["id"])
            with Session(db) as s:
                row = s.execute(
                    text("SELECT gruppo_corsa_id FROM corse WHERE utente_id = :uid"),
                    {"uid": str(utente_test["id"])}
                ).fetchone()
            assert row.gruppo_corsa_id is None
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_get_storico_restituisce_corse(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-GS-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo_id)
            from sqlalchemy.orm import Session as OrmSession
            with OrmSession(db) as s:
                svc = ServizioMobilita(s)
                storico = svc.get_storico(utente_test["id"])
            assert len(storico) == 1
            assert storico[0]["codice_mezzo"] == codice
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])
```

- [ ] **Step 2: Esegui — devono fallire**

```bash
cd backend
uv run pytest tests/test_storico_corsa.py::TestServizioMobilita -v -m integration 2>&1 | head -20
```

Output atteso: `FAILED` con errori sulle firme o metodi mancanti.

- [ ] **Step 3: Implementa le modifiche a `ServizioMobilita`**

In `backend/bll/servizio_mobilita.py`:

1. Aggiungi `import uuid as _uuid` in cima al file (dopo gli altri import):

```python
import uuid as _uuid
```

2. Sostituisci il metodo `sblocca_mezzi` esistente:

```python
    # [IF-UT.04] CS-05 — sblocca uno o più mezzi in batch
    def sblocca_mezzi(
        self,
        mezzo_ids: list[UUID],
        utente_id: UUID,
        lat: float | None = None,
        lng: float | None = None,
    ) -> dict:
        sbloccati = []
        falliti = []
        # [IF-UT.14] gruppo_corsa_id condiviso se sblocco multiplo
        gruppo_id = _uuid.uuid4() if len(mezzo_ids) > 1 else None
        for mezzo_id in mezzo_ids:
            try:
                corsa = self._sblocca_singolo(mezzo_id, utente_id, gruppo_id)
                sbloccati.append({"mezzo_id": str(mezzo_id), "corsa_id": corsa["id"]})
            except Exception:
                # [CS-05.01] mezzo non sbloccabile — segnaFallito
                falliti.append(str(mezzo_id))
        return {"sbloccati": sbloccati, "falliti": falliti}
```

3. Sostituisci il metodo `_sblocca_singolo` esistente:

```python
    def _sblocca_singolo(
        self,
        mezzo_id: UUID,
        utente_id: UUID,
        gruppo_corsa_id: _uuid.UUID | None = None,
    ) -> dict:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")
        stato = mezzo["stato"]
        prenotazione_id = None
        if stato == "Disponibile":
            pass
        elif stato == "Prenotato":
            pren = self._pren_repo.trova_attiva_per_utente_e_mezzo(utente_id, mezzo_id)
            if pren is None:
                raise MezzoNonDisponibileException("Mezzo prenotato da un altro utente")
            prenotazione_id = pren["id"]
        else:
            raise MezzoNonDisponibileException(f"Mezzo non disponibile (stato: {stato})")
        corsa = self._corsa_repo.crea(utente_id, mezzo_id, prenotazione_id, gruppo_corsa_id)
        if prenotazione_id:
            self._pren_repo.aggiorna_stato(UUID(prenotazione_id), "convertita")
        self._mezzo_repo.aggiorna_stato(mezzo_id, "In uso")
        return corsa
```

4. Aggiungi il metodo `get_storico` in fondo alla classe:

```python
    # [IF-UT.14] CS-11 — Storico corse dell'utente
    def get_storico(self, utente_id: UUID) -> list[dict]:
        return self._corsa_repo.find_by_utente_order_by_data(utente_id)
```

- [ ] **Step 4: Esegui i test — devono passare**

```bash
cd backend
uv run pytest tests/test_storico_corsa.py::TestServizioMobilita -v -m integration
```

Output atteso: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_mobilita.py backend/tests/test_storico_corsa.py
git commit -m "feat(bll): sblocca_mezzi propaga gruppo_corsa_id + get_storico [IF-UT.14]"
```

---

## Task 4: Schema + Endpoint HTTP

**Files:**
- Modify: `backend/controllers/schemas.py`
- Modify: `backend/controllers/prenotazione_utente_controller.py`

- [ ] **Step 1: Scrivi il test che fallisce** — aggiungi a `backend/tests/test_storico_corsa.py`:

```python
class TestStoricoEndpoint:

    def _token(self, email: str, password: str) -> str:
        import httpx
        r = httpx.post("http://localhost:8000/auth/login",
                       json={"email": email, "password": password})
        assert r.status_code == 200
        return r.json()["access_token"]

    @pytest.mark.integration
    def test_storico_vuoto(self, utente_test):
        import httpx
        token = self._token(utente_test["email"], utente_test["password"])
        r = httpx.get("http://localhost:8000/utente/corse/storico",
                      headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json() == []

    @pytest.mark.integration
    def test_storico_con_corse(self, db, utente_test):
        import httpx
        codice = f"TEST-EP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            _inserisci_corsa(db, utente_test["id"], mezzo_id)
            token = self._token(utente_test["email"], utente_test["password"])
            r = httpx.get("http://localhost:8000/utente/corse/storico",
                          headers={"Authorization": f"Bearer {token}"})
            assert r.status_code == 200
            data = r.json()
            assert len(data) == 1
            assert data[0]["codice_mezzo"] == codice
            assert data[0]["tipo_mezzo"] == "monopattino"
            assert "inizio_at" in data[0]
            assert "gruppo_corsa_id" in data[0]
        finally:
            _cleanup(db, utente_test["id"], [mezzo_id])

    @pytest.mark.integration
    def test_storico_richiede_autenticazione(self):
        import httpx
        r = httpx.get("http://localhost:8000/utente/corse/storico")
        assert r.status_code == 401
```

- [ ] **Step 2: Esegui — devono fallire**

```bash
cd backend
uv run pytest tests/test_storico_corsa.py::TestStoricoEndpoint -v -m integration 2>&1 | head -20
```

Output atteso: `FAILED` con `404 Not Found` (route non esiste ancora).

- [ ] **Step 3: Aggiungi `CorsaStoricoOut` a `schemas.py`**

In `backend/controllers/schemas.py`, aggiungi in fondo:

```python
class CorsaStoricoOut(BaseModel):
    id: UUID
    tipo_mezzo: str
    codice_mezzo: str
    inizio_at: datetime
    fine_at: datetime | None
    durata_min: float | None
    distanza_km: float | None
    gruppo_corsa_id: UUID | None
```

- [ ] **Step 4: Aggiungi l'endpoint in `prenotazione_utente_controller.py`**

In `backend/controllers/prenotazione_utente_controller.py`:

1. Aggiungi `CorsaStoricoOut` agli import da `controllers.schemas`:

```python
from controllers.schemas import (
    PrenotazioneRequest,
    MezzoMappaOut,
    SbloccoRequest,
    MezzoSbloccabileOut,
    RisultatoSblocco,
    CorsaStoricoOut,
)
```

2. Aggiungi l'endpoint in fondo al file:

```python
# [IF-UT.14] CS-11 — Storico corse dell'utente
@router.get("/corse/storico", response_model=list[CorsaStoricoOut])
def get_storico_corse(
    utente=Depends(verify_token(["UT"])),
    db=Depends(get_db),
):
    """[CS-11] Restituisce la cronologia delle corse terminate dell'utente."""
    try:
        return ServizioMobilita(db).get_storico(utente["id"])
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Storico non disponibile al momento. Riprova più tardi.",
        )
```

- [ ] **Step 5: Riavvia il backend e verifica che la route sia presente**

```bash
# Kill processo uvicorn esistente, poi riavvia
cd backend
uv run python -c "
import httpx, json
r = httpx.get('http://localhost:8000/openapi.json')
paths = list(r.json()['paths'].keys())
print([p for p in paths if 'storico' in p])
"
```

Output atteso: `['/utente/corse/storico']`

- [ ] **Step 6: Esegui i test — devono passare**

```bash
cd backend
uv run pytest tests/test_storico_corsa.py::TestStoricoEndpoint -v -m integration
```

Output atteso: `3 passed`

- [ ] **Step 7: Commit**

```bash
git add backend/controllers/schemas.py backend/controllers/prenotazione_utente_controller.py backend/tests/test_storico_corsa.py
git commit -m "feat(api): GET /utente/corse/storico [CS-11/IF-UT.14]"
```

---

## Task 5: Frontend — `CorsaService.ts`

**Files:**
- Modify: `frontend/src/services/CorsaService.ts`

- [ ] **Step 1: Aggiungi interfaccia e funzione**

In `frontend/src/services/CorsaService.ts`, aggiungi dopo le interfacce esistenti:

```typescript
// [IF-UT.14] CS-11 — Storico corse
export interface CorsaStorico {
  id: string
  tipo_mezzo: 'monopattino' | 'bicicletta' | 'automobile'
  codice_mezzo: string
  inizio_at: string
  fine_at: string | null
  durata_min: number | null
  distanza_km: number | null
  gruppo_corsa_id: string | null
}

export const getStoricoCorsa = async (): Promise<CorsaStorico[]> => {
  const r = await api.get<CorsaStorico[]>('/utente/corse/storico')
  return r.data
}
```

- [ ] **Step 2: Verifica TypeScript**

```bash
cd frontend
npx tsc --noEmit 2>&1 | grep -i error || echo "OK"
```

Output atteso: `OK`

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/CorsaService.ts
git commit -m "feat(fe): getStoricoCorsa + CorsaStorico interface [IF-UT.14]"
```

---

## Task 6: Frontend — `VistaCorse.tsx` + `VistaCorse.css`

**Files:**
- Create: `frontend/src/views/utente/VistaCorse.tsx`
- Create: `frontend/src/views/utente/VistaCorse.css`

- [ ] **Step 1: Crea `VistaCorse.css`**

```css
/* VistaCorse.css — [IF-UT.14] IUI-9 Cronologia Corse */

.vista-corse-wrap {
  min-height: 100vh;
  background: #f5f8f5;
  display: flex;
  flex-direction: column;
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

/* ── Header ── */
.corse-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px 16px;
  background: #fff;
  border-bottom: 1px solid #eef0f3;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.btn-back-corse {
  background: none;
  border: none;
  color: #155e52;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  font-family: inherit;
}

.corse-titolo-header {
  font-size: 18px;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}

/* ── Corpo ── */
.corse-body {
  flex: 1;
  max-width: 560px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 20px 40px;
}

/* ── Stati ── */
.corse-loading,
.corse-vuoto {
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
  padding: 48px 0;
}

.corse-errore-banner {
  background: #fff0f0;
  border: 1.5px solid #f43f5e;
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.corse-errore-testo {
  color: #e11d48;
  font-size: 14px;
  font-weight: 600;
  margin: 0;
}

.btn-riprova {
  background: #155e52;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 8px 20px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
}

/* ── Lista ── */
.corse-lista {
  list-style: none;
  padding: 0;
  margin: 0;
}

.corse-item {
  background: #fff;
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 10px;
  box-shadow: 0 1px 4px rgba(15,23,42,0.06);
  border: 1px solid rgba(15,23,42,0.06);
}

.corse-item-riga {
  display: flex;
  align-items: center;
  gap: 14px;
}

.corse-item-icona {
  font-size: 28px;
  flex-shrink: 0;
}

.corse-item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.corse-item-codice {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
}

.corse-item-dettagli {
  font-size: 12px;
  color: #64748b;
}

.corse-item-data {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
}

/* ── Gruppo ── */
.corse-gruppo-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.corse-gruppo-icone {
  display: flex;
  gap: 2px;
  font-size: 20px;
}

.corse-gruppo-badge {
  background: #155e52;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 10px;
  border-radius: 99px;
}

.corse-gruppo-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.corse-gruppo-data {
  font-size: 12px;
  color: #94a3b8;
}

.btn-dettagli-gruppo {
  background: none;
  border: 1.5px solid #155e52;
  color: #155e52;
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  flex-shrink: 0;
}

/* ── Popup gruppo ── */
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15,23,42,0.5);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.popup-card {
  background: #fff;
  border-radius: 20px;
  padding: 24px 22px;
  width: 100%;
  max-width: 380px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.popup-titolo {
  font-size: 16px;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}

.btn-chiudi-popup {
  background: none;
  border: none;
  font-size: 20px;
  color: #94a3b8;
  cursor: pointer;
  line-height: 1;
  padding: 0 4px;
}

.popup-lista {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.popup-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8fafc;
  border-radius: 10px;
  padding: 10px 12px;
}

.popup-item-icona { font-size: 22px; flex-shrink: 0; }

.popup-item-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.popup-item-codice {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
}

.popup-item-dettagli {
  font-size: 12px;
  color: #64748b;
}
```

- [ ] **Step 2: Crea `VistaCorse.tsx`**

```tsx
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getStoricoCorsa, type CorsaStorico } from '../../services/CorsaService'
import './VistaCorse.css'

const GLYPH: Record<string, string> = {
  monopattino: '🛴', bicicletta: '🚲', automobile: '🚗',
}

function formatData(iso: string): string {
  return new Date(iso).toLocaleDateString('it-IT', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

function formatDurata(min: number | null): string {
  if (min == null) return '—'
  const m = Math.round(min)
  return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m} min`
}

type VoceStorico =
  | { tipo: 'singola'; corsa: CorsaStorico }
  | { tipo: 'gruppo'; gruppo_id: string; corse: CorsaStorico[] }

function raggruppa(corse: CorsaStorico[]): VoceStorico[] {
  const voci: VoceStorico[] = []
  const gruppiVisti = new Map<string, CorsaStorico[]>()
  for (const c of corse) {
    if (!c.gruppo_corsa_id) {
      voci.push({ tipo: 'singola', corsa: c })
    } else {
      if (!gruppiVisti.has(c.gruppo_corsa_id)) {
        const gruppo: CorsaStorico[] = []
        gruppiVisti.set(c.gruppo_corsa_id, gruppo)
        voci.push({ tipo: 'gruppo', gruppo_id: c.gruppo_corsa_id, corse: gruppo })
      }
      gruppiVisti.get(c.gruppo_corsa_id)!.push(c)
    }
  }
  return voci
}

// [IF-UT.14] CS-11 — Visualizza Storico Corse
export default function VistaCorse() {
  const navigate = useNavigate()
  const [voci, setVoci] = useState<VoceStorico[]>([])
  const [stato, setStato] = useState<'loading' | 'ok' | 'errore'>('loading')
  const [popupGruppo, setPopupGruppo] = useState<CorsaStorico[] | null>(null)

  const carica = () => {
    setStato('loading')
    getStoricoCorsa()
      .then(corse => {
        setVoci(raggruppa(corse))
        setStato('ok')
      })
      .catch(() => setStato('errore'))
  }

  useEffect(() => { carica() }, [])

  return (
    <div className="vista-corse-wrap">
      <header className="corse-header">
        <button type="button" className="btn-back-corse" onClick={() => navigate(-1)}>
          ← Indietro
        </button>
        <h1 className="corse-titolo-header">Cronologia Corse</h1>
      </header>

      <div className="corse-body">
        {stato === 'loading' && (
          <p className="corse-loading">Caricamento...</p>
        )}

        {/* [CS-11.1] DatiNonDisponibili */}
        {stato === 'errore' && (
          <div className="corse-errore-banner">
            <p className="corse-errore-testo">
              Storico delle corse non disponibile al momento. Riprova più tardi.
            </p>
            <button type="button" className="btn-riprova" onClick={carica}>
              Riprova
            </button>
          </div>
        )}

        {stato === 'ok' && voci.length === 0 && (
          <p className="corse-vuoto">Nessuna corsa effettuata.</p>
        )}

        {stato === 'ok' && voci.length > 0 && (
          <ul className="corse-lista">
            {voci.map((v, i) =>
              v.tipo === 'singola' ? (
                <li key={v.corsa.id} className="corse-item">
                  <div className="corse-item-riga">
                    <span className="corse-item-icona">{GLYPH[v.corsa.tipo_mezzo] ?? '●'}</span>
                    <div className="corse-item-info">
                      <span className="corse-item-codice">{v.corsa.codice_mezzo}</span>
                      <span className="corse-item-dettagli">
                        {formatDurata(v.corsa.durata_min)}
                        {v.corsa.distanza_km != null && ` · ${v.corsa.distanza_km.toFixed(1)} km`}
                      </span>
                    </div>
                    <span className="corse-item-data">{formatData(v.corsa.inizio_at)}</span>
                  </div>
                </li>
              ) : (
                <li key={v.gruppo_id} className="corse-item">
                  <div className="corse-gruppo-header">
                    <span className="corse-gruppo-icone">
                      {v.corse.map(c => GLYPH[c.tipo_mezzo] ?? '●').join('')}
                    </span>
                    <div className="corse-gruppo-info">
                      <span className="corse-gruppo-badge">Gruppo ({v.corse.length} mezzi)</span>
                      <span className="corse-gruppo-data">{formatData(v.corse[0].inizio_at)}</span>
                    </div>
                    <button
                      type="button"
                      className="btn-dettagli-gruppo"
                      onClick={() => setPopupGruppo(v.corse)}
                    >
                      Dettagli
                    </button>
                  </div>
                </li>
              )
            )}
          </ul>
        )}
      </div>

      {/* Popup dettaglio gruppo */}
      {popupGruppo && (
        <div className="popup-overlay" onClick={() => setPopupGruppo(null)}>
          <div className="popup-card" onClick={e => e.stopPropagation()}>
            <div className="popup-header">
              <h2 className="popup-titolo">Dettaglio corsa di gruppo</h2>
              <button
                type="button"
                className="btn-chiudi-popup"
                onClick={() => setPopupGruppo(null)}
                aria-label="Chiudi"
              >
                ✕
              </button>
            </div>
            <ul className="popup-lista">
              {popupGruppo.map(c => (
                <li key={c.id} className="popup-item">
                  <span className="popup-item-icona">{GLYPH[c.tipo_mezzo] ?? '●'}</span>
                  <div className="popup-item-info">
                    <span className="popup-item-codice">{c.codice_mezzo}</span>
                    <span className="popup-item-dettagli">
                      {formatDurata(c.durata_min)}
                      {c.distanza_km != null && ` · ${c.distanza_km.toFixed(1)} km`}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: Verifica TypeScript**

```bash
cd frontend && npx tsc --noEmit 2>&1 | grep -i error || echo "OK"
```

Output atteso: `OK`

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/utente/VistaCorse.tsx frontend/src/views/utente/VistaCorse.css
git commit -m "feat(fe): VistaCorse — storico con raggruppamento gruppo [IF-UT.14/IUI-9]"
```

---

## Task 7: Route + Sidebar

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/views/utente/VistaMappa.tsx`

- [ ] **Step 1: Aggiungi route in `App.tsx`**

In `frontend/src/App.tsx`:

1. Aggiungi l'import dopo gli altri import di viste utente:

```tsx
import VistaCorse from './views/utente/VistaCorse'
```

2. Aggiungi la route prima di `<Route path="/utente/*"`:

```tsx
        <Route
          path="/utente/storico"
          element={
            <RoutaProtetta ruoloRichiesto="UT">
              <VistaCorse />
            </RoutaProtetta>
          }
        />
```

- [ ] **Step 2: Aggiungi voce sidebar in `VistaMappa.tsx`**

In `frontend/src/views/utente/VistaMappa.tsx`, aggiungi il bottone "Cronologia" nel `<nav className="sidebar-voci">`, dopo il bottone "Abbonamenti" (riga ~593):

```tsx
              <button
                className="sidebar-voce"
                onClick={() => { setSidebarAperta(false); navigate('/utente/storico') }}
              >
                <span className="sidebar-voce__testo">Cronologia</span>
                <span className="sidebar-voce__icona">📋</span>
              </button>
```

- [ ] **Step 3: Verifica build**

```bash
cd frontend && npm run build 2>&1 | tail -6
```

Output atteso: `✓ built in ...`

- [ ] **Step 4: Commit**

```bash
git add frontend/src/App.tsx frontend/src/views/utente/VistaMappa.tsx
git commit -m "feat(fe): route /utente/storico + voce sidebar Cronologia [IF-UT.14]"
```

---

## Task 8: Verifica end-to-end manuale

- [ ] **Step 1: Assicurati che backend e frontend siano avviati**

```bash
# Backend (da root)
cd backend && uv run uvicorn main:app --reload
# Frontend (da root)
cd frontend && npm run dev
```

- [ ] **Step 2: Scenari da verificare nel browser su http://localhost:5173**

1. Login come utente → apri sidebar → clicca "Cronologia"
2. Con storico vuoto → verifica messaggio "Nessuna corsa effettuata"
3. Esegui una corsa (sblocca + termina) → torna a Cronologia → verifica che appaia
4. Sblocca 2 mezzi insieme → termina → in Cronologia verifica badge "Gruppo (2 mezzi)" e popup con i dettagli
5. Simula errore (spegni backend) → verifica banner "Storico non disponibile" + bottone "Riprova" che si riattiva quando il backend torna

- [ ] **Step 3: Esegui tutti i test backend**

```bash
cd backend && uv run pytest tests/test_storico_corsa.py -v -m integration
```

Output atteso: tutti i test passano.

- [ ] **Step 4: Commit finale**

```bash
git add .
git commit -m "feat(corsa): implementa IF-UT.14 Visualizza Storico Corse con corsa di gruppo"
```
