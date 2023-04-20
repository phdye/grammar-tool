import token

from astpatch import TokenInfo_

from parser import create_test_class

# create_test_class( "atom", [
#     ['wonder'       , 'wonder'          , [ TokenInfo_(token.NAME, 'wonder') ] ],
#    ['hello world'  , 'hello world'     , [ TokenInfo_(token.NAME, 'hello'),
#                                            TokenInfo_(token.NAME, 'world') ] ],
#    ['Seven'        , '7'               , [ TokenInfo_(token.NUMBER, '7') ] ],
#    ['Seven Eight'  , '7 8'             , [ TokenInfo_(token.NUMBER, '7'),
#                                            TokenInfo_(token.NUMBER, '8'), ] ],
#    ['123.50'       , '123.50'          , [ TokenInfo_(token.NUMBER, '123.50') ] ],
# ] )

from prettyprinter import pprint as pp
from pathlib import Path

from pegen.grammar_parser import GeneratedParser as GrammarParser
from pegen.utils import generate_parser, make_parser, parse_string

from pegen.grammar import Rule, NamedItem, NameLeaf, StringLeaf
from pegen.grammar import Repeat0   # '*' : Zero or more, Kleene star
from pegen.grammar import Repeat1   # '+' : One or more
from pegen.grammar import Alt       # '|' : OR, alternative
from pegen.grammar import Opt       # '?' : optional
from pegen.grammar import Rhs       # right hand side for Rule

def SKIP_test_grammar_show_rules() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)
    pp(grammar.rules)
        
def test_rule_structure_atom() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)
    expected = Rule('atom', None,
                    Rhs([Alt([NamedItem('a', NameLeaf('NAME'))],
                             action='a'),
                         Alt([NamedItem('a', NameLeaf('NUMBER'))],
                             action='a')]))    
    assert repr(grammar.rules[expected.name]) == repr(expected)
    
        
def test_rule_structure_factor() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)
    expected = Rule('factor', None,
                    Rhs([Alt([NamedItem(None, StringLeaf("'('")),
                              NamedItem('e', NameLeaf('expr')),
                              NamedItem(None, StringLeaf("')'"))],
                             action='e'),
                         Alt([NamedItem(None, NameLeaf('atom'))], action='atom')]))
    assert repr(grammar.rules[expected.name]) == repr(expected)
    
        
def test_rule_structure_term() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)
    expected = Rule('term', None,
                    Rhs([Alt([NamedItem('l', NameLeaf('term')),
                              NamedItem(None, StringLeaf("'*'")),
                              NamedItem('r', NameLeaf('factor'))],
                             action=('ast . BinOp ( left = l , '
                                     'op = ast . Mult ( ) , '
                                     'right = r , LOCATIONS )')),
                         Alt([NamedItem('l', NameLeaf('term')),
                              NamedItem(None, StringLeaf("'/'")),
                              NamedItem('r', NameLeaf('factor'))],
                             action=('ast . BinOp ( left = l , '
                                     'op = ast . Div ( ) , '
                                     'right = r , LOCATIONS )')),
                         Alt([NamedItem(None, NameLeaf('factor'))])]))
    
    assert repr(grammar.rules[expected.name]) == repr(expected)
    
        
def test_rule_structure_expr() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)
    expected = Rule('expr', None,
                    Rhs([Alt([NamedItem('l', NameLeaf('expr')),
                              NamedItem(None, StringLeaf("'+'")),
                              NamedItem('r', NameLeaf('term'))],
                             action=('ast . BinOp ( left = l , '
                                     'op = ast . Add ( ) , '
                                     'right = r , LOCATIONS )')),
                         Alt([NamedItem('l', NameLeaf('expr')),
                              NamedItem(None, StringLeaf("'-'")),
                              NamedItem('r', NameLeaf('term'))],
                             action=('ast . BinOp ( left = l , '
                                     'op = ast . Sub ( ) , '
                                     'right = r , LOCATIONS )')),
                         Alt([NamedItem(None, NameLeaf('term'))])]))
    assert repr(grammar.rules[expected.name]) == repr(expected)
    
        
def test_rule_structure_stmt() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)
    expected = Rule('stmt', None,
                    Rhs([Alt([NamedItem('a', NameLeaf('expr')),
                              NamedItem(None, NameLeaf('NEWLINE'))],
                             action='ast . Expr ( value = a , LOCATIONS )'),
                         Alt([NamedItem('a', NameLeaf('expr')),
                              NamedItem(None, NameLeaf('ENDMARKER'))],
                             action='ast . Expr ( value = a , LOCATIONS )')]))
    assert repr(grammar.rules[expected.name]) == repr(expected)
    
        
def test_rule_structure_start() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)
    expected = Rule('start', 'ast . Module',
                    Rhs([Alt([NamedItem('a', Repeat0(NameLeaf('stmt'))),
                              NamedItem(None, NameLeaf('ENDMARKER'))],
                             action='ast . Module ( body = a or [] )')]))
    assert repr(grammar.rules[expected.name]) == repr(expected)
    
        
def test_atom_42_newline() -> None:
    grammar_source = Path("grammar.gram").read_text()
    grammar = parse_string(grammar_source, GrammarParser)

    rule_name = 'atom'
    grammar.rules['start'] = Rule('start', None,
                                  Rhs([Alt([NamedItem('a',Repeat1(NameLeaf(rule_name))),
                                            NamedItem(None, Opt(NameLeaf('NEWLINE'))),
                                            NamedItem(None, NameLeaf('ENDMARKER'))],
                                           action='a')]))

    parser_class = generate_parser(grammar)
    n = 42
    node = parse_string(f"{n}\n", parser_class)
    # pp(node)
    assert node == [ TokenInfo_(token.NUMBER, f'{n}') ]

