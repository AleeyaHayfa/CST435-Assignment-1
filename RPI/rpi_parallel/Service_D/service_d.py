from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
import os

# Read PORT from environment variable (Docker will set this)
# Default to 9013 when running locally
PORT = int(os.getenv("PORT", 9013))

app = FastAPI()

# Define the expected JSON structure for incoming POST requests
class Numbers(BaseModel):
    numbers: list[int]           # List of integers sent by the client
    send_timestamp_ns: int       # Timestamp when the client sent the request

@app.post("/")
async def process(data: Numbers):
    # Start processing timer (high-precision monotonic clock)
    p_start = time.perf_counter_ns()

    # Timestamp when the worker receives the request
    worker_received = time.time_ns()

    # Calculate round-trip time from client → worker
    rtt_ns = worker_received - data.send_timestamp_ns

    # Compute the minimum number in the list (or None if empty)
    worker_min = min(data.numbers) if data.numbers else None

    # End processing timer
    p_end = time.perf_counter_ns()
    processing_ns = p_end - p_start

    # Return metrics and worker output
    return {
        "numbers": data.numbers,
        "worker_min": worker_min,
        "rtt_ns": rtt_ns,               # RTT to measure network overhead
        "processing_ns": processing_ns  # Time spent handling the request
    }

if __name__ == "__main__":
    # Start FastAPI server using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
