import streamlit as st
import requests
import subprocess

# Set the base URL for the API
BASE_URL = "http://localhost:5000"

st.title("Node and Pod Management")

# Add Node Section
st.header("Add Node")
node_id = st.text_input("Node ID")
cpu = st.number_input("CPU", min_value=1, step=1)
if st.button("Add Node"):
    try:
        # Run the client.py script with the provided arguments
        result = subprocess.run(
            ["python", "d:/CC/cli/client.py", node_id, str(cpu)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success(f"Node {node_id} added successfully.")
        else:
            st.error(result.stderr.strip())
    except Exception as e:
        st.error(f"Error: {str(e)}")

# List Nodes Section
st.header("List Nodes")
if st.button("List Nodes"):
    response = requests.get(f"{BASE_URL}/list_nodes")
    if response.status_code == 200:
        nodes = response.json()
        for node_id, node_details in nodes.items():
            node_status = node_details.get('status', 'unknown')
            node_color = "#FFCCCC" if node_status == "unhealthy" else "blue"
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: {node_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <strong>Node ID:</strong> {node_id}<br>
                        <strong>CPU:</strong> {node_details.get('cpu', 'N/A')}<br>
                        <strong>Status:</strong> {node_status}<br>
                        <strong>Pods:</strong> {', '.join(node_details.get('pods', 'none'))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.error("Failed to fetch nodes.")

# Launch Pod Section
st.header("Launch Pod")
pod_cpu = st.number_input("Pod CPU", min_value=1, step=1, key="pod_cpu")
if st.button("Launch Pod"):
    response = requests.post(f"{BASE_URL}/launch_pod", json={"cpu": pod_cpu})
    if response.status_code == 200:
        st.success(response.json().get("message"))
    else:
        st.error(response.json().get("error"))