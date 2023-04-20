from parser import create_test_class

create_test_class( "start", [
    [ "add 8 5"               , " 8 + 5"        , [ 8, 5 ] ],    # OK
    [ "INDENT add 7 3"        , " 7 + 3"        , [ 7, 3 ] ],    # OK
    [ "INDENT add 1.5 1"      , " 1.5 + 1"      , [ 1.5, 1 ] ],  # OK
    [ "INDENT add 1 3 5"      , " 1 + 3 + 5"    , None ],        # FAIL
    [ "INDENT add 1 nothing"  , " 1 +"          , None ],        # FAIL
  ],
)
