# v15.29 — Pre-Time Provenance Faithfulness / Source Extension Gate

**Design status:** approved and frozen. No scientific implementation is authorized by this file alone.

**Base scientific head:** `42244310b065f473c8bd459a6f065a61afbd2292` (certified v15.28 exact head).

**Primary purpose:** determine whether the source quotient used in v15.25–v15.28,

\[
q = B_1\delta b,
\]

is already the complete physically meaningful pre-time source object, or whether frozen provenance distinguishes source representatives inside the same quotient fiber strongly enough to define a richer source carrier **without using downstream gravity behavior**.

The gate is upstream of constitutive-coupling selection. It does not evaluate a gravity canary, holonomy, inverse-square behavior, GR, cosmology, pruning, entropy, or physical time.

---

## 1. Scientific motivation

v15.25 established that bare compatibility does not force a long-range response because

\[
q=B_1\delta b
\]

admits the exact local cancellation

\[
j_{\rm local}=-\delta b,
\]

as well as Hodge and cycle-shifted responses.

v15.26 showed that higher-incidence coordinates can uniquely reconstruct a response **conditional on a supplied target**, but do not derive that target.

v15.27 proved that the full cycle-response target cannot factor through `q` alone because the response coordinates are nonzero on `ker(B1)`.

v15.28 then classified the exact q-only equivariant coupling space and found

\[
\boxed{d_\eta(q\to Y_{\rm cyc})=3},
\]

while all archived provenance-enhanced physical candidates were blocked by the absence of a certified natural representation link into the cycle-response carrier.

The remaining question is therefore not “which of the three q-couplings looks gravitational?” That is forbidden. The question is:

> **Did the quotient `q=B1 delta_b` erase source information that frozen provenance itself certifies as physically distinct before time?**

---

## 2. Three possible conceptual routes

### Route A — Provenance-fiber faithfulness audit (**recommended and in scope**)

Treat the current source quotient as a projection

\[
\pi:\mathcal S_{\rm micro}\to \mathcal Q,
\qquad
\pi(\delta b)=B_1\delta b=q.
\]

For a fixed `q`, examine the fiber

\[
\pi^{-1}(q)=\{\delta b+z:\; z\in\ker B_1\}.
\]

Ask whether the already-frozen provenance/source-legitimacy structure assigns the **same** certified provenance state to all members of a fiber, or whether some source representatives carry certified distinctions that survive every allowed provenance gauge/relabeling.

If such distinctions exist, define only the **typed extension data** they justify; do not yet define a response law.

### Route B — Declare the microscopic representative physical (**control only; not admissible by default**)

One could set `S_prov = delta_b` and thereby retain all cycle information. This would immediately distinguish `delta_b` from `delta_b+B2 f`, but it is not allowed merely because it repairs v15.27. It becomes admissible only if the frozen provenance ontology already certifies those distinctions as source-relevant and covariant.

This route is a negative control against silently promoting microscopic bookkeeping to physics.

### Route C — Add a new source-semantics axiom (**out of scope in v15.29**)

v15.08 showed that source semantics are irreducible relative to the frozen ontology. A new axiom could explicitly declare some provenance object to be the physical source. That would be a new theory input and requires separate explicit approval. v15.29 must not smuggle it in.

**Recommendation:** execute Route A only. Use B and C solely as boundaries/controls.

---

## 3. Typed objects

The gate must keep distinct the following objects:

### 3.1 Coarse source quotient

\[
\mathcal Q := \operatorname{im}(B_1)\subset C_0,
\]

represented by neutral vertex/source vectors `q`.

This is the exact source object used in v15.25–v15.28 and remains a valid **coarse control**.

### 3.2 Microscopic incidence representative

\[
\delta b\in C_1,
\qquad
B_1\delta b=q.
\]

This is a representative, not automatically a physical source.

### 3.3 Provenance record

A provenance record is a frozen, typed object describing legitimate source/history identity, witness/root continuity, role classification, multiplicity, or other certified provenance information already present in archived artifacts.

No text label such as “source,” “generator,” or “origin” is sufficient to identify it with `delta_b`, `q`, a Hermitian operator, or a cycle target.

### 3.4 Provenance-enhanced source carrier

A candidate extension has the abstract form

\[
0\longrightarrow K_{\rm prov}
\longrightarrow \mathcal S_{\rm prov}
\overset{\pi}{\longrightarrow}\mathcal Q
\longrightarrow 0.
\]

This exact-sequence notation is descriptive: `K_prov` means provenance distinctions invisible to `q`. The gate must determine whether frozen evidence actually supplies such a nontrivial kernel and its transformation law.

The gate must **not** assume this extension is split, vector-linear, quantum, metric, or isomorphic to `ker(B1)`.

---

## 4. Primary scientific questions

The gate answers the following in order.

### Q1. Provenance fiber faithfulness

For source representatives `s1,s2` with the same coarse source,

\[
B_1s_1=B_1s_2,
\]

does the frozen provenance stack necessarily identify them, necessarily distinguish them, or leave the relation unspecified?

### Q2. Gauge versus physical distinction

If provenance distinguishes two representatives, is the distinction invariant under the already-earned provenance gauge/relabeling equivalences? A distinction that disappears under certified gauge is not eligible as new source content.

### Q3. Transformation law

Do the surviving provenance classes carry a certified action under the same relabeling/automorphism structure used in v15.28, or under a separately certified natural action that can be compared to it without an arbitrary embedding?

### Q4. Extension structure

Does the evidence support a typed projection

\[
\pi:\mathcal S_{\rm prov}\to\mathcal Q
\]

whose fibers are provenance-distinguished in a mathematically stable way?

### Q5. Representation bridge readiness

If a nontrivial `S_prov` is certified, does it now possess the typed, covariant label relationship required to become an eligible input for the v15.28 exact coupling-space problem?

A positive answer requires more than covariance. The source carrier must also supply either:

- a finite-dimensional linear representation with exact action matrices; or
- a canonical linearization already determined by the frozen ontology.

Without that structure, the carrier may be typed/covariant but is **not representation-ready** for the coupling solver.

The gate stops before solving any downstream gravity response. A representation-ready source carrier merely authorizes a separate later coupling-space gate.

---

## 5. Frozen evidence inventory

v15.29 must hash-pin and type-audit, at minimum:

- v15.28 coupling-space report/ledger and exact source head;
- v15.27 target-origin result;
- v15.26 response-selector-rank result;
- v15.09 quantum-carrier origin report;
- v15.08 source-semantics irreducibility report;
- v15.03 graph-site/source-lift report;
- v15.02 shared-label carrier report;
- v15.01 common-parent representation report;
- v14.04 provenance representation report;
- v13.26 source-calibration/origin boundary;
- Genesis Pin / pinned-registry artifacts actually used by those reports;
- source-role / retained source-grade artifacts cited by v15.08 and v14.04.

The inventory must distinguish:

```text
CERTIFIED_PROVENANCE_RELATION
CERTIFIED_GAUGE_OR_EQUIVALENCE
CERTIFIED_ACTION
CERTIFIED_PROJECTION_TO_Q
ARCHIVE_EVIDENCE_ONLY
NO_TYPED_RELATION
CONDITIONAL_ON_SUPPLIED_MAP
```

No carrier becomes eligible because of matching dimensions, matching cardinality, shared words, visual similarity, or downstream performance.

---

## 6. Formal fiber audit

For each microscopic source fixture used in v15.25–v15.28, construct source-equivalent representatives using exact chain relations, including

\[
s' = s + B_2f
\]

where defined, and more generally exact cycle additions

\[
s' = s+z,\qquad z\in\ker B_1.
\]

The gate must compare **only provenance certificates/typed data** attached to the representatives.

For each tested pair classify:

```text
PROVENANCE_IDENTICAL
PROVENANCE_DISTINCT_CERTIFIED
PROVENANCE_DISTINCTION_GAUGE_ONLY
PROVENANCE_RELATION_UNSPECIFIED
```

A nontrivial source extension requires at least one `PROVENANCE_DISTINCT_CERTIFIED` class that survives every certified provenance gauge and relabeling control.

The gate must not infer physical distinctness from `s != s'` alone.

---

## 7. Countermodel requirement

To claim that provenance **does** determine an enhanced source carrier, the gate must defeat a countermodel analogous to v15.08:

- same coarse `q`;
- same externally visible frozen source-role/legitimacy data wherever the archive says they are the same;
- different microscopic representatives;
- alternative admissible provenance assignments consistent with all frozen certificates.

If two such assignments survive while one distinguishes the representatives and the other identifies them, then the frozen ontology does not entail a unique provenance extension.

Classification:

```text
PROVENANCE_EXTENSION_NOT_ENTAILED
```

This logical non-entailment takes priority over a convenient computational lift.

---

## 8. Covariance and naturality requirements

A provenance distinction can enter `S_prov` only if its transformation rule is already certified or derivable from exact frozen combinatorics.

Required checks:

1. **Relabeling covariance:** equivalent cell/node relabelings transport provenance classes consistently.
2. **Orientation convention independence:** reversing a stored incidence orientation changes coordinates according to the certified signed action, not source identity arbitrarily.
3. **Genesis-root preservation:** transformations allowed inside the gate must preserve whatever root/witness data the relevant frozen artifact declares invariant.
4. **Composition compatibility:** if the frozen provenance structure defines composition/concatenation, the candidate carrier must respect it exactly.
5. **No target feedback:** cycle-response or gravity observables cannot define the provenance action.

A candidate without a certified action is classified:

```text
PROVENANCE_DISTINCTION_EXISTS_BUT_ACTION_NOT_CERTIFIED
```

and does not reach representation-readiness.

### 8.1 Representation-readiness requirement

A certified action is necessary but not sufficient to reopen the coupling solver. A candidate must additionally carry a finite linear representation or a canonical frozen-theory linearization whose equivariance and projection to `Q` can be checked exactly.

If the provenance carrier is only a set/groupoid/discrete-label object with no canonical linearization, v15.29 may certify the carrier itself but must classify it as not representation-ready. An arbitrary free-vector-space construction is not automatically physical and must not be introduced merely to feed the solver.

---

## 9. Projection-to-q requirement

The candidate enhanced carrier must retain the already-certified coarse source as an explicit quotient/projection.

At minimum the gate must establish a typed map

\[
\pi:\mathcal S_{\rm prov}\to \mathcal Q
\]

such that tested representatives reproduce the same `q` exactly.

No hidden metric, basis optimization, pseudoinverse, or chosen section

\[
\sigma:\mathcal Q\to\mathcal S_{\rm prov}
\]

is permitted. A section would itself be a selector and is not needed to certify the extension.

---

## 10. Preregistered outcomes

The gate must adjudicate mechanically into one of these primary statuses.

### A. `PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE`

All provenance information certified as source-relevant is constant on each tested and theorem-covered `q` fiber, or is removed by certified gauge. No enhanced source carrier is earned.

### B. `PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED`

Frozen provenance evidence does not determine whether `q`-equivalent representatives are physically/provenance-equivalent. Countermodels survive. No extension is earned.

### C. `PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION`

A certified nontrivial distinction exists inside `q` fibers, but there is no certified covariant action/label structure connecting that distinction to the v15.28 representation problem.

### D. `PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED`

A nontrivial typed carrier `S_prov`, projection `pi:S_prov->Q`, and certified natural transformation law are all earned without downstream tuning. The carrier itself is certified, but this status does **not** imply a linear representation suitable for the v15.28 coupling solver.

### E. `PROVENANCE_SOURCE_REPRESENTATION_READY`

Outcome D holds and, in addition, the carrier has a certified finite linear representation or canonical frozen-theory linearization with exact action and projection equivariance. This is the only outcome that may open a **separate future coupling-space gate** for `S_prov`.

### F. `PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM`

The desired distinction can be obtained only by explicitly declaring new physical source semantics. v15.29 must stop and request separate approval rather than adopt it.

---

## 11. Breakthrough rule

v15.29 may issue an **upstream structural breakthrough alert** only for outcome E and only if all of the following are true:

- nontrivial provenance distinctions survive certified gauge;
- the projection to `q` is exact;
- the carrier/action are natural under the frozen relabeling structure;
- a finite linear representation or canonical frozen-theory linearization is certified;
- no arbitrary cross-domain embedding or free-vector-space convenience construction is inserted;
- no gravity observable or response target is used in selection;
- the result survives explicit countermodels.

Outcome D without representation-readiness is progress but not the preregistered breakthrough threshold.

Even for E:

```text
signal_of_life = false
gravity_canary_certified = false
physical_gravity_derived = false
Pillar_3 = OPEN
```

A representation-ready source carrier is not a gravity signal. It merely supplies the missing typed input required to resume constitutive-coupling classification in a separate gate.

---

## 12. Hard forbidden selectors

The gate must not use any of the following to decide provenance faithfulness or carrier structure:

```text
remote holonomy
holonomy magnitude
inverse-square response
Newtonian agreement
Einstein/GR agreement
lensing/cosmology
continuum smoothness
minimum norm / Hodge choice
physical distance
entropy
pruning
RCR/actual outcome
physical time
best-fit response
PCA/SVD alignment
random isometry
hand-selected node↔site correspondence
matching dimensions/cardinalities alone
```

The words may appear only in explicit false claim-boundary flags or historical context, never as scores or selectors.

---

## 13. Controls

### Positive synthetic control

Construct a toy provenance extension with a declared nontrivial fiber label and an exact relabeling action. The gate must certify it as an enhanced carrier.

Add a second synthetic variant with an explicit finite linear representation to prove the machinery distinguishes `PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED` from `PROVENANCE_SOURCE_REPRESENTATION_READY`.

These controls are never admitted as UQCF physical evidence.

### Negative collapsed control

Construct a provenance record that is a deterministic function of `q` only. The gate must classify it as `PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE`.

### Negative arbitrary-representative control

Use raw `delta_b` labels with no provenance certificate. The gate must reject them despite their ability to distinguish cycle shifts.

### Negative supplied-map control

Reuse v14.04-style supplied intertwiners/maps. The gate must retain conditional status and refuse physical promotion.

---

## 14. Implementation architecture

Implementation, if later approved, should be additive under

`ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/`

with modules conceptually separated as:

```text
provenance_inventory.py
fiber_model.py
provenance_equivalence.py
action_audit.py
source_extension_gate.py
replay.py
viewer.html
```

Tests must be written before implementation and must include:

- exact hash/type inventory checks;
- exact q-fiber construction;
- face-boundary and general-cycle representative controls;
- countermodel non-entailment tests;
- relabeling/action covariance tests;
- projection-to-q tests;
- representation-readiness/linearization tests;
- fail-closed source-semantics tests;
- synthetic positive/negative extension controls;
- claim-boundary tests;
- inherited v15.11–v15.28 regressions in exact-head CI.

No implementation file may import or compute gravity/holonomy scoring.

---

## 15. Presentation boundary

The offline inspector/video may show only:

```text
q-fiber representative
→ provenance certificate/equivalence class
→ gauge survival
→ action status
→ carrier status
→ representation-readiness status
```

It must not plot a gravitational field, spatial falloff, remote holonomy, or preferred coupling.

Suggested six-scene replay:

1. coarse q quotient;
2. multiple microscopic representatives in one fiber;
3. provenance identity versus distinction;
4. gauge/relabeling controls;
5. extension/countermodel/representation-readiness adjudication;
6. final status and gravity boundary.

Playback remains explicitly nonphysical time.

---

## 16. Relationship to previous results

v15.29 must preserve, not reinterpret away:

- v15.08: source semantics irreducible relative to frozen ontology;
- v15.09: canonical neutral quantum structure does not derive a retained quantum carrier or cross-sort functor;
- v14.04: nontrivial provenance-to-support mapping requires representation data not automatically supplied;
- v15.27: the desired cycle response does not factor through coarse `q` alone;
- v15.28: q-only symmetry leaves a 3-dimensional coupling space, while no archived provenance-enhanced physical carrier was representation-eligible.

A positive v15.29 result would not contradict those statements. It would require genuinely new information already present in provenance that was not part of the coarse `q` quotient, with its own certified action and, for representation-readiness, linear structure.

---

## 17. Stop rule

Stop immediately if any proposed positive result depends on:

- declaring raw microscopic incidence physical by fiat;
- choosing among q-fiber representatives using a response/geometry score;
- identifying provenance and torus/quantum labels by matching counts or dimensions;
- using an arbitrary supplied intertwiner;
- freely linearizing a discrete provenance object merely to make the coupling solver applicable;
- interpreting Genesis/history legitimacy as operator source semantics;
- using pruning, entropy or physical time upstream.

If the archive does not entail the provenance relation on q fibers, report the non-entailment result and stop. Do not continue searching the same frozen dependency set for a relation ruled out by explicit countermodels.

---

## 18. Delivery discipline

Implementation, if approved later, uses tests-first commits, exact-head GitHub Actions, all inherited selected regressions, a draft/unmerged PR, and a digest-verified prerelease containing source/report/numerical evidence plus gravity-blind HTML/video.

`main` remains unchanged unless the user explicitly approves a later merge.
