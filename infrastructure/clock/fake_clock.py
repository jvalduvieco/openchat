from datetime import datetime

from misc.clock import Clock


class FakeClock(Clock):
    def __init__(self, fake_now: datetime):
        self.fake_now = fake_now

    def now(self) -> datetime:
        return self.fake_now
