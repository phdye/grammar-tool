"""
Tests for grammar-tool/test-files/lark/adder/num
"""

from parser import create_test_class

import astpatch

from grammar import ( Token,
                      UnexpectedCharacters,
                      UnexpectedToken,
                    )

from astpatch import unexpected_eof

unexpected_a = UnexpectedCharacters('a', 0, 1, 1)

create_test_class( "num", [
    ['empty string' , ''            , unexpected_eof ],
    ['zero'         , '0'           , Token('SIGNED_NUMBER', '0') ],
    ['one'          , '1'           , Token('SIGNED_NUMBER', '1') ],
    ['seven'        , '7'           , Token('SIGNED_NUMBER', '7') ],
    ['15'           , '15'          , Token('SIGNED_NUMBER', '15') ],
    ['123.50'       , '123.50'      , Token('SIGNED_NUMBER', '123.50') ],
    ['a'            , 'a'           , unexpected_a ],
] )

#------------------------------------------------------------------------------

import unittest

from grammar import ConfigurationError, assert_config

# Line 49
class Test_Other(unittest.TestCase):
    def test_assert_config__ConfigurationError(self):
        options = []
        with self.assertRaises(ConfigurationError):
            assert_config(value='missing', options=[])

# Line 84-86
b_expect = UnexpectedCharacters(b'a', 0, 1, 1)  #

#------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main(["-vvv", "--cov"]))
