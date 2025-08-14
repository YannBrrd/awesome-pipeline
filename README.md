# awesome-pipeline
Automated Pipeline & Data Trust by Design

## Description

Ce projet démontre une chaîne de valeur “Data Trust by Design” complète, de la définition d’un contrat de données jusqu’à l’orchestration et la mise à disposition dans un catalogue:
- Définir des contrats producteurs (schéma, qualité, SLA, sécurité)
- Valider et compiler ces contrats pour générer des artefacts (schémas JSON, DDL, suites de tests)
- Générer le code d’ingestion (dlt) avec des attentes (not_null, unique, min/enum/regex)
- Exécuter des contrôles de qualité (Great Expectations) et des checks transverses
- Publier des schémas dans l’entrepôt/cataloque
- Orchestrer le tout (Dagster)

## Structure du projet

1. Data contract (`1.Data_contract/`)
2. Validation & artefacts (`2.Validation/`)
3. Ingestion DLTHub (`3.Ingestion/`)
4. DDL pour catalogues (`4.DDL_for_catalogs/`)
5. Great Expectations (`5.GX_code/`)
6. Data processing (`6.Data_processing/`)
7. Orchestrateur Dagster (`7.Orchestrator/`)
8. Data Catalog (OpenMetadata) (`8.Data_catalog/`)

## Parcours type
1) Générer un petit dataset synthétique (Olist mini) et valider le contrat
2) Générer DDL, suites GX et pipeline dlt depuis le contrat
3) Charger les données dans Databricks (SQL Warehouse) avec dlt
4) Orchestrer l’enchaînement des étapes avec Dagster
5) Lancer le Data Catalog OpenMetadata en local et configurer des ingestions

## Démarrage rapide (PowerShell)
- Installer dépendances Python:
  
  ```powershell
  py -m pip install -r requirements.txt
  ```

- Générer données + valider contrat:
  
  ```powershell
  py .\scripts\generate_olist_mini.py
  py .\2.Validation\contract_validator.py .\1.Data_contract\olist_mini\contract.yaml
  ```

- Générer DDL & suites GX via Data Contracts CLI + pipeline dlt:
  
  ```powershell
  # Installer le CLI (une fois) – voir doc officielle du projet
  # pipx install data-contract-cli
  data-contract-cli ddl --dialect databricks --contract .\1.Data_contract\olist_mini\contract.yaml --out .\4.DDL_for_catalogs\ddl_cli
  data-contract-cli gx --contract .\1.Data_contract\olist_mini\contract.yaml --out .\5.GX_code\suites_cli
  py .\3.Ingestion\generate_dlt_pipeline_databricks.py .\1.Data_contract\olist_mini\contract.yaml
  ```

- Exécuter ingestion (Databricks SQL Warehouse):
  
  ```powershell
  $env:OLIST_DATA_DIR = "data/olist_mini"
  $env:DLT_DATASET = "raw_olist"
  $env:DATABRICKS_SERVER_HOSTNAME = "<workspace-host>"
  $env:DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/<id>"
  $env:DATABRICKS_ACCESS_TOKEN = "<token>"
  py .\3.Ingestion\pipelines\contract_databricks_pipeline.py
  ```
- Orchestrateur Dagster (UI):
  
  ```powershell
  dagster dev -m 7.Orchestrator.orchestrator
  ```

- Data Catalog OpenMetadata:
  
  ```powershell
  cd .\8.Data_catalog; cp .env.example .env; docker compose up -d; start http://localhost:8585
  ```

## Liens
- Data Contracts: https://datacontract.com/
- DLTHub: https://dlthub.com/
- Great Expectations: https://greatexpectations.io/
- Dagster: https://dagster.io/
- OpenMetadata: https://open-metadata.org/

## Diagramme de flux (Mermaid)

```mermaid
flowchart TD
  A["Contrat de données<br/>(1.Data_contract)"] --> B["Validation & Compilation<br/>(2.Validation)"]

  B --> C["DDL (Databricks UC) via CLI<br/>(4.DDL_for_catalogs)"]
  B --> D["Suites GX via CLI<br/>(5.GX_code)"]
  B --> E["Code dlt généré (Databricks)<br/>(3.Ingestion)"]

  subgraph ING[Ingestion]
    direction LR
    E --> F2["Ingestion Databricks"]
  end

  F2 --> G

  C --> H["Unity Catalog (Databricks)"]
  G --> I["OpenMetadata (Data Catalog)<br/>(8.Data_catalog)"]
  H --> I

  subgraph ORCH["Orchestrateur (Dagster)"]
    direction TB
    O1 -.-> A
    O2 -.-> B
    O3 -.-> C
    O4 -.-> D
    O5 -.-> E
    O7 -.-> F2
  end
```
