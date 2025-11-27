import time
import requests
import os

# Detect if running inside Docker
IN_DOCKER = os.environ.get("IN_DOCKER", "0") == "1"

# Define service order and ports
SERVICES = ["servicea", "serviceb", "servicec", "serviced", "servicee"]
PORTS = {"servicea":8001, "serviceb":8002, "servicec":8003, "serviced":8004, "servicee":8005}

# Build URLs dynamically
SERVICE_URLS = {}
for s in SERVICES:
    host = s if IN_DOCKER else "localhost"
    SERVICE_URLS[s] = f"http://{host}:{PORTS[s]}/process"

# Input list
initial_values = [98, 87, 65, 43, 21]

def wait_for_service(url, timeout=30):
    start = time.time()
    while True:
        try:
            resp = requests.get(url.replace("/process", "/health"), timeout=1)
            if resp.status_code == 200:
                return
        except:
            pass
        if time.time() - start > timeout:
            raise RuntimeError(f"Service {url} not responding after {timeout}s")
        time.sleep(1)

# --- Pipeline ---
print(f"Client Input: {initial_values}\n")

pipeline_results = []
pipeline_start = time.time_ns()
data = initial_values.copy()

for service, url in SERVICE_URLS.items():
    wait_for_service(url)
    t_start = time.time_ns()
    try:
        resp = requests.post(url, json={"data": data})
        resp.raise_for_status()
        resp_json = resp.json()
        data = resp_json["data"]
        work_time = resp_json.get("processing_ns", 0)
    except requests.RequestException as e:
        print(f"[ERROR] {service} request failed: {e}")
        break
    t_end = time.time_ns()
    pipeline_results.append((service, data, work_time))

pipeline_end = time.time_ns()

# --- Output ---
print("\n=== RPI SERVICES PIPELINE RESULTS ===")
print(f"Sorted Output: {data}\n")

print("=== LOGS ===")
for service, output, work_time in pipeline_results:
    print(f"Service {service.capitalize()} Output: {output} (Work Time: {work_time} ns)")

total_time = pipeline_end - pipeline_start
processing_time = sum(wt for _, _, wt in pipeline_results)
rtt_time = total_time - processing_time

print("\n=== FINAL METRICS ===")
print(f"Transaction Time (Total): {total_time} ns")
print(f"Processing Time (Work): {processing_time} ns")
print(f"RTT (Network Delay): {rtt_time} ns")
print("--------------------------------")
