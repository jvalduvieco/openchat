from typing import List, Callable

from injector import Injector

from domain.misc import CommandBus, EventBus


def register_command_handlers(injector: Injector, command_bus: CommandBus, event_bus: EventBus,
                              modules: List[Callable]):
    for module in modules:
        module(injector, command_bus, event_bus)
