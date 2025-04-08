import subprocess
import sys

def add_node(node_id, cpu):
    subprocess.run([
        "docker", "run", "-d",
        "-e", f"NODE_ID={node_id}",
        "-e", f"CPU={cpu}",
        "--name", node_id,
        "cluster_node_image"  # Build using: docker build -t cluster_node_image .
    ])

if __name__ == '__main__':
    node_id = sys.argv[1]
    cpu = sys.argv[2]
    add_node(node_id, cpu)
