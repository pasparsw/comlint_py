import unittest
from comlint.command_properties import CommandProperties
from comlint.types import ANY, NONE


class TestCommandProperties(unittest.TestCase):
    def test_requires_value_returns_true(self):
        num_of_required_values: int = 1
        command_properties: CommandProperties = CommandProperties(ANY, NONE, NONE, "", num_of_required_values, NONE)

        self.assertTrue(command_properties.requires_value())

    def test_requires_value_returns_false(self):
        num_of_required_values: int = 0
        command_properties: CommandProperties = CommandProperties(ANY, NONE, NONE, "", num_of_required_values, NONE)

        self.assertFalse(command_properties.requires_value())
