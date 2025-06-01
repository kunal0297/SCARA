"""
Deployment script for testing the mutation system with MutableCounter
"""

import os
from web3 import Web3
from dotenv import load_dotenv
from scara.core.contracts.onchain_mutation import OnchainMutationManager
import json

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(os.getenv('RPC_URL')))
    if not w3.is_connected():
        raise Exception("Failed to connect to Ethereum node")
    
    # Initialize mutation manager
    manager = OnchainMutationManager(
        w3=w3,
        deployer_key=os.getenv('DEPLOYER_PRIVATE_KEY')
    )
    
    # Deploy MutableCounter
    contract_address, proxy_address = manager.deploy_and_initialize(
        contract_name="MutableCounter",
        initial_code=open("scara/contracts/MutableCounter.sol").read(),
        constructor_args=[0, 60],  # initialCount=0, initialDelay=60 seconds
        performance_thresholds={
            "gas_usage": 100000,
            "execution_time": 0.1
        },
        mutation_rules={
            "max_mutations_per_day": 10,
            "allowed_mutation_types": ["optimization", "feature_addition"],
            "safety_checks": True
        },
        is_upgradeable=True
    )
    
    print(f"Deployed MutableCounter:")
    print(f"Contract address: {contract_address}")
    print(f"Proxy address: {proxy_address}")
    
    # Get initial state
    state = manager.get_contract_state(contract_address)
    print("\nInitial contract state:")
    print(json.dumps(state, indent=2))
    
    # Propose and apply a mutation
    context = {
        "current_metrics": {
            "gas_usage": 50000,
            "execution_time": 0.05
        },
        "system_state": {
            "block_number": w3.eth.block_number,
            "gas_price": w3.eth.gas_price
        },
        "user_preferences": {
            "optimization_priority": "gas",
            "safety_level": "high"
        }
    }
    
    mutation = manager.propose_and_apply_mutation(
        contract_address,
        context
    )
    
    if mutation:
        print("\nApplied mutation:")
        print(json.dumps(mutation.__dict__, indent=2))
        
        # Get updated state
        state = manager.get_contract_state(contract_address)
        print("\nUpdated contract state:")
        print(json.dumps(state, indent=2))
        
        # Get mutation logs
        logs = manager.get_mutation_logs(contract_address)
        print("\nMutation logs:")
        print(json.dumps(logs, indent=2))
    else:
        print("\nNo mutation was applied")

if __name__ == "__main__":
    main() 