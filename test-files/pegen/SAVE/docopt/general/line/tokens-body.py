from dataclasses import dataclass

import ast

from tokenize import TokenInfo

@dataclass
class Line(ast.AST):

    value : list
    token : TokenInfo = None   # probably always None

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value
    
