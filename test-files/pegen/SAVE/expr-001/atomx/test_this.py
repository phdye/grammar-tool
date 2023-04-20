from parser import create_test_class

import token
from tokenize import TokenInfo

class TokenInfo_(TokenInfo):
    def __new__(cls, type, string, start=0, end=0, line=''):
        return super().__new__(cls, type, string, start, end, line)
    def __repr__(self):
        return f"TokenInfo_(type={self.type}, string='{self.string}')"

def TokenInfo_eq(self, other):
    return ( isinstance(other, TokenInfo)
             and self.type == other.type
             and self.string == other.string )
TokenInfo.__eq__ = TokenInfo_eq

create_test_class( "atom", [
    ['wonder'       , 'wonder'          , [ TokenInfo_(token.NAME, 'wonder') ] ],
    ['hello world'  , 'hello world'     , [ TokenInfo_(token.NAME, 'hello'),
                                            TokenInfo_(token.NAME, 'world') ] ],
    ['Seven'        , '7'               , [ TokenInfo_(token.NUMBER, '7') ] ],
    ['Seven Eight'  , '7 8'             , [ TokenInfo_(token.NUMBER, '7'),
                                            TokenInfo_(token.NUMBER, '8'), ] ],
    ['123.50'       , '123.50'          , [ TokenInfo_(token.NUMBER, '123.50') ] ],
] )
