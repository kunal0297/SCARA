"""
Onchain Personality and Behavior System
Manages unique user and AI agent personalities that influence contract mutations
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import hashlib
from dataclasses import dataclass
from enum import Enum
import numpy as np
from web3 import Web3
from .mutation_triggers import TriggerType, TriggerCondition
from .ai_mutation import AIMutationManager, MutationSource

class PersonalityTrait(Enum):
    CONSERVATIVE = "conservative"  # Prefers stable, proven mutations
    ADVENTUROUS = "adventurous"    # Willing to try risky mutations
    EFFICIENT = "efficient"        # Focuses on gas optimization
    SECURITY_FOCUSED = "security_focused"  # Prioritizes security
    INNOVATIVE = "innovative"      # Seeks novel solutions
    BALANCED = "balanced"         # Balanced approach to mutations

@dataclass
class PersonalityProfile:
    id: str
    traits: Dict[PersonalityTrait, float]  # Trait weights (0-1)
    memory_log: List[Dict[str, Any]]  # Historical actions and decisions
    intent_history: List[Dict[str, Any]]  # Recorded intentions
    created_at: datetime
    last_updated: datetime
    metadata: Dict[str, Any]

@dataclass
class BehaviorTrigger:
    id: str
    personality_id: str
    condition: TriggerCondition
    weight: float
    created_at: datetime
    last_triggered: Optional[datetime]
    metadata: Dict[str, Any]

class PersonalityManager:
    def __init__(self, web3: Web3):
        self.web3 = web3
        self.profiles: Dict[str, PersonalityProfile] = {}
        self.behavior_triggers: Dict[str, BehaviorTrigger] = {}
        self.ai_manager = AIMutationManager()
        
    def create_personality(self,
                          traits: Dict[PersonalityTrait, float],
                          metadata: Dict[str, Any] = None) -> PersonalityProfile:
        """Create a new personality profile"""
        profile_id = f"personality_{hashlib.sha256(str(traits).encode()).hexdigest()[:16]}"
        
        profile = PersonalityProfile(
            id=profile_id,
            traits=traits,
            memory_log=[],
            intent_history=[],
            created_at=datetime.utcnow(),
            last_updated=datetime.utcnow(),
            metadata=metadata or {}
        )
        
        self.profiles[profile_id] = profile
        return profile
        
    def record_memory(self,
                     personality_id: str,
                     action: str,
                     context: Dict[str, Any],
                     timestamp: Optional[datetime] = None) -> None:
        """Record a memory in the personality's log"""
        if personality_id not in self.profiles:
            raise ValueError(f"Personality {personality_id} not found")
            
        memory = {
            'action': action,
            'context': context,
            'timestamp': timestamp or datetime.utcnow()
        }
        
        self.profiles[personality_id].memory_log.append(memory)
        self.profiles[personality_id].last_updated = datetime.utcnow()
        
    def record_intent(self,
                     personality_id: str,
                     intent: str,
                     context: Dict[str, Any],
                     timestamp: Optional[datetime] = None) -> None:
        """Record an intent in the personality's history"""
        if personality_id not in self.profiles:
            raise ValueError(f"Personality {personality_id} not found")
            
        intent_record = {
            'intent': intent,
            'context': context,
            'timestamp': timestamp or datetime.utcnow()
        }
        
        self.profiles[personality_id].intent_history.append(intent_record)
        self.profiles[personality_id].last_updated = datetime.utcnow()
        
    def create_behavior_trigger(self,
                              personality_id: str,
                              condition: TriggerCondition,
                              weight: float = 1.0,
                              metadata: Dict[str, Any] = None) -> BehaviorTrigger:
        """Create a new behavior trigger for a personality"""
        if personality_id not in self.profiles:
            raise ValueError(f"Personality {personality_id} not found")
            
        trigger_id = f"trigger_{hashlib.sha256(str(condition).encode()).hexdigest()[:16]}"
        
        trigger = BehaviorTrigger(
            id=trigger_id,
            personality_id=personality_id,
            condition=condition,
            weight=weight,
            created_at=datetime.utcnow(),
            last_triggered=None,
            metadata=metadata or {}
        )
        
        self.behavior_triggers[trigger_id] = trigger
        return trigger
        
    def evaluate_triggers(self,
                         context: Dict[str, Any]) -> List[Tuple[BehaviorTrigger, float]]:
        """Evaluate all behavior triggers in the current context"""
        triggered = []
        
        for trigger in self.behavior_triggers.values():
            # Evaluate trigger condition
            if trigger.condition.evaluate(context):
                # Calculate trigger weight based on personality traits
                personality = self.profiles[trigger.personality_id]
                trait_weight = self._calculate_trait_weight(personality, trigger)
                
                # Apply trigger weight
                final_weight = trigger.weight * trait_weight
                
                triggered.append((trigger, final_weight))
                
                # Update last triggered timestamp
                trigger.last_triggered = datetime.utcnow()
        
        return triggered
        
    def _calculate_trait_weight(self,
                              personality: PersonalityProfile,
                              trigger: BehaviorTrigger) -> float:
        """Calculate weight based on personality traits"""
        # Default weight
        weight = 1.0
        
        # Adjust based on personality traits
        if trigger.condition.type == TriggerType.METRIC_THRESHOLD:
            if personality.traits.get(PersonalityTrait.EFFICIENT, 0) > 0.5:
                weight *= 1.2  # Boost efficiency-focused triggers
                
        elif trigger.condition.type == TriggerType.EVENT_PATTERN:
            if personality.traits.get(PersonalityTrait.ADVENTUROUS, 0) > 0.5:
                weight *= 1.2  # Boost pattern-based triggers
                
        elif trigger.condition.type == TriggerType.SIMULATION_RESULT:
            if personality.traits.get(PersonalityTrait.CONSERVATIVE, 0) > 0.5:
                weight *= 1.2  # Boost simulation-based triggers
                
        return weight
        
    def get_personality_insights(self,
                               personality_id: str) -> Dict[str, Any]:
        """Get insights about a personality's behavior"""
        if personality_id not in self.profiles:
            raise ValueError(f"Personality {personality_id} not found")
            
        profile = self.profiles[personality_id]
        
        # Analyze memory log
        memory_analysis = self._analyze_memory_log(profile.memory_log)
        
        # Analyze intent history
        intent_analysis = self._analyze_intent_history(profile.intent_history)
        
        # Calculate trait influence
        trait_influence = self._calculate_trait_influence(profile)
        
        return {
            'memory_analysis': memory_analysis,
            'intent_analysis': intent_analysis,
            'trait_influence': trait_influence,
            'last_updated': profile.last_updated.isoformat()
        }
        
    def _analyze_memory_log(self,
                           memory_log: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in memory log"""
        if not memory_log:
            return {}
            
        # Count action types
        action_counts = {}
        for memory in memory_log:
            action = memory['action']
            if action not in action_counts:
                action_counts[action] = 0
            action_counts[action] += 1
            
        # Calculate time-based patterns
        timestamps = [m['timestamp'] for m in memory_log]
        time_deltas = np.diff([t.timestamp() for t in timestamps])
        
        return {
            'total_memories': len(memory_log),
            'action_distribution': action_counts,
            'average_time_between_actions': float(np.mean(time_deltas)) if time_deltas else 0,
            'action_frequency': len(memory_log) / (timestamps[-1] - timestamps[0]).total_seconds() if len(timestamps) > 1 else 0
        }
        
    def _analyze_intent_history(self,
                               intent_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in intent history"""
        if not intent_history:
            return {}
            
        # Count intent types
        intent_counts = {}
        for record in intent_history:
            intent = record['intent']
            if intent not in intent_counts:
                intent_counts[intent] = 0
            intent_counts[intent] += 1
            
        # Calculate intent success rate
        successful_intents = sum(1 for r in intent_history if r.get('success', False))
        
        return {
            'total_intents': len(intent_history),
            'intent_distribution': intent_counts,
            'success_rate': successful_intents / len(intent_history) if intent_history else 0
        }
        
    def _calculate_trait_influence(self,
                                 profile: PersonalityProfile) -> Dict[str, float]:
        """Calculate the influence of each trait on behavior"""
        influence = {}
        
        for trait, weight in profile.traits.items():
            # Calculate influence based on trait weight and recent actions
            recent_memories = [m for m in profile.memory_log 
                             if (datetime.utcnow() - m['timestamp']).days < 7]
            
            if recent_memories:
                # Calculate trait-specific metrics
                if trait == PersonalityTrait.CONSERVATIVE:
                    influence[trait.value] = weight * (1 - len(recent_memories) / 100)
                elif trait == PersonalityTrait.ADVENTUROUS:
                    influence[trait.value] = weight * (len(recent_memories) / 100)
                elif trait == PersonalityTrait.EFFICIENT:
                    influence[trait.value] = weight * (1 - sum(1 for m in recent_memories 
                                                             if m.get('gas_used', 0) > 100000) / len(recent_memories))
                else:
                    influence[trait.value] = weight
            else:
                influence[trait.value] = weight
                
        return influence 