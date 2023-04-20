from parser import create_test_class

create_test_class( "eof", [
    ['empty string'                 , ''        , '' ],
    ['1 space'                      , ' '       , ' '],
    ['3 spaces'                     , '   '     , '   '],
    ['1 tab'                        , '\t'      , '\t'],
    ['3 tabs'                       , '\t'      , '\t'],
    ['space tab'                    , ' \t'     , ' \t'],
    ['some spaces and tabs'         , ' \t \t\t', ' \t \t\t'],
    ['carriage-return'              , '\r'      , '\r'],
    ['linefeed'                     , '\n'      , '\n'],
    ['a few whitespace lines'       , '\t \n\t\n','\t \n\t\n'],
    #
    # peg implementation does not yet support failure
    #
    #['letter-a'                     , 'a'       , 1],
    #['colon'                        , ':'       , 1],
    #['period'                       , '.'       , 1],
] )
