-- =============================================
-- Script 02: Llenar tablas con datos de prueba
-- Ejecutar: psql -h IP_CLOUD_SQL -U scorebank_user -d scorebank-db -f 02_llenar_datos.sql
-- =============================================

-- Insertar clientes
INSERT INTO clientes (nombre, ingreso_mensual, puntaje_crediticio, deuda_actual) VALUES
    ('Ana García',      5000000.00, 780, 1200000.00),
    ('Carlos Pérez',    3500000.00, 650, 800000.00),
    ('María López',     8000000.00, 820, 0.00),
    ('Juan Rodríguez',  2800000.00, 510, 2500000.00),
    ('Laura Martínez',  6500000.00, 710, 500000.00);

-- Insertar solicitudes de crédito
INSERT INTO solicitudes_credito (cliente_id, monto_solicitado, plazo_meses, estado, tasa_interes) VALUES
    (1, 10000000.00, 24, 'APROBADO',  1.2),
    (2, 5000000.00,  12, 'PENDIENTE', NULL),
    (3, 20000000.00, 36, 'APROBADO',  0.9),
    (4, 3000000.00,  6,  'RECHAZADO', NULL),
    (5, 15000000.00, 24, 'PENDIENTE', NULL);

-- Insertar evaluaciones
INSERT INTO evaluaciones (solicitud_id, score_calculado, decision, razon) VALUES
    (1, 85.5, 'APROBADO',  'Buen puntaje crediticio y bajo nivel de deuda'),
    (3, 92.0, 'APROBADO',  'Excelente perfil financiero'),
    (4, 42.3, 'RECHAZADO', 'Alto nivel de deuda respecto al ingreso mensual');

-- Verificar datos insertados
SELECT 'Clientes insertados: ' || COUNT(*) AS resultado FROM clientes
UNION ALL
SELECT 'Solicitudes insertadas: ' || COUNT(*) FROM solicitudes_credito
UNION ALL
SELECT 'Evaluaciones insertadas: ' || COUNT(*) FROM evaluaciones;
