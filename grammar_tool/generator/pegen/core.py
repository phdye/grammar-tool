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

        print(f"start : a={rule_name}+ NEWLINE* DEDENT* ENDMARKER {{ a }}\n",
              file=fp)

    def build_action(self):

        # (local['python'])[ '-m', 'pegen',
        #                    os.path.basename(self.ctx.test_grammar),
        #                    '-o', self.grammar_code ] (retcode = 0)

        python = local['python']
        
        argv = [ '-m', 'pegen',
                 os.path.basename(self.ctx.test_grammar),
                 '-o', self.ctx.grammar_code ]
        
        python[argv] (retcode = 0)

#------------------------------------------------------------------------------
