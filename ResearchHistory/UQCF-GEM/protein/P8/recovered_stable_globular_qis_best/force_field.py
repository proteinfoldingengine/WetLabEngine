# force_field.py
# Patch ID: 624.1 (Logging Fix)

import torch

class ForceField:
    """
    Calculates the total potential energy ('loss') of the system.
    This class contains all the physics-based force calculations.
    """
    def __init__(self, global_constants: dict, device: torch.device):
        self.global_constants = global_constants
        self.device = device
        self.eps = self.global_constants.get('eps', 1e-6)
        
        self.gating_params = self.global_constants.get('topological_gating', {})
        self.betti_threshold = self.gating_params.get('betti_threshold', 8)
        self.force_lifetime_threshold = self.gating_params.get('force_activation_lifetime', 50)

        self.gamma_coherence_threshold = self.global_constants.get('gamma_coherence_threshold', 2.5)
        self.phi_rms_disorder_threshold = self.global_constants.get('phi_rms_disorder_threshold', 1.2)

    def _get_active_param(self, active_params: dict, param_name: str, default_value: float = 0.0) -> float:
        return active_params.get(param_name, default_value)

    # --- (Base forces and Betti-gated forces are unchanged) ---
    def apply_lennard_jones(self, coords: torch.Tensor, active_params: dict) -> torch.Tensor:
        k = self._get_active_param(active_params, 'k_lj_repulsion_base')
        if k == 0: return torch.tensor(0.0, device=self.device)
        dist_matrix = torch.cdist(coords, coords)
        sigma = 3.8
        inv_dist_6 = (sigma / (dist_matrix + self.eps))**6
        repulsion = inv_dist_6**2
        return k * torch.mean(repulsion[torch.triu(torch.ones_like(repulsion), diagonal=1).bool()])

    def apply_hydrophobic_collapse(self, coords: torch.Tensor, residue_types: list, active_params: dict) -> torch.Tensor:
        k = self._get_active_param(active_params, 'k_hydro_base')
        if k == 0: return torch.tensor(0.0, device=self.device)
        hydrophobic_indices = [i for i, res in enumerate(residue_types) if res in self.global_constants['HYDROPHOBIC_RESIDUES']]
        if len(hydrophobic_indices) < 2: return torch.tensor(0.0, device=self.device)
        hydrophobic_coords = coords[hydrophobic_indices]
        centroid = hydrophobic_coords.mean(dim=0)
        return k * torch.mean(torch.sum((hydrophobic_coords - centroid)**2, dim=1))

    def apply_ramachandran_potential(self, phi: torch.Tensor, psi: torch.Tensor, active_params: dict) -> torch.Tensor:
        k = self._get_active_param(active_params, 'k_rama')
        if k == 0: return torch.tensor(0.0, device=self.device)
        phi_center = self.global_constants.get('RAMA_PHI_CENTER', 0.0)
        psi_center = self.global_constants.get('RAMA_PSI_CENTER', 0.0)
        return k * (torch.mean((phi - phi_center)**2) + torch.mean((psi - psi_center)**2))
        
    def apply_angular_torque_locking(self, phi: torch.Tensor, psi: torch.Tensor, active_params: dict) -> torch.Tensor:
        k_phi = self._get_active_param(active_params, 'k_phi_torque_base')
        if k_phi == 0: return torch.tensor(0.0, device=self.device)
        return k_phi * (torch.mean(phi**2) + torch.mean(psi**2))

    def apply_fractal_compaction_funnel(self, coords: torch.Tensor, active_params: dict) -> torch.Tensor:
        k_df = self._get_active_param(active_params, 'k_df_funnel')
        if k_df == 0: return torch.tensor(0.0, device=self.device)
        rg = torch.sqrt(torch.mean(torch.sum((coords - coords.mean(dim=0))**2, dim=1)))
        return k_df * rg

    def apply_coherence_potential_well(self, gamma_param: torch.Tensor, metrics: dict, active_params: dict) -> torch.Tensor:
        k_gamma = self._get_active_param(active_params, 'k_gamma_surge')
        if k_gamma == 0: return torch.tensor(0.0, device=self.device)
        gamma_target = self.global_constants.get('gamma_target', 3.0)
        if gamma_param.item() >= gamma_target:
            return torch.tensor(0.0, device=self.device)
        gamma_well_loss = k_gamma * (gamma_target - gamma_param)**2
        return gamma_well_loss

    def apply_screened_electrostatics(self, coords: torch.Tensor, charges: torch.Tensor, active_params: dict) -> torch.Tensor:
        k = self._get_active_param(active_params, 'k_electrostatic_base')
        if k == 0: return torch.tensor(0.0, device=self.device)
        dist_matrix = torch.cdist(coords, coords)
        charge_matrix = charges.unsqueeze(1) * charges
        debye_length = self.global_constants['DEBYE_LENGTH']
        screening = torch.exp(-dist_matrix / debye_length)
        energy = (charge_matrix * screening) / (dist_matrix + self.eps)
        mask = torch.ones_like(energy, dtype=torch.bool).fill_diagonal_(False)
        for i in range(coords.shape[0] - 1):
            mask[i, i+1] = False; mask[i+1, i] = False
        return k * torch.sum(energy[mask]) / 2.0

    def apply_contact_springs(self, coords: torch.Tensor, active_params: dict) -> torch.Tensor:
        k_contact = self._get_active_param(active_params, 'k_contact_spring_base')
        if k_contact == 0: return torch.tensor(0.0, device=self.device)
        contact_dist = self.global_constants['contact_dist']
        dist_matrix = torch.cdist(coords, coords)
        potential_pairs = (dist_matrix < contact_dist).nonzero(as_tuple=False)
        potential_pairs = potential_pairs[potential_pairs[:, 0] < potential_pairs[:, 1]]
        potential_pairs = potential_pairs[potential_pairs[:, 1] > potential_pairs[:, 0] + 3]
        if potential_pairs.numel() == 0: return torch.tensor(0.0, device=self.device)
        i, j = potential_pairs[:, 0], potential_pairs[:, 1]
        dist_seeded = dist_matrix[i, j]
        return k_contact * torch.mean(dist_seeded**2)

    def calculate_total_force_loss(self, current_coords: torch.Tensor, phi_tensor: torch.Tensor, psi_tensor: torch.Tensor, gamma_param: torch.Tensor, residue_types: list, charges_tensor: torch.Tensor, active_params: dict, metrics: dict, metrics_history, current_phase: str, step: int) -> tuple[torch.Tensor, dict, list]:
        total_loss = torch.tensor(0.0, device=self.device)
        individual_losses = {}
        triggered_force_messages = []
        
        base_forces = {
            'lennard_jones_repulsion': self.apply_lennard_jones(current_coords, active_params),
            'hydrophobic_collapse': self.apply_hydrophobic_collapse(current_coords, residue_types, active_params),
            'ramachandran_potential': self.apply_ramachandran_potential(phi_tensor, psi_tensor, active_params),
            'angular_torque_locking': self.apply_angular_torque_locking(phi_tensor, psi_tensor, active_params),
            'fractal_compaction_funnel': self.apply_fractal_compaction_funnel(current_coords, active_params),
            'gamma_well': self.apply_coherence_potential_well(gamma_param, metrics, active_params),
        }
        for name, loss_tensor in base_forces.items():
            if loss_tensor.item() != 0:
                total_loss += loss_tensor
                individual_losses[f'{name}_loss'] = loss_tensor.item()
                # ✅ FIX: Restore logging for base forces
                triggered_force_messages.append(name.replace('_', ' ').title())

        betti1_count = metrics.get('betti1_count', 0)
        betti1_lifetime = metrics_history.get_betti1_lifetime(threshold=self.betti_threshold)
        topology_gate_active = (current_phase == "LockIn" and betti1_count >= self.betti_threshold and betti1_lifetime >= self.force_lifetime_threshold)
        individual_losses['contact_springs_active'] = 1 if topology_gate_active else 0
        
        if topology_gate_active:
            cs_loss = self.apply_contact_springs(current_coords, active_params)
            se_loss = self.apply_screened_electrostatics(current_coords, charges_tensor, active_params)
            total_loss += cs_loss + se_loss
            individual_losses['contact_springs_loss'] = cs_loss.item()
            individual_losses['screened_electrostatics_loss'] = se_loss.item()
            triggered_force_messages.append(f"[TOPO] Contact Springs (B₁={betti1_count})")

        k_penalty = self._get_active_param(active_params, "k_torsion_penalty")
        if k_penalty > 0 and current_phase == "LockIn":
            phi_rms = metrics.get("phi_rms", 0.0)
            
            incoherence_penalty = k_penalty * \
                                  torch.relu(gamma_param - self.gamma_coherence_threshold) * \
                                  torch.relu(torch.tensor(phi_rms, device=self.device) - self.phi_rms_disorder_threshold)
            
            if incoherence_penalty.item() > self.eps:
                total_loss += incoherence_penalty
                individual_losses["torsional_incoherence_penalty_loss"] = incoherence_penalty.item()
                triggered_force_messages.append(f"[PENALTY] Torsional Incoherence (γ̄={gamma_param.item():.2f}, φ_RMS={phi_rms:.2f})")

        return total_loss, individual_losses, triggered_force_messages
