from datetime import datetime

from misc.clock import Clock


class RealClock(Clock):
    def now(self) -> datetime:
        return datetime.now()
