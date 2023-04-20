#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys

from pathlib import Path

# top = Path(__file__).parent.parent)
# sys.path.insert(0, top)

import grammar_tool

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(grammar_tool.main())
