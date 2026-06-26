from pydantic import BaseModel, EmailStr, model_validator
from typing import Any, Literal
from uuid import UUID
from decimal import Decimal


class RegistrazioneRequest(BaseModel):
    email: EmailStr
    password: str
    nome: str
    cognome: str
    consenso_privacy: bool = False  # [IIN-2 / GDPR art. 7] obbligatorio per la registrazione


class LoginRequest(BaseModel):
    email: str
    password: str


class PosizioneDemoRequest(BaseModel):
    lat: float
    lng: float
    batteria: int | None = None  # batteria che cala col movimento (demo)


class AuthResponse(BaseModel):
    access_token: str
    ruolo: str
    profilo: dict


class AggiungiMetodoRequest(BaseModel):
    tipo: str
    dati: dict[str, Any] | None = None


class EffettuaPagamentoRequest(BaseModel):
    corsa_id: str
    tipo_mezzo: str
    durata_min: float
    distanza_km: float
    offerta_id: str | None = None
    penale_fuori_zona: bool = False  # [IF-OP.06 / UT-04] corsa transitata in zona vietata/fuori operativa


class MetodoPagamentoResponse(BaseModel):
    id: str
    tipo: str
    last_four: str | None
    predefinito: bool


class MezzoMappaOut(BaseModel):
    id: UUID
    codice: str
    tipo: str
    stato: str
    lat: float
    lng: float
    batteria: int | None


class ZonaOut(BaseModel):
    id: UUID
    nome: str
    tipo: str
    perimetro: dict[str, Any]
    limite_velocita: int | None
    attiva: bool


class ZonaCreate(BaseModel):
    nome: str
    tipo: str
    coordinate: list[list[float]]
    limite_velocita: int | None = None


class CreaTariffaRequest(BaseModel):
    tipo_mezzo: str
    costo_al_minuto: float | None = None
    costo_al_km: float | None = None

    @model_validator(mode="after")
    def valida_xor_costo(self) -> "CreaTariffaRequest":
        minuto, km = self.costo_al_minuto, self.costo_al_km
        if (minuto is None) == (km is None):
            raise ValueError(
                "Specificare esattamente uno tra costo_al_minuto e costo_al_km"
            )
        valore = minuto if minuto is not None else km
        if valore is None or valore <= 0:
            raise ValueError("Il costo deve essere un numero maggiore di zero")
        return self


class TariffaResponse(BaseModel):
    id: str
    tipo_mezzo: str
    costo_al_minuto: float | None
    costo_al_km: float | None


class PrenotazioneRequest(BaseModel):
    mezzo_ids: list[UUID]


# [IF-UT.12] Invia Segnalazione / [IF-OP.08] Gestisce Segnalazione
class InviaSegnalazioneRequest(BaseModel):
    tipologia: str
    descrizione: str


class SegnalazioneOut(BaseModel):
    id: str
    utente_id: str | None = None
    tipologia: str
    descrizione: str
    stato: str
    created_at: str
    nome_utente: str | None = None


# [IF-UT.15] Scrive Recensione
class ScriviRecensioneRequest(BaseModel):
    voto: int
    commento: str | None = None


class RecensioneOut(BaseModel):
    id: str
    voto: int
    commento: str | None = None
    created_at: str


# [IF-OP.12] Visualizza Recensioni — serializza l'Object {recensioni, votoMedio}
class RecensioniOperatoreOut(BaseModel):
    recensioni: list[RecensioneOut]
    voto_medio: float


# [IF-OP.13] Mostra Storico Modifiche
class StoricoModificaOut(BaseModel):
    id: str
    tipo_configurazione: str
    descrizione: str
    valore_precedente: str | None = None
    valore_nuovo: str | None = None
    operatore_id: str
    created_at: str
    operatore_nome: str | None = None


class SbloccoRequest(BaseModel):
    mezzo_ids: list[UUID]
    lat: float | None = None
    lng: float | None = None


class MezzoSbloccabileOut(MezzoMappaOut):
    prenotato: bool
    prenotazione_id: str | None


class RisultatoSbloccoItem(BaseModel):
    mezzo_id: str
    corsa_id: str
    gruppo_corsa_id: str | None = None


class RisultatoSblocco(BaseModel):
    sbloccati: list[RisultatoSbloccoItem]
    falliti: list[str]


from datetime import datetime
from decimal import Decimal


class ConfigurazioneFineCorsaRequest(BaseModel):
    durata_max_prenotazione_min: int
    durata_periodo_grazia_min: int
    max_mezzi_per_utente: int
    tipo_vincolo: str
    batteria_minima: int | None = None
    penale_fuori_zona: float = 0.0


class CreaOffertaRequest(BaseModel):
    nome: str
    tipo: str  # 'promozione' | 'abbonamento'
    descrizione: str | None = None
    sconto_percentuale: Decimal | None = None
    prezzo: Decimal | None = None
    durata_giorni: int | None = None
    data_inizio: datetime | None = None
    data_scadenza: datetime | None = None
    tipo_mezzo: str | None = None  # None = valido per tutti; 'monopattino'|'bicicletta'|'automobile'


class ModificaOffertaRequest(BaseModel):
    nome: str | None = None
    descrizione: str | None = None
    sconto_percentuale: Decimal | None = None
    prezzo: Decimal | None = None
    durata_giorni: int | None = None
    data_inizio: datetime | None = None
    data_scadenza: datetime | None = None
    stato: str | None = None
    tipo_mezzo: str | None = None


class OffertaOut(BaseModel):
    id: UUID
    nome: str
    tipo: str
    stato: str
    descrizione: str | None
    sconto_percentuale: Decimal | None
    prezzo: Decimal | None
    durata_giorni: int | None
    data_inizio: datetime | None
    data_scadenza: datetime | None
    tipo_mezzo: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class RegolaFinecorsaRequest(BaseModel):
    tipo_vincolo: str  # 'penale' | 'divieto' | 'avviso'
    penale_fuori_zona: Decimal = Decimal("0.00")
    batteria_minima: int | None = None
    bonus_parcheggi_corretti: int | None = None
    bonus_valore: Decimal | None = None


class RegolaFinecorsaOut(BaseModel):
    id: UUID
    tipo_vincolo: str
    penale_fuori_zona: Decimal
    batteria_minima: int | None
    bonus_parcheggi_corretti: int | None
    bonus_valore: Decimal | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TariffaOut(BaseModel):
    id: UUID
    tipo_mezzo: str
    costo_al_minuto: str | None
    costo_al_km: str | None


class PromozioneOut(BaseModel):
    id: UUID
    titolo: str
    descrizione: str | None
    sconto_percentuale: str
    data_fine: str


class AggiungiMezzoRequest(BaseModel):
    tipo: str       # "monopattino" | "bicicletta" | "automobile"
    codice: str
    lat: float
    lng: float
    stato: Literal["Disponibile", "In manutenzione", "Fuori servizio"] = "Disponibile"


# [IF-OP.04] Modifica Stato Mezzo
class ModificaStatoMezzoRequest(BaseModel):
    stato: Literal["Disponibile", "In manutenzione", "Fuori servizio"]


class MezzoFlottaOut(BaseModel):
    id: UUID
    codice: str
    tipo: str
    stato: str
    lat: float | None
    lng: float | None
    batteria: int | None


# [IF-UT.16] Abbonamento Utente
class AbbonamentoOut(BaseModel):
    id: UUID
    utente_id: UUID
    offerta_id: UUID
    data_inizio: datetime
    data_fine: datetime
    stato: str
    created_at: datetime

    model_config = {"from_attributes": True}


# [IF-UT.07/IF-UT.14] Corsa (classe del diagramma delle classi)
class Corsa(BaseModel):
    id: UUID
    inizio_at: datetime
    fine_at: datetime | None = None
    costo_totale: float | None = None    # costoTotale nel diagramma, da JOIN pagamenti
    stato: str | None = None
    distanza_km: float | None = None     # distanzaPercorsa nel diagramma
    gruppo_corsa_id: UUID | None = None  # gruppoCorsaID nel diagramma
    importo_pieno: float | None = None   # da pagamenti, per badge abbonamento/promo
    # Campi aggiuntivi per lo storico (join con Mezzo)
    tipo_mezzo: str | None = None
    codice_mezzo: str | None = None
    durata_min: float | None = None
    nome_offerta_applicata: str | None = None


# [CS-15] Parametri Numerici di Sistema
class ParametriSistemaRequest(BaseModel):
    durata_max_prenotazione_min: int
    durata_periodo_grazia_min: int
    max_mezzi_per_utente: int
    addebito_pausa_min: Decimal = Decimal("0.0000")


class ParametriSistemaOut(BaseModel):
    durata_max_prenotazione_min: int
    durata_periodo_grazia_min: int
    max_mezzi_per_utente: int
    addebito_pausa_min: Decimal

    model_config = {"from_attributes": True}


# [IF-UT.14] Suggerimenti Intelligenti
class SuggerimentoOut(BaseModel):
    id: str
    tipo: str
    testo: str
    dati_contesto: dict = {}
    stato: str
    creato_at: str | None = None


# [IF-OP.09] Sospende Account Utente
class UtenteListItemOut(BaseModel):
    id: str
    nome: str
    cognome: str
    email: str
    sospeso: bool
    sospensione_fine: str | None = None


class UtenteDettaglioOut(UtenteListItemOut):
    pass


class SospensioneRequest(BaseModel):
    motivazione: str
    durata_giorni: int


class ModificaProfiloRequest(BaseModel):
    nome: str
    cognome: str


# [IF-AP.01] Accede Report — statistiche aggregate per l'Amministrazione Pubblica
class DatoSettimanaleOut(BaseModel):
    giorno: str
    monopattino: int
    bicicletta: int
    automobile: int


class DatoTortaOut(BaseModel):
    name: str
    value: float
    colore: str


class ReportOut(BaseModel):
    corse_totali: int
    durata_media_h: float
    distanza_totale_km: float
    dati_settimanali: list[DatoSettimanaleOut]
    dati_torta: list[DatoTortaOut]
