"""
Data Processing Framework - Main Transformation Wrapper

This module provides a DQ-enforced wrapper for data transformations that:
1. Runs pre-transformation data quality checks
2. Executes the transformation using the specified engine
3. Runs post-transformation data quality checks
4. Tracks data lineage and generates reports

Usage:
    python -m framework.wrapper --contract path/to/contract.yaml --config path/to/transform_config.yaml
"""

import sys
import os
import argparse
import yaml
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from pathlib import Path

# Add framework to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.dbt_engine import DbtEngine
from engines.sql_engine import SqlEngine
from engines.spark_engine import SparkEngine
from engines.python_engine import PythonEngine
from dq.gx_runner import GXRunner
from utils.config import ConfigManager
from utils.lineage import LineageTracker


@dataclass
class TransformationConfig:
    """Configuration for a data transformation"""
    name: str
    type: str
    source_tables: List[str]
    target_tables: List[str]
    transformation_config: Dict[str, Any]
    pre_dq_checks: List[str]
    post_dq_checks: List[str]
    contract_path: str
    output_dir: str
    gx_suites_path: Optional[str] = None  # Path to Step 5 generated GX suites


class TransformationEngine(ABC):
    """Abstract base class for transformation engines"""
    
    @abstractmethod
    def execute(self, config: TransformationConfig) -> bool:
        """Execute the transformation"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate engine-specific configuration"""
        pass


class DQCheckFailedException(Exception):
    """Exception raised when DQ checks fail"""
    pass


class TransformationFailedException(Exception):
    """Exception raised when transformation execution fails"""
    pass


class DQTransformationWrapper:
    """Main wrapper class that enforces DQ checks around transformations"""
    
    def __init__(self, config: TransformationConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.engine = self._get_engine()
        self.gx_runner = GXRunner(config.contract_path, config.output_dir, config.gx_suites_path)
        self.lineage_tracker = LineageTracker(config.output_dir)
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{self.config.output_dir}/transformation.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _get_engine(self) -> TransformationEngine:
        """Get the appropriate transformation engine"""
        engines = {
            'dbt': DbtEngine,
            'sql': SqlEngine,
            'spark': SparkEngine,
            'python': PythonEngine
        }
        
        engine_class = engines.get(self.config.type)
        if not engine_class:
            raise ValueError(f"Unsupported transformation type: {self.config.type}")
            
        return engine_class()
    
    def run(self) -> bool:
        """Execute transformation with enforced DQ checks"""
        try:
            self.logger.info(f"Starting transformation: {self.config.name}")
            
            # Validate configuration
            if not self.engine.validate_config(self.config.transformation_config):
                raise TransformationFailedException("Invalid transformation configuration")
            
            # 1. Pre-transformation DQ checks
            self.logger.info("Running pre-transformation DQ checks...")
            if not self._run_pre_checks():
                raise DQCheckFailedException("Pre-transformation DQ checks failed")
            
            # 2. Execute transformation
            self.logger.info(f"Executing {self.config.type} transformation...")
            if not self.engine.execute(self.config):
                raise TransformationFailedException("Transformation execution failed")
            
            # 3. Post-transformation DQ checks
            self.logger.info("Running post-transformation DQ checks...")
            if not self._run_post_checks():
                raise DQCheckFailedException("Post-transformation DQ checks failed")
            
            # 4. Update lineage
            self.logger.info("Updating data lineage...")
            self._update_lineage()
            
            self.logger.info("Transformation completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Transformation failed: {str(e)}")
            self._generate_failure_report(str(e))
            return False
    
    def _run_pre_checks(self) -> bool:
        """Run pre-transformation DQ checks"""
        if not self.config.pre_dq_checks:
            self.logger.info("No pre-transformation DQ checks configured")
            return True
            
        return self.gx_runner.run_checks(
            check_names=self.config.pre_dq_checks,
            tables=self.config.source_tables,
            check_type="pre_transformation"
        )
    
    def _run_post_checks(self) -> bool:
        """Run post-transformation DQ checks"""
        if not self.config.post_dq_checks:
            self.logger.info("No post-transformation DQ checks configured")
            return True
            
        return self.gx_runner.run_checks(
            check_names=self.config.post_dq_checks,
            tables=self.config.target_tables,
            check_type="post_transformation"
        )
    
    def _update_lineage(self):
        """Update data lineage information"""
        lineage_info = {
            'transformation_name': self.config.name,
            'transformation_type': self.config.type,
            'source_tables': self.config.source_tables,
            'target_tables': self.config.target_tables,
            'contract_path': self.config.contract_path,
            'execution_time': self.logger.handlers[0].formatter.formatTime(
                logging.LogRecord('', 0, '', 0, '', (), None)
            )
        }
        
        self.lineage_tracker.track_transformation(lineage_info)
    
    def _generate_failure_report(self, error_message: str):
        """Generate a failure report"""
        report_path = f"{self.config.output_dir}/failure_report.yaml"
        failure_info = {
            'transformation_name': self.config.name,
            'transformation_type': self.config.type,
            'error_message': error_message,
            'source_tables': self.config.source_tables,
            'target_tables': self.config.target_tables,
            'contract_path': self.config.contract_path
        }
        
        with open(report_path, 'w') as f:
            yaml.dump(failure_info, f, default_flow_style=False)
        
        self.logger.info(f"Failure report generated: {report_path}")


def load_config(config_path: str, contract_path: str, output_dir: str) -> TransformationConfig:
    """Load transformation configuration from YAML file"""
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    transformation = config_data['transformation']
    source = config_data['source']
    target = config_data['target']
    data_quality = config_data.get('data_quality', {})
    
    # Get GX suites path from data_quality config, with default to Step 5
    gx_config = data_quality.get('gx_config', {})
    gx_suites_path = gx_config.get('suites_path', '../../gx_generation/suites_cli')
    
    return TransformationConfig(
        name=transformation['name'],
        type=transformation['type'],
        source_tables=source['tables'],
        target_tables=target['tables'],
        transformation_config=config_data.get('transformation_config', {}),
        pre_dq_checks=data_quality.get('pre_checks', []),
        post_dq_checks=data_quality.get('post_checks', []),
        contract_path=contract_path,
        output_dir=output_dir,
        gx_suites_path=gx_suites_path
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Execute data transformation with DQ enforcement')
    parser.add_argument('--contract', required=True, help='Path to data contract YAML file')
    parser.add_argument('--config', required=True, help='Path to transformation config YAML file')
    parser.add_argument('--output', default='./output', help='Output directory for reports and logs')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    os.makedirs(f"{args.output}/reports", exist_ok=True)
    os.makedirs(f"{args.output}/lineage", exist_ok=True)
    os.makedirs(f"{args.output}/logs", exist_ok=True)
    
    # Load configuration
    config = load_config(args.config, args.contract, args.output)
    
    # Execute transformation
    wrapper = DQTransformationWrapper(config)
    success = wrapper.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
