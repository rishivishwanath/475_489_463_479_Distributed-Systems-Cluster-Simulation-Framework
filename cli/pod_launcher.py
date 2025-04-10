import requests
import sys

def launch_pod(cpu_required):
    res = requests.post("http://localhost:5000/launch_pod", json={"cpu": int(cpu_required)})
    print(res.json())

if __name__ == '__main__':
    cpu_required = sys.argv[1]
    launch_pod(cpu_required)
