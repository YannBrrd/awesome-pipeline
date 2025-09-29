#!/usr/bin/env python3
"""
Example: Custom Python transformation with DQ checks

This example demonstrates how to use the DQ Transformation Framework
with a custom Python script as the transformation engine.
"""

import os
import sys
import logging
from pathlib import Path

# Add framework to path
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))

from wrapper import DQTransformationWrapper
from utils.config import ConfigLoader

repo_root = Path(__file__).resolve().parents[4]
contract_path = str(repo_root / "demo" / "contracts" / "contract.yaml")
gx_suites_path = str(repo_root / "src" / "gx_generation" / "suites_cli")

def main():
    """Run Python transformation with DQ checks"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Create a sample configuration for this example
        config = {
            'transformation': {
                'id': 'python_example',
                'description': 'Python transformation example',
                'engine_type': 'python',
                'source_tables': ['raw_data.customers'],
                'target_tables': ['processed_data.customer_summary'],
                'config_path': './python_scripts',
                'metadata': {
                    'owner': 'data_team',
                    'version': '1.0'
                }
            },
            'data_quality': {
                'pre_checks': {
                    'enabled': True,
                    'check_names': ['completeness_check', 'schema_validation'],
                    'fail_on_error': True
                },
                'post_checks': {
                    'enabled': True,
                    'check_names': ['accuracy_check', 'completeness_check'],
                    'fail_on_error': True
                },
                'gx_config': {
                    'contract_path': contract_path,
                    'gx_dir': './gx',
                    'reports_dir': './reports',
                    'suites_path': gx_suites_path
                }
            },
            'engines': {
                'python': {
                    'script_path': './python_scripts/transform.py',
                    'requirements_file': './python_scripts/requirements.txt'
                }
            },
            'output': {
                'base_dir': './output',
                'generate_lineage': True,
                'lineage_format': 'yaml'
            }
        }
        
        # Initialize DQ wrapper
        wrapper = DQTransformationWrapper(config)
        
        # Execute transformation with DQ checks
        logger.info("Starting Python transformation with DQ checks...")
        success = wrapper.execute()
        
        if success:
            logger.info("✅ Transformation completed successfully!")
            logger.info("Check the output directory for results and reports")
            return 0
        else:
            logger.error("❌ Transformation failed!")
            return 1
            
    except Exception as e:
        logger.error(f"Error running transformation: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
