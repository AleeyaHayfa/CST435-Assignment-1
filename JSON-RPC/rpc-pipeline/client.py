import jsonrpclib
import time
import os

ENTRY_HOST = os.getenv('ENTRY_HOST', 'localhost')
ENTRY_PORT = int(os.getenv('ENTRY_PORT', 8001))

def run_client():
    initial_data = [98, 87, 65, 43, 21]
    
    payload = {
        'data': initial_data,
        'processing_ns': 0,
        'trace': [] 
    }

    # --- START TRANSACTION ---
    client_start_time = time.time_ns()
    
    try:
        # Connect using JSON-RPC
        url = f'http://{ENTRY_HOST}:{ENTRY_PORT}'
        proxy = jsonrpclib.Server(url)
        response = proxy.process(payload)
    except Exception as e:
        print(f"Connection Error: {e}")
        return
        
    client_end_time = time.time_ns()
    # --- END TRANSACTION ---

    # Calculations
    total_ns = client_end_time - client_start_time
    server_work_ns = response['processing_ns']
    rtt_ns = total_ns - server_work_ns

    # --- DISPLAY OUTPUT ---
    print(f"Client input: {initial_data}\n")
    print("========== JSON-RPC PIPELINE STEPS ==============")
    
    for step in response['trace']:
        print(f"[{step['service']}] Result: {step['result_snapshot']} | Work Time: {step['work_time']} ns")

    print("\n" + "="*30)
    print("FINAL METRICS")
    print("="*30)
    print(f"Sorted result       : {response['data']}")
    print(f"Transaction Time    : {total_ns} ns")
    print(f"Processing Time     : {server_work_ns} ns")
    print(f"RTT (Network Delay) : {rtt_ns} ns")
    print("="*30)

if __name__ == '__main__':
    run_client()
