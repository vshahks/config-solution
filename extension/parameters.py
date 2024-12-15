# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import utils

# Struct for storing parameter cache configurations
class ParameterConfiguration:
    def __init__(self, region, names):
        self.region = region
        self.names = names

# Struct for caching the information
class Parameter:
    def __init__(self, cache_data, region):
        self.cache_data = cache_data
        self.region = region

parameter_cache = {}
region_cache = {}

# Initialize map and cache objects (if requested)
def init_parameters(parameters, initialize_cache):
    for config in parameters:
        for parameter in config.names:
            if parameter not in parameter_cache:
                if initialize_cache:
                    # Read from SSM and add it to the cache
                    get_parameter(parameter, config.region, get_ssm_client(config.region))
                else:
                    parameter_cache[parameter] = Parameter(utils.CacheData(), config.region)
            else:
                print(f"{utils.PrintPrefix} {parameter} already exists so skipping it")

# Initialize parameter cache
def get_parameter(name, region, ssmsvc):
    try:
        param = ssmsvc.get_parameter(Name=name, WithDecryption=True)
        value = param['Parameter']['Value']
        parameter_cache[name] = Parameter(
            utils.CacheData(data=value, cache_expiry=utils.get_cache_expiry()),
            region
        )
        return value
    except Exception as err:
        print(f"{utils.PrintPrefix} Error while fetching parameter {name}: {err}")
        return ""

# Get SSM Client and cache it based on region
def get_ssm_client(region):
    if region not in region_cache:
        session = boto3.Session(region_name=region)
        ssm_client = session.client('ssm')
        region_cache[region] = ssm_client
    return region_cache[region]

# Fetch Parameter cache
def get_parameter_cache(name):
    parameter = parameter_cache.get(name)
    
    # If expired or not available in cache then read it from SSM, else return from cache
    if not parameter or not parameter.cache_data.data or utils.is_expired(parameter.cache_data.cache_expiry):
        return get_parameter(name, parameter.region, get_ssm_client(parameter.region))
    else:
        return parameter.cache_data.data


