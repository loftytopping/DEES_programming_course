"""Maintainer script: make sure the self-check cells agree with solutions/.

For each practical that has self-checks, this script builds two copies of the
student notebook and runs them with a real Jupyter kernel:

1. "solved": every exercise cell is replaced by the matching cell from
   solutions/. Every check cell must then report "all checks passed".
2. "blank": the notebook exactly as students get it. No check cell may pass
   or crash with a traceback; each should print friendly feedback instead.

Run from the repository root:

    pip install nbclient ipykernel numpy matplotlib scipy pandas seaborn \\
        scikit-learn cartopy geopandas contextily
    python selfcheck/validate_selfchecks.py        # all practicals
    python selfcheck/validate_selfchecks.py 4 5    # just some of them
"""

import difflib
import re
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

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


def is_check(cell):
    return cell.cell_type == "code" and cell.source.lstrip().startswith("# Check your answer")


def exercise_cells(nb):
    """Indices of the exercise cells, i.e. the code cell just above each check cell."""
    return [i - 1 for i, c in enumerate(nb.cells) if is_check(c)]


def solution_cells(student, solution):
    """Pair each exercise cell with its cell in the solution notebook.

    First we look for the markdown cell just above the exercise (the task
    text) in the solution notebook and take the code cell in the same position
    after it. If the text differs, we fall back to the most similar code cell
    that comes after the previous match.
    """
    pairs = []
    last = -1
    for i in exercise_cells(student):
        m = i - 1
        while m >= 0 and student.cells[m].cell_type != "markdown":
            m -= 1
        nth = sum(1 for c in student.cells[m + 1:i] if c.cell_type == "code" and not is_check(c))
        j = None
        for k, c in enumerate(solution.cells):
            if k > last and c.cell_type == "markdown" and c.source.strip() == student.cells[m].source.strip():
                codes = [n for n in range(k + 1, len(solution.cells)) if solution.cells[n].cell_type == "code"]
                if len(codes) > nth:
                    j = codes[nth]
                break
        if j is None:
            later = [n for n, c in enumerate(solution.cells) if n > last and c.cell_type == "code"]
            j = max(later, key=lambda n: difflib.SequenceMatcher(
                None, student.cells[i].source, solution.cells[n].source).ratio())
        pairs.append((i, solution.cells[j].source))
        last = j
    return pairs


def run(nb):
    NotebookClient(nb, timeout=1200, kernel_name="python3", allow_errors=True,
                   resources={"metadata": {"path": str(ROOT)}}).execute()
    return [(re.search(r"exercise(\w+)", c.source).group(1), text_of(c)) for c in nb.cells if is_check(c)]


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
