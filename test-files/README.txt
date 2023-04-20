Example grammars for each grammar parser supported by grammar-tool

Note:  compose-order.gt only populated in order to be able to clean.
       i.e. 'x/wipe'

And later, a Makefile was added here and in each style to support
each of the grammar-tool actions.
  - init
  - compose
  - build
  - test
  - clean


Build and test everything :
  $ make

Build and test just antlr4 :
  $ make antlr4

Clean just antlr4 :
  $ GT_ACTION=clean make antlr4

Build and test just pegen with verbosity level 3 :
  $ GT_OPT="-v 3" make antlr4

