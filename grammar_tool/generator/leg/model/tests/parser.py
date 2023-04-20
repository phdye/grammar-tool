import unittest
import inspect

from plumbum import commands, local, BG

parser = local['parse/parser']

class Test_Parser(unittest.TestCase):
    def parse_value(self, value, expected_value):
        try :
            # (parser << value)(retcode = expected_return)
            bg = ( parser << value ) & BG
            bg.wait()
            #print("")
            #print(f"=== Parse output = '{bg.stdout.strip()}'")
            #print("")
            self.assertEqual(bg.stdout[:-1], expected_value)
            self.assertEqual(bg.stderr.strip(), '')
        except commands.processes.ProcessExecutionError:
            self.assertFalse(f"ProcessExecutionError for value '{value}',"
                             f" expected output '{expected_value}', "
                             f" received output '{bg.stdout[:-1]}'")

def create_test_class(name, test_map):
    exec ( f"""
from parameterized import parameterized

from parser import Test_Parser

class Test_{name}(Test_Parser):
    @parameterized.expand({test_map})
    def test_(self, name, value, expected_return):
        self.parse_value(value, expected_return)
""", inspect.stack()[1][0].f_globals )

def create_no_test_class(name):
    exec ( f"""
import unittest

class Test_{name}(unittest.TestCase):
    def test_pass(self):
        pass
""", inspect.stack()[1][0].f_globals )
