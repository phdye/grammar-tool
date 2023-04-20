import os
import re
import unittest
from plumbum import local, commands

from parameterized import parameterized

from parser import Test_Parser

test_cases = [
    ['space', ' ', 0],
    ['tab', '\t', 0],
    ['carriage-return', '\r', 1],
    ['linefeed', '\n', 1],
]

class Test_This_Peg(Test_Parser):

    @parameterized.expand(test_cases)
    def test_value(self, name, value, expected_return):
        self.parse_value(value, expected_return)

