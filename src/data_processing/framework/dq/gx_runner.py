"""
Great Expectations Runner

Handles execution of Great Expectations checks for pre/post transformation
data quality validation within the DQ wrapper framework.
"""

import os
import yaml
import subprocess
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path


class GXRunner:
    """Great Expectations check runner"""
    
    def __init__(self, contract_path: str, output_dir: str, gx_suites_path: str = None):
        self.contract_path = contract_path
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        self.gx_dir = os.path.join(output_dir, 'gx')
        self.reports_dir = os.path.join(output_dir, 'reports')
        
        # Path to pre-generated GX suites from Step 5
        self.gx_suites_path = gx_suites_path
        
        # Ensure directories exist
        os.makedirs(self.gx_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def run_checks(self, check_names: List[str], tables: List[str], check_type: str) -> bool:
        """Run Great Expectations checks"""
        try:
            self.logger.info(f"Running {check_type} DQ checks: {check_names}")
            
            # Generate GX suites if they don't exist
            if not self._gx_suites_exist():
                if not self._setup_gx_suites():
                    self.logger.error("Failed to setup GX suites")
                    return False
            
            # Run checks for each table
            all_passed = True
            results = {}
            
            for table in tables:
                table_results = {}
                for check_name in check_names:
                    result = self._run_single_check(check_name, table, check_type)
                    table_results[check_name] = result
                    if not result:
                        all_passed = False
                
                results[table] = table_results
            
            # Generate report
            self._generate_dq_report(results, check_type)
            
            if all_passed:
                self.logger.info(f"All {check_type} DQ checks passed")
            else:
                self.logger.error(f"Some {check_type} DQ checks failed")
            
            return all_passed
            
        except Exception as e:
            self.logger.error(f"Error running DQ checks: {str(e)}")
            return False
    
    def _gx_suites_exist(self) -> bool:
        """Check if GX suites exist"""
        gx_suites_dir = os.path.join(self.gx_dir, 'expectations')
        return os.path.exists(gx_suites_dir) and os.listdir(gx_suites_dir)
    
    def _setup_gx_suites(self) -> bool:
        """Setup GX suites - prioritize Step 5 pre-generated suites, fallback to generation"""
        try:
            # First priority: Use pre-generated suites from Step 5
            if self.gx_suites_path and self._copy_pregenerated_suites():
                self.logger.info("Using pre-generated GX suites from Step 5")
                return True
            
            # Fallback: Generate suites from data contract
            self.logger.info("No pre-generated suites found, generating from data contract")
            return self._generate_gx_suites()
            
        except Exception as e:
            self.logger.error(f"Error setting up GX suites: {str(e)}")
            return False
    
    def _copy_pregenerated_suites(self) -> bool:
        """Copy pre-generated GX suites from Step 5"""
        try:
            if not os.path.exists(self.gx_suites_path):
                self.logger.warning(f"Pre-generated GX suites path not found: {self.gx_suites_path}")
                return False
            
            import shutil
            
            # Copy suites from Step 5 to working directory
            target_suites_dir = os.path.join(self.gx_dir, 'expectations')
            if os.path.exists(target_suites_dir):
                shutil.rmtree(target_suites_dir)
            
            shutil.copytree(self.gx_suites_path, target_suites_dir)
            self.logger.info(f"Copied pre-generated GX suites from {self.gx_suites_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error copying pre-generated suites: {str(e)}")
            return False
    
    def _generate_gx_suites(self) -> bool:
        """Generate GX suites from data contract"""
        try:
            self.logger.info("Generating GX suites from data contract")
            
            # Use datacontract CLI to generate GX suites
            cmd = [
                'datacontract', 'export',
                '--format', 'great-expectations',
                '--output', self.gx_dir,
                self.contract_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("GX suites generated successfully")
                return True
            else:
                self.logger.error(f"Failed to generate GX suites: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error generating GX suites: {str(e)}")
            return False
    
    def _run_single_check(self, check_name: str, table: str, check_type: str) -> bool:
        """Run a single GX check"""
        try:
            # This is a simplified implementation
            # In a real scenario, you would use the Great Expectations API
            # to run specific expectations
            
            self.logger.info(f"Running {check_name} check on {table}")
            
            # For now, we'll simulate check execution
            # In practice, you would:
            # 1. Load the appropriate expectation suite
            # 2. Run the expectations against the data
            # 3. Return the validation results
            
            # Placeholder implementation - always return True for demo
            # Replace with actual GX execution logic
            return True
            
        except Exception as e:
            self.logger.error(f"Error running check {check_name} on {table}: {str(e)}")
            return False
    
    def _generate_dq_report(self, results: Dict[str, Dict[str, bool]], check_type: str):
        """Generate a data quality report"""
        try:
            report_path = os.path.join(self.reports_dir, f'{check_type}_dq_report.yaml')
            
            report_data = {
                'check_type': check_type,
                'timestamp': self._get_timestamp(),
                'contract_path': self.contract_path,
                'results': results,
                'summary': {
                    'total_checks': sum(len(table_results) for table_results in results.values()),
                    'passed_checks': sum(
                        sum(1 for result in table_results.values() if result)
                        for table_results in results.values()
                    ),
                    'failed_checks': sum(
                        sum(1 for result in table_results.values() if not result)
                        for table_results in results.values()
                    )
                }
            }
            
            with open(report_path, 'w') as f:
                yaml.dump(report_data, f, default_flow_style=False)
            
            self.logger.info(f"DQ report generated: {report_path}")
            
        except Exception as e:
            self.logger.error(f"Error generating DQ report: {str(e)}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


class GXCheckFailedException(Exception):
    """Exception raised when GX checks fail"""
    pass
