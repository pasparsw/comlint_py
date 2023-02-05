import unittest

from comlint.parsed_command import ParsedCommand
from comlint.types import CommandName, CommandValues, OptionsMap, FlagsMap


class TestParsedCommand(unittest.TestCase):
    def test_is_option_used_returns_true(self):
        command_name: CommandName = 'command'
        values: CommandValues = []
        options: OptionsMap = {'-option_name': 'option_value'}
        flags: FlagsMap = {}
        parsed_command: ParsedCommand = ParsedCommand(command_name, values, options, flags)

        self.assertTrue(parsed_command.is_option_used(option_name='-option_name'))

    def test_is_option_used_returns_false(self):
        command_name: CommandName = 'command'
        values: CommandValues = []
        options: OptionsMap = {'-option_name': 'option_value'}
        flags: FlagsMap = {}
        parsed_command: ParsedCommand = ParsedCommand(command_name, values, options, flags)

        self.assertFalse(parsed_command.is_option_used(option_name='-some_option_name'))
