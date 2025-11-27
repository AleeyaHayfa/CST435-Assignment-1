from concurrent import futures
import grpc
import time
import mapreduce_pb2, mapreduce_pb2_grpc

class MapReduceServicer(mapreduce_pb2_grpc.MapReduceServicer):

        def Map(self, request, context):

                #Time when worker starts processing
                start_processing_ns = time.perf_counter_ns()

                # RTT = times_received - time_sent
                worker_received_ns = time.time_ns()
                rtt_ns = worker_received_ns - request.send_timestamp_ns

                #Actual task: Compute minimum
                worker_min = min(request.numbers)

                #End processing time
                end_processing_ns = time.perf_counter_ns()
                processing_time_ns = end_processing_ns - start_processing_ns


                return mapreduce_pb2.MapReply(
                        worker_min=worker_min,
                        rtt_ns=rtt_ns,
                        processing_time_ns=processing_time_ns
                )

        def Reduce(self, request, context):
                # final minimum from all workers
                return mapreduce_pb2.ReduceReply(
                        final_min=min(request.worker_mins)
                )

def serve(port):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        mapreduce_pb2_grpc.add_MapReduceServicer_to_server(MapReduceServicer(>        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"Server started on port {port}")
        server.wait_for_termination()

if __name__ == "__main__":
        import sys
        port = int(sys.argv[1]) if len(sys.argv) >  1 else 50051
        serve(port)
