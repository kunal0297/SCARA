"""
SCARA SDK - Core Engine
Main interface for interacting with the SCARA mutation system.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from web3 import Web3
from web3.contract import Contract

from ..core.contracts.core_loop import CoreLoop
from ..core.contracts.logic_mutation import LogicMutator
from ..core.contracts.mutation_triggers import MutationTrigger
from ..core.contracts.mutation_sandbox import MutationSandbox
from ..core.contracts.ai_mutation import AIMutationManager

@dataclass
class SCARAMetrics:
    """System performance metrics"""
    gas_usage: int
    execution_time: float
    success_rate: float
    error_rate: float
    memory_usage: int

@dataclass
class SCARAMutation:
    """Mutation information"""
    mutation_id: str
    type: str
    original_code: str
    mutated_code: str
    metrics: SCARAMetrics
    timestamp: int
    status: str

class SCARAEngine:
    def __init__(
        self,
        web3: Web3,
        contract_address: str,
        evaluation_interval: int = 100,
        min_blocks_between_mutations: int = 50,
        ai_intervention_threshold: float = 0.8
    ):
        """Initialize SCARA Engine"""
        self.web3 = web3
        self.contract_address = contract_address
        
        # Initialize components
        self.core_loop = CoreLoop(
            web3=web3,
            contract_address=contract_address,
            evaluation_interval=evaluation_interval,
            min_blocks_between_mutations=min_blocks_between_mutations,
            ai_intervention_threshold=ai_intervention_threshold
        )
        
        self.mutator = LogicMutator()
        self.trigger = MutationTrigger()
        self.sandbox = MutationSandbox()
        self.ai_manager = AIMutationManager()
    
    async def evaluate(self, metrics: Optional[SCARAMetrics] = None) -> Dict:
        """
        Evaluate current system state and determine if mutation is needed
        
        Args:
            metrics: Optional metrics to override current system metrics
            
        Returns:
            Dict containing evaluation results
        """
        if metrics is None:
            metrics = await self._get_current_metrics()
        
        should_mutate = self.trigger.should_trigger(metrics.__dict__)
        
        return {
            'should_mutate': should_mutate,
            'metrics': metrics,
            'trigger_conditions': self.trigger.get_conditions(),
            'ai_recommendation': await self.ai_manager.get_recommendation(metrics.__dict__)
        }
    
    async def mutate(
        self,
        mutation_type: Optional[str] = None,
        force: bool = False
    ) -> SCARAMutation:
        """
        Generate and apply a mutation
        
        Args:
            mutation_type: Optional specific mutation type to apply
            force: Whether to force mutation without evaluation
            
        Returns:
            SCARAMutation object containing mutation details
        """
        if not force:
            evaluation = await self.evaluate()
            if not evaluation['should_mutate']:
                raise Exception("Mutation not recommended based on current state")
        
        # Generate mutation
        mutation = self.mutator.generate_mutation(
            metrics=await self._get_current_metrics().__dict__,
            mutation_type=mutation_type
        )
        
        # Simulate mutation
        simulation = self.sandbox.simulate_mutation(mutation)
        
        if not simulation.success:
            raise Exception("Mutation simulation failed")
        
        # Apply mutation
        await self.core_loop._apply_mutation(mutation)
        
        return SCARAMutation(
            mutation_id=mutation.mutation_id,
            type=mutation.type,
            original_code=mutation.original_code,
            mutated_code=mutation.mutated_code,
            metrics=SCARAMetrics(**simulation.metrics),
            timestamp=mutation.timestamp,
            status='applied'
        )
    
    async def visualize(self) -> Dict:
        """
        Get visualization data for the mutation system
        
        Returns:
            Dict containing visualization data
        """
        return {
            'dna_sequence': await self._get_dna_sequence(),
            'logic_tree': await self._get_logic_tree(),
            'mutation_history': await self._get_mutation_history(),
            'simulation_results': await self._get_simulation_results()
        }
    
    async def _get_current_metrics(self) -> SCARAMetrics:
        """Get current system metrics"""
        metrics = await self.core_loop._get_current_metrics()
        return SCARAMetrics(**metrics)
    
    async def _get_dna_sequence(self) -> List[Dict]:
        """Get DNA sequence visualization data"""
        return await self.core_loop.fetchDnaSequence()
    
    async def _get_logic_tree(self) -> Dict:
        """Get logic tree visualization data"""
        return await self.core_loop.fetchLogicTree()
    
    async def _get_mutation_history(self) -> List[Dict]:
        """Get mutation history"""
        return await self.core_loop.fetchTriggerHistory()
    
    async def _get_simulation_results(self) -> Dict:
        """Get simulation results"""
        return await self.core_loop.fetchSimulationResults()
    
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        return self.core_loop.get_statistics()
    
    def get_state(self) -> Dict:
        """Get current system state"""
        return self.core_loop.get_state().__dict__ 