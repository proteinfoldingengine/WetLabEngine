# UQCF-GEM v13.27 Full-Stack Gravity Progress Simulation

This package turns the current retained Path-A research stack into one deterministic executable simulation and one visual narrative.

It is designed to answer a narrow question:

> How far can the current finite quantum-relational machinery be pushed toward gravity-like geometric structure **without inserting a gravitational force law or using an Einstein residual as a selector?**

## What it simulates

```text
exact 6-qubit relational state
-> PGRL/ETL source family
-> exact local and pair reductions
-> BKM information metrics
-> connected pair correlations
-> SO(3) polar transports
-> discrete nonmetricity
-> loop holonomy / curvature proxy
-> balanced source/current flow
-> conditional cycle-current selection witness
-> represented q=A^-1
-> DeWitt-sign ADM-like diagnostic
-> projective Sigma = kappa T boundary
-> RGCL missing / physical Einstein closure open
```

The animation parameter is a **source-family coordinate, not physical time**. The graph embedding is abstract and is **not physical space**.

## Quick start

```bash
python -m pip install -r requirements.txt
python run_simulation.py --quick --no-video
```

Full static telemetry:

```bash
python run_simulation.py --frames 25 --no-video
```

Full animation:

```bash
python run_simulation.py --frames 25 --fps 6
```

When `ffmpeg` is installed this writes both H.264 MP4 and GIF. Without ffmpeg the GIF still works through Pillow.

## Outputs

`outputs/summary.json` contains the complete machine-readable telemetry and claim ledger. `outputs/telemetry.csv` contains one row per source-family frame. `outputs/final_frame.png` is the 1920×1080 summary view. Video mode additionally writes `gravity_progress.gif` and, when possible, `gravity_progress.mp4`.

Generated binary outputs are intentionally not required for source control; the deterministic code regenerates them.

## Executed default result

The canonical 25-frame run produced:

```text
scientific_fingerprint               6f2830c47a877676f6ff4ad028769bb285d00f9194f33035c85dd785b3e9f5b6
reference raw telemetry hash         e994538f3e04a06270b17b66c21ee29dc07730c5ceaf0805ba412f754624f945
min global-state eigenvalue          3.7185106924494124e-05
min local BKM eigenvalue             0.5673128649814877
max source-balance residual          4.611102534756203e-16
max projective direction drift       3.380886602644082e-16
PGRL reparameterization error        9.55170005517049e-16
DeWitt pure-trace control            -4.5
DeWitt traceless control             1.9999999999999982
cycle response-rank deficit          0
RGCL                                 MISSING
physical Einstein closure            OPEN
```

The video generated locally as 25 frames, 1920×1080, H.264, 6 fps.

## Scientific status shown by the four panels

**Pre-time quantum relations.** The network is an abstract layout of quantum factors and relation edges. Node/edge changes come from the exact finite quantum source family.

**Retained metric-affine geometry.** Local BKM metrics and polar relational transports produce nonmetricity defects and finite loop holonomy. The vertical lift is visualization only.

**Source/current + projective coupling.** The graph source is balanced and the selected witness current satisfies `BJ=s` to machine precision. Positive common scaling preserves the ray, directly visualizing the v13.27 coupling-magnitude obstruction.

**ADM-like diagnostics + claim ledger.** The finite `q=A^-1` representation and DeWitt-sign diagnostic are plotted alongside the live scientific ledger so derived results cannot be confused with conditional or missing steps.

## Verification

```bash
PYTHONPATH=. pytest -q
python CHECKER.py
```

`CHECKER.py` reruns the canonical 25-frame telemetry and checks structural tolerances plus a **portable scientific fingerprint** built from rounded invariant observables and gate outcomes. The full raw telemetry hash is still emitted as an archival numerical diagnostic, but it is not used as the cross-machine certification key because LAPACK/SVD representatives can drift at machine epsilon. Video encoding is deliberately excluded from scientific verification.

## Read next

- `MATH_AND_PHYSICS.md` — equations and executed values.
- `CLAIM_BOUNDARIES.md` — what the demo does and does not establish.
- `REVIEW.md` — archived methods/claims peer review recommending revision and rescoping.
- `AUTHOR_RESPONSE.md` — author response, homogeneity lemma, answers to all 24 reviewer questions, and revision commitments.
- `X_UPDATE.md` — public update copy with the original demo claim boundary.
- `EXPECTED_RESULTS.json` — frozen executed result used by the checker.

## Peer-review status

The archived review accepts the artifact as a reproducible finite-model laboratory but recommends that any journal-facing version be rescoped around the **projective source-coupling obstruction**, not presented as a gravity derivation. The author response accepts that rescoping, treats the DeWitt controls as implementation identities rather than emergent ADM evidence, and freezes explicit failure criteria for the next source-to-geometry coupling gate.

No executable scientific result or fingerprint is changed by archiving the review and response.

## Research conclusion

The package demonstrates substantial finite **quantum → information geometry → relational transport → metric-affine/ADM-like structure** in one reproducible model. It does not derive a physical gravitational field equation.

The simulation makes the current missing law explicit:

```text
RGCL — Retained Geometric Coupling Law
```

RGCL must fix the target-blind source-to-coframe/geometric coupling magnitude and tensor type before any physical Einstein closure can be claimed.
