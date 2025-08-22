"""
Spark Transformation Engine

Handles PySpark-based transformations with proper configuration validation
and execution within the DQ wrapper framework.
"""

import subprocess
import os
import logging
from typing import Dict, Any
from ..wrapper import TransformationEngine, TransformationConfig


class SparkEngine(TransformationEngine):
    """Spark transformation engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate Spark-specific configuration"""
        spark_config = config.get('spark', {})
        
        # Check required fields
        required_fields = ['script_path']
        for field in required_fields:
            if field not in spark_config:
                self.logger.error(f"Missing required Spark config field: {field}")
                return False
        
        # Check if Spark script exists
        script_path = spark_config['script_path']
        if not os.path.exists(script_path):
            self.logger.error(f"Spark script not found: {script_path}")
            return False
        
        return True
    
    def execute(self, config: TransformationConfig) -> bool:
        """Execute Spark transformation"""
        try:
            spark_config = config.transformation_config.get('spark', {})
            script_path = spark_config['script_path']
            
            # Build spark-submit command
            cmd_parts = ['spark-submit']
            
            # Add Spark configuration options
            spark_conf = spark_config.get('conf', {})
            for key, value in spark_conf.items():
                cmd_parts.extend(['--conf', f'{key}={value}'])
            
            # Add executor and driver settings
            if 'executor_memory' in spark_config:
                cmd_parts.extend(['--executor-memory', spark_config['executor_memory']])
            
            if 'driver_memory' in spark_config:
                cmd_parts.extend(['--driver-memory', spark_config['driver_memory']])
            
            if 'executor_cores' in spark_config:
                cmd_parts.extend(['--executor-cores', str(spark_config['executor_cores'])])
            
            if 'num_executors' in spark_config:
                cmd_parts.extend(['--num-executors', str(spark_config['num_executors'])])
            
            # Add packages if specified
            packages = spark_config.get('packages', [])
            if packages:
                cmd_parts.extend(['--packages', ','.join(packages)])
            
            # Add py-files if specified
            py_files = spark_config.get('py_files', [])
            if py_files:
                cmd_parts.extend(['--py-files', ','.join(py_files)])
            
            # Add the script path
            cmd_parts.append(script_path)
            
            # Add script arguments
            script_args = spark_config.get('args', [])
            
            # Pass contract path and output dir as arguments
            script_args.extend([
                '--contract', config.contract_path,
                '--output', config.output_dir
            ])
            
            cmd_parts.extend(script_args)
            
            cmd = ' '.join(cmd_parts)
            self.logger.info(f"Executing Spark command: {cmd}")
            
            # Set environment variables if specified
            env = os.environ.copy()
            spark_env = spark_config.get('env', {})
            env.update(spark_env)
            
            # Execute spark-submit command
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                env=env
            )
            
            # Log output
            if result.stdout:
                self.logger.info(f"Spark stdout: {result.stdout}")
            if result.stderr:
                self.logger.warning(f"Spark stderr: {result.stderr}")
            
            if result.returncode == 0:
                self.logger.info("Spark transformation completed successfully")
                return True
            else:
                self.logger.error(f"Spark transformation failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing Spark transformation: {str(e)}")
            return False
