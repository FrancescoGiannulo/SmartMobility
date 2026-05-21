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
