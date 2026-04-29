-- =============================================
-- Script 01: Crear tablas
-- Ejecutar: psql -h IP_CLOUD_SQL -U scorebank_user -d scorebank-db -f 01_crear_tablas.sql
-- =============================================

CREATE SEQUENCE IF NOT EXISTS clientes_id_seq;
CREATE SEQUENCE IF NOT EXISTS solicitudes_credito_id_seq;
CREATE SEQUENCE IF NOT EXISTS evaluaciones_id_seq;

CREATE TABLE IF NOT EXISTS clientes (
    id                  INTEGER     NOT NULL DEFAULT nextval('clientes_id_seq'),
    nombre              VARCHAR     NOT NULL,
    ingreso_mensual     NUMERIC     NOT NULL CHECK (ingreso_mensual > 0),
    puntaje_crediticio  INTEGER     NOT NULL CHECK (puntaje_crediticio >= 300 AND puntaje_crediticio <= 850),
    deuda_actual        NUMERIC     NOT NULL CHECK (deuda_actual >= 0),
    created_at          TIMESTAMP   DEFAULT now(),
    CONSTRAINT clientes_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS solicitudes_credito (
    id                  INTEGER     NOT NULL DEFAULT nextval('solicitudes_credito_id_seq'),
    cliente_id          INTEGER     NOT NULL,
    monto_solicitado    NUMERIC     NOT NULL CHECK (monto_solicitado > 0),
    plazo_meses         INTEGER     NOT NULL CHECK (plazo_meses > 0),
    estado              VARCHAR     NOT NULL DEFAULT 'PENDIENTE',
    tasa_interes        NUMERIC,
    fecha_creacion      TIMESTAMP   DEFAULT now(),
    CONSTRAINT solicitudes_credito_pkey PRIMARY KEY (id),
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS evaluaciones (
    id                  INTEGER     NOT NULL DEFAULT nextval('evaluaciones_id_seq'),
    solicitud_id        INTEGER     NOT NULL,
    score_calculado     NUMERIC     NOT NULL,
    decision            VARCHAR     NOT NULL,
    razon               TEXT,
    fecha_evaluacion    TIMESTAMP   DEFAULT now(),
    CONSTRAINT evaluaciones_pkey PRIMARY KEY (id),
    CONSTRAINT fk_solicitud FOREIGN KEY (solicitud_id) REFERENCES solicitudes_credito(id)
);

-- Permisos al usuario
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO scorebank_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO scorebank_user;

SELECT 'Tablas creadas exitosamente' AS resultado;
