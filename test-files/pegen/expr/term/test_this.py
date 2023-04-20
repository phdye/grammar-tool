import ast

from astpatch import Name, Number

from parser import *

create_test_class( "term", [
    [ 'wonder'          , 'wonder'    , [ Name('wonder') ] ],
    [ '123.50'          , '123.50'    , [ Number('123.50') ] ],
    [ 'parenthesis-a'   , '( a )'     , [ Name('a') ] ],
    #
    [ 'two_times_three' , '2 * 3'     , [ ast.BinOp(left=Number('2'),
                                                    op=ast.Mult(),
                                                    right=Number('3') ) ] ],
    #
    [ 'div 7 by 2, mult 3'    , '7 / 2 * 3' , [ ast.BinOp( ast.BinOp(left=Number('7'),
                                                               op=ast.Div(),
                                                               right=Number('2')),
                                                     op=ast.Mult(),
                                                     right=Number('3') ) ] ],
    #
    # Syntax errors
    #
    [ 'colon'           , ':'         , None ],
    [ 'plus'            , '+'         , None ],
    [ 'two mult nil'    , '2 *'       , None ],
    [ 'two div nil'     , '2 /'       , None ],
] )
