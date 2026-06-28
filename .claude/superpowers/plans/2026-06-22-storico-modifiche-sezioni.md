# Storico Modifiche — sezioni per categoria e diff leggibile — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Riorganizzare la vista "Storico Modifiche" [IF-OP.13] in sezioni per categoria con diff leggibile (solo campi cambiati, etichette in italiano), ed estendere il backend a registrare anche le modifiche a Tariffe e Offerte.

**Architecture:** Il backend riusa la convenzione testuale esistente `"campo1=valore1, campo2=valore2"` già usata da `parametri_sistema`/`regole_fine_corsa`/`zona_*` per loggare anche `tariffa_creata`, `tariffa_modificata`, `offerta_creata`, `offerta_modificata`, `offerta_eliminata` in `storico_modifiche` — nessuna modifica di schema. Il frontend riscrive `VistaStoricoModifiche.tsx` come accordion: parsing generico del formato `key=value`, calcolo diff (solo campi cambiati), raggruppamento in 5 categorie con etichette/unità per campo.

**Tech Stack:** FastAPI + SQLAlchemy 2.0 (backend), React 19 + TypeScript (frontend), pytest (test backend).

## Global Constraints

- Nessuna modifica allo schema DB di `storico_modifiche` (rimane `TEXT` per `valore_precedente`/`valore_nuovo`).
- Nessuna modifica a `parametri_sistema`, `regole_fine_corsa`, `zona_creata`, `zona_eliminata` — restano come sono.
- Il formato `"campo=valore, campo=valore"` va mantenuto identico per retrocompatibilità con le righe storiche già presenti.
- Layer architecture: Controller solo validazione HTTP/smistamento, BLL logica applicativa, DAL solo accesso dati (da CLAUDE.md del progetto).
- Branch dedicato: nessun commit diretto su `main` — lavorare su `feature/storico-modifiche-sezioni`.

---

### Task 1: Backend — logging storico per Tariffa

**Files:**
- Modify: `backend/bll/servizio_tariffa.py`
- Modify: `backend/controllers/tariffa_controller.py`
- Modify: `backend/tests/test_servizio_tariffa.py`
- Test: `backend/tests/test_storico_modifiche.py` (nuovo test di integrazione)

**Interfaces:**
- Consumes: `ServizioStoricoModifiche.registra_modifica(tipo_configurazione: str, descrizione: str, valore_precedente: str | None, valore_nuovo: str | None, operatore_id: UUID) -> None` (già esistente in `backend/bll/servizio_storico_modifiche.py`).
- Produces: `ServizioTariffa.crea_tariffa(tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float, operatore_id: UUID) -> dict` e `ServizioTariffa.aggiorna_tariffa(tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float, operatore_id: UUID) -> dict` — firme cambiate, nuovo parametro obbligatorio `operatore_id` in coda.

- [ ] **Step 1: Aggiorna i test unitari esistenti per il nuovo parametro `operatore_id`**

Apri `backend/tests/test_servizio_tariffa.py`. I test chiamano `ServizioTariffa().crea_tariffa(...)` e `.aggiorna_tariffa(...)` senza `operatore_id`. Aggiungi l'import e un `operatore_id` di test, e patcha `ServizioStoricoModifiche` per isolare il test dalla scrittura reale su DB:

```python
import uuid
from unittest.mock import MagicMock, patch
from decimal import Decimal


# [IF-OP.07 / IF-OP.08] Definisce Tariffa / Modifica Tariffa
class TestServizioTariffa:

    def test_get_tariffe_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        riga = MagicMock()
        riga.id = uuid.uuid4()
        riga.tipo_mezzo = "monopattino"
        riga.costo_al_minuto = Decimal("0.05")
        riga.costo_al_km = Decimal("0.10")

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.find_all.return_value = [riga]
            result = ServizioTariffa().get_tariffe()

        assert result == [{
            "id": str(riga.id),
            "tipo_mezzo": "monopattino",
            "costo_al_minuto": 0.05,
            "costo_al_km": 0.10,
        }]

    def test_get_tariffe_lista_vuota(self):
        from bll.servizio_tariffa import ServizioTariffa

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo:
            MockRepo.return_value.find_all.return_value = []
            result = ServizioTariffa().get_tariffe()

        assert result == []

    def test_crea_tariffa_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        tariffa = MagicMock()
        tariffa.id = uuid.uuid4()
        tariffa.tipo_mezzo = "bicicletta"
        tariffa.costo_al_minuto = Decimal("0.03")
        tariffa.costo_al_km = Decimal("0.08")
        operatore_id = uuid.uuid4()

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo, \
             patch("bll.servizio_tariffa.ServizioStoricoModifiche") as MockStorico:
            MockRepo.return_value.exists_by_tipologia.return_value = False
            MockRepo.return_value.crea.return_value = tariffa
            result = ServizioTariffa().crea_tariffa("bicicletta", 0.03, 0.08, operatore_id)

        MockRepo.return_value.crea.assert_called_once_with("bicicletta", Decimal("0.03"), Decimal("0.08"))
        assert result["tipo_mezzo"] == "bicicletta"
        MockStorico.return_value.registra_modifica.assert_called_once()
        kwargs = MockStorico.return_value.registra_modifica.call_args.kwargs
        assert kwargs["tipo_configurazione"] == "tariffa_creata"
        assert kwargs["valore_precedente"] is None
        assert "tipo_mezzo=bicicletta" in kwargs["valore_nuovo"]
        assert kwargs["operatore_id"] == operatore_id

    def test_crea_tariffa_gia_esistente(self):
        from bll.servizio_tariffa import ServizioTariffa, TariffaGiaEsistente

        operatore_id = uuid.uuid4()
        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo, \
             patch("bll.servizio_tariffa.ServizioStoricoModifiche"):
            MockRepo.return_value.exists_by_tipologia.return_value = True
            try:
                ServizioTariffa().crea_tariffa("bicicletta", 0.03, 0.08, operatore_id)
                assert False, "doveva lanciare TariffaGiaEsistente"
            except TariffaGiaEsistente:
                pass
        MockRepo.return_value.crea.assert_not_called()

    def test_aggiorna_tariffa_delega_al_repository(self):
        from bll.servizio_tariffa import ServizioTariffa

        precedente = MagicMock()
        precedente.tipo_mezzo = "monopattino"
        precedente.costo_al_minuto = Decimal("0.05")
        precedente.costo_al_km = Decimal("0.10")

        tariffa = MagicMock()
        tariffa.id = uuid.uuid4()
        tariffa.tipo_mezzo = "monopattino"
        tariffa.costo_al_minuto = Decimal("0.07")
        tariffa.costo_al_km = Decimal("0.12")
        operatore_id = uuid.uuid4()

        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo, \
             patch("bll.servizio_tariffa.ServizioStoricoModifiche") as MockStorico:
            MockRepo.return_value.find_by_tipologia.return_value = precedente
            MockRepo.return_value.aggiorna.return_value = tariffa
            result = ServizioTariffa().aggiorna_tariffa("monopattino", 0.07, 0.12, operatore_id)

        assert result["costo_al_minuto"] == 0.07
        kwargs = MockStorico.return_value.registra_modifica.call_args.kwargs
        assert kwargs["tipo_configurazione"] == "tariffa_modificata"
        assert "costo_al_minuto=0.05" in kwargs["valore_precedente"]
        assert "costo_al_minuto=0.07" in kwargs["valore_nuovo"]

    def test_aggiorna_tariffa_non_trovata(self):
        from bll.servizio_tariffa import ServizioTariffa, TariffaNonTrovata

        operatore_id = uuid.uuid4()
        with patch("bll.servizio_tariffa.TariffaRepository") as MockRepo, \
             patch("bll.servizio_tariffa.ServizioStoricoModifiche"):
            MockRepo.return_value.find_by_tipologia.return_value = None
            MockRepo.return_value.aggiorna.return_value = None
            try:
                ServizioTariffa().aggiorna_tariffa("monopattino", 0.07, 0.12, operatore_id)
                assert False, "doveva lanciare TariffaNonTrovata"
            except TariffaNonTrovata:
                pass
```

Nota: il test `test_aggiorna_tariffa_delega_al_repository` introduce `MockRepo.return_value.find_by_tipologia` — verifica nel passo 3 se `TariffaRepository` ha già un metodo per leggere una singola tariffa per tipo; se non esiste, nello Step 3 va usato `find_all()` e filtrato in `ServizioTariffa`, aggiornando questo mock di conseguenza a `find_all.return_value = [precedente]`.

- [ ] **Step 2: Verifica che il metodo per leggere la tariffa corrente esista nel repository**

```bash
grep -n "def " backend/dal/tariffa_repository.py
```

Se non esiste un metodo che restituisce la singola riga per `tipo_mezzo` (es. `find_by_tipologia`), usa `find_all()` filtrato in `ServizioTariffa.aggiorna_tariffa` (vedi Step 3) e correggi il test del Step 1 di conseguenza (sostituendo `find_by_tipologia` con `find_all`).

- [ ] **Step 3: Esegui i test — devono fallire (funzioni non ancora modificate)**

```bash
cd backend && uv run pytest tests/test_servizio_tariffa.py -v
```

Expected: FAIL — `TypeError: crea_tariffa() takes from 4 to 4 positional arguments but 5 were given` (o simile, dato che `operatore_id` non è ancora un parametro).

- [ ] **Step 4: Implementa il logging in `servizio_tariffa.py`**

```python
from decimal import Decimal
from uuid import UUID
from dal.tariffa_repository import TariffaRepository
from bll.servizio_storico_modifiche import ServizioStoricoModifiche


class TariffaNonTrovata(Exception):
    pass


class TariffaGiaEsistente(Exception):
    pass


class ServizioTariffa:
    """[IF-OP.07 / IF-OP.08] Definisce Tariffa / Modifica Tariffa."""

    def __init__(self, tariffa_repo: TariffaRepository | None = None):
        self._tariffa_repo = tariffa_repo or TariffaRepository()
        self._storico = ServizioStoricoModifiche()

    def get_tariffe(self) -> list[dict]:
        tariffe = self._tariffa_repo.find_all()
        return [
            {
                "id": str(t.id),
                "tipo_mezzo": t.tipo_mezzo,
                "costo_al_minuto": float(t.costo_al_minuto),
                "costo_al_km": float(t.costo_al_km),
            }
            for t in tariffe
        ]

    def crea_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float, operatore_id: UUID
    ) -> dict:
        if self._tariffa_repo.exists_by_tipologia(tipo_mezzo):
            raise TariffaGiaEsistente(f"Tariffa per '{tipo_mezzo}' già esistente")
        tariffa = self._tariffa_repo.crea(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_creata",
            descrizione=f"Creazione tariffa '{tipo_mezzo}'",
            valore_precedente=None,
            valore_nuovo=(
                f"tipo_mezzo={tariffa.tipo_mezzo}, "
                f"costo_al_minuto={tariffa.costo_al_minuto}, "
                f"costo_al_km={tariffa.costo_al_km}"
            ),
            operatore_id=operatore_id,
        )
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }

    def aggiorna_tariffa(
        self, tipo_mezzo: str, costo_al_minuto: float, costo_al_km: float, operatore_id: UUID
    ) -> dict:
        precedenti = [t for t in self._tariffa_repo.find_all() if t.tipo_mezzo == tipo_mezzo]
        precedente = precedenti[0] if precedenti else None
        tariffa = self._tariffa_repo.aggiorna(
            tipo_mezzo,
            Decimal(str(costo_al_minuto)),
            Decimal(str(costo_al_km)),
        )
        if not tariffa:
            raise TariffaNonTrovata(f"Nessuna tariffa per '{tipo_mezzo}'")
        self._storico.registra_modifica(
            tipo_configurazione="tariffa_modificata",
            descrizione=f"Modifica tariffa '{tipo_mezzo}'",
            valore_precedente=(
                f"tipo_mezzo={precedente.tipo_mezzo}, "
                f"costo_al_minuto={precedente.costo_al_minuto}, "
                f"costo_al_km={precedente.costo_al_km}"
            ) if precedente is not None else None,
            valore_nuovo=(
                f"tipo_mezzo={tariffa.tipo_mezzo}, "
                f"costo_al_minuto={tariffa.costo_al_minuto}, "
                f"costo_al_km={tariffa.costo_al_km}"
            ),
            operatore_id=operatore_id,
        )
        return {
            "id": str(tariffa.id),
            "tipo_mezzo": tariffa.tipo_mezzo,
            "costo_al_minuto": float(tariffa.costo_al_minuto),
            "costo_al_km": float(tariffa.costo_al_km),
        }
```

Adatta `precedenti = [...]` a `find_by_tipologia` se quel metodo esiste già (Step 2), per evitare di scaricare tutta la tabella.

- [ ] **Step 5: Aggiorna `tariffa_controller.py` per passare `operatore_id`**

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from middleware.auth_middleware import verify_token
from bll.servizio_tariffa import ServizioTariffa, TariffaGiaEsistente, TariffaNonTrovata
from controllers.schemas import CreaTariffaRequest, TariffaResponse

router = APIRouter(prefix="/operatore", tags=["Tariffe"])
_servizio = ServizioTariffa()


# [IF-OP.07] Definisce Tariffa
@router.get("/tariffe", response_model=list[TariffaResponse])
def lista_tariffe(_=Depends(verify_token(["OP"]))):
    return _servizio.get_tariffe()


@router.post("/tariffe", response_model=TariffaResponse, status_code=status.HTTP_201_CREATED)
def crea_tariffa(
    body: CreaTariffaRequest,
    _op=Depends(verify_token(["OP"])),
):
    try:
        return _servizio.crea_tariffa(
            body.tipo_mezzo, body.costo_al_minuto, body.costo_al_km, UUID(str(_op["id"]))
        )
    except TariffaGiaEsistente as e:
        raise HTTPException(status_code=409, detail=str(e))


# [IF-OP.08] Modifica Tariffa
@router.put("/tariffe/{tipo_mezzo}", response_model=TariffaResponse)
def aggiorna_tariffa(
    tipo_mezzo: str,
    body: CreaTariffaRequest,
    _op=Depends(verify_token(["OP"])),
):
    try:
        return _servizio.aggiorna_tariffa(
            tipo_mezzo, body.costo_al_minuto, body.costo_al_km, UUID(str(_op["id"]))
        )
    except TariffaNonTrovata as e:
        raise HTTPException(status_code=404, detail=str(e))
```

- [ ] **Step 6: Esegui i test unitari — devono passare**

```bash
cd backend && uv run pytest tests/test_servizio_tariffa.py -v
```

Expected: PASS su tutti i test.

- [ ] **Step 7: Aggiungi test di integrazione in `test_storico_modifiche.py`**

Apri `backend/tests/test_storico_modifiche.py` e aggiungi questo test alla classe `TestIntegrazioneServiziEsistenti` (dopo `test_crea_ed_elimina_zona_registrano_modifica_nello_storico`):

```python
    def test_crea_e_aggiorna_tariffa_registrano_modifica_nello_storico(self, db):
        from bll.servizio_tariffa import ServizioTariffa

        operatore_id = _uuid.uuid4()
        tipo_mezzo = f"test-mezzo-{operatore_id.hex[:6]}"
        try:
            ServizioTariffa().crea_tariffa(tipo_mezzo, 0.05, 0.10, operatore_id)
            ServizioTariffa().aggiorna_tariffa(tipo_mezzo, 0.07, 0.12, operatore_id)
            storico = ServizioStoricoModifiche().get_storico()
            tipi_evento = [
                v["tipo_configurazione"]
                for v in storico
                if v["operatore_id"] == str(operatore_id)
            ]
            assert "tariffa_creata" in tipi_evento
            assert "tariffa_modificata" in tipi_evento
        finally:
            _pulisci(db, operatore_id)
            with Session(db) as session:
                session.execute(text("DELETE FROM tariffe WHERE tipo_mezzo = :t"), {"t": tipo_mezzo})
                session.commit()
```

- [ ] **Step 8: Esegui i test di integrazione**

```bash
cd backend && uv run pytest tests/test_storico_modifiche.py -v -m integration
```

Expected: PASS (richiede `DATABASE_URL` in `backend/.env`).

- [ ] **Step 9: Commit**

```bash
git add backend/bll/servizio_tariffa.py backend/controllers/tariffa_controller.py backend/tests/test_servizio_tariffa.py backend/tests/test_storico_modifiche.py
git commit -m "feat(storico): registra creazione e modifica tariffe nello storico modifiche"
```

---

### Task 2: Backend — logging storico per Offerta

**Files:**
- Modify: `backend/bll/servizio_offerte.py`
- Modify: `backend/controllers/offerta_controller.py`
- Test: `backend/tests/test_storico_modifiche.py` (nuovo test di integrazione)

**Interfaces:**
- Consumes: `ServizioStoricoModifiche.registra_modifica(...)` (come Task 1).
- Produces: `ServizioOfferta.crea_offerta(..., operatore_id: UUID)`, `ServizioOfferta.modifica_offerta(..., operatore_id: UUID)`, `ServizioOfferta.elimina_offerta(offerta_id: UUID, db: Session, operatore_id: UUID) -> None` — tutte con nuovo parametro `operatore_id` obbligatorio.

- [ ] **Step 1: Esegui i test HTTP esistenti per avere una baseline**

```bash
cd backend && uv run pytest tests/test_offerte.py -v -m integration
```

Expected: PASS (baseline prima delle modifiche — richiede server/DB attivi secondo `conftest.py`).

- [ ] **Step 2: Implementa il logging in `servizio_offerte.py`**

Aggiungi l'helper privato `_serializza` e usa `registra_modifica` nei tre metodi di scrittura:

```python
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from dal.offerta_repository import OffertaRepository, NomeDuplicatoException, OffertaNonTrovataException
from model.offerta import Offerta, Promozione, Abbonamento
from bll.servizio_storico_modifiche import ServizioStoricoModifiche


class OffertaValidazioneException(Exception):
    pass


class OffertaDuplicataException(Exception):
    pass


class ServizioOfferta:

    def __init__(self) -> None:
        self._repo = OffertaRepository()
        self._storico = ServizioStoricoModifiche()

    def lista_offerte(self, db: Session) -> list[Offerta]:
        return self._repo.lista(db)

    @staticmethod
    def _serializza(offerta: Offerta) -> str:
        return (
            f"nome={offerta.nome}, tipo={offerta.tipo}, stato={offerta.stato}, "
            f"descrizione={offerta.descrizione}, sconto_percentuale={offerta.sconto_percentuale}, "
            f"prezzo={offerta.prezzo}, durata_giorni={offerta.durata_giorni}, "
            f"data_inizio={offerta.data_inizio}, data_scadenza={offerta.data_scadenza}, "
            f"tipo_mezzo={offerta.tipo_mezzo}"
        )

    def crea_offerta(
        self,
        nome: str,
        tipo: str,
        descrizione: Optional[str],
        sconto_percentuale: Optional[Decimal],
        prezzo: Optional[Decimal],
        durata_giorni: Optional[int],
        data_inizio: Optional[datetime],
        data_scadenza: Optional[datetime],
        db: Session,
        operatore_id: uuid.UUID,
        tipo_mezzo: Optional[str] = None,
    ) -> Offerta:
        self._valida(
            nome=nome,
            tipo=tipo,
            sconto_percentuale=sconto_percentuale,
            prezzo=prezzo,
            durata_giorni=durata_giorni,
            data_scadenza=data_scadenza,
            tipo_mezzo=tipo_mezzo,
            data_inizio=data_inizio,
        )
        try:
            offerta = self._repo.crea(
                nome=nome,
                tipo=tipo,
                descrizione=descrizione,
                sconto_percentuale=sconto_percentuale,
                prezzo=prezzo,
                durata_giorni=durata_giorni,
                data_inizio=data_inizio,
                data_scadenza=data_scadenza,
                db=db,
                tipo_mezzo=tipo_mezzo,
            )
        except NomeDuplicatoException:
            raise OffertaDuplicataException(f"Esiste già un'offerta con nome '{nome}'")
        self._storico.registra_modifica(
            tipo_configurazione="offerta_creata",
            descrizione=f"Creazione offerta '{nome}'",
            valore_precedente=None,
            valore_nuovo=self._serializza(offerta),
            operatore_id=operatore_id,
        )
        return offerta

    def modifica_offerta(
        self,
        offerta_id: uuid.UUID,
        db: Session,
        operatore_id: uuid.UUID,
        nome: Optional[str] = None,
        descrizione: Optional[str] = None,
        sconto_percentuale: Optional[Decimal] = None,
        prezzo: Optional[Decimal] = None,
        durata_giorni: Optional[int] = None,
        data_inizio: Optional[datetime] = None,
        data_scadenza: Optional[datetime] = None,
        stato: Optional[str] = None,
        tipo_mezzo: Optional[str] = None,
    ) -> Offerta:
        try:
            offerta_corrente = self._repo.trova_per_id(offerta_id, db)
        except OffertaNonTrovataException:
            raise OffertaValidazioneException(f"Offerta {offerta_id} non trovata")
        valore_precedente = self._serializza(offerta_corrente)
        nome_precedente = offerta_corrente.nome
        tipo = offerta_corrente.tipo
        self._valida(
            nome=nome or offerta_corrente.nome,
            tipo=tipo,
            sconto_percentuale=sconto_percentuale if sconto_percentuale is not None else offerta_corrente.sconto_percentuale,
            prezzo=prezzo if prezzo is not None else offerta_corrente.prezzo,
            durata_giorni=durata_giorni if durata_giorni is not None else offerta_corrente.durata_giorni,
            data_scadenza=data_scadenza if data_scadenza is not None else offerta_corrente.data_scadenza,
            tipo_mezzo=tipo_mezzo if tipo_mezzo is not None else offerta_corrente.tipo_mezzo,
            data_inizio=data_inizio if data_inizio is not None else offerta_corrente.data_inizio,
        )
        try:
            aggiornata = self._repo.aggiorna(
                offerta_id=offerta_id,
                db=db,
                nome=nome,
                descrizione=descrizione,
                sconto_percentuale=sconto_percentuale,
                prezzo=prezzo,
                durata_giorni=durata_giorni,
                data_inizio=data_inizio,
                data_scadenza=data_scadenza,
                stato=stato,
                tipo_mezzo=tipo_mezzo,
            )
        except NomeDuplicatoException:
            raise OffertaDuplicataException(f"Esiste già un'offerta con nome '{nome}'")
        self._storico.registra_modifica(
            tipo_configurazione="offerta_modificata",
            descrizione=f"Modifica offerta '{nome_precedente}'",
            valore_precedente=valore_precedente,
            valore_nuovo=self._serializza(aggiornata),
            operatore_id=operatore_id,
        )
        return aggiornata

    def elimina_offerta(self, offerta_id: uuid.UUID, db: Session, operatore_id: uuid.UUID) -> None:
        try:
            offerta = self._repo.trova_per_id(offerta_id, db)
        except OffertaNonTrovataException:
            raise OffertaValidazioneException(f"Offerta {offerta_id} non trovata")
        valore_precedente = self._serializza(offerta)
        nome = offerta.nome
        self._repo.elimina(offerta_id, db)
        self._storico.registra_modifica(
            tipo_configurazione="offerta_eliminata",
            descrizione=f"Eliminazione offerta '{nome}'",
            valore_precedente=valore_precedente,
            valore_nuovo=None,
            operatore_id=operatore_id,
        )

    def _valida(
        self,
        nome: str,
        tipo: str,
        sconto_percentuale: Optional[Decimal],
        prezzo: Optional[Decimal],
        durata_giorni: Optional[int],
        data_scadenza: Optional[datetime],
        tipo_mezzo: Optional[str] = None,
        data_inizio: Optional[datetime] = None,
    ) -> None:
        if not nome or not nome.strip():
            raise OffertaValidazioneException("Il nome è obbligatorio")
        if tipo not in ("promozione", "abbonamento"):
            raise OffertaValidazioneException("Tipo non valido: usa 'promozione' o 'abbonamento'")
        if tipo_mezzo is not None and tipo_mezzo not in ("monopattino", "bicicletta", "automobile"):
            raise OffertaValidazioneException("tipo_mezzo non valido: usa 'monopattino', 'bicicletta' o 'automobile'")
        if tipo == "promozione":
            if sconto_percentuale is None:
                raise OffertaValidazioneException("Lo sconto percentuale è obbligatorio per una promozione")
            if sconto_percentuale <= 0 or sconto_percentuale > 100:
                raise OffertaValidazioneException("Lo sconto deve essere compreso tra 1 e 100")
            if data_scadenza is None:
                raise OffertaValidazioneException("La data di scadenza è obbligatoria per una promozione")
            ds = data_scadenza if data_scadenza.tzinfo else data_scadenza.replace(tzinfo=timezone.utc)
            if ds <= datetime.now(timezone.utc):
                raise OffertaValidazioneException("La data di scadenza deve essere nel futuro")
        if tipo == "abbonamento":
            if prezzo is None:
                raise OffertaValidazioneException("Il prezzo è obbligatorio per un abbonamento")
            if prezzo <= 0:
                raise OffertaValidazioneException("Il prezzo deve essere maggiore di zero")
            if durata_giorni is None:
                raise OffertaValidazioneException("La durata in giorni è obbligatoria per un abbonamento")
            if durata_giorni <= 0:
                raise OffertaValidazioneException("La durata deve essere maggiore di zero")
        if data_inizio is not None and data_scadenza is not None:
            di = data_inizio if data_inizio.tzinfo else data_inizio.replace(tzinfo=timezone.utc)
            ds = data_scadenza if data_scadenza.tzinfo else data_scadenza.replace(tzinfo=timezone.utc)
            if ds <= di:
                raise OffertaValidazioneException("La data di scadenza deve essere successiva alla data di inizio")
```

- [ ] **Step 3: Aggiorna `offerta_controller.py` per passare `operatore_id`**

```python
import uuid
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import verify_token
from controllers.schemas import CreaOffertaRequest, ModificaOffertaRequest, OffertaOut
from bll.servizio_offerte import ServizioOfferta, OffertaValidazioneException, OffertaDuplicataException

router = APIRouter(prefix="/operatore", tags=["Operatore - Offerte"])
_servizio = ServizioOfferta()


# [IF-OP.06] — lista offerte
@router.get("/offerte", response_model=list[OffertaOut])
def lista_offerte(
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    return _servizio.lista_offerte(db)


# [IF-OP.06] — crea offerta
@router.post("/offerte", response_model=OffertaOut, status_code=201)
def crea_offerta(
    body: CreaOffertaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.crea_offerta(
            nome=body.nome,
            tipo=body.tipo,
            descrizione=body.descrizione,
            sconto_percentuale=body.sconto_percentuale,
            prezzo=body.prezzo,
            durata_giorni=body.durata_giorni,
            data_inizio=body.data_inizio,
            data_scadenza=body.data_scadenza,
            db=db,
            operatore_id=uuid.UUID(str(_op["id"])),
            tipo_mezzo=body.tipo_mezzo,
        )
    except OffertaDuplicataException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))


# [IF-OP.06] — modifica offerta
@router.patch("/offerte/{offerta_id}", response_model=OffertaOut)
def modifica_offerta(
    offerta_id: uuid.UUID,
    body: ModificaOffertaRequest,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        return _servizio.modifica_offerta(
            offerta_id=offerta_id,
            db=db,
            operatore_id=uuid.UUID(str(_op["id"])),
            nome=body.nome,
            descrizione=body.descrizione,
            sconto_percentuale=body.sconto_percentuale,
            prezzo=body.prezzo,
            durata_giorni=body.durata_giorni,
            data_inizio=body.data_inizio,
            data_scadenza=body.data_scadenza,
            stato=body.stato,
            tipo_mezzo=body.tipo_mezzo,
        )
    except OffertaDuplicataException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=422, detail=str(e))


# [IF-OP.06] — elimina offerta
@router.delete("/offerte/{offerta_id}", status_code=204)
def elimina_offerta(
    offerta_id: uuid.UUID,
    _op=Depends(verify_token(["OP"])),
    db=Depends(get_db),
):
    try:
        _servizio.elimina_offerta(offerta_id, db, operatore_id=uuid.UUID(str(_op["id"])))
    except OffertaValidazioneException as e:
        raise HTTPException(status_code=404, detail=str(e))
```

- [ ] **Step 4: Esegui i test HTTP esistenti — devono ancora passare**

```bash
cd backend && uv run pytest tests/test_offerte.py -v -m integration
```

Expected: PASS (nessuna rottura — i test passano per il controller, che ora inietta `operatore_id` internamente).

- [ ] **Step 5: Aggiungi test di integrazione in `test_storico_modifiche.py`**

Aggiungi alla classe `TestIntegrazioneServiziEsistenti`:

```python
    def test_crea_modifica_ed_elimina_offerta_registrano_modifica_nello_storico(self, db):
        from decimal import Decimal
        from datetime import datetime, timedelta, timezone
        from bll.servizio_offerte import ServizioOfferta

        operatore_id = _uuid.uuid4()
        nome = f"OffertaTest-{operatore_id.hex[:6]}"
        try:
            with Session(db) as session:
                offerta = ServizioOfferta().crea_offerta(
                    nome=nome,
                    tipo="promozione",
                    descrizione="Test",
                    sconto_percentuale=Decimal("10"),
                    prezzo=None,
                    durata_giorni=None,
                    data_inizio=None,
                    data_scadenza=datetime.now(timezone.utc) + timedelta(days=1),
                    db=session,
                    operatore_id=operatore_id,
                )
            with Session(db) as session:
                ServizioOfferta().modifica_offerta(
                    offerta_id=offerta.id,
                    db=session,
                    operatore_id=operatore_id,
                    sconto_percentuale=Decimal("20"),
                )
            with Session(db) as session:
                ServizioOfferta().elimina_offerta(offerta.id, session, operatore_id=operatore_id)
            storico = ServizioStoricoModifiche().get_storico()
            tipi_evento = [
                v["tipo_configurazione"]
                for v in storico
                if v["operatore_id"] == str(operatore_id)
            ]
            assert "offerta_creata" in tipi_evento
            assert "offerta_modificata" in tipi_evento
            assert "offerta_eliminata" in tipi_evento
        finally:
            _pulisci(db, operatore_id)
            with Session(db) as session:
                session.execute(text("DELETE FROM offerte WHERE nome = :n"), {"n": nome})
                session.commit()
```

- [ ] **Step 6: Esegui i test di integrazione**

```bash
cd backend && uv run pytest tests/test_storico_modifiche.py -v -m integration
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend/bll/servizio_offerte.py backend/controllers/offerta_controller.py backend/tests/test_storico_modifiche.py
git commit -m "feat(storico): registra creazione, modifica ed eliminazione offerte nello storico modifiche"
```

---

### Task 3: Frontend — riscrittura `VistaStoricoModifiche` con sezioni e diff leggibile

**Files:**
- Modify: `frontend/src/views/operatore/VistaStoricoModifiche.tsx`
- Modify: `frontend/src/views/operatore/VistaStoricoModifiche.css`

**Interfaces:**
- Consumes: `getStoricoModifiche(): Promise<StoricoModifica[]>` da `frontend/src/services/StoricoModificheService.ts` (interfaccia `StoricoModifica` invariata: `{ id, tipo_configurazione, descrizione, valore_precedente, valore_nuovo, operatore_id, created_at }`).
- Produces: nessuna nuova esportazione consumata da altri file — componente terminale di route.

- [ ] **Step 1: Sostituisci il contenuto di `VistaStoricoModifiche.tsx`**

```tsx
import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getStoricoModifiche, type StoricoModifica } from '../../services/StoricoModificheService'
import './VistaStoricoModifiche.css'

interface CampoConfig {
  label: string
  formatta?: (v: string) => string
  valori?: Record<string, string>
}

interface CategoriaConfig {
  label: string
  tipi: string[]
  campi: Record<string, CampoConfig>
}

const EURO = (v: string) => `${Number(v).toFixed(2)}€`
const PERCENTO = (v: string) => `${v}%`
const MINUTI = (v: string) => `${v} min`

const CATEGORIE: CategoriaConfig[] = [
  {
    label: 'Parametri di sistema',
    tipi: ['parametri_sistema'],
    campi: {
      durata_max_prenotazione_min: { label: 'Durata massima prenotazione', formatta: MINUTI },
      durata_periodo_grazia_min: { label: 'Durata periodo di grazia', formatta: MINUTI },
      max_mezzi_per_utente: { label: 'Numero massimo mezzi per utente' },
      addebito_pausa_min: { label: 'Addebito pausa al minuto', formatta: EURO },
    },
  },
  {
    label: 'Regole di fine corsa',
    tipi: ['regole_fine_corsa'],
    campi: {
      tipo_vincolo: {
        label: 'Vincolo rilascio fuori zona parcheggio',
        valori: { penale: 'Penale (addebito importo)', divieto: 'Blocco fine corsa', avviso: 'Avviso (nessun addebito)' },
      },
      penale_fuori_zona: { label: 'Importo penale', formatta: EURO },
      batteria_minima: { label: 'Batteria minima richiesta', formatta: PERCENTO },
      bonus_parcheggi_corretti: { label: 'Numero parcheggi corretti necessari' },
      bonus_valore: { label: 'Valore bonus', formatta: EURO },
    },
  },
  {
    label: 'Zone',
    tipi: ['zona_creata', 'zona_eliminata'],
    campi: {
      nome: { label: 'Nome zona' },
      tipo: {
        label: 'Tipo zona',
        valori: { operativa: 'Operativa', parcheggio: 'Parcheggio', limitata: 'Limitata', vietata: 'Vietata' },
      },
      limite_velocita: { label: 'Limite di velocità' },
    },
  },
  {
    label: 'Tariffe',
    tipi: ['tariffa_creata', 'tariffa_modificata'],
    campi: {
      tipo_mezzo: { label: 'Tipo mezzo' },
      costo_al_minuto: { label: 'Costo al minuto', formatta: EURO },
      costo_al_km: { label: 'Costo al km', formatta: EURO },
    },
  },
  {
    label: 'Offerte',
    tipi: ['offerta_creata', 'offerta_modificata', 'offerta_eliminata'],
    campi: {
      nome: { label: 'Nome offerta' },
      tipo: { label: 'Tipo', valori: { promozione: 'Promozione', abbonamento: 'Abbonamento' } },
      stato: { label: 'Stato', valori: { attiva: 'Attiva', bozza: 'Bozza', scaduta: 'Scaduta' } },
      descrizione: { label: 'Descrizione' },
      sconto_percentuale: { label: 'Sconto', formatta: PERCENTO },
      prezzo: { label: 'Prezzo', formatta: EURO },
      durata_giorni: { label: 'Durata', formatta: v => `${v} giorni` },
      data_inizio: { label: 'Data inizio' },
      data_scadenza: { label: 'Data scadenza' },
      tipo_mezzo: {
        label: 'Valido per',
        valori: { monopattino: 'Monopattino', bicicletta: 'Bicicletta', automobile: 'Automobile' },
      },
    },
  },
]

function trovaCategoria(tipo: string): CategoriaConfig | undefined {
  return CATEGORIE.find(c => c.tipi.includes(tipo))
}

// "a=1, b=2, c=None" -> { a: "1", b: "2", c: "None" }
// split solo prima di un token "parola=" per non rompersi su virgole nei valori liberi (es. descrizione)
function parseValori(s: string | null): Record<string, string> {
  if (!s) return {}
  const risultato: Record<string, string> = {}
  for (const coppia of s.split(/,\s*(?=[a-zA-Z_][a-zA-Z0-9_]*=)/)) {
    const idx = coppia.indexOf('=')
    if (idx === -1) continue
    risultato[coppia.slice(0, idx).trim()] = coppia.slice(idx + 1).trim()
  }
  return risultato
}

interface RigaDiff {
  campo: string
  prima?: string
  dopo?: string
}

function calcolaDiff(precedente: string | null, nuovo: string | null): RigaDiff[] {
  const prec = parseValori(precedente)
  const dopo = parseValori(nuovo)
  const righe: RigaDiff[] = []
  if (precedente && nuovo) {
    for (const campo of Object.keys(dopo)) {
      if (prec[campo] !== dopo[campo]) {
        righe.push({ campo, prima: prec[campo], dopo: dopo[campo] })
      }
    }
  } else if (nuovo) {
    for (const campo of Object.keys(dopo)) {
      if (dopo[campo] !== 'None') righe.push({ campo, dopo: dopo[campo] })
    }
  } else if (precedente) {
    for (const campo of Object.keys(prec)) {
      if (prec[campo] !== 'None') righe.push({ campo, prima: prec[campo] })
    }
  }
  return righe
}

function formattaValore(categoria: CategoriaConfig | undefined, campo: string, valore: string): string {
  const config = categoria?.campi[campo]
  if (!config) return valore
  if (config.valori) return config.valori[valore] ?? valore
  if (config.formatta) return config.formatta(valore)
  return valore
}

function etichettaCampo(categoria: CategoriaConfig | undefined, campo: string): string {
  return categoria?.campi[campo]?.label ?? campo
}

function formatData(iso: string) {
  return new Date(iso).toLocaleString('it-IT', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

// [IF-OP.13] Mostra Storico Modifiche
export default function VistaStoricoModifiche() {
  const navigate = useNavigate()
  const [storico, setStorico] = useState<StoricoModifica[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')
  const [categoriaAperta, setCategoriaAperta] = useState<string | null>(null)

  const caricaStorico = useCallback(async () => {
    try {
      const modifiche = await getStoricoModifiche()
      setStorico(modifiche)
    } catch {
      setErrore('Impossibile caricare lo storico delle modifiche.')
    } finally {
      setCaricamento(false)
    }
  }, [])

  useEffect(() => { caricaStorico() }, [caricaStorico])

  const sezioni = CATEGORIE
    .map(categoria => ({
      categoria,
      voci: storico.filter(v => categoria.tipi.includes(v.tipo_configurazione)),
    }))
    .filter(s => s.voci.length > 0)

  return (
    <div className="vista-storico-mod-wrap">
      <button type="button" className="btn-back-storico-mod" onClick={() => navigate(-1)}>
        ← Torna alla mappa
      </button>

      <h1 className="storico-mod-titolo">Storico Modifiche</h1>

      {errore && <p className="storico-mod-errore">{errore}</p>}

      {caricamento ? (
        <p className="storico-mod-vuoto">Caricamento...</p>
      ) : sezioni.length === 0 ? (
        <p className="storico-mod-vuoto">Nessuna modifica registrata.</p>
      ) : (
        <div className="storico-mod-sezioni">
          {sezioni.map(({ categoria, voci }) => {
            const aperta = categoriaAperta === categoria.label
            return (
              <div key={categoria.label} className="storico-mod-sezione">
                <button
                  type="button"
                  className="storico-mod-sezione-header"
                  onClick={() => setCategoriaAperta(aperta ? null : categoria.label)}
                >
                  <span className="storico-mod-sezione-titolo">
                    {categoria.label}
                    <span className="storico-mod-sezione-badge">{voci.length}</span>
                  </span>
                  <span className={`storico-mod-chevron ${aperta ? 'aperta' : ''}`}>▾</span>
                </button>
                {aperta && (
                  <div className="storico-mod-lista">
                    {voci.map(v => (
                      <div key={v.id} className="storico-mod-card">
                        <div className="storico-mod-card-header">
                          <span className="storico-mod-data">{formatData(v.created_at)}</span>
                        </div>
                        <p className="storico-mod-descrizione">{v.descrizione}</p>
                        <div className="storico-mod-valori">
                          {calcolaDiff(v.valore_precedente, v.valore_nuovo).map(riga => (
                            <div key={riga.campo} className="storico-mod-riga-diff">
                              <span className="storico-mod-riga-etichetta">{etichettaCampo(categoria, riga.campo)}:</span>
                              {riga.prima !== undefined && (
                                <span className="storico-mod-valore-precedente">
                                  {formattaValore(categoria, riga.campo, riga.prima)}
                                </span>
                              )}
                              {riga.prima !== undefined && riga.dopo !== undefined && (
                                <span className="storico-mod-freccia">→</span>
                              )}
                              {riga.dopo !== undefined && (
                                <span className="storico-mod-valore-nuovo">
                                  {formattaValore(categoria, riga.campo, riga.dopo)}
                                </span>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Aggiorna `VistaStoricoModifiche.css`**

Sostituisci il contenuto con (mantiene le classi base, aggiunge quelle per accordion e diff):

```css
.vista-storico-mod-wrap {
  min-height: 100vh;
  background: #f5f6fa;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 24px 20px 48px;
}

.btn-back-storico-mod {
  background: none;
  border: none;
  color: #4caf9a;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-bottom: 20px;
}

.storico-mod-titolo {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 16px;
}

.storico-mod-errore {
  color: #e53935;
  font-size: 13px;
  margin: 0 0 12px;
}

.storico-mod-vuoto {
  color: #888;
  font-size: 14px;
}

.storico-mod-sezioni {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 720px;
}

.storico-mod-sezione {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.storico-mod-sezione-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 14px 16px;
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
}

.storico-mod-sezione-titolo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.storico-mod-sezione-badge {
  background: #eef2f1;
  color: #4caf9a;
  font-size: 12px;
  font-weight: 700;
  border-radius: 999px;
  padding: 2px 8px;
}

.storico-mod-chevron {
  color: #888;
  transition: transform 0.15s ease;
}

.storico-mod-chevron.aperta {
  transform: rotate(180deg);
}

.storico-mod-lista {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 16px 16px;
}

.storico-mod-card {
  background: #fafbfc;
  border: 1px solid #ececec;
  border-radius: 8px;
  padding: 12px 14px;
}

.storico-mod-card-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 6px;
}

.storico-mod-data {
  font-size: 12px;
  color: #888;
}

.storico-mod-descrizione {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px;
}

.storico-mod-valori {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: #444;
}

.storico-mod-riga-diff {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.storico-mod-riga-etichetta {
  color: #666;
  font-weight: 500;
}

.storico-mod-valore-precedente {
  color: #c62828;
}

.storico-mod-valore-nuovo {
  color: #2e7d32;
  font-weight: 600;
}

.storico-mod-freccia {
  color: #999;
}
```

- [ ] **Step 3: Avvia il frontend e verifica manualmente nel browser**

```bash
cd frontend && npm run dev
```

Apri `http://localhost:5173`, accedi come operatore, vai su "Storico Modifiche". Verifica:
- Le sezioni con voci sono visibili con il contatore corretto.
- Cliccando una sezione si espande e le altre eventualmente aperte si chiudono.
- Le voci mostrano solo i campi cambiati con etichetta, unità e freccia prima→dopo.
- Una modifica ai parametri di sistema, alle regole di fine corsa, a una zona, a una tariffa, a un'offerta (creale/modificale dalle rispettive viste operatore) compare nella sezione corretta.

- [ ] **Step 4: Esegui la build per verificare assenza di errori TypeScript**

```bash
cd frontend && npm run build
```

Expected: build completata senza errori.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/operatore/VistaStoricoModifiche.tsx frontend/src/views/operatore/VistaStoricoModifiche.css
git commit -m "feat(storico): riorganizza lo storico modifiche in sezioni per categoria con diff leggibile"
```

---

## Aggiornamento documentazione (Definition of Done)

- [ ] **Aggiorna `docs/Sprintn3.md`** aggiungendo una nota nella sezione del caso d'uso IF-OP.13 che descrive: registrazione storico estesa a tariffe e offerte; UI riorganizzata in sezioni per categoria con diff sui soli campi cambiati.

```bash
git add docs/Sprintn3.md
git commit -m "docs: aggiorna IF-OP.13 con sezioni storico modifiche e logging tariffe/offerte"
```
