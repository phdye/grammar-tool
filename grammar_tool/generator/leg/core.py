# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

"""
Grammar Tool implementation for peg, https://piumarta.com/software/peg

peg/leg — recursive-descent parser generators for C

Report bugs as issues at https://github.com/philip-h-dye/grammar-tool.
"""

import os
import shutil

from pathlib import Path

from plumbum import local, commands

from grammar_tool.generator.common import GrammarToolCommon

from plumbum import local


def _make(ctx, caller, argv, expected_return):
    try :
        (local['make'])[argv](retcode = expected_return)
    except commands.processes.ProcessExecutionError:
        raise ValueError(f"{ctx.program} {caller}:  'make {argv}' failed.")


class GrammarTool(GrammarToolCommon):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.actions.add('compose')
        self.actions.add('test')
        # 'build' action is implicit

    def compose_action(self):
        if (driver := Path("main.c")).exists():
            shutil.copy(driver, self.ctx.work_base)        
        if (ast_c := Path("ast.c")).exists():
            shutil.copy(ast_c, self.ctx.work_base)

    def start_action(self, fp, rule_name):
        print(f'start <- < {rule_name} > !. '
              '{ printf("%s\\n", yytext); }\n', # f-strings, backslash not ok
              file=fp)
        
    def build_action(self):
        _make(self.ctx, 'build', ['all'], 0)

    def test_action(self):
        _make(self.ctx, 'test', ['test'], 0)

#------------------------------------------------------------------------------
