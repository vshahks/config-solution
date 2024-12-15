# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import requests
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

@dataclass
class RegisterResponse:
    functionName: str
    functionVersion: str
    handler: str

@dataclass
class Tracing:
    type: str
    value: str

class EventType(Enum):
    INVOKE = "INVOKE"
    SHUTDOWN = "SHUTDOWN"

@dataclass
class NextEventResponse:
    eventType: EventType
    deadlineMs: int
    requestId: str
    invokedFunctionArn: str
    tracing: Tracing

EXTENSION_NAME_HEADER = "Lambda-Extension-Name"
EXTENSION_IDENTIFIER_HEADER = "Lambda-Extension-Identifier"

class Client:
    def __init__(self, aws_lambda_runtime_api: str):
        self.base_url = f"http://{aws_lambda_runtime_api}/2020-01-01/extension"
        self.http_client = requests.Session()
        self.extension_id: Optional[str] = None

    def register(self, filename: str) -> RegisterResponse:
        url = f"{self.base_url}/register"
        req_body = {
            "events": [EventType.INVOKE.value, EventType.SHUTDOWN.value]
        }
        headers = {EXTENSION_NAME_HEADER: filename}
        response = self.http_client.post(url, json=req_body, headers=headers)
        response.raise_for_status()
        
        self.extension_id = response.headers.get(EXTENSION_IDENTIFIER_HEADER)
        return RegisterResponse(**response.json())

    def next_event(self) -> NextEventResponse:
        url = f"{self.base_url}/event/next"
        headers = {EXTENSION_IDENTIFIER_HEADER: self.extension_id}
        response = self.http_client.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        data['eventType'] = EventType(data['eventType'])
        data['tracing'] = Tracing(**data['tracing'])
        return NextEventResponse(**data)

def new_client(aws_lambda_runtime_api: str) -> Client:
    return Client(aws_lambda_runtime_api)

