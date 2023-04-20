import unittest

from parameterized import parameterized

from parser import Test_Parser

class Test_Case(Test_Parser):

    @parameterized.expand([ ['empty-string', '', 0],
                            ['space', ' ', 0],
                            ['tab', '\t', 0],
                            ['three spaces', '   ', 0],
                            ['three tabs', '\t\t\t', 0],
                            ['space tab space', ' \t ', 0],
                            ['tab space tab', '\t \t', 0],
                            # Including non-whitespace must fail
                            ['"x"', 'x', 1],
                            ['space carriage-return space', ' \r ', 1],
                            ['space linefeed space', ' \n ', 1],
                          ])

    def test_value(self, name, value, expected_return):
        self.parse_value(value, expected_return)
