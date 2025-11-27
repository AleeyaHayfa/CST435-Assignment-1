from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
import os

# Get PORT from environment variable (used when running inside Docker)
# If no environment variable is provided, default to 9011 for local run
PORT = int(os.getenv("PORT", 9011))

# Create FastAPI application instance
app = FastAPI()

# Define the expected JSON structure using Pydantic
class Numbers(BaseModel):
    numbers: list[int]          # A list of integers to process
    send_timestamp_ns: int      # Timestamp when client sent the request (for RTT)

# POST endpoint to process incoming data
@app.post("/")
async def process(data: Numbers):
    # Start processing timer (high-precision)
    p_start = time.perf_counter_ns()

    # Timestamp when this worker receives the request (for RTT calculation)
    worker_received = time.time_ns()

    # Round-trip time = worker_received_time – client_sent_time
    rtt_ns = worker_received - data.send_timestamp_ns

    # Compute minimum value (to simulate "min" worker logic)
    worker_min = min(data.numbers) if data.numbers else None

    # End processing timer
    p_end = time.perf_counter_ns()

    # Total processing time inside this worker
    processing_ns = p_end - p_start

    # Return computation results
    return {
        "numbers": data.numbers,
        "worker_min": worker_min,
        "rtt_ns": rtt_ns,
        "processing_ns": processing_ns
    }

# Run the FastAPI server with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
