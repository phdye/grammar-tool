## Grammar composition and testing tool
  
Grammar Parser Generators
-------------------------
  - ✓ pegen     -- Based on python's own PEG parser generator
  - ✓ peg       -- Ian Piumarta's peg - PEG recursive-descent parser generators for C
  - _ leg       -- Ian Piumarta's leg - 'peg' with closer to full lex/yacc syntax
  - ✓ Lark      -- Fastest python parser generator
  - ✓ ANTLR4
  - _ TatSu
  - _ Arpeggio
  - _ Parsimonious
  - _ Ply       -- David Beazley’s awesome PLY
  - _ rPly      -- Rewrite of PLY with public API
  - _ Sly       -- David Beazley revisit with clean/modern syntax, OOP
  
I hope you enjoy this tool and don't hesitate to reach out to me by email:
phdye@acm.org or just open an issue / open a PR if you see any opportunity
for improvements.  Additional parser generators can typically be added in an
hour two. I will detail the necessary changes in New Parser Generator HOWTO.md

### How to install and run it

```
$ git clone git@github.com:philip-h-dye/grammar-tool.git
$ cd grammar-tool
$ python3.10 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

# or in one command
$ make setup

# ... usage ...

```

------------------------------------------------------------------------------------

### Running the tests and other tools

```
(venv) $ pytest
# or
(venv) $ make cov

# run flake8 and mypy
(venv) $ make lint
(venv) $ make typing
```

### Ian Piumarta's peg/leg - recursive-descent parser generators for C

...

### Python Arpeggio

...

