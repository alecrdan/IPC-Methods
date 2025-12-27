import os
import socket
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.ipc_lib import DEFAULT_UNIX_SOCKET_PATH, send_file_to_server


FILE_PATH = "10gb_file.txt"


try:
    run_once = os.getenv("RUN_ONCE") == "1"
    while True:
        send_file_to_server(
            FILE_PATH,
            socket_path=DEFAULT_UNIX_SOCKET_PATH,
            family=socket.AF_UNIX,
        )
        if run_once:
            break
        time.sleep(2)
except socket.error as e:
    print(f"Socket error: {e}")
except KeyboardInterrupt:
    print("\nClient stopping...")
