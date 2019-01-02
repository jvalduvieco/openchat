from typing import TypeVar

from injector import Injector

from domain.misc import EventBus


def build_local_command_handler(injector: Injector, command_type: TypeVar, service_type: TypeVar,
                                repository_type: TypeVar, event_bus: EventBus):
    def command_handler(command: command_type):
        service = injector.get(service_type)
        repository = injector.get(repository_type)
        entity, events = service.execute(command)
        if entity is not None:
            repository.save(entity)
        event_bus.publish(events)

    return command_handler
