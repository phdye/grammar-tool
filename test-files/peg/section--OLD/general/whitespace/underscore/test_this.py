from parser import create_test_class

create_test_class( "underscore", [
    ['empty-string', '', 0],
    ['space', ' ', 0],
    ['tab', '\t', 0],
    ['three spaces', '   ', 0],
    ['three tabs', '\t\t\t', 0],
    ['space tab space', ' \t ', 0],
    ['tab space tab', '\t \t', 0],
    ['"x"', 'x', 1],
    # Non-whitespace characters which must fail
    ['" x"', ' x', 1],
    ['"x "', 'x ', 1],
    ['" x "', ' x ', 1],
    ['space carriage-return space', ' \r ', 1],
    ['space linefeed space', ' \n ', 1],
    # # Force uncaught exception
    # ['"x"', 'x', 0],
])
