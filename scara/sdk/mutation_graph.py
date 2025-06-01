"""
SCARA SDK - Mutation Graph
Handles mutation visualization and analysis through graph structures.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import networkx as nx
import numpy as np
from datetime import datetime

from .scara_engine import SCARAMutation

@dataclass
class GraphNode:
    """Node in the mutation graph"""
    mutation_id: str
    type: str
    timestamp: int
    metrics: Dict
    parent_id: Optional[str] = None

@dataclass
class GraphEdge:
    """Edge in the mutation graph"""
    source: str
    target: str
    weight: float
    similarity: float

class MutationGraph:
    def __init__(self):
        """Initialize Mutation Graph"""
        self.graph = nx.DiGraph()
        self.metrics_history = []
    
    def add_mutation(self, mutation: SCARAMutation):
        """
        Add a mutation to the graph
        
        Args:
            mutation: SCARAMutation object
        """
        # Create node
        node = GraphNode(
            mutation_id=mutation.mutation_id,
            type=mutation.type,
            timestamp=mutation.timestamp,
            metrics=mutation.metrics.__dict__
        )
        
        # Add node to graph
        self.graph.add_node(
            mutation.mutation_id,
            **node.__dict__
        )
        
        # Add edge if parent exists
        if mutation.parent_id:
            self.graph.add_edge(
                mutation.parent_id,
                mutation.mutation_id,
                weight=1.0,
                similarity=self._calculate_similarity(
                    self.graph.nodes[mutation.parent_id]['metrics'],
                    mutation.metrics.__dict__
                )
            )
        
        # Update metrics history
        self.metrics_history.append({
            'timestamp': mutation.timestamp,
            'metrics': mutation.metrics.__dict__
        })
    
    def get_mutation_path(self, start_id: str, end_id: str) -> List[str]:
        """
        Get path between two mutations
        
        Args:
            start_id: Starting mutation ID
            end_id: Ending mutation ID
            
        Returns:
            List of mutation IDs in path
        """
        try:
            return nx.shortest_path(self.graph, start_id, end_id)
        except nx.NetworkXNoPath:
            return []
    
    def get_mutation_clusters(self, threshold: float = 0.8) -> List[List[str]]:
        """
        Get clusters of similar mutations
        
        Args:
            threshold: Similarity threshold for clustering
            
        Returns:
            List of mutation ID clusters
        """
        # Create similarity matrix
        nodes = list(self.graph.nodes())
        n = len(nodes)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                similarity = self._calculate_similarity(
                    self.graph.nodes[nodes[i]]['metrics'],
                    self.graph.nodes[nodes[j]]['metrics']
                )
                similarity_matrix[i, j] = similarity_matrix[j, i] = similarity
        
        # Perform hierarchical clustering
        from scipy.cluster.hierarchy import linkage, fcluster
        Z = linkage(similarity_matrix, method='complete')
        clusters = fcluster(Z, threshold, criterion='distance')
        
        # Group mutations by cluster
        mutation_clusters = {}
        for i, cluster_id in enumerate(clusters):
            if cluster_id not in mutation_clusters:
                mutation_clusters[cluster_id] = []
            mutation_clusters[cluster_id].append(nodes[i])
        
        return list(mutation_clusters.values())
    
    def get_metrics_trend(self) -> Dict:
        """
        Get metrics trend over time
        
        Returns:
            Dict containing metrics trends
        """
        if not self.metrics_history:
            return {}
        
        # Calculate trends
        metrics = ['gas_usage', 'execution_time', 'success_rate', 'error_rate', 'memory_usage']
        trends = {}
        
        for metric in metrics:
            values = [h['metrics'][metric] for h in self.metrics_history]
            trends[metric] = {
                'min': min(values),
                'max': max(values),
                'mean': np.mean(values),
                'std': np.std(values),
                'trend': np.polyfit(range(len(values)), values, 1)[0]
            }
        
        return trends
    
    def export_graph(self, filepath: str):
        """
        Export graph to file
        
        Args:
            filepath: Path to export file
        """
        nx.write_graphml(self.graph, filepath)
    
    @classmethod
    def from_graph_file(cls, filepath: str) -> 'MutationGraph':
        """
        Create MutationGraph from file
        
        Args:
            filepath: Path to graph file
            
        Returns:
            MutationGraph instance
        """
        graph = cls()
        graph.graph = nx.read_graphml(filepath)
        return graph
    
    def _calculate_similarity(self, metrics1: Dict, metrics2: Dict) -> float:
        """
        Calculate similarity between two sets of metrics
        
        Args:
            metrics1: First set of metrics
            metrics2: Second set of metrics
            
        Returns:
            Similarity score between 0 and 1
        """
        # Normalize metrics
        def normalize(m):
            return {
                'gas_usage': m['gas_usage'] / 1e6,  # Convert to millions
                'execution_time': m['execution_time'] / 1000,  # Convert to seconds
                'success_rate': m['success_rate'],
                'error_rate': m['error_rate'],
                'memory_usage': m['memory_usage'] / 1e6  # Convert to MB
            }
        
        m1 = normalize(metrics1)
        m2 = normalize(metrics2)
        
        # Calculate weighted Euclidean distance
        weights = {
            'gas_usage': 0.3,
            'execution_time': 0.2,
            'success_rate': 0.3,
            'error_rate': 0.1,
            'memory_usage': 0.1
        }
        
        distance = 0
        for metric, weight in weights.items():
            distance += weight * (m1[metric] - m2[metric]) ** 2
        
        # Convert distance to similarity
        return 1 / (1 + np.sqrt(distance)) 