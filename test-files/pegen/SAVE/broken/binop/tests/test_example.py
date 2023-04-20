import unittest

from parameterized import parameterized

import ast

import math

@parameterized([
        (2, 2, 4),
        (2, 3, 8),
        (1, 9, 1),
        (0, 9, 0),
    ])
def test_pow(base, exponent, expected):
       assert_equal(math.pow(base, exponent), expected)
       
# @parameterized([
#     [ 'example' , '2 * 3', ast.BinOp(left=2, op=ast.Mult(), right=3) ],
# ])
# def test_single(name, input_, expected):
#     assertEqual(expected, expected)


# class Test_Case(unittest.TestCase):
#     @parameterized.expand([
#         [ 'example' , '2 * 3', ast.BinOp(left=2, op=ast.Mult(), right=3) ],
#     ])
#     def test_(self, name, input, expected):
#         pass

