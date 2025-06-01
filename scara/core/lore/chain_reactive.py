"""
Chain-Reactive Lore Propagation System
Manages narrative and lore propagation between universes
"""

from typing import Dict, Any, List, Optional, Set
from datetime import datetime
import json
import hashlib
import uuid
from dataclasses import dataclass
import numpy as np

@dataclass
class LoreEvent:
    id: str
    source_universe: str
    event_type: str
    data: Dict[str, Any]
    created_at: datetime
    propagation_path: List[str]
    metadata: Dict[str, Any]

class LoreNode:
    def __init__(self,
                 universe_id: str,
                 initial_state: Dict[str, Any],
                 propagation_rules: Dict[str, Any]):
        self.universe_id = universe_id
        self.state = initial_state
        self.propagation_rules = propagation_rules
        self.events: List[LoreEvent] = []
        self.connections: Set[str] = set()
        self.created_at = datetime.utcnow()
        self.last_updated = self.created_at
        
    def add_connection(self, target_universe_id: str) -> None:
        """Add a connection to another universe"""
        self.connections.add(target_universe_id)
        self.last_updated = datetime.utcnow()
    
    def remove_connection(self, target_universe_id: str) -> None:
        """Remove a connection to another universe"""
        self.connections.discard(target_universe_id)
        self.last_updated = datetime.utcnow()
    
    def create_event(self,
                    event_type: str,
                    data: Dict[str, Any],
                    metadata: Optional[Dict[str, Any]] = None) -> LoreEvent:
        """Create a new lore event"""
        event = LoreEvent(
            id=str(uuid.uuid4()),
            source_universe=self.universe_id,
            event_type=event_type,
            data=data,
            created_at=datetime.utcnow(),
            propagation_path=[self.universe_id],
            metadata=metadata or {}
        )
        
        self.events.append(event)
        self.last_updated = datetime.utcnow()
        return event
    
    def receive_event(self, event: LoreEvent) -> bool:
        """Receive and process a lore event from another universe"""
        # Check if event should be propagated based on rules
        if not self._should_propagate(event):
            return False
        
        # Process event
        self._process_event(event)
        
        # Update event propagation path
        event.propagation_path.append(self.universe_id)
        
        # Add to events list
        self.events.append(event)
        
        self.last_updated = datetime.utcnow()
        return True
    
    def _should_propagate(self, event: LoreEvent) -> bool:
        """Check if an event should be propagated based on rules"""
        if event.source_universe not in self.connections:
            return False
            
        rules = self.propagation_rules.get(event.event_type, {})
        if not rules:
            return False
            
        # Check event data against rules
        return self._check_event_rules(event, rules)
    
    def _check_event_rules(self, event: LoreEvent, rules: Dict[str, Any]) -> bool:
        """Check if an event matches propagation rules"""
        # TODO: Implement rule checking logic
        return True
    
    def _process_event(self, event: LoreEvent) -> None:
        """Process a received event and update universe state"""
        # Update state based on event type and data
        if event.event_type in self.state:
            self._update_state(event)
        
        # Update propagation rules if needed
        if event.event_type == 'rule_update':
            self._update_rules(event)
    
    def _update_state(self, event: LoreEvent) -> None:
        """Update universe state based on event"""
        # TODO: Implement state update logic
        pass
    
    def _update_rules(self, event: LoreEvent) -> None:
        """Update propagation rules based on event"""
        # TODO: Implement rule update logic
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """Get current node state"""
        return {
            'universe_id': self.universe_id,
            'state': self.state,
            'event_count': len(self.events),
            'connection_count': len(self.connections),
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }
    
    def get_events(self,
                  event_type: Optional[str] = None,
                  limit: Optional[int] = None) -> List[LoreEvent]:
        """Get events, optionally filtered by type and limited in number"""
        events = self.events
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if limit:
            events = events[-limit:]
        return events

class LorePropagationManager:
    def __init__(self):
        self.nodes: Dict[str, LoreNode] = {}
        
    def create_node(self,
                   universe_id: str,
                   initial_state: Dict[str, Any],
                   propagation_rules: Dict[str, Any]) -> LoreNode:
        """Create a new lore node"""
        node = LoreNode(
            universe_id=universe_id,
            initial_state=initial_state,
            propagation_rules=propagation_rules
        )
        
        self.nodes[universe_id] = node
        return node
    
    def get_node(self, universe_id: str) -> Optional[LoreNode]:
        """Get a node by universe ID"""
        return self.nodes.get(universe_id)
    
    def connect_universes(self, universe_id_1: str, universe_id_2: str) -> bool:
        """Create a bidirectional connection between universes"""
        node1 = self.get_node(universe_id_1)
        node2 = self.get_node(universe_id_2)
        
        if not node1 or not node2:
            return False
            
        node1.add_connection(universe_id_2)
        node2.add_connection(universe_id_1)
        return True
    
    def disconnect_universes(self, universe_id_1: str, universe_id_2: str) -> bool:
        """Remove a bidirectional connection between universes"""
        node1 = self.get_node(universe_id_1)
        node2 = self.get_node(universe_id_2)
        
        if not node1 or not node2:
            return False
            
        node1.remove_connection(universe_id_2)
        node2.remove_connection(universe_id_1)
        return True
    
    def propagate_event(self,
                       source_universe_id: str,
                       event_type: str,
                       data: Dict[str, Any],
                       metadata: Optional[Dict[str, Any]] = None) -> List[str]:
        """Propagate an event through connected universes"""
        source_node = self.get_node(source_universe_id)
        if not source_node:
            return []
            
        # Create initial event
        event = source_node.create_event(event_type, data, metadata)
        
        # Track propagation
        propagated_to = []
        to_process = [(source_node, event)]
        processed = set()
        
        while to_process:
            current_node, current_event = to_process.pop(0)
            
            if current_node.universe_id in processed:
                continue
                
            processed.add(current_node.universe_id)
            
            # Propagate to connected nodes
            for target_id in current_node.connections:
                if target_id in processed:
                    continue
                    
                target_node = self.get_node(target_id)
                if not target_node:
                    continue
                    
                if target_node.receive_event(current_event):
                    propagated_to.append(target_id)
                    to_process.append((target_node, current_event))
        
        return propagated_to
    
    def list_nodes(self) -> List[Dict[str, Any]]:
        """List all nodes"""
        return [node.get_state() for node in self.nodes.values()]
    
    def get_node_events(self,
                       universe_id: str,
                       event_type: Optional[str] = None,
                       limit: Optional[int] = None) -> List[LoreEvent]:
        """Get events for a specific node"""
        node = self.get_node(universe_id)
        if not node:
            return []
            
        return node.get_events(event_type, limit) 