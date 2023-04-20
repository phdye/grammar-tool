# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

"""
Grammar composition and testing tool

Usage:  grammar-tool [options] <action> [ARG...]

Actions :
  <action>        One of :
                    init <style>  Initialize a work area for grammar <style>
                    compose       Generate composite grammar using components.gt
                    build         Build the grammar parser
                    test          Test the grammar
                    clean         Remove all generated files and directories

Grammar Styles :
  <style>         One of :
                    peg         Ian Piumarta's peg/leg, recursive-descent
                                parser generators for C.

Prefix Actions:
  --all           Prior to <action>, perform all prior actions
  --clean         Prior to <action>, perform clean
  --init          Prior to <action>, perform init 
  --compose       Prior to <action>, perform compose
  --build         Prior to <action>, perform build

  --style <style> specify style for init action when '--all'

Options:
  -h, --help      Show this usage message.
  --version       Show version and exit.
  --debug         Show internal processing details.  For 'test', show internal
                  parsing details where available.
  --argdebug      Show arguments as received and after parsed by docopt().


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

from docopt_attr import docopt_attr
from plumbum import local, commands

from functools import partial

import indent_wrap

from .__init__ import __version__

from .ChDir import ChDir

from .p import hash_pp

#------------------------------------------------------------------------------

program = 'grammar-tool'

actions = "init compose build test clean".split() 

grammar_styles = "peg".split()

work_base = 'work'

models = { 'style'				: "{work_base}/grammar-style",
           'components' 		: "components.gt",
           'grammar'			: "grammar.{style}",
           'grammar_terminate'	: "terminate.{style}",
           'test_grammar'		: "{work_base}/test-grammar.{style}",
           'tests-base'			: "{work_base}/tests",
           'test-this'			: "test_this.py",
           'compose-order'			: "compose-order.txt",
}

make = local['make']


text = {
    'width'		: 80,
    'indent'	: 2,
    }

#------------------------------------------------------------------------------
             
def main ( argv = sys.argv, depth=0) :

    wrapper = indent_wrap.IndentWrap()

    if '--argdebug' in argv:
        wrapper.wprint("# main( argv ) :")
        hash_pp(argv, xprint = wrapper.wprint)
        wrapper.wprint('')

    args = docopt_attr(__doc__, argv=argv[1:], options_first=True,
                       version=__version__ )


    args.wrapper = wrapper

    wprint = wrapper.wprint

    if args.argdebug:
        wprint("# main(): args <- docopt(...) :")
        hash_pp(args, xprint = wprint)
        wprint('')

    if args.action not in actions:
        wprint(f"{program}:  <action> '{args.action}' not supported."
              f"  Please specify one of {actions}")
        return 1

    setattr(args, 'depth', depth)

    compose_order = models['compose-order']
    setattr(args, 'parent', os.path.exists(compose_order))
    if args.parent:
        with open(compose_order, 'r') as fp:
            setattr(args, 'order', [ child for child in fp ])

    this_module = sys.modules[__name__]    
    return getattr(this_module, f"do_{args.action}")(args, recurse=True)

#------------------------------------------------------------------------------

def work_base_must_not_exist(ctx, action):

    if os.path.exists(work_base):
        if os.path.isfile(work_base):
            raise ValueError(f"{program} {action} :  Work base '{work_base}'"
                             f"exists but oddly it is file rather than a"
                             f"directory.  Please resolve.")

        raise ValueError(f"{program} {action} :  Work base '{work_base}'"
                         f" exists.\n If you do wish to recreate it, please"
                         f" first execute 'grammar-tool clean'")

def work_base_must_exist(ctx, action):

    if not os.path.exists(work_base):
        raise ValueError(f"{program} {action} :  Work base '{work_base}' does"
                         f" not exist.\n"
                         f"Please first execute 'grammar-tool init <style>'")

#------------------------------------------------------------------------------

def process_children(ctx):

    wprint = partial(ctx.wprint, ctx)

    for child in reversed(ctx['order']) :
        child = child.strip()
        wprint(f"- descend into {child}")
        with ChDir(child):
            if retcode := main(sys.argv, ctx.depth+1):
                return retcode

    return 0

#------------------------------------------------------------------------------

def do_init(ctx, recurse=False):

    wprint = partial(ctx.wprint, ctx)

    if not ctx.ARG:
        if not ctx.style:
            wprint(f"{program} init:  Grammar <style> missing."
                  f"  Please specify one of {grammar_styles}")
            return 1
        ctx.ARG = [ctx.style]

    style = ctx.ARG[0]
    if style not in grammar_styles:
        wprint(f"{program} init:  Grammar <style> '{style}' not supported."
              f"  Please specify one of {grammar_styles}")
        return 1

    wprint(f"- init {style} ...")

    if recurse and ctx.parent:
        return process_children(ctx)
    
    if ctx.clean or ctx.all:
        ctx.depth += 1
        if ( retcode := do_clean(ctx, not_exists_ok=True) ):
            return retcode
        ctx.depth -= 1

    work_base_must_not_exist(ctx, 'init')

    _ROOT = os.path.abspath(os.path.dirname(__file__))

    model_base = os.path.relpath(os.path.join(_ROOT, 'model', style), '.')

    shutil.copytree(model_base, work_base)
    wprint(f"  - installed {model_base} in {os.path.join('.', work_base)}")

    style_file = models['style'].format(work_base=work_base)
    with open(style_file, 'w') as style_fp:
        wprint(style, file=style_fp)

#------------------------------------------------------------------------------

# No reason 
def concatenate_files(destination, input_files):
    cat = local['cat']
    try :
        (cat[input_files] > destination)(retcode = 0)
    except commands.processes.ProcessExecutionError:
        raise ValueError(f"{program} {caller}:  'make {argv}' failed.")
    
#------------------------------------------------------------------------------

def do_compose(ctx, recurse=False):

    if ctx.parent:
        if retcode := process_children(ctx, recurse=False):
            return retcode
    
    wprint = partial(ctx.wprint, ctx)

    if ctx.init or ctx.all:
        if retcode := do_init(ctx, recurse=False):
            return retcode

    wprint(f"- compose ...")

    if not ctx.parent:
        
        work_base_must_exist(ctx, 'compose')
        
        style_file = models['style'].format(work_base=work_base)
        with open(style_file, 'r') as style_fp:
            style = style_fp.read().strip()
            grammar = models['grammar'].format(style=style)
            components_file = models['components']
            with open(components_file, 'r') as components_fp:
                input_files = [ line.strip() for line in components_fp ]
                concatenate_files(grammar, input_files)
            wprint(f"  - composed {grammar}")

    grammar_terminate = models['grammar_terminate'].format(style=style)
    test_grammar = models['test_grammar'].format(work_base=work_base, style=style)

    concatenate_files(test_grammar, [ grammar_terminate, grammar ])
    wprint(f"  - composed {test_grammar}")

    test_this = models['test-this']
    tests_base = models['tests-base'].format(work_base=work_base)

    shutil.copy(test_this, tests_base)
    installed = os.path.join(tests_base, test_this)
    wprint(f"  - installed {installed}")

    wprint("  - composed complete")

#------------------------------------------------------------------------------

def _make(caller, argv, expected_return):
    try :
        make[argv](retcode = expected_return)
    except commands.processes.ProcessExecutionError:
        raise ValueError(f"{program} {caller}:  'make {argv}' failed.")

#------------------------------------------------------------------------------

def do_build(ctx, recurse=False):

    wprint = partial(ctx.wprint, ctx)

    if recurse and ctx.parent and ( retcode := process_children(ctx) ):
        return retcode
    
    if ctx.compose or ctx.all:
        if ( retcode := do_compose(ctx) ):
            return retcode

    wprint(f"- build ...")

    with ChDir(work_base) :
        _make('build', ['all'], 0)

    wprint(f"  - parser built")

#------------------------------------------------------------------------------

def do_test(ctx, recurse=False):

    wprint = partial(ctx.wprint, ctx)

    if recurse and ctx.parent and ( retcode := process_children(ctx) ):
        return retcode
    
    if ctx.build or ctx.all:
        if ( retcode := do_build(ctx) ):
            return retcode

    wprint(f"- test ...")

    with ChDir(work_base) :
        _make('test', ['test'], 0)

    wprint(f"  - all tests passed")

#------------------------------------------------------------------------------

def do_clean(ctx, recurse=False, not_exists_ok=False):

    wprint = partial(ctx.wprint, ctx)

    if recurse and ctx.parent and ( retcode := process_children(ctx) ):
        return retcode
    
    if not os.path.exists(work_base):
        if not_exists_ok:
            wprint(f"- cleaning ... Work area '{work_base}' does not exist, ok.")
            return 0
        
    work_base_must_exist(ctx, 'clean')

    wprint(f"- cleaning ...")

    shutil.rmtree(work_base)
    wprint(f"  - removed {os.path.join('.', work_base)}")

#------------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main(sys.argv))

#------------------------------------------------------------------------------
