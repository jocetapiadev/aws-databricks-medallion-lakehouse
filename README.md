# AWS & Databricks Medallion Lakehouse Pipeline

Este proyecto implementa un pipeline de datos de extremo a extremo basado en la **Arquitectura Medallion** (Bronze, Silver y Gold) utilizando **PySpark**, **Delta Lake**, **Databricks Serverless** y almacenamiento en **AWS S3**.

## 🏗️ Arquitectura
- **AWS S3**: Almacenamiento distribuido multicapa (`s3a://jocelyn-lakehouse-bronze`, `silver`, `gold`).
- **AWS IAM**: Control de acceso y políticas por roles para integración con Databricks.
- **Databricks Serverless & Delta Lake**: Procesamiento distribuido y tablas con transacciones ACID.
- **Databricks SQL Warehouse**: Motor de consultas para capas analíticas de consumo.

## 🔄 Flujo de Datos
1. **Bronze (Raw)**: Ingesta de datos en bruto guardando la marca de tiempo (`ingested_at`).
2. **Silver (Cleaned & PII)**: Filtrado de registros sin correo válido y anonimización de datos sensibles con **SHA-256**.
3. **Gold (Analytics)**: Agregaciones de negocio optimizadas para tableros de control y BI.
