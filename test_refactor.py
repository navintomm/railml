import os
import networkx as nx
from railway_network import RailwayNetwork, NodeType
from railml_importer import import_railml_and_analyze

def test_refactor():
    railml_file = "example_station.railml"
    if not os.path.exists(railml_file):
        print("Error: RailML file not found.")
        return

    print("Running Refactor Verification...")
    
    # helper to check if NodeType has TRACK
    # It has a legacy value, but we shouldn't find nodes with it from importer
    
    network = import_railml_and_analyze(railml_file)
    
    print("\nVerifying Graph Structure:")
    
    track_edges = 0
    connected_edges = 0
    track_nodes = 0
    switch_nodes = 0
    junction_nodes = 0
    buffer_nodes = 0
    platform_nodes = 0
    
    for n, data in network.graph.nodes(data=True):
        ntype = data.get('node_type')
        if ntype == 'track':
            track_nodes += 1
        elif ntype == 'switch':
            switch_nodes += 1
        elif ntype == 'junction':
            junction_nodes += 1
        elif ntype == 'buffer':
            buffer_nodes += 1
        elif ntype == 'platform_node':
            platform_nodes += 1
            
    for u, v, data in network.graph.edges(data=True):
        etype = data.get('edge_type')
        if etype == 'track':
            track_edges += 1
            print(f"  Found Track Edge: {data.get('id')} ({u} -> {v}) Length: {data.get('length')}")
        else:
            connected_edges += 1

    print(f"\nStats:")
    print(f"  Track Nodes: {track_nodes} (Should be 0)")
    print(f"  Switch Nodes: {switch_nodes}")
    print(f"  Junction Nodes: {junction_nodes}")
    print(f"  Buffer Nodes: {buffer_nodes}")
    print(f"  Platform Nodes: {platform_nodes}")
    print(f"  Track Edges: {track_edges} (Should be > 0)")
    
    if track_nodes == 0 and track_edges > 0:
        print("\nSUCCESS: Tracks are now Edges!")
    else:
        print("\nFAILURE: Tracks are still Nodes or something is wrong.")
        
    # Generate visualization
    network.visualize(save_path="refactor_test.png", show_edge_labels=False)

if __name__ == "__main__":
    test_refactor()
