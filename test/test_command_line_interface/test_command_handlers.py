import unittest
from unittest.mock import MagicMock
from typing import List

from comlint.command_handler_interface import CommandHandlerInterface
from comlint.command_line_interface import CommandLineInterface
from comlint.types import CommandValues, OptionsMap, FlagsMap, ANY


class TestCommandLineInterfaceCommandHandlers(unittest.TestCase):
    def test_proper_command_handler_is_ran(self):
        argv: List[str] = ['program.exe', 'command_2']
        cli: CommandLineInterface = CommandLineInterface(argv)

        command_1_handler: CommandHandlerInterface = CommandHandlerInterface()
        command_2_handler: CommandHandlerInterface = CommandHandlerInterface()
        command_3_handler: CommandHandlerInterface = CommandHandlerInterface()

        command_1_handler.run = MagicMock()
        command_2_handler.run = MagicMock()
        command_3_handler.run = MagicMock()

        cli.add_command('command_1', 'Some command 1')
        cli.add_command('command_2', 'Some command 2')
        cli.add_command('command_3', 'Some command 3')

        cli.add_command_handler('command_1', command_1_handler)
        cli.add_command_handler('command_2', command_2_handler)
        cli.add_command_handler('command_3', command_3_handler)

        cli.run()

        assert command_2_handler.run.called

    def test_proper_command_handler_is_ran_with_proper_arguments(self):
        argv: List[str] = ['program.exe', 'command_2', 'value_1', 'value_2', '-option_1', 'option_value_1', '-option_2',
                           'option_value_2', '--flag_1', '--flag_2']
        cli: CommandLineInterface = CommandLineInterface(argv)

        command_1_handler: CommandHandlerInterface = CommandHandlerInterface()
        command_2_handler: CommandHandlerInterface = CommandHandlerInterface()
        command_3_handler: CommandHandlerInterface = CommandHandlerInterface()

        command_1_handler.run = MagicMock()
        command_2_handler.run = MagicMock()
        command_3_handler.run = MagicMock()

        expected_command_values: CommandValues = ['value_1', 'value_2']
        expected_options: OptionsMap = {'-option_1': 'option_value_1',
                                        '-option_2': 'option_value_2'}
        expected_flags: FlagsMap = {'--flag_1': True,
                                    '--flag_2': True,
                                    '--flag_3': False}

        cli.add_command('command_1', 'Some command 1', allowed_options=['-option_1', '-option_2'],
                        allowed_flags=['--flag_1', '--flag_2', '--flag_3'])
        cli.add_command('command_2', 'Some command 2', num_of_required_values=2, allowed_values=ANY,
                        allowed_options=['-option_1', '-option_2'], allowed_flags=['--flag_1', '--flag_2', '--flag_3'])
        cli.add_command('command_3', 'Some command 3', allowed_options=['-option_1', '-option_2'],
                        allowed_flags=['--flag_1', '--flag_2', '--flag_3'])

        cli.add_option('-option_1', 'Some option 1')
        cli.add_option('-option_2', 'Some option 2')

        cli.add_flag('--flag_1', 'Some flag 1')
        cli.add_flag('--flag_2', 'Some flag 2')
        cli.add_flag('--flag_3', 'Some flag 3')

        cli.add_command_handler('command_1', command_1_handler)
        cli.add_command_handler('command_2', command_2_handler)
        cli.add_command_handler('command_3', command_3_handler)

        cli.run()

        command_2_handler.run.assert_called_with(expected_command_values, expected_options, expected_flags)
