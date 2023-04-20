G_TEST = grammar-test.peg
G_TERMINATE = test.peg
GRAMMAR = grammar.peg
RECIPE = g-recipe
PARTS := $(shell cat ${RECIPE} )

PYCACHE = __pycache__ .pytest_cache

PARSER = parse/parser

.SUFFIXES:

.PHONY: all clean

all: parse/parser parse/parser_debug


clean:
	rm -rf ${G_TEST} ${GRAMMAR} parse ${PYCACHE}


parse:
	mkdir parse

parse/parser.c: ${G_TEST} | parse
	peg $^ > $@

parse/parser: main.c | parse/parser.c
	$(CC) -O3 -o $@ $^

parse/parser_debug: main.c
	$(CC) -O3 -o $@ $^ -DYY_DEBUG


${G_TEST} : ${G_TERMINATE} ${GRAMMAR}
	cat $^ > $@

${GRAMMAR} : ${PARTS}
	cat $^ > $@

test: ${PARSER}
	pytest
