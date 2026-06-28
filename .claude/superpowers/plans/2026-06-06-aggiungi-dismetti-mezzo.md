# IF-OP.11/IF-OP.12 — Aggiunge Mezzo & Dismette Mezzo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementare la gestione flotta operatore: censimento di nuovi mezzi (IF-OP.11) e dismissione di mezzi esistenti (IF-OP.12), con view dedicata `VistaMezziOperatore` e relative API REST.

**Architecture:** Backend a tre layer (DAL → BLL → Controller) secondo il pattern già stabilito. Il controller `MezzoOperatoreController` espone 4 nuove route su prefisso `/operatore`. Il frontend aggiunge `VistaMezziOperatore` come pagina separata raggiungibile da `/operatore/mezzi`.

**Tech Stack:** Python / FastAPI / SQLAlchemy 2.0 / PostGIS (backend) · React 19 / TypeScript / Axios (frontend) · pytest con `@pytest.mark.integration` (test)

---

## File Map

| File | Operazione | Responsabilità |
|---|---|---|
| `backend/dal/mezzo_repository.py` | Modify | Aggiungi `esiste_by_codice`, `crea`, `lista_tutti`, `ha_corse_attive` |
| `backend/dal/zona_repository.py` | Modify | Aggiungi `punto_in_zona_operativa` |
| `backend/bll/servizio_gis.py` | Modify | Aggiungi `verifica_posizione_in_zona_operativa` |
| `backend/bll/servizio_mobilita.py` | Modify | Aggiungi `IdentificativoEsistenteException`, `PosizioneNonOperativaException`, `MezzoInMissioneException` + 4 nuovi metodi |
| `backend/controllers/schemas.py` | Modify | Aggiungi `AggiungiMezzoRequest`, `MezzoFlottaOut` |
| `backend/controllers/mezzo_operatore_controller.py` | Modify | Aggiungi 4 route |
| `backend/tests/test_aggiungi_mezzo.py` | Create | Test integrazione IF-OP.11 |
| `backend/tests/test_dismetti_mezzo.py` | Create | Test integrazione IF-OP.12 |
| `frontend/src/services/FlottaService.ts` | Modify | Fix path, aggiungi tipi e funzioni |
| `frontend/src/views/operatore/VistaMezziOperatore.tsx` | Create | View gestione flotta |
| `frontend/src/views/operatore/VistaMezziOperatore.css` | Create | Stili view |
| `frontend/src/App.tsx` | Modify | Aggiungi route `/operatore/mezzi` |

---

## Task 1: DAL — `MezzoRepository` nuovi metodi

**Files:**
- Modify: `backend/dal/mezzo_repository.py`
- Test: `backend/tests/test_aggiungi_mezzo.py` (parziale — metodi DAL)

- [ ] **Step 1: Crea il file di test con i test DAL**

Crea `backend/tests/test_aggiungi_mezzo.py`:

```python
import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

LAT_BARI = 41.1177
LNG_BARI = 16.8719


def _inserisci_mezzo(db, codice: str, stato: str = "Disponibile") -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, :lat, :lng, 80)
        """), {"codice": codice, "stato": stato, "lat": LAT_BARI, "lng": LNG_BARI})
        s.commit()
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


class TestMezzoRepositoryAggiungi:

    @pytest.mark.integration
    def test_esiste_by_codice_trovato(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-EX-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            assert MezzoRepository(db).esiste_by_codice(codice) is True
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_esiste_by_codice_non_trovato(self, db):
        from dal.mezzo_repository import MezzoRepository
        assert MezzoRepository(db).esiste_by_codice(f"NOEXIST-{_uuid.uuid4().hex}") is False

    @pytest.mark.integration
    def test_crea_mezzo(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-CR-{_uuid.uuid4().hex[:6]}"
        repo = MezzoRepository(db)
        mezzo = repo.crea("monopattino", codice, LAT_BARI, LNG_BARI, "Disponibile")
        try:
            assert mezzo["codice"] == codice
            assert mezzo["tipo"] == "monopattino"
            assert mezzo["stato"] == "Disponibile"
            assert mezzo["lat"] == pytest.approx(LAT_BARI)
        finally:
            _elimina_mezzo(db, str(mezzo["id"]))

    @pytest.mark.integration
    def test_lista_tutti_esclude_dismessi(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice_disp = f"TEST-LD-{_uuid.uuid4().hex[:6]}"
        codice_dism = f"TEST-DI-{_uuid.uuid4().hex[:6]}"
        id_disp = _inserisci_mezzo(db, codice_disp, "Disponibile")
        id_dism = _inserisci_mezzo(db, codice_dism, "Dismesso")
        try:
            lista = MezzoRepository(db).lista_tutti()
            codici = [m["codice"] for m in lista]
            assert codice_disp in codici
            assert codice_dism not in codici
        finally:
            _elimina_mezzo(db, id_disp)
            _elimina_mezzo(db, id_dism)

    @pytest.mark.integration
    def test_ha_corse_attive_true(self, db, utente_test):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-CA-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        corsa_id = str(_uuid.uuid4())
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at)
                VALUES (:id, :uid, :mid, 'in_uso', now())
            """), {"id": corsa_id, "uid": str(utente_test["id"]), "mid": mezzo_id})
            s.commit()
        try:
            assert MezzoRepository(db).ha_corse_attive(_uuid.UUID(mezzo_id)) is True
        finally:
            with Session(db) as s:
                s.execute(text("DELETE FROM corse WHERE id = :id"), {"id": corsa_id})
                s.commit()
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_ha_corse_attive_false(self, db):
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-CF-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            assert MezzoRepository(db).ha_corse_attive(_uuid.UUID(mezzo_id)) is False
        finally:
            _elimina_mezzo(db, mezzo_id)
```

- [ ] **Step 2: Esegui il test per verificare che fallisca**

```bash
cd backend && uv run pytest tests/test_aggiungi_mezzo.py -v -m integration
```

Atteso: `FAILED` — `AttributeError: 'MezzoRepository' object has no attribute 'esiste_by_codice'`

- [ ] **Step 3: Aggiungi i 4 nuovi metodi a `MezzoRepository`**

Apri `backend/dal/mezzo_repository.py` e aggiungi alla fine della classe `MezzoRepository`, dopo il metodo `aggiorna_stato`:

```python
    def esiste_by_codice(self, codice: str) -> bool:
        sql = text("SELECT EXISTS(SELECT 1 FROM mezzi WHERE codice = :codice) AS esiste")
        with self._sessione() as s:
            row = s.execute(sql, {"codice": codice}).fetchone()
        return bool(row.esiste) if row else False

    def crea(self, tipo: str, codice: str, lat: float, lng: float, stato: str) -> dict:
        sql = text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng)
            VALUES (:codice, :tipo, :stato, :lat, :lng)
            RETURNING id, codice, tipo, stato, lat, lng, batteria
        """)
        with self._sessione() as s:
            row = s.execute(sql, {
                "codice": codice, "tipo": tipo, "stato": stato, "lat": lat, "lng": lng,
            }).fetchone()
            s.commit()
        return {
            "id": row.id,
            "codice": row.codice,
            "tipo": row.tipo,
            "stato": row.stato,
            "lat": row.lat,
            "lng": row.lng,
            "batteria": row.batteria,
        }

    def lista_tutti(self) -> list[dict]:
        sql = text("""
            SELECT id, codice, tipo, stato, lat, lng, batteria
            FROM mezzi
            WHERE stato != 'Dismesso'
            ORDER BY created_at DESC
        """)
        with self._sessione() as s:
            rows = s.execute(sql).fetchall()
        return [
            {
                "id": row.id,
                "codice": row.codice,
                "tipo": row.tipo,
                "stato": row.stato,
                "lat": row.lat,
                "lng": row.lng,
                "batteria": row.batteria,
            }
            for row in rows
        ]

    def ha_corse_attive(self, mezzo_id: UUID) -> bool:
        sql = text("""
            SELECT EXISTS(
                SELECT 1 FROM corse
                WHERE mezzo_id = :mezzo_id
                  AND stato != 'terminata'
            ) AS ha_corse
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"mezzo_id": str(mezzo_id)}).fetchone()
        return bool(row.ha_corse) if row else False
```

- [ ] **Step 4: Esegui i test per verificare che passino**

```bash
cd backend && uv run pytest tests/test_aggiungi_mezzo.py -v -m integration
```

Atteso: tutti e 6 i test `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add backend/dal/mezzo_repository.py backend/tests/test_aggiungi_mezzo.py
git commit -m "feat(dal): aggiungi metodi MezzoRepository per gestione flotta [IF-OP.11/IF-OP.12]"
```

---

## Task 2: DAL — `ZonaRepository.punto_in_zona_operativa`

**Files:**
- Modify: `backend/dal/zona_repository.py`
- Test: `backend/tests/test_aggiungi_mezzo.py` (aggiungi classe `TestZonaRepositoryPunto`)

- [ ] **Step 1: Aggiungi i test per `punto_in_zona_operativa`**

Apri `backend/tests/test_aggiungi_mezzo.py` e aggiungi dopo `TestMezzoRepositoryAggiungi`:

```python
class TestZonaRepositoryPunto:

    @pytest.mark.integration
    def test_punto_dentro_zona_operativa(self, db):
        from dal.zona_repository import ZonaRepository
        zona_id = None
        with Session(db) as s:
            row = s.execute(text("""
                INSERT INTO zone (nome, tipo, perimetro, limite_velocita)
                VALUES ('ZonaTestOP', 'operativa',
                    ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[16.8,41.0],[16.95,41.0],[16.95,41.2],[16.8,41.2],[16.8,41.0]]]}'),
                    NULL)
                RETURNING id
            """)).fetchone()
            s.commit()
            zona_id = str(row.id)
        try:
            # lat=41.11, lng=16.87 è dentro il poligono
            assert ZonaRepository(db).punto_in_zona_operativa(41.11, 16.87) is True
        finally:
            with Session(db) as s:
                s.execute(text("DELETE FROM zone WHERE id = :id"), {"id": zona_id})
                s.commit()

    @pytest.mark.integration
    def test_punto_fuori_zona_operativa(self, db):
        from dal.zona_repository import ZonaRepository
        # Coordinate lontane da Bari (Roma)
        assert ZonaRepository(db).punto_in_zona_operativa(41.90, 12.49) is False
```

- [ ] **Step 2: Esegui il test per verificare che fallisca**

```bash
cd backend && uv run pytest tests/test_aggiungi_mezzo.py::TestZonaRepositoryPunto -v -m integration
```

Atteso: `FAILED` — `AttributeError: 'ZonaRepository' object has no attribute 'punto_in_zona_operativa'`

- [ ] **Step 3: Aggiungi `punto_in_zona_operativa` a `ZonaRepository`**

Apri `backend/dal/zona_repository.py` e aggiungi alla fine della classe, dopo `esiste_zona_operativa_contenente`:

```python
    def punto_in_zona_operativa(self, lat: float, lng: float) -> bool:
        """True se il punto (lat, lng) ricade in almeno una zona operativa attiva."""
        sql = text("""
            SELECT EXISTS(
                SELECT 1 FROM zone
                WHERE tipo = 'operativa'
                  AND attiva = true
                  AND ST_Within(
                      ST_SetSRID(ST_MakePoint(:lng, :lat), 4326),
                      perimetro
                  )
            ) AS esiste
        """)
        with self._sessione() as s:
            row = s.execute(sql, {"lat": lat, "lng": lng}).fetchone()
        return bool(row.esiste) if row else False
```

Nota: `ST_MakePoint` prende `(x, y)` = `(lng, lat)` in PostGIS.

- [ ] **Step 4: Esegui i test per verificare che passino**

```bash
cd backend && uv run pytest tests/test_aggiungi_mezzo.py::TestZonaRepositoryPunto -v -m integration
```

Atteso: entrambi `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add backend/dal/zona_repository.py backend/tests/test_aggiungi_mezzo.py
git commit -m "feat(dal): aggiungi punto_in_zona_operativa a ZonaRepository [IF-OP.11]"
```

---

## Task 3: BLL — `ServizioGIS.verifica_posizione_in_zona_operativa`

**Files:**
- Modify: `backend/bll/servizio_gis.py`

Questo metodo è un thin wrapper su `ZonaRepository.punto_in_zona_operativa`; la logica di zona è già testata in Task 2. Non servono test aggiuntivi.

- [ ] **Step 1: Aggiungi il metodo a `ServizioGIS`**

Apri `backend/bll/servizio_gis.py` e aggiungi alla fine della classe `ServizioGIS`, dopo `elimina_zona`:

```python
    # [IF-OP.11] Verifica che la posizione ricada in una zona operativa attiva
    def verifica_posizione_in_zona_operativa(self, lat: float, lng: float) -> bool:
        return self._zone_repo.punto_in_zona_operativa(lat, lng)
```

- [ ] **Step 2: Verifica che il modulo importi correttamente**

```bash
cd backend && uv run python -c "from bll.servizio_gis import ServizioGIS; print('OK')"
```

Atteso: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/bll/servizio_gis.py
git commit -m "feat(bll): aggiungi verifica_posizione_in_zona_operativa a ServizioGIS [IF-OP.11]"
```

---

## Task 4: BLL — `ServizioMobilita` — eccezioni e `aggiungi_mezzo`

**Files:**
- Modify: `backend/bll/servizio_mobilita.py`
- Test: `backend/tests/test_aggiungi_mezzo.py` (aggiungi classe `TestServizioMobilitaAggiungi`)

- [ ] **Step 1: Aggiungi i test BLL per `aggiungi_mezzo`**

Aggiungi alla fine di `backend/tests/test_aggiungi_mezzo.py`:

```python
def _inserisci_zona_operativa(db) -> str:
    with Session(db) as s:
        row = s.execute(text("""
            INSERT INTO zone (nome, tipo, perimetro, limite_velocita)
            VALUES ('ZonaTestOP-BLL', 'operativa',
                ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[16.8,41.0],[16.95,41.0],[16.95,41.2],[16.8,41.2],[16.8,41.0]]]}'),
                NULL)
            RETURNING id
        """)).fetchone()
        s.commit()
        return str(row.id)


def _elimina_zona(db, zona_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM zone WHERE id = :id"), {"id": zona_id})
        s.commit()


class TestServizioMobilitaAggiungi:

    @pytest.mark.integration
    def test_aggiungi_mezzo_ok(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        from sqlalchemy.orm import Session as S
        zona_id = _inserisci_zona_operativa(db)
        codice = f"TEST-BLL-{_uuid.uuid4().hex[:6]}"
        mezzo: dict = {}
        try:
            with S(db) as s:
                mezzo = ServizioMobilita(s).aggiungi_mezzo(
                    "monopattino", codice, LAT_BARI, LNG_BARI, "Disponibile"
                )
            assert mezzo["codice"] == codice
            assert mezzo["stato"] == "Disponibile"
        finally:
            if "id" in mezzo:
                _elimina_mezzo(db, str(mezzo["id"]))
            _elimina_zona(db, zona_id)

    @pytest.mark.integration
    def test_aggiungi_mezzo_codice_duplicato(self, db):
        from bll.servizio_mobilita import ServizioMobilita, IdentificativoEsistenteException
        from sqlalchemy.orm import Session as S
        zona_id = _inserisci_zona_operativa(db)
        codice = f"TEST-DUP-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice)
        try:
            with S(db) as s:
                with pytest.raises(IdentificativoEsistenteException):
                    ServizioMobilita(s).aggiungi_mezzo(
                        "monopattino", codice, LAT_BARI, LNG_BARI, "Disponibile"
                    )
        finally:
            _elimina_mezzo(db, mezzo_id)
            _elimina_zona(db, zona_id)

    @pytest.mark.integration
    def test_aggiungi_mezzo_fuori_zona(self, db):
        from bll.servizio_mobilita import ServizioMobilita, PosizioneNonOperativaException
        from sqlalchemy.orm import Session as S
        codice = f"TEST-FZ-{_uuid.uuid4().hex[:6]}"
        with S(db) as s:
            with pytest.raises(PosizioneNonOperativaException):
                ServizioMobilita(s).aggiungi_mezzo(
                    "monopattino", codice, 41.90, 12.49, "Disponibile"
                )
```

- [ ] **Step 2: Esegui il test per verificare che fallisca**

```bash
cd backend && uv run pytest tests/test_aggiungi_mezzo.py::TestServizioMobilitaAggiungi -v -m integration
```

Atteso: `FAILED` — `ImportError: cannot import name 'IdentificativoEsistenteException'`

- [ ] **Step 3: Aggiungi eccezioni e metodi a `ServizioMobilita`**

Apri `backend/bll/servizio_mobilita.py`.

Aggiungi le nuove eccezioni dopo le eccezioni già esistenti (dopo `CorsaNonTrovataException`):

```python
class IdentificativoEsistenteException(Exception):
    pass


class PosizioneNonOperativaException(Exception):
    pass


class MezzoInMissioneException(Exception):
    pass
```

Aggiungi l'import di `ServizioGIS` all'inizio del file (dopo gli import DAL già presenti):

```python
from bll.servizio_gis import ServizioGIS
```

Aggiungi i metodi alla classe `ServizioMobilita`, dopo `termina_corsa`:

```python
    # [IF-OP.11] CS-11 — Lista flotta per operatore
    def get_mezzi_flotta(self) -> list[dict]:
        return self._mezzo_repo.lista_tutti()

    # [IF-OP.11] CS-11 — Aggiunge un nuovo mezzo alla flotta
    def aggiungi_mezzo(
        self,
        tipo: str,
        codice: str,
        lat: float,
        lng: float,
        stato: str,
    ) -> dict:
        if self._mezzo_repo.esiste_by_codice(codice):
            raise IdentificativoEsistenteException(f"Identificativo '{codice}' già in uso")
        if not ServizioGIS(self._db).verifica_posizione_in_zona_operativa(lat, lng):
            raise PosizioneNonOperativaException("La posizione non ricade in nessuna zona operativa")
        return self._mezzo_repo.crea(tipo, codice, lat, lng, stato)
```

Nota: `ServizioGIS` richiede la `Session` di DB. Aggiungi `self._db` come attributo nel costruttore — aggiungi `self._db = db` come prima riga del `__init__`:

```python
    def __init__(self, db: Session) -> None:
        self._db = db   # ← aggiungi questa riga
        self._mezzo_repo = MezzoRepository(db)
        # ... resto invariato ...
```

- [ ] **Step 4: Esegui i test per verificare che passino**

```bash
cd backend && uv run pytest tests/test_aggiungi_mezzo.py::TestServizioMobilitaAggiungi -v -m integration
```

Atteso: tutti e 3 `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_mobilita.py backend/tests/test_aggiungi_mezzo.py
git commit -m "feat(bll): aggiungi eccezioni e metodo aggiungi_mezzo in ServizioMobilita [IF-OP.11]"
```

---

## Task 5: BLL — `ServizioMobilita` — `verifica_dismissione` e `dismetti_mezzo`

**Files:**
- Modify: `backend/bll/servizio_mobilita.py`
- Test: `backend/tests/test_dismetti_mezzo.py`

- [ ] **Step 1: Crea il file di test**

Crea `backend/tests/test_dismetti_mezzo.py`:

```python
import pytest
import uuid as _uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

LAT_BARI = 41.1177
LNG_BARI = 16.8719


def _inserisci_mezzo(db, codice: str, stato: str = "Disponibile") -> str:
    with Session(db) as s:
        s.execute(text("""
            INSERT INTO mezzi (codice, tipo, stato, lat, lng, batteria)
            VALUES (:codice, 'monopattino', :stato, :lat, :lng, 80)
        """), {"codice": codice, "stato": stato, "lat": LAT_BARI, "lng": LNG_BARI})
        s.commit()
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
    return str(row.id)


def _elimina_mezzo(db, mezzo_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": mezzo_id})
        s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": mezzo_id})
        s.commit()


class TestServizioMobilitaDismetti:

    @pytest.mark.integration
    def test_verifica_dismissione_ok(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-VD-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            with Session(db) as s:
                ris = ServizioMobilita(s).verifica_dismissione(_uuid.UUID(mezzo_id))
            assert ris["dismettibile"] is True
            assert ris["motivo"] is None
            assert ris["mezzo"]["id"] == mezzo_id
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_verifica_dismissione_stato_bloccante(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-VB-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            with Session(db) as s:
                ris = ServizioMobilita(s).verifica_dismissione(_uuid.UUID(mezzo_id))
            assert ris["dismettibile"] is False
            assert ris["motivo"] is not None
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_verifica_dismissione_corsa_attiva(self, db, utente_test):
        from bll.servizio_mobilita import ServizioMobilita
        codice = f"TEST-VC-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        corsa_id = str(_uuid.uuid4())
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO corse (id, utente_id, mezzo_id, stato, inizio_at)
                VALUES (:id, :uid, :mid, 'in_uso', now())
            """), {"id": corsa_id, "uid": str(utente_test["id"]), "mid": mezzo_id})
            s.commit()
        try:
            with Session(db) as s:
                ris = ServizioMobilita(s).verifica_dismissione(_uuid.UUID(mezzo_id))
            assert ris["dismettibile"] is False
        finally:
            with Session(db) as s:
                s.execute(text("DELETE FROM corse WHERE id = :id"), {"id": corsa_id})
                s.commit()
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_dismetti_mezzo_ok(self, db):
        from bll.servizio_mobilita import ServizioMobilita
        from dal.mezzo_repository import MezzoRepository
        codice = f"TEST-DM-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "Disponibile")
        try:
            with Session(db) as s:
                ServizioMobilita(s).dismetti_mezzo(_uuid.UUID(mezzo_id))
            assert MezzoRepository(db).trova_per_id(_uuid.UUID(mezzo_id))["stato"] == "Dismesso"
        finally:
            _elimina_mezzo(db, mezzo_id)

    @pytest.mark.integration
    def test_dismetti_mezzo_non_trovato(self, db):
        from bll.servizio_mobilita import ServizioMobilita, MezzoNonTrovatoException
        with Session(db) as s:
            with pytest.raises(MezzoNonTrovatoException):
                ServizioMobilita(s).dismetti_mezzo(_uuid.uuid4())

    @pytest.mark.integration
    def test_dismetti_mezzo_in_missione(self, db):
        from bll.servizio_mobilita import ServizioMobilita, MezzoInMissioneException
        codice = f"TEST-DI-{_uuid.uuid4().hex[:6]}"
        mezzo_id = _inserisci_mezzo(db, codice, "In uso")
        try:
            with Session(db) as s:
                with pytest.raises(MezzoInMissioneException):
                    ServizioMobilita(s).dismetti_mezzo(_uuid.UUID(mezzo_id))
        finally:
            _elimina_mezzo(db, mezzo_id)
```

- [ ] **Step 2: Esegui il test per verificare che fallisca**

```bash
cd backend && uv run pytest tests/test_dismetti_mezzo.py -v -m integration
```

Atteso: `FAILED` — `AttributeError: 'ServizioMobilita' object has no attribute 'verifica_dismissione'`

- [ ] **Step 3: Aggiungi `verifica_dismissione` e `dismetti_mezzo` a `ServizioMobilita`**

Apri `backend/bll/servizio_mobilita.py` e aggiungi dopo `aggiungi_mezzo`:

```python
    # [IF-OP.12] CS-12 — Verifica se un mezzo può essere dismesso (senza effetti collaterali)
    def verifica_dismissione(self, mezzo_id: UUID) -> dict:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")
        stati_bloccanti = {"In uso", "In pausa", "Prenotato"}
        if mezzo["stato"] in stati_bloccanti or self._mezzo_repo.ha_corse_attive(mezzo_id):
            return {
                "dismettibile": False,
                "motivo": f"Mezzo non dismettibile (stato: {mezzo['stato']})",
                "mezzo": mezzo,
            }
        return {"dismettibile": True, "motivo": None, "mezzo": mezzo}

    # [IF-OP.12] CS-12 — Dismette il mezzo impostando lo stato a "Dismesso"
    def dismetti_mezzo(self, mezzo_id: UUID) -> None:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")
        stati_bloccanti = {"In uso", "In pausa", "Prenotato"}
        if mezzo["stato"] in stati_bloccanti or self._mezzo_repo.ha_corse_attive(mezzo_id):
            raise MezzoInMissioneException(f"Mezzo {mezzo_id} ha missioni attive")
        self._mezzo_repo.aggiorna_stato(mezzo_id, "Dismesso")
```

- [ ] **Step 4: Esegui i test per verificare che passino**

```bash
cd backend && uv run pytest tests/test_dismetti_mezzo.py -v -m integration
```

Atteso: tutti e 6 i test `PASSED`.

- [ ] **Step 5: Commit**

```bash
git add backend/bll/servizio_mobilita.py backend/tests/test_dismetti_mezzo.py
git commit -m "feat(bll): aggiungi verifica_dismissione e dismetti_mezzo in ServizioMobilita [IF-OP.12]"
```

---

## Task 6: Controller — schemi Pydantic

**Files:**
- Modify: `backend/controllers/schemas.py`

- [ ] **Step 1: Aggiungi i due nuovi schemi a `schemas.py`**

Apri `backend/controllers/schemas.py` e aggiungi alla fine del file:

```python
class AggiungiMezzoRequest(BaseModel):
    tipo: str       # "monopattino" | "bicicletta" | "automobile"
    codice: str
    lat: float
    lng: float
    stato: str = "Disponibile"


class MezzoFlottaOut(BaseModel):
    id: UUID
    codice: str
    tipo: str
    stato: str
    lat: float | None
    lng: float | None
    batteria: int | None
```

- [ ] **Step 2: Verifica che il modulo importi correttamente**

```bash
cd backend && uv run python -c "from controllers.schemas import AggiungiMezzoRequest, MezzoFlottaOut; print('OK')"
```

Atteso: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/controllers/schemas.py
git commit -m "feat(controller): aggiungi schemi AggiungiMezzoRequest e MezzoFlottaOut [IF-OP.11/IF-OP.12]"
```

---

## Task 7: Controller — route `GET` e `POST /operatore/mezzi`

**Files:**
- Modify: `backend/controllers/mezzo_operatore_controller.py`

- [ ] **Step 1: Aggiungi gli import necessari in cima al controller**

Apri `backend/controllers/mezzo_operatore_controller.py`. Aggiungi `MezzoFlottaOut` e `AggiungiMezzoRequest` agli import dagli schemi esistenti:

```python
from controllers.schemas import (
    MezzoMappaOut,
    ConfigurazioneFineCorsaRequest,
    CreaTariffaRequest,
    TariffaResponse,
    AggiungiMezzoRequest,
    MezzoFlottaOut,
)
```

Sostituisci la riga di import degli schemi esistente con quella sopra.

- [ ] **Step 2: Aggiungi le due nuove route dopo il commento `[IF-OP.07]`**

Aggiungi dopo la route `@router.get("/mappa/mezzi", ...)` già esistente:

```python
# [IF-OP.11] CS-11 — Lista flotta operatore (tutti i mezzi non dismessi)
@router.get("/mezzi", response_model=list[MezzoFlottaOut])
def lista_mezzi_flotta(
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    return ServizioMobilita(db).get_mezzi_flotta()


# [IF-OP.11] CS-11 — Aggiunge nuovo mezzo alla flotta
@router.post("/mezzi", response_model=MezzoFlottaOut, status_code=201)
def aggiungi_mezzo(
    body: AggiungiMezzoRequest,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    from bll.servizio_mobilita import IdentificativoEsistenteException, PosizioneNonOperativaException
    tipi_validi = {"monopattino", "bicicletta", "automobile"}
    if body.tipo not in tipi_validi:
        raise HTTPException(status_code=422, detail=f"tipo non valido: {body.tipo}")
    if not body.codice.strip():
        raise HTTPException(status_code=422, detail="codice non può essere vuoto")
    try:
        return ServizioMobilita(db).aggiungi_mezzo(
            body.tipo, body.codice.strip(), body.lat, body.lng, body.stato
        )
    except IdentificativoEsistenteException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PosizioneNonOperativaException as e:
        raise HTTPException(status_code=422, detail=str(e))
```

- [ ] **Step 3: Verifica che il backend si avvii senza errori**

```bash
cd backend && uv run uvicorn main:app --reload &
sleep 3
curl -s http://localhost:8000/docs | grep -o "openapi" | head -1
pkill -f uvicorn
```

Atteso: `openapi`

- [ ] **Step 4: Commit**

```bash
git add backend/controllers/mezzo_operatore_controller.py
git commit -m "feat(controller): aggiungi GET e POST /operatore/mezzi [IF-OP.11]"
```

---

## Task 8: Controller — route `POST .../verifica` e `DELETE /operatore/mezzi/{id}`

**Files:**
- Modify: `backend/controllers/mezzo_operatore_controller.py`

- [ ] **Step 1: Aggiungi le due route rimanenti**

Apri `backend/controllers/mezzo_operatore_controller.py` e aggiungi dopo le route aggiunte in Task 7:

```python
# [IF-OP.12] CS-12 — Verifica se un mezzo può essere dismesso (no side-effects)
@router.post("/mezzi/{mezzo_id}/verifica")
def verifica_dismissione(
    mezzo_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    from bll.servizio_mobilita import MezzoNonTrovatoException
    try:
        return ServizioMobilita(db).verifica_dismissione(mezzo_id)
    except MezzoNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))


# [IF-OP.12] CS-12 — Dismette il mezzo (imposta stato "Dismesso")
@router.delete("/mezzi/{mezzo_id}")
def dismetti_mezzo(
    mezzo_id: UUID,
    _=Depends(verify_token(["OP"])),
    db: Session = Depends(get_db),
):
    from bll.servizio_mobilita import MezzoNonTrovatoException, MezzoInMissioneException
    try:
        ServizioMobilita(db).dismetti_mezzo(mezzo_id)
        return {"status": "ok"}
    except MezzoNonTrovatoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MezzoInMissioneException as e:
        raise HTTPException(status_code=409, detail=str(e))
```

- [ ] **Step 2: Aggiungi i test HTTP di integrazione per le 4 route**

Crea `backend/tests/test_aggiungi_mezzo_http.py`:

```python
import pytest
import uuid as _uuid
import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session

BASE = "http://localhost:8000"
LAT_BARI = 41.1177
LNG_BARI = 16.8719


def _login_op(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


def _elimina_mezzo(db, codice: str) -> None:
    with Session(db) as s:
        row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
        if row:
            s.execute(text("DELETE FROM corse WHERE mezzo_id = :id"), {"id": str(row.id)})
            s.execute(text("DELETE FROM mezzi WHERE id = :id"), {"id": str(row.id)})
            s.commit()


def _inserisci_zona_operativa(db) -> str:
    with Session(db) as s:
        row = s.execute(text("""
            INSERT INTO zone (nome, tipo, perimetro, limite_velocita)
            VALUES ('ZonaTestHTTP', 'operativa',
                ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[16.8,41.0],[16.95,41.0],[16.95,41.2],[16.8,41.2],[16.8,41.0]]]}'),
                NULL)
            RETURNING id
        """)).fetchone()
        s.commit()
        return str(row.id)


def _elimina_zona(db, zona_id: str) -> None:
    with Session(db) as s:
        s.execute(text("DELETE FROM zone WHERE id = :id"), {"id": zona_id})
        s.commit()


class TestAggiungiMezzoHTTP:

    @pytest.mark.integration
    def test_get_mezzi_flotta_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        r = httpx.get(f"{BASE}/operatore/mezzi", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    @pytest.mark.integration
    def test_post_mezzo_201(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        zona_id = _inserisci_zona_operativa(db)
        codice = f"HTTP-OK-{_uuid.uuid4().hex[:6]}"
        try:
            r = httpx.post(
                f"{BASE}/operatore/mezzi",
                json={"tipo": "monopattino", "codice": codice, "lat": LAT_BARI, "lng": LNG_BARI},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 201, r.text
            assert r.json()["codice"] == codice
        finally:
            _elimina_mezzo(db, codice)
            _elimina_zona(db, zona_id)

    @pytest.mark.integration
    def test_post_mezzo_409_duplicato(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        zona_id = _inserisci_zona_operativa(db)
        codice = f"HTTP-DUP-{_uuid.uuid4().hex[:6]}"
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO mezzi (codice, tipo, stato, lat, lng)
                VALUES (:c, 'monopattino', 'Disponibile', :lat, :lng)
            """), {"c": codice, "lat": LAT_BARI, "lng": LNG_BARI})
            s.commit()
        try:
            r = httpx.post(
                f"{BASE}/operatore/mezzi",
                json={"tipo": "monopattino", "codice": codice, "lat": LAT_BARI, "lng": LNG_BARI},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 409
        finally:
            _elimina_mezzo(db, codice)
            _elimina_zona(db, zona_id)

    @pytest.mark.integration
    def test_verifica_dismissione_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        codice = f"HTTP-VD-{_uuid.uuid4().hex[:6]}"
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO mezzi (codice, tipo, stato, lat, lng)
                VALUES (:c, 'monopattino', 'Disponibile', :lat, :lng)
            """), {"c": codice, "lat": LAT_BARI, "lng": LNG_BARI})
            s.commit()
            row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
            mezzo_id = str(row.id)
        try:
            r = httpx.post(
                f"{BASE}/operatore/mezzi/{mezzo_id}/verifica",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200
            assert r.json()["dismettibile"] is True
        finally:
            _elimina_mezzo(db, codice)

    @pytest.mark.integration
    def test_delete_mezzo_200(self, db, operatore_test):
        token = _login_op(operatore_test["email"], operatore_test["password"])
        codice = f"HTTP-DEL-{_uuid.uuid4().hex[:6]}"
        with Session(db) as s:
            s.execute(text("""
                INSERT INTO mezzi (codice, tipo, stato, lat, lng)
                VALUES (:c, 'monopattino', 'Disponibile', :lat, :lng)
            """), {"c": codice, "lat": LAT_BARI, "lng": LNG_BARI})
            s.commit()
            row = s.execute(text("SELECT id FROM mezzi WHERE codice = :c"), {"c": codice}).fetchone()
            mezzo_id = str(row.id)
        try:
            r = httpx.delete(
                f"{BASE}/operatore/mezzi/{mezzo_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert r.status_code == 200
        finally:
            _elimina_mezzo(db, codice)
```

- [ ] **Step 3: Avvia il backend e lancia i test HTTP**

In un terminale separato:
```bash
cd backend && uv run uvicorn main:app --reload
```

In un altro terminale:
```bash
cd backend && uv run pytest tests/test_aggiungi_mezzo_http.py tests/test_dismetti_mezzo.py tests/test_aggiungi_mezzo.py -v -m integration
```

Atteso: tutti i test `PASSED`.

- [ ] **Step 4: Commit**

```bash
git add backend/controllers/mezzo_operatore_controller.py backend/tests/test_aggiungi_mezzo_http.py
git commit -m "feat(controller): aggiungi route verifica e dismetti mezzo [IF-OP.12]"
```

---

## Task 9: Frontend — `FlottaService.ts`

**Files:**
- Modify: `frontend/src/services/FlottaService.ts`

- [ ] **Step 1: Riscrivi `FlottaService.ts`**

Apri `frontend/src/services/FlottaService.ts` e sostituisci l'intero contenuto:

```typescript
import { api } from './ApiService'

export interface MezzoFlotta {
  id: string
  codice: string
  tipo: string
  stato: string
  lat: number | null
  lng: number | null
  batteria: number | null
}

export interface AggiungiMezzoPayload {
  tipo: string
  codice: string
  lat: number
  lng: number
  stato: string
}

export interface ZonaParcheggio {
  id: string
  nome: string
}

export interface ConfigurazioneFinecorsa {
  durata_max_prenotazione_min: number
  durata_periodo_grazia_min: number
  max_mezzi_per_utente: number
  tipo_vincolo: 'penale' | 'divieto' | 'avviso'
  batteria_minima: number | null
  penale_fuori_zona: number
  zone_parcheggio: ZonaParcheggio[]
}

// [IF-OP.11] Lista flotta operatore
export const getMezziFlotta = (): Promise<{ data: MezzoFlotta[] }> =>
  api.get('/operatore/mezzi')

// [IF-OP.11] Aggiunge nuovo mezzo
export const aggiungiMezzo = (mezzo: AggiungiMezzoPayload): Promise<{ data: MezzoFlotta }> =>
  api.post('/operatore/mezzi', mezzo)

// [IF-OP.12] Verifica se il mezzo può essere dismesso
export const verificaDismissione = (
  id: string
): Promise<{ data: { dismettibile: boolean; motivo: string | null; mezzo: MezzoFlotta } }> =>
  api.post(`/operatore/mezzi/${id}/verifica`, {})

// [IF-OP.12] Dismette il mezzo
export const dismetti = (id: string): Promise<{ data: { status: string } }> =>
  api.delete(`/operatore/mezzi/${id}`)

// [IF-OP.04] Modifica Stato Mezzo (implementato separatamente)
export const modificaStato = (id: string, stato: string) =>
  api.put(`/operatore/mezzi/${id}/stato`, { stato })

export interface Tariffa {
  id: string
  tipo_mezzo: string
  costo_al_minuto: number
  costo_al_km: number
}

// [IF-OP.07] Definisce Tariffa
export const getTariffe = (): Promise<{ data: Tariffa[] }> =>
  api.get('/operatore/tariffe')

export const creaTariffa = (
  tipo_mezzo: string,
  costo_al_minuto: number,
  costo_al_km: number,
): Promise<{ data: Tariffa }> =>
  api.post('/operatore/tariffe', { tipo_mezzo, costo_al_minuto, costo_al_km })

export const aggiornaTariffa = (
  tipo_mezzo: string,
  costo_al_minuto: number,
  costo_al_km: number,
): Promise<{ data: Tariffa }> =>
  api.put(`/operatore/tariffe/${tipo_mezzo}`, { tipo_mezzo, costo_al_minuto, costo_al_km })

// [IF-OP.13] Configurazione regole fine corsa
export const getConfigurazioneFinecorsa = async (): Promise<ConfigurazioneFinecorsa> => {
  const r = await api.get<ConfigurazioneFinecorsa>('/operatore/configurazione/fine-corsa')
  return r.data
}

export const salvaConfigurazioneFinecorsa = async (
  config: Omit<ConfigurazioneFinecorsa, 'zone_parcheggio'>
): Promise<void> => {
  await api.post('/operatore/configurazione/fine-corsa', config)
}
```

- [ ] **Step 2: Verifica che la build TypeScript non abbia errori**

```bash
cd frontend && npm run build 2>&1 | tail -10
```

Atteso: `built in Xs` senza errori TypeScript.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/services/FlottaService.ts
git commit -m "feat(frontend): aggiorna FlottaService con path corretti e nuovi metodi [IF-OP.11/IF-OP.12]"
```

---

## Task 10: Frontend — `VistaMezziOperatore.tsx` e `.css`

**Files:**
- Create: `frontend/src/views/operatore/VistaMezziOperatore.tsx`
- Create: `frontend/src/views/operatore/VistaMezziOperatore.css`

- [ ] **Step 1: Crea `VistaMezziOperatore.css`**

Crea `frontend/src/views/operatore/VistaMezziOperatore.css`:

```css
.vmezzi {
  min-height: 100vh;
  background: #f8fafc;
  font-family: 'Inter', sans-serif;
}

.vmezzi__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 32px;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  gap: 16px;
}

.vmezzi__header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.vmezzi__back {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  padding: 4px 8px;
  border-radius: 8px;
  color: #64748b;
  transition: background 0.15s;
}

.vmezzi__back:hover {
  background: #f1f5f9;
}

.vmezzi__titolo {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.vmezzi__btn-aggiungi {
  background: #4caf9a;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s;
}

.vmezzi__btn-aggiungi:hover {
  background: #38a385;
}

.vmezzi__body {
  padding: 32px;
}

.vmezzi__tabella-wrapper {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,.07);
  overflow-x: auto;
}

.vmezzi__tabella {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.vmezzi__tabella th {
  background: #f8fafc;
  color: #64748b;
  font-weight: 600;
  text-align: left;
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.vmezzi__tabella td {
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  vertical-align: middle;
}

.vmezzi__tabella tr:last-child td {
  border-bottom: none;
}

.vmezzi__tabella tr:hover td {
  background: #f8fafc;
}

.vmezzi__pill {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.vmezzi__pill--disponibile { background: #dcfce7; color: #166534; }
.vmezzi__pill--prenotato   { background: #fef9c3; color: #854d0e; }
.vmezzi__pill--in-uso      { background: #dbeafe; color: #1e40af; }
.vmezzi__pill--in-pausa    { background: #e0e7ff; color: #3730a3; }
.vmezzi__pill--manutenzione{ background: #ffedd5; color: #c2410c; }
.vmezzi__pill--fuori       { background: #fee2e2; color: #991b1b; }

.vmezzi__btn-dismetti {
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #ef4444;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}

.vmezzi__btn-dismetti:hover {
  background: #fee2e2;
  border-color: #ef4444;
}

.vmezzi__empty {
  text-align: center;
  color: #94a3b8;
  padding: 48px 0;
}

/* ── Modal ── */
.vmezzi__overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.vmezzi__modal {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  width: 440px;
  max-width: 95vw;
  box-shadow: 0 8px 32px rgba(0,0,0,.15);
}

.vmezzi__modal h2 {
  margin: 0 0 24px;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

.vmezzi__campo {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.vmezzi__campo label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.vmezzi__campo input,
.vmezzi__campo select {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s;
}

.vmezzi__campo input:focus,
.vmezzi__campo select:focus {
  border-color: #4caf9a;
}

.vmezzi__errore {
  color: #ef4444;
  font-size: 13px;
  margin: 0 0 12px;
}

.vmezzi__modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}

.vmezzi__btn-annulla {
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
}

.vmezzi__btn-conferma {
  background: #4caf9a;
  border: none;
  border-radius: 24px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  cursor: pointer;
}

.vmezzi__btn-conferma:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.vmezzi__btn-conferma--danger {
  background: #ef4444;
}

/* ── Toast ── */
.vmezzi__toast {
  position: fixed;
  bottom: 32px;
  right: 32px;
  padding: 14px 22px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  z-index: 200;
  box-shadow: 0 4px 16px rgba(0,0,0,.15);
}

.vmezzi__toast--ok  { background: #22c55e; }
.vmezzi__toast--err { background: #ef4444; }

/* ── Skeleton ── */
.vmezzi__skeleton td {
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 400% 100%;
  animation: shimmer 1.2s infinite;
  height: 18px;
  border-radius: 4px;
}

@keyframes shimmer {
  0%   { background-position: 100% 50%; }
  100% { background-position: 0%   50%; }
}
```

- [ ] **Step 2: Crea `VistaMezziOperatore.tsx`**

Crea `frontend/src/views/operatore/VistaMezziOperatore.tsx`:

```tsx
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import {
  getMezziFlotta,
  aggiungiMezzo,
  verificaDismissione,
  dismetti,
  type MezzoFlotta,
  type AggiungiMezzoPayload,
} from '../../services/FlottaService'
import './VistaMezziOperatore.css'

const TIPO_EMOJI: Record<string, string> = {
  monopattino: '🛴',
  bicicletta: '🚲',
  automobile: '🚗',
}

const STATO_PILL_CLASS: Record<string, string> = {
  'Disponibile':    'vmezzi__pill--disponibile',
  'Prenotato':      'vmezzi__pill--prenotato',
  'In uso':         'vmezzi__pill--in-uso',
  'In pausa':       'vmezzi__pill--in-pausa',
  'In manutenzione':'vmezzi__pill--manutenzione',
  'Fuori servizio': 'vmezzi__pill--fuori',
}

interface FormState {
  tipo: string
  codice: string
  lat: string
  lng: string
  stato: string
}

const FORM_VUOTO: FormState = {
  tipo: 'monopattino',
  codice: '',
  lat: '',
  lng: '',
  stato: 'Disponibile',
}

interface Toast { msg: string; tipo: 'ok' | 'err' }

export default function VistaMezziOperatore() {
  const navigate = useNavigate()
  const [mezzi, setMezzi] = useState<MezzoFlotta[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [toast, setToast] = useState<Toast | null>(null)
  const [mostraModal, setMostraModal] = useState(false)
  const [form, setForm] = useState<FormState>(FORM_VUOTO)
  const [erroreForm, setErroreForm] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [confermaDismissione, setConfermaDismissione] = useState<MezzoFlotta | null>(null)
  const [controllando, setControllando] = useState(false)

  const mostraToast = (msg: string, tipo: 'ok' | 'err') => {
    setToast({ msg, tipo })
    setTimeout(() => setToast(null), 3500)
  }

  const ricarica = useCallback(() => {
    setCaricamento(true)
    getMezziFlotta()
      .then(r => setMezzi(r.data))
      .catch(() => mostraToast('Errore nel caricamento della flotta', 'err'))
      .finally(() => setCaricamento(false))
  }, [])

  useEffect(() => { ricarica() }, [ricarica])

  const apriModal = () => {
    setForm(FORM_VUOTO)
    setErroreForm('')
    setMostraModal(true)
  }

  const handleCampo = (k: keyof FormState, v: string) =>
    setForm(f => ({ ...f, [k]: v }))

  const handleSubmitAggiungi = async () => {
    if (!form.codice.trim()) {
      setErroreForm('Il codice è obbligatorio')
      return
    }
    const lat = parseFloat(form.lat)
    const lng = parseFloat(form.lng)
    if (isNaN(lat) || isNaN(lng)) {
      setErroreForm('Latitudine e longitudine devono essere numeri validi')
      return
    }
    const payload: AggiungiMezzoPayload = {
      tipo: form.tipo,
      codice: form.codice.trim(),
      lat,
      lng,
      stato: form.stato,
    }
    setSubmitting(true)
    setErroreForm('')
    try {
      await aggiungiMezzo(payload)
      setMostraModal(false)
      ricarica()
      mostraToast('Mezzo aggiunto con successo', 'ok')
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail ?? 'Errore durante l\'aggiunta'
        if (err.response?.status === 409) {
          setErroreForm('Identificativo già in uso. Scegli un codice diverso.')
        } else {
          setErroreForm(String(detail))
        }
      } else {
        setErroreForm('Errore imprevisto')
      }
    } finally {
      setSubmitting(false)
    }
  }

  const handleCliccaDismetti = async (mezzo: MezzoFlotta) => {
    setControllando(true)
    try {
      const r = await verificaDismissione(mezzo.id)
      if (r.data.dismettibile) {
        setConfermaDismissione(mezzo)
      } else {
        mostraToast(r.data.motivo ?? 'Impossibile dismettere il mezzo', 'err')
      }
    } catch {
      mostraToast('Errore durante la verifica', 'err')
    } finally {
      setControllando(false)
    }
  }

  const handleConfermaDismissione = async () => {
    if (!confermaDismissione) return
    try {
      await dismetti(confermaDismissione.id)
      setConfermaDismissione(null)
      ricarica()
      mostraToast('Mezzo dismesso con successo', 'ok')
    } catch {
      mostraToast('Errore durante la dismissione', 'err')
    }
  }

  return (
    <div className="vmezzi">
      <header className="vmezzi__header">
        <div className="vmezzi__header-left">
          <button className="vmezzi__back" onClick={() => navigate('/operatore/dashboard')}>
            ←
          </button>
          <h1 className="vmezzi__titolo">Gestione Flotta</h1>
        </div>
        <button className="vmezzi__btn-aggiungi" onClick={apriModal}>
          + Aggiungi mezzo
        </button>
      </header>

      <main className="vmezzi__body">
        <div className="vmezzi__tabella-wrapper">
          <table className="vmezzi__tabella">
            <thead>
              <tr>
                <th>Tipo</th>
                <th>Codice</th>
                <th>Stato</th>
                <th>Batteria</th>
                <th>Coordinate</th>
                <th>Azioni</th>
              </tr>
            </thead>
            <tbody>
              {caricamento ? (
                Array.from({ length: 4 }).map((_, i) => (
                  <tr key={i} className="vmezzi__skeleton">
                    {Array.from({ length: 6 }).map((_, j) => <td key={j}>&nbsp;</td>)}
                  </tr>
                ))
              ) : mezzi.length === 0 ? (
                <tr>
                  <td colSpan={6} className="vmezzi__empty">
                    Nessun mezzo in flotta
                  </td>
                </tr>
              ) : (
                mezzi.map(m => (
                  <tr key={m.id}>
                    <td>{TIPO_EMOJI[m.tipo] ?? '●'} {m.tipo}</td>
                    <td><strong>{m.codice}</strong></td>
                    <td>
                      <span className={`vmezzi__pill ${STATO_PILL_CLASS[m.stato] ?? ''}`}>
                        {m.stato}
                      </span>
                    </td>
                    <td>{m.batteria != null ? `${m.batteria}%` : '—'}</td>
                    <td>
                      {m.lat != null && m.lng != null
                        ? `${m.lat.toFixed(4)}, ${m.lng.toFixed(4)}`
                        : '—'}
                    </td>
                    <td>
                      <button
                        className="vmezzi__btn-dismetti"
                        disabled={controllando}
                        onClick={() => handleCliccaDismetti(m)}
                      >
                        Dismetti
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>

      {/* Modal aggiunta mezzo */}
      {mostraModal && (
        <div className="vmezzi__overlay" onClick={() => setMostraModal(false)}>
          <div className="vmezzi__modal" onClick={e => e.stopPropagation()}>
            <h2>Aggiungi nuovo mezzo</h2>

            <div className="vmezzi__campo">
              <label>Tipologia</label>
              <select value={form.tipo} onChange={e => handleCampo('tipo', e.target.value)}>
                <option value="monopattino">🛴 Monopattino</option>
                <option value="bicicletta">🚲 Bicicletta</option>
                <option value="automobile">🚗 Automobile</option>
              </select>
            </div>

            <div className="vmezzi__campo">
              <label>Codice identificativo</label>
              <input
                type="text"
                placeholder="es. MON-001"
                value={form.codice}
                onChange={e => handleCampo('codice', e.target.value)}
              />
            </div>

            <div className="vmezzi__campo">
              <label>Latitudine</label>
              <input
                type="number"
                step="0.0001"
                placeholder="es. 41.1177"
                value={form.lat}
                onChange={e => handleCampo('lat', e.target.value)}
              />
            </div>

            <div className="vmezzi__campo">
              <label>Longitudine</label>
              <input
                type="number"
                step="0.0001"
                placeholder="es. 16.8719"
                value={form.lng}
                onChange={e => handleCampo('lng', e.target.value)}
              />
            </div>

            <div className="vmezzi__campo">
              <label>Stato iniziale</label>
              <select value={form.stato} onChange={e => handleCampo('stato', e.target.value)}>
                <option value="Disponibile">Disponibile</option>
                <option value="In manutenzione">In manutenzione</option>
                <option value="Fuori servizio">Fuori servizio</option>
              </select>
            </div>

            {erroreForm && <p className="vmezzi__errore">{erroreForm}</p>}

            <div className="vmezzi__modal-footer">
              <button className="vmezzi__btn-annulla" onClick={() => setMostraModal(false)}>
                Annulla
              </button>
              <button
                className="vmezzi__btn-conferma"
                onClick={handleSubmitAggiungi}
                disabled={submitting}
              >
                {submitting ? 'Salvataggio…' : 'Aggiungi'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Dialog conferma dismissione */}
      {confermaDismissione && (
        <div className="vmezzi__overlay">
          <div className="vmezzi__modal">
            <h2>Conferma dismissione</h2>
            <p style={{ color: '#475569', marginBottom: 24 }}>
              Vuoi dismettere il mezzo <strong>{confermaDismissione.codice}</strong>?
              L'operazione è irreversibile e il mezzo non sarà più disponibile per nuove corse.
            </p>
            <div className="vmezzi__modal-footer">
              <button
                className="vmezzi__btn-annulla"
                onClick={() => setConfermaDismissione(null)}
              >
                Annulla
              </button>
              <button
                className="vmezzi__btn-conferma vmezzi__btn-conferma--danger"
                onClick={handleConfermaDismissione}
              >
                Dismetti
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Toast */}
      {toast && (
        <div className={`vmezzi__toast vmezzi__toast--${toast.tipo}`}>
          {toast.msg}
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 3: Verifica la build TypeScript**

```bash
cd frontend && npm run build 2>&1 | tail -10
```

Atteso: build completata senza errori TypeScript.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/operatore/VistaMezziOperatore.tsx frontend/src/views/operatore/VistaMezziOperatore.css
git commit -m "feat(frontend): aggiungi VistaMezziOperatore [IF-OP.11/IF-OP.12]"
```

---

## Task 11: Frontend — Routing in `App.tsx`

**Files:**
- Modify: `frontend/src/App.tsx`

- [ ] **Step 1: Aggiungi import e route**

Apri `frontend/src/App.tsx`.

Aggiungi l'import dopo quello di `VistaTariffePromozioni`:

```tsx
import VistaMezziOperatore from './views/operatore/VistaMezziOperatore'
```

Aggiungi la route **prima** della route catch-all `/operatore/*`:

```tsx
<Route
  path="/operatore/mezzi"
  element={
    <RoutaProtetta ruoloRichiesto="OP">
      <VistaMezziOperatore />
    </RoutaProtetta>
  }
/>
```

La route catch-all `/operatore/*` deve rimanere **dopo** questa.

- [ ] **Step 2: Verifica la build**

```bash
cd frontend && npm run build 2>&1 | tail -10
```

Atteso: build completata senza errori.

- [ ] **Step 3: Avvia il dev server e verifica manualmente**

```bash
cd backend && uv run uvicorn main:app --reload &
cd frontend && npm run dev
```

Accedi con un account Operatore. Naviga a `http://localhost:5173/operatore/mezzi`. Verifica:
- la tabella della flotta si carica correttamente
- il click su "+ Aggiungi mezzo" apre il modal
- l'inserimento di un mezzo con coordinate dentro Bari (lat: 41.1177, lng: 16.8719) riesce con toast verde
- il click su "Dismetti" su un mezzo disponibile mostra il dialog di conferma
- la conferma dismette il mezzo e aggiorna la lista

- [ ] **Step 4: Commit**

```bash
git add frontend/src/App.tsx
git commit -m "feat(frontend): aggiungi route /operatore/mezzi per VistaMezziOperatore [IF-OP.11/IF-OP.12]"
```

---

## Checklist finale

- [ ] `uv run pytest tests/ -v -m integration` — tutti i test passano
- [ ] `npm run build` — build TypeScript senza errori
- [ ] Flusso "Aggiungi mezzo" funzionante end-to-end in browser
- [ ] Flusso "Dismetti mezzo" (verifica → conferma → dismissione) funzionante in browser
- [ ] Errore 409 (identificativo duplicato) mostrato correttamente nel modal
- [ ] Toast errore se mezzo in missione attiva
