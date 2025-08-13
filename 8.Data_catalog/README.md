# 8. Data Catalog (OpenMetadata)

But: fournir un catalogue de données local avec OpenMetadata pour explorer schémas, lineage et qualité.

Prérequis
- Docker Desktop
- ~4–6 Go de RAM disponible pour le stack (ES, MySQL, Kafka, OM)

Démarrage rapide (PowerShell)
- Démarrer:
  .\start.ps1
- Vérifier l’état:
  .\status.ps1
- Suivre les logs serveur:
  .\logs.ps1
- Arrêter (conserver données):
  .\stop.ps1
- Réinitialiser (supprime volumes):
  .\reset.ps1

Accès UI
- http://localhost:8585
- Identifiants: admin@open-metadata.org / admin

Intégration avec ce repo
- Le DDL généré dans `4.DDL_for_catalogs/ddl/` peut être appliqué à votre entrepôt/source, puis enregistré dans OpenMetadata via ses connecteurs d’ingestion (non inclus ici).
- Vous pouvez déclarer des connexions de base de données et scheduler des ingestions depuis l’UI (Ingestion).

Notes
- Ce docker-compose est pour la démo locale uniquement (Elasticsearch sans auth, Kafka single-broker).
- Pour la prod, suivre la documentation officielle: https://open-metadata.org/docs/
