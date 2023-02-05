import unittest

from comlint.interface_validator import InterfaceValidator


class TestInterfaceValidator(unittest.TestCase):
    def test_is_command_name_valid_returns_true_for_single_character_command_name(self):
        self.assertTrue(InterfaceValidator.is_command_name_valid('a'))

    def test_is_command_name_valid_returns_true_for_regular_command_name(self):
        self.assertTrue(InterfaceValidator.is_command_name_valid('some_command'))

    def test_is_command_name_valid_returns_true_for_command_name_containing_all_alphanumerical_characters(self):
        self.assertTrue(InterfaceValidator.is_command_name_valid('abcdefghijklmnoprstuwxyz0123456789'))

    def test_is_command_name_valid_returns_true_for_command_name_with_dash_in_the_middle(self):
        self.assertTrue(InterfaceValidator.is_command_name_valid('some-command'))

    def test_is_command_name_valid_returns_false_for_empty_command_name(self):
        self.assertFalse(InterfaceValidator.is_command_name_valid(''))

    def test_is_command_name_valid_returns_false_for_command_name_with_option_prefix(self):
        self.assertFalse(InterfaceValidator.is_command_name_valid('-command'))

    def test_is_command_name_valid_returns_false_for_command_name_with_flag_prefix(self):
        self.assertFalse(InterfaceValidator.is_command_name_valid('--command'))

    def test_is_option_name_valid_returns_true_for_single_character_option_name(self):
        self.assertTrue(InterfaceValidator.is_option_name_valid('-a'))

    def test_is_option_name_valid_returns_true_for_regular_option_name(self):
        self.assertTrue(InterfaceValidator.is_option_name_valid('-option'))

    def test_is_option_name_valid_returns_true_for_option_name_containing_all_alphanumerical_characters(self):
        self.assertTrue(InterfaceValidator.is_option_name_valid('-abcdefghijklmnoprstuwxyz0123456789'))

    def test_is_option_name_valid_returns_false_for_empty_option_name(self):
        self.assertFalse(InterfaceValidator.is_option_name_valid(''))

    def test_is_option_name_valid_returns_false_for_option_name_with_no_option_prefix(self):
        self.assertFalse(InterfaceValidator.is_option_name_valid('option'))

    def test_is_option_name_valid_returns_false_for_option_name_with_flag_prefix(self):
        self.assertFalse(InterfaceValidator.is_option_name_valid('--option'))

    def test_is_flag_name_valid_returns_true_for_single_character_flag_name(self):
        self.assertTrue(InterfaceValidator.is_flag_name_valid('--a'))

    def test_is_flag_name_valid_returns_true_for_regular_flag_name(self):
        self.assertTrue(InterfaceValidator.is_flag_name_valid('--flag'))

    def test_is_flag_name_valid_returns_true_for_flag_name_containing_all_alphanumerical_characters(self):
        self.assertTrue(InterfaceValidator.is_flag_name_valid('--abcdefghijklmnoprstuwxyz0123456789'))

    def test_is_flag_name_valid_returns_false_for_empty_flag_name(self):
        self.assertFalse(InterfaceValidator.is_flag_name_valid(''))

    def test_is_flag_name_valid_returns_false_for_flag_name_with_no_flag_prefix(self):
        self.assertFalse(InterfaceValidator.is_flag_name_valid('flag'))

    def test_is_flag_name_valid_returns_false_for_flag_name_with_option_prefix(self):
        self.assertFalse(InterfaceValidator.is_flag_name_valid('-flag'))
