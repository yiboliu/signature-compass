import unittest
import re

from server.utils import analyze_regex
from server.utils import RegexType


class TestAnalyzeRegex(unittest.TestCase):

    def test_start_pattern(self):
        self.assertEqual(analyze_regex("^hello"), RegexType.START)

    def test_end_pattern(self):
        self.assertEqual(analyze_regex("world$"), RegexType.END)

    def test_contain_pattern(self):
        self.assertEqual(analyze_regex("content"), RegexType.CONTAIN)

    def test_unknown_pattern(self):
        self.assertEqual(analyze_regex("*invalid*"), RegexType.UNKNOWN)

    def test_start_and_end_not_supported(self):
        self.assertEqual(analyze_regex("^start$"), RegexType.UNKNOWN)

    def test_special_characters(self):
        self.assertEqual(analyze_regex("\\d+"), RegexType.UNKNOWN)


if __name__ == '__main__':
    unittest.main()