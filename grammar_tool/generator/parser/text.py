import unittest
import inspect

from typing import Any

from prettyprinter import pprint as pp

from .common import *

class Test_Parser_Text(unittest.TestCase):

    def parse(self, value, verbose=0):
        raise NotImplementedError

    def parse_and_verify(self, value : str, expected : Any,
                         verbose : int = 0) -> None :

        if isinstance(expected, Exception):
            self.parse_value_exception(value, expected, verbose)
        elif isinstance(expected, type(DITTO)):
            self.parse_value_string(value, expected.filter(value), verbose)
        elif isinstance(expected, str):
            self.parse_value_string(value, expected, verbose)
        else:
            raise ValueError(f"Unknown type for <expected> '{type(expected)}'.  "
                             "Please provide a string, DITTO/Replace/Without or FAIL.")


    def parse_value_exception(self, value : str, expected_exception : Exception,
                           verbose : int = 0) -> None :
        
        expected_exception_type = type(expected_exception)
        try :
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

    def parse_value_string(self, value : str, expected_value : str,
                           verbose : int = 0) -> None :

        output = self.parse(value, verbose=verbose)
        # pp(output) ; print('= = = = =')
        self.assertEqual( output, expected_value )

