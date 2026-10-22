# dag_engine.py
# Patch ID: 624.1 (Force Activation Fix)

import numpy as np
import math
from collections import deque

DAG_SCHEMA = {
    "phases": [
        { "id": "P0", "name": "Compaction",
          "activated_forces": [
              "lennard_jones_repulsion", "angular_torque_locking", "gamma_well",
              "ramachandran_potential", "fractal_compaction_funnel", "hydrophobic_collapse"
          ]
        },
        { "id": "P1", "name": "LockIn",
          "activated_forces": [
              "lennard_jones_repulsion", "angular_torque_locking", "gamma_well",
              "ramachandran_potential", "fractal_compaction_funnel", "hydrophobic_collapse",
              "screened_electrostatics", "contact_springs",
              # ✅ FIX: Activate the new torsional penalty force during LockIn
              "torsional_incoherence_penalty"
          ]
        },
    ]
}
_dag_force_mapping = {
    "contact_springs": "k_contact_spring_base", "fractal_compaction_funnel": "k_df_funnel",
    "angular_torque_locking": "k_phi_torque_base",
    "lennard_jones_repulsion": "k_lj_repulsion_base", 
    "gamma_well": "k_gamma_surge", # Note: k_gamma_surge now controls the well
    "hydrophobic_collapse": "k_hydro_base", "screened_electrostatics": "k_electrostatic_base",
    "ramachandran_potential": "k_rama",
    # ✅ FIX: Map the new force name to its constant
    "torsional_incoherence_penalty": "k_torsion_penalty"
}


class DagEngine:
    """
    Manages the simulation's progression through phases based on a live
    set of physical observables, ensuring policy-compliant force activation.
    """
    def __init__(self, dag_schema: dict, global_physics_constants: dict, dag_force_mapping: dict):
        self.dag_schema = dag_schema
        self.global_physics_constants = global_physics_constants
        self.dag_force_mapping = dag_force_mapping
        self.current_phase_index = 0
        self.log_buffer = []
        self.gating_params = self.global_physics_constants.get('topological_gating', {})
        self.betti_threshold = self.gating_params.get('betti_threshold', 8)
        self.dag_lifetime_threshold = self.gating_params.get('dag_transition_lifetime', 100)

    def get_current_phase_name(self):
        return self.dag_schema["phases"][self.current_phase_index]["name"]

    def _update_phase(self, metrics: dict, metrics_history, step: int):
        if self.current_phase_index != 0:
            return False

        betti1_count = metrics.get('betti1_count', 0)
        betti1_lifetime = metrics_history.get_betti1_lifetime(threshold=self.betti_threshold)
        
        transition_triggered = (
            betti1_count >= self.betti_threshold and
            betti1_lifetime >= self.dag_lifetime_threshold
        )

        if transition_triggered:
            self.current_phase_index = 1 # Transition to LockIn
            log_msg = (f"[PHYSICS_DAG] Phase Transition: COMPACTION → LOCKIN at step {step}\n"
                       f"  Reason: Betti₁ count = {betti1_count} (>= {self.betti_threshold}) & "
                       f"Betti₁ lifetime = {betti1_lifetime} (>= {self.dag_lifetime_threshold})")
            self.log_buffer.append(log_msg)
            print(f"\033[96m{log_msg}\033[0m")
            return True
        
        return False

    def _recalculate_active_params(self):
        current_phase_data = self.dag_schema["phases"][self.current_phase_index]
        self.active_params = {}
        for force_group_name in current_phase_data.get("activated_forces", []):
            py_var_name = self.dag_force_mapping.get(force_group_name)
            if py_var_name:
                self.active_params[py_var_name] = self.global_physics_constants.get(py_var_name, 0.0)

    def update_and_get_params(self, metrics: dict, metrics_history, step: int):
        self.log_buffer.clear()
        transitioned_this_step = self._update_phase(metrics, metrics_history, step)
        self._recalculate_active_params()
        return self.active_params.copy(), self.log_buffer, transitioned_this_step
