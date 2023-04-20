# -*- coding: utf-8 -*-

"textwrap with fix-size column indentation adjustment"

__version__ = '0.2.1'

import sys
import logging

from dataclasses import dataclass, field

from typing import List

import textwrap

DEFAULT_INITIAL_COLUMN = 0
DEFAULT_COLUMN_WIDTH = 4
DEFAULT_PAGE_WIDTH = 80

@dataclass
class IndentWrap ( textwrap.TextWrapper ):
    
    """

    Supply a context manager to manage indentation columns.

    IndentWrap ( initial_column = 0, column_width = page_width = 80 )

    Moves left or right are kept on a stack unless keep=False.

      >>> from indent_wrap import IndentWrap
      >>>
      >>> wrapper = IndentWrap()
      >>> wrapper.wprint('Hello')
      Hello
      >>> wrapper.move_right(2)
      >>> wrapper.wprint('Hello')
              Hello
      >>> wrapper.move_left()
      >>> wrapper.wprint('Hello')
          Hello
      >>> wrapper.revert()
      >>> wrapper.wprint('Hello')
              Hello
      >>> wrapper.revert()
      >>> wrapper.wprint('Hello')
      Hello

      >>> wrapper = IndentWrap(initial_column=2)
      >>> wrapper.wprint('Hello')
              Hello
      >>> wrapper.move_right()
      >>> wrapper.wprint('Hello')
                  Hello
      >>> wrapper.move_right(keep=False)
      >>> wrapper.wprint('Hello')
                      Hello
      >>> wrapper.revert()
      >>> wrapper.wprint('Hello')
              Hello
      >>> wrapper.move(-1)
      >>> wrapper.wprint('Hello')
          Hello

    """

    current_column  : int
    column_width    : int
    column_stack    : List
    logger          : logging.Logger
    hierarchy       : bool
    area_fill       : str = None
    spaces_fill     : str = None

    # Note: dataclass does not implement __init__ when parent class has __init__
    def __init__( self,
                  initial_column  : int = DEFAULT_INITIAL_COLUMN,
                  column_width    : int = DEFAULT_COLUMN_WIDTH,
                  page_width      : int = DEFAULT_PAGE_WIDTH,
                  logger          : logging.Logger = None,
                  hierarchy       : bool = False,
                  area_fill       : str = None,
                  spaces_fill     : str = None,
                ) :

        #print(f"::: IndentWrap( initial = {initial_column} )", flush=True)

        super().__init__()
        self.logger              = logger
        self.area_fill           = area_fill
        self.spaces_fill         = spaces_fill
        self.current_column      = initial_column
        self.column_width        = column_width
        self.width               = page_width
        self.column_stack        = []
        self._set_indents()

    #--------------------------------------------------------------------------

    def fill(self, text):
        ( tag, output ) = self._fill(text)
        #print(f": {tag:<6} : '{output}'", flush=True)
        return output
        
    def _fill(self, text):
        if not self.area_fill:
            return ( 'dash', super().fill('- ' + text) )
        if self.spaces_fill:
            # print(f": space fill  :  '{self.area_fill}'")
            return ( 'space', super().fill(self.spaces_fill + text) )
        # print(f": area fill   :  '{self.area_fill}'")
        return ( 'area', super().fill(self.area_fill + text) )

    #--------------------------------------------------------------------------

    def _spaces_fill(self, log_level : int):
        if ( not self.hierarchy and
             self.area_fill and
             self.logger.level <= log_level
           ) :
            self.spaces_fill = ' ' * (len(self.area_fill) - 2 ) + ': '

    #--------------------------------------------------------------------------

    def critical(self, *objects, sep=' '):
        self.logger.critical(self.fill(sep.join(objects)))
        self._spaces_fill(logging.CRITICAL)

    def error(self, *objects, sep=' '):
        self.logger.error(self.fill(sep.join(objects)))
        self._spaces_fill(logging.ERROR)

    def success(self, *objects, sep=' '):
        self.logger.success(self.fill(sep.join(objects)))
        self._spaces_fill(logging.SUCCESS)

    def warning(self, *objects, sep=' '):
        self.logger.warning(self.fill(sep.join(objects)))
        self._spaces_fill(logging.WARNING)

    def notice(self, *objects, sep=' '):
        self.logger.notice(self.fill(sep.join(objects)))
        self._spaces_fill(logging.NOTICE)

    def info(self, *objects, sep=' '):
        self.logger.info(self.fill(sep.join(objects)))
        self._spaces_fill(logging.INFO)

    def verbose(self, *objects, sep=' '):
        self.logger.verbose(self.fill(sep.join(objects)))
        self._spaces_fill(logging.VERBOSE)

    def debug(self, *objects, sep=' '):
        self.logger.debug(self.fill(sep.join(objects)))
        self._spaces_fill(logging.DEBUG)

    def spam(self, *objects, sep=' '):
        self.logger.spam(self.fill(sep.join(objects)))
        self._spaces_fill(logging.SPAM)

    #--------------------------------------------------------------------------

    def wprint(self, *objects, sep=' ', end='\n', file=None, flush=False):
        if file is None:
            file = sys.stdout
        print(self.fill(sep.join(objects)), sep=sep, end=end, file=file,
              flush=flush)

    #--------------------------------------------------------------------------

    def move_right(self, columns = 1, keep = True):
        if columns <= 0:
            raise ValueError(f"move_right(columns) : columns {columns} must be at least 1.")
        # print(f": move right  ( columns = {columns}, keep = {keep} )", file=sys.__stderr__)
        self.move(columns, keep)

    def move_left(self, columns = 1, keep = True):
        if columns <= 0:
            raise ValueError(f"move_left(columns) : columns {columns} must be at least 1.")
        # print(f": move left   ( columns = {columns}, keep = {keep} )", file=sys.__stderr__)
        self.move(-columns, keep)

    def move(self, columns = 0, keep = True):
        # print(f": move        ( columns = {columns}, keep = {keep} )", file=sys.__stderr__)
        if keep:
            self.column_stack.append(self.current_column)
        self.current_column = max(self.current_column + columns, 0)
        self._set_indents()
        spaces = self.current_column * self.column_width
        # print(f": move        => {self.column_stack}", file=sys.__stderr__)
        # print(f": move        => current_column = {self.current_column}", file=sys.__stderr__)

    def revert(self):
        # print(f": revert      {self.column_stack}", file=sys.__stderr__)
        try:
            self.current_column = self.column_stack.pop()
        except IndexError:
            self.current_column = 0
        self._set_indents()
        # print(f": revert      => {self.column_stack}", file=sys.__stderr__)
        # print(f": revert      => current_column = {self.current_column}", file=sys.__stderr__)

    def move_to(self, column, keep = True):
        # print(f": move_to     ( columns = {columns}, keep = {keep} )", file=sys.__stderr__)
        if keep:
            self.column_stack.append(self.current_column)
        self.current_column = max(column, 0)
        self._set_indents()
        # spaces = self.current_column * self.column_width
        # print(f": move_to     => {self.column_stack}", file=sys.__stderr__)
        # print(f": move_to     => current_column = {self.current_column}", file=sys.__stderr__)

    def _set_indents(self):
        # prefix = ' ' * self.current_column * self.column_width
        spaces = self.current_column * self.column_width
        # print(f": spaces =    {spaces}", file=sys.__stderr__)
        prefix = ' ' * spaces
        self.initial_indent = prefix
        self.subsequent_indent = prefix


@dataclass
class IndentWrapContext:
    wrapper             : IndentWrap
    offset              : int
    original_column     : int = 0
    def __enter__(self):
        #print(f"::: IndentWrapContext( offset = {self.offset} )", flush=True)
        self.original_column = self.wrapper.current_column
        self.wrapper.move(self.offset, keep=False)
    def __exit__(self, type, value, traceback):
        self.wrapper.move_to(self.original_column, keep=False)

if __name__ == "__main__":
    import doctest
    flags = doctest.REPORT_NDIFF|doctest.FAIL_FAST
    doctest.testmod(optionflags=flags)

