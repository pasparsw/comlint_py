import unittest
from typing import List
from comlint.command_line_interface import CommandLineInterface
from comlint.parsed_command import ParsedCommand
from comlint.types import CommandName, CommandValues, OptionsMap, FlagsMap, OptionValues


class TestCommandLineInterfaceNonCommandBasedInterface(unittest.TestCase):
    def test_interface_with_a_single_option(self):
        argv: List[str] = ['program.exe', '-option', 'option_value']

        expected_command_name: CommandName = ''
        expected_command_values: CommandValues = []
        expected_options: OptionsMap = {'-option': 'option_value'}
        expected_flags: FlagsMap = {}
        expected_parsed_command: ParsedCommand = ParsedCommand(expected_command_name, expected_command_values,
                                                               expected_options, expected_flags)
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_option('-option', 'Some option')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_interface_with_a_single_option_and_predefined_option_values(self):
        argv: List[str] = ['program.exe', '-option', 'option_value_2']

        expected_command_name: CommandName = ''
        expected_command_values: CommandValues = []
        expected_options: OptionsMap = {'-option': 'option_value_2'}
        expected_flags: FlagsMap = {}
        expected_parsed_command: ParsedCommand = ParsedCommand(expected_command_name, expected_command_values,
                                                               expected_options, expected_flags)
        cli: CommandLineInterface = CommandLineInterface(argv)
        allowed_option_values: OptionValues = ['option_value_1', 'option_value_2']

        cli.add_option('-option', 'Some option', allowed_values=allowed_option_values)

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_interface_with_a_single_flag(self):
        argv: List[str] = ['program.exe', '--flag']

        expected_command_name: CommandName = ''
        expected_command_values: CommandValues = []
        expected_options: OptionsMap = {}
        expected_flags: FlagsMap = {'--flag': True}
        expected_parsed_command: ParsedCommand = ParsedCommand(expected_command_name, expected_command_values,
                                                               expected_options, expected_flags)
        cli: CommandLineInterface = CommandLineInterface(argv)

        cli.add_flag('--flag', 'Some flag')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)

    def test_combo(self):
        argv: List[str] = ['program.exe', '-option_1', 'option_value_1', '-option_2', 'option_value_2', '--flag_1',
                           '--flag_2']
        expected_command_name: CommandName = ''
        expected_command_values: CommandValues = []
        expected_options: OptionsMap = {'-option_1': 'option_value_1',
                                        '-option_2': 'option_value_2'}
        expected_flags: FlagsMap = {'--flag_1': True,
                                    '--flag_2': True,
                                    '--flag_3': False}
        expected_parsed_command: ParsedCommand = ParsedCommand(expected_command_name, expected_command_values,
                                                               expected_options, expected_flags)
        cli: CommandLineInterface = CommandLineInterface(argv)
        option_2_allowed_values: OptionValues = ['option_value_2', 'option_value_3']

        cli.add_option('-option_1', 'Some option 1')
        cli.add_option('-option_2', 'Some option 2', allowed_values=option_2_allowed_values)

        cli.add_flag('--flag_1', 'Some flag 1')
        cli.add_flag('--flag_2', 'Some flag 2')
        cli.add_flag('--flag_3', 'Some flag 3')

        parsed_command: ParsedCommand = cli.parse()

        self.assertEqual(parsed_command, expected_parsed_command)
