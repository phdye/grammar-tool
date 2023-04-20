from parser import create_test_class

create_test_class( "wx", [
    ['letter-a'			, 'a', 0],
    ['colon'			, ':', 0],
    ['space'			, ' ', 1],
    ['tab'				, '\t', 1],
    ['carriage-return'	, '\r', 1],
    ['linefeed'			, '\n', 1],
] )
