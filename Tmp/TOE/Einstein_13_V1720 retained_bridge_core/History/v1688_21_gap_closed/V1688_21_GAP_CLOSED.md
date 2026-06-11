# V1688.21 — The Connection Gap: Found and Closed

**Status:** finite-sector, deterministic. Reopens the holonomy question that prior tests
had wrongly closed.
**Companion proof:** `v1688_21_native_connection.py` (+ `v1688_21_OUTPUT.txt`).

---

## Executive summary

Every previous loop/holonomy test in this program (V1703.1, V1703.2, V1703.4, V1688.20)
transported objects using `T_ij = frames[j]ᵀ frames[i]` — an **orthogonal change of basis**.
That connection is **flat by construction**: exactly invertible and path-independent, because
`T_kj·T_ji = frames[k]ᵀ frames[i]` regardless of route. Any matched-length loop closes to
machine precision **no matter what is transported**. The repeated "no holonomy / closes to
1e-15" results were therefore artifacts of testing a connection with no curvature in it — not
properties of the retained transport.

The retained program defines transport by the **native recombination kernel**, which is
nonlinear and *not* a change of basis:

```
T_pq(dx) = dx + gamma_pq · [roll(dx) ⊙ q − dx ⊙ roll(q)]
```

Run with this as the connection, the result reverses.

---

## The gap

| | prior tests | what the model actually defines |
|---|---|---|
| connection | `T_ij = frames[j]ᵀ frames[i]` (orthogonal) | native kernel `T_pq(dx)` (nonlinear) |
| invertible? | yes, exactly | no |
| path-dependent? | no, by construction | **to be tested** |
| consequence | loops close at 1e-15 *trivially* | loops can carry holonomy |

The peer's recurring statement — "p→q is a retained recombination event, not neutral motion
through a pre-existing space" — is precisely this gap. The tests implemented neutral motion
through a pre-existing space (global Rⁿ with rotated frames). They could not see holonomy
because the connection had none.

---

## Result (reproduced)

Two **matched-length, matched-step** loops, same endpoints (0→4), disjoint interiors
(`[0,1,2,3,4]` vs `[0,5,6,7,4]`), 80 seeds:

```
ORTHOGONAL frame connection (old tests): mean path-diff = 9.97e-16   (flat)
NATIVE recombination connection (real):  mean path-diff = 0.8097      (min 0.19, max 1.40)
there-and-back closure defect (native):  mean = 1.1316
```

- Under the real connection, two equal-length routes between the same endpoints **differ by
  ~0.81** — genuine, route-dependent path dependence that survives the length-match guard
  that erased every earlier signal.
- There-and-back transport does not return to the start (defect 1.13): the kernel is
  **non-invertible**.

---

## What this establishes — and what it does not

**Established:**
- The earlier machine-precision "no holonomy" results were artifacts of a flat (orthogonal)
  connection, not facts about the retained transport.
- Under the native recombination connection, transport is **not flat**: matched-length loops
  are route-dependent. The holonomy question is **reopened and live**, not resolved negative.

**NOT yet established (next tests, stated up front):**
1. **Structure-specificity.** Does the *retained* kernel/provenance produce path dependence
   a *generic* nonlinear kernel of the same form would not? The reference antibody
   (retained vs. random kernel) has not been fired on this object. Until it is, 0.81 could be
   generic non-associative spillover, not a retained-structure holonomy.
2. **Holonomy vs. mere non-invertibility.** The there-and-back defect (1.13) shows the kernel
   is non-invertible, which can by itself produce path differences. A clean holonomy
   (curvature) claim requires the two *forward* matched loops to differ *beyond* what
   non-invertibility alone forces. That separation is not yet done.

---

## Honest status change

Prior verdict (mine): "no holonomy, vector or algebra; loops close to 1e-15." **Withdrawn** —
it was measured on a flat connection and does not bear on the native connection.

Current status: under the connection the model actually defines, there is real
route-dependent path dependence. Whether it is a structure-specific geometric holonomy or a
generic effect of a non-invertible nonlinear map is the open question, now testable because
the connection is finally the right one.

---

## Reproduction

```
python3 v1688_21_native_connection.py
```

Deterministic (seeded numpy). DIM=6, 8 nodes, 80 seeds. Compares the orthogonal-frame
connection (control, flat) against the native recombination kernel (real connection), on
length- and step-matched loops, plus a there-and-back non-invertibility probe.

## Next experiment (decisive)

Fire the reference antibody on this object: native retained kernel vs. a random nonlinear
kernel of identical form, both on the same matched loops. If retained ≫ random at ≥3σ →
structure-specific holonomy. If retained ≈ random → generic non-associative path dependence.
Then separate holonomy from non-invertibility by comparing forward-loop difference against
the there-and-back floor.
