# v15.26 — Pre-Time Response Selector Rank / Cycle-Target Origin Gate

**Status:** `PRETIME_RESPONSE_RANK_GATE_CLOSES_GIVEN_TARGET_TARGET_ORIGIN_OPEN`  
**Selector verdict:** `CYCLE_RESPONSE_TARGET_NOT_DERIVED`

v15.25 killed bare compatibility as a gravity canary: the same local incidence defect admitted a global Hodge representative, exact one-edge cancellation, and arbitrary cycle additions. v15.26 asks the next gravity-facing question directly: **what finite object would actually resolve that cycle freedom, and is that object already supplied by the pre-time ontology?**

The answer is sharp. A metric-free higher-incidence response operator can resolve the full cycle space **if its target values are supplied**. The source/admissibility datum `q` does not supply those target values. Thus the missing object is no longer “a metric” or “another pseudoinverse”; it is a pre-time source→cycle-response target law.

No pruning, entropy, physical time, Newtonian target, GR residual, edge-metric selector, minimum-action principle, or smoothness objective is used to adjudicate the target.

## 1. Frozen source equation

The v15.25 finite torus complex and source are reused unchanged:

```text
B1 j + q = 0
q = B1 delta_b
```

For the 7x7 periodic complex:

- vertices: 49;
- edges: 98;
- `rank(B1)=48`;
- cycle dimension `dim ker(B1)=50`.

The v15.25 falsification remains in force: `j_local=-delta_b` is an exact one-edge solution, so conservation alone cannot force a long-range field.

## 2. A metric-free response operator can resolve all cycle degrees

The face-boundary response operator is

```text
R_face = B2^T.
```

On the cycle space its rank is 48, leaving two unresolved topological/homology modes. This is exactly the first Betti number of the periodic torus control.

Add two period/cut rows `H`, one detecting horizontal winding and one vertical winding. They are chosen from the existing incidence/topology and satisfy

```text
H B2 = 0.
```

The full diagnostic response operator is

```text
R = [ B2^T ; H ].
```

For the frozen complex:

```text
rank(R Z) = 50 = dim Z
sigma_min(R Z) = 0.8677674782351158
```

where the columns of `Z` span `ker(B1)`. This is the finite pre-time analogue of the earlier conditional response-rank theorem: once a target `y=Rj` is supplied, the cycle coefficients are identifiable.

## 3. Given a target, the current is unique

Choose any particular solution `j0` of `B1 j0 + q=0`. Then every solution is

```text
j = j0 + Z a.
```

Given a target `y`, solve

```text
R Z a = y - R j0.
```

Because `RZ` has full column rank, `a` and hence `j` are unique. The reconstructed current is independent of the starting particular section to about `3.33e-15` in the executed control.

This recovers the structural content of the archived v13.25 theorem, where an externally supplied response `R` selected a current when `rank(RZ)=dim Z`. v15.26 moves that theorem directly into the pre-time gravity canary and isolates the remaining missing input: **the response target**.

## 4. The same source q supports incompatible targets

Three exact target/current pairs are frozen:

1. **Hodge target** — `y_H=R j_H`, where `j_H` is the v15.25 equal-edge diagnostic representative. Reconstruction error: `2.41e-15`. Remote noncommuting holonomy: `2.1978e-3`.
2. **Microscopic target** — `y_local=R(-delta_b)`. Reconstruction error: `3.36e-15`. Remote holonomy: numerical zero.
3. **Cycle-shift target** — `y_shift=R(j_H+0.25 z)` for a lawful closed cycle `z`. Reconstruction error: `2.61e-15`. Remote holonomy: about `0.1998035`.

All three currents satisfy the **same source equation** to about `7.01e-15` or better. Their target values differ. Therefore the rank theorem does not select gravity; it faithfully reconstructs whichever target law has already been chosen.

## 5. Why zero target does not rescue the derivation

Setting the face-curl target to zero leaves two harmonic modes unresolved. Adding the two period coordinates closes the rank gate, but then setting those period targets to zero is an additional condition.

The full zero target selects a unique current, but it is **not** the Hodge representative. In the executed control its distance from `j_H` is `0.8571428571`. Thus “choose zero response” is a new selector, not a consequence of compatibility or topology.

## 6. Microscopic inheritance is not quotient-invariant

One might try to obtain the target directly from the microscopic defect representative `delta_b`:

```text
y_micro = -R delta_b.
```

This indeed reconstructs the exact local cancellation. But a source-equivalent representative

```text
delta_b' = delta_b + B2 f
```

has exactly the same `q` because `B1 B2=0`, while its inherited target changes. The executed target difference is about `4.472135955` with `||q'-q||=0`.

Therefore the microscopic representative cannot define a physical target unless an additional quotient-covariant provenance law distinguishes representatives. That law is not present in the frozen canary.

## 7. Why archived candidates do not silently fill the gap

This gate does **not** reopen already-closed branches by renaming them:

- v13.01 stopped metric origin inside the BKM/naturality stack; MEA/BIFL remained an explicit conditional input.
- the earlier small-network Gate-A control already showed that Hodge/minimum-action currents depend on an underived metric `W`.
- v15.03 explicitly prohibited promoting a minimum-norm/Hodge current to a provenance-selected source law.
- v13.28 found Genesis/support, PGRL/BKM, RESA/coframe, and QMAR/covariance source→geometry pairing classes insufficient to derive the missing absolute coupling law.

Accordingly v15.26 uses topology only to test **identifiability given target**. It does not use BKM, metric weights, a downstream gravity residual, or observer fitting to manufacture the target.

## 8. Executed numerical result

Fresh local execution before GitHub publication gives:

```text
cycle_dimension                         50
face_response_rank_on_cycle_space      48
homology_dimension                       2
full_response_rank_on_cycle_space       50
full_response_sigma_min           0.8677674782
hodge_reconstruction_error        2.406e-15
local_reconstruction_error        3.358e-15
cycle_shift_reconstruction_error  2.612e-15
same-q maximum source residual     7.011e-15
rank-gate permutation error        7.021e-15
```

The 26 new tests cover the rank theorem, homology controls, three exact target reconstructions, source-equivalent microscopic ambiguity, relabeling covariance, ontology boundaries, and presentation/export integrity. GitHub CI independently reruns these with all inherited selected tests before a release is certified.

## 9. Adjudication

The exact outcome is:

```text
rank gate closes given target:     YES
rank gate supplies target:         NO
cycle target derived from q:       NO
signal of life certified:          NO
gravity canary certified:          NO
```

So:

```text
CYCLE_RESPONSE_TARGET_NOT_DERIVED
```

and the next required object is

```text
PRETIME_SOURCE_TO_CYCLE_RESPONSE_TARGET_LAW
```

A lawful next gate must test ontology-native, target-blind candidates for that map. Any candidate must be quotient-covariant under source representatives, independent of pruning/time/entropy, and must not be chosen because it yields long-range holonomy, inverse-square behavior, or GR agreement.

## Claim boundary

This is a **structural narrowing of the gravity problem**, not a gravity detection. It supplies no actual record, metric, physical duration, entropy production, source calibration, Newtonian law, Einstein equation, or physical field. Pre-time reversible change remains allowed. Pillar 3 remains OPEN.
