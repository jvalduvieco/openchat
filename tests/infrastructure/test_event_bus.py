from dataclasses import dataclass
from unittest import TestCase

from parameterized import parameterized

from domain.misc import EventBus
from infrastructure.local_synchronous_event_bus import LocalSynchronousEventBus


@dataclass(frozen=True)
class ADummyEventHappened:
    username: str


class TestLocalSynchronousEventBus(TestCase):

    @parameterized.expand([
        [LocalSynchronousEventBus()]
    ])
    def test_should_allow_subscribing_to_events(self, event_bus: EventBus):
        handlers_called = []
        event_bus.subscribe(ADummyEventHappened, lambda event: handlers_called.append(1))

        event_bus.publish(ADummyEventHappened('username'))
        assert 1 == len(handlers_called)

    @parameterized.expand([
        [LocalSynchronousEventBus()]
    ])
    def test_should_allow_multiple_subscribers_to_events(self, event_bus: EventBus):
        handlers_called = []
        event_bus.subscribe(ADummyEventHappened, lambda event: handlers_called.append(1))
        event_bus.subscribe(ADummyEventHappened, lambda event: handlers_called.append(2))

        event_bus.publish(ADummyEventHappened('username'))

        assert 2 == len(handlers_called)

    @parameterized.expand([
        [LocalSynchronousEventBus()]
    ])
    def test_should_publish_an_event_with_no_subscribers_and_nothing_happens(self, event_bus: EventBus):
        event_bus.publish(ADummyEventHappened('username'))

    @parameterized.expand([
        [LocalSynchronousEventBus()]
    ])
    def test_should_call_all_subscribers_even_if_one_fails(self, event_bus: EventBus):
        handlers_called = []
        event_bus.subscribe(ADummyEventHappened, lambda event: handlers_called.append(1))
        event_bus.subscribe(ADummyEventHappened, lambda event: 1/0)
        event_bus.subscribe(ADummyEventHappened, lambda event: handlers_called.append(2))

        event_bus.publish(ADummyEventHappened('username'))

        assert 2 == len(handlers_called)

    @parameterized.expand([
        [LocalSynchronousEventBus()]
    ])
    def test_should_publish_an_event_array(self, event_bus: EventBus):
        handlers_called = []
        event_bus.subscribe(ADummyEventHappened, lambda event: handlers_called.append(1))

        event_bus.publish([ADummyEventHappened('username'), ADummyEventHappened('username')])

        assert 2 == len(handlers_called)
