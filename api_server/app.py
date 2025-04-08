from flask import Flask, request, jsonify
from node_manager import NodeManager

app = Flask(__name__)
node_manager = NodeManager()

@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.json
    node_id, cpu = data.get("node_id"), data.get("cpu")
    if node_manager.add_node(node_id, cpu):
        return jsonify({"message": f"Node {node_id} added successfully."}), 200
    else:
        return jsonify({"error": "Node already exists."}), 400

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify(node_manager.list_nodes())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
