-- =============================================
-- Script 03: Drop completo de la base de datos
-- Ejecutar: psql -h IP_CLOUD_SQL -U scorebank_user -d scorebank-db -f 03_drop_tablas.sql
-- =============================================

-- Eliminar tablas en orden por dependencias (foreign keys)
DROP TABLE IF EXISTS evaluaciones CASCADE;
DROP TABLE IF EXISTS solicitudes_credito CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

-- Eliminar secuencias
DROP SEQUENCE IF EXISTS evaluaciones_id_seq;
DROP SEQUENCE IF EXISTS solicitudes_credito_id_seq;
DROP SEQUENCE IF EXISTS clientes_id_seq;

SELECT 'Base de datos eliminada completamente' AS resultado;
