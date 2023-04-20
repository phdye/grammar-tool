from parser import create_test_class

create_test_class( "dc", [
    [ "add 8 5"               , " 8 + 5\n"        , '13' ],    # OK
    [ "INDENT add 7 3"        , " 7 + 3\n"        , '10' ],    # OK
    [ "INDENT multiply 3 5"   , " 3 * 5\n"        , '15' ],    # OK
    #
    # grammar-tool's PEG implementation does not yet support failed tests
    #
    #[ "INDENT add 1 3 5"      , " 1 + 3 + 5\n"    , None ],    # FAIL
    #[ "INDENT add 1 nothing"  , " 1 +\n"          , None ],    # FAIL
  ],
)
