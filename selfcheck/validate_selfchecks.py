"""Maintainer script: make sure the self-check cells agree with the solutions.

For each practical that has self-checks, this script builds two copies of the
student notebook and runs them with a real Jupyter kernel:

1. "solved": every exercise cell is replaced by the code in its "Show solution"
   dropdown. Every check cell must then report "all checks passed".
2. "blank": the notebook exactly as students get it. No check cell may pass
   or crash with a traceback; each should print friendly feedback instead.

Run from the repository root:

    pip install nbclient ipykernel numpy matplotlib scipy pandas seaborn \\
        scikit-learn cartopy geopandas contextily
    python selfcheck/validate_selfchecks.py        # all practicals
    python selfcheck/validate_selfchecks.py 4 5    # just some of them
"""

import re
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notebook_solutions import is_check, solved_copy  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PRACTICALS = [int(a) for a in sys.argv[1:]] or list(range(1, 10))
PASS_TEXT = "all checks passed"


def text_of(cell):
    parts = []
    for out in cell.get("outputs", []):
        if out.get("output_type") == "stream":
            parts.append(out["text"])
        elif out.get("output_type") == "error":
            parts.append("TRACEBACK " + out["ename"] + ": " + out["evalue"])
    return "".join(parts)


def run(nb):
    NotebookClient(nb, timeout=1200, kernel_name="python3", allow_errors=True,
                   resources={"metadata": {"path": str(ROOT)}}).execute()
    return [(re.search(r"exercise(\w+)", c.source).group(1), text_of(c)) for c in nb.cells if is_check(c)]


def main():
    problems = []
    for p in PRACTICALS:
        path = ROOT / f"Practical_{p}.ipynb"
        student = nbformat.read(path, as_version=4)
        solved = solved_copy(student)
        for ex, out in run(solved):
            ok = PASS_TEXT in out and "TRACEBACK" not in out
            print(f"Practical {p} Exercise {ex} [solved]: {'PASS' if ok else 'FAIL'}")
            if not ok:
                problems.append(f"P{p} Ex{ex} solved:\n{out}")

        for ex, out in run(nbformat.read(path, as_version=4)):
            ok = PASS_TEXT not in out and "TRACEBACK" not in out and "Checking" in out
            print(f"Practical {p} Exercise {ex} [blank]:  {'gives feedback' if ok else 'PROBLEM'}")
            if not ok:
                problems.append(f"P{p} Ex{ex} blank:\n{out}")

    if problems:
        print("\n\n".join(problems))
        sys.exit(1)
    print("\nAll self-checks agree with the solutions.")


if __name__ == "__main__":
    main()
