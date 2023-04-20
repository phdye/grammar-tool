from parser import create_test_class

import os

from token import OP

from parser import create_test_class

from tokens import UsageIntro

create_test_class( "Usage_Intro", [
    [ 'Usage COLON'            , 'Usage:'   , UsageIntro('Usage:') ],
    [ 'Usage space COLON'      , 'Usage :'  , UsageIntro('Usage:') ],
    [ 'usage COLON lowercase'  , 'usage:'   , UsageIntro('Usage:') ],
    [ 'UsAgE COLON'            , 'UsAgE:'   , UsageIntro('Usage:') ],
] )

