from parser import create_test_class

from tokens import Word, Number, String

create_test_class( "word", [
    ['wonder'       , 'wonder'          , [ Word('wonder') ] ],
    ['hello there'  , 'hello there'     , [ Word('hello'), Word('there') ] ],
    ['Hello Plus'   , 'Hello +'         , [ Word('Hello'), Word('+') ] ],
    ['Hello Exclaimation' , 'Hello !'   , [ Word('Hello'), Word(' '), Word('!') ] ],
    ['123.50'       , '123.50'          , [ Number('123.50') ] ],
    ["don't"        , "don't"           , [ Word('don'), Word("'"), Word('t') ] ],
    ["phdye_at_acm" , "phdye@acm"       , [ Word('phdye'), Word('@'), Word('acm') ] ],
    ["quoted string" , 'Hello "test"'   , [ Word('Hello'), String('"test"') ] ],
] )
