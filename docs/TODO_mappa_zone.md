# TODO — Miglioramenti mappa zone

> **ELIMINARE QUESTO FILE al merge su main.**

## Backlog tecnico emerso durante Sprint 1 (feature/mappa-zone)

### 1. Vincolo zona operativa (IF-OP.02 / regola di business)
Le zone di tipo `vietata`, `limitata` e `parcheggio` possono essere create solo all'interno di una zona operativa (confine operativo) esistente.
- **Backend**: `ServizioGIS.crea_zona()` deve verificare che il poligono da creare sia contenuto (ST_Within) o intersechi la zona operativa attiva prima di procedere con l'INSERT. Sollevare `PoligonoFuoriZonaOperativaException` (HTTP 422) in caso contrario.
- **Frontend**: mostrare errore descrittivo nel modal se l'API risponde 422 per questo motivo.

### 2. Eliminazione zone (IF-OP.03)
L'operatore deve poter eliminare zone già create direttamente dalla mappa.
- **Backend**: endpoint `DELETE /operatore/zone/{id}` già implementato in `zona_operatore_controller.py` + `ZonaRepository.elimina()`.
- **Frontend (`VistaMappaOperatore`)**: aggiungere interazione click sul `Polygon` sulla mappa (o lista zone nel pannello laterale) che apre un dialog di conferma ed esegue `eliminaZona(id)` da `ZonaService.ts`, seguito da `ricaricaDati()`.

### 3. Tooltip/overview al hover sulle zone (IF-UT.01 + IF-OP.01)
Quando l'utente passa il mouse sopra una zona, deve apparire un tooltip con nome, tipo e (se presente) limite di velocità.
- Riguarda sia `VistaMappa` (utente) che `VistaMappaOperatore` (operatore).
- `@vis.gl/react-google-maps` non espone `onMouseOver` su `Polygon` direttamente; usare `google.maps.event.addListener(polygonInstance, 'mouseover', ...)` oppure `InfoWindow` posizionata sulle coordinate del cursore.
- Stato suggerito: `zonaHover: { zona: ZonaMappa; posizione: google.maps.LatLngLiteral } | null`.
- Il tooltip deve sparire al `mouseout`.
