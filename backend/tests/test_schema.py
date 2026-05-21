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
    assert len(list(StatoMezzo)) == 7


def test_mezzo_columns():
    from model.mezzo import Mezzo
    cols = {c.name for c in Mezzo.__table__.columns}
    assert cols == {"id", "codice", "tipo", "stato", "lat", "lng", "batteria", "created_at"}
