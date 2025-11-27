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
    4.  
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
