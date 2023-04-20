from parser import create_test_class, FAIL, DITTO, Without

create_test_class( "start", [
    [ "add 8 5"             , "8 + 5"       , Without(' ') ],
    [ "INDENT add 7 3"      , " 7 + 3"      , Without(' ') ],
    [ "INDENT add 1.5 1"    , " 1.5 + 1"    , Without(' ') ],
    #
    # Expected parse failure(s)
    #
    ['a'                    , 'a'           , FAIL ],
    [ "add 1 3 5"           , "1 + 3 + 5"   , FAIL ],
    [ "add 1 nothing"       , "1 +"         , FAIL ],
] )

