import time
from concurrent import futures
import grpc
import pipeline_pb2
import pipeline_pb2_grpc
import sys

def bubble_sort(numbers):
 arr = numbers[:]
 n =  len(arr)

 for i in range(n):
   swapped = False
   for j in range(0, n-i-1):
     if arr[j] > arr[j+1]:
        arr[j], arr[j+1] = arr[j+1], arr[j]
        swapped = True
   if not swapped:
       break
 return arr

class PipelineServicer(pipeline_pb2_grpc.PipelineServicer):

 def __init__(self, service_id):
   self.service_id = service_id
 def Step(self, request, context):

   numbers = list(request.numbers)
   cumulative = request.cumulative_processing

   start_ns = time.time_ns()
   sorted_numbers = bubble_sort(numbers)

   time.sleep(0.01)

   end_ns = time.time_ns()

   work_time = end_ns - start_ns
   cumulative += work_time

   return pipeline_pb2.PipelineResponse(
     numbers=sorted_numbers,
     cumulative_processing=cumulative,
     work_time=work_time
   )

def serve(service_id, port):
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
   pipeline_pb2_grpc.add_PipelineServicer_to_server(
     PipelineServicer(service_id), server
   )
   server.add_insecure_port(f"[::]:{port}")
   server.start()
   print(f"Service {service_id} started on port {port}")
   server.wait_for_termination()

if __name__ == "__main__":
   service_id = int(sys.argv[1])
   port = int(sys.argv[2])
   serve(service_id, port)
