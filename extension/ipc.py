# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from flask import Flask,Response,jsonify
import fetch_configuration
from extension_logging import LogLevel,print_log

app = Flask(__name__)

def start_http_server(port):
    @app.route('/configuration/api/config/<scope>/<app_name>/section/<section_name>/keys/<key>')
    def handle_request(scope,app_name,section_name,key):
        value = fetch_configuration.fetch(scope,app_name,section_name,key)

        if value:
            return jsonify(value)
        else:
            response = jsonify({"msg":f"Could not find the configuration for {scope} {app_name} {section_name} {key}"})
            response.status_code = 400
            return response

    print_log(f"Starting HTTP server on port {port}",LogLevel.Info)
    app.run(host='0.0.0.0', port=int(port))

if __name__ == '__main__':
    start_http_server('4566')  # Example usage

