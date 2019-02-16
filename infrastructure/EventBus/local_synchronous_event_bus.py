import logging
from collections.abc import Iterable
from typing import List, TypeVar, Callable

import typing

from domain.misc.EventBus import EventBus

logger = logging.getLogger()


class LocalSynchronousEventBus(EventBus):
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: TypeVar, callback: Callable) -> None:
        if isinstance(event_type, typing.List):
            for type in event_type:
                self.subscribe_one(type, callback)
        else:
            self.subscribe_one(event_type, callback)

    def subscribe_one(self, event_type, callback):
        if event_type in self.subscribers:
            self.subscribers[event_type].append(callback)
        else:
            self.subscribers[event_type] = [callback]

    def publish(self, events: List):
        if not isinstance(events, Iterable):
            events = [events]
        for event in events:
            event_type = type(event)
            if event_type in self.subscribers:
                for subscriber_callback in self.subscribers[event_type]:
                    try:
                        subscriber_callback.__call__(event)
                    except:  # noqa: E722
                        logging.exception("exception handling %s." % event_type)
                        continue
