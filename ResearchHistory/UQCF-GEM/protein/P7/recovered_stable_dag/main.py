# main.py
import torch
import torch.optim as optim
import numpy as np
import os
import sys
import time
from collections import deque

# --- Robust Path and Import Management ---
try:
    from google.colab import drive
    if not os.path.exists('/content/drive'):
        print("Mounting Google Drive...")
        drive.mount('/content/drive')
    BASE_DIR = '/content/drive/My Drive/Folding'
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)
    import physics_constants
    import physics_metrics
    from protein_model import ProteinModel, load_pdb_coords
    # ✅ FIX: Removed the incorrect import of 'coherence_tolerance' which is an internal function.
    from dag_engine import DagEngine, DAG_SCHEMA, _dag_force_mapping
    from chart_utils import FoldingChartEngine
    from force_field import ForceField
    from fractal_dimension_utils import compute_fractal_dimension as compute_df_rigorous, reset_fractal_dimension_state
    from metrics_history import MetricsHistory
    from physics_purity_auditor import run_purity_audit
    print("All project modules imported successfully.")
except (ImportError, ModuleNotFoundError) as e:
    print(f"Could not import project modules. Error: {e}")
    sys.exit(1)

# --- Simulation Configuration ---
GLOBAL_CONSTANTS = physics_constants.GLOBAL_PHYSICS_CONSTANTS
PDB_ID = "1UBQ"; N_RESIDUES = 76; LEARNING_RATE = 0.001
# Using the same patch number as the user's context
PATCH_ID = "Patch 602.4"
NUM_STEPS = 2000
LOG_INTERVAL = 50;
RANDOM_SEED = 42
FORCE_RANDOM_COIL_INIT = True
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"--- UQCF-GEM Engine Initializing ({PATCH_ID}) ---")
print(f"Using device: {DEVICE}")

# --- Physics Purity Audit ---
run_purity_audit(DAG_SCHEMA)

# --- Initialize Model and Optimizer ---
initial_coords_np = load_pdb_coords(PDB_ID, N_RESIDUES, seed=RANDOM_SEED, force_random_coil=FORCE_RANDOM_COIL_INIT)
native_coords_np = load_pdb_coords(PDB_ID, N_RESIDUES, seed=RANDOM_SEED + 1, force_random_coil=False)
initial_coords = torch.tensor(initial_coords_np, dtype=torch.float32, device=DEVICE, requires_grad=True)
native_coords_tensor = torch.tensor(native_coords_np, dtype=torch.float32, device=DEVICE)
protein_model = ProteinModel(initial_coords).to(DEVICE)
gamma_bar = torch.tensor(GLOBAL_CONSTANTS['gamma_base'], device=DEVICE, requires_grad=True)
optimizer = optim.Adam([protein_model.coords, gamma_bar], lr=LEARNING_RATE)

# --- Define Output Directories ---
PATCH_FOLDER_NAME = PATCH_ID.replace(" ", "_").replace(".", "_")
output_plots_dir = os.path.join(BASE_DIR, 'plots', PATCH_FOLDER_NAME)
os.makedirs(output_plots_dir, exist_ok=True)
print(f"Plots will be saved to: {output_plots_dir}")

# --- Initialize Engines and History ---
dag_engine = DagEngine(DAG_SCHEMA, GLOBAL_CONSTANTS, _dag_force_mapping)
chart_engine = FoldingChartEngine(output_dir_base_path=output_plots_dir, current_patch_id=PATCH_ID)
metrics_history = MetricsHistory(memory_window=GLOBAL_CONSTANTS['memory_window'], global_constants=GLOBAL_CONSTANTS)
force_field = ForceField(GLOBAL_CONSTANTS, DEVICE)
reset_fractal_dimension_state()


# --- Main Simulation Loop ---
print(f"\n--- Starting Protein Folding Simulation ({PATCH_ID}) ---")
start_time = time.time()
initial_pseudo_phi_angles_np, initial_pseudo_psi_angles_np, _, _ = physics_metrics.compute_pseudo_dihedrals(protein_model.coords)

# --- State variables for relational metrics ---
dgamma_dt_prev = 0.0
max_phi_rms_variance = 1.0

# --- Log dictionary ---
logs = {
    "step": [], "current_phase": [], "total_loss": [], "rg": [], "entropy": [],
    "df": [], "phi_rms": [], "psi_rms": [], "rmsd": [], "betti1_count": [], "gamma_bar": [],
    "d2S_dt2": [], "dgamma_dt": [], "dphi_rms_dt": [],
    "df_r2": [], "betti1_delta": [],
    "phi_rms_variance": [], "ddf_dt": [], "sustained_entropy_funnel": [], "d2gamma_dt2": [],
    "betti1_delta_persistent": [],
    "rmsd_slope": [], "min_distance": [], "contact_percentage": [], "ramachandran_spread": [],
    "contact_spring_active": [], "entropy_pulse_active": []
}
force_loss_keys = [
    'contact_springs_loss', 'fractal_compaction_funnel_loss',
    'gamma_surge_loss', 'angular_torque_locking_loss',
    'lennard_jones_repulsion_loss', 'entropy_pulse_loss'
]
for key in force_loss_keys:
    logs[key] = []


for step in range(NUM_STEPS):
    optimizer.zero_grad()
    current_coords = protein_model()

    # --- Full Metrics Calculation ---
    rg_tensor = physics_metrics.compute_rg(current_coords)
    entropy_tensor = physics_metrics.compute_entropy(current_coords)
    df_audit_results = compute_df_rigorous(current_coords, step)
    df, df_r2 = df_audit_results['df_value'], df_audit_results['r_squared']
    
    _, _, phi_tensor, psi_tensor = physics_metrics.compute_pseudo_dihedrals(current_coords)
    phi_rms = phi_tensor.std().item() if phi_tensor.numel() > 0 else 0.0
    psi_rms = psi_tensor.std().item() if psi_tensor.numel() > 0 else 0.0
    rmsd_aligned, _ = physics_metrics.compute_rmsd(current_coords, native_coords_tensor)
    betti1_count = physics_metrics.compute_betti1_count(current_coords, N_RESIDUES)
    
    min_distance = physics_metrics.compute_min_inter_residue_distance(current_coords)
    contact_percentage = physics_metrics.compute_contact_percentage(current_coords, GLOBAL_CONSTANTS['NATIVE_CONTACT_DISTANCE_THRESHOLD'])
    ramachandran_spread = physics_metrics.compute_ramachandran_spread_index(phi_tensor, psi_tensor, GLOBAL_CONSTANTS.get('RAMACHANDRAN_REGIONS', {}))
    
    # --- Update Histories ---
    metrics_history.entropy_history.append(entropy_tensor.item())
    metrics_history.gamma_bar_history.append(gamma_bar.item())
    metrics_history.phi_rms_history.append(phi_rms)
    metrics_history.betti_history.append(betti1_count)
    metrics_history.df_value_history.append(df)
    metrics_history.rmsd_history.append(rmsd_aligned)

    # --- Derivative & Stability Metrics for the Purified DAG ---
    d2s_dt2 = np.gradient(np.gradient(np.array(metrics_history.entropy_history)))[-1] if len(metrics_history.entropy_history) >= 3 else 0.0
    dphi_rms_dt = np.gradient(np.array(metrics_history.phi_rms_history))[-1] if len(metrics_history.phi_rms_history) >= 2 else 0.0
    ddf_dt = np.gradient(np.array(metrics_history.df_value_history))[-1] if len(metrics_history.df_value_history) >= 2 else 0.0
    rmsd_slope = np.polyfit(range(len(metrics_history.rmsd_history)), list(metrics_history.rmsd_history), 1)[0] if len(metrics_history.rmsd_history) > 1 else 0.0
    
    dgamma_dt, d2gamma_dt2 = 0.0, 0.0
    if len(metrics_history.gamma_bar_history) >= 3:
        gamma_series = np.array(list(metrics_history.gamma_bar_history))
        dgamma_dt_series = np.gradient(gamma_series)
        dgamma_dt = dgamma_dt_series[-1]
        d2gamma_dt2 = np.gradient(dgamma_dt_series)[-1]

    betti1_delta = np.std(list(metrics_history.betti_history)[-20:]) if len(metrics_history.betti_history) >= 20 else 99.0
    phi_rms_variance = np.var(list(metrics_history.phi_rms_history)[-20:]) if len(metrics_history.phi_rms_history) >= 20 else 99.0
    
    if step < 100:
        max_phi_rms_variance = max(max_phi_rms_variance, phi_rms_variance)

    metrics_history.d2S_dt2_history.append(d2s_dt2)
    metrics_history.betti1_delta_history.append(betti1_delta)
    
    sustained_entropy_funnel = all(s < 0 for s in list(metrics_history.d2S_dt2_history)) and len(metrics_history.d2S_dt2_history) >= GLOBAL_CONSTANTS.get('COMPACT_SUSTAINED_ENTROPY_WINDOW', 50)
    
    # Re-implementing the coherence_tolerance logic locally to avoid the import issue.
    base_tolerance = GLOBAL_CONSTANTS.get('COHERENCE_STABILITY_TOLERANCE_BASE', 1.0)
    current_coherence_tolerance = base_tolerance / (1.0 + gamma_bar.item())
    is_stable_now = betti1_delta < current_coherence_tolerance
    
    metrics_history.betti1_delta_is_stable_history.append(is_stable_now)
    betti1_delta_persistent = all(list(metrics_history.betti1_delta_is_stable_history))

    # --- Populate Metrics for DAG Engine ---
    metrics_for_physics = {
        'step': step, 'df': df, 'gamma_bar': gamma_bar.item(), 'phi_rms': phi_rms,
        'betti1_count': betti1_count, 'rmsd': rmsd_aligned, 'rg': rg_tensor.item(),
        'd2S_dt2': d2s_dt2, 'dphi_rms_dt': dphi_rms_dt, 'dgamma_dt': dgamma_dt, 'ddf_dt': ddf_dt, 'd2gamma_dt2': d2gamma_dt2,
        'df_r2': df_r2, 'betti1_delta': betti1_delta, 'phi_rms_variance': phi_rms_variance,
        'sustained_entropy_funnel': sustained_entropy_funnel,
        'dgamma_dt_prev': dgamma_dt_prev, 'max_phi_rms_variance': max_phi_rms_variance,
        'betti1_delta_persistent': betti1_delta_persistent
    }
    dag_engine.update_phase(metrics_for_physics, step)
    
    dgamma_dt_prev = dgamma_dt
            
    # --- Force Activation & Optimization ---
    step_active_params = dag_engine.active_params.copy()
    total_loss, individual_losses, triggered_force_messages = force_field.calculate_total_force_loss(
        current_coords, phi_tensor, psi_tensor, gamma_bar, entropy_tensor, step_active_params, metrics_for_physics
    )

    if total_loss.requires_grad: total_loss.backward()
    optimizer.step()
    
    with torch.no_grad():
        gamma_bar.clamp_min_(GLOBAL_CONSTANTS.get('gamma_base', 1.0))

    # --- Logging ---
    logs["step"].append(step)
    logs["current_phase"].append(dag_engine.get_current_phase_name())
    logs["total_loss"].append(total_loss.item())
    logs["rmsd"].append(rmsd_aligned)
    logs["rg"].append(rg_tensor.item())
    logs["df"].append(df)
    logs["gamma_bar"].append(gamma_bar.item())
    logs["betti1_count"].append(betti1_count)
    logs["d2S_dt2"].append(d2s_dt2)
    logs["dphi_rms_dt"].append(dphi_rms_dt)
    logs["phi_rms"].append(phi_rms)
    logs["psi_rms"].append(psi_rms)
    logs["entropy"].append(entropy_tensor.item())
    logs["df_r2"].append(df_r2)
    logs["betti1_delta"].append(betti1_delta)
    logs["phi_rms_variance"].append(phi_rms_variance)
    logs["ddf_dt"].append(ddf_dt)
    logs["sustained_entropy_funnel"].append(sustained_entropy_funnel)
    logs["dgamma_dt"].append(dgamma_dt)
    logs["d2gamma_dt2"].append(d2gamma_dt2)
    logs["betti1_delta_persistent"].append(betti1_delta_persistent)
    logs["rmsd_slope"].append(rmsd_slope)
    logs["min_distance"].append(min_distance)
    logs["contact_percentage"].append(contact_percentage)
    logs["ramachandran_spread"].append(ramachandran_spread)
    logs["contact_spring_active"].append('k_contact_spring_base' in step_active_params)
    logs["entropy_pulse_active"].append('k_entropy_pulse' in step_active_params)

    for key in individual_losses:
        if key in logs:
            logs[key].append(individual_losses.get(key, 0.0))

    if step % LOG_INTERVAL == 0 and step > 0:
        print(f"\n--- TRUSTED STATE @ Step {step} | Phase: {dag_engine.get_current_phase_name()} ---")
        print(f"  RMSD: {rmsd_aligned:.3f} | Rg: {rg_tensor.item():.3f} | Df: {df:.3f} (R²={df_r2:.2f}) | γ̄: {gamma_bar.item():.3f}")
        print(f"  Betti1: {betti1_count} (Δ={betti1_delta:.2f}) | d(φ_RMS)/dt: {dphi_rms_dt:.5f} | d²S/dt²: {d2s_dt2:.5f}")
        if triggered_force_messages: print(f"  Active Forces: {', '.join(triggered_force_messages)}")

# --- Finalization and Charting Block ---
end_time = time.time()
print(f"\n--- Simulation Finished in {end_time - start_time:.2f} seconds ---")

if not logs["step"]:
    print("Simulation ended before any steps were logged. No report will be generated.")
else:
    final_coords_np = protein_model().detach().cpu().numpy()
    final_pseudo_phi_angles_np, final_pseudo_psi_angles_np, _, _ = physics_metrics.compute_pseudo_dihedrals(protein_model.coords)
    final_contact_map_tensor = physics_metrics.compute_contact_map(protein_model(), GLOBAL_CONSTANTS['contact_dist'])

    max_len = len(logs['step'])
    for key, val_list in logs.items():
        if len(val_list) < max_len:
            default_val = False if any(k in key for k in ['_active', '_trigger', 'funnel', 'persistent']) else 0.0
            val_list.extend([default_val] * (max_len - len(val_list)))

    chart_engine.generate_all_charts(
        final_coords_np=final_coords_np, native_coords_np=native_coords_np, RMSD=logs['rmsd'][-1],
        initial_pseudo_phi_angles=initial_pseudo_phi_angles_np, initial_pseudo_psi_angles=initial_pseudo_psi_angles_np,
        final_pseudo_phi_angles=final_pseudo_phi_angles_np, final_pseudo_psi_angles=final_pseudo_psi_angles_np,
        final_contact_map_np=final_contact_map_tensor.cpu().numpy(),
        logs=logs,
        GLOBAL_PHYSICS_CONSTANTS=GLOBAL_CONSTANTS
    )
