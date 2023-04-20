import unittest
import inspect

# from plumbum import local, commands

import io
import sys
import time
import token
import tokenize
from tokenize import TokenInfo
import ast
import argparse
from dataclasses import dataclass
from typing import Type, Iterator

from pegen.tokenizer import Tokenizer # , Mark, exact_token_types
from pegen.parser import Parser
import pegen

class CommentTokenInfo(TokenInfo):
    pass

class ErrorTokenInfo(TokenInfo):
    pass

#------------------------------------------------------------------------------

import ast

from dataclasses import dataclass

from tokenize import TokenInfo

from typing import Type

@dataclass
class _Token(ast.AST):
    value : str
    token : TokenInfo = None
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

@dataclass
class _TokenList(_Token):
    value : list

#------------------------------------------------------------------------------

# 'tests/grammar.py' -- populated by 'grammar-tool --style pegen init'
from grammar import GeneratedParser

class Test_Parser(unittest.TestCase):

    def parse(self, value):
        # Tokenizer ERRORTOKEN and COMMENT become None 
        def filter(tokengen: Iterator[TokenInfo]):
            for tok in tokengen:
                if tok.type == token.ERRORTOKEN:
                    tok = ErrorTokenInfo(token.NAME, tok.string, tok.start, tok.end, tok.line)
                if tok.type == token.COMMENT:
                    tok = CommentTokenInfo(token.NAME, tok.string, tok.start, tok.end, tok.line)
                yield tok
        fp = io.StringIO(value)
        tokengen = tokenize.generate_tokens(fp.readline)
        tokenizer = Tokenizer(filter(tokengen), verbose=False)
        parser = GeneratedParser(tokenizer, verbose=False)
        return parser.start()
    
    def parse_value(self, value, expected_return):
        if isinstance(expected_return, Exception):
            with self.assertRaises(type(expected_return)):
               tree = self.parse(value)
               print(tree)
               self.assertEqual( tree, None,
                                 "Error, parse succeeded but should have failed")
        else:
            tree = self.parse(value)
            self.assertEqual( tree, expected_return )


def parser_create_class(name, test_map):
    code = f"""
from parameterized import parameterized

from parser import Test_Parser

class Test_{name}(Test_Parser):
    @parameterized.expand({test_map})
    def test_(self, name, value, expected_return):
        if ( isinstance(expected_return, list) and expected_return and 
             expected_return[0] == 'eval' ):
            expected_return = [ eval(expected_return[1]) ]
        self.parse_value(value, expected_return)
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

