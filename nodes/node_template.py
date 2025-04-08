import time
import requests
import os

NODE_ID = os.environ.get("NODE_ID", "node-1")
CPU_CORES = os.environ.get("CPU", 2)

while True:
    try:
        requests.post("http://host.docker.internal:5000/add_node", json={
            "node_id": NODE_ID,
            "cpu": int(CPU_CORES)
        })
    except Exception as e:
        print("Node registration failed. Retrying...")
    time.sleep(30)  # Simulate heartbeat
