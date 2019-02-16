from dataclasses import dataclass
from unittest import TestCase

from typing import List, TypeVar, Tuple

from injector import Injector, inject, SingletonScope

from EventBus.local_synchronous_event_bus import LocalSynchronousEventBus


@dataclass(frozen=True)
class AnEventThatCreatesAProcessManagerHappened:
    someData: str


def build_process_manager_event_handler(injector: Injector, event_types: List[TypeVar], service_type: TypeVar):
    def event_handler(event):
        service = injector.get(service_type)
        service.handle(event)

    return {'event_type': event_types, 'callback': event_handler}


class Events(object):
    pass


class PMState(object):
    pass


class Command(object):
    pass


class ProcessManagerSUT(object):
    def __init__(self):
        self.called = False

    def handle(self, event) -> Tuple[List[Events], PMState, List[Command]]:
        self.called = True
        return [], PMState(), []

    def handle_has_been_called(self):
        return self.called


class TestProcessManager(TestCase):
    def test_process_managers_are_created_by_an_event(self):
        injector = Injector()
        injector.binder.bind(ProcessManagerSUT, scope=SingletonScope)
        event_bus = LocalSynchronousEventBus()
        sut = injector.get(ProcessManagerSUT)
        event_bus.subscribe(**build_process_manager_event_handler(injector, [AnEventThatCreatesAProcessManagerHappened],
                                                                  ProcessManagerSUT))
        event_bus.publish([AnEventThatCreatesAProcessManagerHappened(someData='username')])
        assert sut.handle_has_been_called() is True
