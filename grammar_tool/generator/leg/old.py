# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

"""
Grammar Tool implementation for Ian Piumarta's peg/leg, recursive-descent
parser generators for C.

Report bugs as issues at https://github.com/philip-h-dye/grammar-tool.
"""

import sys
import os
import shutil

from pathlib import Path

from plumbum import local, commands

from grammar_tool.wrap import IndentWrapContext

from grammar_tool.ChDir import ChDir

from grammar_tool.pp import hash_pp

#------------------------------------------------------------------------------

make = local['make']

# GRAMMAR_CODE = "grammar.py"

#------------------------------------------------------------------------------

def work_base_must_not_exist(ctx, action):

    if Path(ctx.work_base).exists():
        if os.path.isfile(ctx.work_base):
            raise ValueError(f"{ctx.program} {action} :  Work base '{ctx.work_base}'"
                             f"exists but oddly it is file rather than a"
                             f"directory.  Please resolve.")

        raise ValueError(f"{ctx.program} {action} :  Work base '{ctx.work_base}'"
                         f" exists.\n If you do wish to recreate it, please"
                         f" first execute 'grammar-tool clean'")

def work_base_must_exist(ctx, action):

    if not Path(ctx.work_base).exists():
        raise ValueError(f"{ctx.program} {action} :  Work base '{ctx.work_base}' does"
                         f" not exist.\n"
                         f"Please first execute 'grammar-tool init <style>'")

def file_must_exist(ctx, action, file_name):

    if not Path(file_name).exists():
        file_path = Path(Path.cwd(), file_name)
        raise ValueError(f"{ctx.program} {action} :  File does not exist,"
                         f"'{file_path}'")

def remove_file(ctx, file_path):
    wprint = ctx.wrapper.wprint
    try :
        Path(file_path).unlink()
        wprint(f"  - removed '{file_path}'")
    except FileNotFoundError:
        wprint(f"  - not present '{file_path}'")

#------------------------------------------------------------------------------

def do_init(ctx, recurse=False):

    wprint = ctx.wrapper.wprint

    if ctx.clean or ctx.all:
        if retcode := do_clean(ctx, not_exists_ok=True):
            return retcode

    wprint(f"- init {ctx.style.name} :")

    work_base_must_not_exist(ctx, 'init')

    root = os.path.dirname( os.path.abspath(os.path.dirname(__file__)) )
    model_base = os.path.relpath(os.path.join(root, 'model', ctx.style.name), '.')
    shutil.copytree(model_base, ctx.work_base)
    wprint(f"  - installed {model_base} in {os.path.join('.', ctx.work_base)}")

    driver = Path("main.c")
    if driver.exists():
        shutil.copy(driver, ctx.work_base)
        
    ast_c = Path("ast.c")
    if ast_c.exists():
        shutil.copy(ast_c, ctx.work_base)
        
    return 0

#------------------------------------------------------------------------------

def concatenate_files(ctx, destination, input_files):
    with open(destination, 'w') as target:
        for file_name in input_files:
            file_must_exist(ctx, destination, file_name)
            with open(file_name, 'r') as source:
                target.write(source.read())        
        
#------------------------------------------------------------------------------

def do_compose(ctx, recurse=False):

    wprint = ctx.wrapper.wprint

    if ctx.init or ctx.all:
            if retcode := do_init(ctx, recurse=False):
                return retcode

    wprint(f"- compose :")

    #tokens_common   = ctx.models['tokens-common']
    #tokens_body     = ctx.models['tokens-body']
    #tokens          = ctx.models['tokens']

    grammar         = ctx.models['grammar'].format(style=ctx.style.ext)
    this_grammar    = ctx.models['this-grammar'].format(style=ctx.style.ext)

    work_base_must_exist(ctx, 'compose')

    rule_name = os.path.basename(os.path.abspath('.'))

    if ctx.parent:
        
        children = [ f'{child}/{this_grammar}' for child in ctx.order ]
        concatenate_files(ctx, this_grammar, children)
        wprint(f"  - composed '{this_grammar}'")

        # # compose tokens.py
        # children = []
        # for child in ctx.order :
        #     body = f'{child}/{tokens_body}'
        #     if Path(body).exists():
        #         children.append(body)
        # if children:
        #     concatenate_files(ctx, tokens_body, children)
        #     wprint(f"  - composed '{tokens_body}'")
        #     concatenate_files(ctx, tokens, [ tokens_common, tokens_body ])
        #     wprint(f"  - composed '{tokens}'")
        # else:
        #     wprint(f"  - No tokens, skipped '{tokens}'")

        shutil.copy(this_grammar, grammar)
        wprint(f"  - composed {grammar}")

    else:

        components_file = ctx.models['components']
        if not Path(components_file).exists():
            wprint(f"  - missing '{components_file}'")
            # none
            components = []
            # unless, parent has compose order, then all before this
            components_file = os.path.join('..', ctx.models['compose-order'])
            if Path(components_file).exists():
                wprint(f"  - found '{components_file}'")
                with open(components_file, 'r') as fp:
                    elements = [ _ for _ in [ _.strip() for _ in fp ] if _ ]
                if rule_name in elements:
                    components = elements[elements.index(rule_name)+1:]
            else:
                wprint(f"  - missing '{components_file}'")
        else:
            with open(components_file, 'r') as fp:
                components = [ _ for _ in [ _.strip() for _ in fp ] if _ ]

        grammar_files = [ this_grammar ]
        wprint(f"  - components {components}")
        for component in components :
            component_base = ctx.models['component-base'].format(component=component)
            component_grammar = f"{component_base}/{this_grammar}"
            if Path(component_grammar).exists():
                grammar_files.append(component_grammar)
        wprint(f"  - input files {grammar_files}")
        concatenate_files(ctx, grammar, grammar_files)
        wprint(f"  - composed {grammar}")

        # token_files = []
        # if Path(tokens_body).exists():
        #     token_files.append(tokens_body)
        # for component in components :
        #     component_base = ctx.models['component-base'].format(component=component)
        #     component_tokens = os.path.join(component_base, tokens_body)            
        #     if Path(component_tokens).exists():
        #         token_files.append(component_tokens)
        # if token_files:
        #     token_files.insert(0, tokens_common)
        #     concatenate_files(ctx, tokens, token_files)
        #     wprint(f"  - composed '{tokens}'")
        # else:
        #     wprint(f"  - No tokens, skipped '{tokens}'")
        
    ctx.test_grammar = ctx.models['test-grammar'].format(work_base=ctx.work_base, style=ctx.style.ext)
    grammars = [ grammar ]
    grammar_start = ctx.models['grammar-start'].format(style=ctx.style.ext)
    if Path(grammar_start).exists():
        grammars.insert(0, grammar_start)
    else:        
        if rule_name == 'start':
            wprint(f"  - missing '{grammar_start}', rule is 'terminate', unnecessary")
        else:
            grammar_start = os.path.join('work', grammar_start)
            with open(grammar_start, 'w') as fp:
                # Removed [ \\t\\r\\n]*
                print(f"start <- < {rule_name} > !."
                      '{ printf("%s\\n", yytext); }\n',
                      file=fp)
            grammars.insert(0, grammar_start)

    concatenate_files(ctx, ctx.test_grammar, grammars)
    wprint(f"  - composed '{ctx.test_grammar}'")

    test_this = ctx.models['test-this']
    tests_base = ctx.models['tests-base'].format(work_base=ctx.work_base)

    shutil.copy(test_this, tests_base)
    installed = os.path.join(tests_base, test_this)
    wprint(f"  - installed {installed}")

    # shutil.copy(tokens, tests_base)
    # installed = os.path.join(tests_base, tokens)
    # wprint(f"  - installed {installed}")

    wprint("  - compose complete")

    return 0

#------------------------------------------------------------------------------

def _make(ctx, caller, argv, expected_return):
    try :
        make[argv](retcode = expected_return)
    except commands.processes.ProcessExecutionError:
        raise ValueError(f"{ctx.program} {caller}:  'make {argv}' failed.")

#------------------------------------------------------------------------------

def do_build(ctx, recurse=False):

    wprint = ctx.wrapper.wprint

    if ctx.compose or ctx.all:
        if retcode := do_compose(ctx):
            return retcode

    wprint(f"- build parser :")

    with ChDir(ctx.work_base) :
        _make(ctx, 'build', ['all'], 0)

    wprint(f"  - parser built")

#------------------------------------------------------------------------------

def do_test(ctx, recurse=False):

    wprint = ctx.wrapper.wprint

    if ctx.build or ctx.all:
        if retcode := do_build(ctx):
            return retcode

    wprint(f"- test :")

    with ChDir(ctx.work_base) :
        _make(ctx, 'test', ['test'], 0)

    wprint(f"  - all tests passed")

#------------------------------------------------------------------------------

def do_clean(ctx, recurse=False, not_exists_ok=False):

    wprint = ctx.wrapper.wprint

    if Path(ctx.work_base).exists() and Path(ctx.work_base).is_dir():
        wprint(f"- cleaning :")
        # remove_file(ctx, ctx.models['tokens'])        
        shutil.rmtree(ctx.work_base)
        wprint(f"  - removed '{os.path.join('.', ctx.work_base)}'")
    else:
        wprint(f"- cleaning, work area '{ctx.work_base}' does not exist, ok.")

    remove_file(ctx, ctx.models['grammar'].format(style=ctx.style.ext))
    
    if ctx.parent:
        remove_file(ctx, ctx.models['this-grammar'].format(style=ctx.style.ext))
        remove_file(ctx, ctx.models['tokens-body'])

#------------------------------------------------------------------------------
