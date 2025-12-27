import sys

DEFAULT_SIZE_BYTES = 1_073_741_824 * 10 # 10 GiB
CHUNK_SIZE = 4 * 1024 * 1024  # 4 MiB


def write_file(filename="10gb_file.txt"):
    chunk = b"a" * CHUNK_SIZE
    remaining = DEFAULT_SIZE_BYTES
    with open(filename, "wb") as f:
        while remaining > 0:
            to_write = chunk if remaining >= CHUNK_SIZE else b"a" * remaining
            f.write(to_write)
            remaining -= len(to_write)


write_file()
print(f"Wrote {DEFAULT_SIZE_BYTES} bytes to 10gb_file.txt")
