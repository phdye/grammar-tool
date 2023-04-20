GRAMMAR = test_grammar.peg

CLEAN = parse .pytest_cache tests/__pycache__ *~

PARSER = parse/parser

.SUFFIXES:

.PHONY: all clean

all: parse/parser parse/debug-parser

parse:
	mkdir parse

parse/parser.c: ${GRAMMAR} | parse
	peg $^ > $@

parse/parser: main.c | parse/parser.c
	$(CC) -O3 -o $@ $^

parse/debug-parser: main.c
	$(CC) -O3 -o $@ $^ -DYY_DEBUG

test: ${PARSER}
	pytest

clean:
	rm -rf ${CLEAN}
