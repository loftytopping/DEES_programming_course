"""Shared helpers for the self-check cells in the practical notebooks.

Students never need to read or edit this file. Each practical has its own
module (practical1.py, practical2.py, ...) with one function per exercise,
for example ``check.exercise1()``. Those functions look up the variables the
student created in their notebook and print friendly feedback.

The checks are only there to help you learn. They are not marked, and the
proposed solutions in the solutions/ folder remain the reference answers.
"""

import contextlib
import inspect
import io
import math
import re

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

    def sequence(self, name, actual, expected, rel=1e-6, describe_index=None, hints=()):
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
        good = np.isclose(a, e, rtol=rel, atol=1e-12)
        if good.all():
            return self.ok(f"`{name}` has the right {_size_words(e)} and every value is correct")
        for wrong, hint in hints:
            if np.shape(wrong) == a.shape and np.isclose(a, np.array(wrong, dtype=float), rtol=rel).all():
                return self.fail(f"`{name}` is not quite right.", hint)
        idx = tuple(int(i) for i in np.argwhere(~good)[0])
        where = describe_index(idx) if describe_index else f"position {list(idx)}"
        n_bad = int((~good).sum())
        return self.fail(
            f"`{name}` has {n_bad} wrong value(s). The first one is at {where}: "
            f"you have {_fmt(a[idx])}, expected {_fmt(e[idx])}.")

    # -- printed output -------------------------------------------------
    def output_of_exercise_cell(self, anchors):
        """Re-run the most recent cell containing one of ``anchors`` and return what it printed.

        Some exercises only ask you to print things, so there is no variable to
        look at. In that case we find the exercise cell in your notebook history
        and run it again quietly to capture its printed output.
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
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                exec(compile(source, "<exercise cell>", "exec"), dict(self.ns))
        except Exception as exc:  # noqa: BLE001 - we want to report any error
            self.fail(f"Your exercise cell stops with an error: {type(exc).__name__}: {exc}",
                      "Fix the error in the exercise cell first.")
            self.stop()
        return buffer.getvalue()


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
