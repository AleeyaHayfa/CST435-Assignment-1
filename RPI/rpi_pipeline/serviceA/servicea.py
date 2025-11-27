import os
import time
import requests
from fastapi import FastAPI

# Basic service configuration for this worker
SERVICE_NAME = "Service A"
PORT = 8001


# Next service in the pipeline (passed by Docker environment variables)
NEXT_SERVICE = os.environ.get("NEXT_SERVICE", "serviceb")
NEXT_PORT = int(os.environ.get("NEXT_PORT", 8002))

# Detect whether running inside Docker (used for hostname resolution)
IN_DOCKER = os.environ.get("IN_DOCKER", "0") == "1"

app = FastAPI()

def wait_for_next_service():
    """
    Waits for the next service in the pipeline to be healthy before sending data.
    It checks the /health endpoint every second for up to 60 seconds.
    """
    if not NEXT_SERVICE or not NEXT_PORT:
        return
    host = NEXT_SERVICE if IN_DOCKER else "localhost"
    url = f"http://{host}:{NEXT_PORT}/process"
    start = time.time()
    while True:
        try:
            requests.get(url.replace("/process", "/health"), timeout=1)
            break
        except:
            if time.time() - start > 60:
                print(f"[WARN] {NEXT_SERVICE} not ready after 60s")
                break
            time.sleep(1)

def bubble_sort_step(data):
    n = len(data)
    for i in range(n-1):
        if data[i] > data[i+1]:
            data[i], data[i+1] = data[i+1], data[i]
    return data

@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE_NAME}

@app.post("/process")
def process(payload: dict):
    input_data = payload.get("data", [])
    start_ns = time.time_ns()
    processed = bubble_sort_step(input_data.copy())
    #time.sleep(0.01)  # simulate work
    end_ns = time.time_ns()
    work_ns = end_ns - start_ns

    output = {"service": SERVICE_NAME, "input": input_data, "data": processed, "processing_ns": work_ns}

    # If a next service exists, forward the processed output
    if NEXT_SERVICE and NEXT_PORT:
        wait_for_next_service()
        try:
            host = NEXT_SERVICE if IN_DOCKER else "localhost"
            resp = requests.post(f"http://{host}:{NEXT_PORT}/process", json={"data": processed})
            resp.raise_for_status()
            output["next"] = resp.json()
        except Exception as e:
            output["error"] = f"[ERROR] {NEXT_SERVICE} request failed: {e}"

    print(f"[{SERVICE_NAME}] processed: {processed} (Work Time: {work_ns} ns)")
    return output

if __name__ == "__main__":
    import uvicorn
     # Start FastAPI service on configured port
    uvicorn.run(app, host="0.0.0.0", port=PORT)

