from flask import Flask, request, jsonify
from node_manager import NodeManager
from pod_scheduler import PodScheduler
from health_monitor import HealthMonitor  # in next step

app = Flask(__name__)
node_manager = NodeManager()
pod_scheduler = PodScheduler(node_manager)
health_monitor = HealthMonitor(node_manager, pod_scheduler)

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

@app.route('/launch_pod', methods=['POST'])
def launch_pod():
    data = request.json
    cpu = data.get("cpu")
    result = pod_scheduler.schedule_pod(cpu)
    if result:
        return jsonify({"message": "Pod scheduled", **result}), 200
    else:
        return jsonify({"error": "No suitable node found"}), 400

pod_scheduler = PodScheduler(node_manager)
health_monitor = HealthMonitor(node_manager, pod_scheduler)

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    node_id = data.get("node_id")
    health_monitor.receive_heartbeat(node_id)
    return jsonify({"message": f"Heartbeat received from {node_id}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
