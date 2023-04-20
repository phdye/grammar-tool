## Grammar composition and testing tool

TODO
----

  ✓ Support parse failure tests with exceptions, primarily for ast
    ✓ antlr4 -- text
    ✓ lark   -- ast
    ✓ peg    -- retcode
    ✓ pegen  -- ast
  
  ✓ Extract common code from various `grammar_tool/generator/<style>.py`
      ✓ Create `grammar_tool/generator/common.py`
      ✓ Reduce `grammar_tool/generator/<style>.py` to strictly `<style>` specifics

  ✓ Consolidate per style under `grammar_tool/generator`
      ✓ For each style (i.e. supported parser generator) :
        ✓ Create `grammar\_tool/generator/<style>` for each style
        ✓ Move `grammar\_tool/generator/<style>.py` to `grammar\_tool/generator/<style>/core.py`
        ✓ Move `grammar\_tool/model/<style>` to `grammar\_tool/generator/<style>/model`
        ✓ Update `grammar\_tool/generator/common.py` to use `grammar\_tool/generator/<style>/model`

::: snapshot `~/archive/grammar-tool/2023-04-13.00-14.before-config.tar.z`

  ✓ Move static configuration strings to `grammar\_tool/config.yaml`
    ✓ create `grammar\_tool/config.yaml` from static strings in `s/core.py`
    ✓ config file, layered :
      ✓ `$HOME/.grammar-tool.yaml`
      ✓ `$HOME/.config/grammar-tool.yaml`
      ✓ `$HOME/config/grammar-tool.yaml`
      ✓ `/usr/share/grammar-tool/config.yaml`
      - `<grammar-tool-package>/generator/<style.name>/config.yaml`
        - `<style>` isn't available when the configuration is being loaded
        - well, yes it is from the command line arguments or `STYLE\_DEFAULT`
      ✓ `<grammar-tool-package>/config.yaml`
    ✓ create `grammar\_tool/config.py` to load attributes from the config file(s)
    ✓ `GtConfig(UserDict)` provides configuration elements as attributes
    ✓ refactor `s/core.py` and `s/generator/common.py`
    ✓ excise static configuration strings from `s/core.py`

  ✓ Move 'model' pattern to configuration f-string
    ✓ In `s/generator/common.py` :
        `module_base` = `Path(__file__).parent`
        `model\_base` = `os.path.relpath(module\_base / self.ctx.style.name / 'model', '.')`
    ✓ `model\_style\_base` = `{base}/{style.name}/model`

  ✓ test-files hierarchy -- added Makefiles to build, test, clean, etc.
    ✓ `test-files/Makefile`
    ✓ `test-files/<style>/Makefile`
    - However, grammar-tool could handle such itself :
      - add container directory type:
        - has compose-order.gt with neither {start,this}.peg
        - container level :
          - carries actions to components
          - nothing otherwise

::: snapshot `~/archive/grammar-tool/2023-04-13.22-40.config+model.tar.z`

  ✓ Split `tests/parser.py` into common and generator specific code
  
    ✓ Common code to `s/generator/common/<which>.py` `Common\_Test\_Parser`
    
      ✓ ast      -- OK/FAIL/ast/exception
        ✓ `Test\_Parser\_AST`
        ✓ support exceptions
        X `FAIL`, `DITTO`, `Without` -- NOT APPLICABLE thus far
        * match structure ?
          ✓ rudimentary proof of concept done
          * haven't yet come up with a necessary use case not handled by ast
          
      ✓ text     -- OK/FAIL/text
        ✓ `Test\_Parser\_Text`
        ✓ support exceptions
          : ANTLR4, not relevant as a syntax error exits with code 0
            with details report to as:
            ```
                $ echo a | PYTHONPATH=.:work work/main.py
                [STDERR]
                line 1:0 token recognition error at: 'a'
                line 1:1 token recognition error at: '\n'
                line 2:0 missing SIGNED\_NUMBER at '<EOF>'
                [STDOUT]
                (start (num <missing <INVALID>>))
            ```
        ✓ FAIL, DITTO, Without
        * support compiled regex ?
        
      ✓ retcode  -- OK/FAIL/text and by parser exit code
        ✓ `Test\_Parser\_RetCode`
        ✓ support exceptions
        ✓ `FAIL`, `DITTO`, `Without` - work beautifully
        * support compiled regex ?
        
    ✓ Reduce `s/generator/<style>/model/tests/parser.py`
      ✓ antlr4  -- text
      ✓ lark    -- ast
      ✓ peg     -- retcode
      ✓ pegen   -- ast

  ✓ FIXME:  'parse\_value' => 'parse\_and\_verify'
    : In `s/generator/parser`
      ✓ common
      ✓ ast
      ✓ text
      ✓ retcode
    : In `s/generator/<style>/parser.py`
      ✓ antlr4
      ✓ lark
      ✓ peg
      ✓ pegen

::: snapshot ~/archive/grammar-tool/2023-04-16.22-52.parse-n-verify.tar.z

  - git

  - Reduce default output
    - add levels of output
    - Use logger instead of print(), levels :
      00 : NOTSET :
      - verbosity 0 - 9 and oddly numerical inverse of log level.
        - Name     = lvl : verbosity :
        - CRITICAL = 50  :    0      :  Fatal error
        - ERROR    = 40  :    2      :  Something not working, continuing
        - SUCCESS  = 35  :    3      :  Confirmation of successes / DEFAULT
        - WARNING  = 30  :    4      :  
        - NOTICE   = 25  :    5      :  
        - INFO     = 20  :    6      :  
        - VERBOSE  = 15  :    7      :  
        - DEBUG    = 10  :    8      :  Necessary debugging details
        - SPAM     =  5  :    9      :  Even greater detail
        - NOTSET   = 0   :           :  nothing prints
      - warning
      - error

  ✓ ChDir.py => chdir.py

  - CHANGE 'style' to be 'generator'

  - Exception cleanup
    - Eliminate stack traces for manually raised exceptions
      - manually raised exceptions should include some state info (i.e. missing file)
        OR may require high verbosity to identify activity.
      - Exceptions caught thus far :
        ✓ `FileNotFoundError` -- maybe, but message weak unless tweaked
        - ...
      - Create custom exceptions to facilitate better error reporting

  - wrapper - Subsequent lines, indent by 1 column

DOCUMENT
--------
  - usage -- all Markdown and Jupyter Notebooks
  - add doc strings to every module, function, class and method
  - every config parameter
  - every non-trivial constant

