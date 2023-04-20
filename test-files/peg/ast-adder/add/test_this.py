from parser import create_test_class

create_test_class( "add", [
    [ 'add 7 3'        , '7 + 3'       , '(7 + 3)'    ],  # OK
    [ "add 3 5"        , "3 + 5"       , '(3 + 5)'  ],  # OK
    #
    # grammar-tool's PEG implementation does not yet support failed tests
    #
    #[ "add 1 3 5"      , "1 + 3 + 5"   , None ],            # FAIL
    #[ "add 1 nothing"  , "1 +"         , None ],            # FAIL
] )

