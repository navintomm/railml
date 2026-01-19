import os
import json
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# Vercel: Set Matplotlib config dir to /tmp (writable) before importing it
import os
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from railway_network import RailwayNetwork, RailwayNode, RailwayEdge, NodeType
from railml_importer import RailMLImporter, import_railml_and_analyze

app = Flask(__name__, static_folder='.')
CORS(app)

# Vercel: Use /tmp for writable directory
OUTPUT_DIR = '/tmp'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

def encode_image_to_base64(image_path):
    """Read image file and convert to base64 data URI"""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"

@app.route('/api/generate', methods=['POST'])
def generate_network():
    try:
        data = request.json
        station_name = data.get('name', 'Manual Station')
        nodes_data = data.get('nodes', [])
        edges_data = data.get('edges', [])
        signal_distance = data.get('signal_distance', 500)

        # Initialize network
        network = RailwayNetwork(station_name)

        # Add nodes
        for node_data in nodes_data:
            node_type = NodeType(node_data['type'])
            network.add_node(RailwayNode(
                id=node_data['id'],
                node_type=node_type,
                position=(node_data['x'], node_data['y'])
            ))

        # Add edges
        for edge_data in edges_data:
            network.add_edge(RailwayEdge(
                from_node=edge_data['from'],
                to_node=edge_data['to'],
                length=edge_data['length']
            ))

        # Process: Identify CDL zones and place signals
        cdl_zones = network.identify_cdl_zones()
        signals = network.place_signals_before_cdl_zones(signal_distance=signal_distance)

        # Generate visualization to /tmp
        img_name = f"manual_station_{hash(station_name) % 10000}.png"
        img_path = os.path.join(OUTPUT_DIR, img_name)
        network.visualize(save_path=img_path)

        # Convert to Base64
        web_img_path = encode_image_to_base64(img_path)

        # Prepare response
        stats = network.get_network_statistics()
        
        # Format CDL and Signal details for UI
        cdl_details = [f"{cdl} (Converging tracks: {', '.join(network.graph.predecessors(cdl))})" for cdl in cdl_zones]
        signal_details = []
        for sig_id in signals:
            sig_node = network.nodes[sig_id]
            meta = sig_node.metadata
            signal_details.append(f"{sig_id}: Protects {meta['protects_cdl_zone']} from {meta['approach_from']}")

        return jsonify({
            'success': True,
            'stats': stats,
            'image_path': web_img_path,
            'cdl_details': cdl_details,
            'signal_details': signal_details
        })

    except Exception as e:
        print(f"Error in /api/generate: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_railml():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        signal_distance = float(request.form.get('signal_distance', 500))
        
        # Save temporary file to /tmp
        temp_path = os.path.join(OUTPUT_DIR, file.filename)
        file.save(temp_path)
        
        # Import and analyze using existing module
        importer = RailMLImporter()
        network = importer.import_from_file(temp_path)
        
        # Process
        cdl_zones = network.identify_cdl_zones()
        signals = network.place_signals_before_cdl_zones(signal_distance=signal_distance)
        
        # Generate visualization to /tmp
        img_name = f"imported_{file.filename}.png"
        img_path = os.path.join(OUTPUT_DIR, img_name)
        network.visualize(save_path=img_path)
        
        # Convert to Base64
        web_img_path = encode_image_to_base64(img_path)
        
        # Prepare response
        stats = network.get_network_statistics()
        cdl_details = [f"{cdl} (Converging tracks: {', '.join(network.graph.predecessors(cdl))})" for cdl in cdl_zones]
        signal_details = []
        for sig_id in signals:
            sig_node = network.nodes[sig_id]
            meta = sig_node.metadata
            signal_details.append(f"{sig_id}: Protects {meta['protects_cdl_zone']} from {meta['approach_from']}")
            
        return jsonify({
            'success': True,
            'stats': stats,
            'image_path': web_img_path,
            'cdl_details': cdl_details,
            'signal_details': signal_details
        })

    except Exception as e:
        print(f"Error in /api/upload: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting RailML Designer Server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
