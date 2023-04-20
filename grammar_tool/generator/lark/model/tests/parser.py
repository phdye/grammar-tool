from grammar_tool.generator.parser.ast import ( Test_Parser_AST,
                                                create_test_class,
                                                create_no_test_class,
                                              )

import grammar

class Test_Parser(Test_Parser_AST):

    def parse(self, value, verbose=0):
        return grammar.Lark_StandAlone().parse(value)

