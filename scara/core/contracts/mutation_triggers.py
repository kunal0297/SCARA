"""
Mutation Triggers System
Manages contract mutation triggers based on on-chain metrics and simulation events
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import json
import hashlib
import uuid
from dataclasses import dataclass
import numpy as np
from enum import Enum

class TriggerType(Enum):
    METRIC_THRESHOLD = "metric_threshold"
    EVENT_PATTERN = "event_pattern"
    SIMULATION_RESULT = "simulation_result"
    TIME_BASED = "time_based"
    COMPOSITE = "composite"

@dataclass
class TriggerCondition:
    id: str
    type: TriggerType
    parameters: Dict[str, Any]
    weight: float
    created_at: datetime
    last_triggered: Optional[datetime]
    metadata: Dict[str, Any]

class MetricTrigger:
    def __init__(self,
                 metric_name: str,
                 threshold: float,
                 comparison: str,
                 weight: float = 1.0):
        self.metric_name = metric_name
        self.threshold = threshold
        self.comparison = comparison
        self.weight = weight
        
    def evaluate(self, metrics: Dict[str, float]) -> bool:
        if self.metric_name not in metrics:
            return False
            
        value = metrics[self.metric_name]
        if self.comparison == ">":
            return value > self.threshold
        elif self.comparison == "<":
            return value < self.threshold
        elif self.comparison == ">=":
            return value >= self.threshold
        elif self.comparison == "<=":
            return value <= self.threshold
        elif self.comparison == "==":
            return abs(value - self.threshold) < 1e-6
        return False

class EventPatternTrigger:
    def __init__(self,
                 pattern: Dict[str, Any],
                 time_window: float,
                 weight: float = 1.0):
        self.pattern = pattern
        self.time_window = time_window
        self.weight = weight
        self.event_history: List[Dict[str, Any]] = []
        
    def add_event(self, event: Dict[str, Any]) -> None:
        self.event_history.append(event)
        # Remove old events outside time window
        current_time = datetime.utcnow()
        self.event_history = [
            e for e in self.event_history
            if (current_time - e['timestamp']).total_seconds() <= self.time_window
        ]
        
    def evaluate(self) -> bool:
        # TODO: Implement pattern matching logic
        return False

class SimulationTrigger:
    def __init__(self,
                 simulation_type: str,
                 success_threshold: float,
                 weight: float = 1.0):
        self.simulation_type = simulation_type
        self.success_threshold = success_threshold
        self.weight = weight
        
    def evaluate(self, simulation_results: Dict[str, Any]) -> bool:
        if self.simulation_type not in simulation_results:
            return False
            
        result = simulation_results[self.simulation_type]
        return result['success_rate'] >= self.success_threshold

class CompositeTrigger:
    def __init__(self, triggers: List[Any], operator: str = "AND"):
        self.triggers = triggers
        self.operator = operator
        
    def evaluate(self, context: Dict[str, Any]) -> bool:
        results = [t.evaluate(context) for t in self.triggers]
        if self.operator == "AND":
            return all(results)
        elif self.operator == "OR":
            return any(results)
        return False

class TriggerManager:
    def __init__(self):
        self.triggers: Dict[str, TriggerCondition] = {}
        self.metric_triggers: Dict[str, MetricTrigger] = {}
        self.event_triggers: Dict[str, EventPatternTrigger] = {}
        self.simulation_triggers: Dict[str, SimulationTrigger] = {}
        self.composite_triggers: Dict[str, CompositeTrigger] = {}
        
    def add_metric_trigger(self,
                          metric_name: str,
                          threshold: float,
                          comparison: str,
                          weight: float = 1.0) -> str:
        """Add a new metric-based trigger"""
        trigger_id = str(uuid.uuid4())
        trigger = MetricTrigger(metric_name, threshold, comparison, weight)
        self.metric_triggers[trigger_id] = trigger
        
        condition = TriggerCondition(
            id=trigger_id,
            type=TriggerType.METRIC_THRESHOLD,
            parameters={
                'metric_name': metric_name,
                'threshold': threshold,
                'comparison': comparison
            },
            weight=weight,
            created_at=datetime.utcnow(),
            last_triggered=None,
            metadata={}
        )
        
        self.triggers[trigger_id] = condition
        return trigger_id
    
    def add_event_trigger(self,
                         pattern: Dict[str, Any],
                         time_window: float,
                         weight: float = 1.0) -> str:
        """Add a new event pattern trigger"""
        trigger_id = str(uuid.uuid4())
        trigger = EventPatternTrigger(pattern, time_window, weight)
        self.event_triggers[trigger_id] = trigger
        
        condition = TriggerCondition(
            id=trigger_id,
            type=TriggerType.EVENT_PATTERN,
            parameters={
                'pattern': pattern,
                'time_window': time_window
            },
            weight=weight,
            created_at=datetime.utcnow(),
            last_triggered=None,
            metadata={}
        )
        
        self.triggers[trigger_id] = condition
        return trigger_id
    
    def add_simulation_trigger(self,
                             simulation_type: str,
                             success_threshold: float,
                             weight: float = 1.0) -> str:
        """Add a new simulation-based trigger"""
        trigger_id = str(uuid.uuid4())
        trigger = SimulationTrigger(simulation_type, success_threshold, weight)
        self.simulation_triggers[trigger_id] = trigger
        
        condition = TriggerCondition(
            id=trigger_id,
            type=TriggerType.SIMULATION_RESULT,
            parameters={
                'simulation_type': simulation_type,
                'success_threshold': success_threshold
            },
            weight=weight,
            created_at=datetime.utcnow(),
            last_triggered=None,
            metadata={}
        )
        
        self.triggers[trigger_id] = condition
        return trigger_id
    
    def add_composite_trigger(self,
                            trigger_ids: List[str],
                            operator: str = "AND") -> str:
        """Add a new composite trigger"""
        trigger_id = str(uuid.uuid4())
        triggers = []
        
        for tid in trigger_ids:
            if tid in self.metric_triggers:
                triggers.append(self.metric_triggers[tid])
            elif tid in self.event_triggers:
                triggers.append(self.event_triggers[tid])
            elif tid in self.simulation_triggers:
                triggers.append(self.simulation_triggers[tid])
                
        composite = CompositeTrigger(triggers, operator)
        self.composite_triggers[trigger_id] = composite
        
        condition = TriggerCondition(
            id=trigger_id,
            type=TriggerType.COMPOSITE,
            parameters={
                'trigger_ids': trigger_ids,
                'operator': operator
            },
            weight=1.0,
            created_at=datetime.utcnow(),
            last_triggered=None,
            metadata={}
        )
        
        self.triggers[trigger_id] = condition
        return trigger_id
    
    def evaluate_triggers(self, context: Dict[str, Any]) -> List[str]:
        """Evaluate all triggers and return IDs of triggered conditions"""
        triggered = []
        
        # Evaluate metric triggers
        for trigger_id, trigger in self.metric_triggers.items():
            if trigger.evaluate(context.get('metrics', {})):
                triggered.append(trigger_id)
                self.triggers[trigger_id].last_triggered = datetime.utcnow()
        
        # Evaluate event triggers
        for trigger_id, trigger in self.event_triggers.items():
            if trigger.evaluate():
                triggered.append(trigger_id)
                self.triggers[trigger_id].last_triggered = datetime.utcnow()
        
        # Evaluate simulation triggers
        for trigger_id, trigger in self.simulation_triggers.items():
            if trigger.evaluate(context.get('simulation_results', {})):
                triggered.append(trigger_id)
                self.triggers[trigger_id].last_triggered = datetime.utcnow()
        
        # Evaluate composite triggers
        for trigger_id, trigger in self.composite_triggers.items():
            if trigger.evaluate(context):
                triggered.append(trigger_id)
                self.triggers[trigger_id].last_triggered = datetime.utcnow()
        
        return triggered
    
    def get_trigger_state(self, trigger_id: str) -> Optional[Dict[str, Any]]:
        """Get the current state of a trigger"""
        if trigger_id not in self.triggers:
            return None
            
        condition = self.triggers[trigger_id]
        return {
            'id': condition.id,
            'type': condition.type.value,
            'parameters': condition.parameters,
            'weight': condition.weight,
            'created_at': condition.created_at.isoformat(),
            'last_triggered': condition.last_triggered.isoformat() if condition.last_triggered else None,
            'metadata': condition.metadata
        }
    
    def list_triggers(self) -> List[Dict[str, Any]]:
        """List all triggers"""
        return [self.get_trigger_state(tid) for tid in self.triggers.keys()] 