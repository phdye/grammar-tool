from parser import parser_create_class

from tokens import Name, Number

import ast

#------------------------------------------------------------------------------

def ast_BinOp_repr(self):
    return f"ast.BinOp(left={repr(self.left)}, op={repr(self.op)}, right={repr(self.right)})"
ast.BinOp.__repr__ = ast_BinOp_repr

def ast_BinOp_eq(self, other):
    return ( isinstance(other, ast.BinOp)
             and self.left == other.left
             # and self.op == other.op
             and self.right == other.right )
ast.BinOp.__eq__ = ast_BinOp_eq

def ast_Mult_repr(self):
    return f"ast.Mult()"
ast.Mult.__repr__ = ast_Mult_repr

def ast_Mult_eq(self, other):
    return isinstance(other, ast.Mult)
ast.Mult.__eq__ = ast_Mult_eq

def ast_Div_repr(self):
    return f"ast.Div()"
ast.Div.__repr__ = ast_Div_repr

def ast_Div_eq(self, other):
    return isinstance(other, ast.Div)
ast.Div.__eq__ = ast_Div_eq

#------------------------------------------------------------------------------

parser_create_class( "atom", [
    [ 'wonder'          , 'wonder'    , [ Name('wonder') ] ],
    [ '123.50'          , '123.50'    , [ Number('123.50') ] ],
    [ 'parenthesis-a'   , '( a )'     , [ Name('a') ] ],
    #
    [ 'two_times_three' , '2 * 3'     , [ ast.BinOp(left=Number('2'),
                                                    op=ast.Mult(),
                                                    right=Number('3') ) ] ],
    #
    [ 'div 7 by 2, mult 3'    , '7 / 2 * 3' , [ ast.BinOp( ast.BinOp(left=Number('7'),
                                                               op=ast.Div(),
                                                               right=Number('2')),
                                                     op=ast.Mult(),
                                                     right=Number('3') ) ] ],
] )
