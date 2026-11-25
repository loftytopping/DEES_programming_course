"""Maintainer helpers: read the solutions that live inside the practical notebooks.

Each exercise in a practical notebook is followed by its "Check your answer" cell
and then by a markdown cell tagged ``solution``. That cell holds a collapsible
dropdown, which students open by clicking "Show solution":

    <details>
    <summary><b>Show solution to Exercise 1</b> (have a go yourself first!)</summary>

    ```python
    ...the complete, working exercise cell...
    ```

    </details>

The code block is the whole exercise cell as it should look once it is solved, so
the helpers below can paste it back into the exercise cell and run the notebook.
``run_solutions.py`` (used by GitHub Actions) and ``validate_selfchecks.py`` both
rely on this.
"""

import re

SOLUTION_TAG = "solution"
CODE_BLOCK = re.compile(r"```python\n(.*?)\n```", re.DOTALL)


def is_check(cell):
    return cell.cell_type == "code" and cell.source.lstrip().startswith("# Check your answer")


def is_solution(cell):
    return cell.cell_type == "markdown" and SOLUTION_TAG in cell.metadata.get("tags", [])


def solution_code(cell):
    """The Python code inside one solution dropdown cell."""
    match = CODE_BLOCK.search(cell.source)
    if match is None:
        raise ValueError("Solution cell has no ```python code block:\n" + cell.source)
    return match.group(1)


def solution_markdown(code, label):
    """Build the markdown for a solution dropdown cell."""
    if "```" in code:
        raise ValueError("Solution code contains ``` and cannot go inside a code block")
    return (
        "<details>\n"
        f"<summary><b>Show solution to {label}</b> (have a go yourself first!)</summary>\n"
        "\n"
        "```python\n"
        f"{code.rstrip()}\n"
        "```\n"
        "\n"
        "</details>"
    )


def exercise_for(nb, k):
    """Index of the exercise cell that the solution cell at index k belongs to.

    The exercise is the nearest code cell above the solution that is not a
    "Check your answer" cell.
    """
    i = k - 1
    while i >= 0 and (nb.cells[i].cell_type != "code" or is_check(nb.cells[i])):
        i -= 1
    if i < 0:
        raise ValueError(f"Solution cell {k} has no exercise cell above it")
    return i


def solution_pairs(nb):
    """List of (exercise cell index, solution code) for every solution dropdown."""
    return [(exercise_for(nb, k), solution_code(c)) for k, c in enumerate(nb.cells) if is_solution(c)]


def solved_copy(nb):
    """Copy of the notebook with each exercise cell replaced by its solution.

    The solution dropdowns themselves are left in place; they are markdown, so
    they do not run.
    """
    import copy

    solved = copy.deepcopy(nb)
    for i, code in solution_pairs(nb):
        solved.cells[i].source = code
    return solved
