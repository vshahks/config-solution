import json
import os
import sys
from datetime import datetime, timedelta

# Lambda environment variable for defining TTL
CACHE_TIMEOUT = "CACHE_EXTENSION_TTL"

# Class for storing cache data with expiry timestamp [datetime.now() + CACHE_EXTENSION_TTL]
class CacheData:
    def __init__(self, data, cache_expiry):
        self.data = data
        self.cache_expiry = cache_expiry

# Check whether cache has expired
def is_expired(cache_expiry):
    return cache_expiry < datetime.now()

# Return cache expiry timestamp based on "datetime.now() + CACHE_EXTENSION_TTL"
def get_cache_expiry():
    # Refresh cache is required via environment variable
    time_out = os.getenv(CACHE_TIMEOUT, "1m")
    print(time_out)

    try:
        if time_out.endswith('m'):
            timeout_in_minutes = int(time_out[:-1])
        else:
            raise ValueError("Invalid time format")
    except ValueError:
        raise ValueError(f"Error while converting CACHE_EXTENSION_TTL env variable {time_out}")

    return datetime.now() + timedelta(minutes=timeout_in_minutes)

# Function for pretty printing objects in logs
def pretty_print(v):
    try:
        return json.dumps(v, indent=4)
    except:
        return ""

