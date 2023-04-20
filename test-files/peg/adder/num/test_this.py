from parser import create_test_class, FAIL, DITTO

create_test_class( "num", [
    ['zero'         , '0'           , DITTO ],
    ['one'          , '1'           , DITTO ],
    ['three'        , '3'           , DITTO ],
    ['seven'        , '7'           , DITTO ],
    ['15'           , '15'          , DITTO ],
    ['123.50'       , '123.50'      , DITTO ],
    #
    # Parse failure(s)
    #
    ['a'            , 'a'           , FAIL ],
    ['+'            , '+'           , FAIL ],
    [':'            , ':'           , FAIL ],
] )

