import inspect
import plumbum
import textwrap
import json

from typing import Callable

from dataclasses import dataclass

#------------------------------------------------------------------------------

# Special Expected Values

# DIITO => expect the same value as the input string
# Possible modifiers:  str.strip, 
class _Ditto:
    def __init__(self, modify : Callable = None):
        self.modify = modify
    def __repr__(self):
        return 'DITTO'
    def filter(self, value):
        return value
DITTO = _Ditto()

@dataclass
class _Single(_Ditto):
    chars_in    : str
    def __repr__(self):
        return f"{self.__class__.__name__}('{json.dumps(self.chars_in)}')"

@dataclass
class Replace(_Ditto):
    chars_in    : str
    chars_out   : str = ''
    # def __init__(self, chars_in : str, chars_out : str = ''):
    #     super().__init__()
    #     self.chars_in = chars_in
    #     self.chars_out = chars_out
    def X__post_init__(self):
        print(f"Replace '{self.chars_in}' -> '{self.chars_out}'")        
    def filter(self, value):
        return value.replace(self.chars_in, self.chars_out)
        # new = value.replace(self.chars_in, self.chars_out)
        # print()
        # print()
        # print(f"FILTER '{value}' -> '{new}'  :  chars IN '{self.chars_in}' -> '{self.chars_out}'")
        # print()
        # return new
    def __repr__(self):
        # return f"Replace('{self.chars_in.encode('unicode-escape')}', '{json.dumps(self.chars_out)}')"
        return f"Replace('{self.chars_in}', '{json.dumps(self.chars_out)}')"
    

@dataclass
class Without(Replace):
    def __init__(self, chars_in : str):
        super().__init__(chars_in, '')
        # print(f"Without '{self.chars_in}'")
    def __repr__(self):
        return f"Without('{self.chars_in}')"


class _Fail ( plumbum.commands.ProcessExecutionError ):
    @classmethod
    def actual_type(cls):
        return plumbum.commands.ProcessExecutionError
    def __repr__(self):
        return 'FAIL'
FAIL = _Fail([], 1, '', '')

#------------------------------------------------------------------------------

def create_test_class(name, test_map):

    source = textwrap.dedent( f"""
        from parameterized import parameterized

        from parser import Test_Parser

        class Test_{name}(Test_Parser):
            @parameterized.expand({test_map})
            def test_(self, name, value, expected_return):
                self.parse_and_verify(value, expected_return)
    """)

    # print() ; print(source) ; print()
    
    exec ( source, inspect.stack()[1][0].f_globals, inspect.stack()[1][0].f_locals )

#------------------------------------------------------------------------------
    
def create_no_test_class(name):

    source = textwrap.dedent( f"""
        import unittest

        class Test_{name}(unittest.TestCase):
            def test_pass(self):
                pass
    """)

    # print() ; print(source) ; print()
    
    exec ( source, inspect.stack()[1][0].f_globals, inspect.stack()[1][0].f_locals )

#------------------------------------------------------------------------------
