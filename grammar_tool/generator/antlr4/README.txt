ANTLR4 -- exception support not found applicable yet.

Using the simple driver work/main.py, syntax errors are reported to STDERR and STDERR

    $ echo a | PYTHONPATH=.:work work/main.py
    [STDERR]
    line 1:0 token recognition error at: 'a'
    line 1:1 token recognition error at: '\n'
    line 2:0 missing SIGNED_NUMBER at '<EOF>'
    [STDOUT]
    (start (num <missing <INVALID>>))

Within s/generator/antlr4/model/tests/parser.py:
  - the stderr output occurs
  - the stdout above it returned to the caller of parse_value().

  This is quite sufficient to test for parse failures.

