from io import StringIO

from antlr4 import *
from test_grammarLexer   import test_grammarLexer   as grammarLexer
from test_grammarParser  import test_grammarParser  as grammarParser

from grammar_tool.generator.parser.text import ( Test_Parser_Text,
                                                 create_test_class,
                                                 create_no_test_class,
                                               )

class Test_Parser(Test_Parser_Text):

    def parse(self, value, verbose=0):
        input_  = InputStream(StringIO(value).readline())
        lexer   = grammarLexer(input_)
        tokens  = CommonTokenStream(lexer)
        parser  = grammarParser(tokens)
        text    = parser.start().toStringTree(recog=parser)
        return text

