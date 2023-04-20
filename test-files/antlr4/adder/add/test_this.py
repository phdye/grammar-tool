from parser import create_test_class

create_test_class( "add", [
    [ 'add 7 3'        , '7 + 3',    '(start (add (num 7) + (num 3)))'],
    [ "add 1.5 1"      , "1.5 + 1",  '(start (add (num 1.5) + (num 1)))'],
    #
    # grammar-tool's LARK implementation does not yet support failed tests
    #
#    [ "add 1 3 5"      , "1 + 3 + 5"   , None ],            # FAIL
#    [ "add 1 nothing"  , "1 +"         , None ],            # FAIL
] )

