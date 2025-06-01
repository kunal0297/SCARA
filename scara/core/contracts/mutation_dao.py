"""
SCARA Mutation DAO
On-chain governance system for mutation decisions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from web3 import Web3
from web3.contract import Contract

@dataclass
class MutationProposal:
    """Mutation proposal for DAO voting"""
    proposal_id: str
    mutation_id: str
    proposer: str
    description: str
    created_at: int
    voting_period: int
    votes_for: int = 0
    votes_against: int = 0
    executed: bool = False

class MutationDAO:
    def __init__(
        self,
        web3: Web3,
        contract_address: str,
        voting_period: int = 86400,  # 24 hours
        quorum: float = 0.1,  # 10% of total supply
        threshold: float = 0.6  # 60% approval required
    ):
        """Initialize Mutation DAO"""
        self.web3 = web3
        self.contract_address = contract_address
        self.voting_period = voting_period
        self.quorum = quorum
        self.threshold = threshold
        
        # Load contract
        self.contract = web3.eth.contract(
            address=contract_address,
            abi=self._get_contract_abi()
        )
        
        # Track proposals
        self.proposals: Dict[str, MutationProposal] = {}
    
    async def propose_mutation(
        self,
        mutation_id: str,
        description: str,
        proposer: str
    ) -> str:
        """
        Create a new mutation proposal
        
        Args:
            mutation_id: ID of the mutation to vote on
            description: Proposal description
            proposer: Address of the proposer
            
        Returns:
            Proposal ID
        """
        # Create proposal
        proposal = MutationProposal(
            proposal_id=self._generate_proposal_id(),
            mutation_id=mutation_id,
            proposer=proposer,
            description=description,
            created_at=int(datetime.now().timestamp()),
            voting_period=self.voting_period
        )
        
        # Submit to contract
        tx = await self.contract.functions.createProposal(
            mutation_id,
            description,
            self.voting_period
        ).transact({'from': proposer})
        
        # Wait for transaction
        receipt = await self.web3.eth.wait_for_transaction_receipt(tx)
        
        # Store proposal
        self.proposals[proposal.proposal_id] = proposal
        
        return proposal.proposal_id
    
    async def vote(
        self,
        proposal_id: str,
        voter: str,
        support: bool,
        reason: Optional[str] = None
    ):
        """
        Vote on a mutation proposal
        
        Args:
            proposal_id: ID of the proposal
            voter: Address of the voter
            support: Whether to support the proposal
            reason: Optional reason for the vote
        """
        # Submit vote
        tx = await self.contract.functions.castVote(
            proposal_id,
            support,
            reason if reason else ""
        ).transact({'from': voter})
        
        # Wait for transaction
        await self.web3.eth.wait_for_transaction_receipt(tx)
        
        # Update proposal
        proposal = self.proposals[proposal_id]
        if support:
            proposal.votes_for += 1
        else:
            proposal.votes_against += 1
    
    async def execute_proposal(self, proposal_id: str, executor: str):
        """
        Execute a successful proposal
        
        Args:
            proposal_id: ID of the proposal
            executor: Address of the executor
        """
        proposal = self.proposals[proposal_id]
        
        # Check if proposal can be executed
        if not self._can_execute(proposal):
            raise Exception("Proposal cannot be executed")
        
        # Execute proposal
        tx = await self.contract.functions.executeProposal(
            proposal_id
        ).transact({'from': executor})
        
        # Wait for transaction
        await self.web3.eth.wait_for_transaction_receipt(tx)
        
        # Update proposal
        proposal.executed = True
    
    def get_proposal(self, proposal_id: str) -> MutationProposal:
        """Get proposal details"""
        return self.proposals[proposal_id]
    
    def get_active_proposals(self) -> List[MutationProposal]:
        """Get list of active proposals"""
        current_time = int(datetime.now().timestamp())
        return [
            p for p in self.proposals.values()
            if not p.executed and
            current_time < p.created_at + p.voting_period
        ]
    
    def _can_execute(self, proposal: MutationProposal) -> bool:
        """Check if proposal can be executed"""
        current_time = int(datetime.now().timestamp())
        if current_time < proposal.created_at + proposal.voting_period:
            return False
        
        total_votes = proposal.votes_for + proposal.votes_against
        if total_votes < self.quorum:
            return False
        
        approval_ratio = proposal.votes_for / total_votes
        return approval_ratio >= self.threshold
    
    def _generate_proposal_id(self) -> str:
        """Generate unique proposal ID"""
        return f"prop_{int(datetime.now().timestamp())}"
    
    def _get_contract_abi(self) -> List[Dict]:
        """Get contract ABI"""
        # Load ABI from file or configuration
        # This is a placeholder - implement actual ABI loading
        return [] 