import unittest
import comlint.utils as utils


class TestUtils(unittest.TestCase):
    def test_get_similar_keys_returns_proper_values(self):
        some_dict: dict = {'open_file': 1,
                           'open_folder': 2,
                           'close_file': 3,
                           'close_folder': 4}

        similar_values_1: str = utils.get_similar_keys(some_dict, value='open', delimiter=', ')
        similar_values_2: str = utils.get_similar_keys(some_dict, value='file', delimiter=', ')
        similar_values_3: str = utils.get_similar_keys(some_dict, value='run_open_file', delimiter=', ')
        similar_values_4: str = utils.get_similar_keys(some_dict, value='abcdef', delimiter=', ')

        expected_values_1: str = 'open_file, open_folder'
        expected_values_2: str = 'open_file, close_file'
        expected_values_3: str = 'open_file'
        expected_values_4: str = ''

        self.assertEqual(similar_values_1, expected_values_1)
        self.assertEqual(similar_values_2, expected_values_2)
        self.assertEqual(similar_values_3, expected_values_3)
        self.assertEqual(similar_values_4, expected_values_4)

    def test_get_similar_values_returns_proper_values(self):
        some_list: list = ['open_file', 'open_folder', 'close_file', 'close_folder']

        self.assertEqual(utils.get_similar_values(some_list, value='open', delimiter=', '), 'open_file, open_folder')
        self.assertEqual(utils.get_similar_values(some_list, value='file', delimiter=', '), 'open_file, close_file')
        self.assertEqual(utils.get_similar_values(some_list, value='run_open_file', delimiter=', '), 'open_file')
        self.assertEqual(utils.get_similar_values(some_list, value='abcdef', delimiter=', '), '')
