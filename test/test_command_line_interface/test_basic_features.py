import unittest
from typing import List

from comlint.command_line_interface import CommandLineInterface
from comlint.parsed_command import ParsedCommand


class TestCommandLineInterfaceBasicFeatures(unittest.TestCase):
    def test_parse_returns_empty_parsed_command_if_input_contains_help_command(self):
        argv: List[str] = ['program.exe', 'help']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='help', values=[], options={}, flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_parse_returns_empty_parsed_command_if_input_contains_help_option(self):
        argv: List[str] = ['program.exe', '-h']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='help', values=[], options={}, flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_parse_returns_empty_parsed_command_if_input_contains_help_flag(self):
        argv: List[str] = ['program.exe', '--help']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='help', values=[], options={}, flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)
