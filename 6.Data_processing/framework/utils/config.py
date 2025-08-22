"""
Configuration utilities for the DQ Transformation Framework
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """Configuration loader for transformation projects"""
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML or JSON file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                return yaml.safe_load(f)
            elif config_path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError(f"Unsupported configuration format: {config_path}")
    
    @staticmethod
    def load_data_contract(contract_path: str) -> Dict[str, Any]:
        """Load and validate data contract"""
        contract = ConfigLoader.load_config(contract_path)
        
        # Basic validation
        required_fields = ['dataContractSpecification', 'id', 'info']
        for field in required_fields:
            if field not in contract:
                raise ValueError(f"Data contract missing required field: {field}")
        
        return contract
    
    @staticmethod
    def get_transformation_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract transformation configuration"""
        return config.get('transformation', {})
    
    @staticmethod
    def get_dq_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data quality configuration"""
        return config.get('data_quality', {})
    
    @staticmethod
    def get_engine_config(config: Dict[str, Any], engine_type: str) -> Dict[str, Any]:
        """Extract engine-specific configuration"""
        return config.get('engines', {}).get(engine_type, {})


class EnvironmentManager:
    """Environment variable and path management"""
    
    @staticmethod
    def setup_environment(config: Dict[str, Any]):
        """Setup environment variables from config"""
        env_vars = config.get('environment', {})
        for key, value in env_vars.items():
            os.environ[key] = str(value)
    
    @staticmethod
    def get_project_root() -> str:
        """Get project root directory"""
        current_dir = Path.cwd()
        while current_dir.parent != current_dir:
            if (current_dir / 'pyproject.toml').exists() or \
               (current_dir / 'setup.py').exists() or \
               (current_dir / 'requirements.txt').exists():
                return str(current_dir)
            current_dir = current_dir.parent
        return str(Path.cwd())
    
    @staticmethod
    def ensure_output_dir(output_dir: str) -> str:
        """Ensure output directory exists"""
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    @staticmethod
    def get_temp_dir(base_dir: str = None) -> str:
        """Get temporary directory for processing"""
        if base_dir is None:
            base_dir = EnvironmentManager.get_project_root()
        
        temp_dir = os.path.join(base_dir, '.dq_temp')
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir


class ValidationUtils:
    """Validation utilities"""
    
    @staticmethod
    def validate_file_exists(file_path: str, description: str = "File"):
        """Validate that a file exists"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{description} not found: {file_path}")
    
    @staticmethod
    def validate_directory_exists(dir_path: str, description: str = "Directory"):
        """Validate that a directory exists"""
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(f"{description} not found: {dir_path}")
    
    @staticmethod
    def validate_engine_type(engine_type: str):
        """Validate engine type"""
        valid_engines = ['dbt', 'sql', 'spark', 'python']
        if engine_type not in valid_engines:
            raise ValueError(f"Invalid engine type: {engine_type}. Must be one of {valid_engines}")
    
    @staticmethod
    def validate_config_structure(config: Dict[str, Any]):
        """Validate basic config structure"""
        required_sections = ['transformation', 'data_quality']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Configuration missing required section: {section}")
