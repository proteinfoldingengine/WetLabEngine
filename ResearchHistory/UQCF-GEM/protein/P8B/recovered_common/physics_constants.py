# physics_constants.py
# Patch ID: 620 (Entropy Pulse & Full Diagnostics Restoration)

import numpy as np
import math

# --- Sequence, Charge, and Hydrophobicity Definitions ---
SEQUENCE_1UBQ = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
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

# --- ✅ RESTORED: QIC-Gated Entropy Pulse Parameters ---
# These constants control the entropy pulse, which helps the simulation
# escape local minima. Its absence was a primary cause of stalls.
K_ENTROPY_BURST = 2.0
QIC_PULSE_GAMMA_MIN = 3.0
QIC_PULSE_PHIRMS_MAX = 1.1
QIC_PULSE_D2S_MAX = -0.05

# --- QIC & QICM Parameters ---
PHI_RMS_QIC_THRESHOLD = 1.25
QIC2_GAMMA_MIN = 3.0
QIC2_PHIRMS_MAX = 1.1
QIC2_BETTI_MIN = 700
QIC2_TORSION_SCORE_MAX = -4.0
KAPPA_DIFF_THRESHOLD = 0.2
PHI_DIFF_THRESHOLD = 0.5


# --- GLOBAL_PHYSICS_CONSTANTS population ---
GLOBAL_PHYSICS_CONSTANTS = {
    'memory_window': memory_window, 'eps': eps,
    'LEARNING_RATE_COORDS': LEARNING_RATE_COORDS,
    'LEARNING_RATE_GAMMA': LEARNING_RATE_GAMMA,
    'SEQUENCE_1UBQ': SEQUENCE_1UBQ,
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
    'QIC_PULSE_GAMMA_MIN': QIC_PULSE_GAMMA_MIN,
    'QIC_PULSE_PHIRMS_MAX': QIC_PULSE_PHIRMS_MAX,
    'QIC_PULSE_D2S_MAX': QIC_PULSE_D2S_MAX,
    'PHI_RMS_QIC_THRESHOLD': PHI_RMS_QIC_THRESHOLD,
    'QIC2_GAMMA_MIN': QIC2_GAMMA_MIN,
    'QIC2_PHIRMS_MAX': QIC2_PHIRMS_MAX,
    'QIC2_BETTI_MIN': QIC2_BETTI_MIN,
    'QIC2_TORSION_SCORE_MAX': QIC2_TORSION_SCORE_MAX,
    'KAPPA_DIFF_THRESHOLD': KAPPA_DIFF_THRESHOLD,
    'PHI_DIFF_THRESHOLD': PHI_DIFF_THRESHOLD,
}
