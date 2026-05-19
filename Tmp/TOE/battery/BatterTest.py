"""
V720: The Recoverability Framework - NASA PCoE Battery Decomposition Pipeline
Author: UQCF-GEM Technologies 
Description: Extracts and mathematically decomposes open-circuit voltage (OCV) 
relaxation trajectories to isolate the 'latent reserve' of degrading LCO batteries.
Demonstrates that the integrated restoration deficit (full_auc) is a superior 
prognostic indicator of capacity fade compared to instantaneous Ohmic impedance.
"""

import os, requests, zipfile, shutil, logging, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- CONFIGURATION ---
BASE_DIR = Path("./v720_publication")
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

class DataFetcher:
    """Handles downloading and nested extraction of the NASA dataset."""
    NASA_URL = "https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip"
    
    @staticmethod
    def fetch_and_extract():
        zip_path = DATA_DIR / "NASA_Battery.zip"
        if not list(DATA_DIR.rglob("B0005.mat")):
            logging.info("Downloading NASA Battery Dataset (~30MB)...")
            r = requests.get(DataFetcher.NASA_URL, stream=True)
            with open(zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
                    
            logging.info("Unzipping main archive...")
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(DATA_DIR)
                
            logging.info("Unpacking nested archives...")
            for nested_zip in list(DATA_DIR.rglob("*.zip")):
                if nested_zip.name == "NASA_Battery.zip": continue
                try:
                    with zipfile.ZipFile(nested_zip, 'r') as z:
                        z.extractall(nested_zip.parent)
                    nested_zip.unlink() # Cleanup nested zip
                except Exception as e:
                    logging.warning(f"Skipped {nested_zip.name}: {e}")
            
            if zip_path.exists(): zip_path.unlink() # Cleanup main zip
            
        mat_files = [p for p in DATA_DIR.rglob("*.mat") if p.stem.lower() in ["b0005", "b0006", "b0007"]]
        logging.info(f"Located {len(mat_files)} target battery profiles.")
        return mat_files

class TrajectoryExtractor:
    """Isolates and decomposes the step-response voltage relaxation."""
    
    @staticmethod
    def safe_trapz(y, x):
        """Cross-version compatible trapezoidal integration."""
        if len(y) < 2: return 0.0
        return float(np.trapz(y, x)) if hasattr(np, 'trapz') else float(np.trapezoid(y, x))

    @staticmethod
    def parse_mat(mat_path):
        mat = loadmat(mat_path)
        battery_name = mat_path.stem
        cycle_array = mat[battery_name]['cycle'][0][0][0]
        rows = []
        cycle_count = 0
        
        for i in range(cycle_array.size):
            cyc = cycle_array[i]
            if cyc['type'][0] != 'discharge': continue
            
            cycle_count += 1
            data = cyc['data'][0][0]
            try:
                V = data['Voltage_measured'][0]
                I = data['Current_measured'][0]
                Time = data['Time'][0]
                Capacity = float(data['Capacity'][0][0])
            except: continue
            
            # Find load sever point (~2A down to ~0A)
            load_severed_idx = -1
            for j in range(5, len(I)):
                if I[j-1] < -1.0 and np.abs(I[j]) < 0.1:
                    load_severed_idx = j
                    break
                    
            if load_severed_idx == -1: continue
            
            t_rest = Time[load_severed_idx:]
            V_rest = V[load_severed_idx:]
            
            # Require minimum diffusion duration
            if len(V_rest) < 4: continue 
            duration = t_rest[-1] - t_rest[0]
            if duration < 60.0: continue
                
            t_rest = t_rest - t_rest[0]
            target = V_rest[-1]
            dist = np.abs(V_rest - target)
            
            # --- V720 DECOMPOSITION ---
            snap_dist = np.abs(V[load_severed_idx] - V[load_severed_idx - 1])
            early_mask = t_rest <= 60.0
            tail_mask = t_rest > 60.0
            
            early_auc = TrajectoryExtractor.safe_trapz(dist[early_mask], t_rest[early_mask])
            tail_auc = TrajectoryExtractor.safe_trapz(dist[tail_mask], t_rest[tail_mask])
            full_auc = TrajectoryExtractor.safe_trapz(dist, t_rest)
                
            rows.append({
                "cell_id": battery_name,
                "cycle": cycle_count,
                "capacity": Capacity,
                "snap_distance": float(snap_dist),
                "early_auc": early_auc,
                "tail_auc": tail_auc,
                "full_auc": full_auc,
                "duration": float(duration)
            })
        return rows

class Evaluator:
    """Handles self-referential Z-scoring and residual mathematical controls."""
    
    @staticmethod
    def score_adm_z(df, measure):
        """Calculates penalty score based on system's own healthy baseline."""
        z = np.full(len(df), np.nan)
        for cell, g in df.groupby("cell_id"):
            adm = g.head(10).dropna(subset=[measure])
            if len(adm) < 3: continue
            mu, sd = adm[measure].mean(), adm[measure].std() + 1e-9
            z[g.index] = (g[measure] - mu) / sd
        return z

    @staticmethod
    def residualize_tail(df):
        """Isolates tail predictive power by subtracting initial snap variance."""
        out = np.full(len(df), np.nan)
        for cell, g in df.groupby("cell_id"):
            adm = g.head(10).dropna(subset=["tail_auc", "snap_distance"])
            if len(adm) < 3: continue
            
            model = LinearRegression().fit(adm[["snap_distance"]], adm["tail_auc"])
            valid = g.dropna(subset=["tail_auc", "snap_distance"])
            
            pred = model.predict(valid[["snap_distance"]])
            adm_pred = model.predict(adm[["snap_distance"]])
            
            resid = valid["tail_auc"].to_numpy() - pred
            adm_resid = adm["tail_auc"].to_numpy() - adm_pred
            
            out[valid.index] = (resid - adm_resid.mean()) / (adm_resid.std() + 1e-9)
        return out

def generate_visualizations(res_df, scored_df):
    """Produces publication-ready charts showing framework efficacy."""
    logging.info("Generating performance visualizations...")
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Predictive Power Bar Chart
    plt.figure(figsize=(10, 6))
    chart_data = res_df[res_df['Metric'] != 'tail_auc_resid_snap'].sort_values('Overall_AUC', ascending=False)
    ax = sns.barplot(x='Overall_AUC', y='Metric', data=chart_data, palette='viridis')
    plt.axvline(0.5, color='red', linestyle='--', label='Random Chance (0.5 AUC)')
    plt.title("Prognostic Power of Recovery Components (ROC AUC)", fontsize=14, pad=15)
    plt.xlabel("Area Under Curve (Higher is Better)")
    plt.ylabel("Decomposed Metric")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig1_component_auc.png", dpi=300)
    plt.close()
    
    # Plot 2: Scatter tracking capacity loss
    plt.figure(figsize=(9, 6))
    plot_df = scored_df.dropna(subset=['adm_z_full_auc', 'capacity_loss'])
    sns.regplot(x='capacity_loss', y='adm_z_full_auc', data=plot_df, 
                scatter_kws={'alpha':0.5, 'color':'#2c7bb6'}, line_kws={'color':'#d7191c'})
    plt.title("Restoration Deficit (Full AUC Penalty) vs. Physical Capacity Loss", fontsize=14, pad=15)
    plt.xlabel("Actual Capacity Loss (%)")
    plt.ylabel("Framework Penalty Score (adm_z)")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig2_degradation_tracking.png", dpi=300)
    plt.close()
    logging.info(f"Visualizations saved to {OUT_DIR}")

def main():
    # 1. Fetch
    mat_files = DataFetcher.fetch_and_extract()
    
    # 2. Extract
    logging.info("Executing State-Machine Extraction...")
    all_rows = []
    for p in mat_files:
        all_rows.extend(TrajectoryExtractor.parse_mat(p))
    df = pd.DataFrame(all_rows)
    logging.info(f"Extracted {len(df)} qualified dynamic recovery trajectories.")
    
    # 3. Process Labels
    base_cap = df.groupby("cell_id")["capacity"].transform(lambda x: np.nanmedian(x.head(5)))
    df["capacity_norm"] = df["capacity"] / base_cap
    df["capacity_loss"] = 1 - df["capacity_norm"]
    
    # 4. Math & Residuals
    scored = df.copy()
    metrics = ["snap_distance", "early_auc", "tail_auc", "full_auc"]
    for m in metrics:
        scored[f"adm_z_{m}"] = Evaluator.score_adm_z(scored, m)
    scored["adm_z_tail_auc_resid_snap"] = Evaluator.residualize_tail(scored)
    
    # 5. Evaluate
    results = []
    for m in metrics + ["tail_auc_resid_snap"]:
        col = f"adm_z_{m}"
        g = scored[scored[col].notna()].copy()
        if g.empty: continue
        
        y_q50 = (g["capacity_norm"] <= g["capacity_norm"].quantile(0.50)).astype(int)
        
        # Stability (Variance across individual cells)
        cell_aucs = []
        for cell in g["cell_id"].unique():
            cg = g[g["cell_id"] == cell]
            if len(cg) > 10 and len(cg["capacity_norm"].unique()) > 1:
                y_c = (cg["capacity_norm"] <= cg["capacity_norm"].quantile(0.50)).astype(int)
                try: cell_aucs.append(roc_auc_score(y_c, cg[col]))
                except: pass
                
        results.append({
            "Metric": m,
            "Corr_Capacity_Loss": spearmanr(g[col], g["capacity_loss"]).correlation,
            "Overall_AUC": roc_auc_score(y_q50, g[col]),
            "Stability_Var": np.var(cell_aucs) if len(cell_aucs) > 1 else np.nan
        })
        
    res_df = pd.DataFrame(results).round(4)
    
    # 6. Output Generation
    generate_visualizations(res_df, scored)
    scored.to_csv(OUT_DIR / "v720_scored_trajectories.csv", index=False)
    res_df.to_csv(OUT_DIR / "v720_results_summary.csv", index=False)
    
    print("\n" + "="*50)
    print("V720 PIPELINE COMPLETE: SUMMARY OF FINDINGS")
    print("="*50)
    print(res_df.to_string(index=False))
    print("="*50)

if __name__ == "__main__":
    main()
