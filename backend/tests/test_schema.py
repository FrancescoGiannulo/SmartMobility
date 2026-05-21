def test_utente_tablename():
    from model.utente import Utente
    assert Utente.__tablename__ == "utenti"


def test_utente_columns():
    from model.utente import Utente
    cols = {c.name for c in Utente.__table__.columns}
    assert cols == {"id", "nome", "cognome", "telefono", "sospeso", "created_at"}


def test_operatore_tablename():
    from model.utente import Operatore
    assert Operatore.__tablename__ == "operatori"


def test_operatore_columns():
    from model.utente import Operatore
    cols = {c.name for c in Operatore.__table__.columns}
    assert cols == {
        "id", "nome",
        "durata_max_prenotazione_min",
        "durata_periodo_grazia_min",
        "max_mezzi_per_utente",
        "created_at",
    }


def test_amministratore_tablename():
    from model.utente import AmministrazionePubblica
    assert AmministrazionePubblica.__tablename__ == "amministratori"


def test_amministratore_columns():
    from model.utente import AmministrazionePubblica
    cols = {c.name for c in AmministrazionePubblica.__table__.columns}
    assert cols == {"id", "nome", "created_at"}


def test_tipo_mezzo_values():
    from model.mezzo import TipoMezzo
    assert set(TipoMezzo) == {
        TipoMezzo.monopattino,
        TipoMezzo.bicicletta,
        TipoMezzo.automobile,
    }


def test_stato_mezzo_values():
    from model.mezzo import StatoMezzo
    assert set(e.value for e in StatoMezzo) == {
        "Disponibile", "Prenotato", "In uso", "In pausa",
        "In manutenzione", "Fuori servizio", "Dismesso",
    }


def test_mezzo_columns():
    from model.mezzo import Mezzo
    cols = {c.name for c in Mezzo.__table__.columns}
    assert cols == {"id", "codice", "tipo", "stato", "lat", "lng", "batteria", "created_at"}


def test_tipo_zona_values():
    from model.zona import TipoZona
    assert set(e.value for e in TipoZona) == {"operativa", "parcheggio", "limitata", "vietata"}


def test_zona_columns():
    from model.zona import Zona
    cols = {c.name for c in Zona.__table__.columns}
    assert cols == {"id", "nome", "tipo", "perimetro", "limite_velocita", "attiva", "created_at"}


def test_zona_perimetro_is_geometry():
    from model.zona import Zona
    from geoalchemy2 import Geometry
    col = Zona.__table__.columns["perimetro"]
    assert isinstance(col.type, Geometry)
    assert col.type.geometry_type == "POLYGON"
    assert col.type.srid == 4326


def test_prenotazione_columns():
    from model.prenotazione import Prenotazione
    cols = {c.name for c in Prenotazione.__table__.columns}
    assert cols == {"id", "utente_id", "mezzo_id", "stato", "scade_at", "created_at"}


def test_stato_prenotazione_values():
    from model.prenotazione import StatoPrenotazione
    assert set(e.value for e in StatoPrenotazione) == {
        "attiva", "scaduta", "annullata", "convertita"
    }


def test_corsa_columns():
    from model.corsa import Corsa
    cols = {c.name for c in Corsa.__table__.columns}
    assert cols == {
        "id", "utente_id", "mezzo_id", "prenotazione_id",
        "stato", "inizio_at", "fine_at", "distanza_km",
        "inizio_lat", "inizio_lng", "fine_lat", "fine_lng", "created_at",
    }


def test_corsa_prenotazione_id_is_nullable():
    from model.corsa import Corsa
    col = Corsa.__table__.columns["prenotazione_id"]
    assert col.nullable is True


def test_stato_corsa_values():
    from model.corsa import StatoCorsa
    assert set(e.value for e in StatoCorsa) == {"in_uso", "in_pausa", "terminata"}


def test_metodo_pagamento_columns():
    from model.pagamento import MetodoPagamento
    cols = {c.name for c in MetodoPagamento.__table__.columns}
    assert cols == {
        "id", "utente_id", "tipo", "token_esterno", "last_four", "predefinito", "created_at"
    }


def test_pagamento_columns():
    from model.pagamento import Pagamento
    cols = {c.name for c in Pagamento.__table__.columns}
    assert cols == {
        "id", "corsa_id", "utente_id", "metodo_pagamento_id", "importo", "stato", "created_at"
    }


def test_pagamento_metodo_id_is_nullable():
    from model.pagamento import Pagamento
    col = Pagamento.__table__.columns["metodo_pagamento_id"]
    assert col.nullable is True


def test_tipo_metodo_pagamento_values():
    from model.pagamento import TipoMetodoPagamento
    assert set(e.value for e in TipoMetodoPagamento) == {
        "google_pay", "apple_pay", "paypal", "carta"
    }


def test_stato_pagamento_values():
    from model.pagamento import StatoPagamento
    assert set(e.value for e in StatoPagamento) == {
        "completato", "rifiutato", "in_attesa"
    }


def test_tariffa_columns():
    from model.tariffa import Tariffa
    cols = {c.name for c in Tariffa.__table__.columns}
    assert cols == {
        "id", "tipo_mezzo", "costo_al_minuto", "costo_al_km", "created_at", "aggiornata_at"
    }


def test_tariffa_tipo_mezzo_unique():
    from model.tariffa import Tariffa
    col = Tariffa.__table__.columns["tipo_mezzo"]
    assert col.unique is True


def test_regola_fine_corsa_columns():
    from model.regola_fine_corsa import RegolaFinecorsa
    cols = {c.name for c in RegolaFinecorsa.__table__.columns}
    assert cols == {
        "id", "zona_parcheggio_id", "batteria_minima",
        "penale_fuori_zona", "tipo_vincolo", "created_at",
    }
