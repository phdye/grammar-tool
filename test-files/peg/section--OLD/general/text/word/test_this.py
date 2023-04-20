from parser import create_test_class

create_test_class( "word", [
    ['letter-a'			, 'a', 0],
    ['hello'			, 'hello', 0],
    ['<space>hello'		, ' hello', 0],
    ['[program]'		, '[program]', 0],
    ['<space><tab>a'	, ' \ta', 0],
    ['space'			, '\t', 1],
    ['tab'				, '\t', 1],
    ['carriage-return'	, '\r', 1],
    ['linefeed'			, '\n', 1],
] )
