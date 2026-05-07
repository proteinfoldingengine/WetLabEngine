# ============================================================
# COLAB: Spectral-Content Normalization Analysis
#
# Purpose:
#   You already ran:
#
#       multi_geometry_trace_dx_scaling_campaign_raw_rows.csv
#
#   This script post-processes that campaign and asks:
#
#       Why does each geometry keep q≈2, while C0 changes?
#
#   It computes spectral/shape descriptors for each conformal field f:
#
#       E0 = <f^2>
#       E1 = <|grad f|^2>
#       E2 = <(Delta f)^2>
#       k_eff^2 = E2/E1
#       participation / IPR
#       gradient anisotropy
#
#   Then it ranks candidate laws:
#
#       abs(C_delta) / dx^q ≈ F(field descriptors)
#
#   using leave-one-geometry-out validation.
#
#   This does NOT claim proof.
#   It finds the next theorem target.
# ============================================================

import os
import json
import numpy as np
import pandas as pd

RAW_CSV = "multi_geometry_trace_dx_scaling_campaign_raw_rows.csv"
OUT_PREFIX = "spectral_content_normalization"

if not os.path.exists(RAW_CSV):
    raise FileNotFoundError(
        f"Missing {RAW_CSV}. Run the multi-geometry campaign first, "
        "or upload the CSV into this Colab runtime."
    )

df = pd.read_csv(RAW_CSV)

GEOMETRY_NAMES = sorted(df["geometry"].unique().tolist())

print("Loaded rows:", len(df))
print("Geometries:", GEOMETRY_NAMES)


# ============================================================
# Analytic/numerical field descriptors
# ============================================================

def field_components(name, X, Y, Z):
    if name == "xyz_product":
        f = np.cos(X)*np.cos(Y)*np.cos(Z)
        fx = -np.sin(X)*np.cos(Y)*np.cos(Z)
        fy = -np.cos(X)*np.sin(Y)*np.cos(Z)
        fz = -np.cos(X)*np.cos(Y)*np.sin(Z)
        lap = -3*f
        return f, fx, fy, fz, lap

    if name == "high_x_product":
        f = np.cos(2*X)*np.cos(Y)*np.cos(Z)
        fx = -2*np.sin(2*X)*np.cos(Y)*np.cos(Z)
        fy = -np.cos(2*X)*np.sin(Y)*np.cos(Z)
        fz = -np.cos(2*X)*np.cos(Y)*np.sin(Z)
        lap = -6*f
        return f, fx, fy, fz, lap

    if name == "additive_mixed":
        f = np.cos(X) + 0.5*np.cos(2*Y) + 0.25*np.cos(3*Z)
        fx = -np.sin(X)
        fy = -1.0*np.sin(2*Y)
        fz = -0.75*np.sin(3*Z)
        lap = -np.cos(X) - 2.0*np.cos(2*Y) - 2.25*np.cos(3*Z)
        return f, fx, fy, fz, lap

    if name == "two_mode_product":
        f1 = np.cos(X)*np.cos(Y)*np.cos(Z)
        f2 = np.cos(2*X)*np.cos(2*Y)*np.cos(Z)
        f = f1 + 0.35*f2
        fx = -np.sin(X)*np.cos(Y)*np.cos(Z) + 0.35*(-2*np.sin(2*X)*np.cos(2*Y)*np.cos(Z))
        fy = -np.cos(X)*np.sin(Y)*np.cos(Z) + 0.35*(-2*np.cos(2*X)*np.sin(2*Y)*np.cos(Z))
        fz = -np.cos(X)*np.cos(Y)*np.sin(Z) + 0.35*(-np.cos(2*X)*np.cos(2*Y)*np.sin(Z))
        lap = -3*f1 + 0.35*(-9*f2)
        return f, fx, fy, fz, lap

    if name == "anisotropic_packet":
        f = np.cos(X) + 0.35*np.cos(X+Y) + 0.20*np.cos(2*Z)
        fx = -np.sin(X) - 0.35*np.sin(X+Y)
        fy = -0.35*np.sin(X+Y)
        fz = -0.40*np.sin(2*Z)
        lap = -np.cos(X) - 0.70*np.cos(X+Y) - 0.80*np.cos(2*Z)
        return f, fx, fy, fz, lap

    raise ValueError(name)


def descriptors_for_geometry(name, N=128):
    L = 2*np.pi
    dx = L/N
    x = np.arange(N)*dx
    X,Y,Z = np.meshgrid(x,x,x,indexing="ij")
    f,fx,fy,fz,lap = field_components(name,X,Y,Z)

    g2 = fx*fx + fy*fy + fz*fz
    vol = (2*np.pi)**3

    E0 = float(np.mean(f*f))
    E1 = float(np.mean(g2))
    E2 = float(np.mean(lap*lap))
    E4 = float(np.mean(f**4))
    ipr = float(E4/(E0*E0 + 1e-15))

    gx = float(np.mean(fx*fx))
    gy = float(np.mean(fy*fy))
    gz = float(np.mean(fz*fz))
    grad_parts = np.array([gx,gy,gz], dtype=float)
    grad_anisotropy = float(np.std(grad_parts)/(np.mean(grad_parts)+1e-15))

    k_eff2 = float(E2/(E1+1e-15))
    k_eff = float(np.sqrt(k_eff2))

    # crude separability / volumetric spread indicators
    f_abs_mean = float(np.mean(np.abs(f)))
    f_abs_ratio = float(f_abs_mean/(np.sqrt(E0)+1e-15))

    return {
        "geometry":name,
        "E0_mean_f2":E0,
        "E1_mean_grad2":E1,
        "E2_mean_lap2":E2,
        "k_eff2_E2_over_E1":k_eff2,
        "k_eff":k_eff,
        "ipr_f4_over_f2sq":ipr,
        "grad_x_energy":gx,
        "grad_y_energy":gy,
        "grad_z_energy":gz,
        "grad_anisotropy":grad_anisotropy,
        "mean_abs_f_over_rms":f_abs_ratio,
        "volume_factor":vol,
    }


desc = pd.DataFrame([descriptors_for_geometry(g) for g in GEOMETRY_NAMES])


# ============================================================
# Fit dx exponent and geometry constant per geometry
# ============================================================

def fit_power_law(gdf):
    # abs_C_delta ≈ c * dx^q
    x = np.log(gdf["dx"].values)
    y = np.log(gdf["abs_C_delta"].values)
    A = np.vstack([np.ones_like(x), x]).T
    coef = np.linalg.lstsq(A,y,rcond=None)[0]
    logc,q = coef
    c = float(np.exp(logc))
    q = float(q)

    pred_C = c*(gdf["dx"].values**q)
    pred_I = -pred_C*gdf["delta_trace_slope"].values
    err = np.abs(pred_I-gdf["delta_int_RdV"].values)/(np.abs(gdf["delta_int_RdV"].values)+1e-12)

    return {
        "geometry":gdf["geometry"].iloc[0],
        "fit_c":c,
        "fit_q":q,
        "fit_I_rel_error_mean":float(np.mean(err)),
        "fit_I_rel_error_max":float(np.max(err)),
        "n_rows":int(len(gdf)),
    }

geom_fit = pd.DataFrame([fit_power_law(g) for _, g in df.groupby("geometry")])
model_df = geom_fit.merge(desc, on="geometry", how="left")

print()
print("GEOMETRY_FIT_AND_DESCRIPTORS:")
print(model_df.to_csv(index=False))


# ============================================================
# Candidate descriptor models
# ============================================================

# We model log(c) using small feature sets.  With only five geometries,
# use leave-one-geometry-out and keep models very low dimensional.
feature_sets = {
    "constant_only": [],
    "log_E1": ["log_E1"],
    "log_E2": ["log_E2"],
    "log_k_eff": ["log_k_eff"],
    "log_E1_plus_log_k": ["log_E1", "log_k_eff"],
    "log_E0_plus_log_k": ["log_E0", "log_k_eff"],
    "log_E2_plus_ipr": ["log_E2", "log_ipr"],
    "log_E1_plus_ipr": ["log_E1", "log_ipr"],
    "log_E1_plus_anisotropy": ["log_E1", "grad_anisotropy"],
    "log_k_plus_ipr": ["log_k_eff", "log_ipr"],
    "log_E0_log_E1_log_k": ["log_E0", "log_E1", "log_k_eff"],
}

work = model_df.copy()
for col in ["E0_mean_f2", "E1_mean_grad2", "E2_mean_lap2", "k_eff", "ipr_f4_over_f2sq"]:
    work["log_" + col.split("_")[0] if False else col] = work[col]

work["log_E0"] = np.log(work["E0_mean_f2"].values + 1e-15)
work["log_E1"] = np.log(work["E1_mean_grad2"].values + 1e-15)
work["log_E2"] = np.log(work["E2_mean_lap2"].values + 1e-15)
work["log_k_eff"] = np.log(work["k_eff"].values + 1e-15)
work["log_ipr"] = np.log(work["ipr_f4_over_f2sq"].values + 1e-15)
work["log_c"] = np.log(work["fit_c"].values)


def fit_linear(train, features):
    y = train["log_c"].values
    if len(features) == 0:
        X = np.ones((len(train),1))
    else:
        X = np.column_stack([np.ones(len(train))] + [train[f].values for f in features])
    beta = np.linalg.lstsq(X,y,rcond=None)[0]
    return beta


def predict_linear(test, features, beta):
    if len(features) == 0:
        X = np.ones((len(test),1))
    else:
        X = np.column_stack([np.ones(len(test))] + [test[f].values for f in features])
    return X @ beta


rank_rows = []
logo_rows = []

geoms = work["geometry"].tolist()

for model_name, feats in feature_sets.items():
    abs_log_errors = []
    rel_c_errors = []

    for holdout in geoms:
        train = work[work["geometry"] != holdout]
        test = work[work["geometry"] == holdout]
        beta = fit_linear(train, feats)
        pred_log_c = float(predict_linear(test, feats, beta)[0])
        true_log_c = float(test["log_c"].iloc[0])
        pred_c = float(np.exp(pred_log_c))
        true_c = float(test["fit_c"].iloc[0])
        rel_c_err = abs(pred_c-true_c)/(abs(true_c)+1e-12)
        abs_log_err = abs(pred_log_c-true_log_c)

        abs_log_errors.append(abs_log_err)
        rel_c_errors.append(rel_c_err)

        logo_rows.append({
            "model":model_name,
            "holdout_geometry":holdout,
            "features":"+".join(feats) if feats else "constant",
            "true_c":true_c,
            "pred_c":pred_c,
            "rel_c_error":rel_c_err,
            "abs_log_error":abs_log_err,
        })

    rank_rows.append({
        "model":model_name,
        "features":"+".join(feats) if feats else "constant",
        "logo_abs_log_error_mean":float(np.mean(abs_log_errors)),
        "logo_abs_log_error_max":float(np.max(abs_log_errors)),
        "logo_rel_c_error_mean":float(np.mean(rel_c_errors)),
        "logo_rel_c_error_max":float(np.max(rel_c_errors)),
        "n_features":len(feats),
    })

rank = pd.DataFrame(rank_rows).sort_values(
    ["logo_abs_log_error_mean", "n_features"],
    ascending=[True, True]
)
logo = pd.DataFrame(logo_rows)

best_model = rank.iloc[0].to_dict()
best_features = feature_sets[best_model["model"]]
best_beta = fit_linear(work, best_features)
work["pred_log_c_best"] = predict_linear(work, best_features, best_beta)
work["pred_c_best"] = np.exp(work["pred_log_c_best"])
work["pred_c_best_rel_error"] = np.abs(work["pred_c_best"]-work["fit_c"])/(np.abs(work["fit_c"])+1e-12)

# Translate back to row-level integral prediction:
row_pred = df.merge(work[["geometry","fit_q","fit_c","pred_c_best"]], on="geometry", how="left")
row_pred["I_pred_with_descriptor"] = -row_pred["pred_c_best"]*(row_pred["dx"]**row_pred["fit_q"])*row_pred["delta_trace_slope"]
row_pred["I_rel_error_with_descriptor"] = np.abs(
    row_pred["I_pred_with_descriptor"]-row_pred["delta_int_RdV"]
)/(np.abs(row_pred["delta_int_RdV"])+1e-12)

summary = {
    "n_geometries":int(len(work)),
    "n_rows":int(len(df)),
    "q_mean":float(work["fit_q"].mean()),
    "q_std":float(work["fit_q"].std()),
    "q_min":float(work["fit_q"].min()),
    "q_max":float(work["fit_q"].max()),
    "c_mean":float(work["fit_c"].mean()),
    "c_cv":float(work["fit_c"].std()/(abs(work["fit_c"].mean())+1e-12)),
    "best_descriptor_model":best_model["model"],
    "best_descriptor_features":best_model["features"],
    "best_logo_rel_c_error_mean":float(best_model["logo_rel_c_error_mean"]),
    "best_logo_rel_c_error_max":float(best_model["logo_rel_c_error_max"]),
    "row_error_mean_using_best_descriptor":float(row_pred["I_rel_error_with_descriptor"].mean()),
    "row_error_max_using_best_descriptor":float(row_pred["I_rel_error_with_descriptor"].max()),
    "classification":(
        "SPECTRAL_CONTENT_NORMALIZATION_PROMISING"
        if best_model["logo_rel_c_error_mean"] < 0.35
        else "SPECTRAL_CONTENT_NORMALIZATION_MIXED"
    )
}

# Save outputs
model_df.to_csv(f"{OUT_PREFIX}_geometry_fit_descriptors.csv", index=False)
rank.to_csv(f"{OUT_PREFIX}_model_rankings.csv", index=False)
logo.to_csv(f"{OUT_PREFIX}_leave_one_geometry_out.csv", index=False)
work.to_csv(f"{OUT_PREFIX}_best_model_by_geometry.csv", index=False)
row_pred.to_csv(f"{OUT_PREFIX}_row_predictions.csv", index=False)

with open(f"{OUT_PREFIX}_summary.json","w") as f:
    json.dump(summary, f, indent=2)

print()
print("================ SPECTRAL CONTENT NORMALIZATION SUMMARY ================")
print(json.dumps(summary, indent=2))

print()
print("MODEL_RANKINGS:")
print(rank.to_csv(index=False))

print()
print("BEST_MODEL_BY_GEOMETRY:")
print(work.to_csv(index=False))

print()
print("LEAVE_ONE_GEOMETRY_OUT:")
print(logo.to_csv(index=False))

print()
print("Saved files:")
print(f"{OUT_PREFIX}_geometry_fit_descriptors.csv")
print(f"{OUT_PREFIX}_model_rankings.csv")
print(f"{OUT_PREFIX}_leave_one_geometry_out.csv")
print(f"{OUT_PREFIX}_best_model_by_geometry.csv")
print(f"{OUT_PREFIX}_row_predictions.csv")
print(f"{OUT_PREFIX}_summary.json")
