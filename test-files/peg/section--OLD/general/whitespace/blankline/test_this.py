from parser import create_test_class

create_test_class( "blankline", [
    ['nl nl', '\n\n', 0],
    ['nl spc nl', '\n \n', 0],
    ['nl spc tab spc nl', '\n \t \n', 0],
    ['nl spc cr nl', '\n \r\n', 0],
    ['nl a spc nl', '\na \n', 1],
] )
