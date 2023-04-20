from io import StringIO

from typing import Any

from grammar_tool.generator.parser.retcode import *

from plumbum import local, BG

class Test_Parser(Test_Parser_Retcode):

    def parse(self, value : str, verbose : int = 0 ) -> Any :
        bg = ( local['parse/parser'] << value ) & BG
        bg.wait()
        return bg

