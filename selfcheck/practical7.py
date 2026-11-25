"""Self-checks for Practical 7: geospatial data with GeoPandas."""

from ._core import Checker

STOCKPORT = "Stockport District (B)"


def _frame(c, name):
    df = c.need(name)
    if not hasattr(df, "geometry"):
        c.fail(f"`{name}` should be a GeoDataFrame (or GeoSeries).",
               "Make sure you used a GeoPandas method such as .clip(...) or gpd.sjoin(...).")
        c.stop()
    return df


def _same(c, name, df, expected, hint=None, wrong=()):
    """Compare two GeoDataFrames by number of rows and total area."""
    def area(x):
        try:
            return float(x.geometry.area.sum())
        except Exception:  # noqa: BLE001
            return None
    if len(df) == len(expected) and _close(area(df), area(expected)):
        return c.ok(f"`{name}` has the right {len(df)} rows")
    for other, other_hint in wrong:
        if len(df) == len(other) and _close(area(df), area(other)):
            return c.fail(f"`{name}` is not quite right.", other_hint)
    return c.fail(f"`{name}` has {len(df)} rows, but I expected {len(expected)}.", hint)


def _close(a, b):
    if a is None or b is None:
        return a is b
    return abs(a - b) <= 1e-6 * max(abs(a), abs(b), 1.0)


def _crs_ok(c, name, df):
    epsg = df.crs.to_epsg() if df.crs is not None else None
    return c.check(epsg == 3857, f"`{name}` uses EPSG:3857",
                   f"`{name}` uses {df.crs}, but it should use EPSG:3857 like the other maps.",
                   "Convert it with .to_crs(epsg=3857)")


def _subset(c, name, word):
    gdf_wm = _frame(c, "gdf_wm")
    df = _frame(c, name)
    expected = gdf_wm[gdf_wm["RCS_D"].str.contains(word)]
    if len(df) and "RCS_D" in df and not df["RCS_D"].str.contains(word).all():
        c.fail(f"Some rows in `{name}` are not {word.lower()}.",
               f"Keep only rows where gdf_wm['RCS_D'].str.contains('{word}')")
        return expected
    _same(c, name, df, expected,
          hint=f"Select rows with gdf_wm[gdf_wm['RCS_D'].str.contains('{word}')]. Capital letters matter.",
          wrong=[(gdf_wm, "This is the whole bedrock dataframe. Select only the rows you need.")])
    return expected


def exercise1():
    """Exercise 1: only the limestone bedrock."""
    with Checker("Practical 7, Exercise 1") as c:
        _subset(c, "gdf_wm_ex1", "LIMESTONE")


def exercise2():
    """Exercise 2: collieries on mudstone bedrock (spatial join)."""
    import geopandas as gpd
    with Checker("Practical 7, Exercise 2") as c:
        mud = _subset(c, "gdf_wm_ex2", "MUDSTONE")
        cdf_wm = _frame(c, "cdf_wm")
        joined = _frame(c, "joined_df_ex2")
        expected = gpd.sjoin(mud, cdf_wm)
        _same(c, "joined_df_ex2", joined, expected,
              hint="Join the mudstone dataframe with the colliery dataframe: gpd.sjoin(gdf_wm_ex2, cdf_wm)")


def exercise3():
    """Exercise 3: clip bedrock and collieries to Greater Manchester."""
    with Checker("Practical 7, Exercise 3") as c:
        gm = _frame(c, "GMdf_wm")
        if not _crs_ok(c, "GMdf_wm", gm):
            c.stop()
        gdf_wm, cdf_wm = _frame(c, "gdf_wm"), _frame(c, "cdf_wm")
        _same(c, "gdf_wm_GM", _frame(c, "gdf_wm_GM"), gdf_wm.clip(gm),
              hint="Clip the bedrock with gdf_wm.clip(GMdf_wm)",
              wrong=[(gdf_wm, "This is the whole bedrock map. Clip it with gdf_wm.clip(GMdf_wm)")])
        _same(c, "cdf_wm_GM", _frame(c, "cdf_wm_GM"), cdf_wm.clip(gm),
              hint="Clip the collieries with cdf_wm.clip(GMdf_wm)",
              wrong=[(cdf_wm, "This is every colliery. Clip it with cdf_wm.clip(GMdf_wm)")])


def exercise4a():
    """Exercise 4, figure 1: read the flood risk shapefile and convert it."""
    with Checker("Practical 7, Exercise 4 (figure 1)") as c:
        frdf = _frame(c, "frdf")
        c.check(len(frdf) > 0 and "type" in frdf, f"`frdf` holds the {len(frdf)} flood zones",
                "`frdf` doesn't look like the flood risk data.", "Use gpd.read_file(file_flood_risk)")
        _crs_ok(c, "frdf_wm", _frame(c, "frdf_wm"))


def exercise4b():
    """Exercise 4, figure 2: flood risk zones inside Greater Manchester."""
    with Checker("Practical 7, Exercise 4 (figure 2)") as c:
        frdf_wm, gm = _frame(c, "frdf_wm"), _frame(c, "GMdf_wm")
        _same(c, "frdf_wm_GM", _frame(c, "frdf_wm_GM"), frdf_wm.clip(gm),
              hint="Clip the flood zones with frdf_wm.clip(GMdf_wm)",
              wrong=[(frdf_wm, "This is every flood zone. Clip it to Greater Manchester with .clip(GMdf_wm)")])


def exercise5():
    """Exercise 5: flood risk and substations in the Stockport District."""
    with Checker("Practical 7, Exercise 5") as c:
        gm = _frame(c, "GMdf_wm")
        stockport = gm[gm["NAME"] == STOCKPORT]
        whole = "You clipped with the whole of Greater Manchester. Use only Stockport: " \
                "GMdf_wm[GMdf_wm['NAME']=='Stockport District (B)']"
        fr, ss = _frame(c, "frdf_wm_GM"), _frame(c, "ssdf_wm_GM")
        _same(c, "Stock_frdf_wm_GM", _frame(c, "Stock_frdf_wm_GM"), fr.clip(stockport),
              hint=whole, wrong=[(fr, whole)])
        _same(c, "Stock_ssdf_wm_GM", _frame(c, "Stock_ssdf_wm_GM"), ss.clip(stockport),
              hint=whole, wrong=[(ss, whole)])
