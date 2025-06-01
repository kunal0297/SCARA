"""
Mutation Visualization System
Visualizes contract mutation history as DNA strands and logic trees
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import hashlib
import uuid
from dataclasses import dataclass
import numpy as np
import networkx as nx
from scipy.spatial import distance

@dataclass
class DNAStrand:
    id: str
    parent_id: Optional[str]
    code_hash: str
    mutation_type: str
    timestamp: datetime
    metrics: Dict[str, float]
    metadata: Dict[str, Any]

class MutationVisualizer:
    def __init__(self):
        self.dna_strands: List[DNAStrand] = []
        self.logic_tree = nx.DiGraph()
        
    def add_mutation(self,
                    parent_id: Optional[str],
                    code_hash: str,
                    mutation_type: str,
                    metrics: Dict[str, float],
                    metadata: Dict[str, Any]) -> str:
        """Add a new mutation to the visualization"""
        strand_id = str(uuid.uuid4())
        strand = DNAStrand(
            id=strand_id,
            parent_id=parent_id,
            code_hash=code_hash,
            mutation_type=mutation_type,
            timestamp=datetime.utcnow(),
            metrics=metrics,
            metadata=metadata
        )
        
        self.dna_strands.append(strand)
        self._update_logic_tree(strand)
        return strand_id
    
    def _update_logic_tree(self, strand: DNAStrand) -> None:
        """Update the logic tree with a new mutation"""
        self.logic_tree.add_node(
            strand.id,
            code_hash=strand.code_hash,
            mutation_type=strand.mutation_type,
            timestamp=strand.timestamp,
            metrics=strand.metrics
        )
        
        if strand.parent_id:
            self.logic_tree.add_edge(strand.parent_id, strand.id)
    
    def get_dna_sequence(self) -> List[Dict[str, Any]]:
        """Get the DNA sequence representation of mutations"""
        return [
            {
                'id': strand.id,
                'parent_id': strand.parent_id,
                'code_hash': strand.code_hash,
                'mutation_type': strand.mutation_type,
                'timestamp': strand.timestamp.isoformat(),
                'metrics': strand.metrics,
                'metadata': strand.metadata
            }
            for strand in sorted(self.dna_strands, key=lambda x: x.timestamp)
        ]
    
    def get_logic_tree(self) -> Dict[str, Any]:
        """Get the logic tree representation of mutations"""
        return nx.node_link_data(self.logic_tree)
    
    def calculate_mutation_similarity(self, strand_id_1: str, strand_id_2: str) -> float:
        """Calculate similarity between two mutations"""
        strand1 = next(s for s in self.dna_strands if s.id == strand_id_1)
        strand2 = next(s for s in self.dna_strands if s.id == strand_id_2)
        
        # Convert metrics to vectors for comparison
        metrics1 = np.array(list(strand1.metrics.values()))
        metrics2 = np.array(list(strand2.metrics.values()))
        
        # Calculate cosine similarity
        similarity = 1 - distance.cosine(metrics1, metrics2)
        return float(similarity)
    
    def get_mutation_path(self, start_id: str, end_id: str) -> List[str]:
        """Get the path between two mutations in the logic tree"""
        try:
            path = nx.shortest_path(self.logic_tree, start_id, end_id)
            return path
        except nx.NetworkXNoPath:
            return []
    
    def get_mutation_clusters(self, similarity_threshold: float = 0.8) -> List[List[str]]:
        """Get clusters of similar mutations"""
        # Create similarity matrix
        n = len(self.dna_strands)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                similarity = self.calculate_mutation_similarity(
                    self.dna_strands[i].id,
                    self.dna_strands[j].id
                )
                similarity_matrix[i, j] = similarity
                similarity_matrix[j, i] = similarity
        
        # Use hierarchical clustering
        from scipy.cluster.hierarchy import linkage, fcluster
        Z = linkage(similarity_matrix, method='complete')
        clusters = fcluster(Z, similarity_threshold, criterion='distance')
        
        # Group mutations by cluster
        cluster_dict = {}
        for i, cluster_id in enumerate(clusters):
            if cluster_id not in cluster_dict:
                cluster_dict[cluster_id] = []
            cluster_dict[cluster_id].append(self.dna_strands[i].id)
        
        return list(cluster_dict.values())
    
    def get_mutation_statistics(self) -> Dict[str, Any]:
        """Get statistics about the mutation history"""
        if not self.dna_strands:
            return {}
            
        mutation_types = {}
        metric_evolution = {}
        time_series = []
        
        for strand in self.dna_strands:
            # Count mutation types
            mutation_types[strand.mutation_type] = mutation_types.get(strand.mutation_type, 0) + 1
            
            # Track metric evolution
            for metric, value in strand.metrics.items():
                if metric not in metric_evolution:
                    metric_evolution[metric] = []
                metric_evolution[metric].append({
                    'timestamp': strand.timestamp.isoformat(),
                    'value': value
                })
            
            # Track time series
            time_series.append({
                'timestamp': strand.timestamp.isoformat(),
                'mutation_type': strand.mutation_type
            })
        
        return {
            'mutation_types': mutation_types,
            'metric_evolution': metric_evolution,
            'time_series': time_series,
            'total_mutations': len(self.dna_strands),
            'unique_mutation_types': len(mutation_types),
            'time_span': {
                'start': min(s.timestamp for s in self.dna_strands).isoformat(),
                'end': max(s.timestamp for s in self.dna_strands).isoformat()
            }
        }
    
    def export_visualization(self, format: str = 'json') -> str:
        """Export visualization data in specified format"""
        data = {
            'dna_sequence': self.get_dna_sequence(),
            'logic_tree': self.get_logic_tree(),
            'statistics': self.get_mutation_statistics()
        }
        
        if format == 'json':
            return json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_visualization(self, data: str, format: str = 'json') -> None:
        """Import visualization data from specified format"""
        if format == 'json':
            data_dict = json.loads(data)
            
            # Clear existing data
            self.dna_strands = []
            self.logic_tree = nx.DiGraph()
            
            # Import DNA sequence
            for strand_data in data_dict['dna_sequence']:
                strand = DNAStrand(
                    id=strand_data['id'],
                    parent_id=strand_data['parent_id'],
                    code_hash=strand_data['code_hash'],
                    mutation_type=strand_data['mutation_type'],
                    timestamp=datetime.fromisoformat(strand_data['timestamp']),
                    metrics=strand_data['metrics'],
                    metadata=strand_data['metadata']
                )
                self.dna_strands.append(strand)
                self._update_logic_tree(strand)
        else:
            raise ValueError(f"Unsupported format: {format}") 