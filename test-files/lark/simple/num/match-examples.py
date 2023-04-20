#!/usr/bin/env python

import atheris

import sys
sys.path.insert(0, 'work')
# sys.path.insert(0, '.')
# sys.path.insert(0, 'grammar')

from prettyprinter import cpprint as pp

with atheris.instrument_imports():
    import grammar
    from typing import (
        TypeVar, Generic, Type, Tuple, List, Dict, Iterator, Collection, Callable, Optional, FrozenSet, Any,
        Union, Iterable, IO, TYPE_CHECKING, overload,
        Pattern as REPattern, ClassVar, Set, Mapping
    )

T = TypeVar('T')

parser = grammar.Lark_StandAlone()

outer : int = 1
inner : int = 1

def TestMatchExamples(parse_fn: Callable[[str], grammar.Tree],
                      examples: Union[Mapping[T, Iterable[str]], Iterable[Tuple[T, Iterable[str]]]] = {},
                      token_type_match_fallback: bool=False,
                      use_accepts: bool=True
                     ) -> Optional[T] :

    if not len(examples):
        global outer, inner
        if outer % 6000 == 0:
            print('.', end='', flush=True)
            if inner % 87 == 0:
                print(f"  outer = {outer}, inner = {inner}")
                outer = 0
            inner += 1
        outer += 1
        return None
        
    s = grammar.LexerState("help")
    a = grammar.UnexpectedCharacters('now is the time for all good men', 0, 1, 1, state=s)

    try :

        result = a.match_examples(parser.parse, examples, token_type_match_fallback, use_accepts)

        if True :
            print()
            print(f"[Success]")
            pp({ 'parse_fn'						: parse_fn,
                 'examples'						: examples,
                 'token_type_match_fallback'	: token_type_match_fallback,
                 'use_accepts'					: use_accepts,
               } )
            print(f"[-]")
            sys.exit(0)

    except AssertionError:
        if True :
            print()
            print(f"[AssertionError]")
            pp({ 'parse_fn'						: parse_fn,
                 'examples'						: examples,
                 'token_type_match_fallback'	: token_type_match_fallback,
                 'use_accepts'					: use_accepts,
               } )
            print(f"[-]")
        pass

atheris.Setup(sys.argv, TestMatchExamples)
atheris.Fuzz()
