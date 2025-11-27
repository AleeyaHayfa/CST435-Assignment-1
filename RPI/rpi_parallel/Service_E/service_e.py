from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time
import os

# PORT from environment variable (Docker sets this), default to 9010 for local
PORT = int(os.getenv("PORT", 9014))

app = FastAPI()

class Numbers(BaseModel):
    numbers: list[int]
    send_timestamp_ns: int

@app.post("/")
async def process(data: Numbers):
    p_start = time.perf_counter_ns()
    worker_received = time.time_ns()
    rtt_ns = worker_received - data.send_timestamp_ns
    worker_min = min(data.numbers) if data.numbers else None
    p_end = time.perf_counter_ns()
    processing_ns = p_end - p_start

    return {
        "numbers": data.numbers,
        "worker_min": worker_min,
        "rtt_ns": rtt_ns,
        "processing_ns": processing_ns
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
