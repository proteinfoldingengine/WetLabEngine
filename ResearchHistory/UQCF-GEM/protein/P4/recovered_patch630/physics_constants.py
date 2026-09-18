# physics_constants.py
# Patch ID: 626 (Generality)

import numpy as np
import math

# --- Sequence, Charge, and Hydrophobicity Definitions ---
# Protein sequences are now defined in the YAML config files.
# These definitions are fundamental properties of amino acids and thus remain here.
HYDROPHOBIC_RESIDUES = {'A', 'V', 'I', 'L', 'M', 'F', 'W', 'Y', 'C'}
CHARGED_RESIDUES = {'D', 'E', 'K', 'R', 'H'}
RESIDUE_CHARGES = {'D': -1, 'E': -1, 'K': 1, 'R': 1, 'H': 1}

# --- Core Configuration ---
memory_window = 150
eps = 1e-6

# --- Optimization Parameters ---
LEARNING_RATE_COORDS = 0.001
LEARNING_RATE_GAMMA = 0.1 

# --- Core Force and Feedback Parameters ---
k_contact_spring_base = 1.5
k_df_funnel = 6000.0
k_gamma_surge = 2.0
k_phi_torque_base = 1.0
k_lj_repulsion_base = 1.25
gamma_base = 1.0
contact_dist = 8.0
k_hydro_base = 0.75
k_electrostatic_base = 1.0
DEBYE_LENGTH = 5.0
k_rama = 0.05
K_ENTROPY_BURST = 2.0
k_torsion_penalty = 2.0

# --- GLOBAL_PHYSICS_CONSTANTS population ---
GLOBAL_PHYSICS_CONSTANTS = {
    'memory_window': memory_window, 'eps': eps,
    'LEARNING_RATE_COORDS': LEARNING_RATE_COORDS,
    'LEARNING_RATE_GAMMA': LEARNING_RATE_GAMMA,
    'HYDROPHOBIC_RESIDUES': HYDROPHOBIC_RESIDUES,
    'CHARGED_RESIDUES': CHARGED_RESIDUES,
    'RESIDUE_CHARGES': RESIDUE_CHARGES,
    'k_contact_spring_base': k_contact_spring_base,
    'k_df_funnel': k_df_funnel,
    'k_gamma_surge': k_gamma_surge,
    'k_phi_torque_base': k_phi_torque_base,
    'k_lj_repulsion_base': k_lj_repulsion_base,
    'gamma_base': gamma_base,
    'contact_dist': contact_dist,
    'k_hydro_base': k_hydro_base,
    'k_electrostatic_base': k_electrostatic_base,
    'DEBYE_LENGTH': DEBYE_LENGTH,
    'k_rama': k_rama,
    'K_ENTROPY_BURST': K_ENTROPY_BURST,
    'k_torsion_penalty': k_torsion_penalty,
}
