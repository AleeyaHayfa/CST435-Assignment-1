import xmlrpc.client
import time
import sys
import os

def get_service_url(index, local_port):
    """
    Decides the URL based on whether we are in Docker or Local mode.
    """
    # Check if we are running inside the Docker Compose environment
    if os.environ.get('DOCKER_MODE') == 'true':
        # Docker Mode: Connect to internal container names on port 8000
        return f"http://service{index}:8000"
    else:
        # Local Mode: Connect to localhost on the specific port
        return f"http://localhost:{local_port}"

def run_client():
    # Local ports mapping (for Local Mode)
    local_ports = [8001, 8002, 8003, 8004, 8005]
    initial_data = [98, 87, 65, 43, 21]
    
    print(f"Client Input: {initial_data}\n")
    print("=== XML-RPC PIPELINE STEPS ===")

    payload = {
        'data': initial_data,
        'processing_ns': 0
    }

    client_start_time = time.time_ns()

    # Give servers a moment to wake up if running in Docker
    if os.environ.get('DOCKER_MODE') == 'true':
        time.sleep(2)

    step = 1
    for port in local_ports:
        try:
            # Get the correct URL (localhost vs service name)
            url = get_service_url(step, port)
            
            proxy = xmlrpc.client.ServerProxy(url)
            
            # Call the server
            payload = proxy.process_data(payload)
            
            current_data = payload['data']
            step_work = payload.get('step_work_ns', 0)
            
            print(f"Service {step}: {current_data} (Work Time: {step_work} ns)")
            
            step += 1
        except Exception as e:
            print(f"Error on Service {step} ({url}): {e}")
            return

    client_end_time = time.time_ns()

    total_ns = client_end_time - client_start_time
    server_work_ns = payload['processing_ns']
    rtt_ns = total_ns - server_work_ns

    print("\n=== FINAL METRICS ===")
    print(f"Sorted Result:              {payload['data']}")
    print("-" * 40)
    print(f"Transaction Time (Total): {total_ns} ns")
    print(f"Processing Time (Work):   {server_work_ns} ns")
    print(f"RTT (Network Delay):      {rtt_ns} ns")
    print("-" * 40)

if __name__ == '__main__':
    run_client()