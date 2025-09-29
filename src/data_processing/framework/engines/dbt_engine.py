"""
dbt Transformation Engine

Handles dbt-based transformations with proper configuration validation
and execution within the DQ wrapper framework.
"""

import subprocess
import os
import logging
from typing import Dict, Any
from ..wrapper import TransformationEngine, TransformationConfig


class DbtEngine(TransformationEngine):
    """dbt transformation engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate dbt-specific configuration"""
        dbt_config = config.get('dbt', {})
        
        # Check required fields
        required_fields = ['project_dir']
        for field in required_fields:
            if field not in dbt_config:
                self.logger.error(f"Missing required dbt config field: {field}")
                return False
        
        # Check if dbt project directory exists
        project_dir = dbt_config['project_dir']
        if not os.path.exists(project_dir):
            self.logger.error(f"dbt project directory not found: {project_dir}")
            return False
        
        # Check if dbt_project.yml exists
        dbt_project_file = os.path.join(project_dir, 'dbt_project.yml')
        if not os.path.exists(dbt_project_file):
            self.logger.error(f"dbt_project.yml not found in: {project_dir}")
            return False
        
        return True
    
    def execute(self, config: TransformationConfig) -> bool:
        """Execute dbt transformation"""
        try:
            dbt_config = config.transformation_config.get('dbt', {})
            project_dir = dbt_config['project_dir']
            models = dbt_config.get('models', [])
            profiles_dir = dbt_config.get('profiles_dir', os.path.expanduser('~/.dbt'))
            
            # Build dbt command
            cmd_parts = ['dbt', 'run']
            cmd_parts.extend(['--project-dir', project_dir])
            cmd_parts.extend(['--profiles-dir', profiles_dir])
            
            if models:
                cmd_parts.extend(['--models', ' '.join(models)])
            
            # Add any additional dbt flags
            dbt_flags = dbt_config.get('flags', [])
            cmd_parts.extend(dbt_flags)
            
            cmd = ' '.join(cmd_parts)
            self.logger.info(f"Executing dbt command: {cmd}")
            
            # Execute dbt command
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=project_dir
            )
            
            # Log output
            if result.stdout:
                self.logger.info(f"dbt stdout: {result.stdout}")
            if result.stderr:
                self.logger.warning(f"dbt stderr: {result.stderr}")
            
            if result.returncode == 0:
                self.logger.info("dbt transformation completed successfully")
                return True
            else:
                self.logger.error(f"dbt transformation failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing dbt transformation: {str(e)}")
            return False
