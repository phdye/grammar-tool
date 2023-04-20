# Additional syntax is required to distinguish between 'underscore' and 'ws'
# since 'underscore' is zero or more 'ws'.  Hence, '<rule> :<value>:'.

from parser import create_test_class, FAIL, DITTO

create_test_class( "underscore", [
    ['_ empty-string'                 , '_ ::'            , DITTO ],
    ['_ space'                        , '_ : :'           , DITTO ],
    ['_ tab'                          , '_ :\t:'          , DITTO ],
    ['_ three spaces'                 , '_ :   :'         , DITTO ],
    ['_ three tabs'                   , '_ :\t\t\t:'      , DITTO ],
    ['_ space tab space'              , '_ :\t :'         , DITTO ],
    ['_ tab space tab'                , '_ :\t \t:'       , DITTO ],
    #
    # Syntax errors
    #
    ['_ x'                            , '_ :x:'           , FAIL ],
    ['_ space carriage-return space'  , '_ : \r :'        , FAIL ],
    ['_ space linefeed space'         , '_ : \n :'        , FAIL ],
])

create_test_class( "ws", [
    ['ws space'                       , 'ws : :'   , DITTO ],
    ['ws tab'                         , 'ws :\t:'  , DITTO ],
    ['ws carriage-return'             , 'ws :\r:'  , FAIL ],
    ['ws linefeed'                    , 'ws :\n:'  , FAIL ],
] )
