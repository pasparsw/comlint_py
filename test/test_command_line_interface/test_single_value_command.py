import unittest
from typing import List
from comlint.command_line_interface import CommandLineInterface
from comlint.parsed_command import ParsedCommand
from comlint.types import CommandName, CommandValues, OptionsMap, FlagsMap, OptionValues


class TestCommandLineInterfaceSingleValueCommands(unittest.TestCase):
    def test_command_accepting_any_value(self):
        argv: List[str] = ['program.exe', 'open', '/some/file.txt']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=['/some/file.txt'], options={},
                                                               flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('open', 'Command to open file', num_of_required_values=1)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_accepting_predefined_values(self):
        argv: List[str] = ['program.exe', 'open', 'file']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=['file'], options={},
                                                               flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('open', 'Command to open file', num_of_required_values=1,
                        allowed_values=['file', 'application'])

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_with_one_allowed_option(self):
        argv: List[str] = ['program.exe', 'open', '/some/file.txt']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=['/some/file.txt'], options={},
                                                               flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('open', 'Command to open file', num_of_required_values=1, allowed_options=['-allowed_option'])

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_with_couple_allowed_options_and_flags(self):
        argv: List[str] = ['program.exe', 'open', '/some/file.txt']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=['/some/file.txt'], options={},
                                                               flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('open', 'Command to open file', num_of_required_values=1, allowed_options=['-allowed_option'],
                        allowed_flags=['--allowed_flag'])

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_with_one_required_option(self):
        argv: List[str] = ['program.exe', 'open', '/some/file.txt', '-required_option', 'required_option_value']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=['/some/file.txt'],
                                                               options={'-required_option': 'required_option_value'},
                                                               flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('open', 'Command to open file', num_of_required_values=1, allowed_options=['-required_option'],
                        required_options=['-required_option'])
        cli.add_option('-required_option', 'Some required option')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_combo(self):
        argv: List[str] = ['program.exe', 'open', '/some/file.txt', '-a', '12', '-c', 'some_string', '--flag_1', '--flag_2']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=['/some/file.txt'],
                                                               options={'-a': '12',
                                                                        '-c': 'some_string'},
                                                               flags={'--flag_1': True,
                                                                      '--flag_2': True,
                                                                      '--flag_3': False})
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('open', 'Command to open', num_of_required_values=1, allowed_options=['-a', '-b', '-c'],
                        allowed_flags=['--flag_1', '--flag_2', '--flag_3'], required_options=['-a'])

        cli.add_option('-a', 'Some required option')
        cli.add_option('-b', 'Some allowed option')
        cli.add_option('-c', 'Some other allowed option')

        cli.add_flag('--flag_1', 'Some flag 1')
        cli.add_flag('--flag_2', 'Some flag 2')
        cli.add_flag('--flag_3', 'Some flag 3')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)
