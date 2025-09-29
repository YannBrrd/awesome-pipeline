# Makefile pour la validation des data contracts
# Usage: make [install|validate|validate-all|test|clean|help]

PYTHON := $(shell command -v python3 2> /dev/null || echo python)
CONTRACTS_DIR := ../../demo/contracts

.PHONY: install validate validate-all test clean help

# Installation des dépendances
install:
	@echo "📦 Installation des outils de validation..."
	@$(PYTHON) -m pip install -r requirements.txt
	@echo "✅ Installation terminée!"

# Validation de tous les contrats
validate-all:
	@echo "🔍 Validation de tous les contrats..."
	@./validate.sh all

# Validation d'un contrat spécifique
# Usage: make validate CONTRACT=path/to/contract.yaml
validate:
	@if [ -z "$(CONTRACT)" ]; then \
		echo "❌ Veuillez spécifier CONTRACT=path/to/contract.yaml"; \
		exit 1; \
	fi
	@./validate.sh $(CONTRACT)

# Test des outils
test:
	@echo "🧪 Test des outils de validation..."
	@./validate.sh test

# Validation du contrat olist_mini (exemple)
validate-olist:
	@./validate.sh $(CONTRACTS_DIR)/olist_mini/contract.yaml

# Lint rapide avec datacontract-cli seulement
# Usage: make lint CONTRACT=path/to/contract.yaml
lint:
	@if [ -z "$(CONTRACT)" ]; then \
		echo "❌ Veuillez spécifier CONTRACT=path/to/contract.yaml"; \
		exit 1; \
	fi
	@echo "📋 Lint Data Contract CLI..."
	@datacontract lint $(CONTRACT)

# Export d'un contrat (si supporté)
# Usage: make export CONTRACT=path/to/contract.yaml FORMAT=jsonschema
export:
	@if [ -z "$(CONTRACT)" ]; then \
		echo "❌ Veuillez spécifier CONTRACT=path/to/contract.yaml"; \
		exit 1; \
	fi
	@echo "📤 Export du contrat..."
	@datacontract export --format $(or $(FORMAT),jsonschema) $(CONTRACT)

# Nettoyage
clean:
	@echo "🧹 Nettoyage..."
	@rm -rf __pycache__ *.pyc .pytest_cache

# Aide
help:
	@echo "🔧 Validation Data Contracts - Commandes Make"
	@echo "============================================="
	@echo ""
	@echo "COMMANDES PRINCIPALES:"
	@echo "  make install          - Installer datacontract-cli et dépendances"
	@echo "  make validate-all     - Valider tous les contrats"
	@echo "  make test            - Tester les outils"
	@echo "  make clean           - Nettoyer les fichiers temporaires"
	@echo ""
	@echo "COMMANDES AVEC PARAMÈTRES:"
	@echo "  make validate CONTRACT=path/to/contract.yaml"
	@echo "  make lint CONTRACT=path/to/contract.yaml"
	@echo "  make export CONTRACT=path/to/contract.yaml FORMAT=jsonschema"
	@echo ""
	@echo "EXEMPLES RAPIDES:"
	@echo "  make validate-olist   - Valider le contrat olist_mini"
	@echo "  make lint CONTRACT=../../demo/contracts/contract.yaml"
	@echo ""
	@echo "USAGE DIRECT:"
	@echo "  ./validate.sh all"
	@echo "  ./validate.sh path/to/contract.yaml"
	@echo "  datacontract lint path/to/contract.yaml"
