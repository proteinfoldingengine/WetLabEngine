# current_state.md — Retained-Atlas Loop Automation State

**Project:** Retained-Atlas Reachability Collapse / Resilience Toy Model  
**Purpose:** Starting state for an AI agent that will continue the loop-science work.  
**Current phase:** Post-V307.  
**Status:** Strong toy-level emergent law identified; next step is controller/intervention validation and ablation.

---

## 0. Claim Boundary

This project is **not** currently claiming:

- recovery of General Relativity,
- derivation of Einstein equations,
- physical spacetime recovery,
- real black hole physics,
- universal physical law.

Allowed current framing:

- retained-atlas toy model,
- emergent toy-level law,
- reachability geometry,
- future-state accessibility,
- horizon-like behavior,
- GR-adjacent diagnostic signal.

The strongest honest claim:

> Inside the retained-atlas toy, bad-basin formation is governed by sustained integrated loss of normalized adaptive reachability.

---

## 1. Current Core Law

### Normalized Adaptive Reachability

```math
A_norm(t) = A(t) / A_baseline
```

where `A(t)` is composite adaptive reachability and `A_baseline` is regime-relative baseline reachability.

### Integrated Reachability Deficit

```math
D_A = mean(max(0, A_c - A_norm(t)))
```

Current calibration:

```text
A_c ≈ 0.527
D_c ≈ 0.0388
```

Current toy law:

```text
D_A > D_c
→ pre-horizon collapse likely
```

Interpretation:

> Failure is not raw damage growth. Failure is sustained loss of reachable adaptive futures.

---

## 2. Current Law Stack

### Stage 0 — Adaptive Reachability

Tracks whether future recovery trajectories remain accessible.

### Stage 1 — Integrated Deficit / Pre-Horizon Collapse

Sustained loss of reachability accumulates as `D_A`.

### Stage 2 — Reachability Horizon Formation

Horizon-like behavior appears when `A_norm` remains near-zero for a sustained portion of the pre-commitment window.

### Stage 3 — Bad-Basin Lock

Bad-basin lock occurs after reachability collapse and horizon formation. Late repair can reduce severity but often cannot restore adaptive recovery.

### Stage 4 — Late Resilience Stack

The older six laws still matter, but they are now subordinate mechanisms preserving reachability:

1. healing capacity,
2. connectivity homeostasis,
3. interface buffering,
4. interface resealing,
5. recovery percolation,
6. long-memory drift detox.

---

## 3. Composite Reachability Definition

```math
A(t) = (R_f · C_w · B_e · D_r · R_v)^(1/5)
```

Components:

| Symbol | Meaning |
|---|---|
| `R_f` | recovery-front speed |
| `C_w` | corridor width |
| `B_e` | branching entropy |
| `D_r` | detox radius |
| `R_v` | reversible-state fraction |

Interpretation:

> `A(t)` estimates how much adaptive future-state volume remains reachable.

---

## 4. Supporting Older Laws

### Healing Capacity

```math
C_health = (repair · decay · mobility · corridor) / (shock · congestion · clustering · (1 + residual))
```

### Connectivity Homeostasis

```math
H_health = (repair · feedback · plasticity · mobility) / (shock · congestion · (1 + poison))
```

### Interface Resealing

```math
R_seal = (C_health · H_health · decay) / ((field + permeability + pocket) · resealDelay)
```

### Recovery Percolation

```math
P_recover = R_seal / (poison · permeability)
```

### Drift Detox

```math
D_health = (R_seal · mobility) / (poison + action)
```

These are no longer considered the deepest law. They are mechanisms that maintain `A_norm` and prevent `D_A` from accumulating.

---

## 5. Most Recent Run: V307

### V307 — Deficit Threshold Stability

Question:

> Does the integrated reachability-deficit threshold `D_c` remain stable across fresh seeds and regime variants?

Variants tested:

- base,
- dense,
- sparse,
- noisy,
- irregular shock,
- long memory.

Result:

```text
D_c ≈ 0.0388
```

Performance:

| Split / Variant | Result |
|---|---:|
| train AUC | 0.990 |
| train balanced accuracy | 0.952 |
| test AUC | 0.991 |
| test balanced accuracy | 0.958 |
| base balanced accuracy | 0.931 |
| dense balanced accuracy | 0.946 |
| irregular shock balanced accuracy | 0.943 |
| long memory balanced accuracy | 0.949 |
| noisy balanced accuracy | 0.963 |
| sparse balanced accuracy | 0.971 |

Outcome separation:

| Outcome | `D_A` | duration below `A_c` |
|---|---:|---:|
| adaptive/recovering | ~0.0128 | ~0.055 |
| bad-basin | ~0.4612 | ~0.951 |

Conclusion:

> `D_A` is currently the cleanest pre-horizon law. It is stable enough to act like a toy-law constant inside the current retained-atlas architecture.

---

## 6. Recent Discovery Sequence

| Version | Finding |
|---|---|
| V282 | Transition band is coexistence, not hard threshold |
| V283 | Early warning predicts final bad outcomes |
| V284–V286 | Staged repair beats one-shot repair |
| V287–V288 | Resealing helps but saturates |
| V289–V290 | Reconnection/action damping do not fully rescue bad branches |
| V291 | Early branch selection confirmed |
| V292–V293 | Pre-commitment intervention outperforms late intervention |
| V294 | Adaptive reachability introduced |
| V295 | `A_norm` threshold stable on fresh seeds |
| V296 | Absolute `A_c` shifts by regime |
| V297 | Normalized reachability collapses variants |
| V298 | Reachability-triggered intervention generalizes |
| V299 | Weak partial repair fails; full staged repair required |
| V301 | Curvature weak; pinch-off signal strong |
| V302 | Reachability horizon law strong |
| V303 | Horizon trigger works, scalar trigger better as early controller |
| V304 | Pre-horizon → horizon → lock ordering confirmed |
| V305 | Dynamic deficit beats instantaneous crossing conceptually |
| V306 | Deficit trigger best controller, slightly better than scalar |
| V307 | `D_A` threshold stable across variants |

---

## 7. GR-Adjacent Interpretation

Strongest current GR-adjacent signal:

> horizon-like loss of reachable recovery futures.

Not currently supported:

- curvature recovery,
- field equations,
- spacetime metric,
- Einstein-like dynamics.

Current interpretation:

| Toy event | GR-adjacent analogy |
|---|---|
| `A_norm` collapse | approach toward horizon |
| `D_A` accumulation | pre-horizon formation |
| horizon width / area | sustained low-reachability region |
| pinch-off | adaptive future paths disconnect |
| bad-basin lock | post-horizon irreversibility-like behavior |

Best safe statement:

> The toy is showing horizon-like reachability loss, not curvature recovery.

---

## 8. Agent Operating Protocol

The automation agent should act as a skeptical loop scientist.

Every loop must follow:

1. **Question** — What is being tested?
2. **Hypothesis** — What would support the law?
3. **Method** — What code/run was executed?
4. **Controls** — What could fool us?
5. **Results** — Numbers only.
6. **Interpretation** — What does it mean?
7. **Failure / Caveat** — What did not work?
8. **Decision** — continue / stop / branch / freeze.
9. **Next** — smallest useful next test.

The agent must not hype results.

---

## 9. Claim Levels

Use this hierarchy:

### Level 0 — Observation
The toy produced X.

### Level 1 — Repeatable Toy Behavior
X repeated across seeds or variants.

### Level 2 — Toy-Level Law
X predicts/explains outcomes across held-out seeds and variants.

### Level 3 — Cross-Architecture Law
X survives substantial architecture changes.

### Level 4 — Physical Hypothesis
X may correspond to a real physical principle.

Current `D_A` law status:

> Level 2 strong toy-level law.

Do not elevate it beyond Level 2 without cross-architecture evidence.

---

## 10. Stop / Continue / Branch Rules

### Continue if

- prediction improves,
- robustness improves,
- intervention rescue improves,
- a failure reveals a clearer mechanism,
- a metric compresses older variables,
- threshold remains stable under fresh validation.

### Stop if

- three consecutive loops fail to improve prediction, explanation, or control,
- new terms are added only to improve fit,
- no fresh seeds are used,
- no baseline is reported,
- no harm accounting exists,
- claims exceed evidence.

### Branch if

- a diagnostic works but controller fails,
- threshold works only regime-by-regime,
- a failure exposes a new mechanism,
- two metrics explain different phases of the same sequence.

---

## 11. Required Metrics

Always report:

- cases,
- phase counts,
- bad rate,
- adaptive rate,
- AUC,
- balanced accuracy,
- accuracy,
- trigger rate,
- rescued,
- harmed,
- net rescue,
- variant-level performance.

Track these core variables:

- `A_norm`,
- `D_A`,
- duration below `A_c`,
- horizon width,
- horizon area,
- pinch,
- mean `A`,
- min `A`,
- late field,
- late action,
- late residual,
- late pocket,
- late mobility,
- late `K`.

---

## 12. Next Recommended Loop

### V308 — Deficit Intervention Threshold Test

Question:

> Does triggering full staged repair at `D_A > D_c` outperform scalar `A_norm`, horizon area, and combined triggers?

Compare controllers:

1. scalar `A_norm` trigger,
2. duration-below-`A_c` trigger,
3. integrated deficit `D_A` trigger,
4. horizon-area trigger,
5. combined rule.

Report:

- baseline bad rate,
- treated bad rate,
- adaptive rate,
- trigger rate,
- rescued,
- harmed,
- net rescue,
- severity reduction,
- variant-level performance.

Expected:

> `D_A` trigger should slightly outperform scalar trigger and be more conceptually faithful to the horizon law.

Failure condition:

> If `D_A` does not outperform scalar `A_norm`, preserve `D_A` as diagnostic law but keep scalar as controller.

---

## 13. Secondary Next Loops

### V309 — Deficit Component Ablation

Question:

> Which component of `A(t)` drives `D_A`?

Ablate:

- recovery-front speed,
- corridor width,
- branching entropy,
- detox radius,
- reversible-state fraction.

### V310 — Addressability Conservation Test

Question:

> Is preserved lineage addressability the conserved object behind reachability?

Define:

```math
L_addr(t)
```

Test whether loss of `L_addr` precedes `D_A`.

### V311 — Coarse-Graining Test

Question:

> Does `D_A` survive aggregation / lower-resolution observation?

This is important for the GR-adjacent signal.

### V312 — Scaling Test

Question:

> Does the horizon law stabilize as system size increases?

If no, the GR signal weakens.

---

## 14. Recommended Agent Prompt

Use this prompt to start the automation:

```text
You are the Retained-Atlas Loop Agent.

Start from current_state.md.

Your job is to continue skeptical toy-model law discovery.

Current central law:
A_norm(t) = A(t) / A_baseline
D_A = mean(max(0, A_c - A_norm(t)))

Current calibration:
A_c ≈ 0.527
D_c ≈ 0.0388

Current interpretation:
Failure occurs when adaptive future trajectories remain inaccessible for a sustained pre-commitment window.

Do not claim GR recovery, spacetime, Einstein equations, or universal physics.

Run the next smallest useful test.

Every loop must include:
Question
Hypothesis
Method
Controls
Results
Interpretation
Failure/Caveat
Decision
Next

Begin with V308: Deficit Intervention Threshold Test.
```

---

## 15. Artifacts Already Created

Existing files from V300 package:

- `V300_Retained_Atlas_Reachability_Collapse_Paper.docx`
- `V300_RETAINED_ATLAS_REACHABILITY_COLLAPSE_PAPER.md`
- `v300_reachability_collapse_law_proof.py`
- `v300_reachability_collapse_law_proof_output.txt`

New automation should create files using versioned names:

- `V308_DEFICIT_INTERVENTION_REPORT.md`
- `v308_deficit_intervention.py`
- `v308_deficit_intervention_output.txt`

---

## 16. Final Current-State Summary

The retained-atlas toy now appears to be governed by a reachability-collapse sequence:

```text
A_norm collapse
→ D_A accumulation
→ reachability horizon
→ bad basin lock
```

The best current toy law is:

```math
D_A = mean(max(0, A_c - A_norm(t)))
```

```text
D_A > D_c
→ pre-horizon collapse likely
```

with:

```text
A_c ≈ 0.527
D_c ≈ 0.0388
```

This is the current automation starting point.
