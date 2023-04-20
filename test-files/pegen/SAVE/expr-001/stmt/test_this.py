from parser import parser_create_class

from tokens import Name, Number

import ast

#------------------------------------------------------------------------------

# @parameterize used by parser_create_class() uses requires the repr() and the
# parser test function requires eq() working without regard to tokeninfo.

def ast_Expr_repr(self):
    return f"ast.Expr()"
ast.Expr.__repr__ = ast_Expr_repr

def ast_Expr_eq(self, other):
    return isinstance(other, ast.Expr)
ast.Expr.__eq__ = ast_Expr_eq

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

def ast_Add_repr(self):
    return f"ast.Add()"
ast.Add.__repr__ = ast_Add_repr

def ast_Add_eq(self, other):
    return isinstance(other, ast.Add)
ast.Add.__eq__ = ast_Add_eq

def ast_Sub_repr(self):
    return f"ast.Sub()"
ast.Sub.__repr__ = ast_Sub_repr

def ast_Sub_eq(self, other):
    return isinstance(other, ast.Sub)
ast.Sub.__eq__ = ast_Sub_eq

#------------------------------------------------------------------------------

parser_create_class( "atom", [
    [ 'wonder'          , 'wonder'    , [ ast.Expr(value=Name('wonder')) ] ],
    [ '123.50'          , '123.50'    , [ ast.Expr(value=Number('123.50')) ] ],
    [ 'parenthesis-a'   , '( a )'     , [ ast.Expr(value=Name('a')) ] ],
    #
    [ 'two_times_three' , '2 * 3'     , [ ast.Expr(value=
                                                   ast.BinOp(
                                                       left=Number('2'),
                                                       op=ast.Mult(),
                                                       right=Number('3') )) ] ],
    #
    [ '7 plus 2 mult 3' , '7 + 2 * 3' , [ ast.Expr(value=
                                                   ast.BinOp(
                                                       left=Number('7'),
                                                       op=ast.Add(),
                                                       right=ast.BinOp(
                                                           left=Number('2'),
                                                           op=ast.Mult(),
                                                           right=Number('3')
                                                       ))) ] ],
] )
