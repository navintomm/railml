"""
Advanced Railway Network Analysis
Demonstrates additional features and custom network creation
"""

from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType


def create_complex_junction() -> RailwayNetwork:
    """
    Create a complex railway junction with multiple CDL zones.
    
    This represents a busy junction where 3 lines converge to a single exit.
    """
    print("\n" + "="*70)
    print("CREATING COMPLEX RAILWAY JUNCTION")
    print("="*70)
    
    network = RailwayNetwork("Grand Junction")
    
    # Three entry lines
    network.add_node(RailwayNode("LINE_A_ENTRY", NodeType.ENTRY_POINT, (0, 300)))
    network.add_node(RailwayNode("LINE_B_ENTRY", NodeType.ENTRY_POINT, (0, 150)))
    network.add_node(RailwayNode("LINE_C_ENTRY", NodeType.ENTRY_POINT, (0, 0)))
    
    # Intermediate tracks
    network.add_node(RailwayNode("TRACK_A1", NodeType.TRACK, (300, 300)))
    network.add_node(RailwayNode("TRACK_A2", NodeType.TRACK, (600, 300)))
    network.add_node(RailwayNode("TRACK_B1", NodeType.TRACK, (300, 150)))
    network.add_node(RailwayNode("TRACK_B2", NodeType.TRACK, (600, 150)))
    network.add_node(RailwayNode("TRACK_C1", NodeType.TRACK, (300, 0)))
    
    # Switches for merging
    network.add_node(RailwayNode("SWITCH_AB", NodeType.SWITCH, (900, 225)))
    network.add_node(RailwayNode("SWITCH_MAIN", NodeType.SWITCH, (1200, 150)))
    
    # Final exit
    network.add_node(RailwayNode("MAIN_EXIT", NodeType.EXIT_POINT, (1500, 150)))
    
    # Track connections - Creating multiple merge points
    # Line A
    network.add_edge(RailwayEdge("LINE_A_ENTRY", "TRACK_A1", 300))
    network.add_edge(RailwayEdge("TRACK_A1", "TRACK_A2", 300))
    network.add_edge(RailwayEdge("TRACK_A2", "SWITCH_AB", 350))
    
    # Line B
    network.add_edge(RailwayEdge("LINE_B_ENTRY", "TRACK_B1", 300))
    network.add_edge(RailwayEdge("TRACK_B1", "TRACK_B2", 300))
    network.add_edge(RailwayEdge("TRACK_B2", "SWITCH_AB", 350))
    
    # Line C
    network.add_edge(RailwayEdge("LINE_C_ENTRY", "TRACK_C1", 300))
    network.add_edge(RailwayEdge("TRACK_C1", "SWITCH_MAIN", 950))
    
    # Merged paths
    network.add_edge(RailwayEdge("SWITCH_AB", "SWITCH_MAIN", 300))
    network.add_edge(RailwayEdge("SWITCH_MAIN", "MAIN_EXIT", 300))
    
    print("✓ Complex junction created!")
    return network


def analyze_network_paths(network: RailwayNetwork):
    """
    Analyze all possible paths through the network.
    """
    print("\n" + "="*70)
    print("PATH ANALYSIS")
    print("="*70)
    
    # Find all entry and exit points
    entries = [n for n, data in network.graph.nodes(data=True) 
               if data.get('node_type') == NodeType.ENTRY_POINT.value]
    exits = [n for n, data in network.graph.nodes(data=True) 
             if data.get('node_type') == NodeType.EXIT_POINT.value]
    
    print(f"\nEntry Points: {len(entries)}")
    for entry in entries:
        print(f"  • {entry}")
    
    print(f"\nExit Points: {len(exits)}")
    for exit_node in exits:
        print(f"  • {exit_node}")
    
    print(f"\nAll Possible Routes:")
    route_count = 0
    for entry in entries:
        for exit_node in exits:
            try:
                import networkx as nx
                paths = list(nx.all_simple_paths(network.graph, entry, exit_node))
                for path in paths:
                    route_count += 1
                    distance = network.calculate_distance_along_path(path)
                    print(f"  {route_count}. {entry} → {exit_node}")
                    print(f"     Path: {' → '.join(path)}")
                    print(f"     Distance: {distance:.0f}m")
            except nx.NetworkXNoPath:
                continue
    
    print(f"\nTotal routes: {route_count}")


def check_signal_coverage(network: RailwayNetwork):
    """
    Check if all CDL zones have adequate signal protection.
    """
    print("\n" + "="*70)
    print("SIGNAL COVERAGE ANALYSIS")
    print("="*70)
    
    for cdl_id in network.cdl_zones:
        incoming_tracks = list(network.graph.predecessors(cdl_id))
        
        # Find signals protecting this CDL zone
        protecting_signals = [
            sig_id for sig_id in network.signals
            if network.nodes[sig_id].metadata.get('protects_cdl_zone') == cdl_id
        ]
        
        coverage = len(protecting_signals) / len(incoming_tracks) * 100 if incoming_tracks else 0
        
        print(f"\nCDL Zone: {cdl_id}")
        print(f"  • Incoming tracks: {len(incoming_tracks)}")
        print(f"  • Protecting signals: {len(protecting_signals)}")
        print(f"  • Coverage: {coverage:.1f}%")
        
        if coverage < 100:
            print(f"  ⚠ WARNING: Incomplete signal coverage!")
        else:
            print(f"  ✓ Full signal coverage")


def main():
    """Main demonstration"""
    
    # Create complex junction
    network = create_complex_junction()
    
    # Identify CDL zones
    print("\n" + "="*70)
    print("CDL ZONE IDENTIFICATION")
    print("="*70)
    cdl_zones = network.identify_cdl_zones()
    print(f"\nFound {len(cdl_zones)} CDL zone(s):")
    for cdl_id in cdl_zones:
        incoming = list(network.graph.predecessors(cdl_id))
        in_degree = network.graph.in_degree(cdl_id)
        print(f"  • {cdl_id} (in-degree: {in_degree})")
        print(f"    Merging from: {', '.join(incoming)}")
    
    # Place signals
    print("\n" + "="*70)
    print("AUTOMATIC SIGNAL PLACEMENT")
    print("="*70)
    signals = network.place_signals_before_cdl_zones(signal_distance=500)
    print(f"\n✓ Successfully placed {len(signals)} signals")
    
    # Analyze paths
    analyze_network_paths(network)
    
    # Check signal coverage
    check_signal_coverage(network)
    
    # Network statistics
    print("\n" + "="*70)
    print("NETWORK STATISTICS")
    print("="*70)
    stats = network.get_network_statistics()
    for key, value in stats.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    # Visualize
    print("\n" + "="*70)
    print("GENERATING VISUALIZATION")
    print("="*70)
    network.visualize(
        figsize=(18, 12),
        save_path="complex_junction.png"
    )
    
    # Export summary
    summary_file = "network_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(network.export_summary())
    print(f"✓ Network summary exported to: {summary_file}")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
