from typing import TypeVar

from injector import Injector


def build_projection_event_handler(injector: Injector, event_type: TypeVar, service_type: TypeVar):
    def event_handler(event: event_type):
        service = injector.get(service_type)
        service.handle(event)

    return {'event_type': event_type, 'callback': event_handler}
