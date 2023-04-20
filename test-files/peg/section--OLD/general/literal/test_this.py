from parser import create_test_class

# # General Utility
# # ---------------
# 
# OR <- _ [Oo][Rr] ( ':' / &ws )
# 
# LBRACKET <- _ '['
# RBRACKET <- _ ']'
# LPAREN <- _ '('
# RPAREN <- _ ')'
# BAR <- _ '|'
# COMMA <- _ ','

create_test_class( "or", [
    ['or colon'				, 'or:', 0 ],
    ['Or colon'				, 'Or:', 0 ],
    ['oR colon'				, 'oR:', 0 ],
    ['OR colon'				, 'OR:', 0 ],
    ['or space'				, 'or ', 0 ],
    ['or eof'				, 'or', 1 ],
] )

create_test_class( "literals", [
    ['left_bracket'			, '[', 0],
#    ['right_bracket'		, ']', 0],
#    ['left_paren'			, '(', 0],
#    ['right_paren'			, ')', 0],
#    ['vertical_bar'			, '|', 0],
#    ['comma'				, ',', 0],
] )
