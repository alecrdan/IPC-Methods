# IPC Methods

This repository currently contains a focused IPC benchmark that compares file transfer speed over a TCP port versus a Unix domain socket.

## Contents

- `SpeedTest/`: Python sender/receiver pairs that transfer a 10 GiB file over TCP (`port/`) and UDS (`unix_socket/`), plus a helper script to generate the test file.

## Quick Start

From the repo root:

```bash
cd SpeedTest
./run.sh
```

Notes:
- `SpeedTest/run.sh` generates `SpeedTest/10gb_file.txt` if it does not exist, then runs both benchmarks.
- The 10 GiB file is large; adjust `DEFAULT_SIZE_BYTES` in `SpeedTest/utils/generate_10gb_txt.py` if needed.
