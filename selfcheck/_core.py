"""Shared helpers for the self-check cells in the practical notebooks.

Students never need to read or edit this file. Each practical has its own
module (practical1.py, practical2.py, ...) with one function per exercise,
for example ``check.exercise1()``. Those functions look up the variables the
student created in their notebook and print friendly feedback.

The checks are only there to help you learn. They are not marked, and the
proposed solutions in the solutions/ folder remain the reference answers.
"""

import ast
import contextlib
import inspect
import io
import math
import re
import warnings

try:
    import numpy as np
except ImportError:  # numpy is installed on every platform we use, but be safe
    np = None


PASS = "✅"   # green tick
FAIL = "❌"   # red cross
HINT = "\U0001F4A1"  # light bulb
PARTY = "\U0001F389"


class _Stop(Exception):
    """Raised internally to stop a check early (e.g. a variable is missing)."""


def user_namespace():
    """Return the notebook's variables (the globals of the __main__ module)."""
    for frame_info in inspect.stack():
        g = frame_info.frame.f_globals
        if g.get("__name__") == "__main__":
            return g
    return {}


class Checker:
    """Collects the results of one exercise check and prints a summary.

    Use it as a context manager::

        with Checker("Practical 1, Exercise 1") as c:
            temperature = c.need("temperature")
            c.check(temperature == 298, "temperature is 298", "temperature should be 298")
    """

    def __init__(self, title):
        self.title = title
        self.ns = user_namespace()
        self.passed = 0
        self.failed = 0

    # -- context manager -------------------------------------------------
    def __enter__(self):
        print(f"Checking {self.title}...\n")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is _Stop:
            pass
        elif exc_type is not None:
            self.failed += 1
            print(f"{FAIL} Something went wrong while checking your answer: "
                  f"{exc_type.__name__}: {exc}")
            print(f"   {HINT} Make sure the exercise cell above runs without an error, "
                  "then run this cell again.")
        print()
        if self.failed == 0 and self.passed > 0:
            print(f"{PARTY} Well done, all checks passed!")
        else:
            print(f"Keep going: {self.passed} of {self.passed + self.failed} checks passed. "
                  "Fix the first problem above, re-run the exercise cell, then run this cell again.")
        return True  # never show a traceback to the student

    # -- recording results -------------------------------------------------
    def ok(self, message):
        self.passed += 1
        print(f"{PASS} {message}")
        return True

    def fail(self, message, hint=None):
        self.failed += 1
        print(f"{FAIL} {message}")
        if hint:
            print(f"   {HINT} {hint}")
        return False

    def check(self, condition, ok_message, fail_message, hint=None):
        if condition:
            self.ok(ok_message)
        else:
            self.fail(fail_message, hint)
        return bool(condition)

    def stop(self):
        raise _Stop()

    # -- looking things up -------------------------------------------------
    def need(self, name):
        """Return the notebook variable ``name`` or stop with a friendly message."""
        if name not in self.ns:
            self.fail(f"I can't find a variable called `{name}`.",
                      "Did you run the exercise cell above? Check the spelling too: "
                      "Python cares about capital letters.")
            self.stop()
        return self.ns[name]

    # -- comparing values -------------------------------------------------
    def number(self, name, actual, expected, rel=1e-6, hints=()):
        """Compare a single number. ``hints`` is a list of (wrong_value, hint)."""
        if not is_number(actual):
            return self.fail(f"`{name}` should be a number, but it is {type(actual).__name__}: {actual!r}")
        if close(actual, expected, rel):
            return self.ok(f"`{name}` is correct ({actual})")
        for wrong, hint in hints:
            if close(actual, wrong, rel):
                return self.fail(f"`{name}` is {actual}, which is not quite right.", hint)
        return self.fail(f"`{name}` is {actual}, but it should be about {expected}.")

    def sequence(self, name, actual, expected, rel=1e-6, describe_index=None, hints=(), atol=1e-12):
        """Compare a list or NumPy array (1D or 2D) with the expected values.

        ``describe_index(i)`` turns a position into words for the message.
        ``hints`` is a list of (wrong_values, hint) for common mistakes.
        """
        if np is None:
            raise RuntimeError("numpy is needed for this check")
        try:
            a = np.array(actual, dtype=float)
        except (TypeError, ValueError):
            return self.fail(f"`{name}` should contain only numbers.")
        e = np.array(expected, dtype=float)
        if a.shape != e.shape:
            if a.ndim == 1 and e.ndim == 1:
                return self.fail(f"`{name}` has {a.size} values, but it should have {e.size}.",
                                 "Check the number you passed to range().")
            return self.fail(f"`{name}` has shape {a.shape}, but it should have shape {e.shape}.")
        good = np.isclose(a, e, rtol=rel, atol=atol)
        if good.all():
            return self.ok(f"`{name}` has the right {_size_words(e)} and every value is correct")
        for wrong, hint in hints:
            if np.shape(wrong) == a.shape and np.isclose(a, np.array(wrong, dtype=float), rtol=rel, atol=atol).all():
                return self.fail(f"`{name}` is not quite right.", hint)
        idx = tuple(int(i) for i in np.argwhere(~good)[0])
        where = describe_index(idx) if describe_index else f"position {list(idx)}"
        n_bad = int((~good).sum())
        return self.fail(
            f"`{name}` has {n_bad} wrong value(s). The first one is at {where}: "
            f"you have {_fmt(a[idx])}, expected {_fmt(e[idx])}.")

    # -- re-running an exercise cell ----------------------------------------
    def output_of_exercise_cell(self, anchors):
        """Re-run the exercise cell and return what it printed."""
        return self.rerun_exercise_cell(anchors).printed

    def rerun_exercise_cell(self, anchors):
        """Quietly re-run the most recent cell containing one of ``anchors``.

        Some exercises only ask you to print something or draw a plot, so there
        is no variable to look at. In that case we find the exercise cell in your
        notebook history and run it again behind the scenes. Returns a
        ``CellRun`` with what it printed, the value of its last line (what
        Jupyter would show as Out[..]) and any Matplotlib figures it drew.
        """
        history = self.ns.get("In")
        if not history:
            self.fail("This check only works inside a Jupyter notebook.")
            self.stop()
        source = None
        for cell in reversed(history[:-1]):  # history[-1] is this check cell
            if "check." in cell or "selfcheck" in cell:
                continue
            if any(anchor in cell for anchor in anchors):
                source = cell
                break
        if source is None:
            self.fail("I can't find your exercise cell.", "Run the exercise cell above first, then this cell.")
            self.stop()

        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            self.fail(f"Your exercise cell has a syntax error on line {exc.lineno}: {exc.msg}",
                      "Look for a missing value after '=', a missing bracket or wrong indentation.")
            self.stop()
        last_expr = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last_expr = ast.Expression(tree.body.pop().value)

        plt = _pyplot()
        before = set(plt.get_fignums()) if plt else set()
        real_show = plt.show if plt else None
        if plt:
            plt.show = lambda *args, **kwargs: None  # keep the figures so we can look at them
        namespace = dict(self.ns)
        buffer = io.StringIO()
        value = None
        try:
            with contextlib.redirect_stdout(buffer), warnings.catch_warnings():
                warnings.simplefilter("ignore")
                exec(compile(tree, "<exercise cell>", "exec"), namespace)
                if last_expr is not None:
                    value = eval(compile(last_expr, "<exercise cell>", "eval"), namespace)
        except Exception as exc:  # noqa: BLE001 - we want to report any error
            self.fail(f"Your exercise cell stops with an error: {type(exc).__name__}: {exc}",
                      "Fix the error in the exercise cell first.")
            self.stop()
        finally:
            figures = []
            if plt:
                plt.show = real_show
                figures = [plt.figure(n) for n in plt.get_fignums() if n not in before]
                for fig in figures:
                    plt.close(fig)
        return CellRun(buffer.getvalue(), value, figures, namespace)


class CellRun:
    """What happened when an exercise cell was re-run by a check."""

    def __init__(self, printed, value, figures, namespace):
        self.printed = printed
        self.value = value
        self.figures = figures
        self.namespace = namespace

    @property
    def axes(self):
        return [ax for fig in self.figures for ax in fig.axes]


def _pyplot():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    return plt


def bar_heights(ax):
    """Total height of the histogram bars drawn on a Matplotlib axes."""
    from matplotlib.patches import Rectangle
    return sum(p.get_height() for p in ax.patches if isinstance(p, Rectangle))


def same_shape(a, b):
    """True if two 0/1 grids draw the same pattern, ignoring position, rotation and mirroring."""
    a = _crop(np.array(a) > 0)
    b = _crop(np.array(b) > 0)
    for k in range(4):
        r = np.rot90(b, k)
        for candidate in (r, np.fliplr(r)):
            if candidate.shape == a.shape and (candidate == a).all():
                return True
    return False


def _crop(grid):
    if not grid.any():
        return grid[:0, :0]
    rows = np.where(grid.any(axis=1))[0]
    cols = np.where(grid.any(axis=0))[0]
    return grid[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]


# -- small utilities ------------------------------------------------------
def is_number(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    return np is not None and isinstance(value, np.number)


def close(a, b, rel=1e-6):
    return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=1e-12)


def numbers_in(text):
    """All numbers that appear in ``text``, as floats, in order."""
    return [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", text)]


def lines_of(text):
    """Non-empty printed lines with extra spaces squashed."""
    return [" ".join(line.split()) for line in text.splitlines() if line.strip()]


def source_of(func):
    try:
        return inspect.getsource(func)
    except (OSError, TypeError):
        return ""


def _fmt(value):
    value = float(value)
    return str(int(value)) if value.is_integer() and abs(value) < 1e15 else repr(value)


def _size_words(e):
    if e.ndim == 1:
        return f"length ({e.size})"
    return f"shape {e.shape}"
