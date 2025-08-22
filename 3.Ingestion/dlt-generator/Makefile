# Générateur DLT - Makefile
# Usage: make [install|test|demo|clean|help]

PYTHON := $(shell command -v python3 2> /dev/null || echo python)
PIP := $(PYTHON) -m pip

.PHONY: install test demo clean help

# Installation des dépendances
install:
	@echo "📦 Installation des dépendances..."
	@$(PIP) install -r requirements.txt
	@echo "✅ Installation terminée!"

# Exécution des tests
test:
	@echo "🧪 Exécution des tests de validation..."
	@$(PYTHON) test_generator.py

# Démonstration avec pipeline DuckDB
demo:
	@echo "🎬 Génération d'un pipeline d'exemple..."
	@$(PYTHON) generate.py --contract ../../1.Data_contract/contract.yaml --out demo-duckdb
	@echo "✅ Pipeline généré dans demo-duckdb/"
	@echo ""
	@echo "📖 Prochaines étapes:"
	@echo "  1. Éditez demo-duckdb/.env.example avec vos credentials"
	@echo "  2. Renommez-le en .env"  
	@echo "  3. Exécutez: python demo-duckdb/ingest.py"

# Démonstration BigQuery
demo-bigquery:
	@echo "☁️ Génération d'un pipeline BigQuery..."
	@$(PYTHON) generate.py --contract ../../1.Data_contract/contract-bigquery.yaml --out demo-bigquery
	@echo "✅ Pipeline BigQuery généré dans demo-bigquery/"

# Nettoyage des builds de test
clean:
	@echo "🧹 Nettoyage des builds de test..."
	@rm -rf demo-* build-* test-* __pycache__ *.pyc
	@echo "✅ Nettoyage terminé"

# Génération personnalisée
# Usage: make generate CONTRACT=path/to/contract.yaml OUT=output-dir
generate:
	@if [ -z "$(CONTRACT)" ]; then \
		echo "❌ Veuillez spécifier CONTRACT=path/to/contract.yaml"; \
		exit 1; \
	fi
	@$(PYTHON) generate.py --contract $(CONTRACT) --out $(or $(OUT),build)

# Validation d'un contrat
# Usage: make validate CONTRACT=path/to/contract.yaml  
validate:
	@if [ -z "$(CONTRACT)" ]; then \
		echo "❌ Veuillez spécifier CONTRACT=path/to/contract.yaml"; \
		exit 1; \
	fi
	@$(PYTHON) -c "from contract_model import Contract; import yaml; Contract.model_validate(yaml.safe_load(open('$(CONTRACT)')))"
	@echo "✅ Contrat $(CONTRACT) valide"

# Aide
help:
	@echo "🔧 Générateur DLT - Commandes Make disponibles"
	@echo "=============================================="
	@echo ""
	@echo "COMMANDES PRINCIPALES:"
	@echo "  make install          - Installer les dépendances Python"
	@echo "  make test            - Exécuter les tests de validation"
	@echo "  make demo            - Générer un pipeline d'exemple (DuckDB)"
	@echo "  make demo-bigquery   - Générer un pipeline BigQuery"
	@echo "  make clean           - Nettoyer les builds de test"
	@echo "  make help            - Afficher cette aide"
	@echo ""
	@echo "COMMANDES AVANCÉES:"
	@echo "  make generate CONTRACT=contract.yaml OUT=build"
	@echo "  make validate CONTRACT=contract.yaml"
	@echo ""
	@echo "USAGE MANUEL:"
	@echo "  python generate.py --contract examples/contract.yaml --out ./build"
	@echo ""
	@echo "EXEMPLES:"
	@echo "  make generate CONTRACT=examples/contract.yaml OUT=my-pipeline"
	@echo "  make validate CONTRACT=examples/contract-bigquery.yaml"
	@echo ""
	@echo "DOCUMENTATION:"
	@echo "  📖 README.md - Documentation complète"
	@echo "  🎬 DEMO.md   - Guide de démonstration"
