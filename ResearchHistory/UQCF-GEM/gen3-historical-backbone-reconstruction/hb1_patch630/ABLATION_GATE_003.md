# Gen3 HB1 — Contact-Mechanism Discrimination Gate 003

Date: 2026-09-16
Target: 1VII
Baseline seed: 42
Steps: 5000

## Question

Does the Gate-002 contact-spring effect contain information beyond generic geometric regularization, or is it primarily an adaptive compaction/constraint term?

## Controls

All controls preserve the recovered full N-CA-C representation, pinned 1VII input, optimizer, seed, step count, pre-LockIn mechanics, and topology transition timing. Only the post-LockIn contact mechanism is changed.

### Historical dynamic contacts

At every post-LockIn step, eligible residue pairs with sequence separation >=3 and current CA distance <7.5 A are selected. The loss is proportional to the sum of squared current distances over that dynamically recomputed set.

### Frozen contacts

The eligible pair set is captured once at the LockIn transition and held fixed thereafter; the same squared-distance loss is applied to those fixed pairs.

### Randomized contacts

The number of contact pairs and sequence-separation distribution are matched to the LockIn contact set, but residue-pair identities are randomized without native-structure information.

### Generic geometric regularizer

A matched non-specific compaction term is used without contact-pair identity. Its initial loss/gradient scale is matched to the historical contact term at LockIn; no native information or parameter retuning is allowed.

## Seed-42 results

| Mechanism | Final RMSD (A) | Final phi_RMS | Interpretation |
|---|---:|---:|---|
| Historical dynamic contacts | 10.1913 | 0.2226 | reproduced baseline |
| Contacts OFF | 10.2674 | 0.4290 | Gate-002 negative control |
| Frozen LockIn contacts | 10.196 | 0.226 | essentially preserves historical effect |
| Randomized matched contacts | 10.22 | 0.25 | retains substantial but weaker ordering |
| Generic matched compaction | 10.24 | 0.30 | improves over contacts-off but does not fully reproduce dynamic/frozen contacts |

## Interpretation

The historical effect is **not explained solely by the fact that some generic compaction force is added at LockIn**. A matched generic compaction control improves phi_RMS relative to contacts-off, but remains materially weaker than the historical/frozen contact constraint.

However, the result also does **not** demonstrate native-contact information. Randomized matched contact identities retain a substantial fraction of the angular-ordering effect, and freezing the contact graph at LockIn performs nearly as well as dynamically recomputing it. This points toward a graph-constrained geometric regularization mechanism: preserving a mesoscale set of nonlocal distance relationships after a topology-triggered transition.

The dynamic recomputation itself is not required for most of the seed-42 effect. The scientifically interesting candidate is therefore narrower than the original historical interpretation:

> topology-conditioned activation of a nonlocal distance-constraint graph on a full backbone can stabilize/improve angular organization.

That candidate mechanism still requires multi-seed and held-out-target testing before it can be distinguished from conventional graph/distance regularization prior art.

## Next gate

Run baseline, contacts-off, frozen-contact, randomized-contact, and generic-compaction conditions across a preregistered multi-seed panel. Report distributions/effect sizes rather than selecting successful seeds. If the graph-constrained advantage survives, repeat on at least one held-out small protein before transferring it to Gen3 kinematic coordinates.
