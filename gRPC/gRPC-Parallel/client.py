import grpc
import time
import random
import mapreduce_pb2, mapreduce_pb2_grpc
from concurrent.futures import ThreadPoolExecutor

WORKERS = [
        "localhost:50051",
        "localhost:50052",
        "localhost:50053",
        "localhost:50054",
        "localhost:50055"
]

FIXED_NUMBERS = [
        74, 56, 20, 93, 16, 25, 96, 42, 93, 86,
        48, 74, 26, 10, 17, 46, 75, 56, 51, 67,
        22, 16,47, 13, 32, 86, 50, 58, 72, 12,
        10, 33, 87, 58, 75, 17, 38, 24, 84, 28,
        18, 51, 34, 73, 26, 63, 16, 84, 76, 51,
        77, 68, 45, 11, 99, 55, 21, 65, 88, 44,
        57, 69, 31, 59, 28, 92, 36, 49, 71, 51,
        29, 13, 15, 62, 70, 66, 35, 83, 79, 18,
        41, 90, 52, 64, 53, 19, 23, 60, 78, 17,
        80, 85, 39, 50, 40, 27, 14, 30, 43, 95,
]

def split_numbers(numbers, num_workers):
        size = len(numbers) // num_workers
        return [numbers[i:i+size] for i in range(0, len(numbers), size)]
  
  def map_call(worker, nums):
        send_timestamp_ns =  time.time_ns()
        with grpc.insecure_channel(worker) as channel:
                stub = mapreduce_pb2_grpc.MapReduceStub(channel)
                return stub.Map(
                        mapreduce_pb2.MapRequest(
                                numbers=nums,
                                send_timestamp_ns=send_timestamp_ns
                        )
                )

def reduce_call(worker_mins):
        with grpc.insecure_channel(WORKERS[0]) as channel:
                stub = mapreduce_pb2_grpc.MapReduceStub(channel)
                return stub.Reduce(
                        mapreduce_pb2.ReduceRequest(worker_mins=worker_mins)
                )

def run_distributed():
        numbers = FIXED_NUMBERS
        print("Numbers:\n", numbers)

        chunks = split_numbers(numbers, len(WORKERS))

        start_transaction_ns = time.perf_counter_ns()

        rtts = []
        processing_times = []
        worker_mins = []

        with ThreadPoolExecutor(max_workers= len(WORKERS)) as exe:
                futures = []
                for i, chunk in enumerate(chunks):
                        futures.append(exe.submit(map_call, WORKERS[i], chunk))

                for f in futures:
                        res = f.result()
                        worker_mins.append(res.worker_min)
                        rtts.append(res.rtt_ns)
                        processing_times.append(res.processing_time_ns)

        reduce_res = reduce_call(worker_mins)

        end_transaction_ns = time.perf_counter_ns()
        transaction_time_ns = end_transaction_ns - start_transaction_ns
       
        print("\n------- GRPC PARALLELIZATION -------\n")
        for i, (chunk, min_val) in enumerate(zip(chunks, worker_mins), 1):
                print(f"Service {i}: ")
                print(f"Numbers: {chunk}")
                print(f"Minimum Number: {min_val}\n")

        print("\n------- FINAL MINIMUM NUMBER ------\n")
        print(f"Minimum Number: {reduce_res.final_min}\n")

        print("------- RESULT -------\n")
        print(f"Transaction Time: {transaction_time_ns} ns")
        print(f"RTT (Round Trip Time): {sum(rtts)} ns")
        print(f"Processing Time: {sum(processing_times)} ns")

if __name__ == "__main__":
        run_distributed()
