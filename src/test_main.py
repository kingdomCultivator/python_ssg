import unittest

from main import extract_title


class TestTitle(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_exception(self):
        self.assertRaises(Exception, extract_title, "## Hello")
