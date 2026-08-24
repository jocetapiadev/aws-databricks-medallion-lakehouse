-- Modelo Semántico dbt para la Capa Gold
{{ config(
    materialized='table',
    file_format='delta'
) }}

WITH silver_data AS (
    SELECT * FROM {{ ref('stg_clientes_silver') }}
)

SELECT
    id_cliente,
    COUNT(id_transaccion) AS total_compras,
    SUM(monto) AS mrr_total,
    MAX(created_at) AS ultima_actividad,
    CASE 
        WHEN SUM(monto) > 1000 THEN 'VIP'
        ELSE 'STANDARD'
    END AS segmento_cliente
FROM silver_data
GROUP BY id_cliente
