import unittest

from include.fileByteCompare import validate_file_contents


class TestByteCompare(unittest.TestCase):
    def test_validate_file_contents(self):
        self.assertTrue(validate_file_contents('fixtures/test1.txt', 'fixtures/test2.txt'))
        self.assertFalse(validate_file_contents('fixtures/test1.txt', 'fixtures/test3.txt'))
