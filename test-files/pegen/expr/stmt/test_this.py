import ast

from astpatch import module_, expr_, mod_expr, Name, Number

from parser import *

#------------------------------------------------------------------------------

create_test_class( "stmt", [
    [ 'wonder'          , 'wonder'    , [ ast.Expr(value=Name('wonder')) ] ],
    [ '123.50'          , '123.50'    , [ ast.Expr(value=Number('123.50')) ] ],
    [ 'parenthesis-a'   , '( a )'     , [ ast.Expr(value=Name('a')) ] ],
    #
    [ 'two_times_three' , '2 * 3'     , [ ast.Expr(value=
                                                   ast.BinOp(
                                                       left=Number('2'),
                                                       op=ast.Mult(),
                                                       right=Number('3') )) ] ],
    #
    [ '7 plus 2 mult 3' , '7 + 2 * 3' , [ ast.Expr(value=
                                                   ast.BinOp(
                                                       left=Number('7'),
                                                       op=ast.Add(),
                                                       right=ast.BinOp(
                                                           left=Number('2'),
                                                           op=ast.Mult(),
                                                           right=Number('3')
                                                       ))) ] ],
    #
    # Syntax errors
    #
    [ 'colon'           , ':'         , None ],
    [ 'plus'            , '+'         , None ],
    [ 'two mult nil'    , '2 *'       , None ],
    [ 'two div nil'     , '2 /'       , None ],
    [ 'two plus nil'    , '2 +'       , None ],
    [ 'two minus nil'   , '2 -'       , None ],
] )
