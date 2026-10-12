"""Run the author kit's own ``merge_files()`` without its Docker launch.

``compile_submission.py`` calls ``merge_files(...)`` and then ``start_jekyll_server()`` at
import time, and the second runs the kit's Docker script, which this container cannot run
(no daemon; ``KIT_NOTES.md`` §S1.6, §S4). This helper parses the kit's file, executes only
its imports and function definitions (no module-level calls), and calls
``merge_files('submission_folder', 'tmlr_do_not_modify')`` from the kit root, exactly as
the kit's last-but-one line does. The merge copies ``submission.md`` into
``_under_review/``, rewrites every lone ``$`` to ``$$`` and copies the assets.

Run it with ``python3 -I`` (isolated: no script or working directory on ``sys.path``),
with the kit root as the only argument. Standard library only.
"""

import ast
import os
import sys


def main() -> None:
    kit_root = os.path.abspath(sys.argv[1])
    path = os.path.join(kit_root, "compile_submission.py")
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    dropped = [ast.dump(n)[:60] for n in tree.body if n not in keep
               and not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
    names = {n.name for n in keep if isinstance(n, ast.FunctionDef)}
    if "merge_files" not in names:
        sys.exit("compile_submission.py has no merge_files()")
    module = ast.Module(body=keep, type_ignores=[])
    namespace: dict = {"__name__": "kit_compile_submission"}
    exec(compile(module, path, "exec"), namespace)  # the kit's own definitions only
    os.chdir(kit_root)
    print(f"kit_merge: running the kit's merge_files(); skipped {len(dropped)} module-level "
          f"statements (the kit's own merge call and start_jekyll_server())")
    namespace["merge_files"]("submission_folder", "tmlr_do_not_modify")


if __name__ == "__main__":
    main()
