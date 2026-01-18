"""
Demo: Import RailML File and Analyze
Shows how to import a RailML file, find CDL zones, and place signals
"""

from railml_importer import import_railml_and_analyze
import os


def main():
    """
    Demonstrate RailML import workflow
    """
    
    print("\n" + "="*70)
    print("RAILML IMPORT DEMONSTRATION")
    print("="*70)
    
    # Path to example RailML file
    railml_file = "example_station.railml"
    
    if not os.path.exists(railml_file):
        print(f"\n⚠ Error: {railml_file} not found!")
        print("Please ensure the example RailML file exists.")
        return
    
    print(f"\n📄 Processing RailML file: {railml_file}")
    print("="*70)
    
    # Import and analyze (完整的工作流程)
    network = import_railml_and_analyze(
        railml_file=railml_file,
        signal_distance=500  # Place signals 500m before CDL zones
    )
    
    # Display detailed summary
    print("\n" + network.export_summary())
    
    # Visualize the imported network
    print("\n" + "="*70)
    print("GENERATING VISUALIZATION")
    print("="*70)
    
    output_file = "imported_station_network.png"
    network.visualize(
        figsize=(18, 12),
        save_path=output_file
    )
    
    print(f"\n✓ Visualization saved: {output_file}")
    
    # Show what was accomplished
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE!")
    print("="*70)
    print("""
What just happened:
1. ✓ Imported RailML file (industry standard format)
2. ✓ Parsed tracks, switches, platforms, connections
3. ✓ Built railway network graph automatically
4. ✓ Identified CDL zones (merge points)
5. ✓ Placed safety signals 500m before each CDL zone
6. ✓ Generated visualization
7. ✓ Created detailed report

This is the REAL-WORLD workflow!
Just upload any RailML file and get automatic safety analysis!
""")


if __name__ == "__main__":
    main()
