import time
import threading

class HealthMonitor:
    def __init__(self, node_manager,pod_scheduler):
        self.node_manager = node_manager
        self.pod_scheduler = pod_scheduler
        self.heartbeats = {}
        self.lock = threading.Lock()  # Add a lock for thread safety
        threading.Thread(target=self.monitor_loop, daemon=True).start()

    def receive_heartbeat(self, node_id):
        with self.lock:  # Use the lock when updating the heartbeats dictionary
            self.heartbeats[node_id] = time.time()
            # print(f"[DEBUG] Heartbeat received for {node_id}. Updated time: {self.heartbeats[node_id]}", flush=True)
            if node_id in self.node_manager.nodes:
                self.node_manager.nodes[node_id]["status"] = "healthy"

    def monitor_loop(self):
        while True:
            now = time.time()
            with self.lock:  # Use the lock when accessing the heartbeats dictionary
                for node_id in list(self.node_manager.nodes.keys()):
                    if node_id not in self.heartbeats:
                        # Skip nodes that have not received a heartbeat yet
                        # print(f"[DEBUG] Skipping {node_id} as no heartbeat has been received yet.", flush=True)
                        continue
                    last_beat = self.heartbeats.get(node_id, 0)
                    # print(f"[DEBUG] Current time: {now}, Last heartbeat for {node_id}: {last_beat}", flush=True)
                    if now - last_beat > 20:  # 20 seconds threshold
                        # print(f"[DEBUG] Node {node_id} marked as unhealthy. Time since last heartbeat: {now - last_beat}", flush=True)
                        self.node_manager.nodes[node_id]["status"] = "unhealthy"
                        self.reschedule_pods(node_id, self.node_manager.nodes[node_id]["pods"])
                        self.node_manager.nodes[node_id]["pods"] = []  # Clear pods from failed node
            time.sleep(5)  # Check every 5 seconds
    def reschedule_pods(self, failed_node_id, pods):
        print(f"[Recovery] Attempting to reschedule pods from {failed_node_id}")
        for pod_id in pods:
            success = self.pod_scheduler.reschedule_existing_pod(pod_id)
            if not success:
                print(f"[Recovery] Failed to reschedule pod {pod_id}")