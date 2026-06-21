# UQCF-GEM Gate A Small-Network Phi Simulation

This package is a small, reproducible demonstration of the Gate A finding:

1. **Bare Genesis/source anchoring + conservation does not select a unique Phi.**
2. **Network-only Hodge/minimum-action selection does not close Phi canonically unless W is itself derived.**
3. **Observer/interaction response closes Phi when `rank(RZ)=dim(Z)`.**

## Run

```bash
python uqcf_gate_a_small_network_phi_simulation.py
```

This creates a `gate_a_outputs/` directory containing CSV evidence tables, plots, and a short report.

## Dependencies

```bash
pip install numpy pandas matplotlib
```

## Claim boundary

This is a finite graph source-current identifiability simulation. It does **not** claim to derive physical spacetime, ADM, or GR.
