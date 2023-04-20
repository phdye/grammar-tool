import unittest

from parameterized import parameterized

from nose.tools import assert_equal
import math

@parameterized([
        (2, 2, 4),
        (2, 3, 8),
        (1, 9, 1),
        (0, 9, 0),
    ])
def test_pow(base, exponent, expected):
       assert_equal(math.pow(base, exponent), expected)
