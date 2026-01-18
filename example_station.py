"""
Example Railway Station
Demonstrates the use of the RailwayNetwork class to model a realistic station
with multiple platforms, switches, and automatic CDL zone/signal detection.
"""

from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType


def create_example_station() -> RailwayNetwork:
    """
    Create a realistic railway station with:
    - Entry/exit points
    - Multiple platforms
    - Track switches creating CDL zones
    - Automatic signal placement before merge points
    
    Station Layout:
                    ┌─── Platform 1 ───┐
    Entry A ──┬─────┤                  ├───┬─── Exit A
              │     └──────────────────┘   │
              │                            │
              │     ┌─── Platform 2 ───┐  │
    Entry B ──┼─────┤                  ├──┴─── Exit B (CDL Zone)
              │     └──────────────────┘
              │
              └──────── Siding Track ───────── Exit C
    """
    
    print("="*70)
    print("CREATING EXAMPLE RAILWAY STATION")
    print("="*70)
    
    # Initialize network
    network = RailwayNetwork("Central Station")
    
    # ========== ENTRY POINTS ==========
    print("\n1. Creating Entry Points...")
    network.add_node(RailwayNode(
        id="ENTRY_A",
        node_type=NodeType.ENTRY_POINT,
        position=(0, 200),
        metadata={"description": "Main entry from North"}
    ))
    
    network.add_node(RailwayNode(
        id="ENTRY_B",
        node_type=NodeType.ENTRY_POINT,
        position=(0, 0),
        metadata={"description": "Secondary entry from South"}
    ))
    
    # ========== SWITCHES (Diverging Points) ==========
    print("2. Creating Switches...")
    network.add_node(RailwayNode(
        id="SWITCH_A1",
        node_type=NodeType.SWITCH,
        position=(200, 200),
        metadata={"type": "turnout", "direction": "diverging"}
    ))
    
    network.add_node(RailwayNode(
        id="SWITCH_B1",
        node_type=NodeType.SWITCH,
        position=(200, 0),
        metadata={"type": "turnout", "direction": "diverging"}
    ))
    
    network.add_node(RailwayNode(
        id="SWITCH_A2",
        node_type=NodeType.SWITCH,
        position=(800, 200),
        metadata={"type": "turnout", "direction": "converging"}
    ))
    
    network.add_node(RailwayNode(
        id="SWITCH_B2",
        node_type=NodeType.SWITCH,
        position=(800, 0),
        metadata={"type": "turnout", "direction": "converging"}
    ))
    
    # ========== PLATFORM TRACKS ==========
    print("3. Creating Platform Tracks...")
    network.add_node(RailwayNode(
        id="PLATFORM_1_START",
        node_type=NodeType.PLATFORM,
        position=(400, 250),
        metadata={"platform_number": 1, "section": "start"}
    ))
    
    network.add_node(RailwayNode(
        id="PLATFORM_1_END",
        node_type=NodeType.PLATFORM,
        position=(600, 250),
        metadata={"platform_number": 1, "section": "end"}
    ))
    
    network.add_node(RailwayNode(
        id="PLATFORM_2_START",
        node_type=NodeType.PLATFORM,
        position=(400, 50),
        metadata={"platform_number": 2, "section": "start"}
    ))
    
    network.add_node(RailwayNode(
        id="PLATFORM_2_END",
        node_type=NodeType.PLATFORM,
        position=(600, 50),
        metadata={"platform_number": 2, "section": "end"}
    ))
    
    # ========== SIDING TRACK ==========
    print("4. Creating Siding Track...")
    network.add_node(RailwayNode(
        id="SIDING_MID",
        node_type=NodeType.TRACK,
        position=(500, -100),
        metadata={"track_type": "siding"}
    ))
    
    # ========== EXIT POINTS ==========
    print("5. Creating Exit Points...")
    network.add_node(RailwayNode(
        id="EXIT_A",
        node_type=NodeType.EXIT_POINT,
        position=(1000, 200),
        metadata={"description": "Exit to East"}
    ))
    
    network.add_node(RailwayNode(
        id="EXIT_B",
        node_type=NodeType.EXIT_POINT,
        position=(1000, 0),
        metadata={"description": "Exit to Southeast"}
    ))
    
    network.add_node(RailwayNode(
        id="EXIT_C",
        node_type=NodeType.EXIT_POINT,
        position=(900, -100),
        metadata={"description": "Exit to Siding Yard"}
    ))
    
    # ========== TRACK CONNECTIONS (EDGES) ==========
    print("6. Creating Track Connections...")
    
    # Entry A → Switch A1 → Platform 1
    network.add_edge(RailwayEdge("ENTRY_A", "SWITCH_A1", length=200))
    network.add_edge(RailwayEdge("SWITCH_A1", "PLATFORM_1_START", length=250))
    network.add_edge(RailwayEdge("PLATFORM_1_START", "PLATFORM_1_END", length=200))
    network.add_edge(RailwayEdge("PLATFORM_1_END", "SWITCH_A2", length=250))
    
    # Entry B → Switch B1 → Platform 2
    network.add_edge(RailwayEdge("ENTRY_B", "SWITCH_B1", length=200))
    network.add_edge(RailwayEdge("SWITCH_B1", "PLATFORM_2_START", length=250))
    network.add_edge(RailwayEdge("PLATFORM_2_START", "PLATFORM_2_END", length=200))
    network.add_edge(RailwayEdge("PLATFORM_2_END", "SWITCH_B2", length=250))
    
    # Switch A1 → Switch B1 (crossover)
    network.add_edge(RailwayEdge("SWITCH_A1", "SWITCH_B1", length=200))
    
    # Siding track
    network.add_edge(RailwayEdge("SWITCH_B1", "SIDING_MID", length=550))
    network.add_edge(RailwayEdge("SIDING_MID", "EXIT_C", length=450))
    
    # Exits (creating CDL zones)
    network.add_edge(RailwayEdge("SWITCH_A2", "EXIT_A", length=200))
    network.add_edge(RailwayEdge("SWITCH_B2", "EXIT_B", length=200))
    
    # CRITICAL: This creates a CDL zone at EXIT_B
    # Both SWITCH_A2 and SWITCH_B2 can route to EXIT_B
    network.add_edge(RailwayEdge("SWITCH_A2", "EXIT_B", length=300))
    
    print("\n✓ Station structure created successfully!")
    
    return network


def main():
    """Main function to demonstrate CDL zone identification and signal placement"""
    
    # Create the station
    network = create_example_station()
    
    # Display initial statistics
    print("\n" + "="*70)
    print("INITIAL NETWORK STATISTICS")
    print("="*70)
    stats = network.get_network_statistics()
    for key, value in stats.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    # Identify CDL zones
    print("\n" + "="*70)
    print("IDENTIFYING CDL ZONES (Track Merge Points)")
    print("="*70)
    cdl_zones = network.identify_cdl_zones()
    print(f"\nFound {len(cdl_zones)} CDL zone(s):")
    for cdl_id in cdl_zones:
        incoming = list(network.graph.predecessors(cdl_id))
        print(f"  • {cdl_id}")
        print(f"    - Merging tracks: {', '.join(incoming)}")
    
    # Place signals automatically
    print("\n" + "="*70)
    print("AUTOMATIC SIGNAL PLACEMENT (500m before CDL zones)")
    print("="*70)
    new_signals = network.place_signals_before_cdl_zones(signal_distance=500.0)
    print(f"\n✓ Placed {len(new_signals)} signal(s)")
    
    # Display final summary
    print(network.export_summary())
    
    # Visualize the network
    print("\n" + "="*70)
    print("GENERATING NETWORK VISUALIZATION")
    print("="*70)
    network.visualize(
        figsize=(18, 12),
        save_path="railway_station_network.png"
    )
    
    print("\n✓ Example completed successfully!")
    print("="*70)


if __name__ == "__main__":
    main()
