import unittest
from typing import List
from comlint.command_line_interface import CommandLineInterface
from comlint.parsed_command import ParsedCommand
from comlint.types import OptionNames, FlagNames


class TestCommandLineInterfaceNonValueCommands(unittest.TestCase):
    def test_command_with_default_properties(self):
        argv: List[str] = ['program.exe', 'open']
        cli: CommandLineInterface = CommandLineInterface(argv)
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=[], options={}, flags={})

        cli.add_command('open', 'Command to open')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_with_one_allowed_option(self):
        argv: List[str] = ['program.exe', 'open']
        cli: CommandLineInterface = CommandLineInterface(argv)
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=[], options={}, flags={})

        allowed_options: OptionNames = ['-allowed_option']

        cli.add_command('open', 'Command to open', allowed_options=allowed_options)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_with_couple_allowed_options_and_flags(self):
        argv: List[str] = ['program.exe', 'open']
        cli: CommandLineInterface = CommandLineInterface(argv)
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=[], options={}, flags={})

        allowed_options: OptionNames = ['-allowed_option']
        allowed_flags: FlagNames = ['--allowed_flag']

        cli.add_command('open', 'Command to open', allowed_options=allowed_options, allowed_flags=allowed_flags)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_with_one_required_option(self):
        argv: List[str] = ['program.exe', 'open', '-required_option', 'required_option_value']
        cli: CommandLineInterface = CommandLineInterface(argv)

        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=[],
                                                               options={'-required_option': 'required_option_value'},
                                                               flags={})

        allowed_options: OptionNames = ['-required_option']
        required_options: OptionNames = ['-required_option']

        cli.add_command('open', 'Command to open', allowed_options=allowed_options, required_options=required_options)
        cli.add_option('-required_option', 'Some required option')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_combo(self):
        argv: List[str] = ['program.exe', 'open', '-a', '12', '-c', 'some_string', '--flag_1', '--flag_2']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='open', values=[],
                                                               options={'-a': '12',
                                                                        '-c': 'some_string'},
                                                               flags={'--flag_1': True,
                                                                      '--flag_2': True,
                                                                      '--flag_3': False})
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_command('open', 'Command to open', allowed_options=['-a', '-b', '-c'],
                        allowed_flags=['--flag_1', '--flag_2', '--flag_3'], required_options=['-a'])

        cli.add_option('-a', 'Some required option')
        cli.add_option('-b', 'Some allowed option')
        cli.add_option('-c', 'Some other allowed option')

        cli.add_flag('--flag_1', 'Some flag 1')
        cli.add_flag('--flag_2', 'Some flag 2')
        cli.add_flag('--flag_3', 'Some flag 3')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)
