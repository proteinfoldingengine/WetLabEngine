
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Official Planck 2018 lensing Table 1 values (MV columns),
# transcribed from the published paper.
cons_rows = [
    (8,40,1.05,0.09,1.40),
    (41,84,1.04,0.05,1.28),
    (85,129,1.01,0.05,0.992),
    (130,174,0.92,0.06,0.761),
    (175,219,0.88,0.08,0.598),
    (220,264,0.87,0.10,0.484),
    (265,309,1.07,0.11,0.401),
    (310,354,1.17,0.14,0.338),
    (355,400,0.89,0.16,0.288),
]
aggr_rows = [
    (8,20,1.07,0.20,1.24),
    (21,39,1.06,0.11,1.40),
    (40,65,1.07,0.08,1.34),
    (66,100,1.02,0.05,1.14),
    (101,144,0.96,0.05,0.904),
    (145,198,0.89,0.06,0.686),
    (199,263,0.91,0.08,0.513),
    (264,338,1.10,0.10,0.382),
    (339,425,0.99,0.13,0.285),
    (426,525,0.95,0.14,0.213),
    (526,637,0.82,0.19,0.160),
    (638,762,0.45,0.23,0.121),
    (763,901,0.77,0.28,0.0934),
    (902,2048,0.70,0.30,0.0518),
]

def build_df(rows):
    df = pd.DataFrame(rows, columns=["Lmin", "Lmax", "amp", "amp_err", "fid"])
    df["Lgeom"] = np.sqrt(df["Lmin"] * df["Lmax"])
    df["C_data"] = df["amp"] * df["fid"]
    df["sigma_C"] = df["amp_err"] * df["fid"]
    return df

gamma = 0.2613
sigma_width = (0.90 * (-np.log(gamma))) / (2*np.sqrt(2*np.log(2)))  # FWHM -> sigma

def m1(L, A):
    return A + 0*L

def m2(L, A, q, L0):
    return A + q*np.exp(-0.5*((np.log(L) - np.log(L0))/sigma_width)**2)

def m3(L, A, q, L0, sigma):
    return A + q*np.exp(-0.5*((np.log(L) - np.log(L0))/sigma)**2)

def fit_models(df, label):
    x = df["Lgeom"].to_numpy()
    y = df["amp"].to_numpy()
    s = df["amp_err"].to_numpy()
    fits = []
    for name, model, p0, bounds in [
        ("M1_constant", m1, [1.0], ([0.0], [10.0])),
        ("M2_fixed_width", m2, [1.0, -0.2, 800.0], ([0.0, -10.0, 10.0], [10.0, 10.0, 5000.0])),
        ("M3_free_width", m3, [1.0, -0.2, 800.0, 0.5], ([0.0, -10.0, 10.0, 0.05], [10.0, 10.0, 5000.0, 3.0])),
    ]:
        popt, _ = curve_fit(model, x, y, p0=p0, sigma=s, absolute_sigma=True, bounds=bounds, maxfev=100000)
        pred = model(x, *popt)
        chi2 = float(np.sum(((y - pred) / s)**2))
        n = len(y)
        k = len(popt)
        fits.append({
            "dataset": label,
            "model": name,
            "params": repr([float(v) for v in popt]),
            "chi2": chi2,
            "dof": n-k,
            "chi2_red": chi2/(n-k),
            "AIC": chi2 + 2*k,
            "BIC": chi2 + k*np.log(n),
            "RMS_pct": float(np.sqrt(np.mean(((y - pred)/y)**2))*100),
        })
    return pd.DataFrame(fits)

def main():
    cons_df = build_df(cons_rows)
    aggr_df = build_df(aggr_rows)
    results = pd.concat([fit_models(cons_df, "conservative"), fit_models(aggr_df, "aggressive")], ignore_index=True)
    print(results.to_string(index=False))

if __name__ == "__main__":
    main()
