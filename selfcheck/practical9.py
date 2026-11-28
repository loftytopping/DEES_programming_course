"""Self-checks for Practical 9: machine learning with scikit-learn."""

from ._core import Checker, np, numbers_in

MFCC = ['MFCCs_ 1', 'MFCCs_ 2', 'MFCCs_ 3', 'MFCCs_ 4', 'MFCCs_ 5', 'MFCCs_ 6',
        'MFCCs_ 7', 'MFCCs_ 8', 'MFCCs_ 9', 'MFCCs_10', 'MFCCs_11', 'MFCCs_12',
        'MFCCs_13', 'MFCCs_14', 'MFCCs_15', 'MFCCs_16', 'MFCCs_17', 'MFCCs_18',
        'MFCCs_19', 'MFCCs_20', 'MFCCs_21', 'MFCCs_22']


def exercise1():
    """Exercise 1: histograms of RH, wind, rain and area."""
    with Checker("Practical 9, Exercise 1") as c:
        axs = np.ravel(c.need("axs"))
        titles = {ax.get_title() for ax in axs if ax.patches}
        for col in ("temp", "RH", "wind", "rain", "area"):
            c.check(col in titles, f"There is a histogram of '{col}'",
                    f"I can't find a histogram of '{col}'.",
                    f"Add data.hist(column='{col}', ax=axs[row, col]) using an empty subplot. "
                    "Column names must match exactly, including capital letters.")


def exercise2():
    """Exercise 2: correlation matrix of the fire data."""
    with Checker("Practical 9, Exercise 2") as c:
        data = c.need("data")
        corr = c.need("corr")
        if not hasattr(corr, "columns"):
            c.fail("`corr` should be a correlation table.", "Use data[['temp','RH','wind','rain','area']].corr()")
            c.stop()
        cols = ['temp', 'RH', 'wind', 'rain', 'area']
        if sorted(corr.columns) != sorted(cols):
            c.fail(f"`corr` uses the columns {list(corr.columns)}, but it should use {cols}.",
                   "Select just those five columns before calling .corr()")
            c.stop()
        c.sequence("corr", corr.loc[cols, cols].values, data[cols].corr().values,
                   describe_index=lambda i: f"{cols[i[0]]} vs {cols[i[1]]}")


def exercise3():
    """Exercise 3: K-means on fires with a positive area."""
    with Checker("Practical 9, Exercise 3") as c:
        data = c.need("data")
        new = c.need("data_new")
        want = int((data["area"] > 0).sum())
        if len(new) == want and (new["area"] > 0).all():
            c.ok(f"`data_new` holds the {want} fires with a positive area")
        elif len(new) == len(data):
            c.fail("`data_new` still holds every row.", "Use data[data['area'] > 0]")
            c.stop()
        else:
            c.fail(f"`data_new` has {len(new)} rows, but {want} fires have area > 0.",
                   "Use data[data['area'] > 0]. Note > 0, not >= 0.")
            c.stop()
        matrix = np.asarray(c.need("numpy_matrix_new"))
        old = c.ns.get("numpy_matrix")
        ncol = np.shape(old)[1] if old is not None and np.ndim(old) == 2 else matrix.shape[-1]
        c.check(matrix.ndim == 2 and matrix.shape == (want, ncol),
                f"`numpy_matrix_new` has one row per fire and the same {ncol} columns as the example",
                f"`numpy_matrix_new` has shape {matrix.shape}, but I expected {(want, ncol)}.",
                "Take the same columns as the example, but from data_new, then .values")
        clusterer = c.need("clusterer")
        fitted = getattr(clusterer, "labels_", None)
        c.check(fitted is not None and len(fitted) == want, "K-means was fitted to the new data",
                "K-means hasn't been fitted to the new data.", "Use clusterer.fit(numpy_matrix_new)")


def exercise4a():
    """Exercise 4a: unique Family, Genus and Species."""
    with Checker("Practical 9, Exercise 4a") as c:
        frogs = c.need("data_frogs")
        text = c.output_of_exercise_cell(["unique Family"])
        nums = numbers_in(text)
        for col in ("Family", "Genus", "Species"):
            n = frogs[col].nunique()
            c.check(n in nums, f"You printed the number of unique {col} entries ({n})",
                    f"I can't see the number of unique {col} entries ({col} has {n}).",
                    f"Use data_frogs['{col}'].value_counts().size")


def exercise4b():
    """Exercise 4b: build the list of the 22 MFCC feature columns with a loop."""
    with Checker("Practical 9, Exercise 4b") as c:
        cols = list(c.need("mfcc_cols"))
        frogs = c.need("data_frogs")
        if not cols:
            c.fail("`mfcc_cols` is still empty.",
                   "Inside the loop, use: if name.startswith('MFCC'): mfcc_cols.append(name)")
            c.stop()
        bad = [x for x in cols if x not in MFCC]
        c.check(not bad, "Every name in `mfcc_cols` is an MFCC feature column",
                f"These names should not be in `mfcc_cols`: {bad[:3]}",
                "Only add a name when name.startswith('MFCC') is True.")
        missing = [x for x in MFCC if x not in cols]
        c.check(not missing, "`mfcc_cols` has all 22 MFCC features",
                f"`mfcc_cols` is missing {len(missing)} of the 22 MFCC features, e.g. {missing[:2]}.",
                "Loop over every name in data_frogs.columns, not just some of them.")
        c.check(len(cols) == len(set(cols)), "No feature appears twice",
                "Some features appear more than once in `mfcc_cols`.",
                "Run the cell again from the top, so mfcc_cols starts as an empty list.")


def _pca(frogs):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    return PCA(n_components=2).fit_transform(StandardScaler().fit_transform(frogs[MFCC]))


def exercise5():
    """Exercise 5: PCA with the Genus label."""
    with Checker("Practical 9, Exercise 5") as c:
        frogs = c.need("data_frogs")
        target = c.need("target")
        c.check(hasattr(target, "equals") and target.equals(frogs["Genus"]), "`target` is the 'Genus' column",
                "`target` should be the 'Genus' column.", "Use data_frogs['Genus']")
        comps = np.asarray(c.need("pca_components"), dtype=float)
        expected = _pca(frogs)
        if comps.shape != expected.shape:
            c.fail(f"`pca_components` has shape {comps.shape}, but I expected {expected.shape}.",
                   "Use pca = PCA(n_components=2) and pca.fit_transform(features_scaled)")
            c.stop()
        # The sign of each principal component is arbitrary, so allow either sign.
        ok = all(np.allclose(comps[:, k], s * expected[:, k], atol=1e-6) for k in range(2)
                 for s in [1 if np.dot(comps[:, k], expected[:, k]) >= 0 else -1])
        c.check(ok, "`pca_components` matches PCA on the standardised features",
                "`pca_components` doesn't match what I expected.",
                "Standardise first with scaler = StandardScaler(), then PCA(n_components=2).")


def exercise6a():
    """Exercise 6a: K-means on Genus without PCA."""
    with Checker("Practical 9, Exercise 6a") as c:
        frogs = c.need("data_frogs")
        target = c.need("target")
        c.check(hasattr(target, "equals") and target.equals(frogs["Genus"]), "`target` is the 'Genus' column",
                "`target` should be the 'Genus' column.", "Use data_frogs['Genus']")
        kmeans = c.need("kmeans")
        genera = frogs["Genus"].nunique()
        c.check(getattr(kmeans, "n_clusters", None) == genera, f"K-means uses {genera} clusters, one per genus",
                f"K-means uses {getattr(kmeans, 'n_clusters', '?')} clusters, but there are {genera} genera.")
        nfeat = getattr(kmeans, "n_features_in_", None)
        c.check(nfeat == len(MFCC), "K-means was fitted on all 22 standardised features (no PCA)",
                f"K-means was fitted on {nfeat} features, not all 22.",
                "Without PCA, fit on the standardised features: kmeans.fit_predict(features_scaled)")
        acc = c.need("accuracy")
        print(f"   Your K-means accuracy is {float(acc):.2f}. Is it close to 80%?")


def exercise6b():
    """Exercise 6b: accuracy for 2 to 12 clusters."""
    with Checker("Practical 9, Exercise 6b") as c:
        ks = list(c.need("k_values"))
        accs = [float(a) for a in c.need("accuracies")]
        if len(accs) != len(ks):
            c.fail(f"`accuracies` has {len(accs)} values, but there are {len(ks)} values of k.",
                   "Append one accuracy inside the loop, and run the whole cell from the top.")
            c.stop()
        c.ok(f"There is one accuracy for each of the {len(ks)} values of k")
        model = c.need("kmeans_k")
        c.check(getattr(model, "n_clusters", None) == ks[-1], "Each K-means uses k clusters",
                f"The last K-means used {getattr(model, 'n_clusters', '?')} clusters, but the last k is {ks[-1]}.",
                "Use KMeans(n_clusters=k, random_state=42)")
        c.check(getattr(model, "n_features_in_", None) == len(MFCC),
                "K-means was fitted on the 22 standardised features",
                f"K-means was fitted on {getattr(model, 'n_features_in_', '?')} features, not 22.",
                "Use kmeans_k.fit_predict(features_scaled), with features_scaled from Exercise 6a.")
        c.check(accs[-1] > accs[0], "Accuracy rises as you add more clusters",
                "The accuracy doesn't change with k as I expected.",
                "Make sure the loop uses k, not a fixed number of clusters.")


def exercise7():
    """Exercise 7: Random Forest predicting Species."""
    with Checker("Practical 9, Exercise 7") as c:
        frogs = c.need("data_frogs")
        y_test = c.need("y_test")
        n = len(frogs)
        c.check(abs(len(y_test) - 0.2 * n) <= 1, f"The test set is 20% of the data ({len(y_test)} rows)",
                f"The test set has {len(y_test)} rows, but 20% of the data is about {round(0.2 * n)}.",
                "Use train_test_split(X, y, test_size=0.2, random_state=42)")
        c.check(set(np.unique(y_test)) <= set(frogs["Species"]), "The labels are species names",
                "`y_test` doesn't hold species names.", "Set y = target, where target is data_frogs['Species']")
        model = c.need("rf_model")
        c.check(hasattr(model, "estimators_"), "The Random Forest has been trained",
                "The Random Forest hasn't been trained yet.", "Use rf_model.fit(X_train, y_train)")
        acc = float(c.need("accuracy"))
        c.check(acc > 0.9, f"Accuracy is {acc:.2f}", f"Accuracy is only {acc:.2f}; I expected over 0.9.",
                "Check you trained on X_train, y_train and predicted on X_test.")


def exercise8():
    """Exercise 8: Random Forest tested on unseen recordings."""
    with Checker("Practical 9, Exercise 8") as c:
        frogs = c.need("data_frogs")
        train_idx = np.asarray(c.need("train_idx"))
        test_idx = np.asarray(c.need("test_idx"))
        rec = frogs["RecordID"].to_numpy()
        shared = set(rec[train_idx]) & set(rec[test_idx])
        c.check(not shared, "No recording is in both the training and test sets",
                f"{len(shared)} recordings are in both the training and test sets.",
                "Pass groups=groups to splitter.split, so whole recordings stay together.")
        for name, idx in (("X_test_g", test_idx), ("y_train_g", train_idx), ("y_test_g", test_idx)):
            val = c.need(name)
            c.check(len(val) == len(idx), f"`{name}` has the right number of rows ({len(idx)})",
                    f"`{name}` has {len(val)} rows, but I expected {len(idx)}.",
                    "Pick the rows with .iloc[train_idx] or .iloc[test_idx].")
        y_test_g = c.need("y_test_g")
        c.check(set(np.unique(y_test_g)) <= set(frogs["Family"]), "The labels are family names",
                "`y_test_g` doesn't hold family names.", "Use y.iloc[test_idx], where y is data_frogs['Family']")
        model = c.need("rf_grouped")
        c.check(hasattr(model, "estimators_") and getattr(model, "n_features_in_", None) == len(MFCC),
                "The new Random Forest was trained on the 22 features",
                "`rf_grouped` hasn't been trained on the 22 features yet.",
                "Use rf_grouped = RandomForestClassifier(n_estimators=100, random_state=42), then rf_grouped.fit(X_train_g, y_train_g)")
        acc = float(c.need("accuracy_grouped"))
        expected = float(np.mean(model.predict(c.need("X_test_g")) == np.asarray(y_test_g)))
        c.check(abs(acc - expected) < 1e-9, f"`accuracy_grouped` is {acc:.2f}",
                f"`accuracy_grouped` is {acc:.2f}, but the model's accuracy on the test recordings is {expected:.2f}.",
                "Use accuracy_score(y_test_g, rf_grouped.predict(X_test_g))")
