import time
import grpc
import sys
import pipeline_pb2, pipeline_pb2_grpc

WORKERS = [
        ("worker1", 50051),
        ("worker2", 50052),
        ("worker3", 50053),
        ("worker4", 50054),
        ("worker5", 50055),

]

NUMBERS = [98, 87, 65, 43, 21]

def call_service(address, numbers, cumulative):

        channel = grpc.insecure_channel(f"{address[0]}:{address[1]}")
        stub = pipeline_pb2_grpc.PipelineStub(channel)

        req = pipeline_pb2.PipelineRequest(
                numbers=numbers,
                cumulative_processing=cumulative
        )
        resp = stub.Step(req)
        return resp
def run_pipeline():

        print(f"Client Number: {NUMBERS}\n")
        print("=== GRPC PIPELINE STEPS ===\n")

        numbers = NUMBERS[:]
        cumulative = 0
        work_times = []

        pipeline_start = time.time_ns()

        for i, addr in enumerate(WORKERS):

                resp = call_service(addr, numbers, cumulative)

                numbers = list(resp.numbers)
                cumulative = resp.cumulative_processing
                work_times.append(resp.work_time)

                print(f"Worker {i+1}: {numbers} (Work Time: {resp.work_time} ns)")

        pipeline_end = time.time_ns()

        transaction_time = pipeline_end - pipeline_start
        processing_time = sum(work_times)
        rtt =  transaction_time - processing_time

        print("\n=== FINAL METRICS ===\n")
        print(f"Sorted Result: {numbers}")
        print("--------------------------------------")
        print(f"Transaction Time (Total): {transaction_time} ns")
        print(f"Processing Time (Work): {processing_time} ns")
        print(f"RTT (Network Delay): {rtt} ns")
        print("--------------------------------------")

if __name__ == "__main__":
        run_pipeline()
