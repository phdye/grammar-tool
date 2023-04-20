from parser import create_test_class, FAIL, DITTO

create_test_class( "ws", [
    ['space'            , ' '   , DITTO ],
    ['tab'              , '\t'  , DITTO ],
    ['carriage-return'  , '\r'  , FAIL ],
    ['linefeed'         , '\n'  , FAIL ],
] )
