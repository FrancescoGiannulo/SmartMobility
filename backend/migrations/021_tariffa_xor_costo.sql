-- ============================================================
-- OP-05: una tariffa ha esattamente un tipo di costo (minuto XOR km),
-- come specificato nel diagramma delle classi (Tariffa.costoPerMinuto/
-- costoPerKm: float?, vincolo: esattamente uno dei due non-null).
-- ============================================================

ALTER TABLE tariffe
    ALTER COLUMN costo_al_minuto DROP NOT NULL,
    ALTER COLUMN costo_al_km DROP NOT NULL;

-- Le righe esistenti avevano entrambi i valori popolati: si mantiene
-- costo_al_minuto e si azzera costo_al_km per rispettare il nuovo vincolo.
UPDATE tariffe SET costo_al_km = NULL WHERE costo_al_minuto IS NOT NULL;

-- I CHECK originali in 001_init_schema.sql erano inline e senza nome
-- esplicito, quindi Postgres li ha auto-nominati in fase di CREATE TABLE
-- (tariffe_costo_al_minuto_check / tariffe_costo_al_km_check) e non con i
-- nomi usati in precedenza nel modello SQLAlchemy: si droppano entrambe le
-- varianti per coprire entrambi i casi.
ALTER TABLE tariffe
    DROP CONSTRAINT IF EXISTS tariffa_costo_minuto_positivo,
    DROP CONSTRAINT IF EXISTS tariffa_costo_km_positivo,
    DROP CONSTRAINT IF EXISTS tariffe_costo_al_minuto_check,
    DROP CONSTRAINT IF EXISTS tariffe_costo_al_km_check;

ALTER TABLE tariffe
    ADD CONSTRAINT tariffa_costo_xor CHECK (
        (costo_al_minuto IS NOT NULL AND costo_al_km IS NULL AND costo_al_minuto > 0)
        OR
        (costo_al_km IS NOT NULL AND costo_al_minuto IS NULL AND costo_al_km > 0)
    );
