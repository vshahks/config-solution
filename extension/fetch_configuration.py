
import requests
import os
import utils
import time
from extension_logging import print_log,LogLevel

CONFIG_BASE_URL = "CONFIG_BASE_URL"

configuration_cache = {}

def fetch(scope,app_name,section,key):
    app_config_in_cache = configuration_cache.get(app_name)
    # If expired or not available in cache then read it from SSM, else return from cache
    if not app_config_in_cache or not app_config_in_cache.data or utils.is_expired(app_config_in_cache.cache_expiry):
        app_config = fetch_config_by_app_name(app_name)
        configuration_cache[app_name]= utils.CacheData(data=app_config, cache_expiry=utils.get_cache_expiry())
        print_log("fetching from server",LogLevel.Info)
        return get_value(app_config,scope,section,key)
    else:
        print_log("serving from cache",LogLevel.Info)
        return get_value(app_config_in_cache.data,scope,section,key)
    
    

def fetch_config_by_app_name(app_name):
    config_base_url = os.getenv(CONFIG_BASE_URL, "http://127.0.0.1:5000")
    config_base_url = config_base_url.lstrip('/')
    try:
        response = requests.get(f'{config_base_url}/configuration/api/config/application/{app_name}')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as err:
        print_log(f'HTTP error occurred: {err}',LogLevel.Error)
    except Exception as err:
        print_log(f'Other error occurred: {err}',LogLevel.Error)


def get_value(data, scope, section, key):
    for sc in data["scopes"]:
        if sc["name"] == scope: 
            for sec in sc["section"]: 
                if sec["name"] == section: 
                    for k in sec["keys"]: 
                        if k["name"] == key: 
                            return k
    return None

if __name__ == '__main__':
    i = 0
    while(i < 120):
        fetch('global',"abc","test_section_2","key2")
        time.sleep(1)
        i+=1