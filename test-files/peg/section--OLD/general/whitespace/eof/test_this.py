from parser import create_test_class

create_test_class( "eof", [
    ['empty string', '', 0 ],
    ['1 space', ' ', 0],
    ['3 spaces', '   ', 0],
    ['1 tab', '\t', 0],
    ['3 tabs', '\t', 0],
    ['space tab', ' \t', 0],
    ['some spaces and tabs', ' \t  \t\t ', 0],
    ['carriage-return', '\r', 0],
    ['linefeed', '\n', 0],
    ['a few whitespace lines', ' \t  \n\t\t\n \n', 0],
    ['letter-a', 'a', 1],
    ['colon', ':', 1],
    ['period', '.', 1],
] )
