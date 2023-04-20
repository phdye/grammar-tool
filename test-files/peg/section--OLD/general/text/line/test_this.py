from parser import create_test_class

create_test_class( "line", [
    ['a'				, 'a', 0],
    ['a b c'			, 'a b c', 0],
    ['a b c<nl>'		, 'a b c\n', 0],
    ['hello there'		, 'hello there', 0],
    ['hello there<nl>'	, 'hello there\n', 0],
    ['space'			, '\t', 1],
    ['tab'				, '\t', 1],
    ['carriage-return'	, '\r', 1],
    ['linefeed'			, '\n', 1],
] )
