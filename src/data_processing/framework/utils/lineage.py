"""
Data lineage tracking utilities for the DQ Transformation Framework
"""

import os
import json
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class LineageTracker:
    """Track data lineage through transformations"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.lineage_dir = os.path.join(output_dir, 'lineage')
        os.makedirs(self.lineage_dir, exist_ok=True)
        
        self.lineage_data = {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'transformations': [],
            'datasets': {},
            'quality_checks': []
        }
    
    def track_transformation(self, 
                           transformation_id: str,
                           engine_type: str,
                           source_tables: List[str],
                           target_tables: List[str],
                           config_path: str,
                           metadata: Dict[str, Any] = None):
        """Track a transformation execution"""
        transformation_record = {
            'id': transformation_id,
            'timestamp': datetime.now().isoformat(),
            'engine_type': engine_type,
            'source_tables': source_tables,
            'target_tables': target_tables,
            'config_path': config_path,
            'metadata': metadata or {}
        }
        
        self.lineage_data['transformations'].append(transformation_record)
        
        # Track datasets
        for table in source_tables + target_tables:
            if table not in self.lineage_data['datasets']:
                self.lineage_data['datasets'][table] = {
                    'first_seen': datetime.now().isoformat(),
                    'transformations': [],
                    'quality_checks': []
                }
            
            self.lineage_data['datasets'][table]['transformations'].append(transformation_id)
    
    def track_quality_check(self,
                          check_id: str,
                          check_type: str,
                          tables: List[str],
                          check_names: List[str],
                          results: Dict[str, Any],
                          transformation_id: str = None):
        """Track a data quality check execution"""
        quality_record = {
            'id': check_id,
            'timestamp': datetime.now().isoformat(),
            'check_type': check_type,
            'tables': tables,
            'check_names': check_names,
            'results': results,
            'transformation_id': transformation_id
        }
        
        self.lineage_data['quality_checks'].append(quality_record)
        
        # Link to datasets
        for table in tables:
            if table in self.lineage_data['datasets']:
                self.lineage_data['datasets'][table]['quality_checks'].append(check_id)
    
    def save_lineage(self, format: str = 'yaml'):
        """Save lineage data to file"""
        if format == 'yaml':
            filename = 'lineage.yaml'
            filepath = os.path.join(self.lineage_dir, filename)
            with open(filepath, 'w') as f:
                yaml.dump(self.lineage_data, f, default_flow_style=False)
        elif format == 'json':
            filename = 'lineage.json'
            filepath = os.path.join(self.lineage_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(self.lineage_data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filepath
    
    def generate_lineage_graph(self) -> Dict[str, Any]:
        """Generate lineage graph structure"""
        nodes = []
        edges = []
        
        # Add dataset nodes
        for dataset_name, dataset_info in self.lineage_data['datasets'].items():
            nodes.append({
                'id': dataset_name,
                'type': 'dataset',
                'label': dataset_name,
                'metadata': dataset_info
            })
        
        # Add transformation nodes and edges
        for transformation in self.lineage_data['transformations']:
            trans_id = transformation['id']
            nodes.append({
                'id': trans_id,
                'type': 'transformation',
                'label': f"{transformation['engine_type']}: {trans_id}",
                'metadata': transformation
            })
            
            # Add edges from source to transformation
            for source in transformation['source_tables']:
                edges.append({
                    'source': source,
                    'target': trans_id,
                    'type': 'input'
                })
            
            # Add edges from transformation to target
            for target in transformation['target_tables']:
                edges.append({
                    'source': trans_id,
                    'target': target,
                    'type': 'output'
                })
        
        # Add quality check nodes and edges
        for check in self.lineage_data['quality_checks']:
            check_id = check['id']
            nodes.append({
                'id': check_id,
                'type': 'quality_check',
                'label': f"DQ: {check['check_type']}",
                'metadata': check
            })
            
            # Add edges from datasets to quality checks
            for table in check['tables']:
                edges.append({
                    'source': table,
                    'target': check_id,
                    'type': 'quality_check'
                })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def export_lineage_graph(self, format: str = 'json') -> str:
        """Export lineage graph to file"""
        graph = self.generate_lineage_graph()
        
        if format == 'json':
            filename = 'lineage_graph.json'
            filepath = os.path.join(self.lineage_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(graph, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filepath
    
    def get_transformation_history(self, dataset_name: str) -> List[Dict[str, Any]]:
        """Get transformation history for a dataset"""
        if dataset_name not in self.lineage_data['datasets']:
            return []
        
        transformation_ids = self.lineage_data['datasets'][dataset_name]['transformations']
        transformations = []
        
        for trans in self.lineage_data['transformations']:
            if trans['id'] in transformation_ids:
                transformations.append(trans)
        
        return sorted(transformations, key=lambda x: x['timestamp'])
    
    def get_quality_check_history(self, dataset_name: str) -> List[Dict[str, Any]]:
        """Get quality check history for a dataset"""
        if dataset_name not in self.lineage_data['datasets']:
            return []
        
        check_ids = self.lineage_data['datasets'][dataset_name]['quality_checks']
        checks = []
        
        for check in self.lineage_data['quality_checks']:
            if check['id'] in check_ids:
                checks.append(check)
        
        return sorted(checks, key=lambda x: x['timestamp'])
