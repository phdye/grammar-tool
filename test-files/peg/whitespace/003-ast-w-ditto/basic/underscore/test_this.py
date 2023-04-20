from parser import create_test_class, FAIL, DITTO

create_test_class( "underscore", [
    ['empty-string'                 , ''            , DITTO ],
    ['space'                        , ' '           , DITTO ],
    ['tab'                          , '\t'          , DITTO ],
    ['three spaces'                 , '   '         , DITTO ],
    ['three tabs'                   , '\t\t\t'      , DITTO ],
    ['space tab space'              , ' \t '        , DITTO ],
    ['tab space tab'                , '\t \t'       , DITTO ],
    #
    # Syntax errors
    #
    ['"x"'                          , 'x'           , FAIL ],
    # Non-whitespace characters which must fail
    ['" x"'                         , ' x'          , FAIL ],
    ['"x "'                         , 'x '          , FAIL ],
    ['" x "'                        , ' x '         , FAIL ],
    ['space carriage-return space'  , ' \r '        , FAIL ],
    ['space linefeed space'         , ' \n '        , FAIL ],
])
