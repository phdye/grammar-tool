from parser import create_test_class

from grammar import Tree, Token, UnexpectedToken

from astpatch import unexpected_eof

unexpected_plus = UnexpectedToken(Token('Plus', '+'), expected= {'$END'})

create_test_class( "add", [
    [ 'add 7 3'        , '7 + 3',
      Tree(Token('RULE', 'add'), [Token('SIGNED_NUMBER', '7'), Token('SIGNED_NUMBER', '3')]) ],
    [ "add 1.5 1"      , "1.5 + 1",
      Tree(Token('RULE', 'add'), [Token('SIGNED_NUMBER', '1.5'), Token('SIGNED_NUMBER', '1')]) ],
    #
    # grammar-tool's LARK implementation does not yet support failed tests
    #
    [ "add 1 3 5"      , "1 + 3 + 5"   , unexpected_plus ],
    [ "add 1 nothing"  , "1 +"         , unexpected_eof ],
] )

