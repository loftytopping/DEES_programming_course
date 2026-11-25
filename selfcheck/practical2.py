"""Self-checks for Practical 2: loops and conditional statements."""

from ._core import Checker, lines_of, numbers_in


def exercise1():
    """Exercise 1: x = 11..85 and Y = X**(2.8/X)."""
    x_expected = list(range(11, 86))
    with Checker("Practical 2, Exercise 1") as c:
        x = c.need("x")
        y = c.need("y")
        c.sequence("x", x, x_expected,
                   describe_index=lambda i: f"x[{i[0]}]",
                   hints=[(list(range(1, 76)), "x should run from 11 to 85, not from 1. Try 10+(step+1)."),
                          (list(range(10, 85)), "Nearly! x should start at 11, not 10.")])
        c.sequence("y", y, [v ** (2.8 / v) for v in x_expected],
                   describe_index=lambda i: f"y[{i[0]}] (where x = {x_expected[i[0]]})",
                   hints=[([v ** 2.8 / v for v in x_expected],
                           "Put brackets around the power: x**(2.8/x). Without them Python "
                           "works out x**2.8 first and then divides by x.")])


def _piecewise(v):
    if v <= 250:
        return v ** 1.03
    if v < 690:
        return v ** 1.2
    return v ** 2.5


def exercise2():
    """Exercise 2: pick one of three equations depending on the value of X."""
    x_expected = list(range(1, 1001))

    def where(i):
        value = x_expected[i[0]]
        text = f"X = {value}"
        if value in (250, 251, 689, 690):
            text += " (right on a boundary: check whether you need < or <=)"
        return text

    with Checker("Practical 2, Exercise 2") as c:
        x = c.need("x")
        y = c.need("y")
        c.sequence("x", x, x_expected, describe_index=lambda i: f"x[{i[0]}]")
        c.sequence("y", y, [_piecewise(v) for v in x_expected], describe_index=where,
                   hints=[([v ** 1.03 for v in x_expected],
                           "Every value used the first equation. Add elif/else branches for X > 250.")])


def exercise3():
    """Exercise 3: a triple loop that prints only the 'Physics can be ...' sentences."""
    expected = ["Physics can be enjoyable", "Physics can be awful!",
                "Physics can be ok, I guess", "Physics can be ...."]
    with Checker("Practical 2, Exercise 3") as c:
        printed = lines_of(c.output_of_exercise_cell(["list3", "list1"]))
        if not printed:
            c.fail("Your cell does not print anything yet.",
                   "Inside the third loop, use print() to show the three words together.")
            c.stop()
        if printed == expected:
            c.ok("You printed exactly the four expected sentences")
            return
        missing = [s for s in expected if s not in printed]
        extra = [s for s in printed if s not in expected]
        if missing:
            c.fail(f"These sentences are missing: {missing}",
                   "Join the words with spaces: word1 + ' ' + word2 + ' ' + word3.")
        if extra:
            c.fail(f"You printed {len(extra)} line(s) that should not be there, e.g. {extra[0]!r}",
                   "Only print when the first word is 'Physics' AND the second is 'can be'. "
                   "Use `and` to combine the two conditions in one if statement.")
        if not missing and not extra:
            c.fail("The sentences are right but in a different order or repeated.")


def exercise4():
    """Exercise 4: find every x, y (0 to 79) where y + x**2 equals 80."""
    pairs = [(x, 80 - x ** 2) for x in range(80) if 0 <= 80 - x ** 2 < 80]
    with Checker("Practical 2, Exercise 4") as c:
        text = c.output_of_exercise_cell(["80"])
        nums = numbers_in(text)
        if not nums:
            c.fail("Your cell does not print any numbers yet.",
                   "Inside the inner loop, work out z and use an if statement to print x and y when z == 80.")
            c.stop()
        found = []
        for x, y in pairs:
            hit = any((nums[i], nums[i + 1]) in ((x, y), (y, x)) for i in range(len(nums) - 1))
            found.append(hit)
        if all(found):
            c.ok(f"You found all {len(pairs)} combinations: "
                 + ", ".join(f"(x={x}, y={y})" for x, y in pairs))
        else:
            n_found = sum(found)
            c.fail(f"You found {n_found} of the {len(pairs)} combinations.",
                   "Print x and y next to each other whenever y + x**2 == 80. "
                   "Did you loop over range(80) for both x and y?")
        if len(nums) > 6 * len(pairs):
            c.fail("Your cell prints a lot of numbers.",
                   "Only print when z is equal to 80 (use == to compare).")


def exercise5():
    """Exercise 5: five nested loops that crack a 5-digit password."""
    with Checker("Practical 2, Exercise 5") as c:
        text = c.output_of_exercise_cell(["password_string"])
        import re
        target = re.search(r"password\s*=\s*(\d{5})", text)
        if not target:
            c.fail("I can't see the line that prints the secret password.",
                   "Keep the line print(\"password = \", password_string) at the top of the cell.")
            c.stop()
        secret = target.group(1)
        rest = text[target.end():]
        if secret in rest:
            c.ok(f"Your loops cracked the password ({secret})")
        elif "match" in rest.lower():
            c.fail("You print a match, but it is not the right password.",
                   "Join all five letters: letter1+letter2+letter3+letter4+letter5.")
        else:
            c.fail("Your loops did not print the matching password.",
                   "You need five loops, one inside the other, each with range(10). "
                   "In the fifth loop, join the letters and compare with password_string using ==.")
