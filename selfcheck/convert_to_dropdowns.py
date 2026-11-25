"""One-off maintainer script: move answers from solutions/ into "Show solution" dropdowns.

For each practical given, every exercise cell (a code cell with INSERT CODE HERE)
is paired with its solved version in solutions/. A markdown cell tagged
``solution`` holding that code in a collapsible dropdown is then added after the
exercise (after its "Check your answer" cell, if it has one).

    python selfcheck/convert_to_dropdowns.py 1          # convert Practical 1
    python selfcheck/convert_to_dropdowns.py --dry-run 2 # show the pairing only

Once every practical has been converted and solutions/ removed, this script can
be deleted.
"""

import difflib
import re
import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notebook_solutions import SOLUTION_TAG, is_check, is_solution, solution_markdown  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def is_exercise(cell):
    return cell.cell_type == "code" and "INSERT CODE" in cell.source.upper()


def key(cell):
    return cell.cell_type + ":" + cell.source.strip()


def pair_exercises(student, solution):
    """Map student exercise cell index -> solved code, by aligning the two notebooks."""
    a = [key(c) for c in student.cells]
    b = [key(c) for c in solution.cells]
    pairs, unmatched = {}, []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        sol_codes = [j for j in range(j1, j2) if solution.cells[j].cell_type == "code"]
        for i in range(i1, i2):
            if not is_exercise(student.cells[i]):
                continue
            if not sol_codes:
                unmatched.append(i)
                continue
            best = max(sol_codes, key=lambda j: difflib.SequenceMatcher(
                None, student.cells[i].source, solution.cells[j].source).ratio())
            pairs[i] = solution.cells[best].source
            sol_codes.remove(best)
    return pairs, unmatched


def exercise_label(student, i, fallback):
    """'Exercise 3' etc, taken from the check cell or the nearest heading above."""
    if i + 1 < len(student.cells) and is_check(student.cells[i + 1]):
        m = re.search(r"exercise(\w+)\(", student.cells[i + 1].source)
        if m:
            return "Exercise " + m.group(1)
    for k in range(i - 1, -1, -1):
        if student.cells[k].cell_type == "markdown":
            m = re.search(r"Exercise\s+(\w+)", student.cells[k].source)
            if m:
                return "Exercise " + m.group(1)
    return fallback


def convert(p, dry_run=False):
    path = ROOT / f"Practical_{p}.ipynb"
    student = nbformat.read(path, as_version=4)
    if any(is_solution(c) for c in student.cells):
        print(f"Practical {p} already has solution dropdowns, skipping")
        return
    solution = nbformat.read(ROOT / "solutions" / path.name, as_version=4)
    pairs, unmatched = pair_exercises(student, solution)

    for i in sorted(pairs, reverse=True):
        label = exercise_label(student, i, "this exercise")
        at = i + 2 if i + 1 < len(student.cells) and is_check(student.cells[i + 1]) else i + 1
        print(f"Practical {p}: cell {i} -> {label}, dropdown at {at}")
        cell = nbformat.v4.new_markdown_cell(solution_markdown(pairs[i], label))
        cell.metadata["tags"] = [SOLUTION_TAG]
        if student.nbformat_minor < 5:
            del cell["id"]  # cell ids only exist from nbformat 4.5
        student.cells.insert(at, cell)
    for i in unmatched:
        print(f"Practical {p}: WARNING no solution found for exercise cell {i}")

    if not dry_run:
        nbformat.write(student, path)


if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry-run" in args
    for a in args:
        if a != "--dry-run":
            convert(int(a), dry)
