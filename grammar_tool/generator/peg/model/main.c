#include <stdio.h>

FILE* input = NULL;
static int lineno = 0;
static char* filename = NULL;

#define YY_CTX_LOCAL

#define YY_INPUT(ctx, buf, result, max) {      \
    int c = getc(input);                       \
    if (c == '\n') ++lineno;                   \
    result = (EOF == c) ? 0 : (*(buf) = c, 1); \
}

#include "parse/parser.c"

void yyerror(yycontext* ctx, char* message) {
    fprintf(stderr, "%s:%d: %s", filename, lineno, message);

    if (ctx->__pos < ctx->__limit || !feof(input)) {
        // Find the offending line.
        int pos = ctx->__limit;
        while (ctx->__pos < pos) {
	        if (ctx->__buf[pos] == '\n') {
	            ++pos;
	            break;
	        }

	        --pos;
        }

        ctx->__buf[ctx->__limit] = '\0';
        fprintf(stderr, "%s", ctx->__buf + pos);
    }

    fprintf(stderr, "\n");
}

int main() {
    input = stdin;
    lineno = 1;
    filename = "<stdin>";

    yycontext ctx;
    memset(&ctx, 0, sizeof(yycontext));
    if (yyparse(&ctx) == 0) {
        yyerror(&ctx, "syntax error\n");
        return 1;
    }

    return 0;
}
