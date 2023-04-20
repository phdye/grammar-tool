import ast

from parser import parser_create_class

from astpatch import module_, expr_, mod_expr, Name, Number

#------------------------------------------------------------------------------
    
parser_create_class( "atom", [
    [ 'wonder'          , 'wonder'    , mod_expr(Name('wonder')) ],
    [ '123.50'          , '123.50'    , mod_expr(Number('123.50')) ],
    [ 'parenthesis-a'   , '( a )'     , mod_expr(Name('a')) ],
    #
    [ 'two_times_three' , '2 * 3'     , mod_expr(ast.BinOp(
                                                       left=Number('2'),
                                                       op=ast.Mult(),
                                                       right=Number('3') )) ],
    #
    [ '7 plus 2 mult 3' , '7 + 2 * 3' , mod_expr(ast.BinOp(
                                                       left=Number('7'),
                                                       op=ast.Add(),
                                                       right=ast.BinOp(
                                                           left=Number('2'),
                                                           op=ast.Mult(),
                                                           right=Number('3')
                                                       ))) ],
    #
    [ 'two stmts, integers' , "3\n7"  , module_( [ expr_(Number('3')),
                                                   expr_(Number('7')) ] ) ],
    #
    [ 'two stmts, mult, add' , "2 * 3\n7 + 2",
      module_( [
          expr_(ast.BinOp(left=Number('2'),
                          op=ast.Mult(),
                          right=Number('3') )),
          expr_(ast.BinOp(left=Number('7'),
                          op=ast.Add(),
                          right=Number('2') )),
      ] ) ],
] )

