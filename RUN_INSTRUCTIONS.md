# 🚂 Railway Network System - How to Run

## Quick Start (3 Steps)

### Step 1: Open Terminal
Navigate to the project directory:
```bash
cd "c:\Users\NAVIN TOM BABU\Desktop\railml"
```

### Step 2: Install Dependencies (One-time)
```bash
pip install -r requirements.txt
```
This installs: NetworkX, Matplotlib, NumPy

### Step 3: Run Examples
```bash
# Option A: Example Station (Recommended first)
python example_station.py

# Option B: Advanced Demo
python advanced_demo.py

# Option C: Run Tests
python test_railway_network.py
```

---

## What Each Command Does

### 1️⃣ Example Station (`example_station.py`)

**Creates:** Multi-platform railway station with 2 platforms, 4 switches

**Output:**
- Console summary with CDL zones and signals
- Visualization window (interactive plot)
- Saved image: `railway_station_network.png`

**What to expect:**
```
======================================================================
CREATING EXAMPLE RAILWAY STATION
======================================================================

1. Creating Entry Points...
2. Creating Switches...
3. Creating Platform Tracks...
4. Creating Siding Track...
5. Creating Exit Points...
6. Creating Track Connections...

✓ Station structure created successfully!

======================================================================
IDENTIFYING CDL ZONES (Track Merge Points)
======================================================================

Found 2 CDL zone(s):
  • EXIT_B
    - Merging tracks: SWITCH_A2, SWITCH_B2
  • SWITCH_B1
    - Merging tracks: ENTRY_B, SWITCH_A1

======================================================================
AUTOMATIC SIGNAL PLACEMENT (500m before CDL zones)
======================================================================

✓ Placed signal 'SIG_SWITCH_A2_to_EXIT_B' at node 'SWITCH_A2' protecting CDL zone 'EXIT_B'
✓ Placed signal 'SIG_SWITCH_B2_to_EXIT_B' at node 'SWITCH_B2' protecting CDL zone 'EXIT_B'
✓ Placed signal 'SIG_ENTRY_B_to_SWITCH_B1' at node 'ENTRY_B' protecting CDL zone 'SWITCH_B1'
✓ Placed signal 'SIG_SWITCH_A1_to_SWITCH_B1' at node 'SWITCH_A1' protecting CDL zone 'SWITCH_B1'

✓ Placed 4 signal(s)

[Visualization window opens - close it to continue]
```

**To close:** Click the X on the matplotlib window

---

### 2️⃣ Advanced Demo (`advanced_demo.py`)

**Creates:** Complex junction with 3 converging railway lines

**Output:**
- Path analysis (all routes through network)
- Signal coverage verification
- Visualization window
- Saved files:
  - `complex_junction.png`
  - `network_summary.txt`

**What to expect:**
```
======================================================================
CDL ZONE IDENTIFICATION
======================================================================

Found 2 CDL zone(s):
  • SWITCH_AB (in-degree: 2)
    Merging from: TRACK_A2, TRACK_B2
  • SWITCH_MAIN (in-degree: 2)
    Merging from: SWITCH_AB, TRACK_C1

======================================================================
PATH ANALYSIS
======================================================================

All Possible Routes:
  1. LINE_A_ENTRY → MAIN_EXIT
     Path: LINE_A_ENTRY → TRACK_A1 → TRACK_A2 → SWITCH_AB → SWITCH_MAIN → MAIN_EXIT
     Distance: 1550m
  2. LINE_B_ENTRY → MAIN_EXIT
     Path: LINE_B_ENTRY → TRACK_B1 → TRACK_B2 → SWITCH_AB → SWITCH_MAIN → MAIN_EXIT
     Distance: 1550m
  3. LINE_C_ENTRY → MAIN_EXIT
     Path: LINE_C_ENTRY → TRACK_C1 → SWITCH_MAIN → MAIN_EXIT
     Distance: 1550m

Total routes: 3

======================================================================
SIGNAL COVERAGE ANALYSIS
======================================================================

CDL Zone: SWITCH_AB
  • Incoming tracks: 2
  • Protecting signals: 2
  • Coverage: 100.0%
  ✓ Full signal coverage

CDL Zone: SWITCH_MAIN
  • Incoming tracks: 2
  • Protecting signals: 2
  • Coverage: 100.0%
  ✓ Full signal coverage
```

---

### 3️⃣ Test Suite (`test_railway_network.py`)

**Validates:** All system functionality

**Output:**
- Test results (5 tests)
- No visualization windows
- Completes in seconds

**What to expect:**
```
======================================================================
RAILWAY NETWORK SYSTEM - TEST SUITE
======================================================================

======================================================================
TEST 1: Simple Two-Track Merge
======================================================================
✓ CDL zones identified: ['M']
✓ Signals placed: ['SIG_A_to_M', 'SIG_B_to_M']
✓ TEST PASSED: Simple merge works correctly

======================================================================
TEST 2: Linear Track (No Merges)
======================================================================
✓ No CDL zones (as expected): []
✓ No signals placed (as expected)
✓ TEST PASSED: Linear track works correctly

[... 3 more tests ...]

======================================================================
TEST SUMMARY
======================================================================
Total Tests: 5
Passed: 5 ✓
Failed: 0 ✗
Success Rate: 100.0%
======================================================================

🎉 ALL TESTS PASSED! 🎉
```

---

## Create Your Own Network

Create a new file `my_station.py`:

```python
from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType

# Create network
network = RailwayNetwork("My Custom Station")

# Add nodes
network.add_node(RailwayNode("ENTRY", NodeType.ENTRY_POINT, (0, 0)))
network.add_node(RailwayNode("TRACK_A", NodeType.TRACK, (300, 100)))
network.add_node(RailwayNode("TRACK_B", NodeType.TRACK, (300, -100)))
network.add_node(RailwayNode("MERGE", NodeType.TRACK, (600, 0)))
network.add_node(RailwayNode("EXIT", NodeType.EXIT_POINT, (900, 0)))

# Connect tracks (create a merge point)
network.add_edge(RailwayEdge("ENTRY", "TRACK_A", 320))
network.add_edge(RailwayEdge("ENTRY", "TRACK_B", 320))
network.add_edge(RailwayEdge("TRACK_A", "MERGE", 360))
network.add_edge(RailwayEdge("TRACK_B", "MERGE", 360))
network.add_edge(RailwayEdge("MERGE", "EXIT", 300))

# Identify CDL zones
print("\n=== CDL ZONES ===")
cdl_zones = network.identify_cdl_zones()
print(f"Found: {cdl_zones}")

# Place signals automatically
print("\n=== SIGNALS ===")
signals = network.place_signals_before_cdl_zones(signal_distance=500)
print(f"Placed: {signals}")

# Show statistics
print("\n=== STATISTICS ===")
stats = network.get_network_statistics()
for key, value in stats.items():
    print(f"{key}: {value}")

# Visualize
network.visualize(save_path="my_custom_station.png")

# Export summary
print(network.export_summary())
```

Then run:
```bash
python my_station.py
```

---

## Understanding the Visualization

When the plot window opens, you'll see:

### Node Colors:
- 🔵 **Blue** = Track segments
- 🟠 **Orange** = Switches (turnouts)
- 🟢 **Green** = Signals (automatically placed!)
- 🔴 **Red** = CDL Zones (merge points)
- 🟣 **Purple** = Platforms
- 🔷 **Cyan** = Entry points
- 🟢 **Light Green** = Exit points

### Edge Labels:
- Show distance in meters (e.g., "500m")

### Arrows:
- Show direction of track (directed graph)

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'networkx'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Visualization window not appearing
**Solution:**
- The window may be behind other windows
- Check your taskbar for Python plots
- On some systems, it may take a few seconds to appear

### Issue: Program seems stuck
**Solution:**
- It's waiting for you to close the visualization window
- Close the matplotlib plot window to continue

### Issue: Want to skip visualization
**Modify the code:** Comment out or remove the `.visualize()` line

---

## File Outputs

After running, you'll find these generated files:

| File | Created By | Description |
|------|------------|-------------|
| `railway_station_network.png` | example_station.py | Multi-platform station diagram |
| `complex_junction.png` | advanced_demo.py | Complex junction diagram |
| `network_summary.txt` | advanced_demo.py | Text export of network |
| `my_custom_station.png` | Your custom scripts | Your custom networks |

All images are high-resolution PNG files (300 DPI).

---

## Next Steps

1. ✅ Run `python test_railway_network.py` to verify installation
2. ✅ Run `python example_station.py` to see basic functionality
3. ✅ Run `python advanced_demo.py` to see advanced features
4. ✅ Create your own network using the template above
5. ✅ Read `README.md` for complete documentation
6. ✅ Read `QUICK_REFERENCE.md` for API reference

---

## Summary

**One command to get started:**
```bash
python example_station.py
```

**Close the visualization window when done, and you're ready to go!** 🚂

For questions, check the full documentation in `README.md`.
