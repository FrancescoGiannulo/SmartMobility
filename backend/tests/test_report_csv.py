from bll.servizio_report import ServizioReport


def _report_esempio() -> dict:
    return {
        "corse_totali": 42,
        "durata_media_h": 1.3,
        "distanza_totale_km": 128.5,
        "dati_settimanali": [
            {"giorno": "Lun", "monopattino": 1, "bicicletta": 2, "automobile": 3},
            {"giorno": "Mar", "monopattino": 0, "bicicletta": 0, "automobile": 0},
            {"giorno": "Mer", "monopattino": 0, "bicicletta": 0, "automobile": 0},
            {"giorno": "Gio", "monopattino": 0, "bicicletta": 0, "automobile": 0},
            {"giorno": "Ven", "monopattino": 0, "bicicletta": 0, "automobile": 0},
            {"giorno": "Sab", "monopattino": 0, "bicicletta": 0, "automobile": 0},
            {"giorno": "Dom", "monopattino": 0, "bicicletta": 0, "automobile": 0},
        ],
        "dati_torta": [
            {"name": "Monopattino", "value": 40.0, "colore": "#155e52"},
            {"name": "Bicicletta", "value": 35.0, "colore": "#2196f3"},
            {"name": "Automobile", "value": 25.0, "colore": "#e91e8c"},
        ],
    }


def _csv() -> str:
    return ServizioReport(None)._serializza_csv(_report_esempio())


def test_csv_inizia_con_bom_utf8():
    """Il BOM permette a Excel di riconoscere la codifica UTF-8."""
    assert _csv().startswith("﻿")


def test_csv_usa_separatore_punto_e_virgola():
    """Excel in locale italiano usa ; come separatore di lista."""
    csv = _csv()
    assert ";" in csv
    # la virgola non deve comparire come separatore di campo (solo come decimale)
    assert "Giorno;Monopattino;Bicicletta;Automobile" in csv


def test_csv_usa_terminatore_riga_crlf():
    assert "\r\n" in _csv()


def test_csv_include_kpi_di_sintesi():
    """[IF-AP.02] Il CSV deve contenere anche i KPI, non solo la tabella settimanale."""
    csv = _csv()
    assert "Corse totali;42" in csv
    assert "Durata media (h);1,3" in csv
    assert "Distanza totale (km);128,5" in csv


def test_csv_include_quote_per_tipologia():
    csv = _csv()
    assert "Monopattino;40,0" in csv
    assert "Bicicletta;35,0" in csv
    assert "Automobile;25,0" in csv


def test_csv_include_tabella_settimanale():
    csv = _csv()
    assert "Lun;1;2;3" in csv
    assert "Dom;0;0;0" in csv


def test_csv_decimali_con_virgola():
    """In locale italiano il separatore decimale è la virgola."""
    csv = _csv()
    assert "1.3" not in csv
    assert "128.5" not in csv
