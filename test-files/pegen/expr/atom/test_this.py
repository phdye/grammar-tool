import token

from astpatch import TokenInfo_

from parser import create_test_class

create_test_class( "atom", [
    ['wonder'       , 'wonder'          , [ TokenInfo_(token.NAME, 'wonder') ] ],
    ['hello world'  , 'hello world'     , [ TokenInfo_(token.NAME, 'hello'),
                                            TokenInfo_(token.NAME, 'world') ] ],
    ['Seven'        , '7'               , [ TokenInfo_(token.NUMBER, '7') ] ],
    ['Seven Eight'  , '7 8'             , [ TokenInfo_(token.NUMBER, '7'),
                                            TokenInfo_(token.NUMBER, '8'), ] ],
    ['123.50'       , '123.50'          , [ TokenInfo_(token.NUMBER, '123.50') ] ],
    #
    # Syntax errors
    #
    ['colon'        , ':'               , None ],
    ['plus'         , '+'               , None ],
] )
