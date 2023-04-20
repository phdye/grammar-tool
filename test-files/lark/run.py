#!/usr/bin/env python

import sys

sys.path.insert(0, 'work')

from grammar import Lark_StandAlone

code = sys.stdin.read()

parser = Lark_StandAlone()
tree = parser.parse(code)

print("- - - - -")
print(repr(tree))
print("- - - - -")
print( tree.pretty() if tree else tree )
print("- - - - -")

