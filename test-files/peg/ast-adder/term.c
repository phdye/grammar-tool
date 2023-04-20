
int main() {
  // main() = 4 + 2 * 10 + 3 * (5 + 1)
  AST *term = AST_NEW(AST_MAIN,
    AST_NEW(AST_ADD,
      AST_NEW(AST_NUMBER, 4),
      AST_NEW(AST_ADD,
        AST_NEW(AST_MUL, 
          AST_NEW(AST_NUMBER, 2), 
          AST_NEW(AST_NUMBER, 10),
        ),
        AST_NEW(AST_MUL,
          AST_NEW(AST_NUMBER, 3),
          AST_NEW(AST_ADD,
            AST_NEW(AST_NUMBER, 5),
            AST_NEW(AST_NUMBER, 1),
          ),
        ),
      ),
    ),
  );
  // printf("/* ");
  ast_print(term); printf("\n");
  // printf(" */\n"); 
  // ast_emit(term);
  // ast_free(term);
}
