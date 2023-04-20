# -*- coding: utf-8 -*-

"""
Grammar Tool common implementation

Report bugs as issues at https://github.com/philip-h-dye/grammar-tool.
"""

import sys
import os
import shutil
import logging

from pathlib import Path

from plumbum import local, commands

from grammar_tool.wrap import IndentWrapContext

from grammar_tool.ChDir import ChDir

from grammar_tool.pp import hash_pp


class GrammarToolCommon:

    def __init__(self, ctx):
        self.ctx = ctx
        self.actions = {'start', 'build'} # implicit actions

    #--------------------------------------------------------------------------

    def init_action(self, ctx):
        pass

    def do_init(self, recurse=False):

        c = self.ctx

        if c.clean or c.all:
            if retcode := self.do_clean(not_exists_ok=True):
                return retcode

        prefix = "" # f"'{c.area}' " if c.hierarchy and not c.print_directory else ''

        c.wrapper.info(f"{prefix}initialize for generator '{c.style.name}'")

        with IndentWrapContext(c.wrapper, 1):

            self.work_base_must_not_exist('init')

            model_style_base = os.path.relpath(c.model_style_base, c.base)
            c.wrapper.verbose(f"populating '{c.work_base}' from '<grammar_tool>/{model_style_base}'")
            shutil.copytree(c.model_style_base, c.work_base)

            if 'init' in self.actions:
                self.init_action()

            if c.logger.level <= logging.VERBOSE:
                prefix = ''
            self.verbose_success(f"{prefix}populated '{c.work_base}'")

        return 0

    #--------------------------------------------------------------------------

    def start_action(self, fp):
        pass

    def compose_action(self, ctx):
        pass

    def do_compose(self, recurse=False):

        c = self.ctx

        c.rule_name = os.path.basename(os.path.abspath('.'))

        if c.init or c.all:
            if retcode := self.do_init(recurse=False):
                return retcode

        prefix = "" # f"'{c.area}' " if c.hierarchy and not c.print_directory else ''

        c.wrapper.info(f"{prefix}compose")

        self.work_base_must_exist('compose')

        with IndentWrapContext(c.wrapper, 1):
            if c.parent:
                self.compose_parent()
            else:
                self.compose_leaf()

            self.compose_common()

            self.verbose_success("compose complete")

    def compose_parent(self, recurse=False):

        c = self.ctx

        children = [ f'{child}/{c.this_grammar}' for child in c.order ]
        self.concatenate_files(c.this_grammar, children)
        c.wrapper.verbose(f"composed '{c.this_grammar}'")

        with IndentWrapContext(c.wrapper, 1):
            children = []
            for child in c.order :
                body = f'{child}/{c.tokens_body}'
                if Path(body).exists():
                    children.append(body)
            if children:
                self.concatenate_files(tokens_body, children)
                c.wrapper.verbose(f"composing '{c.tokens_body}'")
                self.concatenate_files(tokens, [ tokens_common, tokens_body ])
                c.wrapper.verbose(f"composed")
            else:
                c.wrapper.verbose(f"No tokens, skipped '{c.tokens}'")

            shutil.copy(c.this_grammar, c.grammar)
            c.wrapper.verbose(f"composed {c.grammar}")

    def compose_leaf(self):
        
        c = self.ctx

        c.wrapper.verbose(f"gathering components")
        with IndentWrapContext(c.wrapper, 1):
            components_file = c.components
            if not Path(components_file).exists():
                c.wrapper.debug(f"missing '{components_file}'")
                # none
                components = []
                # unless, parent has compose order, then all before this
                components_file = Path('..') / c.compose_order
                if not Path(components_file).exists():
                    c.wrapper.debug(f"missing '{components_file}'")
                else:
                    c.wrapper.debug(f"loading '{components_file}'")
                    elements = self.load_lines(components_file)
                    if c.rule_name in elements:
                        components = elements[elements.index(c.rule_name)+1:]
            else:
                c.wrapper.debug(f"loading '{components_file}'")
                with open(components_file, 'r') as fp:
                    components = self.load_lines(components_file)

            remark = f"{len(components)}" if components else "No"
            c.wrapper.debug(f"{remark} components applicable")

        c.wrapper.verbose(f"composing {c.grammar}")            
        with IndentWrapContext(c.wrapper, 1):
            grammar_files = [ c.this_grammar ]
            c.wrapper.debug(f"components {c.components}")
            for component in components :
                c.component = component # required to resolve component_base
                component_grammar = f"{c.component_base}/{c.this_grammar}"
                if Path(component_grammar).exists():
                    grammar_files.append(component_grammar)
                    c.wrapper.debug(f"input files {[str(g) for g in grammar_files]}")
            self.concatenate_files(c.grammar, grammar_files)
            c.wrapper.debug(f"composed")

        c.wrapper.verbose(f"composing '{c.tokens}'")
        with IndentWrapContext(c.wrapper, 1):
            token_files = []
            if Path(c.tokens_body).exists():
                token_files.append(c.tokens_body)
            for component in components :
                c.component = component # required to resolve component_base
                # component_tokens = os.path.join(c.component_base, c.tokens_body)
                component_tokens = c.component_base / c.tokens_body
                if Path(component_tokens).exists():
                    token_files.append(component_tokens)
            if token_files:
                token_files.insert(0, c.tokens_common)
                self.concatenate_files(c.tokens, token_files)
                c.wrapper.debug(f"composed '{c.tokens}'")
            else:
                c.wrapper.debug(f"No tokens, skipped '{c.tokens}'")

    def compose_start(self):

        c = self.ctx

        if c.grammar_start.exists():
            return [ c.grammar_start ]

        if c.rule_name == 'start':
            c.wrapper.debug(f"missing '{c.grammar_start}', rule is 'start', unnecessary")
            return []
        
        if 'start' not in self.actions:
            return []
    
        grammar_start = c.work_base / c.grammar_start
        with open(grammar_start, 'w') as fp:
            self.start_action(fp, c.rule_name)
            return [ grammar_start ]                

    def compose_common(self):

        c = self.ctx

        with IndentWrapContext(c.wrapper, 1):
            c.wrapper.verbose(f"composing '{c.test_grammar}'")

            grammars = self.compose_start() + [ c.grammar ]

            with IndentWrapContext(c.wrapper, 1):
                c.wrapper.debug(f"grammars {[str(g) for g in grammars]}")
                self.concatenate_files(c.test_grammar, grammars)
                c.wrapper.debug(f"composed")

            shutil.copy(c.test_this, c.tests_base)
            c.wrapper.verbose(f"installed {c.tests_base / c.test_this}")

            if 'compose' in self.actions:
                self.compose_action()

        return 0

    #--------------------------------------------------------------------------

    def build_action(self, ctx):
        pass

    def do_build(self, recurse=False):

        c = self.ctx

        if c.compose or c.all:
            if retcode := self.do_compose():
                return retcode

        prefix = "" # f"'{c.area}' " if c.hierarchy and not c.print_directory else ''

        c.wrapper.info(f"{prefix}build")

        with IndentWrapContext(c.wrapper, 1):
            with ChDir(c.work_base) :
                python = local['python']
                try :
                    c.wrapper.verbose(f"build {c.grammar_code}")
                    if 'build' in self.actions :
                        self.build_action()
                except commands.processes.ProcessExecutionError:
                    raise ValueError(f"{c.program} build : failed.")

            self.verbose_success("parser built")

    #--------------------------------------------------------------------------

    def test_action(self, ctx):
        pass

    def do_test(self, recurse=False):

        c = self.ctx

        if c.build or c.all:
            if retcode := self.do_build():
                return retcode

        prefix = "" # f"'{c.area}' " if c.hierarchy and not c.print_directory else ''

        c.wrapper.info(f"{prefix}test")

        with IndentWrapContext(c.wrapper, 1):
            with ChDir(c.work_base) :
                try :
                    if 'test' in self.actions:
                        self.test_action()
                    else:
                        local['pytest']()
                    self.verbose_success("all tests passed")
                except commands.processes.ProcessExecutionError:
                    raise ValueError(f"{c.program} test : failed.")

    #--------------------------------------------------------------------------

    def clean_action(self, ctx):
        return True

    def do_clean(self, recurse=False, not_exists_ok=False):

        c = self.ctx

        prefix = "" # f"'{c.area}' " if c.hierarchy and not c.print_directory else ''

        c.wrapper.info(f"{prefix}cleaning")

        with IndentWrapContext(c.wrapper, 1):
            if not c.work_base.exists():
                c.wrapper.info(f"work area '{c.work_base}' does not exist, ok.")
            else:
                if not c.work_base.is_dir():
                    raise ValueError(f"work area '{c.work_base}' "
                                     "exists but is not a directory.")
                else :                    
                    shutil.rmtree(c.work_base)
                    c.wrapper.verbose(f"removed '{c.work_base}'")

            self.remove_file(c.grammar)

            if c.parent:
                self.remove_file(c.this_grammar)
                self.remove_file(c.tokens_body)

            if 'clean' in self.actions:
                self.clean_action()

            self.verbose_success(f"cleaning done")

    #--------------------------------------------------------------------------

    def concatenate_files(self, destination, input_files):
        with open(destination, 'w') as target:
            for file_name in input_files:
                try :
                    with open(file_name, 'r') as source:
                        target.write(source.read())
                except :
                    file_path = Path.cwd() / file_name
                    raise FileNotFoundError(file_path)

    #--------------------------------------------------------------------------

    def work_base_must_not_exist(self, action):
        c = self.ctx
        if Path(c.work_base).exists():
            if not os.path.isdir(c.work_base):
                raise ValueError(f"{c.program} {action} :  Work base '{c.work_base}'"
                                 f"exists but oddly it is not a directory.  "
                                 f"Please resolve.")
            raise ValueError(f"{c.program} {action} :  Work base '{c.work_base}'"
                             f" exists.\n If you do wish to recreate it, please"
                             f" first execute 'grammar-tool clean'")

    def work_base_must_exist(self, action):
        c = self.ctx
        if not Path(c.work_base).exists():
            raise ValueError(f"{c.program} {action} :  Work base '{c.work_base}' does"
                             f" not exist.\n"
                             f"Please first execute 'grammar-tool init <style>'")

    def file_must_exist(self, action, file_name):
        c = self.ctx
        if not Path(file_name).exists():
            file_path = Path(Path.cwd(), file_name)
            raise ValueError(f"{c.program} {action} :  File does not exist,"
                             f"'{file_path}'")

    def remove_file(self, file_path):
        c = self.ctx
        try :
            Path(file_path).unlink()
            c.wrapper.debug(f"removed '{file_path}'")
        except FileNotFoundError:
            c.wrapper.debug(f"not present '{file_path}'")

    #--------------------------------------------------------------------------

    def load_lines(self, file_name):
        with open(file_name, 'r') as fp:
            return [ _ for _ in [ _.strip() for _ in fp ]
                     if _ and not _.startswith('#') ]

    #--------------------------------------------------------------------------

    def verbose_success(self, text : str):
        c = self.ctx
        if c.hierarchy:  
            # c.wrapper.verbose(f"[h] {c.verbose} : {text}")
            c.wrapper.verbose(text)
        else:
            c.wrapper.move_to(0)
            # c.wrapper.success(f"[v] {c.verbose} : {text}")
            c.wrapper.success(text)

#------------------------------------------------------------------------------
