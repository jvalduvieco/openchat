from typing import TypeVar, Callable

from domain.misc.CommandBus import CommandBus
from infrastructure.CommandBus.exceptions import AlreadyRegisteredCommand, NoHandlerForCommand


class LocalSynchronousCommandBus(CommandBus):
    def __init__(self):
        self.handlers = {}

    def register(self, command_type: TypeVar, callback: Callable) -> None:
        if command_type not in self.handlers:
            self.handlers[command_type] = callback
        else:
            raise AlreadyRegisteredCommand('A command handler for %s is already registered' % command_type)

    def handle(self, command) -> None:
        command_type = type(command)
        if command_type in self.handlers:
            self.handlers[command_type].__call__(command)
        else:
            raise NoHandlerForCommand('Could not find a handler for command %s' % command_type)
