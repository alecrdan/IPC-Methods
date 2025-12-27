import os
import socket
import struct
import tempfile
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 57795
DEFAULT_UNIX_SOCKET_PATH = os.path.join(tempfile.gettempdir(), "speedtest.sock")

RECEIVE_BUFFER_SIZE = 4096
FILE_CHUNK_SIZE = 4096


def _to_bytes(message):
    if message is None:
        return None
    if isinstance(message, bytes):
        return message
    return str(message).encode("utf-8")


def _socket_address(family, host, port, socket_path):
    if family == socket.AF_UNIX:
        return socket_path or DEFAULT_UNIX_SOCKET_PATH
    return (host, port)


def _create_socket(family):
    s = socket.socket(family, socket.SOCK_STREAM)
    if family == socket.AF_INET:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s


def cleanup_unix_socket(socket_path=None):
    path = socket_path or DEFAULT_UNIX_SOCKET_PATH
    if os.path.exists(path):
        os.unlink(path)


def send_bytes(conn, message):
    payload = _to_bytes(message)
    if payload is not None:
        conn.sendall(payload)


def send_file(conn, file_path, chunk_size=FILE_CHUNK_SIZE):
    file_size = os.path.getsize(file_path)
    conn.sendall(struct.pack("!Q", file_size))
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            conn.sendall(chunk)


def receive_file(conn, chunk_size=FILE_CHUNK_SIZE):
    header = conn.recv(8)
    if len(header) < 8:
        raise ValueError("Incomplete file size header")
    file_size = struct.unpack("!Q", header)[0]
    remaining = file_size
    while remaining > 0:
        data = conn.recv(min(chunk_size, remaining))
        if not data:
            break           
        remaining -= len(data)
    return file_size


def start_file_server(
    host=DEFAULT_HOST,
    port=DEFAULT_PORT,
    socket_path=None,
    family=socket.AF_INET,
    chunk_size=FILE_CHUNK_SIZE,
):
    address = _socket_address(family, host, port, socket_path)
    if family == socket.AF_UNIX:
        cleanup_unix_socket(socket_path=address)
    with _create_socket(family) as s:
        s.bind(address)
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                if family == socket.AF_UNIX:
                    print(f"Connected to {address}")
                else:
                    print(f"Connected by {addr}")
                file_size = receive_file(conn, chunk_size=chunk_size)
                print(f"Received file with {file_size} bytes")


def send_file_to_server(
    file_path,
    host=DEFAULT_HOST,
    port=DEFAULT_PORT,
    socket_path=None,
    family=socket.AF_INET,
    chunk_size=FILE_CHUNK_SIZE,
):
    address = _socket_address(family, host, port, socket_path)
    with _create_socket(family) as s:
        _connect_with_retry(s, address)
        send_file(s, file_path, chunk_size=chunk_size)


def _connect_with_retry(sock, address, attempts=50, delay_s=0.1):
    last_error = None
    for _ in range(attempts):
        try:
            sock.connect(address)
            return
        except OSError as e:
            last_error = e
            time.sleep(delay_s)
    raise last_error


def start_server(
    host=DEFAULT_HOST,
    port=DEFAULT_PORT,
    socket_path=None,
    family=socket.AF_INET,
    on_receive=None,
):
    if on_receive is None:
        def on_receive(_conn, _message):
            return

    address = _socket_address(family, host, port, socket_path)
    if family == socket.AF_UNIX:
        cleanup_unix_socket(socket_path=address)

    with _create_socket(family) as s:
        s.bind(address)
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                if family == socket.AF_UNIX:
                    print(f"Connected to {address}")
                else:
                    print(f"Connected by {addr}")
                while True:
                    data = conn.recv(RECEIVE_BUFFER_SIZE)
                    if not data:
                        break
                    message = data.decode("utf-8", errors="replace")
                    on_receive(conn, message)


def send_message(
    message,
    host=DEFAULT_HOST,
    port=DEFAULT_PORT,
    socket_path=None,
    family=socket.AF_INET,
    on_receive=None,
):
    if on_receive is None:
        def on_receive(_reply):
            return

    address = _socket_address(family, host, port, socket_path)
    with _create_socket(family) as s:
        _connect_with_retry(s, address)
        s.sendall(_to_bytes(message))
        data = s.recv(RECEIVE_BUFFER_SIZE)
        reply = data.decode("utf-8", errors="replace")
        on_receive(reply)
