#!/bin/bash
#
# Script d'installation pour la validation des data contracts
# Usage: ./install.sh
#

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}📦 Installation des outils de validation Data Contracts${NC}"
echo "========================================================"

# Détection de Python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}❌ Python non trouvé. Installez Python 3.8+${NC}"
    exit 1
fi

echo -e "${GREEN}🐍 Python trouvé: $($PYTHON_CMD --version)${NC}"

# Installation des dépendances Python
echo -e "${BLUE}📦 Installation des dépendances Python...${NC}"
$PYTHON_CMD -m pip install -r requirements.txt

# Vérification de l'installation
echo -e "${BLUE}🔍 Vérification de l'installation...${NC}"

if command -v datacontract &> /dev/null; then
    echo -e "${GREEN}✅ datacontract-cli installé${NC}"
    datacontract --version 2>/dev/null || echo "  Version: installé"
else
    echo -e "${RED}❌ datacontract-cli non trouvé${NC}"
    exit 1
fi

# Test rapide
echo -e "${BLUE}🧪 Test rapide...${NC}"
if [ -f "../1.Data_contract/olist_mini/contract.yaml" ]; then
    echo -e "${CYAN}  Test avec contrat olist_mini...${NC}"
    if datacontract lint "../1.Data_contract/olist_mini/contract.yaml" &> /dev/null; then
        echo -e "${GREEN}  ✅ Test de validation: OK${NC}"
    else
        echo -e "${YELLOW}  ⚠️ Test de validation: échec (peut être normal si format différent)${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠️ Aucun contrat de test trouvé${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Installation terminée!${NC}"
echo ""
echo -e "${YELLOW}📖 Prochaines étapes:${NC}"
echo "  1. Validez tous les contrats: ./validate.sh all"
echo "  2. Validez un contrat spécifique: ./validate.sh path/to/contract.yaml"
echo "  3. Testez l'outil: ./validate.sh test"
echo ""
echo -e "${CYAN}📚 Documentation:${NC}"
echo "  • README.md - Guide complet"
echo "  • https://cli.datacontract.com/ - Documentation Data Contract CLI"
