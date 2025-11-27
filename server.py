from xmlrpc.server import SimpleXMLRPCServer
import time
import sys

# Function to export
def find_min(numbers, client_send_time_str):
    receive_time = time.time_ns()
    client_send_time = int(client_send_time_str)
    
    # The actual work
    min_val = min(numbers)
    
    # Simulate processing time if needed
    # time.sleep(0.1) 
    
    end_process_time = time.time_ns()
    
    return {
        "worker_min": min_val,
        "numbers_chunk": numbers,
        "rtt_ns": receive_time - client_send_time,
        "processing_time_ns": end_process_time - receive_time
    }

if __name__ == "__main__":
    # Default port is 8000
    port = 8000
    
    # Allow changing port via command line args (e.g., python server.py 8001)
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    server = SimpleXMLRPCServer(("0.0.0.0", port), allow_none=True)
    print(f"Worker listening on port {port}...")
    server.register_function(find_min, "find_min")
    server.serve_forever()