Example peg grammars with tests

Functional
----------

  basic         Whitespace handling, used by adder and ast-adder
  adder         Simplest, parses addition of two numbers
  ast-adder     Adder extended with AST matching (ast.c)
  dc            peg's example calculator with tests

Unmaintained
------------

  basic-ok      Earlier version of basic with pass/fail
  section--OLD  Incomplete early expansion of basic-ok with operands


These require more detailed scaffolding (ast.c) than required for pegen
which build directly upon Python's AST and lists.

Note:  compose-order.gt only populated in order to be able to clean.
       i.e. 'grammar-tool clean'

