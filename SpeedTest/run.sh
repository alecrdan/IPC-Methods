#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

create_test_data_file() {
  if [ ! -f "$SCRIPT_DIR/10gb_file.txt" ]; then
      python3 "$SCRIPT_DIR/utils/generate_10gb_txt.py"
  fi
}

run_port() {
  pkill -f "port/process_a.py" 2>/dev/null || true
  pkill -f "port/process_b.py" 2>/dev/null || true

  python3 "$SCRIPT_DIR/port/process_a.py" &
  SERVER_PID=$!

  sleep 0.1
  echo "Port transfer timing:"
  /usr/bin/time -p python3 "$SCRIPT_DIR/port/process_b.py"

  kill "$SERVER_PID" 2>/dev/null || true
  unset SERVER_PID
}

run_unix() {
  pkill -f "unix_socket/process_a.py" 2>/dev/null || true
  pkill -f "unix_socket/process_b.py" 2>/dev/null || true

  python3 "$SCRIPT_DIR/unix_socket/process_a.py" &
  SERVER_PID=$!

  sleep 0.1
  echo "Unix socket transfer timing:"
  /usr/bin/time -p env RUN_ONCE=1 python3 "$SCRIPT_DIR/unix_socket/process_b.py"

  kill "$SERVER_PID" 2>/dev/null || true
  unset SERVER_PID
}

create_test_data_file
run_port
run_unix
