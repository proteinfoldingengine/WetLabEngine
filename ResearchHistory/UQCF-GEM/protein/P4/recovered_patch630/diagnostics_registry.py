# diagnostics_registry.py
# Patch ID: 624 (Torsional Incoherence Penalty)

from collections import namedtuple

MetricDefinition = namedtuple('MetricDefinition', [
    'key', 'name', 'plot_group', 'plot_type', 'color', 'yscale'
])

DIAGNOSTICS_REGISTRY = [
    MetricDefinition('rmsd', 'RMSD (Å)', 1, 'dual_primary', 'darkred', 'linear'),
    MetricDefinition('phi_rms', 'φ_RMS', 1, 'dual_secondary', 'darkcyan', 'linear'),
    MetricDefinition('current_phase', 'Simulation Phase', 2, 'phase', 'black', 'linear'),
    MetricDefinition('gamma_bar', 'γ̄', 3, 'dual_primary', 'gold', 'linear'),
    MetricDefinition('d2S_dt2', 'd²S/dt²', 3, 'dual_secondary', 'purple', 'symlog'),
    MetricDefinition('betti1_count', 'Betti₁ Count', 4, 'dual_primary', 'darkmagenta', 'linear'),
    MetricDefinition('betti1_lifetime', 'Betti₁ Lifetime (steps)', 4, 'dual_secondary', 'plum', 'linear'),
    MetricDefinition('contact_springs_active', 'Contact Springs Active', 5, 'boolean', 'forestgreen', 'linear'),
    MetricDefinition('gamma_well_loss', 'Gamma Well Loss', 6, 'single', 'orange', 'symlog'),
    
    # ✅ Patch 624: Add new incoherence penalty plot
    MetricDefinition('torsional_incoherence_penalty_loss', 'γ̄–φ RMS Incoherence Loss', 7, 'single', 'darkorange', 'symlog'),
    
    MetricDefinition('total_loss', 'Total Loss', -1, 'single', 'black', 'symlog'),
]

# Keys for all force loss terms that should be logged.
FORCE_LOSS_KEYS = [
    'contact_springs_loss', 'fractal_compaction_funnel_loss', 'gamma_well_loss',
    'angular_torque_locking_loss', 'lennard_jones_repulsion_loss',
    'hydrophobic_collapse_loss', 'screened_electrostatics_loss', 'ramachandran_potential_loss',
    # ✅ Patch 624: Add new loss key
    'torsional_incoherence_penalty_loss'
]

def get_log_keys():
    all_keys = {metric.key for metric in DIAGNOSTICS_REGISTRY}
    all_keys.add('step')
    all_keys.update(FORCE_LOSS_KEYS)
    all_keys.update(['betti1_lifetime', 'contact_springs_active', 'dag_transition_triggered'])
    return list(all_keys)
