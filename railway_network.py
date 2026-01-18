"""
Railway Network Graph Module
Uses NetworkX to model railway stations with tracks, switches, and CDL zones.
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    """Types of nodes in the railway network"""
    TRACK = "track"
    SWITCH = "switch"
    SIGNAL = "signal"
    CDL_ZONE = "cdl_zone"
    PLATFORM = "platform"
    ENTRY_POINT = "entry"
    EXIT_POINT = "exit"


@dataclass
class RailwayNode:
    """Represents a node in the railway network"""
    id: str
    node_type: NodeType
    position: Tuple[float, float]  # (x, y) coordinates in meters
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RailwayEdge:
    """Represents an edge (track segment) in the railway network"""
    from_node: str
    to_node: str
    length: float  # Length in meters
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class RailwayNetwork:
    """
    Directed graph representation of a railway station network.
    Handles tracks, switches, CDL zones, and automatic signal placement.
    """
    
    def __init__(self, name: str = "Railway Station"):
        """
        Initialize a railway network.
        
        Args:
            name: Name of the railway station
        """
        self.name = name
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, RailwayNode] = {}
        self.edges: Dict[Tuple[str, str], RailwayEdge] = {}
        self.cdl_zones: Set[str] = set()
        self.signals: Set[str] = set()
    
    def add_node(self, node: RailwayNode) -> None:
        """
        Add a node to the railway network.
        
        Args:
            node: RailwayNode to add
        """
        self.nodes[node.id] = node
        self.graph.add_node(
            node.id,
            node_type=node.node_type.value,
            position=node.position,
            **node.metadata
        )
        
        # Track special node types
        if node.node_type == NodeType.SIGNAL:
            self.signals.add(node.id)
        elif node.node_type == NodeType.CDL_ZONE:
            self.cdl_zones.add(node.id)
    
    def add_edge(self, edge: RailwayEdge) -> None:
        """
        Add an edge (track segment) to the railway network.
        
        Args:
            edge: RailwayEdge to add
        """
        if edge.from_node not in self.nodes or edge.to_node not in self.nodes:
            raise ValueError(f"Both nodes must exist before adding edge: {edge.from_node} -> {edge.to_node}")
        
        self.edges[(edge.from_node, edge.to_node)] = edge
        self.graph.add_edge(
            edge.from_node,
            edge.to_node,
            length=edge.length,
            **edge.metadata
        )
    
    def identify_cdl_zones(self) -> List[str]:
        """
        Identify CDL (Conflicting Direction Logic) zones where tracks merge.
        A CDL zone is any node with in-degree > 1 (multiple tracks converging).
        
        Returns:
            List of node IDs that are CDL zones
        """
        cdl_zones = []
        
        for node_id in self.graph.nodes():
            # Check in-degree (number of incoming edges)
            in_degree = self.graph.in_degree(node_id)
            
            # If multiple tracks converge, it's a CDL zone
            if in_degree > 1:
                node = self.nodes[node_id]
                
                # Mark as CDL zone if not already marked
                if node.node_type != NodeType.CDL_ZONE:
                    node.node_type = NodeType.CDL_ZONE
                    self.graph.nodes[node_id]['node_type'] = NodeType.CDL_ZONE.value
                    node.metadata['cdl_incoming_tracks'] = list(self.graph.predecessors(node_id))
                
                cdl_zones.append(node_id)
                self.cdl_zones.add(node_id)
        
        return cdl_zones
    
    def calculate_distance_along_path(self, path: List[str]) -> float:
        """
        Calculate total distance along a path.
        
        Args:
            path: List of node IDs forming a path
            
        Returns:
            Total distance in meters
        """
        total_distance = 0.0
        for i in range(len(path) - 1):
            edge_data = self.graph.get_edge_data(path[i], path[i + 1])
            if edge_data:
                total_distance += edge_data.get('length', 0)
        return total_distance
    
    def find_signal_placement_point(self, cdl_zone_id: str, approach_track: str, 
                                    signal_distance: float = 500.0) -> Tuple[str, float] or None:
        """
        Find the optimal point to place a signal before a CDL zone.
        
        Args:
            cdl_zone_id: ID of the CDL zone
            approach_track: ID of the node approaching the CDL zone
            signal_distance: Distance in meters before CDL zone to place signal (default: 500m)
            
        Returns:
            Tuple of (node_id, remaining_distance) where signal should be placed,
            or None if placement not possible
        """
        # Try to find a path backward from CDL zone
        try:
            # Get all paths from approach_track to cdl_zone
            paths = list(nx.all_simple_paths(self.graph, approach_track, cdl_zone_id, cutoff=10))
            
            if not paths:
                return None
            
            # Use the shortest path
            path = min(paths, key=lambda p: self.calculate_distance_along_path(p))
            
            # Traverse backward from CDL zone to find placement point
            accumulated_distance = 0.0
            
            for i in range(len(path) - 1, 0, -1):
                current_node = path[i]
                previous_node = path[i - 1]
                
                edge_data = self.graph.get_edge_data(previous_node, current_node)
                segment_length = edge_data.get('length', 0)
                
                if accumulated_distance + segment_length >= signal_distance:
                    # Signal should be placed on this segment
                    remaining_distance = signal_distance - accumulated_distance
                    return (previous_node, remaining_distance)
                
                accumulated_distance += segment_length
            
            # If we can't go back far enough, place at the first node
            return (path[0], 0.0)
            
        except nx.NetworkXNoPath:
            return None
    
    def place_signals_before_cdl_zones(self, signal_distance: float = 500.0) -> List[str]:
        """
        Automatically place signal nodes 500 meters before each CDL zone.
        
        Args:
            signal_distance: Distance in meters before CDL zone (default: 500m)
            
        Returns:
            List of newly created signal node IDs
        """
        # First, identify all CDL zones
        cdl_zones = self.identify_cdl_zones()
        
        new_signals = []
        
        for cdl_zone_id in cdl_zones:
            cdl_node = self.nodes[cdl_zone_id]
            
            # Get all incoming tracks to this CDL zone
            incoming_tracks = list(self.graph.predecessors(cdl_zone_id))
            
            for approach_track in incoming_tracks:
                # Find placement point
                placement = self.find_signal_placement_point(cdl_zone_id, approach_track, signal_distance)
                
                if placement:
                    placement_node_id, offset_distance = placement
                    placement_node = self.nodes[placement_node_id]
                    
                    # Create signal ID
                    signal_id = f"SIG_{approach_track}_to_{cdl_zone_id}"
                    
                    # Skip if signal already exists
                    if signal_id in self.nodes:
                        continue
                    
                    # Calculate signal position (interpolate between nodes if needed)
                    signal_position = placement_node.position
                    
                    # Create signal node
                    signal_node = RailwayNode(
                        id=signal_id,
                        node_type=NodeType.SIGNAL,
                        position=signal_position,
                        metadata={
                            'protects_cdl_zone': cdl_zone_id,
                            'approach_from': approach_track,
                            'distance_to_cdl': signal_distance,
                            'offset_from_placement': offset_distance
                        }
                    )
                    
                    # Add signal to network
                    self.add_node(signal_node)
                    new_signals.append(signal_id)
                    
                    print(f"✓ Placed signal '{signal_id}' at node '{placement_node_id}' "
                          f"protecting CDL zone '{cdl_zone_id}'")
        
        return new_signals
    
    def get_network_statistics(self) -> Dict:
        """
        Get statistics about the railway network.
        
        Returns:
            Dictionary containing network statistics
        """
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'tracks': sum(1 for n in self.nodes.values() if n.node_type == NodeType.TRACK),
            'switches': sum(1 for n in self.nodes.values() if n.node_type == NodeType.SWITCH),
            'signals': len(self.signals),
            'cdl_zones': len(self.cdl_zones),
            'platforms': sum(1 for n in self.nodes.values() if n.node_type == NodeType.PLATFORM),
            'total_track_length': sum(e.length for e in self.edges.values())
        }
    
    def visualize(self, figsize=(16, 12), save_path=None, show_edge_labels=False):
        """
        Visualize the railway network using matplotlib.
        
        Args:
            figsize: Figure size (width, height)
            save_path: Optional path to save the visualization
            show_edge_labels: Whether to show edge distance labels (can clutter for large networks)
        """
        fig, ax = plt.subplots(figsize=figsize, dpi=100)
        
        # Get positions - use provided positions or calculate better layout
        pos = nx.get_node_attributes(self.graph, 'position')
        
        # If no positions or they're clustered, use spring layout for better spacing
        if not pos or len(pos) != len(self.graph.nodes()):
            pos = nx.spring_layout(
                self.graph, 
                k=3,  # Optimal distance between nodes
                iterations=50,
                scale=2000,  # Larger scale for better spacing
                seed=42
            )
        
        # Color map for different node types
        color_map = {
            NodeType.TRACK.value: '#4A90E2',
            NodeType.SWITCH.value: '#F5A623',
            NodeType.SIGNAL.value: '#7ED321',
            NodeType.CDL_ZONE.value: '#D0021B',
            NodeType.PLATFORM.value: '#9013FE',
            NodeType.ENTRY_POINT.value: '#50E3C2',
            NodeType.EXIT_POINT.value: '#B8E986'
        }
        
        # Draw edges (tracks) with lighter color
        nx.draw_networkx_edges(
            self.graph, pos, 
            edge_color='#AAAAAA',
            arrows=True,
            arrowsize=15,
            arrowstyle='->',
            width=1.5,
            alpha=0.6,
            ax=ax,
            connectionstyle='arc3,rad=0.1'  # Curved edges to avoid overlap
        )
        
        # Draw nodes by type with better sizing
        node_sizes = {
            NodeType.CDL_ZONE.value: 1200,  # Larger for important nodes
            NodeType.SIGNAL.value: 900,
            NodeType.SWITCH.value: 800,
            NodeType.PLATFORM.value: 700,
            NodeType.ENTRY_POINT.value: 900,
            NodeType.EXIT_POINT.value: 900,
            NodeType.TRACK.value: 600
        }
        
        for node_type in NodeType:
            nodes_of_type = [
                node for node, data in self.graph.nodes(data=True)
                if data.get('node_type') == node_type.value
            ]
            
            if nodes_of_type:
                nx.draw_networkx_nodes(
                    self.graph, pos,
                    nodelist=nodes_of_type,
                    node_color=color_map.get(node_type.value, '#CCCCCC'),
                    node_size=node_sizes.get(node_type.value, 600),
                    label=node_type.value.upper(),
                    alpha=0.9,
                    edgecolors='black',
                    linewidths=1.5,
                    ax=ax
                )
        
        # Draw labels with better readability - only for important nodes
        important_nodes = [
            node for node, data in self.graph.nodes(data=True)
            if data.get('node_type') in [
                NodeType.CDL_ZONE.value,
                NodeType.PLATFORM.value,
                NodeType.ENTRY_POINT.value,
                NodeType.EXIT_POINT.value
            ]
        ]
        
        # Draw labels for important nodes only
        important_labels = {node: node for node in important_nodes}
        nx.draw_networkx_labels(
            self.graph, pos,
            labels=important_labels,
            font_size=7,
            font_weight='bold',
            font_color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7, edgecolor='none'),
            ax=ax
        )
        
        # Optionally draw edge labels (disabled by default for complex networks)
        if show_edge_labels and self.graph.number_of_edges() < 20:
            edge_labels = nx.get_edge_attributes(self.graph, 'length')
            edge_labels = {k: f"{v}m" for k, v in edge_labels.items()}
            try:
                nx.draw_networkx_edge_labels(
                    self.graph, pos,
                    edge_labels=edge_labels,
                    font_size=6,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8),
                    ax=ax
                )
            except (TypeError, AttributeError):
                pass
        
        # Title and legend
        ax.set_title(
            f"Railway Network: {self.name}\n"
            f"Nodes: {self.graph.number_of_nodes()} | "
            f"Edges: {self.graph.number_of_edges()} | "
            f"CDL Zones: {len(self.cdl_zones)} | "
            f"Signals: {len(self.signals)}",
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        
        # Better legend positioning
        legend = ax.legend(
            loc='upper left',
            fontsize=9,
            framealpha=0.9,
            edgecolor='black',
            title='Node Types'
        )
        legend.get_title().set_fontweight('bold')
        
        ax.axis('off')
        ax.margins(0.1)  # Add margins to prevent clipping
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"✓ Visualization saved to: {save_path}")
        
        # plt.show()
    
    def export_summary(self) -> str:
        """
        Export a text summary of the railway network.
        
        Returns:
            Formatted string summary
        """
        stats = self.get_network_statistics()
        
        summary = f"""
{'='*70}
RAILWAY NETWORK SUMMARY: {self.name}
{'='*70}

NETWORK STATISTICS:
  • Total Nodes: {stats['total_nodes']}
  • Total Edges: {stats['total_edges']}
  • Track Nodes: {stats['tracks']}
  • Switches: {stats['switches']}
  • Signals: {stats['signals']}
  • CDL Zones: {stats['cdl_zones']}
  • Platforms: {stats['platforms']}
  • Total Track Length: {stats['total_track_length']:.2f} meters

CDL ZONES (Conflict/Merge Points):
"""
        
        for cdl_id in sorted(self.cdl_zones):
            cdl_node = self.nodes[cdl_id]
            incoming = list(self.graph.predecessors(cdl_id))
            summary += f"  • {cdl_id}\n"
            summary += f"    - Incoming tracks: {', '.join(incoming)}\n"
        
        summary += f"\nSIGNALS:\n"
        for signal_id in sorted(self.signals):
            signal_node = self.nodes[signal_id]
            meta = signal_node.metadata
            summary += f"  • {signal_id}\n"
            if 'protects_cdl_zone' in meta:
                summary += f"    - Protects CDL Zone: {meta['protects_cdl_zone']}\n"
                summary += f"    - Approach from: {meta['approach_from']}\n"
                summary += f"    - Distance to CDL: {meta['distance_to_cdl']}m\n"
        
        summary += f"\n{'='*70}\n"
        
        return summary
