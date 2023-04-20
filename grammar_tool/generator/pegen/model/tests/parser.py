import io
import ast

from dataclasses import dataclass
from typing import Type, Iterator

from prettyprinter import pprint as pp

import token
from tokenize import TokenInfo, generate_tokens

from pegen.tokenizer import Tokenizer

from grammar_tool.generator.parser.ast import *

from grammar import GeneratedParser

#------------------------------------------------------------------------------

class CommentTokenInfo(TokenInfo):
    pass

class ErrorTokenInfo(TokenInfo):
    pass

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

class Test_Parser(Test_Parser_AST):

    def parse(self, value, verbose=0):
        # Tokenizer ERRORTOKEN and COMMENT become None
        def filter(tokengen: Iterator[TokenInfo]):
            for tok in tokengen:
                if tok.type == token.ERRORTOKEN:
                    tok = ErrorTokenInfo(token.NAME, tok.string, tok.start, tok.end, tok.line)
                if tok.type == token.COMMENT:
                    # tok = CommentTokenInfo(token.NAME, tok.string, tok.start, tok.end, tok.line)
                    continue
                yield tok
        fp = io.StringIO(value)
        tokengen = generate_tokens(fp.readline)
        tokenizer = Tokenizer(filter(tokengen), verbose=( verbose >= 2 ))
        parser = GeneratedParser(tokenizer, verbose=( verbose >= 3 ))
        return parser.start()

#------------------------------------------------------------------------------
