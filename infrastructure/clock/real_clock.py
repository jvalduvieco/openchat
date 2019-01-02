from datetime import datetime

from domain.misc.clock import Clock


class RealClock(Clock):
    def now(self) -> datetime:
        return datetime.now()
