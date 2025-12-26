import os
import socket
import sys
import tempfile
import time

# Match the server's socket path
SOCKET_NAME = 'speedtest.sock'
SERVER_ADDRESS = os.path.join(tempfile.gettempdir(), SOCKET_NAME)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    sock.connect(SERVER_ADDRESS)
    print(f"Connected to {SERVER_ADDRESS}")

    while True:
        # Prepare and send heartbeat or data message
        message = b"Heartbeat or Data"
        print(f"Sending: {message.decode()}")
        sock.sendall(message)

        # Note: In a real app, you'd use a fixed header or delimiter 
        # to know exactly how much to read.
        # data = sock.recv(4096)

        # # Small delay so we don't spam the CPU/Server too fast
        time.sleep(2)

except socket.error as e:
    print(f"Socket error: {e}")
except KeyboardInterrupt:
    print("\nClient stopping...")
finally:
    print("Closing socket")
    sock.close()