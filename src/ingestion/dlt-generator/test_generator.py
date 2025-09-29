#!/usr/bin/env python
"""
Script de test pour valider le générateur DLT.
Usage: python test_generator.py
"""

import sys
from pathlib import Path
import yaml
from contract_model import Contract

def test_contract_validation():
    """Test la validation des modèles Pydantic."""
    print("🧪 Test de validation des contrats...")
    
    # Test contrat valide
    valid_contract = {
        "version": "1.0",
        "pipeline": {"name": "test-pipeline"},
        "source": {
            "type": "api",
            "base_url": "https://api.example.com",
            "auth": {"kind": "none"}
        },
        "destination": {
            "type": "duckdb",
            "schema": "main"
        },
        "schema": {
            "test_table": {
                "primary_key": ["id"],
                "columns": {
                    "id": {"type": "bigint", "nullable": False},
                    "name": {"type": "text", "nullable": True}
                }
            }
        }
    }
    
    try:
        contract = Contract.model_validate(valid_contract)
        print("✅ Validation contrat valide : OK")
    except Exception as e:
        print(f"❌ Erreur validation contrat valide : {e}")
        return False
    
    # Test contrat invalide (manque base_url)
    invalid_contract = valid_contract.copy()
    del invalid_contract["source"]["base_url"]
    
    try:
        Contract.model_validate(invalid_contract)
        print("❌ Validation contrat invalide : devrait échouer")
        return False
    except Exception:
        print("✅ Validation contrat invalide : OK (échec attendu)")
    
    return True

def test_example_contracts():
    """Test les contrats d'exemple."""
    print("\n📋 Test des contrats d'exemple...")
    
    examples_dir = Path("../../../demo/contracts")
    if not examples_dir.exists():
        print("❌ Répertoire ../../../demo/contracts/ introuvable")
        return False
    
    for contract_file in examples_dir.glob("*.yaml"):
        print(f"  Validation de {contract_file.name}...")
        try:
            with contract_file.open() as f:
                data = yaml.safe_load(f)
            
            # Les exemples peuvent avoir des champs vides, on ne valide que la structure
            if not data:
                print(f"    ⚠️  {contract_file.name} est vide")
                continue
                
            print(f"    ✅ {contract_file.name} : structure YAML valide")
            
        except Exception as e:
            print(f"    ❌ {contract_file.name} : erreur - {e}")
            return False
    
    return True

def test_template_files():
    """Vérifie la présence des templates."""
    print("\n📄 Test des fichiers templates...")
    
    templates_dir = Path("templates")
    required_templates = ["ingest.py.j2", "README.md.j2", "env.example.j2"]
    
    for template in required_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"  ✅ {template}")
        else:
            print(f"  ❌ {template} manquant")
            return False
    
    return True

def main():
    """Point d'entrée principal."""
    print("🚀 Test du générateur DLT")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Tests de validation
    if not test_contract_validation():
        all_tests_passed = False
    
    # Tests des exemples  
    if not test_example_contracts():
        all_tests_passed = False
        
    # Tests des templates
    if not test_template_files():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("🎉 Tous les tests sont passés !")
        print("\nPour tester la génération complète :")
        print("  python generate.py --contract ../../../demo/contracts/contract.yaml --out test-build")
        return 0
    else:
        print("💥 Certains tests ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
