#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE* input = NULL;
static int lineno = 0;
static char* filename= NULL;

#define STACK_SIZE 1024
char *stack[STACK_SIZE];
int used = 0;

char* push(char * text)
{
    if (used >= STACK_SIZE) {
        fprintf(stderr,"ERROR:  push() stack overrun, already contains %d strings\n", STACK_SIZE);
        exit(1);
    }
    // printf("push:  '%s'\n", text);
    char * value = stack[used++] = strdup(text);
    // printf("push:  '%s'\n", value);
    return value;
}

char* pop(void)
{
    if (used <= 0) {
        fprintf(stderr,"ERROR:  pop() on empty stack\n");
        exit(1);
    }
    char * value = stack[--used];
    // printf("pop:   '%s'\n", value);
    return value;
}

char* gather()
{
    int bytes = 0;
    for ( int i = 0; i <= used; i++)
        bytes += strlen(stack[i]);

    char * result = (char*) malloc(bytes);
    if ( result == NULL ) {
        fprintf(stderr,"gather():  malloc(%d) failed.\n", bytes);
        exit(1);
    }

    char * insert = result;
    for ( int i = 0; i < used; i++) {
        char * value = pop();
        strcpy(insert, value);
        insert += strlen(value);
    }

    return result;
}

void print()
{
    for (int i = 0; i < used; i++)
        printf("%s", stack[i]);
    printf("\n");
}

// #include "dc.peg.c"

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
