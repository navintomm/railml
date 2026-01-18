# Railway Network System

A Python-based railway systems engineering application using NetworkX to model railway stations with automatic CDL (Conflicting Direction Logic) zone detection and signal placement.

## Features

✅ **Directed Graph Modeling**: Represents railway networks as directed graphs with:
- Track nodes
- Switch nodes (turnouts)
- Platform nodes
- Entry/exit points

✅ **CDL Zone Detection**: Automatically identifies zones where tracks merge (nodes with in-degree > 1)

✅ **Automatic Signal Placement**: Places signal elements 500 meters (configurable) before each CDL zone

✅ **Network Visualization**: Generates visual representations of the railway network with:
- Color-coded node types
- Track distances
- Signal positions
- CDL zone highlights

✅ **Network Analysis**: Provides statistics and summaries of:
- Total track length
- Number of switches, platforms, signals
- CDL zone details

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Example Station

```bash
python example_station.py
```

This will:
1. Create a realistic multi-platform railway station
2. Identify all CDL zones (merge points)
3. Automatically place signals 500m before each CDL zone
4. Generate a visualization (saved as `railway_station_network.png`)
5. Print a detailed network summary

### Creating Your Own Railway Network

```python
from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType

# Initialize network
network = RailwayNetwork("My Station")

# Add nodes
network.add_node(RailwayNode(
    id="TRACK_1",
    node_type=NodeType.TRACK,
    position=(0, 0)
))

network.add_node(RailwayNode(
    id="SWITCH_1",
    node_type=NodeType.SWITCH,
    position=(100, 50)
))

# Add track connections
network.add_edge(RailwayEdge(
    from_node="TRACK_1",
    to_node="SWITCH_1",
    length=150  # meters
))

# Identify CDL zones
cdl_zones = network.identify_cdl_zones()

# Place signals automatically
signals = network.place_signals_before_cdl_zones(signal_distance=500)

# Visualize
network.visualize(save_path="my_station.png")

# Get summary
print(network.export_summary())
```

## Node Types

- **TRACK**: Standard track segment
- **SWITCH**: Railway switch/turnout where tracks diverge or converge
- **SIGNAL**: Signal element (auto-placed or manually added)
- **CDL_ZONE**: Conflicting Direction Logic zone (track merge point)
- **PLATFORM**: Station platform
- **ENTRY_POINT**: Entry point to the network
- **EXIT_POINT**: Exit point from the network

## CDL Zones

A **CDL (Conflicting Direction Logic) Zone** is identified as any node where:
- Multiple tracks converge (in-degree > 1)
- Potential conflict points requiring signaling protection

The system automatically:
1. Identifies all CDL zones in the network
2. Calculates optimal signal placement (default: 500m before zone)
3. Creates signal nodes along approach tracks
4. Links signals to the CDL zones they protect

## Signal Placement Algorithm

For each CDL zone:
1. Identify all incoming approach tracks
2. For each approach:
   - Traverse backward 500m (configurable) from the CDL zone
   - Find the optimal node for signal placement
   - Create a signal node with metadata linking to the CDL zone
3. Signals include metadata:
   - Protected CDL zone ID
   - Approach track
   - Distance to CDL zone

## Network Statistics

The system provides comprehensive statistics:
- Total nodes and edges
- Count by node type (tracks, switches, signals, etc.)
- Total track length in meters
- Detailed CDL zone analysis
- Signal placement details

## Example Output

```
======================================================================
RAILWAY NETWORK SUMMARY: Central Station
======================================================================

NETWORK STATISTICS:
  • Total Nodes: 18
  • Total Edges: 15
  • Track Nodes: 5
  • Switches: 4
  • Signals: 2
  • CDL Zones: 1
  • Platforms: 4
  • Total Track Length: 3450.00 meters

CDL ZONES (Conflict/Merge Points):
  • EXIT_B
    - Incoming tracks: SWITCH_A2, SWITCH_B2

SIGNALS:
  • SIG_SWITCH_A2_to_EXIT_B
    - Protects CDL Zone: EXIT_B
    - Approach from: SWITCH_A2
    - Distance to CDL: 500m
  • SIG_SWITCH_B2_to_EXIT_B
    - Protects CDL Zone: EXIT_B
    - Approach from: SWITCH_B2
    - Distance to CDL: 500m

======================================================================
```

## Visualization

The generated visualization shows:
- **Blue nodes**: Track segments
- **Orange nodes**: Switches
- **Green nodes**: Signals
- **Red nodes**: CDL zones
- **Purple nodes**: Platforms
- **Cyan nodes**: Entry points
- **Light green nodes**: Exit points

Edges show track distances in meters.

## Architecture

```
railway_network.py       # Core module with RailwayNetwork class
example_station.py       # Example implementation
requirements.txt         # Python dependencies
README.md               # This file
```

## Technical Details

- **Graph Library**: NetworkX (directed graph - DiGraph)
- **Visualization**: Matplotlib
- **Data Structures**: Python dataclasses for type safety
- **Distance Calculation**: Path-based distance accumulation along edges

## Railway Systems Engineering Concepts

This system models key railway engineering concepts:

1. **Interlocking**: CDL zones represent points requiring interlocking logic
2. **Signaling**: Automatic placement ensures safe stopping distances
3. **Track Topology**: Directed graph naturally represents unidirectional tracks
4. **Safety Zones**: 500m distance allows for braking and signal sighting

## Future Enhancements

Potential extensions:
- Route conflict detection
- Train path planning
- Platform allocation optimization
- Speed restrictions and braking curves
- Integration with RailML format
- Real-time train position tracking
- Capacity analysis

## License

MIT License - Feel free to use and modify for your railway engineering projects!

## Author

Created for Railway Systems Engineering applications using Python and NetworkX.
