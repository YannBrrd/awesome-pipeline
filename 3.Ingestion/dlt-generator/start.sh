#!/bin/bash
#
# Assistant de démarrage pour le générateur DLT
# Usage: ./start.sh [install|test|demo|help]
#

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

function print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                          🚀 Générateur DLT                                  ║"
    echo "║                  Data contracts → Scripts d'ingestion DLT                   ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

function install_dlt_generator() {
    echo -e "${BLUE}📦 Installation des dépendances...${NC}"
    
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python n'est pas installé ou pas dans le PATH${NC}"
        exit 1
    fi
    
    # Utiliser python3 si disponible, sinon python
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    
    PYTHON_VERSION=$(${PYTHON_CMD} --version)
    echo -e "${GREEN}🐍 ${PYTHON_VERSION} détecté${NC}"
    
    ${PYTHON_CMD} -m pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Installation terminée avec succès!${NC}"
    else
        echo -e "${RED}❌ Échec de l'installation${NC}"
        exit 1
    fi
}

function test_dlt_generator() {
    echo -e "${BLUE}🧪 Exécution des tests de validation...${NC}"
    
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    
    ${PYTHON_CMD} test_generator.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Tous les tests sont passés!${NC}"
    else
        echo -e "${RED}❌ Certains tests ont échoué${NC}"
        exit 1
    fi
}

function start_demo() {
    echo -e "${BLUE}🎬 Démonstration du générateur...${NC}"
    echo ""
    
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    
    # Génération avec contrat d'exemple DuckDB
    echo -e "${YELLOW}1️⃣ Génération d'un pipeline DuckDB...${NC}"
    ${PYTHON_CMD} generate.py --contract ../../1.Data_contract/contract.yaml --out demo-duckdb
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Pipeline DuckDB généré dans demo-duckdb/${NC}"
        echo ""
        
        echo -e "${CYAN}📁 Fichiers générés:${NC}"
        if [ -d "demo-duckdb" ]; then
            for file in demo-duckdb/*; do
                if [ -f "$file" ]; then
                    echo -e "  ${WHITE}📄 $(basename "$file")${NC}"
                fi
            done
        fi
        echo ""
        
        echo -e "${YELLOW}📖 Prochaines étapes:${NC}"
        echo -e "  ${WHITE}1. Éditez demo-duckdb/.env.example avec vos credentials${NC}"
        echo -e "  ${WHITE}2. Renommez-le en .env${NC}"
        echo -e "  ${WHITE}3. Exécutez: python demo-duckdb/ingest.py${NC}"
        echo ""
        
        echo -e "${YELLOW}📚 Documentation:${NC}"
        echo -e "  ${WHITE}• demo-duckdb/README.md - Guide du pipeline généré${NC}"
        echo -e "  ${WHITE}• DEMO.md - Guide de démonstration détaillé${NC}"
        echo -e "  ${WHITE}• README.md - Documentation complète${NC}"
    else
        echo -e "${RED}❌ Échec de la génération${NC}"
        exit 1
    fi
}

function show_help() {
    echo -e "${WHITE}"
    cat << 'EOF'
🔧 Générateur DLT - Assistant de démarrage
=========================================

ACTIONS DISPONIBLES:
  install     Installer les dépendances Python
  test        Exécuter les tests de validation  
  demo        Générer un pipeline d'exemple
  help        Afficher cette aide

USAGE:
  ./start.sh install
  ./start.sh test
  ./start.sh demo

USAGE MANUEL:
  python generate.py --contract path/to/contract.yaml --out ./build

EXEMPLES DE CONTRATS:
  ../../1.Data_contract/contract.yaml         - Pipeline DuckDB basique
  ../../1.Data_contract/contract-bigquery.yaml - Pipeline BigQuery avancé

DESTINATIONS SUPPORTÉES:
  • DuckDB (local, idéal pour développement)
  • PostgreSQL (base de données relationnelle)  
  • BigQuery (Google Cloud, data warehouse)
  • Snowflake (cloud data platform)
  • Databricks (analytics platform)

SOURCES SUPPORTÉES:
  • API HTTP avec auth Bearer Token ou Basic
  • Pagination par numéro de page
  • Expectations de validation des données

DOCUMENTATION:
  📖 README.md   - Documentation complète du générateur
  🎬 DEMO.md     - Guide de démonstration pas-à-pas
  🧪 test_generator.py - Tests de validation

SUPPORT:
  Ce générateur fait partie de awesome-pipeline.
  Voir ../../2.Validation/README.md pour l'intégration complète.
EOF
    echo -e "${NC}"
}

# Point d'entrée principal
print_banner

ACTION=${1:-help}

case "$ACTION" in
    "install")
        install_dlt_generator
        ;;
    "test")
        test_dlt_generator
        ;;
    "demo")
        start_demo
        ;;
    "help"|*)
        show_help
        ;;
esac
