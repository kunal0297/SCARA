"""
Test script for the personality system
"""

import os
import json
from datetime import datetime, timedelta
from web3 import Web3
from scara.core.contracts.personality_system import (
    PersonalityManager,
    PersonalityTrait,
    TriggerType
)
from scara.core.contracts.mutation_triggers import TriggerCondition

def main():
    # Initialize Web3
    web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    
    # Initialize personality manager
    manager = PersonalityManager(web3)
    
    # Create a personality profile
    traits = {
        PersonalityTrait.CONSERVATIVE: 0.7,
        PersonalityTrait.EFFICIENT: 0.8,
        PersonalityTrait.SECURITY_FOCUSED: 0.9,
        PersonalityTrait.INNOVATIVE: 0.3,
        PersonalityTrait.ADVENTUROUS: 0.2,
        PersonalityTrait.BALANCED: 0.5
    }
    
    profile = manager.create_personality(
        traits=traits,
        metadata={
            'name': 'Security-First Agent',
            'description': 'Prioritizes security and stability in mutations'
        }
    )
    
    print(f"Created personality profile: {profile.id}")
    
    # Record some memories
    manager.record_memory(
        personality_id=profile.id,
        action='mutation_proposed',
        context={
            'mutation_type': 'security_enhancement',
            'gas_used': 50000,
            'success': True
        }
    )
    
    manager.record_memory(
        personality_id=profile.id,
        action='mutation_rejected',
        context={
            'mutation_type': 'feature_addition',
            'reason': 'security_risk',
            'gas_used': 150000
        }
    )
    
    # Record some intents
    manager.record_intent(
        personality_id=profile.id,
        intent='optimize_security',
        context={
            'target_contract': '0x123...',
            'priority': 'high'
        }
    )
    
    # Create behavior triggers
    gas_trigger = manager.create_behavior_trigger(
        personality_id=profile.id,
        condition=TriggerCondition(
            id='gas_threshold',
            type=TriggerType.METRIC_THRESHOLD,
            parameters={
                'metric': 'gas_usage',
                'threshold': 100000,
                'operator': '>'
            },
            weight=1.0
        ),
        weight=1.5,
        metadata={'description': 'Trigger on high gas usage'}
    )
    
    pattern_trigger = manager.create_behavior_trigger(
        personality_id=profile.id,
        condition=TriggerCondition(
            id='security_pattern',
            type=TriggerType.EVENT_PATTERN,
            parameters={
                'pattern': 'security_vulnerability',
                'window': 3600,  # 1 hour
                'threshold': 3
            },
            weight=1.0
        ),
        weight=2.0,
        metadata={'description': 'Trigger on security patterns'}
    )
    
    # Evaluate triggers
    context = {
        'gas_usage': 120000,
        'events': [
            {'type': 'security_vulnerability', 'timestamp': datetime.utcnow()},
            {'type': 'security_vulnerability', 'timestamp': datetime.utcnow() - timedelta(minutes=30)},
            {'type': 'security_vulnerability', 'timestamp': datetime.utcnow() - timedelta(minutes=45)}
        ]
    }
    
    triggered = manager.evaluate_triggers(context)
    
    print("\nTriggered Behaviors:")
    for trigger, weight in triggered:
        print(f"Trigger: {trigger.id}")
        print(f"Weight: {weight}")
        print(f"Last Triggered: {trigger.last_triggered}")
        print("---")
    
    # Get personality insights
    insights = manager.get_personality_insights(profile.id)
    
    print("\nPersonality Insights:")
    print(f"Last Updated: {insights['last_updated']}")
    
    print("\nMemory Analysis:")
    memory_analysis = insights['memory_analysis']
    print(f"Total Memories: {memory_analysis['total_memories']}")
    print("Action Distribution:")
    for action, count in memory_analysis['action_distribution'].items():
        print(f"  {action}: {count}")
    
    print("\nIntent Analysis:")
    intent_analysis = insights['intent_analysis']
    print(f"Total Intents: {intent_analysis['total_intents']}")
    print(f"Success Rate: {intent_analysis['success_rate']:.2%}")
    
    print("\nTrait Influence:")
    for trait, influence in insights['trait_influence'].items():
        print(f"  {trait}: {influence:.2f}")
    
    # Save insights to file
    with open("personality_insights.json", "w") as f:
        json.dump(insights, f, indent=2)
    
    print("\nInsights saved to personality_insights.json")

if __name__ == "__main__":
    main() 