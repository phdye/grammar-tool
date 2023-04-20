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
        print(f'grammar test_grammar ;\n\n'
              f'start : {rule_name} ;\n',
              file=fp)

    # java -jar /Users/jason/antlr/antlr-4.9.1-complete.jar -Dlanguage=Python3 "$@"
    # /usr/share/java/antlr4-4.7.2.jar

    # 
    # export CLASSPATH=".:${ANTLR4_JARS}:$CLASSPATH"
    # alias antlr4='      java -Xmx500M -cp "${CLASSPATH}" org.antlr.v4.Tool '
    # alias gpython='     antlr4 -Dlanguage=Python3 '

    def build_action(self):

        ANTLR4_JAR = '/usr/share/java/antlr-4.12.0-complete.jar'

        java = local['java']

        argv = [ '-Xmx500M', '-cp', f".:{ANTLR4_JAR}",
                 'org.antlr.v4.Tool', '-Dlanguage=Python3',
                 os.path.basename(self.ctx.test_grammar) ]

        ( java[argv] > str(self.ctx.grammar_code) ) (retcode = 0)

#------------------------------------------------------------------------------
