# UQCF-GEM v15.30 — Provenance–Fiber Definability / Common-Carrier Gate

**Design status:** CONCEPT APPROVED / WRITTEN SPEC REVIEW PENDING  
**Date:** 2026-09-17  
**Stacked base:** v15.29 certified source head `6535ea69214f6661e340fe201813dfd17ddbb7e1`  
**v15.29 adjudication:** `PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED`  
**Scientific source pin inherited from v15.29:** `42244310b065f473c8bd459a6f065a61afbd2292`  
**Pillar 3:** OPEN

## 1. Purpose

v15.29 established two facts simultaneously:

1. exact microscopic source representatives can differ while sharing the same coarse source quotient `q = B1 x`;
2. the frozen archive does not entail whether such representatives are provenance-identical or provenance-distinct.

The unresolved object is therefore not another q-fiber construction. It is a typed, ontology-native relation connecting already-certified provenance/source objects to the exact microscopic q-fiber.

v15.30 asks one question only:

> Does any already-frozen ontology-native structure canonically define a provenance relation on microscopic representatives inside one exact q-fiber, without adding a new source-semantics axiom, supplying an arbitrary cross-domain embedding, or consulting downstream coupling/gravity criteria?

This is a theorem-first definability/common-carrier gate. It does not reopen the v15.28 coupling solver and does not evaluate a gravity canary.

## 2. Frozen claim boundary

The following are forbidden as selection principles in v15.30:

- holonomy, inverse-square, Newton, Einstein, ADM, or other gravity agreement;
- metric/Hodge/minimum-action selectors;
- entropy, pruning, recoverability score, or physical-time criteria used to choose a relation;
- PCA/SVD/alignment or learned embeddings between unrelated carriers;
- dimension/cardinality matching;
- matching names, labels, indices, or shared vocabulary without a certified typed map;
- arbitrary representative selection inside a q-fiber;
- hand-supplied intertwiners or basis identifications;
- adding a new source-semantics primitive and then treating it as derived.

Playback/ordered-update index remains nonphysical time.

## 3. Frozen inputs

v15.30 inherits the exact v15.29 q-fiber model and frozen evidence inventory. The admissible provenance-side candidate classes are limited to four already-audited origins.

### 3.1 Genesis/history lineage

Primary frozen evidence: V997 Genesis Pin.

Certified type:

```text
recoverable-history legitimacy / pinned registry / genesis root /
witness quorum / append-only continuity
```

Known boundary: same visible state does not imply legitimate history. No microscopic torus incidence relation is certified merely by that result.

### 3.2 Minimal ternary source role

Primary frozen evidence: V923 source-role closure.

Certified value set:

```text
source_active_role
source_basin_eligible_nonactive_role
source_rejected_or_broken_role
```

Known boundary: the primitive closes source legitimacy in its tested branch. It is not already a torus edge label or q-fiber partition.

### 3.3 Retained graph source/current

Primary frozen evidence: v13.26 retained source/current structure, including balance form `B J = s_ret` and protected retained source grade.

Known boundary: retained source/current information has its own graph representation and retains positive scaling freedom relative to observer normalization.

### 3.4 Genesis 6-D provenance carrier

Primary frozen evidence: the nontrivial Genesis/pruning field carrier identified in v14.04.

Known boundary: it is a real nontrivial carrier with model-specific transformations, but v14.04 found no certified natural representation link from it into the audited support carrier.

No fifth candidate class may be added in v15.30 without reopening the design.

## 4. Core mathematical objects

Let `C1` denote the inherited exact oriented edge-chain carrier and let

```text
q = B1 x
```

for an integral microscopic representative `x in C1`.

For a fixed coarse source `q0`, define the exact microscopic fiber

```text
F(q0) = { x in C1 : B1 x = q0 }.
```

The symbol `x` is reserved in v15.30 for the torus microscopic representative. Older retained-graph source variables are written `s_ret` to prevent cross-carrier type confusion.

A provenance-fiber relation is an equivalence or typed labeling law on `F(q0)` whose values come from one of the frozen provenance-side candidate carriers.

The central issue is definability, not mere constructibility. A relation is admissible only if the frozen ontology itself selects it.

## 5. Gate A — Typed common-carrier test

For each candidate origin `P`, search only the frozen archive for one of the following certified structures:

1. a typed map `phi: F(q0) -> P`;
2. a typed map `psi: P -> F(q0)`;
3. a typed map involving the full edge carrier `C1` whose restriction to `F(q0)` canonically determines the provenance relation;
4. a common parent carrier `K` with certified maps to both sides;
5. a certified equivalence, quotient, incidence, functorial, or representation relation that determines the comparison without a supplied embedding.

Passing Gate A requires concrete frozen evidence of the map/relation and its transformation law.

The following do not pass Gate A:

- same dimension;
- same number of labels;
- matching vertex/site names;
- shared use of the word `source` or `provenance`;
- post hoc correspondence tables;
- manually chosen basis maps.

If no candidate passes, v15.30 closes immediately as:

`NO_TYPED_COMMON_CARRIER`.

## 6. Gate B — Exact q-fiber compatibility

Any candidate relation surviving Gate A must be evaluated on at least two distinct exact representatives `x1 != x2` satisfying

```text
B1 x1 = B1 x2 = q0
```

with equality checked exactly over integers/rationals.

The provenance relation must be evaluated while `q0` is held fixed. It may classify the representatives as identical or distinct, but it must not alter the coarse source quotient to obtain that classification.

A candidate that only distinguishes different q values does not answer v15.30.

## 7. Gate C — Definability / naturality

Let `Aut(D)` be any certified relabeling, gauge transformation, or automorphism that preserves all frozen data used by a candidate relation.

An admissible provenance-fiber relation `R` must be invariant/equivariant under those frozen symmetries. Informally:

```text
if a transformation preserves every frozen fact,
it may not change the physical provenance relation.
```

Operationally, v15.30 must test the strongest transformation law actually certified for each candidate carrier; it must not invent a larger or smaller symmetry group for convenience.

If two representatives can be swapped by a frozen-data automorphism while every candidate provenance fact remains unchanged, a proposed relation that distinguishes them is not definable from those facts.

This gate is theorem-first. Finite exhaustive controls may accompany the proof where the relevant symmetry group is finite, but numerical sampling cannot replace the logical argument.

## 8. Gate D — Uniqueness / countermodel test

For every relation surviving Gates A–C, either prove uniqueness from the frozen typed constraints or construct explicit inequivalent admissible countermodels. If the admissible relation family is infinite, two inequivalent surviving relations are sufficient to disprove uniqueness; exhaustive enumeration is not required.

If two inequivalent provenance-fiber relations:

- share the same frozen q-fiber;
- preserve the same provenance/source facts;
- satisfy the same certified transformation laws;
- require no forbidden selector;

then the frozen ontology does not canonically select either one.

That outcome is:

`MULTIPLE_NATURAL_RELATIONS_REMAIN`.

The countermodel standard from v15.29 is retained: a logical expansion may prove non-entailment but may not be described as physically realized merely because it is consistent.

## 9. Gate E — No-choice audit

Before any positive certification, inspect the full dependency path of the proposed relation.

The relation fails Gate E if any decisive choice enters through:

- a fitted parameter chosen to improve downstream behavior;
- an arbitrary basis/intertwiner;
- an untyped cross-domain lookup table;
- a preferred microscopic representative;
- a gravity/coupling/metric score;
- a new semantic declaration not present in frozen evidence.

If a nontrivial relation can be constructed only by introducing a new source-semantics declaration, v15.30 records the missing object but does not add it.

## 10. Preregistered outcomes and precedence

The only admissible real-archive outcomes are:

### `NO_TYPED_COMMON_CARRIER`

No frozen candidate supplies a typed relation or common carrier connecting q-fiber representatives to provenance/source identity.

This has highest precedence when Gate A fails for all four candidates.

### `PROVENANCE_FIBER_RELATION_NOT_DEFINABLE`

A typed connection exists, but frozen-data automorphisms/equivalences preserve all evidence while changing the proposed representative-level relation, or the candidate otherwise fails the definability/naturality requirement.

### `MULTIPLE_NATURAL_RELATIONS_REMAIN`

At least two inequivalent relations satisfy the same frozen typed and naturality constraints, so no unique canonical relation is selected.

### `CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED`

Exactly one nontrivial relation survives the typed common-carrier, exact-fiber, naturality, uniqueness, and no-choice gates.

Positive certification requires an explicit witness describing:

```text
domain
codomain/common carrier
relation/map
certified transformation law
exact q-fiber behavior
uniqueness argument
claim boundary
```

No weaker positive label is allowed.

## 11. Mechanical precedence rule

Adjudication proceeds in this order:

```text
if no candidate passes typed common-carrier gate:
    NO_TYPED_COMMON_CARRIER
elif every typed candidate fails definability/naturality:
    PROVENANCE_FIBER_RELATION_NOT_DEFINABLE
elif two or more inequivalent natural relations survive:
    MULTIPLE_NATURAL_RELATIONS_REMAIN
elif exactly one nontrivial relation survives every gate:
    CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED
else:
    fail closed as PROVENANCE_FIBER_RELATION_NOT_DEFINABLE
```

The final `else` is deliberate. Ambiguous positive evidence cannot promote the branch.

## 12. Required controls

### 12.1 Null/common-word control

A synthetic record that shares labels such as `source`, `site`, `origin`, or `provenance` with the q-fiber but has no typed map must be rejected by Gate A.

### 12.2 Supplied-embedding control

A synthetic explicit embedding may demonstrate that a relation can be made operative, but the gate must classify it as supplied/non-derived and never promote it into frozen evidence.

### 12.3 Collapsed relation control

A synthetic provenance law depending only on `q` must classify all members of one q-fiber identically. This checks that the adjudicator can recognize genuine collapse.

### 12.4 Distinguishing relation control

A synthetic, explicitly supplied exact partition of one q-fiber must be recognized as distinguishing while remaining marked synthetic/nonphysical.

### 12.5 Automorphism control

Construct a finite control where an automorphism preserves the frozen reduct while swapping two representatives. A non-invariant proposed relation must be rejected as non-definable.

### 12.6 Unique-natural-relation control

Construct a small synthetic carrier for which exactly one relation satisfies the declared typed maps and group action. The gate must be capable of returning the positive status in principle.

## 13. Deterministic evidence model

The implementation must use a hash-pinned evidence inventory inherited from v15.29 and may add only frozen artifacts needed to prove the transformation/common-carrier claims for the four declared candidates.

Each evidence record must declare at least:

```text
key
path
blob hash
domain
codomain/common parent if any
relation class
transformation law source
certifies common carrier? yes/no
certifies q-fiber relation? yes/no
claim boundary
```

No evidence record may infer a typed relation from prose similarity alone.

## 14. Gravity and coupling firewall

v15.30 must expose explicit machine-readable flags proving:

```text
coupling_solver_reopened = false
gravity_observables_evaluated = false
uses_holonomy_selector = false
uses_newton_or_gr = false
uses_metric_selector = false
uses_pruning_as_selector = false
uses_entropy_as_selector = false
uses_physical_time = false
new_source_semantics_axiom_added = false
signal_of_life = false
gravity_canary_certified = false
physical_gravity_derived = false
Pillar_3 = OPEN
```

Archived pruning/recoverability objects may be inspected as typed provenance evidence, but pruning/recoverability performance may not choose the relation.

## 15. Deterministic output contract

The final ledger must include at least:

```text
version = v15.30
base_sha = 6535ea69214f6661e340fe201813dfd17ddbb7e1
status
candidate_count = 4
candidate_results
common_carrier_count
exact_fiber_relation_count
natural_relation_count
countermodels_survive
canonical_relation_certified
new_source_semantics_axiom_added = false
coupling_solver_reopened = false
gravity_observables_evaluated = false
scientific_breakthrough
signal_of_life = false
gravity_canary_certified = false
physical_gravity_derived = false
Pillar_3 = OPEN
next_required_object
```

`scientific_breakthrough` may be true only for `CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED`; all other statuses require false.

## 16. Next-step mapping

```text
NO_TYPED_COMMON_CARRIER
  -> stop archive derivation; next object is a genuinely typed common carrier or an explicitly approved new axiom.

PROVENANCE_FIBER_RELATION_NOT_DEFINABLE
  -> localize the symmetry/definability obstruction; do not fit a relation around it.

MULTIPLE_NATURAL_RELATIONS_REMAIN
  -> identify the exact additional primitive needed to choose among the surviving natural relations; no coupling solve.

CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED
  -> open a separate provenance-action/representation-readiness gate. Do not reopen the coupling solver in v15.30 itself.
```

No v15.30 outcome directly authorizes a coupling or gravity gate.

## 17. Verification standard

A v15.30 claim is publishable only after:

1. RED→GREEN TDD for every gate surface;
2. exact replay of inherited v15.29 q-fiber and provenance inventory checks;
3. frozen-blob verification for every new evidence record;
4. exact automorphism/group-law checks where finite controls are used;
5. explicit countermodel search/uniqueness proof for every surviving real candidate;
6. deterministic ledger regeneration and byte comparison;
7. inherited selected-test regression with no scientific changes after exact-head certification;
8. digest-verified release artifacts if a release is produced.

## 18. Interpretation discipline

A positive `CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED` result would mean only that the present frozen ontology canonically relates microscopic q-fiber representatives to a provenance/source distinction. It would not by itself establish a source representation suitable for the v15.28 coupling target, choose a coupling member, or establish any gravity signal.

A negative result would be equally informative: it would show that the missing structure identified in v15.29 is not recoverable from the four strongest frozen candidate origins under their certified transformation laws.

The gate therefore measures definability of source provenance, not agreement with desired downstream physics.
