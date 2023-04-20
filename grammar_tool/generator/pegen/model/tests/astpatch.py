import ast

import token

from tokenize import TokenInfo

AST_ROOTS = ( ast.AST, TokenInfo, list, type(None) )

# @parameterize used by parser_create_class() uses requires the repr() and the
# parser test function requires eq() working without regard to location details.

def ast_Module_repr(self):
    return f"ast.Module({repr(self.body)})"
ast.Module.__repr__ = ast_Module_repr

def ast_Module_eq(self, other):
    return isinstance(other, ast.Module) and self.body == other.body
ast.Module.__eq__ = ast_Module_eq

def ast_Expr_repr(self):
    return f"ast.Expr({repr(self.value)})"
ast.Expr.__repr__ = ast_Expr_repr

def ast_Expr_eq(self, other):
    return isinstance(other, ast.Expr) and self.value == other.value
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

def TokenInfo_eq(self, other):
    return ( isinstance(other, TokenInfo)
             and self.type == other.type
             and self.string == other.string )
TokenInfo.__eq__ = TokenInfo_eq

#------------------------------------------------------------------------------

def module_(x):
    return ast.Module(body=x)

def expr_(stmt):
    return ast.Expr(value=stmt)

def mod_expr(stmt):
    return module_( [ expr_( stmt ) ] )

#------------------------------------------------------------------------------

class TokenInfo_(TokenInfo):
    def __new__(cls, type, string, start=0, end=0, line=''):
        return super().__new__(cls, type, string, start, end, line)
    def __repr__(self):
        return f"TokenInfo_(type={self.type}, string='{self.string}')"

#------------------------------------------------------------------------------

class Number(TokenInfo_):
    def __new__(cls, string, start=0, end=0, line=''):
        return super().__new__(cls, token.NUMBER, string, start, end, line)
    def __repr__(self):
        return f"Number('{self.string}')"

from prettyprinter import pprint as pp

class Name(TokenInfo_):
    def __new__(cls, string, start=0, end=0, line=''): # , tag=''):
        # print() ; pp(tag+string)
        return super().__new__(cls, token.NAME, string, start, end, line)
    def __repr__(self):
        return f"Name('{self.string}')"
    
class String(TokenInfo_):
    def __new__(cls, string, start=0, end=0, line=''):
        return super().__new__(cls, token.STRING, string, start, end, line)
    def __repr__(self):
        return f"String('{self.string}')"
    
#------------------------------------------------------------------------------
