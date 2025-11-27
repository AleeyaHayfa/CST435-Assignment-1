from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
import os

# Read PORT from environment variable (used in Docker).  
# Default to 9012 when running locally.
PORT = int(os.getenv("PORT", 9012))

app = FastAPI()

# Define the request body structure using Pydantic.
# - numbers: list of integers sent by the client
# - send_timestamp_ns: client-side send timestamp (for RTT calculation)
class Numbers(BaseModel):
    numbers: list[int]
    send_timestamp_ns: int

@app.post("/")
async def process(data: Numbers):
    # Start processing timer using high-precision perf counter
    p_start = time.perf_counter_ns()

    # Timestamp when worker receives the request
    worker_received = time.time_ns()

    # Round-trip time from client → service (ns)
    rtt_ns = worker_received - data.send_timestamp_ns

    # Compute the minimum number in the list
    worker_min = min(data.numbers) if data.numbers else None

    # End processing timer
    p_end = time.perf_counter_ns()

    # Processing time inside this worker (ns)
    processing_ns = p_end - p_start

    # Return metrics + original input
    return {
        "numbers": data.numbers,
        "worker_min": worker_min,
        "rtt_ns": rtt_ns,
        "processing_ns": processing_ns
    }

# Run FastAPI server (for local and Docker)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
