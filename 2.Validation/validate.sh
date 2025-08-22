#!/bin/bash
#
# Script de validation des data contracts avec Data Contract CLI
# Usage: ./validate.sh [contract.yaml|all]
#

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

CONTRACTS_DIR="../1.Data_contract"

function print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                          🔍 Validation Data Contracts                       ║"
    echo "║                      Data Contract CLI + Pydantic                           ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

function check_dependencies() {
    echo -e "${BLUE}📦 Vérification des dépendances...${NC}"
    
    # Vérifier datacontract CLI
    if ! command -v datacontract &> /dev/null; then
        echo -e "${YELLOW}⚠️ Data Contract CLI non trouvé. Installation...${NC}"
        pip install datacontract-cli
        
        if ! command -v datacontract &> /dev/null; then
            echo -e "${RED}❌ Échec de l'installation de datacontract-cli${NC}"
            echo "Installez manuellement avec: pip install datacontract-cli"
            exit 1
        fi
    fi
    
    # Vérifier Python
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    
    if ! command -v $PYTHON_CMD &> /dev/null; then
        echo -e "${RED}❌ Python non trouvé${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Dépendances OK${NC}"
    echo "  datacontract: $(datacontract --version 2>/dev/null || echo 'installé')"
    echo "  python: $($PYTHON_CMD --version)"
}

function validate_contract() {
    local contract_file="$1"
    local contract_name=$(basename "$contract_file" .yaml)
    
    echo -e "${BLUE}🔍 Validation de ${contract_name}...${NC}"
    
    # Validation avec Data Contract CLI
    echo -e "  ${CYAN}📋 Data Contract CLI lint...${NC}"
    if datacontract lint "$contract_file"; then
        echo -e "  ${GREEN}✅ Data Contract CLI: OK${NC}"
    else
        echo -e "  ${RED}❌ Data Contract CLI: ERREUR${NC}"
        return 1
    fi
    
    # Test de structure YAML
    echo -e "  ${CYAN}📄 Structure YAML...${NC}"
    if python3 -c "import yaml; yaml.safe_load(open('$contract_file'))" 2>/dev/null; then
        echo -e "  ${GREEN}✅ YAML valide${NC}"
    else
        echo -e "  ${RED}❌ YAML invalide${NC}"
        return 1
    fi
    
    # Validation custom si disponible
    if [ -f "contract_validator.py" ]; then
        echo -e "  ${CYAN}🐍 Validation custom...${NC}"
        if python3 contract_validator.py "$contract_file" 2>/dev/null; then
            echo -e "  ${GREEN}✅ Validation custom: OK${NC}"
        else
            echo -e "  ${YELLOW}⚠️ Validation custom: échec (non bloquant)${NC}"
        fi
    fi
    
    echo -e "${GREEN}🎉 ${contract_name} validé avec succès${NC}"
    return 0
}

function validate_all_contracts() {
    echo -e "${BLUE}📁 Recherche des contrats dans ${CONTRACTS_DIR}...${NC}"
    
    local contracts_found=0
    local contracts_valid=0
    local contracts_failed=0
    
    # Chercher les fichiers contract.yaml et *.yaml dans les sous-répertoires
    while IFS= read -r -d '' contract_file; do
        ((contracts_found++))
        echo ""
        if validate_contract "$contract_file"; then
            ((contracts_valid++))
        else
            ((contracts_failed++))
        fi
    done < <(find "$CONTRACTS_DIR" -name "*.yaml" -type f -print0)
    
    echo ""
    echo -e "${CYAN}📊 Résumé de validation:${NC}"
    echo "  Contrats trouvés: $contracts_found"
    echo -e "  ${GREEN}✅ Valides: $contracts_valid${NC}"
    if [ $contracts_failed -gt 0 ]; then
        echo -e "  ${RED}❌ Échoués: $contracts_failed${NC}"
        return 1
    else
        echo -e "  ${RED}❌ Échoués: $contracts_failed${NC}"
        return 0
    fi
}

function test_datacontract_cli() {
    echo -e "${BLUE}🧪 Test de Data Contract CLI...${NC}"
    
    # Test avec un contrat d'exemple
    local test_contract="$CONTRACTS_DIR/olist_mini/contract.yaml"
    
    if [ ! -f "$test_contract" ]; then
        echo -e "${YELLOW}⚠️ Contrat de test non trouvé: $test_contract${NC}"
        return 0
    fi
    
    echo -e "${CYAN}  Test lint...${NC}"
    if datacontract lint "$test_contract"; then
        echo -e "${GREEN}  ✅ Test lint: OK${NC}"
    else
        echo -e "${RED}  ❌ Test lint: ERREUR${NC}"
        return 1
    fi
    
    echo -e "${CYAN}  Test export (si supporté)...${NC}"
    if datacontract export --format jsonschema "$test_contract" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✅ Test export: OK${NC}"
    else
        echo -e "${YELLOW}  ⚠️ Test export: non supporté ou échec${NC}"
    fi
    
    return 0
}

function show_help() {
    echo -e "${WHITE}"
    cat << 'EOF'
🔍 Validation Data Contracts
============================

USAGE:
  ./validate.sh [contract.yaml|all|test|help]

COMMANDES:
  ./validate.sh all                    - Valider tous les contrats
  ./validate.sh contract.yaml          - Valider un contrat spécifique
  ./validate.sh test                   - Tester Data Contract CLI
  ./validate.sh help                   - Afficher cette aide

EXEMPLES:
  ./validate.sh all
  ./validate.sh ../1.Data_contract/olist_mini/contract.yaml
  ./validate.sh ../1.Data_contract/contract.yaml

VALIDATION EFFECTUÉE:
  ✅ Data Contract CLI lint
  ✅ Structure YAML
  ✅ Validation custom (si disponible)

DÉPENDANCES:
  • datacontract-cli (installé automatiquement si manquant)
  • python3
  • pyyaml

INTEGRATION:
  Ce script fait partie du workflow awesome-pipeline:
  1. Data contracts (1.Data_contract/)
  2. Validation (2.Validation/) ← VOUS ÊTES ICI
  3. Génération DLT (3.Ingestion/dlt-generator/)
EOF
    echo -e "${NC}"
}

# Point d'entrée principal
print_banner

# Vérifier les dépendances
check_dependencies
echo ""

# Parser les arguments
case "${1:-all}" in
    "all")
        validate_all_contracts
        ;;
    "test")
        test_datacontract_cli
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *.yaml|*.yml)
        if [ -f "$1" ]; then
            validate_contract "$1"
        else
            echo -e "${RED}❌ Fichier non trouvé: $1${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${RED}❌ Argument invalide: $1${NC}"
        show_help
        exit 1
        ;;
esac
