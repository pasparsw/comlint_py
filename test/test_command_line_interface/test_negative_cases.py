import unittest
from typing import List

from comlint.command_handler_interface import CommandHandlerInterface
from comlint.command_line_interface import CommandLineInterface
from comlint.exceptions.duplicated_command import DuplicatedCommand
from comlint.exceptions.duplicated_flag import DuplicatedFlag
from comlint.exceptions.duplicated_option import DuplicatedOption
from comlint.exceptions.forbidden_flag import ForbiddenFlag
from comlint.exceptions.forbidden_option import ForbiddenOption
from comlint.exceptions.forbidden_option_value import ForbiddenOptionValue
from comlint.exceptions.invalid_command_name import InvalidCommandName
from comlint.exceptions.invalid_flag_name import InvalidFlagName
from comlint.exceptions.invalid_option_name import InvalidOptionName
from comlint.exceptions.missing_command_handler import MissingCommandHandler
from comlint.exceptions.missing_command_value import MissingCommandValue
from comlint.exceptions.missing_option_value import MissingOptionValue
from comlint.exceptions.missing_required_option import MissingRequiredOption
from comlint.exceptions.unsupported_command import UnsupportedCommand
from comlint.exceptions.unsupported_command_value import UnsupportedCommandValue
from comlint.exceptions.unsupported_flag import UnsupportedFlag
from comlint.exceptions.unsupported_option import UnsupportedOption
from comlint.types import CommandValues, OptionValues, OptionNames, FlagNames, NONE


class TestCommandLineInterfaceNegativeCases(unittest.TestCase):
    def test_parse_throws_unsupported_command(self):
        argv: List[str] = ['program.exe', 'unsupported_command']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('supported_command', 'Some supported command')

        with self.assertRaises(UnsupportedCommand):
            cli.parse()

    def test_parse_throws_missing_command_value(self):
        argv: List[str] = ['program.exe', 'supported_command']
        cli: CommandLineInterface = CommandLineInterface(argv)

        num_of_required_values: int = 1

        cli.add_command('supported_command', 'Some supoprted_command', num_of_required_values)

        with self.assertRaises(MissingCommandValue):
            cli.parse()

    def test_parse_throws_missing_command_value_when_option_follows_command(self):
        argv: List[str] = ['program.exe', 'supported_command', '-option', '-option_value']
        cli: CommandLineInterface = CommandLineInterface(argv)

        num_of_required_values: int = 1

        cli.add_command('supported_command', 'Some supported_command', num_of_required_values)
        cli.add_option('-option', 'Some option')

        with self.assertRaises(MissingCommandValue):
            cli.parse()

    def test_parse_throws_missing_command_value_when_flag_follows_command(self):
        argv: List[str] = ['program.exe', 'supported_command', '--flag']
        cli: CommandLineInterface = CommandLineInterface(argv)

        num_of_required_values: int = 1

        cli.add_command('supported_command', 'Some supported_command', num_of_required_values)
        cli.add_flag('--flag', 'Some flag')

        with self.assertRaises(MissingCommandValue):
            cli.parse()

    def test_parse_throws_unsupported_command_value(self):
        argv: List[str] = ['program.exe', 'supported_command', 'unsupported_value']
        cli: CommandLineInterface = CommandLineInterface(argv)

        num_of_required_values: int = 1
        allowed_values: CommandValues = ["supported_value"]

        cli.add_command('supported_command', 'Some supported_command', num_of_required_values, allowed_values)

        with self.assertRaises(UnsupportedCommandValue):
            cli.parse()

    def test_parse_throws_unsupported_option(self):
        argv: List[str] = ['program.exe', 'supported_command', '-unsupported_option', 'option_value']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('supported_command', 'Some supported_command')

        with self.assertRaises(UnsupportedOption):
            cli.parse()

    def test_parse_throws_missing_required_option(self):
        argv: List[str] = ['program.exe', 'supported_command', '-allowed_option', 'some_value']
        cli: CommandLineInterface = CommandLineInterface(argv)
        allowed_options: OptionNames = ['-allowed_option', '-required_option']
        allowed_flags: FlagNames = NONE
        required_options: OptionNames = ['-required_option']

        cli.add_command('supported_command', 'Some supported_command', allowed_options=allowed_options,
                        allowed_flags=allowed_flags, required_options=required_options)

        cli.add_option('-allowed_option', 'Some allowed option')
        cli.add_option('-required_option', 'Some required option')

        with self.assertRaises(MissingRequiredOption):
            cli.parse()

    def test_parse_throws_missing_option_value(self):
        argv: List[str] = ['program.exe', 'command', '-option_name']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('command', 'Some command')
        cli.add_option('-option_name', 'Some option')

        with self.assertRaises(MissingOptionValue):
            cli.parse()

    def test_parse_throws_forbidden_option(self):
        argv: List[str] = ['program.exe', 'command_2', '-option_1', 'option_value']
        cli: CommandLineInterface = CommandLineInterface(argv)

        command_1_allowed_options: OptionNames = ['-option_1']

        cli.add_command('command_1', 'Some command 1', allowed_options=command_1_allowed_options)
        cli.add_command('command_2', 'Some command 2')

        cli.add_option('-option_1', 'Some option')

        with self.assertRaises(ForbiddenOption):
            cli.parse()

    def test_parse_throws_forbidden_option_for_specified_allowed_options(self):
        argv: List[str] = ['program.exe', 'command_1', '-option_2', 'option_value']
        cli: CommandLineInterface = CommandLineInterface(argv)

        command_1_allowed_options: OptionNames = ['-option_1']
        command_2_allowed_options: OptionNames = ['-option_2']

        cli.add_command('command_1', 'Some command 1', allowed_options=command_1_allowed_options)
        cli.add_command('command_2', 'Some command 2', allowed_options=command_2_allowed_options)

        cli.add_option('-option_1', 'Some option 1')
        cli.add_option('-option_2', 'Some option 2')

        with self.assertRaises(ForbiddenOption):
            cli.parse()

    def test_parse_throws_forbidden_option_value(self):
        argv: List[str] = ['program.exe', 'command', '-option', 'forbidden_option_value']
        cli: CommandLineInterface = CommandLineInterface(argv)

        command_allowed_options: OptionNames = ['-option']
        option_allowed_values: OptionNames = ['allowed_option_value_1', 'allowed_option_value_2']

        cli.add_command('command', 'Some command', allowed_options=command_allowed_options)

        cli.add_option('-option', 'Some option', allowed_values=option_allowed_values)

        with self.assertRaises(ForbiddenOptionValue):
            cli.parse()

    def test_parse_throws_unsupported_flag(self):
        argv: List[str] = ['program.exe', 'command', '--unsupported_flag']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('command', 'Some command')

        with self.assertRaises(UnsupportedFlag):
            cli.parse()

    def test_parse_throws_forbidden_flag(self):
        argv: List[str] = ['program.exe', 'command', '--flag_1']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('command', 'Some command')
        cli.add_flag('--flag_1', 'Some flag 1')

        with self.assertRaises(ForbiddenFlag):
            cli.parse()

    def test_throws_forbidden_flag_for_specified_allowed_flags(self):
        argv: List[str] = ['program.exe', 'command', '--flag_2']
        cli: CommandLineInterface = CommandLineInterface(argv)

        allowed_options: OptionNames = NONE
        allowed_flags: FlagNames = ['--flag_1']

        cli.add_command('command', 'Some command', allowed_options=allowed_options, allowed_flags=allowed_flags)

        cli.add_flag('--flag_1', 'Some flag 1')
        cli.add_flag('--flag_2', 'Some flag 2')

        with self.assertRaises(ForbiddenFlag):
            cli.parse()

    def test_add_command_handler_throws_unsupported_command(self):
        argv: List[str] = ['program.exe']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('command', 'Some command')

        with self.assertRaises(UnsupportedCommand):
            cli.add_command_handler('unsupported_command', CommandHandlerInterface())

    def test_add_command_handler_throws_missing_command_handler(self):
        argv: List[str] = ['program.exe', 'command_2']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('command_1', 'Some command 1')
        cli.add_command('command_2', 'Some command 2')

        command_1_handler: CommandHandlerInterface = CommandHandlerInterface()

        cli.add_command_handler('command_1', command_1_handler)

        with self.assertRaises(MissingCommandHandler):
            cli.run()

    def test_add_command_throws_invalid_command_name(self):
        argv: List[str] = ['program.exe']
        cli: CommandLineInterface = CommandLineInterface(argv)

        with self.assertRaises(InvalidCommandName):
            cli.add_command('-command', 'Some command')

    def test_add_command_throws_duplicated_command(self):
        argv: List[str] = ['program.exe']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('command', 'Some command')

        with self.assertRaises(DuplicatedCommand):
            cli.add_command('command', 'Some command')

    def test_add_option_throws_invalid_option_name(self):
        argv: List[str] = ['program.exe']
        cli: CommandLineInterface = CommandLineInterface(argv)

        with self.assertRaises(InvalidOptionName):
            cli.add_option('option', 'Some option')

    def test_add_option_throws_duplicated_option(self):
        argv: List[str] = ['program.exe']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_option('-option', 'Some option')

        with self.assertRaises(DuplicatedOption):
            cli.add_option('-option', 'Some option')

    def test_add_flag_throws_invalid_flag_name(self):
        argv: List[str] = ['program.exe']
        cli: CommandLineInterface = CommandLineInterface(argv)

        with self.assertRaises(InvalidFlagName):
            cli.add_flag('flag', 'Some flag')

    def test_add_flag_throws_duplicated_flag(self):
        argv: List[str] = ['program.exe']
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_flag('--flag', 'Some flag')

        with self.assertRaises(DuplicatedFlag):
            cli.add_flag('--flag', 'Some flag')
