import time
import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def bubble_sort_pass(payload):
    p_start = time.time_ns()

    numbers = payload.get('data', [])
    n = len(numbers)
    
    for i in range(n - 1):
        if numbers[i] > numbers[i + 1]:
            numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]

    time.sleep(0.01)
    p_end = time.time_ns()
    my_work = p_end - p_start
    
    if 'processing_ns' not in payload:
        payload['processing_ns'] = 0
    
    payload['processing_ns'] += my_work
    payload['step_work_ns'] = my_work # Track step time specifically
    payload['data'] = numbers
    
    print(f"Processed Data: {numbers} | Work Time: {my_work} ns")
    return payload

def start_server(port):
    # Listen on all interfaces (0.0.0.0)
    with SimpleXMLRPCServer(('0.0.0.0', port), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()
        server.register_function(bubble_sort_pass, 'process_data')
        print(f"XML-RPC Service listening on port {port}...")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    start_server(port)