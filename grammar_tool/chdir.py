# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import os

from pathlib import Path

#------------------------------------------------------------------------------

class ChDir ( object ) :

    """
    Context manager to step into a directory temporarily.
      - On entry, caches original working directory
      - Changes to the user specified working directory
      - On exit, changes back to original working directory

      with Chdir('working/area') :
          do some work

    Lifted whole from :
       https://pythonadventures.wordpress.com/2013/12/15/chdir-a-context-manager-for-switching-working-directories/

    Resolve paths to improve error reporting.
    """

    __slots__ = ( 'origin', 'target' )

    def __init__(self, path):
        self.origin = str(Path(os.getcwd()).resolve())
        self.target = str(Path(path).resolve())

    def __enter__(self):
        os.chdir(self.target)

    def __exit__(self, *args):
        os.chdir(self.origin)

#------------------------------------------------------------------------------
