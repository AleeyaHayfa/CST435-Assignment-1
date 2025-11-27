import xmlrpc.client
import time
import os
import concurrent.futures

# --- CONFIGURATION ---
NUM_WORKERS = 5
HOST_MODE = os.getenv("MODE", "LOCAL")

# --- NETWORK SETUP ---
if HOST_MODE == "DOCKER":
    WORKERS = [f"http://server-{i}:8000" for i in range(1, NUM_WORKERS + 1)]
else:
    WORKERS = [f"http://localhost:{8000+i}" for i in range(1, NUM_WORKERS + 1)]

def rpc_call(worker_url, numbers_chunk):
    try:
        proxy = xmlrpc.client.ServerProxy(worker_url)
        send_time = str(time.time_ns()) 
        return proxy.find_min(numbers_chunk, send_time)
    except Exception as e:
        print(f"Connection failed to {worker_url}: {e}")
        return None

def main():
    # --- FIX: WAIT FOR SERVERS TO WAKE UP ---
    print("Waiting 5 seconds for servers to initialize...")
    time.sleep(5) 
    # ----------------------------------------

    # 1. HARDCODED DATA INPUT
    full_list = [
        74, 56, 20, 93, 16, 25, 96, 42, 93, 86, 48, 74, 26, 10, 17, 46, 75, 56, 51, 67, 
        22, 16, 47, 13, 32, 86, 50, 58, 72, 12, 10, 33, 87, 58, 75, 17, 38, 24, 84, 28, 
        18, 51, 34, 73, 26, 63, 16, 84, 76, 51, 77, 68, 45, 11, 99, 55, 21, 65, 88, 44, 
        57, 69, 31, 59, 28, 92, 36, 49, 71, 51, 29, 13, 15, 62, 70, 66, 35, 83, 79, 18, 
        41, 90, 52, 64, 53, 19, 23, 60, 78, 17, 80, 85, 39, 50, 40, 27, 14, 30, 43, 95
    ]
    
    print(f"Numbers:\n{full_list}")
    print() 
    print("....... XML-RPC PARALLELIZATION .......")
    print()

    # Split data
    chunk_size = len(full_list) // NUM_WORKERS
    chunks = [full_list[i:i + chunk_size] for i in range(0, len(full_list), chunk_size)]
    
    start_transaction_ns = time.perf_counter_ns()
    
    sorted_results = [None] * NUM_WORKERS
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        future_to_index = {
            executor.submit(rpc_call, WORKERS[i], chunks[i]): i 
            for i in range(NUM_WORKERS)
        }
        
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                data = future.result()
                sorted_results[index] = data
            except Exception as exc:
                print(f"Service {index+1} generated an exception: {exc}")

    end_transaction_ns = time.perf_counter_ns()
    transaction_time_ns = end_transaction_ns - start_transaction_ns

    # PRINT FORMATTING
    valid_results = []
    for i, res in enumerate(sorted_results):
        if res:
            valid_results.append(res)
            print(f"Service {i+1}:")
            print(f"Numbers: {res['numbers_chunk']}")
            print(f"Minimum Number: {res['worker_min']}")
            print() 

    if valid_results:
        final_min = min(r['worker_min'] for r in valid_results)
        total_rtt = sum(r['rtt_ns'] for r in valid_results)
        total_proc = sum(r['processing_time_ns'] for r in valid_results)
    
        print("....... FINAL MINIMUM NUMBER .......")
        print()
        print(f"Minimum Number: {final_min}")
        print()
        print("....... RESULT .......")
        print()
        print(f"Transaction Time: {transaction_time_ns} ns")
        print(f"RTT (Round Trip Time): {total_rtt} ns")
        print(f"Processing Time: {total_proc} ns")

if __name__ == "__main__":
    main()