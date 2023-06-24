import json
import sys
from colorama import init, Cursor

# Initialize colorama
init()

# Your other code...
for i in range(100):
    sys.stdout.write(f"number: {i}\r")
    sys.stdout.flush()

# Comment out or remove the clear_line() function call
# clear_line()
