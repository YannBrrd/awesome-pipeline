# 4. DDL for catalogs

Purpose
- Generate DDL to register datasets in warehouses/catalogs from the data contract.

Generators
- generate_ddl.py: generic SQL with PK/FK and dependency-ordered create_all.sql (DuckDB/Postgres-friendly)
- generate_ddl_multi.py: multi-dialect generator for Databricks (Unity Catalog), BigQuery, Snowflake, Postgres

Usage (PowerShell)
- Databricks Unity Catalog:
  py .\4.DDL_for_catalogs\generate_ddl_multi.py --dialect databricks --catalog my_catalog --schema raw_olist
  # outputs .\4.DDL_for_catalogs\ddl_multi\create_all_databricks.sql

- BigQuery (dataset-only):
  py .\4.DDL_for_catalogs\generate_ddl_multi.py --dialect bigquery --schema raw_olist

- Snowflake (schema):
  py .\4.DDL_for_catalogs\generate_ddl_multi.py --dialect snowflake --schema RAW_OLIST

- Postgres (schema):
  py .\4.DDL_for_catalogs\generate_ddl_multi.py --dialect postgres --schema raw_olist

Notes
- Type mapping and constraints differ per platform. BigQuery omits PK/FK; Databricks includes PK only.
- Table creation order respects FK dependencies.
- Extend mappings as needed (field descriptions → column comments, indexes, clustering/partitioning).
