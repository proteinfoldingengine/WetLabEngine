# main.py
# Patch ID: 622.2 (Contact Activation Fix)

import torch
import torch.optim as optim
import numpy as np
import os
import sys
import time
import math
import csv
from collections import deque
import argparse

# --- Path and Configuration Setup ---
try:
    from google.colab import drive
    if not os.path.exists('/content/drive'):
        print("Mounting Google Drive...")
        drive.mount('/content/drive')
    BASE_DIR = '/content/drive/My Drive/Folding'
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)
    print(f"Running in Google Colab. Project BASE_DIR set to: {BASE_DIR}")
except ImportError:
    BASE_DIR = '.'
    if os.path.abspath(BASE_DIR) not in sys.path:
        sys.path.append(os.path.abspath(BASE_DIR))
    print(f"Running in a local environment. Project BASE_DIR set to: {os.path.abspath(BASE_DIR)}")

# --- Project-Specific Imports ---
import physics_constants
import physics_metrics
from protein_model import ProteinModel, load_pdb_coords
from dag_engine import DagEngine, DAG_SCHEMA, _dag_force_mapping
from chart_utils import FoldingChartEngine
from force_field import ForceField
from fractal_dimension_utils import compute_fractal_dimension as compute_df_rigorous, reset_fractal_dimension_state
from metrics_history import MetricsHistory
from physics_purity_auditor import run_purity_audit
from config_loader import load_config
from diagnostics_registry import get_log_keys, FORCE_LOSS_KEYS

# --- Experiment Initialization ---
parser = argparse.ArgumentParser(description="UQCF-GEM Protein Folding Simulation")
parser.add_argument('--config', type=str, default='1ubq_baseline.yaml', help="Path to the experiment configuration YAML file.")
args, unknown = parser.parse_known_args()
BASE_CONSTANTS = physics_constants.GLOBAL_PHYSICS_CONSTANTS
config_full_path = os.path.join(BASE_DIR, args.config)
GLOBAL_CONSTANTS = load_config(config_full_path, BASE_CONSTANTS)

PDB_ID = GLOBAL_CONSTANTS['pdb_id']
N_RESIDUES = GLOBAL_CONSTANTS['num_residues']
PATCH_ID = "Patch_625"
NUM_STEPS = GLOBAL_CONSTANTS['num_steps']
LOG_INTERVAL = GLOBAL_CONSTANTS['log_interval']
RANDOM_SEED = GLOBAL_CONSTANTS['random_seed']
FORCE_RANDOM_COIL_INIT = GLOBAL_CONSTANTS['force_random_coil_init']
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"--- UQCF-GEM Engine Initializing ({PATCH_ID}) ---")
print(f"Using device: {DEVICE}")

initial_coords_np = load_pdb_coords(PDB_ID, N_RESIDUES, seed=RANDOM_SEED, force_random_coil=FORCE_RANDOM_COIL_INIT)
native_coords_np = load_pdb_coords(PDB_ID, N_RESIDUES, seed=RANDOM_SEED + 1, force_random_coil=False)
sequence = GLOBAL_CONSTANTS['SEQUENCE_1UBQ']
residue_types = list(sequence)
charges_tensor = torch.tensor(np.array([GLOBAL_CONSTANTS['RESIDUE_CHARGES'].get(res, 0) for res in residue_types], dtype=np.float32), device=DEVICE)
initial_coords = torch.tensor(initial_coords_np, dtype=torch.float32, device=DEVICE, requires_grad=True)
native_coords_tensor = torch.tensor(native_coords_np, dtype=torch.float32, device=DEVICE)
protein_model = ProteinModel(initial_coords).to(DEVICE)
gamma_bar = torch.tensor(GLOBAL_CONSTANTS['gamma_base'], device=DEVICE, requires_grad=True)
optimizer_coords = optim.Adam([protein_model.coords], lr=GLOBAL_CONSTANTS['LEARNING_RATE_COORDS'])
optimizer_gamma = optim.Adam([gamma_bar], lr=GLOBAL_CONSTANTS['LEARNING_RATE_GAMMA'])
PATCH_FOLDER_NAME = PATCH_ID.replace(' ', '_')
output_plots_dir = os.path.join(BASE_DIR, 'plots', PATCH_FOLDER_NAME)
os.makedirs(output_plots_dir, exist_ok=True)
print(f"Plots will be saved to: {output_plots_dir}")
dag_engine = DagEngine(DAG_SCHEMA, GLOBAL_CONSTANTS, _dag_force_mapping)
chart_engine = FoldingChartEngine(output_dir_base_path=output_plots_dir, current_patch_id=PATCH_ID)
metrics_history = MetricsHistory(memory_window=GLOBAL_CONSTANTS['memory_window'], global_constants=GLOBAL_CONSTANTS)
force_field = ForceField(GLOBAL_CONSTANTS, DEVICE)
reset_fractal_dimension_state()

# --- Main Simulation Loop ---
print(f"\n--- Starting Protein Folding Simulation ({PATCH_ID}) ---")
start_time = time.time()
with torch.no_grad():
    initial_pseudo_phi_angles, initial_pseudo_psi_angles = physics_metrics.compute_pseudo_dihedrals(protein_model.coords)
logs = {key: [] for key in get_log_keys()}
all_triggered_force_messages = []
dag_log_events = []

for step in range(NUM_STEPS):
    optimizer_coords.zero_grad()
    optimizer_gamma.zero_grad()
    current_coords = protein_model.coords.clone()
    
    # --- Full Metrics Calculation ---
    entropy_tensor = physics_metrics.compute_entropy(current_coords)
    phi_tensor, psi_tensor = physics_metrics.compute_pseudo_dihedrals(current_coords)
    phi_rms = phi_tensor.std().item() if phi_tensor.numel() > 0 else 0.0
    rmsd_aligned, aligned_coords = physics_metrics.compute_rmsd(current_coords, native_coords_tensor)
    betti1_count = physics_metrics.compute_betti1_count(current_coords, N_RESIDUES)
    
    # --- Update Histories ---
    metrics_history.entropy_history.append(entropy_tensor.item())
    metrics_history.gamma_bar_history.append(gamma_bar.item())
    metrics_history.phi_rms_history.append(phi_rms)
    metrics_history.betti_history.append(betti1_count)
    
    # --- Calculate Betti Lifetime ---
    betti_threshold = GLOBAL_CONSTANTS.get('topological_gating', {}).get('betti_threshold', 8)
    betti1_lifetime = metrics_history.get_betti1_lifetime(threshold=betti_threshold)
    
    d2s_dt2 = np.gradient(np.gradient(np.array(metrics_history.entropy_history)))[-1] if len(metrics_history.entropy_history) >= 3 else 0.0
    
    # --- Populate Metrics & Update DAG ---
    metrics_for_dag = {'betti1_count': betti1_count}
    step_active_params, new_dag_logs, dag_transition_triggered = dag_engine.update_and_get_params(metrics_for_dag, metrics_history, step)
    dag_log_events.extend(new_dag_logs)
    current_phase_name = dag_engine.get_current_phase_name()
    
    # --- ForceField Calculation ---
    metrics_for_physics = {'gamma_bar': gamma_bar.item(), 'phi_rms': phi_rms, 'd2S_dt2': d2s_dt2, 'betti1_count': betti1_count}
    
    # ✅ Standardized Call Site
    total_loss, individual_losses, triggered_force_messages = force_field.calculate_total_force_loss(
        current_coords,
        phi_tensor,
        psi_tensor,
        gamma_bar,
        residue_types,
        charges_tensor,
        step_active_params,
        metrics_for_physics,
        metrics_history,
        current_phase_name,
        step
    )
    all_triggered_force_messages.extend(triggered_force_messages)
    if total_loss.requires_grad: total_loss.backward()
    optimizer_coords.step()
    optimizer_gamma.step()
    with torch.no_grad():
        gamma_bar.clamp_min_(GLOBAL_CONSTANTS.get('gamma_base', 1.0))
    
    # --- Robust Logging Block ---
    logs["step"].append(step)
    logs["current_phase"].append(current_phase_name)
    logs["rmsd"].append(rmsd_aligned)
    logs["phi_rms"].append(phi_rms)
    logs["gamma_bar"].append(gamma_bar.item())
    logs["d2S_dt2"].append(d2s_dt2)
    logs["betti1_count"].append(betti1_count)
    logs["dag_transition_triggered"].append(1 if dag_transition_triggered else 0)
    logs["betti1_lifetime"].append(betti1_lifetime)
    logs["contact_springs_active"].append(individual_losses.get('contact_springs_active', 0))
    logs["total_loss"].append(total_loss.item())
    
    for key in FORCE_LOSS_KEYS:
        logs[key].append(individual_losses.get(key, 0.0))

    if step % LOG_INTERVAL == 0 and step > 0:
        print(f"\n--- TRUSTED STATE @ Step {step} | Phase: {current_phase_name} ---")
        print(f"  RMSD: {rmsd_aligned:.3f} | Loss: {total_loss.item():.4f} | γ̄: {gamma_bar.item():.3f} | B₁: {betti1_count} (Lifetime: {betti1_lifetime})")

# --- Finalization and Charting Block ---
end_time = time.time()
print(f"\n--- Simulation Finished in {end_time - start_time:.2f} seconds ---")

if not logs["step"]:
    print("Simulation ended before any steps were logged. No summary generated.")
else:
    # --- Save Summary Log ---
    force_log_path = os.path.join(output_plots_dir, f"forces_log_{PATCH_ID}.txt")
    with open(force_log_path, 'w') as f:
        f.write(f"--- UQCF-GEM Force Activation Log ---\n")
        f.write(f"Patch ID: {PATCH_ID}\n\n")
        f.write("--- Final State Summary ---\n")
        f.write(f"  Final RMSD: {logs['rmsd'][-1]:.4f} Å\n")
        f.write(f"  Final γ̄: {logs['gamma_bar'][-1]:.4f}\n")
        f.write(f"  Final φ_RMS: {logs['phi_rms'][-1]:.4f}\n")
        f.write(f"  Final Betti₁ Count: {logs['betti1_count'][-1]}\n")
        f.write(f"  Final Betti₁ Lifetime: {logs['betti1_lifetime'][-1]}\n")
        f.write(f"  Final Phase: {logs['current_phase'][-1]}\n\n")
        f.write("--- Force Field Activations (Unique) ---\n")
        unique_ff_messages = sorted(list(set(all_triggered_force_messages)))
        for line in unique_ff_messages: f.write(f"- {line}\n")
        f.write("\n--- DAG Engine Log ---\n")
        for line in dag_log_events: f.write(line + "\n")
    print(f"Saved Summary Log to: {force_log_path}")

    # --- Save Verbose Timeseries CSV ---
    csv_log_path = os.path.join(output_plots_dir, f"diagnostics_timeseries_{PATCH_ID}.csv")
    max_len = max(len(v) for v in logs.values())
    for key, val in logs.items():
        if len(val) < max_len:
            padding_value = np.nan if not val or isinstance(val[0], (int, float)) else 'N/A'
            logs[key].extend([padding_value] * (max_len - len(val)))
    log_rows = [dict(zip(logs.keys(), i)) for i in zip(*logs.values())]
    try:
        with open(csv_log_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=logs.keys())
            writer.writeheader()
            writer.writerows(log_rows)
        print(f"Saved Verbose Timeseries CSV to: {csv_log_path}")
    except Exception as e:
        print(f"Error writing CSV log: {e}")

    # --- Generate All Charts ---
    chart_engine.generate_all_charts(
        final_coords_np=aligned_coords.cpu().numpy(),
        native_coords_np=native_coords_tensor.cpu().numpy(),
        RMSD=logs['rmsd'][-1],
        logs=logs,
        final_contact_map_np=physics_metrics.compute_contact_map(current_coords, GLOBAL_CONSTANTS['contact_dist']).cpu().numpy(),
        initial_pseudo_phi_angles=initial_pseudo_phi_angles.cpu().numpy(),
        initial_pseudo_psi_angles=initial_pseudo_psi_angles.cpu().numpy(),
        final_pseudo_phi_angles=phi_tensor.detach().cpu().numpy(),
        final_pseudo_psi_angles=psi_tensor.detach().cpu().numpy()
    )
