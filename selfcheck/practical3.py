"""Self-checks for Practical 3: modules, functions and NumPy."""

from ._core import HINT, Checker, lines_of, np, source_of


def _grid(n):
    """Expected z for z = x + y*x where x is the row number and y the column number (from 1)."""
    v = np.arange(1, n + 1, dtype=float)
    return v[:, None] + v[None, :] * v[:, None]


def _rc(i):
    return f"row {i[0]}, column {i[1]}"


def exercise1():
    """Exercise 1: a 5x6 array, 2.5 in the first two rows and 5.5 below."""
    expected = np.full((5, 6), 5.5)
    expected[:2, :] = 2.5
    with Checker("Practical 3, Exercise 1") as c:
        m = c.need("practice_matrix")
        c.sequence("practice_matrix", m, expected, describe_index=_rc, hints=[
            (np.zeros((5, 6)), "The array is still all zeros. Use slicing such as practice_matrix[0:2, :] = 2.5"),
            (np.where(np.arange(5)[:, None] < 3, 2.5, 5.5) * np.ones((5, 6)),
             "Three rows have 2.5. Remember 0:2 means rows 0 and 1 only."),
        ])


def exercise2():
    """Exercise 2: fill x and y with 1..100, then z[row, column] with a nested loop."""
    with Checker("Practical 3, Exercise 2") as c:
        values = np.arange(1, 101)
        c.sequence("x", c.need("x"), values, describe_index=lambda i: f"x[{i[0]}]",
                   hints=[(np.zeros(100), "x is still all zeros. Use a loop: x[step] = step + 1")])
        c.sequence("y", c.need("y"), values, describe_index=lambda i: f"y[{i[0]}]",
                   hints=[(np.zeros(100), "y is still all zeros. Fill it in the same loop as x.")])
        c.sequence("z", c.need("z"), _grid(100), describe_index=_rc, hints=[
            (np.zeros((100, 100)), "z is still all zeros. Inside the inner loop set z[row, column] = ..."),
            (_grid(100).T, "Rows and columns are swapped. x goes with row and y goes with column."),
        ])


def exercise3():
    """Exercise 3: call test() 30 times with a for loop."""
    sentence = "All work and no play makes Jack a dull boy"
    with Checker("Practical 3, Exercise 3") as c:
        printed = lines_of(c.output_of_exercise_cell(["test()", "def test"]))
        count = printed.count(sentence)
        if count == 30:
            c.ok("The sentence is printed exactly 30 times")
        elif count == 0:
            c.fail("The sentence is not printed at all.",
                   "Defining a function does not run it. Call it with test() inside a for loop.")
        else:
            c.fail(f"The sentence is printed {count} times, but it should be 30.",
                   "range(30) gives 30 steps.")


def exercise4():
    """Exercise 4: put the nested loop inside a function create_z(x, y, z)."""
    with Checker("Practical 3, Exercise 4") as c:
        values = np.arange(1, 301)
        c.sequence("x", c.need("x"), values, describe_index=lambda i: f"x[{i[0]}]",
                   hints=[(np.zeros(300), "x is still all zeros. Note this time there are 300 values.")])
        c.sequence("y", c.need("y"), values, describe_index=lambda i: f"y[{i[0]}]",
                   hints=[(np.zeros(300), "y is still all zeros. Note this time there are 300 values.")])
        c.check(callable(c.ns.get("create_z")), "`create_z` is a function",
                "I can't find a function called `create_z`.")
        c.sequence("z", c.need("z"), _grid(300), describe_index=_rc, hints=[
            (np.zeros((300, 300)), "z is still all zeros. Put the nested loop inside create_z, "
                                   "before `return z`, and loop over 300 rows and columns."),
            (_grid(300).T, "Rows and columns are swapped. x goes with row and y goes with column."),
        ])


def exercise5():
    """Exercise 5: create_z using whole-array NumPy operations."""
    with Checker("Practical 3, Exercise 5") as c:
        c.check(callable(c.ns.get("create_z")), "`create_z` is a function",
                "I can't find a function called `create_z`.")
        ok = c.sequence("z", c.need("z"), _grid(300), describe_index=_rc, hints=[
            (np.zeros((300, 300)), "z is still all zeros. Inside create_z, work out z from x and y "
                                   "before `return z`."),
        ])
        if ok and "for " in source_of(c.ns.get("create_z")):
            print(f"   {HINT} It works! Now try it without any loops: NumPy can do "
                  "z = x + y*x on whole arrays in one line.")
