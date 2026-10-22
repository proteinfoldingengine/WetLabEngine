# physics_constants.py

import numpy as np
import math

# --- Sequence and Hydrophobicity Definitions ---
SEQUENCE_1UBQ = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
HYDROPHOBIC_RESIDUES = {'A', 'V', 'I', 'L', 'M', 'F', 'W', 'Y', 'C'}

# --- Core Configuration ---
memory_window = 150
eps = 1e-6

# --- PATCH 602.0: Purified Relational Physics Parameters ---
# These parameters govern the relationships between observables, not fixed thresholds.

# Base tolerance for topological stability, modulated by the coherence field (gamma_bar).
COHERENCE_STABILITY_TOLERANCE_BASE = 1.0
# Small epsilon for detecting thermodynamic freeze-out (dynamic flatness).
THERMODYNAMIC_STALL_EPSILON = 1e-5

# --- Core Force and Feedback Parameters ---
k_contact_spring_base = 0.30
k_df_funnel = 8000.0
k_entropy_pulse = 1.5
k_gamma_surge = 2.0
k_phi_torque_base = 1.0
k_lj_repulsion_base = 0.1
gamma_base = 1.0
contact_dist = 6.0
contact_permanence_window = 50
torque_boost_factor = 2.0
gamma_feedback_max_gain = 5.0
df_target_base = 2.5
df_target_max = 2.8
gamma_max = 3.0
NATIVE_CONTACT_DISTANCE_THRESHOLD = 4.5 # For diagnostic metric only


# --- GLOBAL_PHYSICS_CONSTANTS population ---
GLOBAL_PHYSICS_CONSTANTS = {
    'memory_window': memory_window, 'eps': eps,
    'SEQUENCE_1UBQ': SEQUENCE_1UBQ,
    'HYDROPHOBIC_RESIDUES': HYDROPHOBIC_RESIDUES,

    # Patch 602.0
    'COHERENCE_STABILITY_TOLERANCE_BASE': COHERENCE_STABILITY_TOLERANCE_BASE,
    'THERMODYNAMIC_STALL_EPSILON': THERMODYNAMIC_STALL_EPSILON,

    # Core Forces
    'k_contact_spring_base': k_contact_spring_base,
    'k_df_funnel': k_df_funnel,
    'k_entropy_pulse': k_entropy_pulse,
    'k_gamma_surge': k_gamma_surge,
    'k_phi_torque_base': k_phi_torque_base,
    'k_lj_repulsion_base': k_lj_repulsion_base,
    'gamma_base': gamma_base,
    'contact_dist': contact_dist,
    'contact_permanence_window': contact_permanence_window,
    'torque_boost_factor': torque_boost_factor,
    'gamma_feedback_max_gain': gamma_feedback_max_gain,
    'df_target_base': df_target_base,
    'df_target_max': df_target_max,
    'gamma_max': gamma_max,
    'NATIVE_CONTACT_DISTANCE_THRESHOLD': NATIVE_CONTACT_DISTANCE_THRESHOLD,
}
