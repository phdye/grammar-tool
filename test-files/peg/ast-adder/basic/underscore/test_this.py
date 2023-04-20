from parser import create_test_class

create_test_class( "underscore", [
    ['empty-string'                 , ''            , '' ],
    ['space'                        , ' '           , ' ' ],
    ['tab'                          , '\t'          , '\t' ],
    ['three spaces'                 , '   '         , '   ' ],
    ['three tabs'                   , '\t\t\t'      , '\t\t\t' ],
    ['space tab space'              , ' \t '        , ' \t ' ],
    ['tab space tab'                , '\t \t'       , '\t \t' ],
    #
    # grammar-tool's PEG implementation does not yet support FAIL
    #
    #['"x"'                          , 'x'           , 1],
    ## Non-whitespace characters which must fail
    #['" x"'                         , ' x'          , 1],
    #['"x "'                         , 'x '          , 1],
    #['" x "'                        , ' x '         , 1],
    #['space carriage-return space'  , ' \r '        , 1],
    #['space linefeed space'         , ' \n '        , 1],
])
