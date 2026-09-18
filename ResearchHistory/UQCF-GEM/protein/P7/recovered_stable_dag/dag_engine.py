# dag_engine.py
import torch
import numpy as np
from collections import deque
import math
import os

# --- Physics-Based Trigger Functions (Patch 601.0 - Fully Purified) ---

def detect_thermodynamic_stall(metrics: dict, consts: dict) -> bool:
    """Detects if the system has thermodynamically frozen by checking if key derivatives are near zero."""
    eps = consts.get('THERMODYNAMIC_STALL_EPSILON', 1e-5)
    return (abs(metrics.get('d2S_dt2', 1.0)) < eps and
            abs(metrics.get('dgamma_dt', 1.0)) < eps and
            abs(metrics.get('dphi_rms_dt', 1.0)) < eps)

def trigger_initial_relaxation_exit(metrics: dict, consts: dict) -> tuple[bool, str]:
    """
    Transition when coherence begins to grow from a state of kinetic stability.
    This is detected by an inflection point in the coherence field's growth (dγ̄/dt turns positive)
    while torsional variance is low relative to its initial maximum.
    """
    # Failsafe is now based on thermodynamic stall, not step count.
    if detect_thermodynamic_stall(metrics, consts):
        return True, "Thermodynamic stall detected"

    gamma_inflecting = metrics.get('dgamma_dt', 0.0) > 0 and metrics.get('dgamma_dt_prev', 0.0) <= 0
    if not gamma_inflecting:
        return False, f"Coherence not inflecting (dγ̄/dt={metrics.get('dgamma_dt', 0.0):.4f}, prev={metrics.get('dgamma_dt_prev', 0.0):.4f})"

    phi_var_stable = metrics.get('phi_rms_variance', 99.0) < (0.05 * metrics.get('max_phi_rms_variance', 1.0))
    if not phi_var_stable:
        return False, f"Torsion too variant (var={metrics.get('phi_rms_variance', 99.0):.4f} vs max={metrics.get('max_phi_rms_variance', 1.0):.4f})"

    return True, "System organizing: Coherence inflecting from stable torsional state."

def trigger_compaction_exit(metrics: dict, consts: dict) -> tuple[bool, str]:
    """
    Transition when the system shows sustained structural convergence, defined by
    composite stability metrics derived from topology and coherence.
    """
    gamma_bar = metrics.get('gamma_bar', 1.0)
    betti_delta = metrics.get('betti1_delta', 99.0)
    dphi_dt = abs(metrics.get('dphi_rms_dt', 99.0))
    
    # Composite score for topological stability relative to coherence strength.
    betti_stability = 1.0 / (1.0 + betti_delta * gamma_bar)
    # Composite score for kinetic stability.
    torque_flatness = 1.0 / (1.0 + dphi_dt)

    # Note: The 0.8 thresholds here are on composite scores, not raw observables.
    # This is a provisional step towards a fully dynamic relational gate.
    if not (betti_stability > 0.8 and torque_flatness > 0.8 and metrics.get('d2S_dt2', 0.0) < 0):
        return False, f"Convergence not met (BettiStability={betti_stability:.3f}, TorqueFlatness={torque_flatness:.3f}, d²S/dt²={metrics.get('d2S_dt2', 0.0):.3f})"

    return True, "Convergence detected: High topological-coherence stability and entropy funneling."

def trigger_final_lock_in_exit(metrics: dict, consts: dict) -> tuple[bool, str]:
    """
    Transition to a final state when a combined topological-coherence lock-in score
    crosses a critical threshold and the system is thermodynamically frozen.
    """
    gamma_bar = metrics.get('gamma_bar', 1.0)
    betti_delta = metrics.get('betti1_delta', 99.0)
    df = metrics.get('df', 0.0)

    # Composite metric combining coherence, topology, and fractal dimension.
    lock_score = gamma_bar * (1.0 / (1.0 + betti_delta)) * df
    
    # Note: The 1.5 threshold is on a composite score.
    if lock_score < 1.5:
        return False, f"Lock-in score too low ({lock_score:.3f} < 1.5)"

    if not detect_thermodynamic_stall(metrics, consts):
        return False, "System has not reached thermodynamic freeze-out"
        
    return True, f"Coherence Freeze-out: Lock score high ({lock_score:.3f}) and system is frozen."

# --- DAG_SCHEMA ---
DAG_SCHEMA = {
    "phases": [
        { "id": "phase_0", "name": "Initial_Relaxation",
          "exit_condition": trigger_initial_relaxation_exit,
          "activated_forces": ["angular_torque_locking", "lennard_jones_repulsion", "gamma_surge"]
        },
        { "id": "phase_1", "name": "Coherence_Growth_and_Compaction",
          "exit_condition": trigger_compaction_exit,
          "activated_forces": ["gamma_surge", "angular_torque_locking", "lennard_jones_repulsion", "fractal_compaction_funnel", "entropy_pulse"]
        },
        { "id": "phase_2", "name": "Contact_Lock_In",
          "exit_condition": trigger_final_lock_in_exit,
          "activated_forces": ["gamma_surge", "angular_torque_locking", "lennard_jones_repulsion", "fractal_compaction_funnel", "contact_springs", "entropy_pulse"]
        },
    ],
}

_dag_force_mapping = {
    "contact_springs": "k_contact_spring_base", "fractal_compaction_funnel": "k_df_funnel",
    "entropy_pulse": "k_entropy_pulse", "angular_torque_locking": "k_phi_torque_base",
    "lennard_jones_repulsion": "k_lj_repulsion_base", "gamma_surge": "k_gamma_surge",
}

class DagEngine:
    def __init__(self, dag_schema: dict, global_physics_constants: dict, dag_force_mapping: dict):
        self.dag_schema = dag_schema
        self.global_physics_constants = global_physics_constants
        self.dag_force_mapping = dag_force_mapping
        self.current_phase_index = 0
        self.current_phase_name = self.dag_schema["phases"][0]["name"]
        self.active_params = {}
        self._recalculate_active_params()
        self.last_blocked_log_step = -1

    def _check_trigger(self, trigger_func, metrics: dict) -> tuple[bool, str]:
        if not callable(trigger_func): return False, "Invalid trigger: not a function"
        try: return trigger_func(metrics, self.global_physics_constants)
        except Exception as e: return False, f"Error in trigger '{trigger_func.__name__}': {e}"

    def update_phase(self, metrics: dict, step: int):
        current_phase_data = self.dag_schema["phases"][self.current_phase_index]
        exit_trigger_func = current_phase_data.get("exit_condition")
        
        if exit_trigger_func:
            is_triggered, reason = self._check_trigger(exit_trigger_func, metrics)
            if is_triggered:
                if self.current_phase_index == len(self.dag_schema["phases"]) - 1:
                    print(f"\n\033[95m--- [DAG] Final State Achieved @ Step {step} ---\033[0m")
                    print(f"\033[95m--- [DAG] Justification: {reason} ---\033[0m")
                else:
                    next_phase_index = self.current_phase_index + 1
                    self._transition_to_phase(next_phase_index, step, reason)
                return
            else:
                if step > 0 and step % 50 == 0 and self.last_blocked_log_step != step:
                    print(f"[DAG] Phase '{self.current_phase_name}' Blocked @ Step {step} | Reason: {reason}")
                    self.last_blocked_log_step = step

    def _transition_to_phase(self, new_phase_index: int, step: int, reason: str):
        self.current_phase_index = new_phase_index
        self.current_phase_name = self.dag_schema["phases"][self.current_phase_index]["name"]
        print(f"\n\033[92m--- [DAG] Phase Transition -> {self.current_phase_name} (ID: {new_phase_index}) @ Step {step} ---\033[0m")
        print(f"\033[92m--- [DAG] Justification: {reason} ---\033[0m")
        self._recalculate_active_params()

    def _recalculate_active_params(self):
        self.active_params = {}
        current_phase_data = self.dag_schema["phases"][self.current_phase_index]
        for force_group_name in current_phase_data.get("activated_forces", []):
            if force_group_name in self.dag_force_mapping:
                py_var_name = self.dag_force_mapping[force_group_name]
                self.active_params[py_var_name] = self.global_physics_constants.get(py_var_name, 0.0)

    def get_current_phase_name(self):
        return self.current_phase_name
