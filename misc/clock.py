import abc
from datetime import datetime


class Clock(abc.ABC):
    @abc.abstractmethod
    def now(self) -> datetime:
        pass
