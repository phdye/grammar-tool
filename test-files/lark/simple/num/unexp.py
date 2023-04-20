#!/usr/bin/env python

from prettyprinter import cpprint as pp
import yaml

import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'grammar')

from grammar import UnexpectedCharacters

pp( yaml.dump(UnexpectedCharacters) )
pp( vars(UnexpectedCharacters) )
    
a_expect_1 = UnexpectedCharacters('a', 0, 1, 1)
a_expect_2 = UnexpectedCharacters('a', 0, 1, 2)

pp( str(a_expect_1) )
pp( repr(a_expect_1) )
print()
pp( str(a_expect_2) )
pp( repr(a_expect_2) )
print()

pp( a_expect_1 == a_expect_2 )
print()
