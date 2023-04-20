from parser import create_test_class

create_test_class( "num", [
    ['zero'         , '0'           , '0' ],            # OK  *** pegen BUG
    ['one'          , '1'           , '1' ],            # OK
    ['three'        , '3'           , '3' ],            # OK
    ['seven'        , '7'           , '7' ],            # OK
    ['15'           , '15'          , '15' ],           # OK
#    ['123.50'       , '123.50'      , '123.50' ],       # OK  -- not supported with AST
#    ['a'            , 'a'           , '' ],             # FAIL
] )

