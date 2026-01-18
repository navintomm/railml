"""
Test Suite for Railway Network System
Tests CDL zone identification and signal placement
"""

import sys
from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType


def test_simple_merge():
    """Test 1: Simple two-track merge creating one CDL zone"""
    print("\n" + "="*70)
    print("TEST 1: Simple Two-Track Merge")
    print("="*70)
    
    network = RailwayNetwork("Test: Simple Merge")
    
    # Create simple merge: A → M ← B
    network.add_node(RailwayNode("A", NodeType.TRACK, (0, 100)))
    network.add_node(RailwayNode("B", NodeType.TRACK, (0, 0)))
    network.add_node(RailwayNode("M", NodeType.TRACK, (500, 50)))
    network.add_node(RailwayNode("EXIT", NodeType.EXIT_POINT, (1000, 50)))
    
    network.add_edge(RailwayEdge("A", "M", 550))
    network.add_edge(RailwayEdge("B", "M", 550))
    network.add_edge(RailwayEdge("M", "EXIT", 500))
    
    # Test CDL zone identification
    cdl_zones = network.identify_cdl_zones()
    
    assert len(cdl_zones) == 1, f"Expected 1 CDL zone, found {len(cdl_zones)}"
    assert "M" in cdl_zones, "Node M should be identified as CDL zone"
    
    print(f"✓ CDL zones identified: {cdl_zones}")
    
    # Test signal placement
    signals = network.place_signals_before_cdl_zones(signal_distance=500)
    
    assert len(signals) == 2, f"Expected 2 signals, found {len(signals)}"
    
    print(f"✓ Signals placed: {signals}")
    print("✓ TEST PASSED: Simple merge works correctly")
    
    return True


def test_no_merge():
    """Test 2: Linear track with no merges (no CDL zones)"""
    print("\n" + "="*70)
    print("TEST 2: Linear Track (No Merges)")
    print("="*70)
    
    network = RailwayNetwork("Test: Linear")
    
    # Create linear path: A → B → C → D
    network.add_node(RailwayNode("A", NodeType.ENTRY_POINT, (0, 0)))
    network.add_node(RailwayNode("B", NodeType.TRACK, (300, 0)))
    network.add_node(RailwayNode("C", NodeType.TRACK, (600, 0)))
    network.add_node(RailwayNode("D", NodeType.EXIT_POINT, (900, 0)))
    
    network.add_edge(RailwayEdge("A", "B", 300))
    network.add_edge(RailwayEdge("B", "C", 300))
    network.add_edge(RailwayEdge("C", "D", 300))
    
    # Test CDL zone identification
    cdl_zones = network.identify_cdl_zones()
    
    assert len(cdl_zones) == 0, f"Expected 0 CDL zones, found {len(cdl_zones)}"
    
    print(f"✓ No CDL zones (as expected): {cdl_zones}")
    
    # Test signal placement
    signals = network.place_signals_before_cdl_zones()
    
    assert len(signals) == 0, f"Expected 0 signals, found {len(signals)}"
    
    print(f"✓ No signals placed (as expected)")
    print("✓ TEST PASSED: Linear track works correctly")
    
    return True


def test_multiple_cdl_zones():
    """Test 3: Multiple CDL zones in complex network"""
    print("\n" + "="*70)
    print("TEST 3: Multiple CDL Zones")
    print("="*70)
    
    network = RailwayNetwork("Test: Multiple CDL")
    
    # Create network with 2 CDL zones
    # Entry1 → M1 ← Entry2
    # M1 → M2 ← Entry3
    network.add_node(RailwayNode("ENTRY1", NodeType.ENTRY_POINT, (0, 200)))
    network.add_node(RailwayNode("ENTRY2", NodeType.ENTRY_POINT, (0, 100)))
    network.add_node(RailwayNode("ENTRY3", NodeType.ENTRY_POINT, (0, 0)))
    network.add_node(RailwayNode("M1", NodeType.TRACK, (600, 150)))
    network.add_node(RailwayNode("M2", NodeType.TRACK, (1200, 100)))
    network.add_node(RailwayNode("EXIT", NodeType.EXIT_POINT, (1600, 100)))
    
    network.add_edge(RailwayEdge("ENTRY1", "M1", 650))
    network.add_edge(RailwayEdge("ENTRY2", "M1", 550))
    network.add_edge(RailwayEdge("M1", "M2", 650))
    network.add_edge(RailwayEdge("ENTRY3", "M2", 1250))
    network.add_edge(RailwayEdge("M2", "EXIT", 400))
    
    # Test CDL zone identification
    cdl_zones = network.identify_cdl_zones()
    
    assert len(cdl_zones) == 2, f"Expected 2 CDL zones, found {len(cdl_zones)}"
    assert "M1" in cdl_zones, "M1 should be a CDL zone"
    assert "M2" in cdl_zones, "M2 should be a CDL zone"
    
    print(f"✓ CDL zones identified: {cdl_zones}")
    
    # Test signal placement
    signals = network.place_signals_before_cdl_zones(signal_distance=500)
    
    # Should have signals for each incoming track to each CDL zone
    # M1: 2 incoming (ENTRY1, ENTRY2) = 2 signals
    # M2: 2 incoming (M1, ENTRY3) = 2 signals
    # Total: 4 signals
    assert len(signals) == 4, f"Expected 4 signals, found {len(signals)}"
    
    print(f"✓ Signals placed: {len(signals)} signals")
    print("✓ TEST PASSED: Multiple CDL zones handled correctly")
    
    return True


def test_signal_distance():
    """Test 4: Verify signal placement distance"""
    print("\n" + "="*70)
    print("TEST 4: Signal Distance Verification")
    print("="*70)
    
    network = RailwayNetwork("Test: Signal Distance")
    
    # Create simple merge with exact 500m approach
    network.add_node(RailwayNode("START", NodeType.ENTRY_POINT, (0, 0)))
    network.add_node(RailwayNode("MID", NodeType.TRACK, (300, 0)))
    network.add_node(RailwayNode("CDL", NodeType.TRACK, (800, 0)))
    network.add_node(RailwayNode("OTHER", NodeType.TRACK, (0, 100)))
    
    network.add_edge(RailwayEdge("START", "MID", 300))
    network.add_edge(RailwayEdge("MID", "CDL", 500))
    network.add_edge(RailwayEdge("OTHER", "CDL", 850))
    
    # Identify CDL zone
    cdl_zones = network.identify_cdl_zones()
    assert len(cdl_zones) == 1, "Should have 1 CDL zone"
    
    # Place signals with 500m distance
    signals = network.place_signals_before_cdl_zones(signal_distance=500)
    
    print(f"✓ CDL zone: {cdl_zones[0]}")
    print(f"✓ Signals placed: {len(signals)}")
    
    # Verify signal metadata
    for signal_id in signals:
        signal_node = network.nodes[signal_id]
        distance = signal_node.metadata.get('distance_to_cdl', 0)
        print(f"  • {signal_id}: {distance}m to CDL zone")
        assert distance == 500, f"Signal should be 500m from CDL, found {distance}m"
    
    print("✓ TEST PASSED: Signal distances correct")
    
    return True


def test_switch_nodes():
    """Test 5: Switches creating CDL zones"""
    print("\n" + "="*70)
    print("TEST 5: Switch Nodes as CDL Zones")
    print("="*70)
    
    network = RailwayNetwork("Test: Switches")
    
    # Create converging switch
    network.add_node(RailwayNode("T1", NodeType.TRACK, (0, 100)))
    network.add_node(RailwayNode("T2", NodeType.TRACK, (0, 0)))
    network.add_node(RailwayNode("SW", NodeType.SWITCH, (600, 50)))
    network.add_node(RailwayNode("EXIT", NodeType.EXIT_POINT, (1000, 50)))
    
    network.add_edge(RailwayEdge("T1", "SW", 650))
    network.add_edge(RailwayEdge("T2", "SW", 650))
    network.add_edge(RailwayEdge("SW", "EXIT", 400))
    
    # Test
    cdl_zones = network.identify_cdl_zones()
    
    assert len(cdl_zones) == 1, f"Expected 1 CDL zone, found {len(cdl_zones)}"
    assert "SW" in cdl_zones, "Switch should be identified as CDL zone"
    
    # Check that switch is marked as CDL zone
    switch_node = network.nodes["SW"]
    assert switch_node.node_type == NodeType.CDL_ZONE, "Switch should be marked as CDL_ZONE type"
    
    print(f"✓ Switch identified as CDL zone")
    print(f"✓ Node type updated to: {switch_node.node_type}")
    print("✓ TEST PASSED: Switches correctly identified as CDL zones")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("RAILWAY NETWORK SYSTEM - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Simple Two-Track Merge", test_simple_merge),
        ("Linear Track (No Merges)", test_no_merge),
        ("Multiple CDL Zones", test_multiple_cdl_zones),
        ("Signal Distance Verification", test_signal_distance),
        ("Switch Nodes as CDL Zones", test_switch_nodes)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"\n✗ TEST FAILED: {test_name}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ TEST ERROR: {test_name}")
            print(f"  Error: {type(e).__name__}: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {passed/len(tests)*100:.1f}%")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
