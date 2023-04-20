from parser import create_test_class

from grammar import ( Tree,
                      Token,
                      UnexpectedCharacters,
                      UnexpectedToken,
                    )

from astpatch import unexpected_eof

unexpected_colon = UnexpectedCharacters(':', 0, 1, 1)

unexpected_plus = UnexpectedToken(Token('Plus', '+'), expected= {'$END'})

create_test_class( "start", [
    [ "add 8 5"               , " 8 + 5",
      Tree(Token('RULE', 'start'),
           [Tree(Token('RULE', 'add'),
                 [Token('SIGNED_NUMBER', '8'),
                  Token('SIGNED_NUMBER', '5')])]) ],
    [ "INDENT add 7 3"        , " 7 + 3",
      Tree(Token('RULE', 'start'),
           [Tree(Token('RULE', 'add'),
                 [Token('SIGNED_NUMBER', '7'),
                  Token('SIGNED_NUMBER', '3')])]) ],
    [ "INDENT add 1.5 1"      , " 1.5 + 1",
      Tree(Token('RULE', 'start'),
           [Tree(Token('RULE', 'add'),
                 [Token('SIGNED_NUMBER', '1.5'),
                  Token('SIGNED_NUMBER', '1')])]) ],
    #
    # Test syntax errors
    #
    ['empty string'             , ''              , unexpected_eof ],
    [ "INDENT add 1 3 5"        , " 1 + 3 + 5"    , unexpected_plus ],
    [ "INDENT add 1 nothing"   , " 1 +"           , unexpected_eof ],
  ],
)
