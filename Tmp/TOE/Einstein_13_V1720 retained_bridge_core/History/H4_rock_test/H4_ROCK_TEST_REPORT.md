# Is H4 a True Geometric Rock? — Reference-Antibody Test

**Status:** finite-sector reproduction + reference null tests
**Claim level:** model-internal. Tests whether the V1687 H4 rank-lift is a structure-specific
geometric obstruction or a generic artifact of non-associativity in a space with headroom.
**Companion files:** `v1687_16.py` (reproduces the manuscript's audit), `v1687_H4_rock.py`
(the three antibodies), and the two `*_OUTPUT.txt` captures.

---

## Background

The V1687 manuscript claims H4 (the canonical fourth-order bracketing residual) is
**irreducible fourth-order hyper-associator information**, evidenced by a rank lift:
`rank(B4+O3+H4) > rank(B4+O3)`. The manuscript's own immune system is strong on
*internal* validity (it built an H4-erasing projection, then caught it as post-hoc via a
generated-algebra faithfulness gap of 3.35e8). That audit reproduces exactly (see
`v1687_16_reproduction_OUTPUT.txt`):

```
rank(B4+O3)=8, rank(B4+O3+H4)=9, H4 erased residual=1.13e-9,
generated_gap_max=3.352748e8, verdict=INADMISSIBLE_POSTHOC
```

So the computation is real and reproducible. The open question is **reference**: does the
rank lift mean what its name says? The manuscript never ran a reference null. This test does.

---

## Method — three antibodies aimed at reference, not consistency

For a true geometric obstruction we require all three:

1. **Robustness (Antibody 1):** lift should survive a sweep over dim and n_branch. A real
   obstruction should not vanish when the chart is resized.
2. **Reference / non-tautology (Antibody 2):** lift should depend on the *structure* of the
   branches. If random vectors lift the rank as much as the structured retained branches,
   the lift is generic headroom, not a structure-specific obstruction.
3. **Operator-dependence (Antibody 3):** lift should vanish for the associative/linear
   control (no non-associativity ⇒ no obstruction) and appear only for the genuine kernel.

All three are deterministic (seeded numpy). Run: `python3 v1687_H4_rock.py`.

---

## Results (reproduced)

### Antibody 1 — robustness sweep: FAIL (headroom-dependent)

```
 dim  nbr |  mean_lift
   8    4 |   0.00      <- saturated: no room, no lift
   8    5 |   0.00
  12    4 |   1.00
  12    5 |   0.00      <- saturates again
  16    4 |   1.00
  16    5 |   1.00
  16    6 |   0.00
  24    4 |   1.00
  32    6 |   1.00
```

Lift = 1 exactly when `dim > rank(B4+O3)`, and 0 whenever lower-order structure saturates
the space. The lift is **not invariant** — it is conditional on ambient headroom, the same
failure that demoted the L3 "+2" lift. The magnitude is an artifact of available dimension.

### Antibody 2 — reference / non-tautology: FAIL (decisive)

```
orthonormal (structured) branches: mean lift = 1.00
random branches:                   mean lift = 1.00
```

**Identical.** The H4 rank lift does not care whether the branches are the structured
retained currents or arbitrary random vectors. The obstruction is not tied to the retained
structure. This is the reference null (analogous to the gamma-shuffle that killed the V1688
holonomy claim), and H4 fails it: the signal survives the perturbation that should destroy a
structure-specific quantity, because it was never structure-specific.

### Antibody 3 — operator-dependence: PARTIAL PASS (the one real signal)

```
native_nonassoc      : mean lift = 1.00
associative_linear   : mean lift = 0.00   <- correctly vanishes
symmetric_overlap    : mean lift = 1.00
nonlinear_symmetric  : mean lift = 1.00
```

Lift is 0 for the associative/linear operator (correct: no non-associativity ⇒ no
obstruction) and ≥1 for nonlinear operators. BUT it is ≥1 for *any* nonlinear operator,
not specifically the program's antisymmetric retained kernel. So the lift detects
"nonlinearity produces high-order terms," not "this retained recombination algebra has a
special hyper-associator obstruction."

---

## Verdict: H4 is NOT a true geometric rock

- **Real:** a nonlinear product generates a fourth-order bracketing residual outside
  span(B4 ∪ O3) **when the ambient space has headroom**. The V1687.16 audit reproduces.
- **Not real:** that this residual is structure-specific, invariant, or a hyper-associator
  obstruction of *this* algebra. It lifts identically for random vectors (Antibody 2),
  vanishes under saturation (Antibody 1), and appears for any nonlinear operator (Antibody 3).

The honest reduced claim: **non-associativity (more precisely, nonlinearity) is necessary
for the fourth-order residual to be irreducible, and it is irreducible only where dimensional
headroom permits.** That is a modest, true statement about operators — not evidence of a
geometric obstruction tied to retained provenance.

---

## Methodological note for the reviewing AI

The V1687 framework has a strong immune system for **internal validity** (it caught its own
post-hoc H4-eraser). It lacks an antibody for **external reference** — a control that
destroys the claimed correspondence (random branches, wrong operator, saturated space). When
that antibody is applied, H4's geometric interpretation dissolves, matching the pattern seen
for L3-as-geometry, V1688 directed holonomy, and the ADM/H-H metric. Recommended standing
reflex: run the random-branch / wrong-operator / saturation controls **before** assigning any
layer a geometric name.

## Falsification of THIS finding

This conclusion weakens if any of the following is shown:
1. an operator-faithful, structure-respecting basis under which random branches give lift 0
   while retained branches give lift > 0 (would restore structure-specificity);
2. a dimension-independent invariant (not raw rank lift) that stays positive under saturation;
3. a quantity that distinguishes the antisymmetric retained kernel from generic nonlinear
   operators. None of these was found here, but the search was finite-sector.
