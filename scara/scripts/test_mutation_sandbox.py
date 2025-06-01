"""
Test script for the mutation sandbox with MutableCounter
"""

import os
import json
from datetime import datetime
from scara.core.contracts.mutation_sandbox import MutationSandbox

def main():
    # Load contract code
    with open("scara/contracts/MutableCounter.sol", "r") as f:
        contract_code = f.read()
    
    # Initial state
    initial_state = {
        "count": 0,
        "increment_delay": 60,
        "last_increment": int(datetime.utcnow().timestamp())
    }
    
    # Performance thresholds
    performance_thresholds = {
        "gas_usage": 100000,
        "execution_time": 0.1,
        "success_rate": 0.95,
        "error_rate": 0.05,
        "memory_usage": 1024
    }
    
    # Mutation rules
    mutation_rules = {
        "max_mutations_per_day": 10,
        "allowed_mutation_types": [
            "optimization",
            "feature_addition",
            "gas_optimization",
            "security_enhancement"
        ],
        "safety_checks": True,
        "min_success_rate": 0.95,
        "max_gas_increase": 0.1  # 10% max gas increase
    }
    
    # Initialize sandbox
    sandbox = MutationSandbox(
        contract_code=contract_code,
        initial_state=initial_state,
        performance_thresholds=performance_thresholds,
        mutation_rules=mutation_rules
    )
    
    # Initial context
    context = {
        "current_metrics": {
            "gas_usage": 50000,
            "execution_time": 0.05,
            "success_rate": 1.0,
            "error_rate": 0.0,
            "memory_usage": 512
        },
        "system_state": {
            "block_number": 1,
            "gas_price": 20
        },
        "user_preferences": {
            "optimization_priority": "gas",
            "safety_level": "high"
        }
    }
    
    print("Starting mutation simulation cycle...")
    
    # Run mutation cycle
    results = sandbox.simulate_mutation_cycle(
        context=context,
        num_iterations=5
    )
    
    # Print results
    print("\nSimulation Results:")
    for i, result in enumerate(results, 1):
        print(f"\nMutation {i}:")
        print(f"Success: {result.success}")
        if not result.success:
            print(f"Error: {result.error_message}")
        print("Performance Metrics:")
        print(f"  Gas Usage Delta: {result.metrics.gas_usage:+.2f}")
        print(f"  Execution Time Delta: {result.metrics.execution_time:+.2f}")
        print(f"  Success Rate: {result.metrics.success_rate:.2%}")
        print(f"  Error Rate: {result.metrics.error_rate:.2%}")
        print(f"  Memory Usage Delta: {result.metrics.memory_usage:+.2f}")
    
    # Get simulation report
    report = sandbox.get_simulation_report()
    
    # Save report
    with open("mutation_simulation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\nSimulation report saved to mutation_simulation_report.json")
    
    # Print key insights
    print("\nKey Insights:")
    impact = report['mutation_impact']
    print(f"Total Mutations: {impact['total_mutations']}")
    print(f"Successful Mutations: {impact['successful_mutations']}")
    print(f"Failed Mutations: {impact['failed_mutations']}")
    print("\nAverage Improvements:")
    for metric, value in impact['average_improvements'].items():
        print(f"  {metric}: {value:+.2f}")
    
    print("\nMutation Types:")
    for mtype, count in impact['mutation_types'].items():
        print(f"  {mtype}: {count}")

if __name__ == "__main__":
    main() 