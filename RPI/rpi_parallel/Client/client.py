#!/usr/bin/env python3
"""
RPI Client — MapReduce Min (calls 5 services)
"""

import socket
import json
import time

# 100 numbers
NUMBERS = [
    74,56,20,93,16,25,96,42,93,86,48,74,26,10,17,46,75,56,51,67,
    22,16,47,13,32,86,50,58,72,12,10,33,87,58,75,17,38,24,84,28,
    18,51,34,73,26,63,16,84,76,51,77,68,45,11,99,55,21,65,88,44,
    57,69,31,59,28,92,36,49,71,51,29,13,15,62,70,66,35,83,79,18,
    41,90,52,64,53,19,23,60,78,17,80,85,39,50,40,27,14,30,43,95
]

# Worker addresses (localhost + ports 9001–9005)
WORKERS = [
    ("localhost", 9001),
    ("localhost", 9002),
    ("localhost", 9003),
    ("localhost", 9004),
    ("localhost", 9005),
]

BUFFER_SIZE = 65536

def chunk_list(lst, n):
    """Split list into chunks of size n"""
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def call_worker(host, port, numbers_chunk):
    """Send numbers to a worker and receive JSON reply"""
    payload = json.dumps({
        "numbers": numbers_chunk,
        "send_timestamp_ns": time.time_ns()
    }).encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(payload)

    data = b""
    while True:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            break
        data += chunk
    sock.close()

    return json.loads(data.decode())

def main():
    # Split numbers into 5 chunks
    chunks = chunk_list(NUMBERS, len(NUMBERS)//len(WORKERS))

    t_start = time.perf_counter_ns()  # Start transaction timer
    results = []

    # Call each worker sequentially (can be parallelized later)
    for (host, port), sublist in zip(WORKERS, chunks):
        resp = call_worker(host, port, sublist)
        results.append(resp)
    t_end = time.perf_counter_ns()
    transaction_time_ns = t_end - t_start

    # Print per-worker results
    print("\n=== WORKER RESULTS ===")
    for i, r in enumerate(results, 1):
        print(f"Worker {i}:")
        print(f"  Min: {r['worker_min']}")
        print(f"  RTT (ns): {r['rtt_ns']}")
        print(f"  Processing Time (ns): {r['processing_time_ns']}")

    # Compute global minimum
    global_min = min(r['worker_min'] for r in results)
    print("\n=== FINAL RESULT ===")
    print(f"Global Minimum: {global_min}")
    print(f"Transaction Time (ns): {transaction_time_ns}")

if __name__ == "__main__":
    main()
