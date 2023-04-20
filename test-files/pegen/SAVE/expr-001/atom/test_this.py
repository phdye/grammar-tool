from parser import create_test_class

from tokens import Name, Number

create_test_class( "atom", [
    ['wonder'       , 'wonder'          , [ Name('wonder') ] ],
    ['hello world'  , 'hello world'     , [ Name('hello'), Name('world') ] ],
    ['Seven'        , '7'               , [ Number('7') ] ],
    ['Seven Eight'  , '7 8'             , [ Number('7'), Number('8') ] ],
    ['123.50'       , '123.50'          , [ Number('123.50') ] ],
] )
