import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.ipc_lib import start_file_server


try:
    start_file_server()
except KeyboardInterrupt:
    print("\nServer stopping...")
