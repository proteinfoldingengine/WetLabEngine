# Protein P7 — Authoritative early-controller source-reduction result

**Decision:** `NO_GO_DISTINCT_EARLY_CONTROLLER_MECHANISM_AS_RECOVERED`

**Certified source-audit head:** `72c6d464cad50183fd17ac932b40745438576331`  
**GitHub Actions:** run `35298063514` — SUCCESS  
**Artifact:** `10528821674`, `protein-p7-source-reduction`  
**Artifact SHA-256:** `c34e49c1ce9f23eae00afa2e0f15b25f15509acc275d4372d5e47726ad33f02d`

The artifact ZIP digest was independently recomputed and matched GitHub's recorded digest.

## Why P7 existed

P6 correctly kept the early Phase-I observable/DAG controller line open because P1/P4/P5 had not directly tested it.

P7 first recovered the historical calling path from Google Drive. That recovery was important: the DAG was real software on the coordinate-update path, not merely an unused class.

The remaining question was whether the recovered native-blind controller contained a genuinely distinct adaptive multi-force mechanism worth a new constrained-backbone experiment.

## Recovered authority

The primary source is the August-3-2025 `StableDAGPhysics` bundle.

Exact source hashes are frozen and the key files are vendored under `recovered_stable_dag/`.

The recovered runner:

- instantiates `DagEngine`;
- computes live observables;
- calls `update_phase`;
- copies the selected active parameters;
- passes them directly into the force-field loss.

The DAG/force path does not read native coordinates or RMSD.

## Authoritative source reduction

The executable audit established all frozen predicates.

### 1. Initial_Relaxation governs zero optimizer steps

At step 0 the historical derivative histories are represented as zeros:

- entropy curvature = 0;
- gamma derivative = 0;
- phi-dispersion derivative = 0.

The source therefore classifies the uninitialized history as a `Thermodynamic stall`.

Because the DAG update occurs before active parameters are copied and before the force loss is calculated, the source transitions:

`Initial_Relaxation -> Coherence_Growth_and_Compaction`

at step 0.

The first phase's force set is therefore never used for an optimizer update.

### 2. The source fractal funnel has no coordinate-gradient path

The recovered `apply_fractal_compaction_funnel(coords, ...)` function never loads its `coords` argument.

It uses a detached Df scalar from the metrics dictionary and contributes an energy offset. It does not apply a coordinate gradient in this source.

This does not say that a differentiable fractal potential is impossible; it says this recovered implementation did not provide one.

### 3. The only later state-triggered coordinate-force addition is contact springs

After the step-0 transition, the phase-1 force set contains:

- gamma surge;
- angular torque;
- Lennard-Jones repulsion;
- entropy pulse;
- the non-gradient fractal term.

The next phase contains the same set plus:

- contact springs.

Machine-checked set difference:

`phase2 - phase1 = ["contact_springs"]`.

Thus the remaining adaptive force-switching mechanism in the admissible recovered controller is a gate controlling when current-state contact springs activate.

## Why P7B was not run

The P7B eligibility rule was frozen before certification.

It stated that if the exact source reduced to contact-spring activation rather than a distinct multi-force adaptive mechanism, a new folding campaign would be a contact-gate rescue rather than the final independent controller test authorized by corrected P6.

That condition was met exactly.

Changing the rule after this source result to launch a protein campaign anyway would be post-hoc expansion of the hypothesis.

## Relation to prior protein evidence

This does not claim that Patch602.4 and Patch630 contact formulas are byte-identical.

It does establish that the surviving adaptive mechanism class is the same one already isolated later: state-triggered activation of current-state contact-collapse restraints.

In the reproduced Patch630 line:

- Ramachandran loss was inactive in the historical run;
- the torsional penalty was inactive;
- electrostatics were negligible;
- contact springs accounted for essentially all of the LockIn angular-order effect.

The held-out 1CRN Gate005 then returned `NO TRANSFER`:

- frozen contacts were worse than contacts OFF in 8/8 paired seeds;
- dynamic contacts were worse on average.

Accordingly the recovered early DAG does not expose a new independent mechanism that escapes the existing held-out falsifier.

## Other recovered controller branches

### Patch505.1

Useful lineage evidence, but not a clean native-blind authority:

- its schema contains `rmsd` and `contact_match` gates;
- it names native-contact forces;
- its preserved runner/source contains omitted-method sections and incomplete metric wiring.

### Patch606

The historical archive contains DAG/force files, but its preserved `main.py` is byte-identical to `force_field.py` and contains force-field source rather than a runner. P7 does not reconstruct the missing runner by inference.

### Physics-only controller

Source exists, but no historical caller was recovered.

## Scientific consequence

P7 closes the specific question left open by corrected P6:

> Is there a distinct, historically wired early observable/DAG mechanism that has not yet been reduced to the mechanism classes already tested?

For the recoverable source, the answer is **no**.

What remains historically valuable is the architectural idea of using observables to schedule model behavior. A newly designed adaptive controller could still be studied as a new algorithmic hypothesis. It would not be evidence that the historical engine had a surviving, validated protein-physics mechanism.

## Program consequence

```text
P7A HISTORICAL DAG CALLING PATH:              RECOVERED
P7 SOURCE INTEGRITY:                          CERTIFIED
DISTINCT MULTIFORCE ADAPTIVE MECHANISM:       NO-GO
P7B HISTORICAL-MECHANISM FOLDING CAMPAIGN:    NOT JUSTIFIED
NEW ADAPTIVE-CONTROLLER RESEARCH:              NEW HYPOTHESIS ONLY
```

No additional historical-engine tuning or contact-gate rescue is justified by the present scientific record.
