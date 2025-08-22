"""
SQL Transformation Engine

Handles raw SQL-based transformations with database connection management
within the DQ wrapper framework.
"""

import os
import yaml
import logging
from typing import Dict, Any
from ..wrapper import TransformationEngine, TransformationConfig


class SqlEngine(TransformationEngine):
    """SQL transformation engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate SQL-specific configuration"""
        sql_config = config.get('sql', {})
        
        # Check required fields
        required_fields = ['script_path']
        for field in required_fields:
            if field not in sql_config:
                self.logger.error(f"Missing required SQL config field: {field}")
                return False
        
        # Check if SQL script exists
        script_path = sql_config['script_path']
        if not os.path.exists(script_path):
            self.logger.error(f"SQL script not found: {script_path}")
            return False
        
        return True
    
    def execute(self, config: TransformationConfig) -> bool:
        """Execute SQL transformation"""
        try:
            sql_config = config.transformation_config.get('sql', {})
            script_path = sql_config['script_path']
            
            # Read SQL script
            with open(script_path, 'r') as f:
                sql_content = f.read()
            
            self.logger.info(f"Executing SQL script: {script_path}")
            
            # Get database connection from contract
            connection = self._get_db_connection(config.contract_path)
            
            if not connection:
                self.logger.error("Failed to establish database connection")
                return False
            
            # Execute SQL
            try:
                # Split SQL content by semicolons for multiple statements
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for i, statement in enumerate(statements):
                    self.logger.info(f"Executing statement {i+1}/{len(statements)}")
                    connection.execute(statement)
                
                # Commit if needed
                if hasattr(connection, 'commit'):
                    connection.commit()
                
                self.logger.info("SQL transformation completed successfully")
                return True
                
            except Exception as e:
                self.logger.error(f"Error executing SQL: {str(e)}")
                # Rollback if needed
                if hasattr(connection, 'rollback'):
                    connection.rollback()
                return False
            
            finally:
                # Close connection
                if hasattr(connection, 'close'):
                    connection.close()
                
        except Exception as e:
            self.logger.error(f"Error in SQL transformation: {str(e)}")
            return False
    
    def _get_db_connection(self, contract_path: str):
        """Get database connection from contract configuration"""
        try:
            # Load contract to get connection details
            with open(contract_path, 'r') as f:
                contract = yaml.safe_load(f)
            
            # Extract connection info from contract
            destination = contract.get('destination', {})
            dest_type = destination.get('type')
            
            if dest_type == 'duckdb':
                return self._get_duckdb_connection(destination)
            elif dest_type == 'postgres':
                return self._get_postgres_connection(destination)
            elif dest_type == 'bigquery':
                return self._get_bigquery_connection(destination)
            elif dest_type == 'snowflake':
                return self._get_snowflake_connection(destination)
            else:
                self.logger.error(f"Unsupported destination type: {dest_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting database connection: {str(e)}")
            return None
    
    def _get_duckdb_connection(self, config: Dict[str, Any]):
        """Get DuckDB connection"""
        try:
            import duckdb
            db_path = config.get('database', ':memory:')
            return duckdb.connect(db_path)
        except ImportError:
            self.logger.error("DuckDB not installed. Install with: pip install duckdb")
            return None
    
    def _get_postgres_connection(self, config: Dict[str, Any]):
        """Get PostgreSQL connection"""
        try:
            import psycopg2
            return psycopg2.connect(
                host=config.get('host', 'localhost'),
                port=config.get('port', 5432),
                database=config.get('database'),
                user=config.get('user'),
                password=config.get('password')
            )
        except ImportError:
            self.logger.error("psycopg2 not installed. Install with: pip install psycopg2-binary")
            return None
    
    def _get_bigquery_connection(self, config: Dict[str, Any]):
        """Get BigQuery connection"""
        try:
            from google.cloud import bigquery
            client = bigquery.Client(project=config.get('project_id'))
            return client
        except ImportError:
            self.logger.error("BigQuery client not installed. Install with: pip install google-cloud-bigquery")
            return None
    
    def _get_snowflake_connection(self, config: Dict[str, Any]):
        """Get Snowflake connection"""
        try:
            import snowflake.connector
            return snowflake.connector.connect(
                user=config.get('user'),
                password=config.get('password'),
                account=config.get('account'),
                warehouse=config.get('warehouse'),
                database=config.get('database'),
                schema=config.get('schema')
            )
        except ImportError:
            self.logger.error("Snowflake connector not installed. Install with: pip install snowflake-connector-python")
            return None
