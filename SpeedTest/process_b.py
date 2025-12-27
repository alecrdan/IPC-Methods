import os
import socket
import sys
import tempfile
import time

# Match the server's socket path
SOCKET_NAME = 'speedtest.sock'
SERVER_ADDRESS = os.path.join(tempfile.gettempdir(), SOCKET_NAME)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Send message
def send_message(sock):
    message = b"Heartbeat or Data"
    print(f"(B) Transmitted")
    sock.sendall(message)

try:
    sock.connect(SERVER_ADDRESS)
    print(f"Connected to {SERVER_ADDRESS}")

    while True:
        # Prepare and send heartbeat or data message

        # Note: In a real app, you'd use a fixed header or delimiter
        # to know exactly how much to read.
        data = sock.recv(4096)
        
        if data:
            # Send a heartbeat or data message
            print(f"(B) ReceSived {len(data)} bytes")
            send_message(sock)
            
        # Slow down messages
        time.sleep(2) 

except socket.error as e:
    print(f"Socket error: {e}")
except KeyboardInterrupt:
    print("\nClient stopping...")
finally:
    print("Closing socket")
    sock.close()