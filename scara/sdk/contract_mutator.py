"""
SCARA SDK - Contract Mutator
Handles contract-specific mutation operations and state management.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from web3 import Web3
from web3.contract import Contract
import json

from .scara_engine import SCARAEngine, SCARAMetrics, SCARAMutation

@dataclass
class ContractState:
    """Contract state information"""
    address: str
    abi: List[Dict]
    bytecode: str
    deployed_at: int
    last_mutation: Optional[SCARAMutation] = None
    current_metrics: Optional[SCARAMetrics] = None

class ContractMutator:
    def __init__(
        self,
        web3: Web3,
        contract_address: str,
        contract_abi: List[Dict],
        contract_bytecode: str
    ):
        """Initialize Contract Mutator"""
        self.web3 = web3
        self.contract = web3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )
        
        self.state = ContractState(
            address=contract_address,
            abi=contract_abi,
            bytecode=contract_bytecode,
            deployed_at=web3.eth.get_block('latest').timestamp
        )
        
        self.engine = SCARAEngine(
            web3=web3,
            contract_address=contract_address
        )
    
    async def deploy(self, constructor_args: Optional[List] = None) -> str:
        """
        Deploy a new instance of the contract
        
        Args:
            constructor_args: Optional constructor arguments
            
        Returns:
            Contract address
        """
        # Build contract
        contract = self.web3.eth.contract(
            abi=self.state.abi,
            bytecode=self.state.bytecode
        )
        
        # Deploy contract
        tx_hash = contract.constructor(
            *constructor_args if constructor_args else []
        ).transact()
        
        # Wait for deployment
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Update state
        self.state.address = tx_receipt.contractAddress
        self.state.deployed_at = tx_receipt.blockTimestamp
        
        return tx_receipt.contractAddress
    
    async def mutate_contract(
        self,
        mutation_type: Optional[str] = None,
        force: bool = False
    ) -> SCARAMutation:
        """
        Mutate the contract using SCARA engine
        
        Args:
            mutation_type: Optional specific mutation type
            force: Whether to force mutation
            
        Returns:
            SCARAMutation object
        """
        # Get current metrics
        self.state.current_metrics = await self.engine._get_current_metrics()
        
        # Generate and apply mutation
        mutation = await self.engine.mutate(
            mutation_type=mutation_type,
            force=force
        )
        
        # Update state
        self.state.last_mutation = mutation
        
        return mutation
    
    async def evaluate_contract(self) -> Dict:
        """
        Evaluate contract state and mutation potential
        
        Returns:
            Dict containing evaluation results
        """
        # Get current metrics
        self.state.current_metrics = await self.engine._get_current_metrics()
        
        # Evaluate
        return await self.engine.evaluate(self.state.current_metrics)
    
    def get_contract_state(self) -> ContractState:
        """Get current contract state"""
        return self.state
    
    def get_mutation_history(self) -> List[SCARAMutation]:
        """Get contract mutation history"""
        return self.engine.core_loop.get_mutation_history()
    
    def get_visualization_data(self) -> Dict:
        """Get contract visualization data"""
        return self.engine.visualize()
    
    def export_state(self, filepath: str):
        """Export contract state to file"""
        state_dict = {
            'address': self.state.address,
            'abi': self.state.abi,
            'bytecode': self.state.bytecode,
            'deployed_at': self.state.deployed_at,
            'last_mutation': self.state.last_mutation.__dict__ if self.state.last_mutation else None,
            'current_metrics': self.state.current_metrics.__dict__ if self.state.current_metrics else None
        }
        
        with open(filepath, 'w') as f:
            json.dump(state_dict, f, indent=2)
    
    @classmethod
    def from_state_file(cls, web3: Web3, filepath: str) -> 'ContractMutator':
        """Create ContractMutator from state file"""
        with open(filepath, 'r') as f:
            state_dict = json.load(f)
        
        mutator = cls(
            web3=web3,
            contract_address=state_dict['address'],
            contract_abi=state_dict['abi'],
            contract_bytecode=state_dict['bytecode']
        )
        
        mutator.state.deployed_at = state_dict['deployed_at']
        if state_dict['last_mutation']:
            mutator.state.last_mutation = SCARAMutation(**state_dict['last_mutation'])
        if state_dict['current_metrics']:
            mutator.state.current_metrics = SCARAMetrics(**state_dict['current_metrics'])
        
        return mutator 