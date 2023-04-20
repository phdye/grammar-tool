from parser import create_test_class

from plumbum.commands import ProcessExecutionError

create_test_class( "num", [
    ['zero'         , '0'           , '(start (num 0))' ],
    ['one'          , '1'           , '(start (num 1))' ],
    ['three'        , '3'           , '(start (num 3))' ],
    ['seven'        , '7'           , '(start (num 7))' ],
    ['15'           , '15'          , '(start (num 15))' ],
    ['123.50'       , '123.50'      , '(start (num 123.50))' ],
    ['0.5'          , '0.5'         , '(start (num 0.5))' ],
    ['1.'           , '1.'          , '(start (num 1.))' ],
    ['.5'           , '.5'          , '(start (num .5))' ],
    #
    # Parse failure(s)
    #
    # ['a'            , 'a'           , ProcessExecutionError([], 1, '','') ],
    ['a'            , 'a'           , '(start (num <missing <INVALID>>))' ],
] )

