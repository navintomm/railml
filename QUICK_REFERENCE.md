# Railway Network System - Quick Reference Guide

## 🚂 Overview

A Python-based railway systems engineering toolkit using **NetworkX** for modeling railway stations with automatic **CDL zone detection** and **signal placement**.

---

## 📁 Project Structure

```
railml/
├── railway_network.py          # Core module with RailwayNetwork class
├── example_station.py          # Example: Multi-platform station
├── advanced_demo.py            # Advanced: Complex junction analysis
├── test_railway_network.py     # Test suite (5 comprehensive tests)
├── requirements.txt            # Dependencies
└── README.md                   # Full documentation
```

---

## 🚀 Quick Start

### Installation
```bash
cd railml
pip install -r requirements.txt
```

### Run Examples
```bash
# Basic station example
python example_station.py

# Advanced junction analysis
python advanced_demo.py

# Run tests
python test_railway_network.py
```

---

## 🔑 Key Features

### 1. **CDL Zone Detection** 
Automatically identifies Conflicting Direction Logic zones (track merge points):
- Any node with **in-degree > 1** is a CDL zone
- Tracks converging at switches
- Multiple lines merging to single exit

### 2. **Automatic Signal Placement**
Places signals **500 meters** (configurable) before each CDL zone:
```python
network.place_signals_before_cdl_zones(signal_distance=500)
```

### 3. **Network Visualization**
Generates color-coded diagrams:
- 🔵 **Blue**: Track segments
- 🟠 **Orange**: Switches
- 🟢 **Green**: Signals
- 🔴 **Red**: CDL zones
- 🟣 **Purple**: Platforms

---

## 💡 Basic Usage

```python
from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType

# 1. Create network
network = RailwayNetwork("My Station")

# 2. Add nodes
network.add_node(RailwayNode(
    id="TRACK_A",
    node_type=NodeType.TRACK,
    position=(0, 0)
))

network.add_node(RailwayNode(
    id="SWITCH_1",
    node_type=NodeType.SWITCH,
    position=(500, 0)
))

# 3. Connect tracks
network.add_edge(RailwayEdge(
    from_node="TRACK_A",
    to_node="SWITCH_1",
    length=500  # meters
))

# 4. Identify CDL zones
cdl_zones = network.identify_cdl_zones()

# 5. Place signals
signals = network.place_signals_before_cdl_zones()

# 6. Visualize
network.visualize(save_path="my_station.png")

# 7. Get summary
print(network.export_summary())
```

---

## 📊 Node Types

| Type | Description | Use Case |
|------|-------------|----------|
| `TRACK` | Standard track segment | Main line tracks |
| `SWITCH` | Railway turnout | Diverging/converging points |
| `SIGNAL` | Signal element | Protection before CDL zones |
| `CDL_ZONE` | Merge point | Automatically identified |
| `PLATFORM` | Station platform | Passenger stations |
| `ENTRY_POINT` | Network entry | Incoming lines |
| `EXIT_POINT` | Network exit | Outgoing lines |

---

## 🧪 Test Results

All **5 tests** passed successfully:

✅ **Test 1**: Simple Two-Track Merge  
✅ **Test 2**: Linear Track (No Merges)  
✅ **Test 3**: Multiple CDL Zones  
✅ **Test 4**: Signal Distance Verification  
✅ **Test 5**: Switch Nodes as CDL Zones  

**Success Rate**: 100%

---

## 📈 Network Statistics

The system provides comprehensive analytics:

```python
stats = network.get_network_statistics()
```

Returns:
- Total nodes and edges
- Count by type (tracks, switches, signals, platforms)
- Total track length in meters
- CDL zone count
- Signal coverage analysis

---

## 🎯 Railway Engineering Concepts

### CDL (Conflicting Direction Logic) Zones
Points where multiple train paths can conflict:
- Track merges
- Converging switches
- Multiple approaches to same exit

### Signal Placement Strategy
- **Distance**: 500m before CDL zone (configurable)
- **Purpose**: Adequate braking distance and signal sighting
- **Coverage**: One signal per approach track

### Safety Features
- Automatic conflict detection
- 100% signal coverage verification
- Path distance calculation
- Route analysis

---

## 🔧 Advanced Features

### Path Analysis
```python
from advanced_demo import analyze_network_paths
analyze_network_paths(network)
```

### Signal Coverage Check
```python
from advanced_demo import check_signal_coverage
check_signal_coverage(network)
```

### Custom Signal Distance
```python
# Place signals 750m before CDL zones
network.place_signals_before_cdl_zones(signal_distance=750)
```

---

## 📝 Example Output

```
======================================================================
RAILWAY NETWORK SUMMARY: Central Station
======================================================================

NETWORK STATISTICS:
  • Total Nodes: 18
  • Total Edges: 14
  • Signals: 4
  • CDL Zones: 2
  • Total Track Length: 3700.00 meters

CDL ZONES (Conflict/Merge Points):
  • EXIT_B
    - Incoming tracks: SWITCH_A2, SWITCH_B2

SIGNALS:
  • SIG_SWITCH_A2_to_EXIT_B
    - Protects CDL Zone: EXIT_B
    - Distance to CDL: 500m
======================================================================
```

---

## 🚧 Generated Files

After running examples:
- `railway_station_network.png` - Multi-platform station visualization
- `complex_junction.png` - Complex junction visualization
- `network_summary.txt` - Text export of network details

---

## 🎓 Use Cases

1. **Railway Station Design**: Model and analyze station layouts
2. **Signaling Systems**: Automatic signal placement and verification
3. **Capacity Analysis**: Identify bottlenecks and conflict points
4. **Safety Audits**: Ensure proper CDL zone protection
5. **Training**: Educational tool for railway systems engineering
6. **RailML Integration**: Foundation for standard format support

---

## 🔍 How It Works

### CDL Zone Identification Algorithm
```
For each node in network:
    if in-degree(node) > 1:
        node is a CDL zone
        mark all incoming tracks
```

### Signal Placement Algorithm
```
For each CDL zone:
    For each incoming track:
        1. Traverse backward 500m from CDL
        2. Find optimal placement node
        3. Create signal with metadata
        4. Link to protected CDL zone
```

---

## 📚 Further Reading

- `README.md` - Complete documentation
- `railway_network.py` - Source code with detailed docstrings
- `example_station.py` - Practical implementation example
- `test_railway_network.py` - Test cases and validation

---

## ⚡ Performance

- **Graph Operations**: O(N + E) for CDL detection
- **Signal Placement**: O(N × E) for path traversal
- **Visualization**: Matplotlib-based rendering
- **Scalability**: Handles networks with 100+ nodes efficiently

---

## 🎨 Customization

### Custom Node Types
Add metadata to nodes for domain-specific attributes:
```python
network.add_node(RailwayNode(
    id="PLATFORM_1",
    node_type=NodeType.PLATFORM,
    position=(500, 100),
    metadata={
        "platform_number": 1,
        "length": 400,  # meters
        "height": 0.76,  # meters
        "capacity": 8  # coaches
    }
))
```

### Custom Visualization
Modify colors, sizes, and layout in `visualize()` method.

---

## 🏆 Acknowledgments

Built using:
- **NetworkX**: Graph manipulation and analysis
- **Matplotlib**: Network visualization
- **Python**: Core implementation

---

## 📞 Support

For questions or issues:
1. Check `README.md` for detailed documentation
2. Review test cases in `test_railway_network.py`
3. Examine examples in `example_station.py` and `advanced_demo.py`

---

**Created for Railway Systems Engineering**  
*Modeling, Analysis, and Signaling Automation*
