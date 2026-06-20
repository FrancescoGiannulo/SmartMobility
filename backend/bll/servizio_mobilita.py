import uuid as _uuid
from math import radians, cos, sin, asin, sqrt
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from dal.mezzo_repository import MezzoRepository
from dal.corsa_repository import CorsaRepository
from dal.prenotazione_repository import PrenotazioneRepository
from dal.zona_repository import ZonaRepository
from dal.regola_fine_corsa_repository import RegoleFineCorsaRawRepository
from dal.operatore_repository import OperatoreRepository
from dal.parametri_sistema_repository import ParametriSistemaRepository
from dal.segnalazione_repository import SegnalazioneRepository
from model.segnalazione import StatoSegnalazione
from bll.servizio_gis import ServizioGIS


class MezzoNonTrovatoException(Exception):
    pass


class MezzoNonDisponibileException(Exception):
    pass


class MezzoTroppoLontanoException(Exception):
    pass


class CorsaNonTrovataException(Exception):
    pass



class CorsaNonInUsaException(Exception):
    pass


class CorsaNonInPausaException(Exception):
    pass


class IdentificativoEsistenteException(Exception):
    pass


class PosizioneNonOperativaException(Exception):
    pass


class MezzoInMissioneException(Exception):
    pass


class SegnalazioneNonTrovata(Exception):
    pass


# [IF-UT.04] CS-05 — raggio massimo (km) entro cui l'utente può sbloccare un mezzo
RAGGIO_SBLOCCO_KM = 0.5


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return R * 2 * asin(sqrt(a))


class ServizioMobilita:

    def __init__(self, db: Session) -> None:
        self._db = db
        self._mezzo_repo = MezzoRepository(db)
        self._corsa_repo = CorsaRepository(db)
        self._pren_repo = PrenotazioneRepository(db)
        self._zona_repo = ZonaRepository(db)
        self._regola_repo = RegoleFineCorsaRawRepository(db)
        self._op_repo = OperatoreRepository(db)
        self._parametri_repo = ParametriSistemaRepository()
        self._segnalazione_repo = SegnalazioneRepository()

    # [IF-UT.04] CS-05 — lista mezzi sbloccabili (msg4 diagramma di sequenza)
    def get_mezzi_sbloccabili(
        self,
        utente_id: UUID,
        lat: float | None = None,
        lng: float | None = None,
    ) -> list[dict]:
        return self._mezzo_repo.trova_sbloccabili(utente_id, lat, lng)

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
                corsa = self._sblocca_singolo(mezzo_id, utente_id, gruppo_id, lat, lng)
                sbloccati.append({"mezzo_id": str(mezzo_id), "corsa_id": corsa["id"], "gruppo_corsa_id": str(gruppo_id) if gruppo_id else None})
            except Exception:
                # [CS-05.01] mezzo non sbloccabile — segnaFallito
                falliti.append(str(mezzo_id))
        return {"sbloccati": sbloccati, "falliti": falliti}

    def _sblocca_singolo(
        self,
        mezzo_id: UUID,
        utente_id: UUID,
        gruppo_corsa_id: _uuid.UUID | None = None,
        lat: float | None = None,
        lng: float | None = None,
    ) -> dict:
        mezzo = self._mezzo_repo.trova_per_id(mezzo_id)
        if mezzo is None:
            raise MezzoNonTrovatoException(f"Mezzo {mezzo_id} non trovato")
        # [IF-UT.04] CS-05 — verifica prossimità: l'utente deve essere entro RAGGIO_SBLOCCO_KM
        # dal mezzo (vale anche per i mezzi prenotati, non solo i disponibili)
        if lat is not None and lng is not None and mezzo.get("lat") is not None and mezzo.get("lng") is not None:
            if _haversine_km(lat, lng, mezzo["lat"], mezzo["lng"]) > RAGGIO_SBLOCCO_KM:
                raise MezzoTroppoLontanoException(f"Mezzo {mezzo_id} troppo lontano")
        stato = mezzo["stato"]
        prenotazione_id = None
        if stato == "Disponibile":
            pass
        elif stato == "Prenotato":
            pren = self._pren_repo.trova_attiva_per_utente_e_mezzo(utente_id, mezzo_id)
            if pren is None:
                # Nessuna prenotazione attiva per questo utente: verifico se esiste per
                # qualsiasi utente per distinguere "prenotato da altri" da "prenotazione scaduta"
                any_active = self._pren_repo.trova_qualsiasi_attiva_per_mezzo(mezzo_id)
                if any_active is not None:
                    raise MezzoNonDisponibileException("Mezzo prenotato da un altro utente")
                # Tutte le prenotazioni sono scadute: reset a Disponibile e procedi
                self._mezzo_repo.aggiorna_stato(mezzo_id, "Disponibile")
            else:
                prenotazione_id = pren["id"]
        else:
            raise MezzoNonDisponibileException(f"Mezzo non disponibile (stato: {stato})")
        corsa = self._corsa_repo.crea(utente_id, mezzo_id, prenotazione_id, gruppo_corsa_id)
        if prenotazione_id:
            self._pren_repo.aggiorna_stato(UUID(prenotazione_id), "convertita")
        self._mezzo_repo.aggiorna_stato(mezzo_id, "In uso")
        return corsa

    # [IF-OP.13] — Ottieni zone parcheggio e configurazione attuale
    def get_zona_parcheggio_e_regole(self, operatore_id: UUID) -> dict:
        zone = [z for z in self._zona_repo.lista_zone() if z["tipo"] == "parcheggio"]
        regole = self._regola_repo.trova_tutte()
        # [CS-15] Usa ParametriSistema come fonte autoritativa per i parametri globali
        p = self._parametri_repo.get(self._db)
        impostazioni = {
            "durata_max_prenotazione_min": p.durata_max_prenotazione_min,
            "durata_periodo_grazia_min": p.durata_periodo_grazia_min,
            "max_mezzi_per_utente": p.max_mezzi_per_utente,
        }
        # ricava params globali dalla prima regola esistente (se presente)
        tipo_vincolo = regole[0]["tipo_vincolo"] if regole else "avviso"
        batteria_minima = regole[0]["batteria_minima"] if regole else None
        penale_fuori_zona = regole[0]["penale_fuori_zona"] if regole else 0.0
        return {
            **impostazioni,
            "tipo_vincolo": tipo_vincolo,
            "batteria_minima": batteria_minima,
            "penale_fuori_zona": penale_fuori_zona,
            "zone_parcheggio": [{"id": str(z["id"]), "nome": z["nome"]} for z in zone],
        }

    # [IF-OP.13] — Salva regole fine corsa (params globali su tutte le zone parcheggio)
    def salva_regole_fine_corsa(
        self,
        operatore_id: UUID,
        durata_max_prenotazione_min: int,
        durata_periodo_grazia_min: int,
        max_mezzi_per_utente: int,
        tipo_vincolo: str,
        batteria_minima: int | None,
        penale_fuori_zona: float,
    ) -> None:
        self._op_repo.aggiorna_impostazioni(
            operatore_id,
            durata_max_prenotazione_min,
            durata_periodo_grazia_min,
            max_mezzi_per_utente,
        )
        zone_parcheggio = [z for z in self._zona_repo.lista_zone() if z["tipo"] == "parcheggio"]
        self._regola_repo.elimina_tutto()
        for zona in zone_parcheggio:
            self._regola_repo.crea(
                UUID(str(zona["id"])),
                batteria_minima,
                penale_fuori_zona,
                tipo_vincolo,
            )

    # [IF-UT.14] UT-11 — Storico corse dell'utente
    def get_storico(self, utente_id: UUID) -> list[dict]:
        return self._corsa_repo.find_by_utente_order_by_data(utente_id)

    # [IF-UT.07] UT-08 — Riepilogo corsa terminata (restituisce Corsa come da diagramma)
    def calcolaRiepilogoSessione(self, corsa_id: UUID, utente_id: UUID) -> dict:
        row = self._corsa_repo.trova_riepilogo(corsa_id, utente_id)
        if row is None:
            raise CorsaNonTrovataException(f"Corsa {corsa_id} non trovata")
        return row

    # [IF-UT.06] CS-11 — Termina Corsa (minimale: aggiorna stati)
    def termina_corsa(self, corsa_id: UUID, utente_id: UUID) -> None:
        corsa = self._corsa_repo.trova_per_id(corsa_id)
        if corsa is None:
            raise CorsaNonTrovataException(f"Corsa {corsa_id} non trovata")
        # Finalizza eventuale pausa attiva prima di terminare
        self._corsa_repo.finalizza_pausa(corsa_id)
        self._corsa_repo.aggiorna_stato(corsa_id, "terminata")
        self._mezzo_repo.aggiorna_stato(UUID(corsa["mezzo_id"]), "Disponibile")

    # [IF-UT.15] Le mie segnalazioni
    def get_mie_segnalazioni(self, utente_id: UUID) -> list[dict]:
        return [
            {
                "id": str(s.id),
                "tipologia": s.tipologia,
                "descrizione": s.descrizione,
                "stato": s.stato,
                "created_at": s.created_at.isoformat(),
            }
            for s in self._segnalazione_repo.find_by_utente(utente_id)
        ]

    # [IF-UT.15] Invia Segnalazione
    def registra_segnalazione(self, utente_id: UUID, tipologia: str, descrizione: str) -> dict:
        segnalazione = self._segnalazione_repo.crea(utente_id, tipologia, descrizione)
        return {
            "id": str(segnalazione.id),
            "tipologia": segnalazione.tipologia,
            "descrizione": segnalazione.descrizione,
            "stato": segnalazione.stato,
            "created_at": segnalazione.created_at.isoformat(),
        }

    # [IF-OP.08] Gestisce Segnalazione — lista
    def get_segnalazioni(self) -> list[dict]:
        return [
            {
                "id": str(s["id"]),
                "utente_id": str(s["utente_id"]),
                "tipologia": s["tipologia"],
                "descrizione": s["descrizione"],
                "stato": s["stato"],
                "created_at": s["created_at"].isoformat(),
                "nome_utente": s["nome_utente"],
            }
            for s in self._segnalazione_repo.find_all()
        ]

    # [IF-OP.08] Gestisce Segnalazione — dettaglio
    def get_dettaglio_segnalazione(self, segnalazione_id: UUID) -> dict:
        s = self._segnalazione_repo.find_by_id(segnalazione_id)
        if not s:
            raise SegnalazioneNonTrovata(f"Segnalazione {segnalazione_id} non trovata")
        return {
            "id": str(s["id"]),
            "utente_id": str(s["utente_id"]),
            "tipologia": s["tipologia"],
            "descrizione": s["descrizione"],
            "stato": s["stato"],
            "created_at": s["created_at"].isoformat(),
            "nome_utente": s["nome_utente"],
        }

    # [IF-OP.08] Gestisce Segnalazione — presa in carico
    def prendi_in_carico(self, segnalazione_id: UUID) -> dict:
        aggiornato = self._segnalazione_repo.aggiorna_stato(
            segnalazione_id, StatoSegnalazione.in_carico
        )
        if not aggiornato:
            raise SegnalazioneNonTrovata(f"Segnalazione {segnalazione_id} non trovata")
        return self.get_dettaglio_segnalazione(segnalazione_id)

    # [IF-UT.10] SD SospendeCorsa — msg4: sospendiCorsa(idCorsa)
    def sospendiCorsa(self, corsa_id: UUID, utente_id: UUID) -> dict:
        corsa = self._corsa_repo.trova_per_id(corsa_id)
        if corsa is None:
            raise CorsaNonTrovataException(f"Corsa {corsa_id} non trovata")
        if corsa["stato"] != "in_uso":
            raise CorsaNonInUsaException("La corsa non è in stato in_uso")
        # msg5: bloccaMezzo() → msg6: save(this)
        self._mezzo_repo.bloccaMezzo(UUID(corsa["mezzo_id"]))
        # msg9: registraInizioPausa(timestamp) → msg10: save(this)
        self._corsa_repo.registraInizioPausa(corsa_id)
        # Calcola tempoGratuitoResiduo e politicaAddebito (msg16)
        parametri = self._parametri_repo.get(self._db)
        grazia_sec = parametri.durata_periodo_grazia_min * 60
        pausa_accumulata = corsa["pausa_durata_accumulata_sec"]
        tempo_gratuito_residuo_sec = max(0, grazia_sec - pausa_accumulata)
        # opt [periodo di grazia scaduto]: A1 rilevaPausaScaduta() — A2 applicaAddebitoPausa()
        periodo_grazia_scaduto = self._rilevaPausaScaduta(pausa_accumulata, grazia_sec)
        if periodo_grazia_scaduto:
            self._corsa_repo.applicaAddebitoPausa(corsa_id)
        return {
            "stato": "in_pausa",
            "tempo_gratuito_residuo_sec": tempo_gratuito_residuo_sec,
            "addebito_pausa_min": float(parametri.addebito_pausa_min),
            "periodo_grazia_scaduto": periodo_grazia_scaduto,
        }

    # A1: rilevaPausaScaduta() — self-call ServizioMobilità
    def _rilevaPausaScaduta(self, pausa_accumulata_sec: int, grazia_sec: int) -> bool:
        return pausa_accumulata_sec >= grazia_sec

    # [IF-UT.05] — Riprende la corsa dalla pausa
    def riprendi_corsa(self, corsa_id: UUID, utente_id: UUID) -> None:
        corsa = self._corsa_repo.trova_per_id(corsa_id)
        if corsa is None:
            raise CorsaNonTrovataException(f"Corsa {corsa_id} non trovata")
        if corsa["stato"] != "in_pausa":
            raise CorsaNonInPausaException("La corsa non è in stato in_pausa")
        self._corsa_repo.riprendi(corsa_id)
        self._mezzo_repo.aggiorna_stato(UUID(corsa["mezzo_id"]), "In uso")

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
