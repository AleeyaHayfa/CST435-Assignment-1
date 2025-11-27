from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import jsonrpclib
import os
from algorithm import process_payload

# Configuration
CURRENT_PORT = int(os.getenv('PORT', 8000))
SERVICE_NAME = os.getenv('SERVICE_NAME', 'Unknown Service')
NEXT_HOST = os.getenv('NEXT_HOST', None)
NEXT_PORT = os.getenv('NEXT_PORT', None)

class PipelineService:
    def process(self, payload):
        print(f"[-] {SERVICE_NAME} processing...")
        
        # Run logic
        processed_payload = process_payload(payload, SERVICE_NAME)
        
        # Forwarding Logic
        if NEXT_HOST and NEXT_PORT:
            try:
                # Connect to next node using JSON-RPC
                next_node_url = f'http://{NEXT_HOST}:{NEXT_PORT}'
                next_node = jsonrpclib.Server(next_node_url)
                return next_node.process(processed_payload)
            except Exception as e:
                print(f"Error forwarding to {NEXT_HOST}: {e}")
                return processed_payload
        else:
            return processed_payload

def start_server():
    # '0.0.0.0' allows external connections (like from Docker)
    server = SimpleJSONRPCServer(('0.0.0.0', CURRENT_PORT))
    server.register_instance(PipelineService())
    print(f"[+] {SERVICE_NAME} (JSON-RPC) running on port {CURRENT_PORT}")
    server.serve_forever()

if __name__ == '__main__':
    start_server()
