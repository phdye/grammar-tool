import unittest

from plumbum import local, commands

parser = local['parse/parser']

class Test_Parser(unittest.TestCase):

    def parse_value(self, value, expected_return):
        try :
            (parser << value)(retcode = expected_return)
        except commands.processes.ProcessExecutionError:
            self.assertFalse(f"ProcessExecutionError for value '{value}',"
                             f" expected return {expected_return} !")
