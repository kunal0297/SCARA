"""
SCARA System Test Script
Verifies all major components of the SCARA system.
"""

import os
import sys
import asyncio
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.contracts.logic_mutation import LogicMutator
from core.contracts.ai_mutation import AIMutationManager, MutationSource
from core.contracts.mutation_dao import MutationDAO
from core.contracts.lore_engine import LoreEngine, Event
from core.contracts.onchain_mutation import OnchainMutationManager
from core.contracts.mutation_sandbox import MutationSandbox

async def test_system():
    """Run comprehensive system tests"""
    print("\n=== SCARA System Test ===")
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Web3
    web3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL')))
    if not web3.is_connected():
        print("❌ Failed to connect to Ethereum network")
        return
    
    print("✅ Connected to Ethereum network")
    
    # Test components
    await test_logic_mutation()
    await test_ai_mutation()
    await test_mutation_dao(web3)
    await test_lore_engine()
    await test_onchain_mutation(web3)
    await test_mutation_sandbox()
    
    print("\n=== All Tests Completed ===")

async def test_logic_mutation():
    """Test logic mutation system"""
    print("\nTesting Logic Mutation System...")
    
    try:
        # Initialize mutator
        mutator = LogicMutator(
            performance_thresholds={
                'gas_usage': 1000000,
                'execution_time': 1000,
                'success_rate': 0.95,
                'error_rate': 0.05,
                'memory_usage': 1000000
            },
            mutation_rules={
                'max_mutations_per_day': 10,
                'allowed_mutation_types': ['optimization', 'security', 'feature'],
                'safety_checks': True,
                'min_success_rate': 0.95,
                'max_gas_increase': 0.1
            }
        )
        
        # Test mutation generation
        context = {
            'current_metrics': {
                'gas_usage': 1500000,
                'execution_time': 1500,
                'success_rate': 0.92,
                'error_rate': 0.08,
                'memory_usage': 1200000
            },
            'system_state': {
                'last_mutation': int(datetime.now().timestamp()) - 86400,
                'total_mutations': 5,
                'successful_mutations': 4
            },
            'user_preferences': {
                'optimization_priority': 0.8,
                'security_priority': 0.9,
                'feature_priority': 0.6
            }
        }
        
        mutation = await mutator.generate_mutation(context)
        print(f"✅ Generated mutation: {mutation.mutation_type}")
        
        # Test mutation application
        result = await mutator.apply_mutation(mutation)
        print(f"✅ Applied mutation: {result.success}")
        
        # Test history retrieval
        history = await mutator.get_mutation_history()
        print(f"✅ Retrieved {len(history)} mutation records")
        
    except Exception as e:
        print(f"❌ Logic Mutation Test Failed: {str(e)}")

async def test_ai_mutation():
    """Test AI mutation system"""
    print("\nTesting AI Mutation System...")
    
    try:
        # Initialize AI mutation manager
        ai_manager = AIMutationManager()
        
        # Test dream seed generation
        dream_seed = await ai_manager.alith.generate_dream_seed()
        print(f"✅ Generated dream seed: {dream_seed.emotion}")
        
        # Test mutation proposal
        proposal = await ai_manager.propose_mutation(
            dream_seed,
            "Test mutation proposal"
        )
        print(f"✅ Generated mutation proposal: {proposal.mutation_type}")
        
        # Test reasoning
        reasoning = await ai_manager.hyperion.analyze_mutation(proposal)
        print(f"✅ Generated reasoning: {reasoning.reasoning_type}")
        
    except Exception as e:
        print(f"❌ AI Mutation Test Failed: {str(e)}")

async def test_mutation_dao(web3):
    """Test mutation DAO"""
    print("\nTesting Mutation DAO...")
    
    try:
        # Initialize DAO
        dao = MutationDAO(
            web3=web3,
            contract_address=os.getenv('DAO_CONTRACT_ADDRESS'),
            voting_period=86400,
            quorum=0.1,
            threshold=0.6
        )
        
        # Test proposal creation
        proposal_id = await dao.propose_mutation(
            mutation_id="test_mutation",
            description="Test proposal",
            proposer=os.getenv('TEST_ADDRESS')
        )
        print(f"✅ Created proposal: {proposal_id}")
        
        # Test voting
        await dao.vote(
            proposal_id=proposal_id,
            voter=os.getenv('TEST_ADDRESS'),
            support=True,
            reason="Test vote"
        )
        print("✅ Cast vote")
        
        # Test proposal retrieval
        proposal = dao.get_proposal(proposal_id)
        print(f"✅ Retrieved proposal: {proposal.description}")
        
    except Exception as e:
        print(f"❌ Mutation DAO Test Failed: {str(e)}")

async def test_lore_engine():
    """Test lore engine"""
    print("\nTesting Lore Engine...")
    
    try:
        # Initialize lore engine
        lore = LoreEngine(narrative_style="epic")
        
        # Create test event
        event = Event(
            event_type="MutationApplied",
            timestamp=int(datetime.now().timestamp()),
            data={
                "mutation_type": "optimization",
                "impact_level": "high",
                "description": "Test mutation"
            },
            block_number=1,
            transaction_hash="0x123"
        )
        
        # Test event addition
        lore.add_event(event)
        print("✅ Added event")
        
        # Test lore entry generation
        entries = lore.get_lore_entries(event_type="MutationApplied")
        print(f"✅ Generated {len(entries)} lore entries")
        
        # Test event chain
        chain = lore.get_event_chain("0x123")
        print(f"✅ Retrieved event chain of length {len(chain)}")
        
    except Exception as e:
        print(f"❌ Lore Engine Test Failed: {str(e)}")

async def test_onchain_mutation(web3):
    """Test onchain mutation system"""
    print("\nTesting Onchain Mutation System...")
    
    try:
        # Initialize onchain mutation manager
        manager = OnchainMutationManager(web3)
        
        # Test contract deployment
        contract = await manager.deploy_contract(
            contract_code=open("contracts/MutableCounter.sol").read(),
            constructor_args=[],
            is_upgradeable=True
        )
        print(f"✅ Deployed contract: {contract.address}")
        
        # Test mutation application
        result = await manager.mutate_contract(
            contract_address=contract.address,
            mutation_type="optimization",
            mutation_data={"target": "increment"}
        )
        print(f"✅ Applied mutation: {result.success}")
        
    except Exception as e:
        print(f"❌ Onchain Mutation Test Failed: {str(e)}")

async def test_mutation_sandbox():
    """Test mutation sandbox"""
    print("\nTesting Mutation Sandbox...")
    
    try:
        # Initialize sandbox
        sandbox = MutationSandbox(
            contract_code=open("contracts/MutableCounter.sol").read(),
            initial_state={
                "count": 0,
                "increment_delay": 1,
                "last_increment": 0
            }
        )
        
        # Test simulation
        result = await sandbox.run_simulation_cycle(
            iterations=5,
            context={
                "current_metrics": {
                    "gas_usage": 100000,
                    "execution_time": 100,
                    "success_rate": 0.95
                }
            }
        )
        print(f"✅ Completed simulation: {result.success}")
        
        # Test report generation
        report = await sandbox.generate_report()
        print(f"✅ Generated report with {len(report.mutations)} mutations")
        
    except Exception as e:
        print(f"❌ Mutation Sandbox Test Failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_system()) 