import abc
from typing import List, TypeVar, Callable


class EventBus(abc.ABC):
    @abc.abstractmethod
    def publish(self, events: List):
        pass

    @abc.abstractmethod
    def subscribe(self, event_type: TypeVar, callback: Callable) -> None:
        pass
