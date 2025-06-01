"""
SCARA Lore Engine
Generates narrative content based on contract events and mutations.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import networkx as nx

@dataclass
class Event:
    """Contract event"""
    event_type: str
    timestamp: int
    data: Dict
    block_number: int
    transaction_hash: str

@dataclass
class LoreEntry:
    """Lore entry in the narrative"""
    entry_id: str
    title: str
    content: str
    timestamp: int
    event_type: str
    related_events: List[str]
    tags: List[str]

class LoreEngine:
    def __init__(self, narrative_style: str = "epic"):
        """Initialize Lore Engine"""
        self.narrative_style = narrative_style
        self.events: List[Event] = []
        self.lore_entries: List[LoreEntry] = []
        self.event_graph = nx.DiGraph()
        
        # Load narrative templates
        self.templates = self._load_templates()
    
    def add_event(self, event: Event):
        """
        Add a new event to the lore engine
        
        Args:
            event: Event to add
        """
        self.events.append(event)
        self.event_graph.add_node(
            event.transaction_hash,
            **event.__dict__
        )
        
        # Generate lore entry
        entry = self._generate_lore_entry(event)
        self.lore_entries.append(entry)
    
    def get_lore_entries(
        self,
        event_type: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> List[LoreEntry]:
        """
        Get filtered lore entries
        
        Args:
            event_type: Filter by event type
            start_time: Filter by start time
            end_time: Filter by end time
            tags: Filter by tags
            
        Returns:
            List of matching lore entries
        """
        entries = self.lore_entries
        
        if event_type:
            entries = [e for e in entries if e.event_type == event_type]
        
        if start_time:
            entries = [e for e in entries if e.timestamp >= start_time]
        
        if end_time:
            entries = [e for e in entries if e.timestamp <= end_time]
        
        if tags:
            entries = [e for e in entries if any(t in e.tags for t in tags)]
        
        return entries
    
    def get_event_chain(self, event_hash: str) -> List[Event]:
        """
        Get chain of related events
        
        Args:
            event_hash: Starting event hash
            
        Returns:
            List of related events
        """
        try:
            path = nx.shortest_path(self.event_graph, event_hash)
            return [self.event_graph.nodes[n]['event'] for n in path]
        except nx.NetworkXNoPath:
            return []
    
    def export_lore(self, filepath: str):
        """
        Export lore to file
        
        Args:
            filepath: Path to export file
        """
        lore_data = {
            'narrative_style': self.narrative_style,
            'events': [e.__dict__ for e in self.events],
            'lore_entries': [e.__dict__ for e in self.lore_entries]
        }
        
        with open(filepath, 'w') as f:
            json.dump(lore_data, f, indent=2)
    
    def _generate_lore_entry(self, event: Event) -> LoreEntry:
        """Generate lore entry from event"""
        template = self.templates.get(event.event_type, self.templates['default'])
        
        # Format template with event data
        content = template.format(**event.data)
        
        # Generate title
        title = self._generate_title(event, content)
        
        # Extract tags
        tags = self._extract_tags(event, content)
        
        # Find related events
        related_events = self._find_related_events(event)
        
        return LoreEntry(
            entry_id=f"lore_{int(datetime.now().timestamp())}",
            title=title,
            content=content,
            timestamp=event.timestamp,
            event_type=event.event_type,
            related_events=related_events,
            tags=tags
        )
    
    def _generate_title(self, event: Event, content: str) -> str:
        """Generate title for lore entry"""
        if event.event_type == 'MutationApplied':
            return f"The Evolution: {event.data.get('mutation_type', 'Unknown')} Mutation"
        elif event.event_type == 'ProposalCreated':
            return f"The Proposal: {event.data.get('description', '')[:50]}..."
        else:
            return f"The {event.event_type}: {content[:50]}..."
    
    def _extract_tags(self, event: Event, content: str) -> List[str]:
        """Extract tags from event and content"""
        tags = [event.event_type]
        
        # Add mutation-specific tags
        if event.event_type == 'MutationApplied':
            tags.extend([
                f"mutation_{event.data.get('mutation_type', 'unknown')}",
                f"impact_{event.data.get('impact_level', 'unknown')}"
            ])
        
        # Add proposal-specific tags
        elif event.event_type == 'ProposalCreated':
            tags.extend([
                'governance',
                f"status_{event.data.get('status', 'unknown')}"
            ])
        
        return tags
    
    def _find_related_events(self, event: Event) -> List[str]:
        """Find related events in the graph"""
        related = []
        
        # Look for events in the same block
        for e in self.events:
            if e.block_number == event.block_number:
                related.append(e.transaction_hash)
        
        # Look for events with similar data
        for e in self.events:
            if e.transaction_hash != event.transaction_hash:
                similarity = self._calculate_event_similarity(event, e)
                if similarity > 0.7:  # 70% similarity threshold
                    related.append(e.transaction_hash)
        
        return related
    
    def _calculate_event_similarity(self, event1: Event, event2: Event) -> float:
        """Calculate similarity between two events"""
        if event1.event_type != event2.event_type:
            return 0.0
        
        # Compare data fields
        common_fields = set(event1.data.keys()) & set(event2.data.keys())
        if not common_fields:
            return 0.0
        
        similarities = []
        for field in common_fields:
            if isinstance(event1.data[field], (int, float)):
                # Numeric similarity
                max_val = max(event1.data[field], event2.data[field])
                if max_val == 0:
                    similarities.append(1.0)
                else:
                    similarities.append(
                        1 - abs(event1.data[field] - event2.data[field]) / max_val
                    )
            else:
                # String similarity
                str1 = str(event1.data[field])
                str2 = str(event2.data[field])
                if str1 == str2:
                    similarities.append(1.0)
                else:
                    similarities.append(0.0)
        
        return sum(similarities) / len(similarities)
    
    def _load_templates(self) -> Dict[str, str]:
        """Load narrative templates"""
        return {
            'MutationApplied': """
In the depths of the digital realm, a new evolution emerged.
The {mutation_type} mutation transformed the contract's essence,
bringing forth {impact_level} changes to its core logic.
The system adapted, growing stronger with each modification.
            """,
            
            'ProposalCreated': """
A new proposal arose from the collective consciousness.
"{description}"
The community gathered to deliberate its fate,
weighing the potential impact on their shared future.
            """,
            
            'VoteCast': """
A voice joined the chorus of governance.
{reason}
The vote was cast, adding to the growing consensus
that would shape the system's evolution.
            """,
            
            'default': """
In the ever-evolving landscape of the blockchain,
a new event unfolded: {event_type}
Its impact rippled through the system,
adding another chapter to the ongoing saga.
            """
        } 