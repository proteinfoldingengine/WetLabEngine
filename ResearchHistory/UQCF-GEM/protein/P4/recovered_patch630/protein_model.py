# protein_model.py
# Patch 630: Full Backbone Angular Physics

import torch
import torch.nn as nn
import numpy as np
import requests
import io

AA_3_TO_1 = {
    'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
    'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
    'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
    'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'
}

class ProteinModel(nn.Module):
    """
    A PyTorch module representing the protein's full backbone (N, Cα, C) coordinates.
    """
    def __init__(self, N_coords: torch.Tensor, CA_coords: torch.Tensor, C_coords: torch.Tensor):
        super(ProteinModel, self).__init__()
        # Each backbone atom type is now an independent, learnable parameter
        self.N_coords = nn.Parameter(N_coords)
        self.CA_coords = nn.Parameter(CA_coords)
        self.C_coords = nn.Parameter(C_coords)

    def forward(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return self.N_coords, self.CA_coords, self.C_coords

def _generate_ideal_backbone(N_residues: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates an idealized, full-atom backbone from a C-alpha random walk.
    Uses standard bond lengths and angles to place N and C atoms relative to Cα.
    """
    print(f"Generating seeded random coil with full backbone (N, CA, C) using seed {seed}.")
    rng = np.random.default_rng(seed)
    
    # Idealized geometry constants
    N_CA_dist, CA_C_dist, C_N_dist = 1.46, 1.53, 1.33
    CA_C_N_angle, N_CA_C_angle = 2.03, 1.94  # radians

    # 1. Generate C-alpha trace
    ca_coords = np.zeros((N_residues, 3), dtype=np.float32)
    for i in range(1, N_residues):
        vec = rng.standard_normal(3)
        vec /= np.linalg.norm(vec)
        ca_coords[i] = ca_coords[i-1] + vec * 3.8

    n_coords = np.zeros_like(ca_coords)
    c_coords = np.zeros_like(ca_coords)

    # 2. Build the full backbone from the C-alpha trace
    for i in range(1, N_residues - 1):
        v_prev = ca_coords[i-1] - ca_coords[i]
        v_next = ca_coords[i+1] - ca_coords[i]
        
        # Bisector of the Cα angle gives the rough direction for N and C
        bisector = (v_prev / np.linalg.norm(v_prev)) + (v_next / np.linalg.norm(v_next))
        bisector /= np.linalg.norm(bisector)
        
        # Cross product gives the perpendicular axis
        cross_vec = np.cross(v_prev, v_next)
        cross_vec /= np.linalg.norm(cross_vec)

        # Place N and C atoms
        n_coords[i] = ca_coords[i] + N_CA_dist * (np.cos(N_CA_C_angle/2) * bisector + np.sin(N_CA_C_angle/2) * cross_vec)
        c_coords[i] = ca_coords[i] + CA_C_dist * (np.cos(N_CA_C_angle/2) * bisector - np.sin(N_CA_C_angle/2) * cross_vec)

    # Handle endpoints (simplified)
    n_coords[0] = ca_coords[0] + (ca_coords[0] - c_coords[1])
    c_coords[0] = ca_coords[0] + (ca_coords[0] - n_coords[1])
    n_coords[-1] = ca_coords[-1] + (ca_coords[-1] - c_coords[-2])
    c_coords[-1] = ca_coords[-1] + (ca_coords[-1] - n_coords[-2])

    return n_coords, ca_coords, c_coords


def load_full_backbone_coords(pdb_id: str, seed: int = 42, force_random_coil: bool = False) -> tuple[np.ndarray | None, np.ndarray | None, np.ndarray | None, str | None, int]:
    """
    Loads full backbone coordinates (N, Cα, C) and sequence from a PDB ID.
    """
    pdb_url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    print(f"Attempting to download PDB and sequence from: {pdb_url}")

    try:
        response = requests.get(pdb_url, timeout=15)
        response.raise_for_status()
        pdb_content = response.text
        print(f"Successfully downloaded PDB ID: {pdb_id}")

        # --- Parse Sequence ---
        seqres_residues = []
        for line in pdb_content.splitlines():
            if line.startswith("SEQRES"):
                seqres_residues.extend(line[19:70].split())
        sequence_str = "".join([AA_3_TO_1.get(res, 'X') for res in seqres_residues if AA_3_TO_1.get(res)])
        if not sequence_str:
            print("Warning: No SEQRES records found. Aborting.")
            return None, None, None, None, 0
        N_residues = len(sequence_str)

        # --- Generate or Parse Coordinates ---
        if force_random_coil:
            n_coords, ca_coords, c_coords = _generate_ideal_backbone(N_residues, seed)
        else:
            atom_coords = {'N': [], 'CA': [], 'C': []}
            for line in pdb_content.splitlines():
                if line.startswith("ATOM"):
                    atom_name = line[12:16].strip()
                    if atom_name in atom_coords:
                        try:
                            x = float(line[30:38]); y = float(line[38:46]); z = float(line[46:54])
                            atom_coords[atom_name].append([x, y, z])
                        except (ValueError, IndexError): continue
            
            # Basic validation
            if not all(len(coords) == N_residues for coords in atom_coords.values()):
                 print(f"Warning: Atom count mismatch. N({len(atom_coords['N'])}), CA({len(atom_coords['CA'])}), C({len(atom_coords['C'])}), SEQRES({N_residues}). Falling back to random coil.")
                 n_coords, ca_coords, c_coords = _generate_ideal_backbone(N_residues, seed)
            else:
                n_coords = np.array(atom_coords['N'], dtype=np.float32)
                ca_coords = np.array(atom_coords['CA'], dtype=np.float32)
                c_coords = np.array(atom_coords['C'], dtype=np.float32)

        return n_coords, ca_coords, c_coords, sequence_str, N_residues

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDB {pdb_id}: {e}. Aborting.")
        return None, None, None, None, 0
