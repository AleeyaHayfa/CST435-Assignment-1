from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
import os

# Get port number from environment variable (used in Docker).
# If no PORT is provided, default to 9010 when running locally.
PORT = int(os.getenv("PORT", 9010))

app = FastAPI()

# Pydantic model to define the structure of incoming JSON data.
# "numbers"      → list of integers to process
# "send_timestamp_ns" → timestamp (in nanoseconds) from the client to calculate RTT
class Numbers(BaseModel):
    numbers: list[int]
    send_timestamp_ns: int

# Main POST endpoint that processes incoming requests.
@app.post("/")
async def process(data: Numbers):
    # Start the internal processing timer
    p_start = time.perf_counter_ns()

    # Timestamp when worker receives the data (used for RTT calculation)
    worker_received = time.time_ns()

    # RTT = time worker receives request - time client sent request
    rtt_ns = worker_received - data.send_timestamp_ns

    # Compute minimum value from the list sent by the client
    # Return None if the list is empty
    worker_min = min(data.numbers) if data.numbers else None

    # End processing timer
    p_end = time.perf_counter_ns()

    # Total time spent by this worker to process the request
    processing_ns = p_end - p_start

    # Response sent back to the client
    return {
        "numbers": data.numbers,
        "worker_min": worker_min,
        "rtt_ns": rtt_ns,
        "processing_ns": processing_ns
    }

# Entry point for running the FastAPI server manually (not inside Docker)
if __name__ == "__main__":
    # Start Uvicorn server on host 0.0.0.0 and configured port
    uvicorn.run(app, host="0.0.0.0", port=PORT)
