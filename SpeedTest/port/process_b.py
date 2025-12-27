import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.ipc_lib import send_file_to_server


try:
    send_file_to_server("10gb_file.txt")
except KeyboardInterrupt:
    print("\nClient stopping...")
