"""Self-checks for Practical 8: Pandas, statistics and Seaborn."""

from ._core import Checker, bar_heights, np, numbers_in

AQ_COLUMNS = ['temperature', 'pressure', 'humidity', 'wind_direction', 'wind_speed',
              'PM2.5', 'PM10', 'NO2', 'CO', 'O3', 'SO2']


def exercise1():
    """Exercise 1: count the meteorological stations."""
    with Checker("Practical 8, Exercise 1") as c:
        meteo = c.need("data_meteo")
        expected = meteo["station_id"].nunique()
        run = c.rerun_exercise_cell(["station_id", "data_meteo"])
        shown = []
        if np.isscalar(run.value) and not isinstance(run.value, str):
            shown.append(float(run.value))
        elif hasattr(run.value, "size") and not hasattr(run.value, "columns") and run.value.ndim == 0:
            shown.append(float(run.value))
        shown += numbers_in(run.printed)
        if expected in shown:
            c.ok(f"You found the {expected} stations")
        elif not shown:
            c.fail("Your cell doesn't show a number yet.",
                   "Use .value_counts() on the 'station_id' column, then .size (see Practical 6).")
        elif len(meteo) in shown:
            c.fail("That is the number of rows, not the number of different stations.",
                   "Use data_meteo['station_id'].value_counts().size")
        else:
            c.fail(f"I expected {expected} stations, but your cell shows {shown[0]:g}.",
                   "Use data_meteo['station_id'].value_counts().size")


def exercise2():
    """Exercise 2: histogram of temperature at Shunyi."""
    with Checker("Practical 8, Exercise 2") as c:
        meteo = c.need("data_meteo")
        run = c.rerun_exercise_cell(["hist", "shunyi"])
        heights = [h for h in (bar_heights(ax) for ax in run.axes) if h > 0]
        if not heights:
            c.fail("Your cell doesn't draw a histogram yet.",
                   "Select the Shunyi rows, then add .hist(column='temperature').")
            c.stop()
        expected = int(meteo.loc[meteo["station_id"] == "shunyi_meo", "temperature"].notna().sum())
        total = int(round(heights[0]))
        if total == expected:
            c.ok(f"Your histogram uses the {expected} temperature readings from Shunyi")
        elif total == int(meteo["temperature"].notna().sum()):
            c.fail("Your histogram uses every station, not just Shunyi.",
                   "Select rows first: data_meteo[data_meteo['station_id'] == 'shunyi_meo']")
        else:
            c.fail(f"Your histogram counts {total} readings, but Shunyi has {expected}.",
                   "Use data_meteo[data_meteo['station_id'] == 'shunyi_meo'].hist(column='temperature')")


def _medians(ax):
    """Median lines drawn by seaborn's boxplot (short horizontal lines)."""
    found = []
    for line in ax.lines:
        x, y = np.asarray(line.get_xdata(), float), np.asarray(line.get_ydata(), float)
        if len(y) == 2 and np.isclose(y[0], y[1]) and 0 < abs(x[1] - x[0]) <= 1:
            found.append(round(float(y[0]), 6))
    return found


def exercise3():
    """Exercise 3: diurnal boxplot of PM2.5 in August."""
    with Checker("Practical 8, Exercise 3") as c:
        df = c.need("combined_df")
        axes = c.need("axes")
        right = np.ravel(axes)[1] if np.size(axes) > 1 else None
        if right is None or not right.patches:
            c.fail("The right-hand plot (August) is still empty.",
                   "Add a second sns.boxplot(...) call with ax=axes[1].")
            c.stop()
        c.ok("The right-hand plot has a boxplot")
        drawn = _medians(right)
        august = df[df.index.month == 8]
        want = august.groupby(august.index.hour)["PM2.5"].median().dropna().round(6).tolist()
        every = df.groupby(df.index.hour)["PM2.5"].median().dropna().round(6).tolist()
        hits = lambda values: sum(any(abs(v - d) < 1e-3 for d in drawn) for v in values)
        if drawn and hits(want) == len(want):
            c.ok("It shows August only, one box for each hour of the day")
        elif drawn and hits(every) == len(every):
            c.fail("The right-hand plot shows the whole year again.",
                   "Select August with combined_df[combined_df.index.month == 8] for data, x and y.")
        elif drawn:
            c.fail("The right-hand plot doesn't match PM2.5 in August.",
                   "Use combined_df[combined_df.index.month == 8], with x=...index.hour and y=...['PM2.5']")


def exercise4():
    """Exercise 4: merged dataframe and maxima for Pingchang."""
    expected = {"PM25": 522.0, "PM10": 1010.0, "NO2": 154.0, "CO": 6.4, "O3": 378.0, "SO2": 300.0}
    with Checker("Practical 8, Exercise 4") as c:
        df = c.need("combined_df_new")
        missing = [col for col in ("PM2.5", "temperature") if col not in df]
        if missing:
            c.fail(f"`combined_df_new` is missing the column(s) {missing}.",
                   "Merge the meteorology and air quality dataframes: pd.merge(pingchang_met_df, pingchang_aq_df)")
            c.stop()
        c.ok("`combined_df_new` has both meteorology and air quality columns")
        for name, value in expected.items():
            c.number(name, c.need(name), value, rel=1e-6)


def exercise5():
    """Exercise 5: correlation heatmap for Pingchang."""
    with Checker("Practical 8, Exercise 5") as c:
        df = c.need("combined_df_new")
        corr = c.need("corr_new")
        if not hasattr(corr, "columns"):
            c.fail("`corr_new` should be a correlation table.", "Use combined_df_new[[...columns...]].corr()")
            c.stop()
        cols = [col for col in AQ_COLUMNS if col in corr.columns]
        c.check(len(cols) == len(AQ_COLUMNS), "`corr_new` uses the same 11 columns as the example",
                f"`corr_new` has {len(corr.columns)} columns; the example heatmap has 11.",
                "Copy the list of columns from the example above.")
        expected = df[cols].corr()
        c.sequence("corr_new", corr.loc[cols, cols].values, expected.values, rel=1e-6,
                   describe_index=lambda i: f"{cols[i[0]]} vs {cols[i[1]]}",
                   hints=[(c.ns["combined_df"][cols].corr().values if "combined_df" in c.ns else np.zeros(1),
                           "These are the correlations from the example dataframe. Use combined_df_new.")])
