"""Self-checks for Practical 4: Conway's Game of Life."""

from ._core import Checker, np, same_shape


def _life_step(space):
    """One generation of the Game of Life (cells off the board count as dead)."""
    padded = np.pad(np.array(space) > 0, 1).astype(int)
    rows, cols = np.shape(space)
    count = sum(padded[1 + dr:1 + dr + rows, 1 + dc:1 + dc + cols]
                for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0))
    alive = np.array(space) > 0
    return ((alive & ((count == 2) | (count == 3))) | (~alive & (count == 3))).astype(int)


def _phases(pattern, steps):
    """All the shapes a pattern takes over a number of generations."""
    grid = np.pad(pattern, 6)
    shapes = [grid]
    for _ in range(steps):
        grid = _life_step(grid)
        shapes.append(grid)
    return shapes


def _grid(cells, shape):
    g = np.zeros(shape, dtype=int)
    for r, c in cells:
        g[r, c] = 1
    return g


TUB = _grid([(1, 2), (2, 1), (3, 2), (2, 3)], (5, 5))
BOAT = _grid([(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)], (5, 5))
BEACON = _grid([(1, 1), (1, 2), (2, 1), (3, 4), (4, 3), (4, 4)], (6, 6))
TOAD = _grid([(2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3)], (6, 6))
GLIDER = _grid([(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)], (5, 5))
LWSS = _grid([(1, 2), (1, 5), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (3, 5)], (6, 7))


def _check_shape(c, name, expected, phases=1):
    grid = c.need(name)
    arr = np.array(grid)
    if not (arr > 0).any():
        return c.fail(f"`{name}` is still empty.",
                      f"Set the black squares to 1, for example {name}[1,2] = 1")
    if any(same_shape(arr, p) for p in _phases(expected, phases)):
        c.ok(f"`{name}` has the right shape")
        if (arr[0, :] > 0).any() or (arr[-1, :] > 0).any() or (arr[:, 0] > 0).any() or (arr[:, -1] > 0).any():
            print("   \U0001F4A1 Tip: your shape touches the edge of the array. Leave a border of empty "
                  "cells so it has room to change in the simulation.")
        return True
    n_now, n_want = int((arr > 0).sum()), int(expected.sum())
    hint = (f"You have {n_now} black squares but a {name} has {n_want}." if n_now != n_want
            else "You have the right number of black squares, but some are in the wrong place. "
                 "Compare with the figure, remembering rows are counted from the top starting at 0.")
    return c.fail(f"`{name}` does not look like a {name} yet.", hint)


def _neighbours(board, r, c):
    block = board[max(r - 1, 0):r + 2, max(c - 1, 0):c + 2]
    return int(block.sum() - board[r, c])


# Small boards (with an empty border) used to test the student's search_each_cell function.
_TESTS = [
    ("a blinker (3 in a row)", _grid([(4, 3), (4, 4), (4, 5)], (9, 9))),
    ("a block (2x2 square that never changes)", _grid([(3, 3), (3, 4), (4, 3), (4, 4)], (8, 8))),
    ("a Beacon", np.pad(BEACON, 2)),
    ("a Glider", np.pad(GLIDER, 2)),
    ("a crowded plus shape (tests overpopulation)", _grid([(3, 4), (4, 3), (4, 4), (4, 5), (5, 4)], (9, 9))),
    ("a single lonely cell (tests underpopulation)", _grid([(4, 4)], (9, 9))),
]


def _check_rules(c):
    func = c.ns.get("search_each_cell")
    if not callable(func):
        c.fail("I can't find a function called `search_each_cell`.",
               "Run the exercise cell above. If it shows an error, fix that first.")
        c.stop()
    for label, board in _TESTS:
        rows, cols = board.shape
        try:
            result = func(rows, cols, board.copy())
        except Exception as exc:  # noqa: BLE001
            c.fail(f"`search_each_cell` crashed on {label}: {type(exc).__name__}: {exc}")
            c.stop()
        expected = _life_step(board)
        result = np.array(result)
        if result.shape == expected.shape and ((result > 0) == (expected > 0)).all():
            continue
        if result.shape != expected.shape:
            c.fail(f"`search_each_cell` returned an array of shape {result.shape} for a board of shape {expected.shape}.")
            c.stop()
        bad = np.argwhere((result > 0) != (expected > 0))[0]
        r, col = int(bad[0]), int(bad[1])
        was = "alive" if board[r, col] else "dead"
        should = "alive" if expected[r, col] else "dead"
        got = "dead" if expected[r, col] else "alive"
        c.fail(f"The rules are not quite right yet. On {label}, the cell at row {r}, column {col} is {was} "
               f"with {_neighbours(board, r, col)} live neighbours. In the next generation it should be "
               f"{should}, but your function makes it {got}.",
               "Remember to set new_space[row, col] in every case. Check < and <= against the four rules.")
        c.stop()
    c.ok("`search_each_cell` follows all four rules of life on every test board")
    return True


def exercise1():
    """Exercise 1: draw a Tub and a Boat."""
    with Checker("Practical 4, Exercise 1") as c:
        _check_shape(c, "Tub", TUB)
        _check_shape(c, "Boat", BOAT)


def exercise2():
    """Exercise 2: draw a Beacon, Toad, Glider and LWSS."""
    with Checker("Practical 4, Exercise 2") as c:
        _check_shape(c, "Beacon", BEACON, phases=1)
        _check_shape(c, "Toad", TOAD, phases=1)
        _check_shape(c, "Glider", GLIDER, phases=3)
        _check_shape(c, "LWSS", LWSS, phases=3)


def exercise3():
    """Exercise 3: implement the four rules of life inside search_each_cell."""
    with Checker("Practical 4, Exercise 3") as c:
        _check_rules(c)


def exercise4():
    """Exercise 4: run the Beacon for 20 generations."""
    with Checker("Practical 4, Exercise 4") as c:
        _check_rules(c)
        beacon = np.array(c.need("Beacon"))
        c.check(beacon.shape == BEACON.shape and ((beacon > 0) == (BEACON > 0)).all(),
                "After 20 generations the Beacon is back where it started (it repeats every 2 steps)",
                "After 20 generations the Beacon should look the same as at the start, but it doesn't.",
                "Re-run the whole exercise cell from the top so the Beacon starts fresh.")


def exercise5():
    """Exercise 5: copy the working search_each_cell into the Universe simulation."""
    with Checker("Practical 4, Exercise 5") as c:
        _check_rules(c)
        universe = np.array(c.need("Universe"))
        c.check(universe.shape == (50, 50), "`Universe` is still a 50x50 board",
                f"`Universe` should be 50x50, but it has shape {universe.shape}.")
