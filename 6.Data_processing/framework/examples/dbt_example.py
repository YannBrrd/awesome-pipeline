#!/usr/bin/env python3
"""
Example: dbt transformation with DQ checks

This example demonstrates how to use the DQ Transformation Framework
with dbt as the transformation engine.
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

def main():
    """Run dbt transformation with DQ checks"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Configuration paths
        config_path = "config/dbt_config.yaml"
        
        # Ensure config exists
        if not os.path.exists(config_path):
            logger.error(f"Configuration file not found: {config_path}")
            logger.info("Please copy and customize framework/templates/config.yaml")
            return 1
        
        # Load configuration
        config = ConfigLoader.load_config(config_path)
        
        # Initialize DQ wrapper
        wrapper = DQTransformationWrapper(config)
        
        # Execute transformation with DQ checks
        logger.info("Starting dbt transformation with DQ checks...")
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
