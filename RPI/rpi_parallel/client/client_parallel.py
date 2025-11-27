from config import SERVICES
import requests
from concurrent.futures import ThreadPoolExecutor
import time

numbers = [74,56,20, 93, 16, 25, 96, 42, 93, 86, 48, 74, 26, 10, 17, 46, 75, 56, 51, 67, 22, 16, 47, 13, 32, 86, 50, 58, 72, 12, 10, 33, 87, 58, 75, 17, 38, 24, 84, 28, 18, 51, 34, 73, 26, 63, 16, 84, 76, 51, 77, 68, 45, 11, 99, 55, 21, 65, 88, 44, 57, 69, 31, 59, 28, 92, 36, 49, 71, 51, 29, 13, 15, 62, 70, 66, 35, 83, 79, 18, 41, 90, 52, 64, 53, 19, 23, 60, 78, 17, 80, 85, 39, 50, 40, 27, 14, 30, 43, 95]

def chunk_list(lst, chunks):
    k, m = divmod(len(lst), chunks)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(chunks)]

def send_request(service, data, retries=5, delay=1):
    host, port = service
    send_timestamp_ns = time.time_ns()
    payload = {"numbers": data, "send_timestamp_ns": send_timestamp_ns}

    for attempt in range(1, retries + 1):
        try:
            r = requests.post(f"http://{host}:{port}/", json=payload)
            return r.json()
        except requests.exceptions.ConnectionError:
            time.sleep(delay)  # no print here, silent retry
    raise ConnectionError(f"Failed to connect to {host}:{port} after {retries} retries")

def main():
    print("Input:", numbers)
    chunks = chunk_list(numbers, len(SERVICES))
    start_transaction_ns = time.perf_counter_ns()

    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_request, SERVICES[i], chunks[i]) for i in range(len(SERVICES))]
        for f in futures:
            results.append(f.result())

    end_transaction_ns = time.perf_counter_ns()
    transaction_time_ns = end_transaction_ns - start_transaction_ns

    print("\n--- Service Results ---")
    for i, res in enumerate(results):
        print(f"Service {chr(65+i)} received numbers: {res['numbers']}")
        print(f"Service {chr(65+i)} found min: {res['worker_min']}\n")

    global_min = min(res['worker_min'] for res in results if res['worker_min'] is not None)
    total_processing_ns = sum(res['processing_ns'] for res in results)
    total_rtt_ns = sum(res['rtt_ns'] for res in results)

    print(f"Global minimum: {global_min}")
    print(f"Transaction time (ns): {transaction_time_ns}")
    print(f"Processing time (ns): {total_processing_ns}")
    print(f"RTT (ns): {total_rtt_ns}")

if __name__ == "__main__":
    main()
