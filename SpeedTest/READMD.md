This project compares the performance of transferring a large file between two processes using either a network port (TCP) or a Unix Domain Socket (UDS).

- Two processes are involved: one sends a large file over a TCP port, and the other sends the same file over a Unix Domain Socket.
- Unix Domain Sockets typically offer lower latency and higher throughput than TCP sockets when both processes run on the same machine.

## How to Run

1. Clone this repository:
    ```sh
    git clone <repo-url>
    cd SpeedTest
    ```
2. Build or install dependencies as required (see `requirements.txt` or project documentation).
3. Start the receiver process:
    ```sh
    python receiver.py --protocol tcp   # For TCP
    python receiver.py --protocol uds   # For Unix Domain Socket
    ```
4. In a separate terminal, start the sender process:
    ```sh
    python sender.py --protocol tcp --file <large-file>
    python sender.py --protocol uds --file <large-file>
    ```
5. Compare the output to evaluate performance differences.

## Real-World Relevance

Databases like PostgreSQL and Redis use Unix Domain Sockets by default for local connections, as this provides a significant performance advantage over TCP.