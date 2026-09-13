# UQCF-GEM v13.27 — A Finite Quantum-Relational Path and a Projective Coupling Obstruction

This repository artifact implements a reproducible six-qubit laboratory for testing a possible route from finite quantum relations toward geometric and source-coupling structure.

It does **not** claim that gravity, spacetime, ADM dynamics, or the Einstein equations have been derived. Its scientific value is narrower and testable: it exhibits a concrete executable path, identifies which structures arise inside that model, audits the modeling choices, and proves where the frozen source-selection rules become underdetermined.

## Central result: fixed-state projective homogeneity obstruction

At a fixed state/tangent point, hold the graph, incidence matrix, cycle basis and state-point geometry fixed. The source/current selection uses a minimum-norm solution and a cycle-space response fit. Under positive source-tangent rescaling

\[
(s,y)\mapsto(c s,c y),\qquad c>0,
\]

the selected quantities scale as

\[
J_0\mapsto cJ_0,\qquad a_*\mapsto ca_*,\qquad J\mapsto cJ.
\]

Therefore any coupled-source representative produced by these degree-one rules obeys

\[
\Sigma\mapsto c\Sigma.
\]

The frozen construction determines at most the ray

\[
[\Sigma]=\{c\Sigma:c>0\},
\]

not its nonzero magnitude.

This is a theorem about the **selection rules at a fixed state/tangent point**. It is not a claim that rescaling the source generator `P` at fixed `lambda` leaves the full state family or its geometry invariant.

## Why the path remains interesting

The executable chain is:

```text
exact six-qubit thermal/source family
-> exact one- and two-site reductions
-> local BKM information metrics
-> connected pair correlations
-> audited O(3) polar factors
-> declared orientation-preserving SO(3) projection
-> state-dependent metric mismatch
-> finite SO(3) loop holonomy diagnostics
-> balanced graph source/current equation
-> conditional cycle-current witness
-> represented q and DeWitt-like quadratic-form diagnostic
-> projective source-coupling obstruction
```

No Newtonian inverse-square law is inserted. No Einstein equation or Einstein residual is used to generate, tune, or select the construction.

The novelty claim is therefore about the **integrated, executable route and the obstruction it exposes**, not about novelty of BKM metrics, polar decomposition, incidence currents, holonomy, or DeWitt-type forms individually.

## Peer-review audit results

### Raw polar determinant

For every edge, the code now records the unconstrained closest orthogonal polar factor before forcing proper orientation.

The canonical 25-frame run contains `25 x 8 = 200` edge/frame samples.

```text
raw O(3) polar factors with det < 0: 200 / 200
reflection fraction:                 1.0
```

This is an important boundary: the `SO(3)` transports used in the loop calculation are an **explicit orientation-preserving projection choice**. They are not uniquely forced by the raw polar decomposition in this example.

### Pre-clip holonomy

For each chosen `SO(3)` loop product `H_C`, the code records

\[
x_C=(\operatorname{Tr}H_C-1)/2
\]

before clipping to `[-1,1]`.

The canonical scan gives:

```text
pi holonomy events:                  8
clip events above 1e-12:             0
maximum clip excess:                 ~2.22e-16
adjudication:                         GENUINE_PI_WITHIN_TOLERANCE_NO_CLIP
```

So the observed `theta=pi` events are not meaningful clipping artifacts at the declared threshold. They remain finite group-angle diagnostics conditional on the chosen `SO(3)` projection—not Riemann curvature or a continuum curvature density.

## What is derived, conditional, controlled, or missing

**Derived inside the finite model**

- faithful finite source family;
- one-site BKM information metrics;
- connected pair-correlation tensors;
- raw O(3) polar-factor audit;
- state-dependent metric mismatch after the declared SO(3) projection;
- finite loop group diagnostics;
- balanced graph source/current relation;
- the fixed-state projective homogeneity obstruction.

**Conditional / modeling choices**

- the graph, couplings, beta and source support are fixed inputs;
- BKM is a declared information metric rather than a uniqueness theorem;
- the proper-rotation `SO(3)` transport is explicitly imposed after the raw-polar audit;
- cycle-current selection uses a declared response aperture;
- the resulting graph current is not physical stress-energy.

**Controls, not emergent physics**

- the `D=-4.5` pure-trace and `D=2` traceless DeWitt-like sign values are algebraic identities / implementation controls;
- the matrix-block distance is a toy underdetermination control, not a `T_{mu nu}` reconstruction;
- the four-panel animation is a dashboard of the construction, not evidence by itself.

**Not derived**

- physical space or spacetime;
- physical time (`lambda_source` is not time);
- a Lorentzian coframe;
- physical stress-energy;
- lapse, shift, Hamiltonian or diffeomorphism constraints;
- an ADM constraint algebra;
- an absolute gravitational coupling;
- Einstein equations.

## The next scientific question

`RGCL` is shorthand for the still-missing requirement: an independently motivated, target-blind source→geometry pairing that fixes the appropriate source type and a non-arbitrary coupling magnitude before any Einstein/Newton comparison is consulted.

The next gate is **not** “write RGCL.” It is to audit named candidate pairings already motivated by the frozen ontology. Only three outcomes are allowed:

```text
DERIVED
OBSTRUCTED
REQUIRES_NEW_AXIOM
```

A no-go in the frozen ontology **or** a repair that succeeds only by inserting a freely chosen dimensionful multiplier counts as failure of the target-blind derivation at that point.

## Quick start

```bash
python -m pip install -r requirements.txt
python run_simulation.py --quick --no-video
```

Canonical static telemetry:

```bash
python run_simulation.py --frames 25 --no-video
```

Canonical animation:

```bash
python run_simulation.py --frames 25 --fps 6
```

## Outputs

- `outputs/summary.json` — complete machine-readable telemetry, audit results and claim ledger;
- `outputs/telemetry.csv` — per-frame scalar and audit telemetry;
- `outputs/final_frame.png` — 1920x1080 summary dashboard;
- `outputs/gravity_progress.gif` — historical filename retained for provenance;
- `outputs/gravity_progress.mp4` — historical filename retained for provenance.

Generated binary outputs are reproducibility artifacts, not source-of-truth inputs. The code regenerates them.

## Verification

```bash
PYTHONPATH=. pytest -q
python CHECKER.py
```

`CHECKER.py` reruns the canonical 25-frame calculation and checks the structural gates, the new polar/holonomy audits, and the portable scientific fingerprint. The full raw telemetry hash remains an archival numerical diagnostic because machine-epsilon LAPACK/SVD differences can alter raw floating-point representatives without changing the audited scientific invariants.

Authoritative frozen values are recorded in `EXPECTED_RESULTS.json`.

## Review history and supporting notes

- `MATH_AND_PHYSICS.md` — equations, theorem statement, transport audit and claim boundaries;
- `CLAIM_BOUNDARIES.md` — concise derived/assumed/conditional/missing classification;
- `REVIEW.md` — first methods/claims peer review;
- `AUTHOR_RESPONSE.md` — response to Review 1;
- `REVIEW_2.md` — second referee round checking whether the response was actually executed;
- `AUTHOR_RESPONSE_2.md` — response making the five-item minimum revision binding;
- `X_UPDATE.md` — public language aligned with this rescope;
- `EXPECTED_RESULTS.json` — frozen certified result.

## Journal-facing abstract

> We implement a reproducible six-qubit thermal family and extract local BKM information metrics, audited polar-factor transports, state-dependent metric mismatch, finite SO(3) loop holonomy diagnostics, and a balanced graph current without using Newtonian or Einstein equations as selectors. At a fixed state/tangent point, the retained source-selection rules are positively homogeneous, so the coupled source is determined only up to positive scale. A new audit shows that all 200 sampled unconstrained polar factors are reflections, making the subsequent SO(3) projection an explicit modeling choice; the observed pi loop angles are not attributable to clipping at the declared tolerance. Absolute gravitational coupling, spacetime emergence, and physical Einstein closure are not obtained.

## Bottom line

The artifact supports a **novel and falsifiable path worth investigating**:

\[
\text{quantum relations}
\to\text{information geometry}
\to\text{declared relational transport}
\to\text{group/metric diagnostics}
\to\text{balanced source structure}
\to\text{projective coupling obstruction}.
\]

It does not claim the destination has already been reached.
