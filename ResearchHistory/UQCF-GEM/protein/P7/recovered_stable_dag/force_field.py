# force_field.py
import torch
import numpy as np

class ForceField:
    """
    Calculates the total potential energy (loss) of the protein system.
    Contains all individual force application methods, now updated with
    quantum information feedback principles for Patch 520.0.
    """
    def __init__(self, global_constants: dict, device: torch.device):
        self.global_constants = global_constants
        self.device = device

    def _get_active_param(self, active_params: dict, param_name: str, default_value: float = 0.0) -> float:
        """Safely gets a parameter from the active_params dictionary."""
        return active_params.get(param_name, 0.0)

    def apply_contact_springs(self, current_coords: torch.Tensor, active_params: dict, metrics: dict, debug_messages: list) -> torch.Tensor:
        """
        Applies an attractive harmonic potential (spring) weighted by the persistence
        of contacts over time (a proxy for Betti₁ persistence). This reinforces
        stable, emergent topological features.
        """
        k_contact = self._get_active_param(active_params, 'k_contact_spring_base')
        if k_contact == 0:
            return torch.tensor(0.0, device=self.device)

        cutoff = self.global_constants.get('CONTACT_SPRING_CUTOFF', 8.0)
        ideal_dist = self.global_constants.get('CONTACT_SPRING_IDEAL_DIST', 0.0)
        
        persistence_weights = metrics.get("betti1_persistence_weights", None)
        use_weighting = persistence_weights is not None and persistence_weights.shape[0] == current_coords.shape[0]

        dist_matrix = torch.cdist(current_coords, current_coords)
        
        n = current_coords.shape[0]
        mask = torch.ones_like(dist_matrix, dtype=torch.bool)
        mask.fill_diagonal_(False); mask.diagonal(offset=1).fill_(False); mask.diagonal(offset=-1).fill_(False)
        mask &= (dist_matrix < cutoff)
        
        if not mask.any():
            return torch.tensor(0.0, device=self.device)

        if use_weighting:
            weight_matrix = persistence_weights.unsqueeze(1) * persistence_weights.unsqueeze(0)
            spring_weights = weight_matrix[mask]
        else:
            spring_weights = torch.ones_like(dist_matrix[mask])

        relevant_dists = dist_matrix[mask]
        spring_potential = (relevant_dists - ideal_dist) ** 2 * spring_weights
        total_loss = k_contact * torch.sum(spring_potential)
        
        debug_messages.append(f"Contact Springs (k={k_contact:.2f}, weighted={use_weighting})")
        return total_loss

    def apply_fractal_compaction_funnel(self, coords: torch.Tensor, active_params: dict, metrics: dict, debug_messages: list) -> torch.Tensor:
        """
        ✅ PATCH 520.2: The base Df target is now adaptive and passed in via metrics.
        """
        k_df = self._get_active_param(active_params, 'k_df_funnel')
        if k_df == 0: return torch.tensor(0.0, device=self.device)

        df_current = metrics.get("df", 2.0)
        gamma_bar = metrics.get("gamma_bar", 1.0)
        betti_delta = metrics.get("betti1_delta", 99.0)

        # The base target is now dynamic, controlled by the main loop.
        base_target = metrics.get('adaptive_df_target', self.global_constants.get('df_target_base', 2.5))
        max_target = self.global_constants.get('df_target_max', 2.8)
        
        gamma_factor = (gamma_bar - 1.0) / (self.global_constants.get('gamma_max', 3.0) - 1.0)
        stability_factor = 1.0 - min(betti_delta / 5.0, 1.0)

        dynamic_df_target = base_target + (max_target - base_target) * (gamma_factor * stability_factor)
        
        df_delta = dynamic_df_target - df_current
        potential = df_delta ** 2
        loss = k_df * potential
        
        debug_messages.append(f"Fractal Funnel (k={k_df:.1f}, Target Df={dynamic_df_target:.2f})")
        return loss

    def apply_entropy_pulse(self, entropy_tensor: torch.Tensor, active_params: dict, debug_messages: list) -> torch.Tensor:
        """Applies a negative force to entropy to escape informational stalls."""
        k_pulse = self._get_active_param(active_params, 'k_entropy_pulse')
        if k_pulse == 0:
            return torch.tensor(0.0, device=self.device)
        loss = -k_pulse * entropy_tensor
        debug_messages.append(f"Entropy Pulse (k={k_pulse:.2f})")
        return loss

    def apply_gamma_surge(self, gamma_param: torch.Tensor, active_params: dict, metrics: dict, debug_messages: list) -> torch.Tensor:
        """
        Implements Gamma Feedback, amplifying the surge when torsional variance is low.
        """
        k_surge_base = self._get_active_param(active_params, 'k_gamma_surge')
        if k_surge_base == 0: return torch.tensor(0.0, device=self.device)

        phi_rms = metrics.get('phi_rms', 1.0)
        dphi_dt = abs(metrics.get('dphi_rms_dt', 99.0))
        
        k_surge_dynamic = k_surge_base
        if dphi_dt < self.global_constants.get('PHI_RMS_PLATEAU_THRESHOLD', 0.001):
            feedback_gain = 1.0 / (phi_rms**2 + self.global_constants.get('eps', 1e-6))
            feedback_gain = min(feedback_gain, self.global_constants.get('gamma_feedback_max_gain', 5.0))
            k_surge_dynamic *= (1.0 + feedback_gain)

        loss = -k_surge_dynamic * gamma_param
        debug_messages.append(f"Gamma Surge (k_dyn={k_surge_dynamic:.2f})")
        return loss

    def apply_angular_torque_locking(self, phi_tensor: torch.Tensor, psi_tensor: torch.Tensor, active_params: dict, metrics: dict, debug_messages: list) -> torch.Tensor:
        """
        Implements Torque Damping, boosted when motion stagnates or coherence is high.
        """
        k_torque_base = self._get_active_param(active_params, 'k_phi_torque_base')
        if k_torque_base == 0 or phi_tensor.numel() < 2: return torch.tensor(0.0, device=self.device)

        dphi_dt = abs(metrics.get('dphi_rms_dt', 99.0))
        gamma_bar = metrics.get('gamma_bar', 1.0)
        
        k_torque_dynamic = k_torque_base
        # Boost 1: If torsion has plateaued
        if dphi_dt < self.global_constants.get('PHI_RMS_PLATEAU_THRESHOLD', 0.001):
            k_torque_dynamic *= self.global_constants.get('torque_boost_factor', 2.0)
        
        # ✅ PATCH 520.2: Boost 2: If coherence is high and torsion has stalled (Torque Lock-In)
        if (gamma_bar > self.global_constants.get('torque_lock_gamma_threshold', 2.5) and
            dphi_dt < self.global_constants.get('torque_lock_dphi_dt_threshold', 0.0002)):
            k_torque_dynamic *= self.global_constants.get('torque_lock_boost_factor', 1.5)

        phi_mean, psi_mean = phi_tensor.mean(), psi_tensor.mean()
        phi_dev_sq, psi_dev_sq = (phi_tensor - phi_mean)**2, (psi_tensor - psi_mean)**2
        total_loss = k_torque_dynamic * (torch.mean(phi_dev_sq) + torch.mean(psi_dev_sq))
        if total_loss.item() != 0: debug_messages.append(f"Angular Torque (k_dyn={k_torque_dynamic:.2f})")
        return total_loss

    def apply_stabilized_lennard_jones(self, current_coords: torch.Tensor, active_params: dict, metrics: dict, debug_messages: list) -> torch.Tensor:
        k_lj = self._get_active_param(active_params, 'k_lj_repulsion_base')
        if k_lj == 0: return torch.tensor(0.0, device=self.device)
        sigma, r_min, r_soft, eps = 3.5, 1.5, 3.0, 1e-6
        dist_matrix = torch.cdist(current_coords, current_coords)
        mask = torch.triu(torch.ones_like(dist_matrix), diagonal=2)
        r = dist_matrix[mask.bool()]
        potential = torch.where(r < r_min, torch.full_like(r, 1000.0), torch.where(r < r_soft, (sigma / (r + eps)) ** 12, torch.zeros_like(r)))
        total_loss = k_lj * torch.sum(potential)
        if total_loss.item() != 0: debug_messages.append(f"LJ Repulsion (k={k_lj:.2f})")
        return total_loss

    def calculate_total_force_loss(self, current_coords: torch.Tensor, phi_tensor: torch.Tensor, psi_tensor: torch.Tensor, gamma_param: torch.Tensor, entropy_tensor: torch.Tensor, active_params: dict, metrics: dict) -> tuple[torch.Tensor, dict, list]:
        total_loss = torch.tensor(0.0, device=self.device)
        individual_losses = {}
        triggered_force_messages = []
        
        force_methods = {
            'contact_springs': self.apply_contact_springs(current_coords, active_params, metrics, triggered_force_messages),
            'fractal_compaction_funnel': self.apply_fractal_compaction_funnel(current_coords, active_params, metrics, triggered_force_messages),
            'gamma_surge': self.apply_gamma_surge(gamma_param, active_params, metrics, triggered_force_messages),
            'angular_torque_locking': self.apply_angular_torque_locking(phi_tensor, psi_tensor, active_params, metrics, triggered_force_messages),
            'lennard_jones_repulsion': self.apply_stabilized_lennard_jones(current_coords, active_params, metrics, triggered_force_messages),
            'entropy_pulse': self.apply_entropy_pulse(entropy_tensor, active_params, triggered_force_messages),
        }
        for name, loss_tensor in force_methods.items():
            total_loss += loss_tensor
            individual_losses[f'{name}_loss'] = loss_tensor.item()
        return total_loss, individual_losses, triggered_force_messages
