from parser import create_test_class

create_test_class( "ws", [
    ['space', ' ', 0],
    ['tab', '\t', 0],
    ['carriage-return', '\r', 1],
    ['linefeed', '\n', 1],
] )
