import unittest

# import io
# import sys
import ast

# from dataclasses import dataclass
from typing import Any
# , Type
# , Iterator

from .common import *

from prettyprinter import pprint as pp

# Import AST changes if any provided for the parser generator or
# along with the grammar being tested.
try :
    import astpatch
except :
    pass

# AST_ROOTS = (ast.AST, grammar.Tree, grammar.Token, list, type(None))

#------------------------------------------------------------------------------

class Test_Parser_AST(unittest.TestCase):

    def parse(self, value, verbose=0):
        raise NotImplementedError

    def parse_and_verify(self, value : str, expected : Any,
                         verbose : int = 0) -> None :

        if isinstance(expected, Exception):
            self.parse_value_exception(value, expected, verbose)
        # elif isinstance(expected, type(DITTO)):
        #     self.parse_value_as_ast(value, expected.filter(value), verbose)
        #     # Doesn't appear to be relevant to AST
        elif isinstance(expected, astpatch.AST_ROOTS):
            self.parse_value_to_ast(value, expected, verbose)
        else:
            raise ValueError(f"Unknown type for <expected> '{type(expected)}'.  "
                             "Please provide a string, DITTO/Replace/Without or FAIL.")


    def parse_value_exception(self, value : str, expected_exception : Exception,
                           verbose : int = 0) -> None :
        
        expected_exception_type = type(expected_exception)
        try :
            # FAIL is a subclass of plumbum.commands.ProcessExecutionError
            # but assertRaises() must be provided the actual exception type
            # which ill be raised.
            expected_exception_type = expected_exception_type.actual_type()
        except :
            pass

        with self.assertRaises(expected_exception_type):
            output = self.parse(value, verbose=verbose)
            print('= = = = =')
            print(f"Error:  parse '{value}' was expected to raise "
                  f"{type(expected_exception)}.")
            print('= = STDOUT = =')
            pp(output)
            print('= = = = =')
            self.assertEqual( output, None, "Error, parse succeeded when "
                              "it should have failed.")

    def parse_value_to_ast(self, value : str, expected_value : str,
                               verbose : int = 0) -> None :

        tree = self.parse(value, verbose=verbose)
        # pp(tree) ; print('= = = = =')
        self.assertEqual( tree, expected_value )

