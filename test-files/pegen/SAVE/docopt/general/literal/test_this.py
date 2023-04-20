import os

print(f"\nPYTHONPATH = '{os.environ['PYTHONPATH']}'\n", flush=True)

from tokenize import TokenError

from parser import create_test_class

from tokens import Literal, Comment

from grammar import Other

create_test_class( "literal", [
    # Parenthesis and brackets must be paired of the Tokenizer fails
    # with 'EOF in multi-line statement'.
    #
    [ 'left-bracket'            , '['   , TokenError("EOF in multi-line statement") ],
    #
    #
    [ 'hello there', 'hello there', [ Other('hello'), Other('there') ] ],
    #
    [ 'TIDLE'                   , '~'   , [ Literal('~') ] ],
    [ 'BACKTICK'                , '`'   , [ Literal('`') ] ],
    [ 'AT'                      , '@'   , [ Literal('@') ] ],
    [ 'HASH'                    , '#'   , [ Comment('#') ] ],
    #['HASH space'              , '# '  , [ Comment('# ')  ] ], # Filtered to NAME in pegen/tests/parser.py
    #['HASH space period'       , '# .' , [ Comment('# .') ] ], # but CommentTokenInfo, then Comment
    [ 'DOLLAR'                  , '$'   , [ Literal('$') ] ],
    [ 'PERCENT'                 , '%'   , [ Literal('%') ] ],
    [ 'CARET'                   , '^'   , [ Literal('^') ] ],
    [ 'AMPERSAND'               , '&'   , [ Literal('&') ] ],
    [ 'ASTERIX'                 , '*'   , [ Literal('*') ] ],
    #[ 'LEFT_PARENTHESIS'       , '('   , [ Literal('(') ] ],
    #[ 'RIGHT_PARENTHESIS'      , ')'   , [ Literal(')') ] ],
    [ 'left, right parenthesis' , '()'  , [ Literal('('), Literal(')') ] ],
    [ 'UNDERSCORE'              , '_'   , [ Literal('_') ] ],
    [ 'MINUS'                   , '-'   , [ Literal('-') ] ],
    [ 'PLUS'                    , '+'   , [ Literal('+') ] ],
    [ 'EQUAL'                   , '='   , [ Literal('=') ] ],
    #[ 'LEFT_CURLY_BRACE'       , '{'   , [ Literal('{') ] ],
    #[ 'RIGHT_CURLY_BRACE'      , '}'   , [ Literal('}') ] ],
    [ 'left, right curty brace'  , '{}'  , [ Literal('{'), Literal('}') ] ],
    #[ 'LEFT_SQAURE_BRACKET'    , '['   , [ Literal('[') ] ],
    #[ 'RIGHT_SQAURE_BRACKET'   , ']'   , [ Literal(']') ] ],
    [ 'left, right square brackets', '[]'    , [ Literal('['), Literal(']') ] ],
    [ 'BAR'                     , '|'   , [ Literal('|') ] ],
    [ 'BACKSLASH'               , '\\'  , [ Literal('\\') ] ],
    [ 'COLON'                   , ':'   , [ Literal(':') ] ],
    [ 'SEMICOLON'               , ';'   , [ Literal(';') ] ],
    [ 'DOUBLE_QUOTE'            , '"'   , [ Literal('"') ] ],
    [ 'SINGLE_QUOTE'            , "'"   , [ Literal("'") ] ],
    #[ 'LEFT_ANGLE_BRACKET'     , '<'   , [ Literal('<') ] ],
    #[ 'RIGHT_ANGLE_BRACKET'    , '>'   , [ Literal('>') ] ],
    [ 'left, right angle brackets', '<>' , [ Literal('<'), Literal('>') ] ],
    [ 'COMMA'                   , ','   , [ Literal(',') ] ],
    [ 'PERIOD'                  , '.'   , [ Literal('.') ] ],
    [ 'QUESTION_MARK'           , '?'   , [ Literal('?') ] ],
    [ 'FORWARD_SLASH'           , '/'   , [ Literal('/') ] ],
    #
    [ 'Letter-a'                  , 'a'   , [ Other('a') ] ],
] )
