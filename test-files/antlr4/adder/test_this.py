from parser import create_test_class

create_test_class( "start", [
    [ "add 8 5"               , " 8 + 5",
      '(start (add (num 8) + (num 5)))' ],
    [ "INDENT add 7 3"        , " 7 + 3",
      '(start (add (num 7) + (num 3)))' ],
    [ "INDENT add 1.5 1"      , " 1.5 + 1",
      '(start (add (num 1.5) + (num 1)))' ],
    #
    # grammar-tool's PEG implementation does not yet support FAIL
    #
#    [ "INDENT add 1 3 5"      , " 1 + 3 + 5"    , None ],        # FAIL
#    [ "INDENT add 1 nothing"  , " 1 +"          , None ],        # FAIL
  ],
)
