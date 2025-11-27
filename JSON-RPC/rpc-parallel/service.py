from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import time
import os

# Configuration
PORT = int(os.getenv('PORT', 8000))
SERVICE_NAME = os.getenv('SERVICE_NAME', 'Unknown Worker')

class WorkerService:
    def map_chunk(self, numbers, send_timestamp_ns):
        """
        MapReduce Map Phase (Find Minimum)
        """
        # 1. Start Measuring Worker Processing Time
        p_start = time.perf_counter_ns()

        # 2. Compute RTT 
        worker_received = time.time_ns()
        rtt_ns = worker_received - send_timestamp_ns

        # 3. Do the Task (Find Min)
        print(f"[-] {SERVICE_NAME} received chunk of size {len(numbers)}")
        worker_min = min(numbers)

        # 4. Stop Processing Timer
        p_end = time.perf_counter_ns()

        # 5. Calculate Actual Worker Processing Time
        processing_ns = p_end - p_start

        # 6. Return Results
        return {
            "worker_id": SERVICE_NAME,
            "worker_min": worker_min,
            "rtt_ns": rtt_ns,
            "processing_time_ns": processing_ns
        }

def start_server():
    server = SimpleJSONRPCServer(('0.0.0.0', PORT))
    server.register_instance(WorkerService())
    print(f"[+] {SERVICE_NAME} listening on port {PORT}...")
    server.serve_forever()

if __name__ == '__main__':
    start_server()
