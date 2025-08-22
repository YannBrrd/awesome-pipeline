# 8. Data Catalog (OpenMetadata)

PurIntegration with this repo
- The DDL generated in `4.DDL_for_catalogs/ddl/` can be applied to your warehouse/source, then registered in OpenMetadata via its ingestion connectors (not included here).
- You can declare database connections and schedule ingestions from the UI (Ingestion).

Notes
- This docker-compose is for local demo only (Elasticsearch without auth, single-broker Kafka).
- For production, follow the official documentation: https://open-metadata.org/docs/rovide a local data catalog with OpenMetadata to explore schemas, lineage and quality.

Prerequisites
- Docker Desktop
- ~4–6 GB of available RAM for the stack (ES, MySQL, Kafka, OM)

Quick start (PowerShell)
- Start:
  
  ```powershell
  .\start.ps1
  ```
- Check status:
  
  ```powershell
  .\status.ps1
  ```
- Follow server logs:
  
  ```powershell
  .\logs.ps1
  ```
- Stop (preserve data):
  
  ```powershell
  .\stop.ps1
  ```
- Reset (delete volumes):
  
  ```powershell
  .\reset.ps1
  ```

UI Access
- http://localhost:8585
- Credentials: admin@open-metadata.org / admin

Intégration avec ce repo
- Le DDL généré dans `4.DDL_for_catalogs/ddl/` peut être appliqué à votre entrepôt/source, puis enregistré dans OpenMetadata via ses connecteurs d’ingestion (non inclus ici).
- Vous pouvez déclarer des connexions de base de données et scheduler des ingestions depuis l’UI (Ingestion).

Notes
- Ce docker-compose est pour la démo locale uniquement (Elasticsearch sans auth, Kafka single-broker).
- Pour la prod, suivre la documentation officielle: https://open-metadata.org/docs/
