from config import SERVICES
import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Input dataset (100 numbers)
numbers = [74,56,20, 93, 16, 25, 96, 42, 93, 86, 48, 74, 26, 10, 17, 46, 75, 56, 51, 67, 22, 16, 47, 13, 32, 86, 50, 58, 72, 12, 10, 33, 87, 58, 75, 17, 38, 24, 84, 28, 18, 51, 34, 73, 26, 63, 16, 84, 76, 51, 77, 68, 45, 11, 99, 55, 21, 65, 88, 44, 57, 69, 31, 59, 28, 92, 36, 49, 71, 51, 29, 13, 15, 62, 70, 66, 35, 83, 79, 18, 41, 90, 52, 64, 53, 19, 23, 60, 78, 17, 80, 85, 39, 50, 40, 27, 14, 30, 43, 95]

def chunk_list(lst, chunks):
    """
    Splits a list into 'chunks' number of even sublists.
    Used to divide the numbers evenly among the parallel workers.
    """
    k, m = divmod(len(lst), chunks)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(chunks)]

def send_request(service, data, retries=5, delay=1):
    """
    Sends the chunk of numbers to a service.

    - service: (host, port)
    - data: list of numbers assigned to that service
    - retries: number of retry attempts if service is not reachable
    - delay: wait time between retries

    Returns the JSON response from the worker service.
    """
    host, port = service
    send_timestamp_ns = time.time_ns()   # timestamp used by worker to compute RTT
    payload = {"numbers": data, "send_timestamp_ns": send_timestamp_ns}

    # Retry logic to handle connection errors
    for attempt in range(1, retries + 1):
        try:
            r = requests.post(f"http://{host}:{port}/", json=payload)
            return r.json()
        except requests.exceptions.ConnectionError:
            time.sleep(delay)  # silent retry with no print

    # Failed after all retries
    raise ConnectionError(f"Failed to connect to {host}:{port} after {retries} retries")

def main():
    print("Input:", numbers)

    # Split dataset into equal parts based on number of worker services
    chunks = chunk_list(numbers, len(SERVICES))

    # Start total transaction timer
    start_transaction_ns = time.perf_counter_ns()

    results = []

    # Use thread pool to send requests to all services in parallel
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(send_request, SERVICES[i], chunks[i])
            for i in range(len(SERVICES))
        ]
        # Collect all results from the futures
        for f in futures:
            results.append(f.result())

    # End transaction timer
    end_transaction_ns = time.perf_counter_ns()
    transaction_time_ns = end_transaction_ns - start_transaction_ns

    print("\n--- Service Results ---")
    # Display results from each service
    for i, res in enumerate(results):
        print(f"Service {chr(65+i)} received numbers: {res['numbers']}")
        print(f"Service {chr(65+i)} found min: {res['worker_min']}\n")

    # Compute global minimum across all worker minimums
    global_min = min(res['worker_min'] for res in results if res['worker_min'] is not None)

    # Sum processing time and round-trip time across all services
    total_processing_ns = sum(res['processing_ns'] for res in results)
    total_rtt_ns = sum(res['rtt_ns'] for res in results)

    # Final output
    print(f"Global minimum: {global_min}")
    print(f"Transaction time (ns): {transaction_time_ns}")
    print(f"Processing time (ns): {total_processing_ns}")
    print(f"RTT (ns): {total_rtt_ns}")

if __name__ == "__main__":
    main()
