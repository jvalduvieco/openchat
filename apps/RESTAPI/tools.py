import functools
import json
from typing import List, Callable

from flask import Response
from injector import Injector

from domain.misc import CommandBus, EventBus


def register_command_handlers(injector: Injector, command_bus: CommandBus, event_bus: EventBus,
                              modules: List[Callable]):
    for module in modules:
        module(injector, command_bus, event_bus)


def register_event_handlers(injector: Injector, event_bus: EventBus,
                            modules: List[Callable]):
    for module in modules:
        module(injector, event_bus)


def find_missing_keys(keys, expected_keys):
    return [key for key in expected_keys if key not in keys]


def validate_client_request(client_request: dict, expected_keys: List[str]):
    if type(client_request) is not dict:
        raise ValueError("Invalid request")
    missing_keys = find_missing_keys(client_request, expected_keys)
    if len(missing_keys) > 0:
        raise ValueError("Invalid request: Missing keys (%s)" % missing_keys)


def return_json(view):
    @functools.wraps(view)
    def wrapped_view(**values):
        response, status = view(**values)
        response = Response(
            response=json.dumps(response),
            status=status,
            mimetype='application/json'
        )
        return response

    return wrapped_view
