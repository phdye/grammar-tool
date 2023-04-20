import token

from astpatch import TokenInfo_, Name, Number

from parser import *

create_test_class( "factor", [
    ['wonder'       , 'wonder'          , [ TokenInfo_(type=token.NAME, string='wonder') ] ],
    ['123.50'       , '123.50'          , [ TokenInfo_(type=token.NUMBER, string='123.50') ] ],
    #
    ['wonder'       , 'wonder'          , [ Name('wonder') ] ],
    ['123.50'       , '123.50'          , [ Number('123.50') ] ],
    ['parenthesis-a', '( a )'           , [ Name('a') ] ],
    #
    # Syntax errors
    #
    ['colon'        , ':'               , None ],
] )

