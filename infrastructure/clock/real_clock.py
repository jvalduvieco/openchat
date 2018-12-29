from datetime import datetime

from domain.misc import Clock


class RealClock(Clock):
    def now(self) -> datetime:
        return datetime.now()
