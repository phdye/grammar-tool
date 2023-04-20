# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

"""
Grammar composition and testing tool

Usage:  grammar-tool [options] <action> [ARG...]

Actions :
  <action>        One of :
                    init          Initialize a work area for the grammar
                    compose       Generate composite grammar using components.gt
                                  and compose-order.gt
                    build         Build the grammar parser
                    test          Test the grammar
                    clean         Remove all generated files and directories

Grammar Styles :
  <style>         One of :        DEFAULT 'pegen'
                    pegen         Python's PEG parser, pegen
                    peg           Ian Piumarta's peg/leg, recursive-descent
                                  parser generators for C.
                    lark          Python Lark
                    antlr4        Java's ANTLR4 generating Python

Prefix Actions:
  --all                   Prior to <action>, perform all prior actions
  --clean                 Prior to <action>, perform clean
  --init                  Prior to <action>, perform init 
  --compose               Prior to <action>, perform compose
  --build                 Prior to <action>, perform build

Options:
  --style <style>         Specify parser generator to use
  -h, --help              Show this usage message.
  --version               Show version and exit.

Verbosity :               If multiple specified, least verbose wins.
  -v, --verbose <n>       Set verbosity level, DEFAULT 5 / INFO (25)
                          Note, verbosity options below override <n>.

  --argdebug              Show arguments as received and after parsed by docopt().

  -s, --silent            Set verbosity level 0   / <no-name>  (55)
  -q, --quiet             Set verbosity level 2   / ERROR      (40)

  --critical              Set log level CRITICAL? (50) / verbose 1
                          Actually, 45 which cannot have a matching verbose
                          number as 0 must map to NOTSET.
  --error                 Set log level ERROR     (40) / verbose 2
  --success               Set log level SUCCESS   (35) / verbose 3
  --warn, --warning       Set log level ERROR     (30) / verbose 4
  --notice                Set log level ERROR     (25) / verbose 5
  --info                  Set log level ERROR     (20) / verbose 6
  --log-verbose           Set log level VERBOSE   (15) / verbose 7
  --debug                 Set log level DEBUG     (10) / verbose 8
                          Show internal processing details.
  --spam                  Set log level SPAM       (5) / verbose 9
                          Show more internal processing details.

Logger Level :            Level = CRITICAL - 5 * verbose  (DEFAULT 25)

  Name      Lvl Verbose : Description
  ---------:----:----:----------------------------------------------------
  CRITICAL  50  :  0 : Serious error, generally the program can't continue
  ERROR     40  :  2 : More serious problem, unable to perform some function
  SUCCESS   35  :  3 : Confirmation of success
  WARNING   30  :  4 : Something unexpected happened or will shortly
                       ^^^ ALWAYS prints.  Will not be used.
  NOTICE    25  :  5 : Auditing information
  INFO      20  :  6 : Confirmation that things are working as expected
  VERBOSE   15  :  7 : Detailed behavior information
  DEBUG     10  :  8 : Details of interest only when diagnosing problems
  SPAM       5  :  9 : Too verbose for regular debugging but sometimes crucial

Report bugs as issues at https://github.com/philip-h-dye/grammar-tool.
"""

not_yet_implemented = """
   Or:  grammar-tool <style> --convert [options] <target-style>
        ** NOT IMPLEMENTED YET **  A bit ambitious really but it would be nice

                    arpeggio      Python Arpeggio, available from PyPi
                    parsimonious  Python parsimonious, available from PyPi
                    pyparsing     Python pyparsing, available from PyPi

"""

import sys
import os
import shutil
import importlib
import yaml

from pathlib import Path

from dataclasses import dataclass
from collections import namedtuple

from docopt_attr import docopt_attr

from grammar_tool.wrap import IndentWrap, IndentWrapContext

from grammar_tool.__init__ import __version__

from grammar_tool.chdir import ChDir

from prettyprinter import cpprint as pp
from grammar_tool.pp import hash_pp

from grammar_tool.config import GtConfig

#------------------------------------------------------------------------------

import logging
import verboselogs

verboselogs.install()

logger = verboselogs.VerboseLogger('grammar_tool')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.SUCCESS)    # 35 : below ERROR(40), above WARNING(30)
logger.setLevel(1)					# Everything prints
#logger.setLevel(0)					# Nothing prints, same as logging.NOTSET

VERBOSE = namedtuple('VerboseLimits', 'MIN MAX')( 0, 9 )

#------------------------------------------------------------------------------

def main ( argv : list = sys.argv, depth : int = 0 ) :

    try :

        return worker ( argv, depth )

    except FileNotFoundError as e :
        # Original :
        #   str()   : [Errno 2] No such file or directory: PosixPath('work')
        #   repr()  : FileNotFoundError(2, 'No such file or directory')
        # Now :
        #   str()   : No such file or directory: \
        #               '/home/phdyex/src/python/grammar-tool/test-files/lark/adder/num/work'
        logger.critical(str(e))
        return 1

#------------------------------------------------------------------------------

def worker( argv : list, depth : int ) :

    wrapper = IndentWrap(initial_column=depth, column_width=2,
                         logger=logger, hierarchy=False)

    if '--argdebug' in argv:
        wrapper.wprint("# main( argv ) :")
        hash_pp(argv, xprint = wrapper.wprint)
        wrapper.wprint('')

    ctx = docopt_attr(__doc__, argv=argv[1:], options_first=True,
                       version=__version__ )

    ctx.ACTIONS   = ( 'init', 'compose', 'build', 'test', 'clean' )
    ctx.depth     = depth
    ctx.wrapper   = wrapper
    ctx.logger    = logger
    ctx.area      = Path('.').resolve().parts[-1]
    ctx._docopt   = None

    ctx = GtConfig(ctx).load()

    configure_logging(ctx)

    ctx.ACTIONS = [ 'init', 'compose', 'build', 'test', 'clean' ]
    ctx.depth = depth
    ctx.wrapper = wrapper
    if ctx.action not in ctx.ACTIONS:
        ctx.wrapper.critical(f"{ctx.program}:  <action> '{ctx.action}' not supported."
               f"  Please specify one of {ctx.ACTIONS.keys()}")
        return 1

    ctx.parent = ctx.compose_order.exists()
    if ctx.parent:
        if retcode := process_children(ctx):
            return retcode

    configure_composition(ctx)

    prev = (os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else ''
    os.environ['PYTHONPATH'] = '.' + prev

    generator_module = importlib.import_module(f'grammar_tool.generator.{ctx.style.name}')
    GrammarTool = generator_module.GrammarTool(ctx)
    return getattr(GrammarTool, f"do_{ctx.action}")()

#------------------------------------------------------------------------------

def configure_logging(ctx):

    # If use specified multiple verbosity options, the least verbose wins.

    verbose = None

    if ctx.spam:
        verbose = 9
    if ctx.debug:
        verbose = 8
    if ctx.log_verbose:
        verbose = 7
    if ctx.info:
        verbose = 6
    if ctx.notice:
        verbose = 5
    if ctx.warning:
        verbose = 4
    if ctx.success:
        verbose = 3
    if ctx.quiet:
        verbose = 2
    if ctx.error:
        verbose = 2
    if ctx.critical:
        verbose = 1
    if ctx.silent:
        verbose = 0

    def int_verbose(verbose):
        return min ( max ( int(verbose), VERBOSE.MIN ), VERBOSE.MAX )

    if ctx.verbose is not None :
        ctx.verbose = int_verbose(ctx.verbose)
        if verbose is not None :
            ctx.verbose = min ( ctx.verbose, verbose )
    else :
        if verbose is not None :
            ctx.verbose = min( verbose, VERBOSE.MAX )
        else :
            ctx.verbose = int_verbose(ctx.DEFAULT_VERBOSE)

    if ctx.verbose > 0:
        ctx.log_level = max( logging.CRITICAL - 5 * ctx.verbose, 1 )
    else:
        ctx.log_level = logging.CRITICAL + 1
    ctx.logger.setLevel( ctx.log_level )

    # If hierarchy, items are indented by recursion depth and level of detail
    ctx.wrapper.hierarchy = ctx.hierarchy = ( ctx.verbose > 5 )
    if not ctx.hierarchy:
        ctx.wrapper.area_fill = f"{ctx.area:<20}  : "
        ctx.wrapper.move_to(0, keep=False)
        ctx.depth = 0

#------------------------------------------------------------------------------

def configure_composition(ctx):

    # ctx.this_grammar.exists()
    # ctx.grammar_start.exists()
    # ctx.no_grammar = not False
    
    ctx.parent = ctx.compose_order.exists()
    if ctx.style is None:
        ctx.style = ctx.DEFAULT_STYLE

    if ctx.style not in ctx.GRAMMAR_STYLES:
        ctx.wrapper.critical(f"{ctx.program}:  Grammar <style> '{ctx.style}' not supported."
                        f"  Please specify one of {GRAMMAR_STYLES.keys()}")
        sys.exit(1)

    ctx.style = ctx.GRAMMAR_STYLES[ctx.style]

#------------------------------------------------------------------------------

def process_children(ctx):

    c = ctx

    def blank_line( limiting_level = logging.SUCCESS):
        c.logger.log(limiting_level, '')

    c.wrapper.success(f"'{c.area}' is a parent, see to it's children")
    blank_line(logging.SUCCESS)

    with IndentWrapContext(c.wrapper, 1):

        c.wrapper.info(f"gather children")
        with IndentWrapContext(c.wrapper, 1):
            with open(c.compose_order, 'r') as fp:
                children = [child.strip() for child in fp]
            c.order = [child for child in children if not child.startswith('#')]
            c.wrapper.verbose(f"found {len(c.order)} children : {c.order}")
            if len(c.order) == 0:
                raise ValueError("No children found in '{Path(c.compose_order).resolve()}'")
        blank_line(logging.INFO)

        c.wrapper.info(f"process children")
        with IndentWrapContext(c.wrapper, 1):
            for child in reversed(c.order) :
                child = child.strip()
                if c.hierarchy:
                    c.wrapper.notice(f"'{child}'")
                with ChDir(child):
                    if retcode := main(sys.argv, c.depth + 3):
                        return retcode
                blank_line()

    # Due to the children, the next notice won't be directly below this one.
    # This applies to either the message below or later.
    c.wrapper.spaces_fill = None

    c.wrapper.info(f"'{c.area}' resume")
    c.wrapper.move(1) # No affect on logging should ctx.hierarchy be false

    return 0

#------------------------------------------------------------------------------
