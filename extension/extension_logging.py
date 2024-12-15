import os
import json
import sys
from enum import Enum

EXTENSION_NAME = os.path.basename(sys.argv[0])  # extension name has to match the filename
PRINT_PREFIX = f"[{EXTENSION_NAME}] "

class LogLevel(Enum):
    Debug = 1
    Error = 2
    Warning = 3
    Info = 4

# Function for pretty printing objects in logs
def pretty_print(v):
    try:
        return json.dumps(v, indent=4)
    except:
        return ""
    

def print_log(message,loglevel:LogLevel):
    if loglevel == LogLevel.Debug:
        print(f"[Debug] {PRINT_PREFIX}: {message}")
    elif loglevel == LogLevel.Error:
        print(f"[Error] {PRINT_PREFIX}: {message}")
    elif loglevel == LogLevel.Warning:
        print(f"[Error] {PRINT_PREFIX}: {message}")
    elif loglevel == LogLevel.Info:
        print(f"[Info] {PRINT_PREFIX}: {message}")