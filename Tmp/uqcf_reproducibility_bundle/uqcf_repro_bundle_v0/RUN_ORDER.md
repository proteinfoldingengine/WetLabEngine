# Run Order

Run these from the `scripts/` directory or with explicit python paths.

1. `python reproduce_baseline_closure.py`
   - Expected: a single selected attractor near gamma ~ 0.273, W ~ 0.431, chi ~ 0.401

2. `python reproduce_selector_refinement.py`
   - Expected: improved selector near gamma ~ 0.2686 using lam_coeff=1.4, q_exp=0.75

3. `python reproduce_observable_proxy.py`
   - Expected: strictly positive F_AP-style shifts from about +0.26% to +0.91% on the locked grid

The outputs are written under `../reproduced/`.
