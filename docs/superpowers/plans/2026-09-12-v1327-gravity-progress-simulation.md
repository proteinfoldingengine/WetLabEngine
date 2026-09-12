# v13.27 Gravity Progress Simulation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a deterministic six-qubit full-stack visualization of the current UQCF-GEM route from pre-time quantum relations through metric-affine/ADM-like diagnostics to the explicit RGCL gravity-coupling gap.

**Architecture:** A small pure-NumPy scientific core computes exact finite density matrices and reductions, BKM information metrics, polar relational transport, nonmetricity, holonomy, source-current balance, projective coupling controls, and DeWitt-sign diagnostics. A separate Matplotlib renderer consumes telemetry and exports PNG/GIF/MP4 without feeding visualization choices back into the science.

**Tech Stack:** Python 3.10+, NumPy, Matplotlib, Pillow, pytest; optional ffmpeg for MP4.

**Spec:** `docs/superpowers/specs/2026-09-12-v1327-gravity-progress-simulation-design.md`

## Global Constraints

- No physical-time primitive; animation parameter is `lambda_source` and must be labeled “not physical time”.
- No Newton force law or Einstein field equation may be inserted into the simulation dynamics.
- Visualization embedding is abstract and non-spatial.
- Every scientific output is classified as `DERIVED`, `CONDITIONAL`, `CONTROLLED_CORRESPONDENCE`, or `MISSING_LAW`.
- Randomness is fixed by an explicit seed; default seed `1327`.
- Exact finite quantum state dimension is `2^6=64` by default.
- Video encoding is optional; numerical verification must not depend on ffmpeg.

---

### Task 1: Core linear algebra and exact quantum source family

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/__init__.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/linalg.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/tests/test_quantum.py`

**Interfaces:**
- Produces `paulis()`, `embed_local()`, `embed_pair()`, `hermitian_exp_normalized()`, `hermitian_log()`, `partial_trace()`, `build_default_model()`, `state_at_lambda()`, `one_site_reductions()`, `pair_reduction()`, `bkm_covariance()`, `connected_correlation()`.

- [ ] Write tests first for trace-one positivity, partial-trace dimensions, BKM symmetry/PSD, and exact PGRL reparameterization.
- [ ] Run `pytest tests/test_quantum.py -v` and confirm RED because modules do not exist.
- [ ] Implement Hermitian eigendecomposition utilities and exact tensor embedding.
- [ ] Implement six-qubit Hamiltonian and two-lobe source generator.
- [ ] Implement exact reductions and BKM logarithmic-mean covariance.
- [ ] Re-run quantum tests and require PASS.

### Task 2: Retained transport, nonmetricity, holonomy, and QMAR jets

**Files:**
- Create: `.../uqcf_demo/geometry.py`
- Create: `.../tests/test_geometry.py`

**Interfaces:**
- Consumes one-site BKM metrics and pair connected correlations.
- Produces `proper_polar()`, `edge_geometry()`, `cycle_holonomy()`, `so3_angle()`, `finite_difference_geometry_jet()`.

- [ ] Write tests asserting `O^T O=I`, `det O=+1`, symmetric nonmetricity, identity-loop angle zero, and finite QMAR jet values.
- [ ] Verify RED.
- [ ] Implement proper polar decomposition by SVD with determinant correction.
- [ ] Implement `M_ij=K_j-O^T K_i O` and cycle products.
- [ ] Implement central finite differences in `lambda_source` without interpreting the derivative as time.
- [ ] Verify GREEN.

### Task 3: Source-current, projective coupling, and ADM-like diagnostic

**Files:**
- Create: `.../uqcf_demo/source_current.py`
- Create: `.../uqcf_demo/adm.py`
- Create: `.../tests/test_source_adm.py`

**Interfaces:**
- Produces `incidence_matrix()`, `cycle_basis()`, `balanced_source()`, `minimum_norm_current()`, `conditional_response_selected_current()`, `projective_direction()`, `represented_q()`, `dewitt_diagnostic()`, `dewitt_controls()`.

- [ ] Write failing tests for `BJ=s`, `BZ=0`, positive-scale projective invariance, and DeWitt negative pure-trace / nonnegative traceless controls.
- [ ] Verify RED.
- [ ] Implement SVD null-space basis and minimum-norm current.
- [ ] Implement a clearly labeled conditional response-selection witness using only precomputed edge-response telemetry.
- [ ] Implement `q=(K+eps I)^-1` and basis-invariant DeWitt trace/traceless decomposition.
- [ ] Verify GREEN.

### Task 4: Deterministic telemetry engine and claim ledger

**Files:**
- Create: `.../uqcf_demo/ledger.py`
- Create: `.../uqcf_demo/simulation.py`
- Create: `.../tests/test_simulation.py`

**Interfaces:**
- Produces `run_telemetry(config) -> dict`, `telemetry_hash(dict) -> str`, `claim_ledger() -> list[dict]`.

- [ ] Write tests requiring a stable hash for identical seed/config and changed hash when source amplitude changes.
- [ ] Verify RED.
- [ ] Sweep 25 default `lambda_source` values from `-0.8` to `0.8`.
- [ ] Record state minimum eigenvalue, BKM eigenvalue floor, mean nonmetricity, cycle-curvature angles, balance residual, current norm, QMAR jet norm, DeWitt diagnostic, projective-ray control, and RGCL gap marker.
- [ ] Canonicalize floats before SHA-256 hashing.
- [ ] Verify GREEN and runtime target.

### Task 5: Renderer and CLI exports

**Files:**
- Create: `.../uqcf_demo/render.py`
- Create: `.../run_simulation.py`
- Create: `.../requirements.txt`

**Interfaces:**
- `python run_simulation.py --quick --no-video` generates JSON/CSV/PNG.
- `python run_simulation.py --frames 60` additionally attempts GIF and MP4.

- [ ] Write a smoke test that renders one final frame with the non-time label and expected four panel titles.
- [ ] Verify RED.
- [ ] Implement abstract circular/chordal graph embedding with no physical-distance interpretation.
- [ ] Implement 1920x1080 four-panel final frame and animation.
- [ ] Export GIF with Pillow; detect ffmpeg before MP4 attempt.
- [ ] Verify smoke test and numerical tests remain GREEN.

### Task 6: Mathematics, claim boundaries, X update, and packaged verification

**Files:**
- Create: `.../README.md`
- Create: `.../MATH_AND_PHYSICS.md`
- Create: `.../CLAIM_BOUNDARIES.md`
- Create: `.../X_UPDATE.md`
- Create: `.../CHECKER.py`
- Create: `.../EXPECTED_RESULTS.json`

**Interfaces:**
- `python CHECKER.py` reruns quick telemetry and verifies structural thresholds plus deterministic hash.

- [ ] Run the full non-video simulation locally and capture numerical results.
- [ ] Write `EXPECTED_RESULTS.json` from that execution, not from desired outcomes.
- [ ] Write checker thresholds around structural invariants, not aesthetic output.
- [ ] Document equations and distinguish finite retained holonomy from physical spacetime curvature.
- [ ] Write X copy that says “potential gravity route” / “gravity-like structure” while explicitly preserving RGCL and Einstein-closure boundaries.
- [ ] Run `pytest -q` and `python CHECKER.py`; require both pass.
- [ ] Compare research branch to `main`; require only intended docs/demo files.
- [ ] Fast-forward `main` only after verification.
