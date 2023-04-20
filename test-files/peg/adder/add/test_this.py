from parser import create_test_class, FAIL, DITTO, Without

create_test_class( "add", [
    [ 'add 7 3'         , '7 + 3'       , Without(' ') ],
    [ 'add 7 3'         , '7 + 3'       , Without(' ') ],
    [ "add 1.5 1"       , "1.5 + 1"     , Without(' ') ],
    #
    # Parse failure(s)
    #
    ['a'                , 'a'           , FAIL ],
    [ "add 1 3 5"       , "1 + 3 + 5"   , FAIL ],
    [ "add 1 nothing"   , "1 +"         , FAIL ],
] )

