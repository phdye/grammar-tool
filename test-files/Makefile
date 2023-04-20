# GENERATORS  = $(shell grep -v '^#' compose-order.gt)
GENERATORS  = antlr4 lark peg pegen

ACTIONS     = init compose build test clean

.PHONY: ${ACTIONS} ${GENERATORS}

all: test

list gen generators :
	@ echo ${GENERATORS}

${ACTIONS} :
	@ for style in ${GENERATORS} ; do \
        export GT_ACTION=$@ ; \
        make $${style} ; \
        echo ; \
      done

# @ ( set -x && export GT_STYLE=$@ && cd $@ && make $${GT_ACTION} 2>&1 )
${GENERATORS} :
	@ ( export GT_STYLE=$@ && cd $@ && make $${GT_ACTION} 2>&1 )
	@ echo

