Simple
------

'simple' exists solely to test grammar-tool's output with a small
but representive hierarchy.

Examples
--------

$ **gt --style lark --all --silent test**

... *no output*


$ **gt --style lark --all --info test**


```
num                   : cleaning done
                      : populated 'work'
                      : compose complete
                      : parser built
                      : all tests passed

add                   : cleaning done
                      : populated 'work'
                      : compose complete
                      : parser built
                      : all tests passed

simple                : cleaning done
                      : populated 'work'
                      : compose complete
                      : parser built
                      : all tests passed
```

$ **gt --style lark --all --info test**

```
- 'simple' is a parent, see to it's children

  - gather children

  - process children
    - 'num'
      - cleaning
      - initialize for generator 'lark'
      - compose
      - build
      - test

    - 'add'
      - cleaning
      - initialize for generator 'lark'
      - compose
      - build
      - test

- 'simple' resume
  - cleaning
  - initialize for generator 'lark'
  - compose
  - build
  - test
                                                                                       
```

$ **gt --style lark --all --spam test**

```
- 'simple' is a parent, see to it's children

  - gather children
    - found 2 children : ['add', 'num']

  - process children
    - 'num'
      - cleaning
        - removed 'work'
        - removed 'grammar.lark'
        - cleaning done
      - initialize for generator 'lark'
        - populating 'work' from '<grammar_tool>/generator/lark/model'
        - populated 'work'
      - compose
        - gathering components
          - missing 'components.gt'
          - loading '../compose-order.gt'
          - No components applicable
        - composing grammar.lark
          - components components.gt
          - composed
        - composing 'work/tests/tokens.py'
          - No tokens, skipped 'work/tests/tokens.py'
          - composing 'work/test_grammar.lark'
            - grammars ['start.lark', 'grammar.lark']
            - composed
          - installed work/tests/test_this.py
        - compose complete
      - build
        - build grammar.py
        - parser built
      - test
        - all tests passed

    - 'add'
      - cleaning
        - removed 'work'
        - removed 'grammar.lark'
        - cleaning done
      - initialize for generator 'lark'
        - populating 'work' from '<grammar_tool>/generator/lark/model'
        - populated 'work'
      - compose
        - gathering components
          - missing 'components.gt'
          - loading '../compose-order.gt'
          - 1 components applicable
        - composing grammar.lark
          - components components.gt
          - input files ['this.lark', '../num/this.lark']
          - composed
        - composing 'work/tests/tokens.py'
          - No tokens, skipped 'work/tests/tokens.py'
          - composing 'work/test_grammar.lark'
            - grammars ['start.lark', 'grammar.lark']
            - composed
          - installed work/tests/test_this.py
        - compose complete
      - build
        - build grammar.py
        - parser built
      - test
        - all tests passed

- 'simple' resume
  - cleaning
    - removed 'work'
    - removed 'grammar.lark'
    - removed 'this.lark'
    - not present 'tokens-body.py'
    - cleaning done
  - initialize for generator 'lark'
    - populating 'work' from '<grammar_tool>/generator/lark/model'
    - populated 'work'
  - compose
    - composed 'this.lark'
      - No tokens, skipped 'work/tests/tokens.py'
      - composed grammar.lark
      - composing 'work/test_grammar.lark'
        - grammars ['start.lark', 'grammar.lark']
        - composed
      - installed work/tests/test_this.py
    - compose complete
  - build
    - build grammar.py
    - parser built
  - test
    - all tests passed
```
