import abc
from typing import TypeVar


class CommandBus(abc.ABC):
    @abc.abstractmethod
    def handle(self, command) -> None:
        pass

    @abc.abstractmethod
    def register(self, command_type: TypeVar, callback_type: TypeVar) -> None:
        pass
