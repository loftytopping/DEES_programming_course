"""Maintainer script: make sure the self-check cells agree with solutions/.

For each practical that has self-checks, this script builds two copies of the
student notebook and runs them with a real Jupyter kernel:

1. "solved": every exercise cell is replaced by the matching cell from
   solutions/. Every check cell must then report "all checks passed".
2. "blank": the notebook exactly as students get it. No check cell may pass
   or crash with a traceback; each should print friendly feedback instead.

Run from the repository root:

    pip install nbclient ipykernel numpy matplotlib
    python selfcheck/validate_selfchecks.py
"""

import difflib
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
PRACTICALS = [1, 2, 3]
PASS_TEXT = "all checks passed"


def text_of(cell):
    parts = []
    for out in cell.get("outputs", []):
        if out.get("output_type") == "stream":
            parts.append(out["text"])
        elif out.get("output_type") == "error":
            parts.append("TRACEBACK " + out["ename"] + ": " + out["evalue"])
    return "".join(parts)


def is_check(cell):
    return cell.cell_type == "code" and cell.source.lstrip().startswith("# Check your answer")


def exercise_cells(nb):
    """Indices of the exercise cells, i.e. the code cell just above each check cell."""
    return [i - 1 for i, c in enumerate(nb.cells) if is_check(c)]


def solution_cells(student, solution):
    """Pair each exercise cell with the most similar code cell in the solution notebook."""
    pairs = []
    candidates = [c for c in solution.cells if c.cell_type == "code"]
    for i in exercise_cells(student):
        best = max(candidates, key=lambda c: difflib.SequenceMatcher(
            None, student.cells[i].source, c.source).ratio())
        pairs.append((i, best.source))
    return pairs


def run(nb):
    NotebookClient(nb, timeout=300, kernel_name="python3", allow_errors=True,
                   resources={"metadata": {"path": str(ROOT)}}).execute()
    return [(n + 1, text_of(c)) for n, c in enumerate([c for c in nb.cells if is_check(c)])]


def main():
    problems = []
    for p in PRACTICALS:
        path = ROOT / f"Practical_{p}.ipynb"
        student = nbformat.read(path, as_version=4)
        solution = nbformat.read(ROOT / "solutions" / path.name, as_version=4)

        solved = nbformat.read(path, as_version=4)
        for i, src in solution_cells(student, solution):
            solved.cells[i].source = src
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
    print("\nAll self-checks agree with solutions/.")


if __name__ == "__main__":
    main()
