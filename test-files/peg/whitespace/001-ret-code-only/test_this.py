from parser import create_test_class

# terminate.peg
#   START <- ( wsx / _x )* eof
#   wsx  <- ws ':'
#   _x   <- _ ':'

create_test_class( "eof", [
    ['empty string'			, '', 0 ],
    ['one space'			, ' ', 0],
    ['three spaces'			, '   ', 0],
    ['one tab'				, '\t', 0],
    ['three tabs'			, '\t', 0],
    ['space tab'			, ' \t', 0],
    ['some spaces and tabs'	, ' \t  \t\t ', 0],
    ['carriage-return'		, '\r', 0],
    ['linefeed'				, '\n', 0],
    ['whitespace lines'		, ' \t  \n\t\t\n \n', 0],
    ['letter-a'				, 'a', 1],
    # ['colon'				, ':', 1], # matches 'wsx'
    ['period'				, '.', 1],
] )

create_test_class( "ws", [
    ['space'				, ' '	+':', 0],
    ['tab'					, '\t'	+':', 0],
    ['carriage-return'		, '\r'	+':', 1],
    ['linefeed'				, '\n'	+':', 1],
] )

create_test_class( "underscore", [
    ['empty-string'			, ''		+':', 0],
    ['space'				, ' '		+':', 0],
    ['tab'					, '\t'		+':', 0],
    ['three spaces'			, '   '		+':', 0],
    ['three tabs'			, '\t\t\t'	+':', 0],
    ['space tab space'		, ' \t '	+':', 0],
    ['tab space tab'		, '\t \t'	+':', 0],
    ['"x"'					, 'x'		+':', 1],
    # Non-whitespace characters which must fail
    ['" x"'					, ' x'		+':', 1],
    ['"x "'					, 'x '		+':', 1],
    ['" x "'				, ' x '		+':', 1],
    ['space CR space'		, ' \r '	+':', 1],
    ['space linefeed space'	, ' \n '	+':', 1],
])

create_test_class( "combinations", [
    ['wsx, _x, eof'			, ' :\n ', 0],
    ['_x, eof'				, '   :\n ', 0],
    ['wsx, _x, eof'			, ' :   :\n ', 0],
    ['newline, wsx'			, '\n :'	, 1],
])
