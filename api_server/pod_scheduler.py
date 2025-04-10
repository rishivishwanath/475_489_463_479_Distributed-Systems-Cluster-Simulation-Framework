class PodScheduler:
    def __init__(self, node_manager):
        self.node_manager = node_manager
        self.pod_id_counter = 1
        self.pod_cpu_map = {}  # pod_id -> cpu_required

    def schedule_pod(self, cpu_required):
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                pod_id = f"pod-{self.pod_id_counter}"
                self.pod_id_counter += 1
                node["cpu"] -= cpu_required
                node["pods"].append(pod_id)
                return {"pod_id": pod_id, "node_id": node_id}
        return None
    
    def reschedule_existing_pod(self, pod_id):
        cpu_required = self.pod_cpu_map.get(pod_id)
        if not cpu_required:
            return False
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                node["cpu"] -= cpu_required
                node["pods"].append(pod_id)
                print(f"[Reschedule] Pod {pod_id} moved to {node_id}")
                return True
        return False
