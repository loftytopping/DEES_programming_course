"""Self-checks for Practical 1: data types, operations and loops."""

from ._core import Checker, close

SPEED_OF_LIGHT = 3.0e8
PLANCK = 6.62607004e-34
ELECTRON_MASS = 9.11e-31
TEMPERATURE = 298.15
GAS_CONSTANT = 8.205736e-5
VOLUME = 1.0
MOLES = 2.15
VELOCITY = 5.31e6


def exercise1():
    """Exercise 1: an integer `temperature` and a float `mass`."""
    with Checker("Practical 1, Exercise 1") as c:
        temperature = c.need("temperature")
        mass = c.need("mass")

        if type(temperature) is int:
            c.ok("`temperature` is an integer")
        elif type(temperature) is float:
            c.fail("`temperature` is a float, but it should be an integer.",
                   "Write 298 without a decimal point. 298.0 is a float.")
        else:
            c.fail(f"`temperature` should be an integer, but it is a {type(temperature).__name__}.",
                   "Numbers should not have quote marks around them.")
        c.check(temperature == 298, "`temperature` is 298 K",
                f"`temperature` is {temperature!r}, but it should be 298.")

        if type(mass) is float:
            c.ok("`mass` is a float")
        else:
            c.fail(f"`mass` should be a float, but it is a {type(mass).__name__}.",
                   "A float is a number with a decimal point, like 3.78.")
        c.check(mass == 3.78, "`mass` is 3.78 kg",
                f"`mass` is {mass!r}, but it should be 3.78.")


def exercise2():
    """Exercise 2: four equations written with arithmetic operators."""
    m, cl, h, vel = ELECTRON_MASS, SPEED_OF_LIGHT, PLANCK, VELOCITY
    n, R, T, V = MOLES, GAS_CONSTANT, TEMPERATURE, VOLUME
    with Checker("Practical 1, Exercise 2") as c:
        c.number("E", c.need("E"), m * cl ** 2, hints=[
            (m * cl, "Remember the speed of light is squared: use c**2."),
            (m * cl * 2, "c**2 means c squared. c*2 means c times two."),
        ])
        c.number("Lambda", c.need("Lambda"), h / (m * vel), hints=[
            (h / m * vel, "Put brackets around the bottom of the fraction: h/(m*vel)."),
        ])
        c.number("P", c.need("P"), n * R * T / V, hints=[
            (V / (n * R * T), "Rearrange PV = nRT to get P on its own: P = nRT / V."),
        ])
        c.number("T_celsius", c.need("T_celsius"), T - 273, hints=[
            (T - 273.15, "Close! The exercise uses the formula C = K - 273."),
            (T + 273, "To go from Kelvin to Celsius you subtract 273."),
        ])


def exercise3():
    """Exercise 3: append two cities and change the 5th entry."""
    expected = ['London', 'Beijing', 'Rome', 'Ankara', 'Hanoi', 'Manchester', 'Edinburgh']
    with Checker("Practical 1, Exercise 3") as c:
        cities = c.need("list_capitals")
        if not isinstance(cities, list):
            c.fail(f"`list_capitals` should be a list, but it is a {type(cities).__name__}.")
            c.stop()
        if cities == expected:
            c.ok("`list_capitals` is exactly right")
            return
        if cities.count('Manchester') > 1 or cities.count('Edinburgh') > 1:
            c.fail("Manchester or Edinburgh appears more than once in your list.",
                   "Each time you run the cell, .append() adds the cities again. Re-run the cells "
                   "from the one that creates `list_capitals`, then run the exercise cell once.")
            c.stop()
        c.check(cities[-2:] == ['Manchester', 'Edinburgh'],
                "Manchester and Edinburgh are at the end of the list, in the right order",
                f"The last two cities should be Manchester then Edinburgh, but they are {cities[-2:]}.",
                "Use list_capitals.append('Manchester') and then the same for Edinburgh.")
        fifth = cities[4] if len(cities) > 4 else None
        c.check(fifth == 'Hanoi', "The 5th entry is now Hanoi",
                f"The 5th entry should be 'Hanoi', but it is {fifth!r}.",
                "Python counts from 0, so the 5th entry is list_capitals[4]."
                if 'Hanoi' in cities else "Change it with list_capitals[4] = 'Hanoi'.")
        c.check(cities == expected, "The whole list matches",
                f"The whole list should be {expected}, but it is {cities}.",
                "Re-run the cells from the one that creates `list_capitals` to start again.")


def exercise4():
    """Exercise 4: a loop that builds x = 1..50 and y = x**2.8."""
    x_expected = list(range(1, 51))
    with Checker("Practical 1, Exercise 4") as c:
        x = c.need("x")
        y = c.need("y")
        c.sequence("x", x, x_expected,
                   describe_index=lambda i: f"x[{i[0]}]",
                   hints=[(list(range(0, 50)), "x should start at 1, but range(50) starts at 0. Try step+1.")])
        c.sequence("y", y, [v ** 2.8 for v in x_expected],
                   describe_index=lambda i: f"y[{i[0]}] (where x = {i[0] + 1})",
                   hints=[([v ** 2.8 for v in range(0, 50)], "y uses x values starting at 0. Fix x first."),
                          ([v * 2.8 for v in x_expected], "Use ** to raise to a power. * means multiply.")])
