from parser import create_test_class

create_test_class( "eol", [
    ['linefeed', '\n', 0],
    ['carriage-return', '\r', 0],
    ['cr linefeed', '\r\n', 0],
    [' ', ' ', 1],
    ['tab', '\t', 1],
] )
