import unittest
from typing import List

from comlint.command_line_interface import CommandLineInterface
from comlint.parsed_command import ParsedCommand
from comlint.types import CommandValues


class TestCommandLineInterfaceMultipleValueCommands(unittest.TestCase):
    def test_command_accepting_any_two_values(self):
        argv: List[str] = ['program.exe', 'copy', '/dst/from', '/dst/to']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='copy', values=['/dst/from', '/dst/to'], options={},
                                                               flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)
        num_of_req_command_values: int = 2

        cli.add_command('copy', 'Command to copy folders', num_of_req_command_values)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_command_accepting_predefined_two_values(self):
        argv: List[str] = ['program.exe', 'list_files', 'txt', 'pdf']
        expected_parsed_command: ParsedCommand = ParsedCommand(name='list_files', values=['txt', 'pdf'], options={},
                                                               flags={})
        cli: CommandLineInterface = CommandLineInterface(argv)
        num_of_req_command_values: int = 2
        allowed_values: CommandValues = ['txt', 'pdf', 'zip', 'jpg', 'gif']

        cli.add_command('list_files', 'Command to list all files of a given type (max two types allowed)',
                        num_of_req_command_values, allowed_values)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)
