# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import yaml
import os
import logging
from typing import List
import parameters
import utils
import fetch_configuration

# Constants definition
PARAMETERS = "parameters"
FETCH_CONFIGURATION = "fetch_configuration"
# FILE_NAME = "/var/task/config.yaml"
FILE_NAME = "./config.yaml"
INITIALIZE_CACHE_ON_STARTUP = "CACHE_EXTENSION_INIT_STARTUP"

# Struct for storing CacheConfiguration
class CacheConfig:
    def __init__(self):
        self.parameters: List[parameters.ParameterConfiguration] = []

cache_config = CacheConfig()

# Initialize cache and start the background process to refresh cache
def init_cache_extensions():
    # Read the cache config file
    data = load_config_file()

    # Unmarshal the configuration to struct
    try:
        config_dict = yaml.safe_load(data)
        cache_config.parameters = config_dict.get('parameters', [])
    except yaml.YAMLError as e:
        logging.fatal(f"{utils.PrintPrefix} error: {e}")

    # Initialize Cache
    init_cache()
    print(f"{utils.PrintPrefix} Cache successfully loaded")

# Initialize individual cache
def init_cache():
    # Read Lambda env variable
    init_cache = os.getenv(INITIALIZE_CACHE_ON_STARTUP)
    init_cache_in_bool = False
    if init_cache:
        try:
            init_cache_in_bool = bool(init_cache.lower() == 'true')
        except ValueError:
            raise ValueError(f"{utils.PrintPrefix} Error while converting CACHE_EXTENSION_INIT_STARTUP env variable {init_cache}")

    # Initialize map and load data from individual services if "CACHE_EXTENSION_INIT_STARTUP" = true
    parameters.init_parameters(cache_config.parameters, init_cache_in_bool)

# Route request to corresponding cache handlers
def route_cache(cache_type: str, name: str) -> str:
    if cache_type == PARAMETERS:
        return parameters.get_parameter_cache(name)
    elif cache_type == FETCH_CONFIGURATION:
        return fetch_configuration.fetch()
    else:
        return ""

# Load the config file
def load_config_file() -> str:
    try:
        with open(FILE_NAME, 'r') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading config file: {e}")

