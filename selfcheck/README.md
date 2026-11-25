# Self-checks for the practicals

This folder gives students instant feedback in Practicals 1-3. Each practical
notebook has a setup cell near the top (`from selfcheck import practicalN as check`)
and a **Check your answer** cell after every `INSERT CODE HERE` exercise that calls
`check.exerciseK()`. The checks are formative only: nothing is marked or recorded.

- `_core.py` holds the shared helpers (friendly pass/fail messages, comparing numbers
  and arrays, re-running print-only exercise cells to read their output).
- `practical1.py`, `practical2.py`, `practical3.py` hold one function per exercise,
  including hints for common mistakes.
- On Google Colab the setup cell downloads these files from the `master` branch if
  the folder is not next to the notebook.

To confirm the checks still agree with `solutions/` after changing an exercise:

    pip install nbclient ipykernel numpy matplotlib
    python selfcheck/validate_selfchecks.py

It runs each practical twice with a real kernel: once with the solution code dropped
into every exercise cell (all checks must pass) and once as students receive it (no
check may pass or show a traceback).
