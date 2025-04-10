import time
import requests
import os

NODE_ID = os.environ.get("NODE_ID", "node-1")
CPU_CORES = os.environ.get("CPU", 2)
API_SERVER = os.environ.get("API_SERVER", "http://172.20.10.6:5000")

print(f"[{NODE_ID}] Using API_SERVER: {API_SERVER}",flush=True) 
# Register node only once at startup
def register_node():
    try:
        response = requests.post(f"{API_SERVER}/add_node", json={
            "node_id": NODE_ID,
            "cpu": int(CPU_CORES)
        })
        print(f"[{NODE_ID}] Registration response: {response.text}",flush=True)
    except Exception as e:
        print(f"[{NODE_ID}] Registration failed: {e}",flush=True)

# Heartbeat loop
def send_heartbeat():
    while True:
        try:
            requests.post(f"{API_SERVER}/heartbeat", json={
                "node_id": NODE_ID
            })
            print(f"[{NODE_ID}] Heartbeat sent.")
        except Exception as e:
            print(f"[{NODE_ID}] Heartbeat failed: {e}")
        time.sleep(5)

if __name__ == "__main__":
    register_node()
    send_heartbeat()
