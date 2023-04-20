from parser import create_test_class

create_test_class( "adder", [
    [ "add 8 5"               , " 8 + 5"        , '(8 + 5)' ],    # OK
    [ "INDENT add 7 3"        , " 7 + 3"        , '(7 + 3)' ],    # OK
    [ "INDENT add 3 5"        , " 3 + 5"        , '(3 + 5)' ],    # OK
    #
    # grammar-tool's PEG implementation does not yet support failed tests
    #
    #[ "INDENT add 1 3 5"      , " 1 + 3 + 5"    , None ],        # FAIL
    #[ "INDENT add 1 nothing"  , " 1 +"          , None ],        # FAIL
    ],
)
