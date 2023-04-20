from parser import create_test_class

import os

from token import OP

from parser import create_test_class

from tokens import Line, Word, Number, String

create_test_class( "word", [
    ['wonder'       , 'wonder'          , [ Line([ Word('wonder') ]) ] ],
    ['hello there'  , 'hello there'     , [ Line([ Word('hello'), Word('there') ]) ] ],
    ['Hello Plus'   , 'Hello +'         , [ Line([ Word('Hello'), Word('+') ]) ] ],
    ["one line"
     , "One fine day\n"
     , [ Line([ Word('One'), Word('fine'), Word('day') ]),
         ] ],
    ["two lines"
     , "Hello there\nOne fine day\n"
     , [ Line([ Word('Hello'), Word('there') ]),
         Line([ Word('One'), Word('fine'), Word('day') ]),
         ] ],
] )
