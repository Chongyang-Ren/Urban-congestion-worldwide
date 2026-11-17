"""country-clustered uncertainty for the existing specifications.

No regressors, outcomes or sample-selection rules are added. Covariance uses
the CR1 finite-sample correction. Confidence intervals and two-sided tests use
Student's t with the number of countries minus one degrees of freedom.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import t
import statsmodels.api as sm



def fit_ols_cluster(df,y_col,x_cols,cluster_col='country'):
    d=df[[y_col,cluster_col]+x_cols].replace([np.inf,-np.inf],np.nan).dropna()
    X=d[x_cols].to_numpy(float); y=d[y_col].to_numpy(float)
    n,k=X.shape; inv=np.linalg.pinv(X.T@X); b=inv@X.T@y; e=y-X@b
    meat=np.zeros((k,k)); groups=d[cluster_col].astype(str).to_numpy(); unique=np.unique(groups); g=len(unique)
    for c in unique:
        score=X[groups==c].T@e[groups==c];meat+=np.outer(score,score)
    cov=(g/(g-1))*((n-1)/(n-k))*inv@meat@inv
    se=np.sqrt(np.maximum(np.diag(cov),0))
    return dict(n=n,k=k,clusters=g,columns=x_cols,beta=b,se=se,cov=cov,r2=1-float(e@e)/float(((y-y.mean())**2).sum()))

def linear_combo(result,weights):
    w=np.array([weights.get(x,0) for x in result['columns']]);b=float(w@result['beta']);se=float(np.sqrt(max(w@result['cov']@w,0)))
    critical=t.ppf(.975,result['clusters']-1)
    return dict(estimate=b,se=se,ci_low=b-critical*se,ci_high=b+critical*se,p=float(2*t.sf(abs(b/se),result['clusters']-1)))


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
    result = fit_ols_cluster(long, "log_length", x_cols, "country")
    summary = {
        "morning_slope": linear_combo(result, {"z": 1.0}),
        "evening_slope": linear_combo(result, {"z": 1.0, "z_evening": 1.0}),
        "evening_minus_morning": linear_combo(result, {"z_evening": 1.0}),
        "n": result["n"],
        "countries": result["clusters"],
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
    result = fit_ols_cluster(source, "log_length", x_cols, "country")
    if spline:
        summary = {
            "below_1m_slope": linear_combo(result, {"z": 1.0}),
            "above_1m_slope": linear_combo(result, {"z": 1.0, "hinge": 1.0}),
            "slope_difference": linear_combo(result, {"hinge": 1.0}),
            "model": "continuous_piecewise",
            "n": result["n"],
            "countries": result["clusters"],
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
            "countries": result["clusters"],
            "r2": result["r2"],
        }
    return result, summary
