# CST435: Distributed Systems Communication Protocol Benchmarking

## Parallel and Cloud Computing - Assignment 1

---

## 🚀 Introduction

This project explores the performance implications of various communication protocols—**gRPC**, **JSON-RPC**, **XML-RPC**, **WebSocket**, and **RPI** (Custom Remote Procedure Invocation)—in a modern distributed microservices architecture. We constructed a system with five service nodes deployed across both **Localhost** and **Docker** environments to benchmark their efficiency.

### Problem / Motivation

The core challenge addressed is determining how protocol overhead, network latency, and deployment environment (Localhost vs. Docker) influence execution performance in distributed algorithms. The goal is to empirically identify the most efficient protocol setup for scalable and containerized applications by measuring **Round Trip Time (RTT)** and **Transaction Time**.

---

## 🎯 Project Objectives

1.  **Demonstrate Distributed Patterns:** Implement **MapReduce** (for data parallelization) and **Bubble Sort** (for pipelined task execution) across 5 service nodes.
2.  **Compare Protocols:** Benchmark gRPC against JSON-RPC, WebSocket, XML-RPC, and RPI in terms of performance and execution speed.
3.  **Evaluate Performance:** Measure **Transaction Time** and **Round Trip Time (RTT)** in both Localhost and Docker environments to evaluate overall system performance.

---

## 💻 Methodology & System Architecture

We implemented two distinct distributed patterns utilizing 5 services and 1 client:

### 1. Data Parallelization (MapReduce)

*   **Goal:** Efficiently find the **global minimum number** from a large array of integers.
*   **Algorithm:**
    1.  **Split (Client):** Generate a large list of integers and partition it into **5 equal chunks**.
    2.  **Map (Distribution):** Send one chunk to each of the 5 Services **simultaneously** (asynchronously).
    3.  **Process (Workers):** Each Service independently finds its **local minimum value**.
    4.  **Reduce (Aggregation):** The Client collects the 5 local minimums and compares them to find the **Final Minimum Number**.

### 2. Function Pipelining (Bubble Sort)

*   **Goal:** Sort a list of numbers by passing it sequentially through a chain of services.
*   **Algorithm:**
    1.  **Initiation:** The Client sends an unsorted list to Service 1.
    2.  **Passes 1-4 (Services 1-4):** Each service performs the next sorting pass of the Bubble Sort algorithm and forwards the partially sorted list to the next service in the chain.
    3.  **Finalization (Service 5):** Service 5 performs the final sort verification and returns the fully sorted list to the Client.

### Deployment Environments

*   **Localhost:** Services run manually in separate Ubuntu terminals (WSL) within a shared Python virtual environment. This served as the baseline with minimal networking overhead.
*   **Docker Desktop:** Each service is containerized and connected via Docker's internal virtual network, introducing realistic overhead from network bridging and container isolation.

---

## 📈 Key Findings and Conclusion

### Overall Architectural Insight

*   **Parallelization Dominates:** The **MapReduce** parallel architecture demonstrated **superior efficiency** over the sequential **Bubble Sort pipeline**, regardless of the communication protocol used.
*   **Synchronous Blocking:** The Bubble Sort pipeline suffered from **"Synchronous Blocking,"** where upstream services were forced into an idle wait state until the entire downstream chain completed its sequential tasks, leading to significantly higher total transaction times.

### Protocol Performance (MapReduce Parallel Setup)

| Protocol | Performance Trend | Optimal Use Case (Based on Study) |
| :--- | :--- | :--- |
| **WebSocket** | **Fastest Overall.** Achieved the lowest RTT in both Localhost and Docker. Its persistent, bidirectional connection eliminates repeated handshake overhead. | Ideal for parallel workloads with frequent, lightweight communication. |
| **JSON-RPC** | **Strong and Stable.** Recorded the lowest transaction times overall in the parallel setup. Low overhead due to simple JSON encoding. | Excellent choice for MapReduce operations involving small payloads and rapid request-response cycles. |
| **gRPC** | **Fastest Processing Time.** Highly efficient server-side computation. However, its structured overhead from HTTP/2 streams resulted in higher RTT than lightweight protocols. | Better suited for large data transfers and high-throughput applications, less optimal for micro-level parallel tasks. |
| **XML-RPC** | **Moderate/Stable.** Higher RTT than JSON-RPC and WebSocket due to verbose XML parsing overhead, but remained predictable. | Stable, but less performant than modern, lightweight alternatives. |
| **RPI (Custom)** | Acceptable on Localhost but **Severe Degradation in Docker**. RTT and transaction times spiked significantly, likely due to a combination of Docker networking overhead and hardware constraints. | Not recommended for containerized environments without significant optimization. |

### Summary

While protocol selection impacts individual service latency, the study confirms that the **underlying system architecture (parallel vs. sequential)** plays the dominant role in total execution speed. For scalable distributed applications, **asynchronous parallel processing combined with lightweight protocols (like JSON-RPC or WebSocket)** yields the optimal balance of speed and efficiency.

---

## 👤 Contributors

| Name | Matric No | Assigned Protocol |
| :--- | :--- | :--- |
| WAN NURMAISARAH BINTI WAN MUSLIM | 164323 | WebSocket |
| JASMINE BINTI MOHD SHAIFUL ADLI CHUNG | 164191 | RPI |
| ALEEYA HAYFA BINTI OSMAN | 162974 | JSON-RPC |
| AIN NABIHAH BINTI MAHAMAD CHAH PARI | 162321 | XML-RPC |
| AINUL MARDHIAH BINTI ABDUL MUTALIP | 161836 | gRPC |

```
