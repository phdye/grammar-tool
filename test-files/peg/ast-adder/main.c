#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ast.c"

#define STACK_SIZE 1024
AST * stack[STACK_SIZE];
int used = 0;

AST* pop(void)
{
    if (used <= 0) {
        fprintf(stderr,"ERROR:  pop() on empty stack\n");
        exit(1);
    }
    AST * value = stack[--used];
    stack[used+1] = NULL;
    return value;
}

AST* push(AST * node)
{
    if (used >= STACK_SIZE) {
        fprintf(stderr,"ERROR:  push() stack overrun, already contains %d nodes\n", STACK_SIZE);
        exit(1);
    }
    AST * value = stack[used++] = node;
    // printf("{ push(<value>) :\n  [value]\n  ");
    // ast_print(value); printf("\n");
    // printf("  [stack]\n  ");
    // ast_print(stack[used-1]); printf("\n");
    // printf("}\n");
    
    return value;
}

#include "parse/parser.c"

int main()
{
  while (yyparse());

  return 0;
}

