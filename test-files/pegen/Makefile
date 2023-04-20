ACTIONS = init compose build test clean

.PHONY: ${ACTIONS}

all: test

# @ for style in $(shell grep -v '^#' compose-order.gt) ; do \

${ACTIONS} :
	@ for grammar in adder ; do \
		(   cd $${grammar} \
        &&  export PYTHONPATH=.:tool:../tool \
        &&  tool/scripts/grammar-tool --all ${GT_OPT} --style $${GT_STYLE} $@ 2>&1 \
        ) ; \
        echo ; \
      done

