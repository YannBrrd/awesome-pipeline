#!/bin/bash
#
# Script de build/test pour CI/CD
# Usage: ./build.sh
#

set -e  # Exit on error

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔨 Build du générateur DLT${NC}"
echo "================================"

# Détection de Python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo -e "${BLUE}📍 Environnement:${NC}"
echo "  Python: $(${PYTHON_CMD} --version)"
echo "  Pip: $(${PYTHON_CMD} -m pip --version)"
echo ""

# Installation des dépendances
echo -e "${BLUE}📦 Installation des dépendances...${NC}"
${PYTHON_CMD} -m pip install -r requirements.txt

# Validation de la syntaxe Python
echo -e "${BLUE}🔍 Validation de la syntaxe...${NC}"
${PYTHON_CMD} -m py_compile generate.py
${PYTHON_CMD} -m py_compile contract_model.py
${PYTHON_CMD} -m py_compile test_generator.py
echo -e "${GREEN}✅ Syntaxe Python valide${NC}"

# Exécution des tests
echo -e "${BLUE}🧪 Exécution des tests...${NC}"
${PYTHON_CMD} test_generator.py

# Test de génération
echo -e "${BLUE}🎬 Test de génération...${NC}"
rm -rf test-build
${PYTHON_CMD} generate.py --contract ../../../demo/contracts/contract.yaml --out test-build
if [ -f "test-build/ingest.py" ] && [ -f "test-build/README.md" ] && [ -f "test-build/.env.example" ]; then
    echo -e "${GREEN}✅ Génération réussie${NC}"
else
    echo -e "${RED}❌ Fichiers manquants dans test-build${NC}"
    exit 1
fi

# Validation du code généré
echo -e "${BLUE}🔍 Validation du code généré...${NC}"
${PYTHON_CMD} -m py_compile test-build/ingest.py
echo -e "${GREEN}✅ Code généré valide${NC}"

# Nettoyage
rm -rf test-build

echo ""
echo -e "${GREEN}🎉 Build réussi!${NC}"
echo -e "${YELLOW}📖 Prochaines étapes:${NC}"
echo "  1. Testez avec: ./start.sh demo"
echo "  2. Lisez: README.md et DEMO.md"
echo "  3. Configurez vos contrats dans ../../../demo/contracts/"
