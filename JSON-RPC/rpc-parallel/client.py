import jsonrpclib
import time
import os
from concurrent.futures import ThreadPoolExecutor

# Configuration: Default to 5 workers for the 5-way split
# format: "host:port,host:port,..."
DEFAULT_WORKERS = ",".join([f"localhost:{8001+i}" for i in range(5)])
WORKER_NODES_ENV = os.getenv('WORKER_NODES', DEFAULT_WORKERS)
WORKERS = [node.strip() for node in WORKER_NODES_ENV.split(',')]

def call_worker(worker_address, chunk):
    try:
        proxy = jsonrpclib.Server(f'http://{worker_address}')
        send_timestamp_ns = time.time_ns()
        
        # RPC Call
        result = proxy.map_chunk(chunk, send_timestamp_ns)
        
        # Attach the original chunk to the result for printing purposes
        result['chunk_processed'] = chunk
        return result
    except Exception as e:
        print(f"Error contacting {worker_address}: {e}")
        return None

def run_client():
    # 1. The Full Input Array (100 Numbers)
    data = [
        74, 56, 20, 93, 16, 25, 96, 42, 93, 86, 48, 74, 26, 10, 17, 46, 75, 56, 51, 67, 
        22, 16, 47, 13, 32, 86, 50, 58, 72, 12, 10, 33, 87, 58, 75, 17, 38, 24, 84, 28, 
        18, 51, 34, 73, 26, 63, 16, 84, 76, 51, 77, 68, 45, 11, 99, 55, 21, 65, 88, 44, 
        57, 69, 31, 59, 28, 92, 36, 49, 71, 51, 29, 13, 15, 62, 70, 66, 35, 83, 79, 18, 
        41, 90, 52, 64, 53, 19, 23, 60, 78, 17, 80, 85, 39, 50, 40, 27, 14, 30, 43, 95
    ]
    
    # 2. Split Data into 5 chunks
    num_workers = 5 
    k, m = divmod(len(data), num_workers)
    chunks = list(data[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(num_workers))

    # --- START TRANSACTION ---
    start_transaction_ns = time.perf_counter_ns()

    results = []
    # Use ThreadPool to send RPCs in parallel
    with ThreadPoolExecutor(max_workers=len(WORKERS)) as executor:
        futures = []
        limit = min(len(WORKERS), len(chunks))
        
        for i in range(limit):
            futures.append(executor.submit(call_worker, WORKERS[i], chunks[i]))
        
        for future in futures:
            res = future.result()
            if res:
                results.append(res)
                
    # Find Global Min
    if results:
        global_min = min(r['worker_min'] for r in results)
        total_processing = sum(r['processing_time_ns'] for r in results)
        total_rtt = sum(r['rtt_ns'] for r in results)
    else:
        global_min = 0
        total_processing = 0
        total_rtt = 0

    end_transaction_ns = time.perf_counter_ns()
    transaction_time_ns = end_transaction_ns - start_transaction_ns
    # --- END TRANSACTION ---

    # --- EXACT OUTPUT MATCHING SCREENSHOT ---
    
    print("Numbers:")
    print(f"{data}\n")
    
    print("------ JSON-RPC PARALLELIZATION ------\n")
    
    # Sort results to ensure Service 1 comes before Service 2
    results.sort(key=lambda x: x['worker_id'])

    for res in results:
        print(f"{res['worker_id']}:")
        print(f"Numbers: {res['chunk_processed']}")
        print(f"Minimum Number: {res['worker_min']}\n")

    print("------ FINAL MINIMUM NUMBER ------\n")
    print(f"Minimum Number: {global_min}\n")

    print("------ RESULT ------\n")
    print(f"Transaction Time: {transaction_time_ns} ns")
    print(f"RTT (Round Trip Time): {total_rtt} ns")
    print(f"Processing Time: {total_processing} ns")

if __name__ == '__main__':
    run_client()
