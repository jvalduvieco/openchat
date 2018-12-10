import datetime


def a_perfect_day_and_time(minutes_later: int = 0) -> datetime:
    return datetime.datetime(2020, 5, 17, 15, 15 + minutes_later, 0)


def a_perfect_day_and_time_ten_minutes_after() -> datetime:
    return a_perfect_day_and_time(10)
