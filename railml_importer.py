"""
RailML Importer Module
Imports railway infrastructure from RailML (XML) files and converts to RailwayNetwork
"""

import xml.etree.ElementTree as ET
from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType
from typing import Dict, List, Tuple
import os


class RailMLImporter:
    """
    Imports RailML files and converts them to RailwayNetwork objects.
    
    RailML is the international standard for railway data exchange.
    This importer supports RailML version 2.x and 3.x infrastructure elements.
    """
    
    def __init__(self):
        self.namespace = {}
        self.track_elements = {}
        self.connections = []
    
    def import_from_file(self, railml_file_path: str) -> RailwayNetwork:
        """
        Import a RailML file and create a RailwayNetwork.
        
        Args:
            railml_file_path: Path to the .railml or .xml file
            
        Returns:
            RailwayNetwork object populated with data from the file
        """
        print(f"\n{'='*70}")
        print(f"IMPORTING RAILML FILE: {os.path.basename(railml_file_path)}")
        print(f"{'='*70}")
        
        if not os.path.exists(railml_file_path):
            raise FileNotFoundError(f"RailML file not found: {railml_file_path}")
        
        # Parse XML
        tree = ET.parse(railml_file_path)
        root = tree.getroot()
        
        # Detect namespace
        self._detect_namespace(root)
        
        # Extract station name
        station_name = self._extract_station_name(root)
        network = RailwayNetwork(station_name)
        
        print(f"Station: {station_name}")
        
        # Import tracks
        self._import_tracks(root, network)
        
        # Import switches
        self._import_switches(root, network)
        
        # Import platforms
        self._import_platforms(root, network)
        
        # Import connections (edges)
        self._import_connections(root, network)
        
        print(f"\n✓ RailML import complete!")
        print(f"  • Nodes: {network.graph.number_of_nodes()}")
        print(f"  • Edges: {network.graph.number_of_edges()}")
        
        return network
    
    def _detect_namespace(self, root):
        """Detect RailML namespace from root element"""
        if root.tag.startswith('{'):
            self.namespace = {'railml': root.tag.split('}')[0].strip('{')}
        else:
            self.namespace = {}
    
    def _extract_station_name(self, root) -> str:
        """Extract station name from RailML"""
        # Try different RailML versions
        for path in [
            './/railml:operationControlPoint',
            './/operationControlPoint',
            './/railml:station',
            './/station'
        ]:
            element = root.find(path, self.namespace)
            if element is not None:
                name = element.get('name') or element.get('id')
                if name:
                    return name
        
        return "Imported Station"
    
    def _import_tracks(self, root, network: RailwayNetwork):
        """Import track elements from RailML as Nodes"""
        print("\nImporting tracks...")
        
        track_count = 0
        
        # Find track elements (RailML 2.x and 3.x)
        for path in ['.//railml:track', './/track', './/railml:netElement', './/netElement']:
            tracks = root.findall(path, self.namespace)
            
            for track in tracks:
                track_id = track.get('id') or track.get('name')
                if not track_id:
                    continue
                
                # Get position (if available)
                position = self._extract_position(track, track_count)
                
                # Create track node
                node = RailwayNode(
                    id=track_id,
                    node_type=NodeType.TRACK,
                    position=position,
                    metadata={
                        'source': 'railml',
                        'length': track.get('length', 'unknown')
                    }
                )
                
                network.add_node(node)
                track_count += 1
        
        print(f"  ✓ Imported {track_count} tracks")
    
    def _import_switches(self, root, network: RailwayNetwork):
        """Import switch/turnout elements from RailML"""
        print("Importing switches...")
        
        switch_count = 0
        
        # Find switch elements
        for path in ['.//railml:switch', './/switch', './/railml:turnout', './/turnout']:
            switches = root.findall(path, self.namespace)
            
            for switch in switches:
                switch_id = switch.get('id') or switch.get('name')
                if not switch_id:
                    continue
                
                position = self._extract_position(switch, switch_count * 2)
                
                node = RailwayNode(
                    id=switch_id,
                    node_type=NodeType.SWITCH,
                    position=position,
                    metadata={
                        'source': 'railml',
                        'type': switch.get('type', 'turnout')
                    }
                )
                
                network.add_node(node)
                switch_count += 1
        
        print(f"  ✓ Imported {switch_count} switches")
    
    def _import_platforms(self, root, network: RailwayNetwork):
        """Import platform elements from RailML"""
        print("Importing platforms...")
        
        platform_count = 0
        
        for path in ['.//railml:platform', './/platform', './/railml:platformEdge', './/platformEdge']:
            platforms = root.findall(path, self.namespace)
            
            for platform in platforms:
                platform_id = platform.get('id') or platform.get('name')
                if not platform_id:
                    continue
                
                position = self._extract_position(platform, platform_count * 3)
                
                node = RailwayNode(
                    id=platform_id,
                    node_type=NodeType.PLATFORM,
                    position=position,
                    metadata={
                        'source': 'railml',
                        'length': platform.get('length', 'unknown'),
                        'height': platform.get('height', 'unknown')
                    }
                )
                
                network.add_node(node)
                platform_count += 1
        
        print(f"  ✓ Imported {platform_count} platforms")
    
    def _import_connections(self, root, network: RailwayNetwork):
        """Import track connections (edges) from RailML"""
        print("Importing connections...")
        
        connection_count = 0
        
        # Find connections/relations
        for path in ['.//railml:connection', './/connection', './/railml:relation', './/relation']:
            connections = root.findall(path, self.namespace)
            
            for conn in connections:
                from_id = conn.get('ref') or conn.get('from')
                to_id = conn.get('to') or conn.get('target')
                
                # Check if both nodes exist
                if from_id in network.nodes and to_id in network.nodes:
                    length = float(conn.get('length', 500))  # Default 500m
                    
                    edge = RailwayEdge(
                        from_node=from_id,
                        to_node=to_id,
                        length=length,
                        metadata={'source': 'railml'}
                    )
                    
                    network.add_edge(edge)
                    connection_count += 1
        
        print(f"  ✓ Imported {connection_count} connections")
    
    def _extract_position(self, element, index: int) -> Tuple[float, float]:
        """
        Extract or generate position for visualization.
        RailML may include geo-coordinates or we generate them.
        """
        # Try to get coordinates from RailML
        lat = element.get('latitude') or element.get('lat')
        lon = element.get('longitude') or element.get('lon')
        
        if lat and lon:
            try:
                return (float(lon) * 10000, float(lat) * 10000)  # Scale for visualization
            except:
                pass
        
        # Generate position based on index
        x = (index % 10) * 300
        y = (index // 10) * 200
        
        return (x, y)


def import_railml_and_analyze(railml_file: str, signal_distance: float = 500) -> RailwayNetwork:
    """
    Complete workflow: Import RailML → Find CDL zones → Place signals
    
    Args:
        railml_file: Path to RailML file
        signal_distance: Distance in meters for signal placement
        
    Returns:
        RailwayNetwork with CDL zones identified and signals placed
    """
    # Import from RailML
    importer = RailMLImporter()
    network = importer.import_from_file(railml_file)
    
    # Identify CDL zones
    print(f"\n{'='*70}")
    print("ANALYZING IMPORTED NETWORK")
    print(f"{'='*70}")
    
    cdl_zones = network.identify_cdl_zones()
    print(f"\n✓ Found {len(cdl_zones)} CDL zone(s)")
    
    for cdl_id in cdl_zones:
        incoming = list(network.graph.predecessors(cdl_id))
        print(f"  • {cdl_id}")
        print(f"    Incoming: {', '.join(incoming)}")
    
    # Place signals
    signals = network.place_signals_before_cdl_zones(signal_distance=signal_distance)
    print(f"\n✓ Placed {len(signals)} signal(s)")
    
    # Show statistics
    stats = network.get_network_statistics()
    print(f"\nNetwork Statistics:")
    for key, value in stats.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    return network


# Example usage
if __name__ == "__main__":
    print("""
RailML Importer Module
======================

This module allows you to import RailML files and automatically:
1. Parse the railway infrastructure
2. Identify CDL zones (merge points)
3. Place safety signals

Usage:
------
from railml_importer import import_railml_and_analyze

# Import and analyze
network = import_railml_and_analyze("mystation.railml")

# Visualize
network.visualize(save_path="imported_station.png")

# Get summary
print(network.export_summary())
""")
