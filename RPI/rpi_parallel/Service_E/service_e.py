from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
import os

# Read PORT from environment variable (used by Docker); default to 9010 when running locally
PORT = int(os.getenv("PORT", 9014))

app = FastAPI()

# Data model for incoming JSON payload:
# - numbers: list of integers
# - send_timestamp_ns: timestamp from the client for RTT calculation
class Numbers(BaseModel):
    numbers: list[int]
    send_timestamp_ns: int

@app.post("/")
async def process(data: Numbers):
    # Start measuring processing time
    p_start = time.perf_counter_ns()

    # Worker receives timestamp to compute RTT
    worker_received = time.time_ns()
    rtt_ns = worker_received - data.send_timestamp_ns

    # Compute minimum number (or None if list is empty)
    worker_min = min(data.numbers) if data.numbers else None

    # End processing time
    p_end = time.perf_counter_ns()
    processing_ns = p_end - p_start

    # Return results to client
    return {
        "numbers": data.numbers,
        "worker_min": worker_min,
        "rtt_ns": rtt_ns,
        "processing_ns": processing_ns
    }

if __name__ == "__main__":
    # Run service using uvicorn web server
    uvicorn.run(app, host="0.0.0.0", port=PORT)
