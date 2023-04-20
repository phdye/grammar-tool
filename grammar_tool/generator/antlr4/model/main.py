#!/usr/bin/env python

import sys
from antlr4 import *
from test_grammarLexer   import test_grammarLexer   as grammarLexer
from test_grammarParser  import test_grammarParser  as grammarParser

def main(argv):

    if len(sys.argv) > 1:
        input_ = FileStream(sys.argv[1])
    else:
        input_ = InputStream(sys.stdin.readline())

    lexer = grammarLexer(input_)
    tokens = CommonTokenStream(lexer)
    parser = grammarParser(tokens)
    tree = parser.start()

    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)
