#include <stdio.h>
#include <stdlib.h>

typedef struct AST AST; // Forward reference

struct AST {
  enum {
    AST_MAIN,
    AST_NUMBER,
    AST_ADD,
    AST_MUL,
  } tag;
  union {
    struct AST_MAIN { AST *body; } AST_MAIN;
    struct AST_NUMBER { int number; } AST_NUMBER;
    struct AST_ADD { AST *left; AST *right; } AST_ADD;
    struct AST_MUL { AST *left; AST *right; } AST_MUL;
  } data;
};

AST *ast_new(AST ast)
{
  AST *ptr = malloc(sizeof(AST));
  if (ptr) *ptr = ast;
  return ptr;
}

void ast_free(AST *ptr) {
  AST ast = *ptr;
  switch (ast.tag) {
    case AST_MAIN: {
      struct AST_MAIN data = ast.data.AST_MAIN;
      ast_free(data.body);
      break;
    }
    case AST_NUMBER: {
      struct AST_NUMBER data = ast.data.AST_NUMBER;
      break;
    }
    case AST_ADD: {
      struct AST_ADD data = ast.data.AST_ADD;
      ast_free(data.left);
      ast_free(data.right);
      break;
    }
    case AST_MUL: {
      struct AST_MUL data = ast.data.AST_MUL;
      ast_free(data.left);
      ast_free(data.right);
      break;
    }
  }
  free(ptr);
}

#define AST_NEW(tag, ...) ast_new((AST){tag, {.tag=(struct tag){__VA_ARGS__}}})

void ast_print(AST *ptr)
{
  AST ast = *ptr;
  switch (ast.tag) {
    case AST_MAIN: {
      struct AST_MAIN data = ast.data.AST_MAIN;
      // printf("main() = ");
      ast_print(data.body);
      return;
    }
    case AST_NUMBER: {
      struct AST_NUMBER data = ast.data.AST_NUMBER;
      printf("%d", data.number);
      return;
    }
    case AST_ADD: {
      struct AST_ADD data = ast.data.AST_ADD;
      printf("(");
      ast_print(data.left);
      printf(" + ");
      ast_print(data.right);
      printf(")");
      return;
    }
    case AST_MUL: {
      struct AST_MUL data = ast.data.AST_MUL;
      printf("(");
      ast_print(data.left);
      printf(" * ");
      ast_print(data.right);
      printf(")");
      return;
    }
  }
}

#define emitf printf

void ast_emit(AST *ptr)
{
  AST ast = *ptr;

  switch (ast.tag) {
    case AST_MAIN: {
      struct AST_MAIN data = ast.data.AST_MAIN;
      emitf(".global _main\n");
      emitf("_main:\n"); 
      ast_emit(data.body);
      emitf("  ret\n");
      emitf("\n");
      return;
    }

    case AST_NUMBER: {
      struct AST_NUMBER data = ast.data.AST_NUMBER;
      emitf("  mov rax, %d\n", data.number);
      return;
    }

    case AST_ADD: {
      struct AST_ADD data = ast.data.AST_ADD;
      ast_emit(data.left);
      emitf("  push rax\n");
      ast_emit(data.right);
      emitf("  pop rbx\n");
      emitf("  add rax, rbx\n");
      return;
    }

    case AST_MUL: {
      struct AST_MUL data = ast.data.AST_MUL;
      ast_emit(data.left);
      emitf("  push rax\n");
      ast_emit(data.right);
      emitf("  pop rbx\n");
      emitf("  mul rbx\n");
      return;
    }
  }
}
