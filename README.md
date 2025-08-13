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
3) Charger les données en local (DuckDB par défaut) avec dlt
4) Orchestrer l’enchaînement des étapes avec Dagster
5) Lancer le Data Catalog OpenMetadata en local et configurer des ingestions

## Démarrage rapide (PowerShell)
- Installer dépendances Python:
  py -m pip install -r requirements.txt
- Générer données + valider contrat:
  py .\scripts\generate_olist_mini.py
  py .\2.Validation\contract_validator.py .\1.Data_contract\olist_mini\contract.yaml
- Générer DDL / GX / pipeline dlt:
  py .\4.DDL_for_catalogs\generate_ddl.py
  py .\5.GX_code\generate_gx_suites.py
  py .\3.Ingestion\generate_dlt_pipeline.py .\1.Data_contract\olist_mini\contract.yaml
- Exécuter ingestion (DuckDB):
  $env:OLIST_DATA_DIR = "data/olist_mini"; $env:DLT_DESTINATION = "duckdb"; $env:DLT_DATASET = "raw_olist"; py .\3.Ingestion\pipelines\contract_pipeline.py
- Orchestrateur Dagster (UI):
  dagster dev -m 7.Orchestrator.orchestrator
- Data Catalog OpenMetadata:
  cd .\8.Data_catalog; cp .env.example .env; docker compose up -d; start http://localhost:8585

## Liens
- Data Contracts: https://datacontract.com/
- DLTHub: https://dlthub.com/
- Great Expectations: https://greatexpectations.io/
- Dagster: https://dagster.io/
- OpenMetadata: https://open-metadata.org/
