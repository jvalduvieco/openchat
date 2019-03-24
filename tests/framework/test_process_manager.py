import abc
import dataclasses
from abc import abstractmethod
from dataclasses import dataclass
from typing import List, TypeVar, Tuple
from unittest import TestCase

from injector import Injector, SingletonScope

from domain.misc import EventBus, CommandBus
from domain.users.register_user_command import RegisterUser
from domain.users.user_registrator import UserRegistrator
from domain.users.users_repository import UsersRepository
from infrastructure.CommandBus.local_command_handler import build_local_command_handler
from infrastructure.CommandBus.local_synchronous_command_bus import LocalSynchronousCommandBus
from infrastructure.EventBus.local_synchronous_event_bus import LocalSynchronousEventBus


class Event(object):
    pass


@dataclass(frozen=True)
class AnEventThatCreatesAProcessManagerHappened(Event):
    some_very_important_id: str
    some_data: str


@dataclass(frozen=True)
class AnEventThatIsVeryImportantHappened(Event):
    some_very_important_id: str
    some_data: str


@dataclass(frozen=True)
class AnEventFromAnotherService(Event):
    id: str
    some_data: str


def build_process_manager_event_handler(injector: Injector, event_types: List[TypeVar], service_type: TypeVar,
                                        repository_type: TypeVar):
    def event_handler(event):
        service = injector.get(service_type)
        repository = injector.get(repository_type)
        event_bus: EventBus = injector.get(EventBus)
        command_bus: CommandBus = injector.get(CommandBus)
        state = repository.by_id(service.get_id(event))
        state, commands, events = service.handle(event, state)
        repository.save(state)
        [event_bus.handle(generated_event) for generated_event in events]
        [command_bus.handle(command) for command in commands]

    return {'event_type': event_types, 'callback': event_handler}


@dataclass(frozen=True)
class ProcessManagerSUTState(object):
    id: str
    received_events: List[str]
    a_counter: int


class ProcessManagerSUTStateRepository(abc.ABC):
    @abstractmethod
    def save(self, state):
        pass

    @abstractmethod
    def by_id(self, process_manager_sut_id):
        pass


class ProcessManagerSUTStateRepositoryInMemory(ProcessManagerSUTStateRepository):
    def __init__(self):
        self.process_manager_sut_states = {}

    def save(self, state: ProcessManagerSUTState) -> None:
        self.process_manager_sut_states[state.id] = state

    def by_id(self, process_manager_sut_id: str) -> ProcessManagerSUTState:
        return self.process_manager_sut_states.get(process_manager_sut_id, {})


class Command(object):
    pass


@dataclass(frozen=True)
class ANiceCommand(Command):
    id: str
    some_parameter: str


class ProcessManager(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_id(event):
        pass

    @abc.abstractmethod
    def handle(self, event, state):
        pass


class ProcessManagerSUT(ProcessManager):
    def __init__(self):
        self.called = False

    @staticmethod
    def get_id(event) -> str:
        return 'PMSUT' + event.some_very_important_id

    def handle(self, event, state: ProcessManagerSUTState) \
            -> Tuple[ProcessManagerSUTState, List[Command], List[Event]]:
        if type(event) == AnEventThatCreatesAProcessManagerHappened:
            return ProcessManagerSUTState(id=self.get_id(event), received_events=[event.__class__.__name__],
                                          a_counter=1), [], []
        if type(event) == AnEventThatIsVeryImportantHappened:
            return dataclasses.replace(state, received_events=state.received_events + [event.__class__.__name__],
                                       a_counter=state.a_counter + 1), \
                   [], []


class TestProcessManager(TestCase):
    def setUp(self):
        self.injector = Injector()
        self.injector.binder.bind(CommandBus, to=lambda: LocalSynchronousCommandBus(), scope=SingletonScope)
        self.injector.binder.bind(EventBus, to=lambda: LocalSynchronousEventBus(), scope=SingletonScope)
        self.injector.binder.bind(ProcessManagerSUT, scope=SingletonScope)
        self.injector.binder.bind(ProcessManagerSUTStateRepository, ProcessManagerSUTStateRepositoryInMemory(),
                                  scope=SingletonScope)
        self.state_repository = self.injector.get(ProcessManagerSUTStateRepository)
        self.event_bus = self.injector.get(EventBus)
        self.command_bus = self.injector.get(CommandBus)
        self.event_bus.subscribe(**build_process_manager_event_handler(self.injector,
                                                                       [AnEventThatCreatesAProcessManagerHappened,
                                                                        AnEventThatIsVeryImportantHappened],
                                                                       ProcessManagerSUT,
                                                                       ProcessManagerSUTStateRepository))
        self.command_bus.register(**build_local_command_handler(self.injector,
                                                                RegisterUser,
                                                                UserRegistrator,
                                                                UsersRepository,
                                                                self.event_bus))

    def test_process_managers_are_created_by_an_event(self):
        an_event = AnEventThatCreatesAProcessManagerHappened(some_data='username', some_very_important_id='3354')
        self.event_bus.publish([an_event])
        sut_state = self.state_repository.by_id(ProcessManagerSUT.get_id(an_event))
        self.assertIn('AnEventThatCreatesAProcessManagerHappened', sut_state.received_events)
        self.assertEqual(1, sut_state.a_counter)

    def test_process_managers_have_internal_state_that_is_preserved_across_events(self):
        an_event = AnEventThatCreatesAProcessManagerHappened(some_data='username', some_very_important_id='3354')
        another_event = AnEventThatIsVeryImportantHappened(some_data='username', some_very_important_id='3354')
        self.event_bus.publish([an_event, another_event])
        sut_state = self.state_repository.by_id(ProcessManagerSUT.get_id(an_event))
        self.assertIn('AnEventThatCreatesAProcessManagerHappened', sut_state.received_events)
        self.assertIn('AnEventThatIsVeryImportantHappened', sut_state.received_events)
        self.assertEqual(2, sut_state.a_counter)
