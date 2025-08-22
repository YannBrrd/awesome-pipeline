# Test et démonstration du générateur DLT

## Installation

```bash
cd 2.Validation/dlt-generator
pip install -r requirements.txt
```

## Méthodes d'utilisation

### Option 1: Script shell (recommandé)
```bash
# Installation
./start.sh install

# Tests
./start.sh test

# Démonstration
./start.sh demo
```

### Option 2: Makefile
```bash
# Installation
make install

# Tests  
make test

# Démonstration
make demo

# Pipeline BigQuery
make demo-bigquery

# Nettoyage
make clean
```

### Option 3: Usage direct
```bash
python generate.py --contract examples/contract.yaml --out build
```

## Test basique avec DuckDB

1. **Générer avec le contrat exemple (incomplet)**:
```bash
python generate.py --contract ../../1.Data_contract/contract.yaml --out test-build
```

Le CLI vous demandera interactivement :
- Nom du pipeline
- URL de base de l'API  
- Nom de la variable d'env pour le token

2. **Voir les fichiers générés**:
```bash
ls test-build/
```

3. **Configurer l'environnement** (exemple avec une API publique):
```bash
# Copier le fichier d'exemple
cp test-build/.env.example test-build/.env

# Éditer test-build/.env avec vos credentials
# Par exemple pour une API publique :
# API_TOKEN=your_token_here
```

4. **Tester l'exécution** (si vous avez une vraie API):
```bash
cd test-build
export CONTRACT_PATH="contract.yaml"
# Sourcer le .env ou définir les variables manuellement
python ingest.py
```

## Test avec BigQuery

```bash
python generate.py --contract ../../1.Data_contract/contract-bigquery.yaml --out test-bigquery
# ou
make demo-bigquery
```

Puis suivre les instructions dans `test-bigquery/README.md` et `test-bigquery/.env.example`.

## Validation du contrat seul

Pour tester juste la validation Pydantic sans génération :

```python
from contract_model import Contract
import yaml

with open("../../1.Data_contract/contract.yaml") as f:
    data = yaml.safe_load(f)

try:
    contract = Contract.model_validate(data)
    print("✅ Contrat valide")
except Exception as e:
    print(f"❌ Erreur : {e}")
```

Ou avec Make :
```bash
make validate CONTRACT=../../1.Data_contract/contract.yaml
```

## Prochaines étapes

1. Intégrer dans votre pipeline de CI/CD
2. Connecter à de vraies APIs
3. Configurer les destinations (DuckDB local, BigQuery, etc.)
4. Ajouter des transformations dbt en aval
5. Orchestrer avec Dagster (voir `../../7.Orchestrator/`)

## Structure finale générée

```
build/
├── ingest.py          # Script DLT prêt à l'emploi
├── README.md          # Doc spécifique au pipeline
├── .env.example       # Variables d'env à configurer  
└── contract.yaml      # Contrat complété et validé
```
