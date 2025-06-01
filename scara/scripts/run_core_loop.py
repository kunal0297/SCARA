"""
SCARA Core Loop Runner
Runs the autonomous mutation system with configurable parameters.
"""

import asyncio
import argparse
from web3 import Web3
from scara.core.contracts.core_loop import CoreLoop

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run SCARA Core Loop')
    parser.add_argument('--rpc-url', required=True, help='Ethereum RPC URL')
    parser.add_argument('--contract-address', required=True, help='Contract address')
    parser.add_argument('--evaluation-interval', type=int, default=100,
                      help='Number of blocks between evaluations')
    parser.add_argument('--min-blocks-between-mutations', type=int, default=50,
                      help='Minimum blocks between mutations')
    parser.add_argument('--ai-intervention-threshold', type=float, default=0.8,
                      help='Threshold for AI intervention')
    
    args = parser.parse_args()
    
    # Initialize Web3
    web3 = Web3(Web3.HTTPProvider(args.rpc_url))
    if not web3.is_connected():
        raise Exception("Failed to connect to Ethereum node")
    
    # Initialize core loop
    core_loop = CoreLoop(
        web3=web3,
        contract_address=args.contract_address,
        evaluation_interval=args.evaluation_interval,
        min_blocks_between_mutations=args.min_blocks_between_mutations,
        ai_intervention_threshold=args.ai_intervention_threshold
    )
    
    print("SCARA Core Loop started")
    print(f"Contract address: {args.contract_address}")
    print(f"Evaluation interval: {args.evaluation_interval} blocks")
    print(f"Min blocks between mutations: {args.min_blocks_between_mutations}")
    print(f"AI intervention threshold: {args.ai_intervention_threshold}")
    
    try:
        # Keep the script running
        while True:
            # Print statistics every minute
            stats = core_loop.get_statistics()
            print("\nCurrent Statistics:")
            print(f"Total mutations: {stats['total_mutations']}")
            print(f"Successful mutations: {stats['successful_mutations']}")
            print(f"Failed mutations: {stats['failed_mutations']}")
            print(f"Success rate: {stats['success_rate']:.2%}")
            print(f"Blocks since last mutation: {stats['blocks_since_last_mutation']}")
            
            await asyncio.sleep(60)
            
    except KeyboardInterrupt:
        print("\nShutting down SCARA Core Loop...")
    except Exception as e:
        print(f"Error in core loop: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 