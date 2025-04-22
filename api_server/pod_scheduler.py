class PodScheduler:
    def __init__(self, node_manager, strategy="first_fit"):
        """
        Initialize the PodScheduler with a specific scheduling strategy.
        
        Args:
            node_manager: Manager that contains node information
            strategy: The scheduling algorithm to use - "first_fit", "best_fit", or "worst_fit"
        """
        self.node_manager = node_manager
        self.pod_id_counter = 1
        self.pod_cpu_map = {}  # pod_id -> cpu_required
        self.strategy = strategy
    
    def schedule_pod(self, cpu_required):
        """
        Schedule a pod using the selected strategy
        
        Args:
            cpu_required: CPU resources needed by the pod
            
        Returns:
            Dict with pod_id and node_id if successful, None otherwise
        """
        # Uncomment ONE of the following lines to select your scheduling strategy:
        #return self._schedule_first_fit(cpu_required)  # First-fit (original strategy)
        #return self._schedule_best_fit(cpu_required)   # Best-fit strategy
        return self._schedule_worst_fit(cpu_required)  # Worst-fit strategy
    
    def _schedule_first_fit(self, cpu_required):
        """
        First-fit scheduling algorithm - uses the first node with enough resources
        """
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                pod_id = f"pod-{self.pod_id_counter}"
                self.pod_id_counter += 1
                node["cpu"] -= cpu_required
                node["pods"].append(pod_id)
                self.pod_cpu_map[pod_id] = cpu_required
                return {"pod_id": pod_id, "node_id": node_id}
        return None
    
    def _schedule_best_fit(self, cpu_required):
        """
        Best-fit scheduling algorithm - uses the node with the smallest sufficient resource capacity
        to minimize wasted resources
        """
        best_fit_node_id = None
        smallest_sufficient_cpu = float('inf')
        
        # Find the node with the smallest sufficient CPU capacity
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                if node["cpu"] < smallest_sufficient_cpu:
                    smallest_sufficient_cpu = node["cpu"]
                    best_fit_node_id = node_id
        
        # If a suitable node was found, allocate the pod to it
        if best_fit_node_id:
            node = self.node_manager.nodes[best_fit_node_id]
            pod_id = f"pod-{self.pod_id_counter}"
            self.pod_id_counter += 1
            node["cpu"] -= cpu_required
            node["pods"].append(pod_id)
            self.pod_cpu_map[pod_id] = cpu_required
            return {"pod_id": pod_id, "node_id": best_fit_node_id}
        
        return None
    
    def _schedule_worst_fit(self, cpu_required):
        """
        Worst-fit scheduling algorithm - uses the node with the largest available resource capacity
        to maximize flexibility for future allocations
        """
        worst_fit_node_id = None
        largest_available_cpu = -1
        
        # Find the node with the largest available CPU capacity
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                if node["cpu"] > largest_available_cpu:
                    largest_available_cpu = node["cpu"]
                    worst_fit_node_id = node_id
        
        # If a suitable node was found, allocate the pod to it
        if worst_fit_node_id:
            node = self.node_manager.nodes[worst_fit_node_id]
            pod_id = f"pod-{self.pod_id_counter}"
            self.pod_id_counter += 1
            node["cpu"] -= cpu_required
            node["pods"].append(pod_id)
            self.pod_cpu_map[pod_id] = cpu_required
            return {"pod_id": pod_id, "node_id": worst_fit_node_id}
        
        return None
    
    def reschedule_existing_pod(self, pod_id):
        """
        Attempt to reschedule an existing pod to a healthy node
        
        Args:
            pod_id: ID of the pod to reschedule
            
        Returns:
            Boolean indicating success/failure of rescheduling
        """
        cpu_required = self.pod_cpu_map.get(pod_id)
        if not cpu_required:
            return False
            
        # You can change the reschedule strategy by uncommenting the desired line:
        # Using the same strategy as the initial scheduling is usually best practice
        return self._reschedule_first_fit(pod_id, cpu_required)
        # return self._reschedule_best_fit(pod_id, cpu_required)
        # return self._reschedule_worst_fit(pod_id, cpu_required)
    
    def _reschedule_first_fit(self, pod_id, cpu_required):
        """First-fit reschedule algorithm"""
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                node["cpu"] -= cpu_required
                node["pods"].append(pod_id)
                print(f"[Reschedule] Pod {pod_id} moved to {node_id}")
                return True
        return False
    
    def _reschedule_best_fit(self, pod_id, cpu_required):
        """Best-fit reschedule algorithm"""
        best_fit_node_id = None
        smallest_sufficient_cpu = float('inf')
        
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                if node["cpu"] < smallest_sufficient_cpu:
                    smallest_sufficient_cpu = node["cpu"]
                    best_fit_node_id = node_id
        
        if best_fit_node_id:
            node = self.node_manager.nodes[best_fit_node_id]
            node["cpu"] -= cpu_required
            node["pods"].append(pod_id)
            print(f"[Reschedule] Pod {pod_id} moved to {best_fit_node_id}")
            return True
        
        return False
    
    def _reschedule_worst_fit(self, pod_id, cpu_required):
        """Worst-fit reschedule algorithm"""
        worst_fit_node_id = None
        largest_available_cpu = -1
        
        for node_id, node in self.node_manager.nodes.items():
            if node["status"] == "healthy" and node["cpu"] >= cpu_required:
                if node["cpu"] > largest_available_cpu:
                    largest_available_cpu = node["cpu"]
                    worst_fit_node_id = node_id
        
        if worst_fit_node_id:
            node = self.node_manager.nodes[worst_fit_node_id]
            node["cpu"] -= cpu_required
            node["pods"].append(pod_id)
            print(f"[Reschedule] Pod {pod_id} moved to {worst_fit_node_id}")
            return True
        
        return False