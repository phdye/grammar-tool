#!/usr/bin/env python3.8
# @generated by pegen from grammar.gram

import ast
import sys
import tokenize

from typing import Any, Optional

from pegen.parser import memoize, memoize_left_rec, logger, Parser
# Keywords and soft keywords are listed at the end of the parser definition.
class GeneratedParser(Parser):

    @memoize
    def start(self) -> Optional[ast . Module]:
        # start: stmt* $
        mark = self._mark()
        if (
            (a := self._loop0_1(),)
            and
            (self.expect('ENDMARKER'))
        ):
            return ast . Module ( body = a or [] );
        self._reset(mark)
        return None;

    @memoize
    def stmt(self) -> Optional[Any]:
        # stmt: expr NEWLINE | expr $
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.expr())
            and
            (self.expect('NEWLINE'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Expr ( value = a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset );
        self._reset(mark)
        if (
            (a := self.expr())
            and
            (self.expect('ENDMARKER'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Expr ( value = a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset );
        self._reset(mark)
        return None;

    @memoize_left_rec
    def expr(self) -> Optional[Any]:
        # expr: expr '+' term | expr '-' term | term
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (l := self.expr())
            and
            (self.expect('+'))
            and
            (r := self.term())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( left = l , op = ast . Add ( ) , right = r , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset );
        self._reset(mark)
        if (
            (l := self.expr())
            and
            (self.expect('-'))
            and
            (r := self.term())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( left = l , op = ast . Sub ( ) , right = r , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset );
        self._reset(mark)
        if (
            (term := self.term())
        ):
            return term;
        self._reset(mark)
        return None;

    @memoize_left_rec
    def term(self) -> Optional[Any]:
        # term: term '*' factor | term '/' factor | factor
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (l := self.term())
            and
            (self.expect('*'))
            and
            (r := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( left = l , op = ast . Mult ( ) , right = r , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset );
        self._reset(mark)
        if (
            (l := self.term())
            and
            (self.expect('/'))
            and
            (r := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( left = l , op = ast . Div ( ) , right = r , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset );
        self._reset(mark)
        if (
            (factor := self.factor())
        ):
            return factor;
        self._reset(mark)
        return None;

    @memoize
    def factor(self) -> Optional[Any]:
        # factor: '(' expr ')' | atom
        mark = self._mark()
        if (
            (self.expect('('))
            and
            (e := self.expr())
            and
            (self.expect(')'))
        ):
            return e;
        self._reset(mark)
        if (
            (atom := self.atom())
        ):
            return atom;
        self._reset(mark)
        return None;

    @memoize
    def atom(self) -> Optional[Any]:
        # atom: NAME | NUMBER
        mark = self._mark()
        if (
            (a := self.name())
        ):
            return a;
        self._reset(mark)
        if (
            (a := self.number())
        ):
            return a;
        self._reset(mark)
        return None;

    @memoize
    def _loop0_1(self) -> Optional[Any]:
        # _loop0_1: stmt
        mark = self._mark()
        children = []
        while (
            (stmt := self.stmt())
        ):
            children.append(stmt)
            mark = self._mark()
        self._reset(mark)
        return children;

    KEYWORDS = ()
    SOFT_KEYWORDS = ()


if __name__ == '__main__':
    from pegen.parser import simple_parser_main
    simple_parser_main(GeneratedParser)
