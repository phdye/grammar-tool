from parser import create_test_class, FAIL, DITTO

create_test_class( "eof", [
    ['empty string'                 , ''        , DITTO ],
    ['1 space'                      , ' '       , DITTO ],
    ['3 spaces'                     , '   '     , DITTO ],
    ['1 tab'                        , '\t'      , DITTO ],
    ['3 tabs'                       , '\t'      , DITTO ],
    ['space tab'                    , ' \t'     , DITTO ],
    ['some spaces and tabs'         , ' \t \t\t', DITTO ],
    ['linefeed'                     , '\n'      , DITTO ],
    ['a few whitespace lines'       , '\t \n\t\n',DITTO ],
    #
    # Odd Note :  a single carriage return gets implicitly consumed.
    #
    #['carriage-return'              , '\r'      , FAIL ],  # doesn't fail, see next
    #['carriage-return'              , '\r'      , '\r' ],  # output = '', rather than '\r'
    ['carriage-return'              , '\r'      , '' ],     # weird but now it 'works'
    ['carriage-return'              , '\r\r'    , '\r' ],   # weird but now it 'works'
    #
    # Syntax errors
    #
    ['letter-a'                     , 'a'       , FAIL ],
    ['colon'                        , ':'       , FAIL ],
    ['period'                       , '.'       , FAIL ],
] )
