class NodeManager:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id, cpu_cores):
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = {
            "cpu": cpu_cores,
            "pods": [],
            "status": "healthy"
        }
        return True

    def list_nodes(self):
        return self.nodes
