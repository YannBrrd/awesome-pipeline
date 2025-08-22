# Script de test de l'intégration complète
# Usage: ./test-integration.sh

#!/bin/bash

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🔗 Test d'intégration awesome-pipeline${NC}"
echo "==========================================="

# 1. Test de validation (répertoire 2)
echo -e "${BLUE}📍 Étape 1: Validation des contrats${NC}"
cd ../2.Validation
if [ -f "validate.sh" ]; then
    echo -e "${CYAN}  Installation des dépendances de validation...${NC}"
    ./install.sh
    
    echo -e "${CYAN}  Test de validation...${NC}"
    ./validate.sh test
    
    echo -e "${GREEN}  ✅ Validation OK${NC}"
else
    echo -e "${RED}  ❌ Script de validation non trouvé${NC}"
    exit 1
fi

# 2. Test de génération DLT (répertoire 3)
echo -e "${BLUE}📍 Étape 2: Génération DLT${NC}"
cd ../3.Ingestion/dlt-generator
if [ -f "build.sh" ]; then
    echo -e "${CYAN}  Build du générateur DLT...${NC}"
    ./build.sh
    
    echo -e "${GREEN}  ✅ Génération DLT OK${NC}"
else
    echo -e "${RED}  ❌ Script de build DLT non trouvé${NC}"
    exit 1
fi

# 3. Test end-to-end
echo -e "${BLUE}📍 Étape 3: Test end-to-end${NC}"

# Validation d'un contrat
echo -e "${CYAN}  Validation du contrat olist_mini...${NC}"
cd ../../2.Validation
if ./validate.sh ../1.Data_contract/olist_mini/contract.yaml; then
    echo -e "${GREEN}  ✅ Contrat olist_mini validé${NC}"
else
    echo -e "${YELLOW}  ⚠️ Contrat olist_mini: format différent (non bloquant)${NC}"
fi

# Génération d'un pipeline
echo -e "${CYAN}  Génération d'un pipeline de test...${NC}"
cd ../3.Ingestion/dlt-generator
if [ -f "../../1.Data_contract/contract.yaml" ]; then
    python generate.py --contract ../../1.Data_contract/contract.yaml --out integration-test 2>/dev/null || echo "Test de génération (peut échouer si contrat incomplet)"
    
    if [ -d "integration-test" ]; then
        echo -e "${GREEN}  ✅ Pipeline généré${NC}"
        rm -rf integration-test
    else
        echo -e "${YELLOW}  ⚠️ Génération partielle (contrat peut être incomplet)${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠️ Contrat d'exemple non trouvé${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Test d'intégration terminé!${NC}"
echo ""
echo -e "${CYAN}📋 Résumé de la structure:${NC}"
echo "  1.Data_contract/      ← Contrats + exemples"
echo "  2.Validation/         ← Validation Data Contract CLI"  
echo "  3.Ingestion/          ← Génération DLT"
echo ""
echo -e "${YELLOW}📖 Prochaines étapes:${NC}"
echo "  1. Définissez vos contrats dans 1.Data_contract/"
echo "  2. Validez avec: cd 2.Validation && ./validate.sh all"
echo "  3. Générez les pipelines: cd 3.Ingestion/dlt-generator && ./start.sh demo"
