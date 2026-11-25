# Self-checks for the practicals

This folder gives students instant feedback in Practicals 1-9. Each practical
notebook has a setup cell near the top (`from selfcheck import practicalN as check`)
and a **Check your answer** cell after every `INSERT CODE HERE` exercise that calls
`check.exerciseK()`. The checks are formative only: nothing is marked or recorded.

- `_core.py` holds the shared helpers (friendly pass/fail messages, comparing numbers
  and arrays, re-running print-only exercise cells to read their output).
- `practical1.py` to `practical9.py` hold one function per exercise, including
  hints for common mistakes. Exercises that only print or plot are checked by
  quietly re-running the exercise cell and looking at its output or figure.
- On Google Colab the setup cell downloads these files from the `master` branch if
  the folder is not next to the notebook.

## Solutions inside the notebooks

Each exercise is followed by its check cell and then a markdown cell tagged
`solution` holding a collapsible **Show solution** dropdown (`<details>` HTML with a
Python code block). The code block is the complete exercise cell once solved, so the
scripts below can paste it into the exercise cell and run the notebook. To change a
solution, edit the code inside the dropdown. Practicals not yet converted still use
`solutions/`, and `convert_to_dropdowns.py N` moves Practical N's answers across.

- `notebook_solutions.py`: shared helpers for reading the dropdowns.
- `run_solutions.py`: runs every practical with its solutions filled in and fails if
  any cell errors or any check does not pass. GitHub Actions runs this.

    python selfcheck/run_solutions.py        # all practicals
    python selfcheck/run_solutions.py 1      # just Practical 1

## Validating the checks

To confirm the checks still agree with the solutions after changing an exercise:

    pip install nbclient ipykernel numpy matplotlib scipy pandas seaborn \
        scikit-learn cartopy geopandas contextily
    python selfcheck/validate_selfchecks.py        # all practicals
    python selfcheck/validate_selfchecks.py 4 5    # just some of them

It runs each practical twice with a real kernel: once with the solution code dropped
into every exercise cell (all checks must pass) and once as students receive it (no
check may pass or show a traceback).
