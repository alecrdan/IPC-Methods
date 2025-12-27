import os
import socket
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.ipc_lib import DEFAULT_UNIX_SOCKET_PATH, cleanup_unix_socket, start_file_server


if __name__ == "__main__":
    try:
        print(f"Unix server listening on {DEFAULT_UNIX_SOCKET_PATH}")
        start_file_server(
            socket_path=DEFAULT_UNIX_SOCKET_PATH,
            family=socket.AF_UNIX,
        )
    except KeyboardInterrupt:
        print("\nServer stopping...")
    finally:
        cleanup_unix_socket(socket_path=DEFAULT_UNIX_SOCKET_PATH)
