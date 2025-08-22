"""
Python Transformation Engine

Handles custom Python-based transformations with proper configuration validation
and execution within the DQ wrapper framework.
"""

import subprocess
import sys
import os
import logging
from typing import Dict, Any
from ..wrapper import TransformationEngine, TransformationConfig


class PythonEngine(TransformationEngine):
    """Python transformation engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate Python-specific configuration"""
        python_config = config.get('python', {})
        
        # Check required fields
        required_fields = ['script_path']
        for field in required_fields:
            if field not in python_config:
                self.logger.error(f"Missing required Python config field: {field}")
                return False
        
        # Check if Python script exists
        script_path = python_config['script_path']
        if not os.path.exists(script_path):
            self.logger.error(f"Python script not found: {script_path}")
            return False
        
        # Check if requirements file exists (if specified)
        requirements_file = python_config.get('requirements_file')
        if requirements_file and not os.path.exists(requirements_file):
            self.logger.error(f"Requirements file not found: {requirements_file}")
            return False
        
        return True
    
    def execute(self, config: TransformationConfig) -> bool:
        """Execute Python transformation"""
        try:
            python_config = config.transformation_config.get('python', {})
            script_path = python_config['script_path']
            
            # Install requirements if specified
            requirements_file = python_config.get('requirements_file')
            if requirements_file:
                if not self._install_requirements(requirements_file):
                    return False
            
            # Build Python command
            python_executable = python_config.get('python_executable', sys.executable)
            cmd_parts = [python_executable, script_path]
            
            # Add script arguments
            script_args = python_config.get('args', [])
            
            # Pass contract path and output dir as arguments
            script_args.extend([
                '--contract', config.contract_path,
                '--output', config.output_dir,
                '--source-tables', ','.join(config.source_tables),
                '--target-tables', ','.join(config.target_tables)
            ])
            
            cmd_parts.extend(script_args)
            
            cmd = ' '.join(cmd_parts)
            self.logger.info(f"Executing Python command: {cmd}")
            
            # Set environment variables if specified
            env = os.environ.copy()
            python_env = python_config.get('env', {})
            env.update(python_env)
            
            # Set working directory if specified
            working_dir = python_config.get('working_dir', os.path.dirname(script_path))
            
            # Execute Python script
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                env=env,
                cwd=working_dir
            )
            
            # Log output
            if result.stdout:
                self.logger.info(f"Python stdout: {result.stdout}")
            if result.stderr:
                self.logger.warning(f"Python stderr: {result.stderr}")
            
            if result.returncode == 0:
                self.logger.info("Python transformation completed successfully")
                return True
            else:
                self.logger.error(f"Python transformation failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing Python transformation: {str(e)}")
            return False
    
    def _install_requirements(self, requirements_file: str) -> bool:
        """Install Python requirements"""
        try:
            self.logger.info(f"Installing requirements from: {requirements_file}")
            
            cmd = [sys.executable, '-m', 'pip', 'install', '-r', requirements_file]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Requirements installed successfully")
                return True
            else:
                self.logger.error(f"Failed to install requirements: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error installing requirements: {str(e)}")
            return False
