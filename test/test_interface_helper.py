import unittest
from typing import List

from comlint.command_properties import CommandProperties
from comlint.flag_properties import FlagProperties
from comlint.interface_helper import InterfaceHelper, Commands, Options, Flags
from comlint.option_properties import OptionProperties
from comlint.types import NONE, ANY


class TestInterfaceHelper(unittest.TestCase):
    def test_is_help_required_returns_true_for_no_argument(self):
        argv: List[str] = ['program.exe']

        self.assertTrue(InterfaceHelper.is_help_required(argv, allow_no_arguments=False))

    def test_is_help_required_returns_false_for_no_argument_and_allowed_no_arguments(self):
        argv: List[str] = ['program.exe']

        self.assertFalse(InterfaceHelper.is_help_required(argv, allow_no_arguments=True))

    def test_is_help_required_returns_true_for_help_command(self):
        argv: List[str] = ['program.exe', 'help']

        self.assertTrue(InterfaceHelper.is_help_required(argv, allow_no_arguments=False))

    def test_is_help_required_returns_true_for_help_option(self):
        argv: List[str] = ['program.exe', '-h']

        self.assertTrue(InterfaceHelper.is_help_required(argv, allow_no_arguments=False))

    def test_is_help_required_returns_true_for_help_flag(self):
        argv: List[str] = ['program.exe', '--help']

        self.assertTrue(InterfaceHelper.is_help_required(argv, allow_no_arguments=False))

    def test_is_help_required_returns_false_for_other_arguments(self):
        argv: List[str] = ['program.exe', 'some_input']

        self.assertFalse(InterfaceHelper.is_help_required(argv, allow_no_arguments=False))

    def test_get_help_returns_proper_text(self):
        program_name: str = 'SomeProgram'
        program_description: str = 'Some detailed description of the application'
        commands: Commands = {'command_1': CommandProperties(allowed_values=['allowed_value_1', 'allowed_value_2'],
                                                             allowed_options=['-allowed_option_1', '-allowed_option_2'],
                                                             allowed_flags=['--allowed_flag_1', '--allowed_flag_2'],
                                                             description='Description of command_1',
                                                             num_of_required_values=0,
                                                             required_options=['-allowed_option_1']),
                              'command_2': CommandProperties(allowed_values=['allowed_value_3', 'allowed_value_4'],
                                                             allowed_options=['-allowed_option_3', '-allowed_option_4'],
                                                             allowed_flags=['--allowed_flag_3', '--allowed_flag_4'],
                                                             description='Description of command_2',
                                                             num_of_required_values=0, required_options=NONE)}
        options: Options = {'-allowed_option_1': OptionProperties(description='Description of option 1',
                                                                  allowed_values=['allowed_option_value_1', 'allowed_option_value_2'],
                                                                  default_value=''),
                            '-allowed_option_2': OptionProperties(description='Description of option 2',
                                                                  allowed_values=ANY,
                                                                  default_value='')}
        flags: Flags = {'--allowed_flag_1': FlagProperties(description='Description of flag 1'),
                        '--allowed_flag_2': FlagProperties(description='Description of flag 2')}
        
        expected_help: str = 'Usage of SomeProgram\n' \
                             'Some detailed description of the application\n' \
                             '\n' \
                             'COMMANDS:\n' \
                             'command_1                Description of command_1\n' \
                             '  allowed values         [\'allowed_value_1\', \'allowed_value_2\']\n' \
                             '  allowed options        [\'-allowed_option_1\', \'-allowed_option_2\']\n' \
                             '  allowed flags          [\'--allowed_flag_1\', \'--allowed_flag_2\']\n' \
                             '  required options       [\'-allowed_option_1\']\n' \
                             '\n' \
                             'command_2                Description of command_2\n' \
                             '  allowed values         [\'allowed_value_3\', \'allowed_value_4\']\n' \
                             '  allowed options        [\'-allowed_option_3\', \'-allowed_option_4\']\n' \
                             '  allowed flags          [\'--allowed_flag_3\', \'--allowed_flag_4\']\n' \
                             '\n' \
                             'OPTIONS:\n' \
                             '-allowed_option_1        Description of option 1\n' \
                             '  allowed values         [\'allowed_option_value_1\', \'allowed_option_value_2\']\n' \
                             '-allowed_option_2        Description of option 2\n' \
                             '\n' \
                             'FLAGS:\n' \
                             '--allowed_flag_1         Description of flag 1\n' \
                             '--allowed_flag_2         Description of flag 2\n'

        help_text: str = InterfaceHelper.get_help(program_name, program_description, commands, options, flags)

        self.assertEqual(help_text, expected_help)
