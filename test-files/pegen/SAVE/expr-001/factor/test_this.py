from parser import parser_create_class

from tokens import Name, Number

parser_create_class( "atom", [
    ['wonder'       , 'wonder'          , [ Name('wonder') ] ],
    ['123.50'       , '123.50'          , [ Number('123.50') ] ],
    ['parenthesis-a', '( a )'           , [ Name('a') ] ],
] )

