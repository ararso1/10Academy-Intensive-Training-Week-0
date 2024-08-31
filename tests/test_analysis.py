# tests/test_analysis.py
import pytest
import unittest
from src.data_loader import load_data

def test_your_function():
    # Example unit test
    # result = your_function(some_input)
    # expected = some_expected_output
    # assert result == expected, "Test failed: Expected {}, got {}".format(expected, result)
    print('here')

    # tests/test_data_loader.py

class TestDataLoader(unittest.TestCase):

    def test_load_data(self):
        data = load_data() # type: ignore
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
