# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

"""
Grammar Tool implementation Lark, https://github.com/lark-parser/lark.

Report bugs as issues at https://github.com/philip-h-dye/grammar-tool.
"""

import os

from grammar_tool.generator.common import GrammarToolCommon

from plumbum import local

class GrammarTool(GrammarToolCommon):

    def start_action(self, fp, rule_name):

        # two strings as f-string does not permit backlashes
        line = f'start <- < {rule_name} > !. ' '{ printf("%s\\n", yytext); }\n'

        print(line, file=fp)


    def build_action(self):

        python = local['python']
        
        argv = [ '-m', 'lark.tools.standalone',
                 os.path.basename(self.ctx.test_grammar) ]
        
        ( python[argv] > str(self.ctx.grammar_code) ) (retcode = 0)

#------------------------------------------------------------------------------
