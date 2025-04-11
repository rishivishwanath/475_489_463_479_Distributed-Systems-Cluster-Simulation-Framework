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
            if node_id in self.node_manager.nodes:
                # Only update the status if it is not already "healthy"
                if self.node_manager.nodes[node_id]["status"] != "healthy":
                    self.node_manager.nodes[node_id]["status"] = "healthy"

    def monitor_loop(self):
        while True:
            now = time.time()
            with self.lock:  # Use the lock when accessing the heartbeats dictionary
                for node_id in list(self.node_manager.nodes.keys()):
                    if node_id not in self.heartbeats:
                        continue
                    last_beat = self.heartbeats.get(node_id, 0)
                    if now - last_beat > 10:  # 20 seconds threshold
                        self.node_manager.nodes[node_id]["status"] = "unhealthy"
                        for pod in self.node_manager.nodes[node_id]["pods"]:
                            print(f"Pod CPU required: {pod}")
                            print(self.pod_scheduler.pod_cpu_map.get(pod, 0))
                        total_cpu_used = sum(self.pod_scheduler.pod_cpu_map.get(pod_id, 0) for pod_id in self.node_manager.nodes[node_id]["pods"])
                        self.node_manager.nodes[node_id]["cpu"] = self.node_manager.nodes[node_id].get("cpu", 0) + total_cpu_used
                        self.reschedule_pods(node_id, self.node_manager.nodes[node_id]["pods"])
                        self.node_manager.nodes[node_id]["pods"] = []  # Clear pods from failed node
            time.sleep(5)  # Check every 5 seconds
    def reschedule_pods(self, failed_node_id, pods):
        print(f"[Recovery] Attempting to reschedule pods from {failed_node_id}")
        for pod_id in pods:
            success = self.pod_scheduler.reschedule_existing_pod(pod_id)
            if not success:
                print(f"[Recovery] Failed to reschedule pod {pod_id}")