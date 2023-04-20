# @parameterize used by parser_create_class() uses requires the repr() and the
# parser test function requires eq() working without regard to location details.

from grammar import ( Lark_StandAlone,
                      Token, Tree,
                      UnexpectedCharacters,
                      UnexpectedToken,
                      ParserState,
                      ParseConf,
                      LexerThread,
                    )

import ast

AST_ROOTS = ( ast.AST, Tree, Token, list, type(None) )

unexpected_eof = UnexpectedToken(Token('$END', ''), expected= {})

# UnexpectedCharacters's original __repr__ is merely 'UnexpectedCharacters()'
# which fails with TypeError executing the generated paremeterization code.
# >>> TypeError: UnexpectedCharacters.__init__() missing 4 required
# >>> positional arguments: 'seq', 'lex_pos', 'line', and 'column'

def UnexpectedCharacters_repr(self):
    return ( f"UnexpectedCharacters(seq = {repr(self.char)}, "
                                  f"lex_pos = {self.pos_in_stream}, "
                                  f"line = {self.line}, "
                                  f"column = {self.column}, "
                                  f"allowed = {repr(self.allowed)}, "
                                  f"considered_tokens = {repr(self.considered_tokens)}, "
                                  f"state = {repr(self.state)}, "
                                  f"token_history = {repr(self.token_history)}, "
                                  f"terminals_by_name = {repr(self._terminals_by_name)}, "
                                  f"considered_rules = {repr(self.considered_rules)})" )
UnexpectedCharacters.__repr__ = UnexpectedCharacters_repr

def UnexpectedToken_repr(self):
    return ( f"UnexpectedToken("
             f"{repr(self.token)}, "
             f"{repr(self.expected)} )" )
UnexpectedToken.__repr__ = UnexpectedToken_repr

def ParserState_repr(self):
    return ( f"ParserState(parse_conf={repr(self.parse_conf)}, "
             f"lexer={repr(self.lexer)}, "
             f"state_stack={repr(self.state_stack)}, "
             f"value_stack={repr(self.value_stack)} )" )
ParserState.__repr__ = ParserState_repr

def ParseConf_repr(self):
    return ( f"ParseConf(parse_table={repr(self.parse_table)}, "
             f"parse_table={repr(self.parse_table)}, "
             f"callbacks={repr(self.callbacks)}, "
             f"start={repr(self.start)}, "
             f"start_state={repr(self.start_state)}, "
             f"end_state={repr(self.end_state)}, "
             f"states={repr(self.states)} )" )
ParseConf.__repr__ = ParseConf_repr

