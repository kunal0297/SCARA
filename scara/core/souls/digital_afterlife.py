"""
Digital Afterlife System
Manages onchain souls and their persistence
"""

from typing import Dict, Any, List, Optional, Set
from datetime import datetime
import json
import hashlib
import uuid
from dataclasses import dataclass

@dataclass
class SoulState:
    id: str
    original_entity_id: str
    universe_id: str
    attributes: Dict[str, Any]
    memories: List[Dict[str, Any]]
    influence: Dict[str, float]
    created_at: datetime
    last_updated: datetime
    metadata: Dict[str, Any]

class DigitalSoul:
    def __init__(self,
                 original_entity_id: str,
                 universe_id: str,
                 attributes: Dict[str, Any],
                 memories: List[Dict[str, Any]],
                 metadata: Optional[Dict[str, Any]] = None):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.last_updated = self.created_at
        
        # Initialize soul state
        self.state = SoulState(
            id=self.id,
            original_entity_id=original_entity_id,
            universe_id=universe_id,
            attributes=attributes,
            memories=memories,
            influence={},
            created_at=self.created_at,
            last_updated=self.last_updated,
            metadata=metadata or {}
        )
        
    def influence_world(self,
                       target_universe_id: str,
                       influence_type: str,
                       strength: float) -> Dict[str, Any]:
        """Exert influence on a target universe"""
        # Record influence attempt
        influence_record = {
            'type': influence_type,
            'strength': strength,
            'target_universe': target_universe_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Update influence tracking
        if target_universe_id not in self.state.influence:
            self.state.influence[target_universe_id] = 0.0
        self.state.influence[target_universe_id] += strength
        
        # Add to memories
        self.state.memories.append({
            'type': 'influence',
            'data': influence_record,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.last_updated = datetime.utcnow()
        return influence_record
    
    def add_memory(self, memory_data: Dict[str, Any]) -> None:
        """Add a new memory to the soul"""
        memory = {
            'data': memory_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.state.memories.append(memory)
        self.last_updated = datetime.utcnow()
    
    def evolve(self, delta_time: float) -> None:
        """Evolve the soul's state"""
        # Update attributes based on time
        self._update_attributes(delta_time)
        
        # Process memories
        self._process_memories()
        
        # Update influence
        self._update_influence()
        
        self.last_updated = datetime.utcnow()
    
    def _update_attributes(self, delta_time: float) -> None:
        """Update soul attributes based on time"""
        # TODO: Implement attribute evolution
        pass
    
    def _process_memories(self) -> None:
        """Process and organize memories"""
        # TODO: Implement memory processing
        pass
    
    def _update_influence(self) -> None:
        """Update influence levels"""
        # TODO: Implement influence updates
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """Get current soul state"""
        return {
            'id': self.state.id,
            'original_entity_id': self.state.original_entity_id,
            'universe_id': self.state.universe_id,
            'attributes': self.state.attributes,
            'influence': self.state.influence,
            'memory_count': len(self.state.memories),
            'created_at': self.state.created_at.isoformat(),
            'last_updated': self.state.last_updated.isoformat(),
            'metadata': self.state.metadata
        }
    
    def get_memories(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get soul memories, optionally limited to recent entries"""
        if limit is None:
            return self.state.memories
        return self.state.memories[-limit:]
    
    def get_influence(self, target_universe_id: Optional[str] = None) -> Dict[str, float]:
        """Get soul's influence, optionally for a specific universe"""
        if target_universe_id:
            return {target_universe_id: self.state.influence.get(target_universe_id, 0.0)}
        return self.state.influence

class AfterlifeManager:
    def __init__(self):
        self.souls: Dict[str, DigitalSoul] = {}
        
    def create_soul(self,
                   original_entity_id: str,
                   universe_id: str,
                   attributes: Dict[str, Any],
                   memories: List[Dict[str, Any]],
                   metadata: Optional[Dict[str, Any]] = None) -> DigitalSoul:
        """Create a new digital soul"""
        soul = DigitalSoul(
            original_entity_id=original_entity_id,
            universe_id=universe_id,
            attributes=attributes,
            memories=memories,
            metadata=metadata
        )
        
        self.souls[soul.id] = soul
        return soul
    
    def get_soul(self, soul_id: str) -> Optional[DigitalSoul]:
        """Get a soul by ID"""
        return self.souls.get(soul_id)
    
    def list_souls(self,
                  universe_id: Optional[str] = None,
                  original_entity_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all souls, optionally filtered by universe or original entity"""
        souls = self.souls.values()
        if universe_id:
            souls = [s for s in souls if s.state.universe_id == universe_id]
        if original_entity_id:
            souls = [s for s in souls if s.state.original_entity_id == original_entity_id]
            
        return [soul.get_state() for soul in souls]
    
    def evolve_souls(self, delta_time: float) -> None:
        """Evolve all souls"""
        for soul in self.souls.values():
            soul.evolve(delta_time)
    
    def get_universe_influence(self, universe_id: str) -> Dict[str, float]:
        """Get total influence on a universe from all souls"""
        influence = {}
        for soul in self.souls.values():
            if universe_id in soul.state.influence:
                influence[soul.id] = soul.state.influence[universe_id]
        return influence 