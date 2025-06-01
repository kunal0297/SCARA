"""
Cryo-State Memory Crystals
Manages universe snapshots and state restoration
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import hashlib
import zlib
import base64

class CryoState:
    def __init__(self,
                 universe_id: str,
                 state_data: Dict[str, Any],
                 metadata: Optional[Dict[str, Any]] = None):
        self.universe_id = universe_id
        self.state_data = state_data
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()
        self.crystal_id = self._generate_crystal_id()
        
    def _generate_crystal_id(self) -> str:
        """Generate a unique identifier for this crystal"""
        data = json.dumps({
            'universe_id': self.universe_id,
            'state': self.state_data,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()
    
    def compress(self) -> str:
        """Compress the crystal data for storage"""
        data = json.dumps({
            'universe_id': self.universe_id,
            'state_data': self.state_data,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
            'crystal_id': self.crystal_id
        })
        compressed = zlib.compress(data.encode())
        return base64.b64encode(compressed).decode()
    
    @classmethod
    def decompress(cls, compressed_data: str) -> 'CryoState':
        """Decompress crystal data from storage"""
        decoded = base64.b64decode(compressed_data)
        decompressed = zlib.decompress(decoded)
        data = json.loads(decompressed.decode())
        
        crystal = cls(
            universe_id=data['universe_id'],
            state_data=data['state_data'],
            metadata=data['metadata']
        )
        crystal.timestamp = datetime.fromisoformat(data['timestamp'])
        crystal.crystal_id = data['crystal_id']
        return crystal

class CryoStateManager:
    def __init__(self):
        self.crystals: Dict[str, List[CryoState]] = {}
        
    def create_snapshot(self,
                       universe_id: str,
                       state_data: Dict[str, Any],
                       metadata: Optional[Dict[str, Any]] = None) -> CryoState:
        """Create a new snapshot of a universe's state"""
        crystal = CryoState(
            universe_id=universe_id,
            state_data=state_data,
            metadata=metadata
        )
        
        if universe_id not in self.crystals:
            self.crystals[universe_id] = []
            
        self.crystals[universe_id].append(crystal)
        return crystal
    
    def get_snapshot(self, universe_id: str, crystal_id: str) -> Optional[CryoState]:
        """Retrieve a specific snapshot by crystal ID"""
        if universe_id not in self.crystals:
            return None
            
        for crystal in self.crystals[universe_id]:
            if crystal.crystal_id == crystal_id:
                return crystal
        return None
    
    def list_snapshots(self, universe_id: str) -> List[Dict[str, Any]]:
        """List all snapshots for a universe"""
        if universe_id not in self.crystals:
            return []
            
        return [
            {
                'crystal_id': crystal.crystal_id,
                'timestamp': crystal.timestamp.isoformat(),
                'metadata': crystal.metadata
            }
            for crystal in self.crystals[universe_id]
        ]
    
    def delete_snapshot(self, universe_id: str, crystal_id: str) -> bool:
        """Delete a specific snapshot"""
        if universe_id not in self.crystals:
            return False
            
        initial_length = len(self.crystals[universe_id])
        self.crystals[universe_id] = [
            crystal for crystal in self.crystals[universe_id]
            if crystal.crystal_id != crystal_id
        ]
        
        return len(self.crystals[universe_id]) < initial_length
    
    def get_latest_snapshot(self, universe_id: str) -> Optional[CryoState]:
        """Get the most recent snapshot for a universe"""
        if universe_id not in self.crystals or not self.crystals[universe_id]:
            return None
            
        return max(
            self.crystals[universe_id],
            key=lambda x: x.timestamp
        )
    
    def export_snapshot(self, universe_id: str, crystal_id: str) -> Optional[str]:
        """Export a snapshot to a compressed string"""
        crystal = self.get_snapshot(universe_id, crystal_id)
        if not crystal:
            return None
            
        return crystal.compress()
    
    def import_snapshot(self, compressed_data: str) -> Optional[CryoState]:
        """Import a snapshot from a compressed string"""
        try:
            crystal = CryoState.decompress(compressed_data)
            if crystal.universe_id not in self.crystals:
                self.crystals[crystal.universe_id] = []
            self.crystals[crystal.universe_id].append(crystal)
            return crystal
        except Exception:
            return None 