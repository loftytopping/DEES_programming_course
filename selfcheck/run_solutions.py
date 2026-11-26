"""Run every practical with its solutions filled in, to catch broken code early.

GitHub Actions runs this on every push, pull request and once a week. For each
practical it pastes the code from every "Show solution" dropdown into the
exercise cell above it, then runs the whole notebook top to bottom with a real
Jupyter kernel. A practical fails if

- any cell raises an error (cells tagged ``raises-exception``, which show an
  error on purpose, are allowed to), or
- any "Check your answer" cell does not say "all checks passed".

Run from the repository root:

    python selfcheck/run_solutions.py        # all practicals
    python selfcheck/run_solutions.py 1 5    # just some of them
"""

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notebook_solutions import is_check, is_solution, solved_copy  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PRACTICALS = [int(a) for a in sys.argv[1:]] or list(range(1, 10))
PASS_TEXT = "all checks passed"


def stream_text(cell):
    return "".join(o.get("text", "") for o in cell.get("outputs", []) if o.get("output_type") == "stream")


def run_practical(p):
    """Return a list of problems (empty if the practical is fine)."""
    path = ROOT / f"Practical_{p}.ipynb"
    nb = nbformat.read(path, as_version=4)
    source = path.name
    if not any(is_solution(c) for c in nb.cells):
        return [f"{source}: has no 'Show solution' dropdowns to test"]
    nb = solved_copy(nb)
    print(f"Running {source} ...", flush=True)

    client = NotebookClient(nb, timeout=900, kernel_name="python3",
                            resources={"metadata": {"path": str(ROOT)}})
    try:
        client.execute()
    except CellExecutionError as err:
        return [f"{source}: a cell raised an error\n{err}"]

    problems = []
    for n, cell in enumerate(nb.cells):
        if is_check(cell) and PASS_TEXT not in stream_text(cell):
            problems.append(f"{source}: check cell {n} did not pass with the solution code\n"
                            f"{cell.source}\n{stream_text(cell)}")
    return problems


def main():
    failed = {}
    for p in PRACTICALS:
        problems = run_practical(p)
        print(f"Practical {p}: {'PASS' if not problems else 'FAIL'}", flush=True)
        if problems:
            failed[p] = problems
            for problem in problems:
                print(f"::error file=Practical_{p}.ipynb::{problem.splitlines()[0]}")
                print(problem)

    if failed:
        print("Failed practicals:", ", ".join(str(p) for p in failed))
        sys.exit(1)
    print("All practicals ran with their solutions.")


if __name__ == "__main__":
    main()
