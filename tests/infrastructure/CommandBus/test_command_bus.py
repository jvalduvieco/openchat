from dataclasses import dataclass
from unittest import TestCase

from parameterized import parameterized

from domain.misc.CommandBus import CommandBus
from infrastructure.CommandBus.exceptions import AlreadyRegisteredCommand, NoHandlerForCommand
from infrastructure.CommandBus.local_synchronous_command_bus import LocalSynchronousCommandBus


@dataclass(frozen=True)
class ADummyCommand:
    username: str


class HandlerCalled(ValueError):
    pass


def dummy_handler(_):
    raise HandlerCalled()


def a_handler_that_fails(_):
    raise ValueError


class TestLocalSynchronousCommandBus(TestCase):
    @parameterized.expand([
        [LocalSynchronousCommandBus()]
    ])
    def test_should_register_a_handler_for_a_command(self, command_bus: CommandBus):
        command_bus.register(ADummyCommand, lambda command: True)

    @parameterized.expand([
        [LocalSynchronousCommandBus()]
    ])
    def test_should_not_let_register_two_handlers_for_a_command(self, command_bus: CommandBus):
        command_bus.register(ADummyCommand, lambda command: True)

        with self.assertRaises(AlreadyRegisteredCommand):
            command_bus.register(ADummyCommand, lambda command: False)

    @parameterized.expand([
        [LocalSynchronousCommandBus()]
    ])
    def test_should_handle_a_registered_command(self, command_bus: CommandBus):
        command_bus.register(ADummyCommand, dummy_handler)

        with self.assertRaises(HandlerCalled):
            command_bus.handle(ADummyCommand(username='Test'))

    @parameterized.expand([
        [LocalSynchronousCommandBus()]
    ])
    def test_should_bubble_up_exceptions(self, command_bus: CommandBus):
        command_bus.register(ADummyCommand, a_handler_that_fails)

        with self.assertRaises(ValueError):
            command_bus.handle(ADummyCommand(username='Test'))

    @parameterized.expand([
        [LocalSynchronousCommandBus()]
    ])
    def test_should_raise_an_exception_for_an_unregistered_command(self, command_bus: CommandBus):
        with self.assertRaises(NoHandlerForCommand):
            command_bus.handle(ADummyCommand(username='Test'))
