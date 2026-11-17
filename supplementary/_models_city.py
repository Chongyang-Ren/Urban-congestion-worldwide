"""Original city-clustered interaction models used in Table S6."""
import math
import numpy as np
import pandas as pd

def normal_pvalue(z: float) -> float:
    return math.erfc(abs(float(z)) / math.sqrt(2.0))

def fit_ols_cluster(
    df: pd.DataFrame,
    y_col: str,
    x_cols: list[str],
    cluster_col: str,
) -> dict:
    work = df[[y_col, cluster_col] + x_cols].dropna().copy()
    y = work[y_col].to_numpy(float)
    X = work[x_cols].to_numpy(float)
    n, k = X.shape
    xtx_inv = np.linalg.pinv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    residual = y - X @ beta

    meat = np.zeros((k, k), dtype=float)
    clusters = work[cluster_col].astype(str).to_numpy()
    unique_clusters = np.unique(clusters)
    for cluster in unique_clusters:
        idx = clusters == cluster
        score = X[idx].T @ residual[idx]
        meat += np.outer(score, score)

    g = len(unique_clusters)
    correction = (g / (g - 1.0)) * ((n - 1.0) / (n - k)) if g > 1 and n > k else 1.0
    cov = correction * xtx_inv @ meat @ xtx_inv
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    z = np.divide(beta, se, out=np.full_like(beta, np.nan), where=se > 0)
    p = np.array([normal_pvalue(v) if np.isfinite(v) else np.nan for v in z])
    pred = X @ beta
    sse = float(np.sum((y - pred) ** 2))
    sst = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - sse / sst if sst > 0 else np.nan
    return {
        "n": int(n),
        "k": int(k),
        "clusters": int(g),
        "r2": float(r2),
        "columns": x_cols,
        "beta": beta,
        "se": se,
        "z": z,
        "p": p,
        "cov": cov,
    }

def linear_combo(result: dict, weights: dict[str, float]) -> dict:
    w = np.zeros(len(result["columns"]), dtype=float)
    for name, value in weights.items():
        w[result["columns"].index(name)] = value
    estimate = float(w @ result["beta"])
    variance = float(w @ result["cov"] @ w)
    se = math.sqrt(max(variance, 0.0))
    z = estimate / se if se > 0 else np.nan
    return {
        "estimate": estimate,
        "se": se,
        "ci_low": estimate - 1.96 * se,
        "ci_high": estimate + 1.96 * se,
        "z": z,
        "p": normal_pvalue(z) if np.isfinite(z) else np.nan,
    }

def add_dummies(df: pd.DataFrame, categorical: list[str]) -> tuple[pd.DataFrame, list[str]]:
    work = df.copy()
    dummy_cols: list[str] = []
    for col in categorical:
        dummies = pd.get_dummies(work[col].astype(str), prefix=col, drop_first=True, dtype=float)
        work = pd.concat([work, dummies], axis=1)
        dummy_cols.extend(dummies.columns.tolist())
    return work, dummy_cols

def peak_model(panel: pd.DataFrame, drop_continent: str | None = None, drop_city: str | None = None) -> tuple[dict, dict]:
    source = panel.copy()
    if drop_continent is not None:
        source = source.loc[source["continent"] != drop_continent].copy()
    if drop_city is not None:
        source = source.loc[source["city_id"] != drop_city].copy()
    id_cols = ["city_id", "country", "city", "continent", "month", "z"]
    long = source[id_cols + ["morning_peak_congested_network_length", "evening_peak_congested_network_length"]].melt(
        id_vars=id_cols,
        value_vars=["morning_peak_congested_network_length", "evening_peak_congested_network_length"],
        var_name="peak",
        value_name="length",
    )
    long["length"] = pd.to_numeric(long["length"], errors="coerce")
    long = long.loc[(long["length"] > 0) & np.isfinite(long["z"])].copy()
    long["log_length"] = np.log10(long["length"])
    long["evening"] = (long["peak"] == "evening_peak_congested_network_length").astype(float)
    long["z_evening"] = long["z"] * long["evening"]
    long["const"] = 1.0
    long, dummies = add_dummies(long, ["month", "continent"])
    x_cols = ["const", "z", "evening", "z_evening"] + dummies
    result = fit_ols_cluster(long, "log_length", x_cols, "city_id")
    summary = {
        "morning_slope": linear_combo(result, {"z": 1.0}),
        "evening_slope": linear_combo(result, {"z": 1.0, "z_evening": 1.0}),
        "evening_minus_morning": linear_combo(result, {"z_evening": 1.0}),
        "n": result["n"],
        "cities": result["clusters"],
        "r2": result["r2"],
    }
    return result, summary

def size_model(panel: pd.DataFrame, spline: bool = False, drop_continent: str | None = None, drop_city: str | None = None) -> tuple[dict, dict]:
    source = panel.copy()
    if drop_continent is not None:
        source = source.loc[source["continent"] != drop_continent].copy()
    if drop_city is not None:
        source = source.loc[source["city_id"] != drop_city].copy()
    source["length"] = pd.to_numeric(source["congested_network_length"], errors="coerce")
    source = source.loc[(source["length"] > 0) & np.isfinite(source["z"])].copy()
    source["log_length"] = np.log10(source["length"])
    source["const"] = 1.0
    if spline:
        source["hinge"] = np.maximum(source["z"], 0.0)
    source, dummies = add_dummies(source, ["month", "continent"])
    x_cols = ["const", "z", "hinge"] + dummies if spline else ["const", "z", "large", "z_large"] + dummies
    result = fit_ols_cluster(source, "log_length", x_cols, "city_id")
    if spline:
        summary = {
            "below_1m_slope": linear_combo(result, {"z": 1.0}),
            "above_1m_slope": linear_combo(result, {"z": 1.0, "hinge": 1.0}),
            "slope_difference": linear_combo(result, {"hinge": 1.0}),
            "model": "continuous_piecewise",
            "n": result["n"],
            "cities": result["clusters"],
            "r2": result["r2"],
        }
    else:
        summary = {
            "below_1m_slope": linear_combo(result, {"z": 1.0}),
            "above_1m_slope": linear_combo(result, {"z": 1.0, "z_large": 1.0}),
            "slope_difference": linear_combo(result, {"z_large": 1.0}),
            "level_shift_at_1m": linear_combo(result, {"large": 1.0}),
            "model": "group_interaction",
            "n": result["n"],
            "cities": result["clusters"],
            "r2": result["r2"],
        }
    return result, summary
