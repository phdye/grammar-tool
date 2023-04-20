# GRAMMAR_CODE = "grammar.py"
# AST_PATCH = 'astpatch.py'

    # ast_patch_path = None
    # prefix = ctx.work_base
    # while True:
    #     path = os.path.abspath(prefix)
    #     if os.path.dirname(path) == path:
    #         raise ValueError(f"{AST_PATCH} not found in {prefix}")
    #     ast_patch_path = os.path.join(prefix, AST_PATCH)
    #     if Path(ast_patch_path).exists():
    #         wprint(f"  - found {ast_patch_path}")
    #         break
    #     prefix = os.path.join('..', prefix)
    # 
    # destination = os.path.join(ctx.work_base, 'tests')
    # shutil.copy(ast_patch_path, destination)
    # wprint(f"  - installed {AST_PATCH} in {destination}")

