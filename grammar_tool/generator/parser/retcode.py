import unittest
import inspect

from typing import Any

from plumbum import commands

from prettyprinter import cpprint as pp

from .common import *

import plumbum

class Test_Parser_Retcode(unittest.TestCase):

    def parse(self, value : str, verbose : int = 0 ) -> Any :
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

            bg = self.parse(value, verbose=verbose)

            # STDOUT strip trailing newline, if any
            text = bg.stdout
            if len(bg.stdout) >= 2 and text[-2:] == '\r\n':
                text = text[:-2]
            elif len(bg.stdout) >= 1 and text[-1] in ['\n', '\r']:
                text = text[:-1]
            # STDERR strip leading and trailing whitespace
            err_text = bg.stderr.strip()
    
            print('= = = = =')
            print(f"Error:  parse '{value}' was expected to raise "
                  f"{expected_exception_type}.")
            print('= = STDOUT = =')
            pp(text)
            print('= = STDERR = =')
            pp(err_text)
            print('= = = = =')

            self.assertNotEqual( bg.returncode, 0, "Error, parse succeeded when "
                                 "it should have failed.")


    def parse_value_string(self, value : str, expected_value : str,
                           verbose : int = 0) -> None :

        try :

            with self.subTest("parse value externally", input_value=value):
                bg = self.parse(value, verbose=verbose)

            # STDOUT strip trailing newline, if any
            text = bg.stdout
            if len(bg.stdout) >= 2 and text[-2:] == '\r\n':
                text = text[:-2]
            elif len(bg.stdout) >= 1 and text[-1] in ['\n', '\r']:
                text = text[:-1]
            # STDERR strip leading and trailing whitespace
            err_text = bg.stderr.strip()

            with self.subTest("exit code 0", bg_retcode=bg.returncode, expected_retcode=0):
                self.assertEqual(bg.returncode, 0)
            with self.subTest("stdout text", output=text, expected=expected_value):
                self.assertEqual(text, expected_value)
            with self.subTest("stderr empty", error_text=err_text, expected=''):
                self.assertEqual(err_text, '')

        except commands.processes.ProcessExecutionError:

            self.assertFalse(f"Unexpected ProcessExecutionError for value '{value}',"
                             f" expected retcode 0, "
                             f" with output '{expected_value}'")

