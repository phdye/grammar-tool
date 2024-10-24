import unittest
import inspect

import io
import sys

from dataclasses import dataclass
from typing import Type, Iterator

from prettyprinter import pprint as pp

# Import AST changes if any provided for the parser generator or
# along with the grammar being tested.
try :
    import astpatch
except :
    pass

# the generated grammar
import grammar

class Test_Parser_AST(unittest.TestCase):

    def parse(self, value, verbose=0):
        raise NotImplementedError()

    def parse_value(self, value, expected_return, verbose=0):
        if isinstance(expected_return, Exception):
            with self.assertRaises(type(expected_return)):
               tree = self.parse(value, verbose=verbose)
               print('= = = = =')
               print(f"Error:  parse '{value}' was expected to raise "
                     f"{type(expected_return)}.")
               pp(tree)
               print('= = = = =')
               self.assertEqual( tree, None,
                                 "Error, parse succeeded but should have failed")
        else:
            tree = self.parse(value, verbose=verbose)
            # pp(tree) ; print('= = = = =')
            self.assertEqual( tree, expected_return )


def parser_create_class(name, test_map, verbose=0):
    code = f"""
from parameterized import parameterized

# From s/generator/<style>/model/tests/parser.py populated as work/tests/parser.py
from parser import Test_Parser

class Test_{name}(Test_Parser):
    @parameterized.expand({test_map})
    def test_(self, name, value, expected_return):
        if ( isinstance(expected_return, list) and expected_return and 
             expected_return[0] == 'eval' ):
            expected_return = [ eval(expected_return[1]) ]
        self.parse_value(value, expected_return, verbose={verbose})
"""
    # print(code)
    exec(code, inspect.currentframe().f_back.f_globals)

create_test_class = parser_create_class


def parser_create_no_class(name):
    exec ( f"""
import unittest

class Test_{name}(unittest.TestCase):
    def test_pass(self):
        pass
""", inspect.stack()[1][0].f_globals )

create_no_test_class = parser_create_no_class

