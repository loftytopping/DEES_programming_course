"""Self-checks for Practical 6: Pandas dataframes and maps with Cartopy."""

from ._core import Checker, bar_heights, np


def _data(c):
    data = c.need("data")
    if not hasattr(data, "columns"):
        c.fail("`data` should be the eruptions dataframe.",
               "Re-run the cell near the top that reads GVP_Eruption_Results.csv.")
        c.stop()
    return data


def _coords(c, expected_lat, expected_lon, hint_all=None):
    lat = c.need("Latitude")
    lon = c.need("Longitude")
    for name, got, want in (("Latitude", lat, expected_lat), ("Longitude", lon, expected_lon)):
        got = np.asarray(got, dtype=float)
        if got.shape == want.shape and np.allclose(got, want, equal_nan=True):
            c.ok(f"`{name}` holds the right {len(want)} values")
        elif hint_all and got.size == hint_all:
            c.fail(f"`{name}` holds every eruption ({got.size} values), not just the ones asked for.",
                   "Select the rows first with a condition in square brackets, then take the column.")
        else:
            c.fail(f"`{name}` has {got.size} values, but I expected {want.size}.",
                   "Check your condition, then take the column with ['Latitude'].values")


def exercise1():
    """Exercise 1: re-draw the eruption map with green circles twice as big."""
    with Checker("Practical 6, Exercise 1") as c:
        data = _data(c)
        _coords(c, data["Latitude"].values.astype(float), data["Longitude"].values.astype(float))
        ax = c.need("ax")
        points = [col for col in getattr(ax, "collections", []) if len(col.get_offsets()) > 0]
        if not points:
            c.fail("I can't see any points on your map.",
                   "Add a plt.scatter(...) line before plt.show(), like in the example above.")
            c.stop()
        dots = points[-1]
        r, g, b = dots.get_facecolor()[0][:3]
        c.check(g > 0.3 and g > r + 0.2 and g > b + 0.2, "The points are green",
                "The points are not green yet.", "Use color='green' in plt.scatter.")
        size = float(np.atleast_1d(dots.get_sizes())[0])
        c.check(np.isclose(size, 18), "The points are twice as big as before (s=18)",
                f"Your points have size s={size:g}. The example used s=9, so twice as big is s=18.")
        c.check(dots.get_paths() and len(dots.get_paths()[0].vertices) > 4, "The points are circles",
                "The points should be circles.", "Use marker='o'.")


def exercise2():
    """Exercise 2: count the unique eruption locations."""
    with Checker("Practical 6, Exercise 2") as c:
        data = _data(c)
        expected = data["Volcano Name"].nunique()
        unique = c.need("unique_eruptions")
        size = getattr(unique, "size", None)
        if size == expected:
            c.ok(f"There are {expected} unique volcanoes, and `unique_eruptions.size` agrees")
        elif size == len(data):
            c.fail("`unique_eruptions` has one entry per eruption, not per volcano.",
                   "Use .value_counts() on the 'Volcano Name' column.")
        else:
            c.fail(f"`unique_eruptions.size` is {size}, but it should be {expected}.",
                   "Use data['Volcano Name'].value_counts()")


def exercise3():
    """Exercise 3: coordinates of eruptions that started in 2019."""
    with Checker("Practical 6, Exercise 3") as c:
        data = _data(c)
        sel = data[data["Start Year"] == 2019]
        _coords(c, sel["Latitude"].values.astype(float), sel["Longitude"].values.astype(float), len(data))


def exercise4():
    """Exercise 4: coordinates of eruptions between 40N and 40S."""
    with Checker("Practical 6, Exercise 4") as c:
        data = _data(c)
        lat = np.asarray(c.need("Latitude"), dtype=float)
        strict = data[(data["Latitude"] > -40) & (data["Latitude"] < 40)]
        inclusive = data[(data["Latitude"] >= -40) & (data["Latitude"] <= 40)]
        for sel in (strict, inclusive):
            if lat.shape == sel["Latitude"].shape and np.allclose(lat, sel["Latitude"].values):
                _coords(c, sel["Latitude"].values.astype(float), sel["Longitude"].values.astype(float))
                return
        if lat.size == (data["Start Year"] == 2019).sum():
            c.fail("These look like the 2019 eruptions from Exercise 3.",
                   "This time the condition is on 'Latitude': between -40 and 40.")
        elif lat.size and (np.nanmax(lat) > 40 or np.nanmin(lat) < -40):
            c.fail(f"Some of your latitudes are outside 40S to 40N (from {np.nanmin(lat):g} to {np.nanmax(lat):g}).",
                   "Combine two conditions: (data['Latitude'] > -40) & (data['Latitude'] < 40)")
        else:
            c.fail(f"`Latitude` has {lat.size} values, but I expected {len(strict)}.",
                   "Combine two conditions: (data['Latitude'] > -40) & (data['Latitude'] < 40)")


def exercise5():
    """Exercise 5: histogram of Etna eruptions from 1200 to the present day."""
    with Checker("Practical 6, Exercise 5") as c:
        data = _data(c)
        run = c.rerun_exercise_cell(["Etna", ".hist", "hist("])
        bars = [bar_heights(ax) for ax in run.axes]
        bars = [b for b in bars if b > 0]
        if not bars:
            c.fail("Your cell doesn't draw a histogram yet.",
                   "Select the rows you want, then add .hist(column='Start Year').")
            c.stop()
        etna = data[data["Volcano Name"] == "Etna"]
        right = {int((etna["Start Year"] >= 1200).sum()), int((etna["Start Year"] > 1200).sum())}
        total = int(round(bars[0]))
        if total in right:
            c.ok(f"Your histogram shows the {total} Etna eruptions since 1200")
        elif total == len(etna):
            c.fail("Your histogram shows every Etna eruption, including those before 1200.",
                   "Add a second condition: (data['Start Year'] >= 1200)")
        elif total == int((data["Start Year"] >= 1200).sum()):
            c.fail("Your histogram shows eruptions from every volcano since 1200.",
                   "Add a second condition: (data['Volcano Name'] == 'Etna')")
        else:
            c.fail(f"Your histogram counts {total} eruptions, but I expected {max(right)}.",
                   "Combine (data['Start Year'] >= 1200) & (data['Volcano Name'] == 'Etna')")
