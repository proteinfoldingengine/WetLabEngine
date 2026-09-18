# force_field.py
# Patch 629: Multi-Well Ramachandran Potential

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
        
        # Load all parameters from the global constants dictionary
        self.gating_params = self.global_constants.get('topological_gating', {})
        self.betti_threshold = self.gating_params.get('betti_threshold', 8)
        self.force_lifetime_threshold = self.gating_params.get('force_activation_lifetime', 50)

        self.gamma_coherence_threshold = self.global_constants.get('gamma_coherence_threshold', 2.5)
        self.phi_rms_disorder_threshold = self.global_constants.get('phi_rms_disorder_threshold', 1.2)
        
        # ✅ Patch 629: Ramachandran parameters
        self.rama_params = self.global_constants.get('ramachandran_params', {})
        self.rama_alpha_phi = self.rama_params.get('alpha_phi', -1.0)
        self.rama_alpha_psi = self.rama_params.get('alpha_psi', -0.5)
        self.rama_beta_phi = self.rama_params.get('beta_phi', -2.2)
        self.rama_beta_psi = self.rama_params.get('beta_psi', 2.0)
        self.rama_well_sigma_sq = self.rama_params.get('well_sigma', 0.5)**2
        self.rama_activation_betti = self.rama_params.get('activation_betti_min', 500)
        self.rama_activation_gamma = self.rama_params.get('activation_gamma_min', 2.5)
        self.rama_activation_phirms = self.rama_params.get('activation_phirms_min', 1.4)


    def _get_active_param(self, active_params: dict, param_name: str, default_value: float = 0.0) -> float:
        return active_params.get(param_name, default_value)

    # --- ✅ Patch 629: Multi-Well Ramachandran Potential ---
    def apply_ramachandran_potential(self, phi: torch.Tensor, psi: torch.Tensor, active_params: dict) -> torch.Tensor:
        """
        Calculates a multi-well Ramachandran potential based on Gaussian attractors
        for alpha-helical and beta-sheet regions. This is a physics-based potential
        derived from steric constraints, not a heuristic.
        """
        k_rama = self._get_active_param(active_params, 'k_rama')
        if k_rama == 0 or phi.numel() == 0:
            return torch.tensor(0.0, device=self.device)

        # Potential is calculated as 1 minus the sum of Gaussian "rewards"
        # This creates wells at the basin centers. Loss is low inside wells, high outside.
        
        # Alpha-helix basin
        dist_alpha_sq = (phi - self.rama_alpha_phi)**2 + (psi - self.rama_alpha_psi)**2
        reward_alpha = torch.exp(-dist_alpha_sq / self.rama_well_sigma_sq)
        
        # Beta-sheet basin
        dist_beta_sq = (phi - self.rama_beta_phi)**2 + (psi - self.rama_beta_psi)**2
        reward_beta = torch.exp(-dist_beta_sq / self.rama_well_sigma_sq)
        
        # The total reward is the likelihood of being in ANY allowed basin
        total_reward = reward_alpha + reward_beta
        
        # The loss is the average deviation from the ideal reward of 1.0
        loss = k_rama * torch.mean((1.0 - total_reward)**2)
        return loss

    # --- Other forces are unchanged ---
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
        return k_gamma * (gamma_target - gamma_param)**2

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
        
        # --- Physics Gate for Ramachandran Potential ---
        betti1_count = metrics.get('betti1_count', 0)
        gamma_bar_val = gamma_param.item()
        phi_rms_val = metrics.get('phi_rms', 0.0)
        
        rama_gate_active = (
            betti1_count >= self.rama_activation_betti and
            gamma_bar_val >= self.rama_activation_gamma and
            phi_rms_val >= self.rama_activation_phirms
        )

        # Base Forces
        base_forces = {
            'lennard_jones_repulsion': self.apply_lennard_jones(current_coords, active_params),
            'hydrophobic_collapse': self.apply_hydrophobic_collapse(current_coords, residue_types, active_params),
            'angular_torque_locking': self.apply_angular_torque_locking(phi_tensor, psi_tensor, active_params),
            'fractal_compaction_funnel': self.apply_fractal_compaction_funnel(current_coords, active_params),
            'gamma_well': self.apply_coherence_potential_well(gamma_param, metrics, active_params),
        }
        # Conditionally add Ramachandran potential
        if rama_gate_active:
            base_forces['ramachandran_potential'] = self.apply_ramachandran_potential(phi_tensor, psi_tensor, active_params)
            triggered_force_messages.append(f"[RAMA_GATE] Multi-well active (B1={betti1_count}, G={gamma_bar_val:.2f}, P_rms={phi_rms_val:.2f})")

        for name, loss_tensor in base_forces.items():
            if loss_tensor.item() != 0:
                total_loss += loss_tensor
                individual_losses[f'{name}_loss'] = loss_tensor.item()

        # Betti₁ Topology Trigger for Contacts
        betti1_lifetime = metrics_history.get_betti1_lifetime(threshold=self.betti_threshold)
        topology_gate_active = (current_phase == "LockIn" and betti1_count >= self.betti_threshold and betti1_lifetime >= self.force_lifetime_threshold)
        individual_losses['contact_springs_active'] = 1 if topology_gate_active else 0
        
        if topology_gate_active:
            cs_loss = self.apply_contact_springs(current_coords, active_params)
            se_loss = self.apply_screened_electrostatics(current_coords, charges_tensor, active_params)
            total_loss += cs_loss + se_loss
            individual_losses['contact_springs_loss'] = cs_loss.item()
            individual_losses['screened_electrostatics_loss'] = se_loss.item()

        # Torsional Incoherence Penalty
        k_penalty = self._get_active_param(active_params, "k_torsion_penalty")
        if k_penalty > 0 and current_phase == "LockIn":
            incoherence_penalty = k_penalty * \
                                  torch.relu(gamma_param - self.gamma_coherence_threshold) * \
                                  torch.relu(torch.tensor(phi_rms_val, device=self.device) - self.phi_rms_disorder_threshold)
            
            if incoherence_penalty.item() > self.eps:
                total_loss += incoherence_penalty
                individual_losses["torsional_incoherence_penalty_loss"] = incoherence_penalty.item()

        return total_loss, individual_losses, triggered_force_messages
