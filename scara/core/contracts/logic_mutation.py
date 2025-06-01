"""
Logic Mutation Engine
Manages adaptive smart contract logic evolution
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import hashlib
import uuid
from dataclasses import dataclass
import numpy as np
from .ai_mutation import AIMutationManager, MutationSource

@dataclass
class MutationRecord:
    id: str
    original_code: str
    mutated_code: str
    performance_metrics: Dict[str, float]
    metadata: Dict[str, Any]
    created_at: datetime
    applied_at: Optional[datetime]

class LogicMutator:
    def __init__(self,
                 contract_id: str,
                 initial_code: str,
                 performance_thresholds: Dict[str, float],
                 mutation_rules: Dict[str, Any]):
        self.contract_id = contract_id
        self.current_code = initial_code
        self.performance_thresholds = performance_thresholds
        self.mutation_rules = mutation_rules
        self.mutation_history: List[MutationRecord] = []
        self.ai_manager = AIMutationManager()
        
    def evaluate_performance(self, metrics: Dict[str, float]) -> bool:
        """Evaluate if performance metrics meet thresholds"""
        for metric, threshold in self.performance_thresholds.items():
            if metric not in metrics or metrics[metric] < threshold:
                return False
        return True
        
    def generate_mutation(self, context: Dict[str, Any]) -> Optional[MutationRecord]:
        """Generate a new mutation using AI co-agents"""
        # Get AI-driven mutation proposal
        mutation_proposal = self.ai_manager.propose_mutation(
            self.current_code,
            context
        )
        
        if not mutation_proposal:
            return None
            
        # Apply mutation to code
        mutated_code = self._apply_mutation(
            self.current_code,
            mutation_proposal
        )
        
        # Create mutation record
        mutation = MutationRecord(
            id=str(uuid.uuid4()),
            original_code=self.current_code,
            mutated_code=mutated_code,
            performance_metrics={},  # Will be updated after evaluation
            metadata={
                'ai_source': mutation_proposal['source'],
                'dream_guidance': mutation_proposal['metadata']['dream_guidance'],
                'reasoning': mutation_proposal['reasoning'].__dict__,
                'proposal': mutation_proposal['proposal']
            },
            created_at=datetime.utcnow(),
            applied_at=None
        )
        
        self.mutation_history.append(mutation)
        return mutation
        
    def _apply_mutation(self,
                       current_code: str,
                       mutation_proposal: Dict[str, Any]) -> str:
        """Apply mutation to code based on AI proposal"""
        # TODO: Implement actual code mutation logic
        return current_code
        
    def apply_mutation(self, mutation_id: str) -> bool:
        """Apply a mutation to the current code"""
        mutation = next(
            (m for m in self.mutation_history if m.id == mutation_id),
            None
        )
        
        if not mutation:
            return False
            
        self.current_code = mutation.mutated_code
        mutation.applied_at = datetime.utcnow()
        return True
        
    def get_mutation_history(self) -> List[Dict[str, Any]]:
        """Get mutation history"""
        return [
            {
                'id': m.id,
                'original_code': m.original_code,
                'mutated_code': m.mutated_code,
                'performance_metrics': m.performance_metrics,
                'metadata': m.metadata,
                'created_at': m.created_at.isoformat(),
                'applied_at': m.applied_at.isoformat() if m.applied_at else None
            }
            for m in self.mutation_history
        ]
        
    def get_ai_insights(self) -> Dict[str, Any]:
        """Get insights from AI co-agents"""
        return self.ai_manager.get_ai_insights()

class MutationManager:
    def __init__(self):
        self.mutators: Dict[str, LogicMutator] = {}
        
    def create_mutator(self,
                      contract_id: str,
                      initial_code: str,
                      performance_thresholds: Dict[str, float],
                      mutation_rules: Dict[str, Any]) -> str:
        """Create a new logic mutator"""
        mutator = LogicMutator(
            contract_id,
            initial_code,
            performance_thresholds,
            mutation_rules
        )
        self.mutators[contract_id] = mutator
        return contract_id
        
    def evaluate_contract(self,
                         contract_id: str,
                         metrics: Dict[str, float]) -> bool:
        """Evaluate if a contract needs mutation"""
        if contract_id not in self.mutators:
            return False
            
        return self.mutators[contract_id].evaluate_performance(metrics)
        
    def generate_mutation(self,
                         contract_id: str,
                         context: Dict[str, Any]) -> Optional[MutationRecord]:
        """Generate a mutation for a contract"""
        if contract_id not in self.mutators:
            return None
            
        return self.mutators[contract_id].generate_mutation(context)
        
    def apply_mutation(self,
                      contract_id: str,
                      mutation_id: str) -> bool:
        """Apply a mutation to a contract"""
        if contract_id not in self.mutators:
            return False
            
        return self.mutators[contract_id].apply_mutation(mutation_id)
        
    def get_mutation_history(self,
                           contract_id: str) -> List[Dict[str, Any]]:
        """Get mutation history for a contract"""
        if contract_id not in self.mutators:
            return []
            
        return self.mutators[contract_id].get_mutation_history()
        
    def get_ai_insights(self,
                       contract_id: str) -> Dict[str, Any]:
        """Get AI insights for a contract"""
        if contract_id not in self.mutators:
            return {}
            
        return self.mutators[contract_id].get_ai_insights()
        
    def update_mutation_rules(self,
                            contract_id: str,
                            rules: Dict[str, Any]) -> bool:
        """Update mutation rules for a contract"""
        if contract_id not in self.mutators:
            return False
            
        self.mutators[contract_id].mutation_rules = rules
        return True
        
    def update_performance_thresholds(self,
                                    contract_id: str,
                                    thresholds: Dict[str, float]) -> bool:
        """Update performance thresholds for a contract"""
        if contract_id not in self.mutators:
            return False
            
        self.mutators[contract_id].performance_thresholds = thresholds
        return True 