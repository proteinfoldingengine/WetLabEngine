# v15.29 — Pre-Time Provenance Faithfulness / Source Extension Gate

**Design status:** approved direction; design-only specification. No scientific implementation is authorized by this file.

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

A positive extension therefore has two levels:

1. **typed extension certified** — a genuine nontrivial provenance carrier and projection to `Q` exist;
2. **representation-ready extension certified** — the frozen structure additionally supplies a finite linear representation, or a canonical functor to one, suitable for the exact equivariant coupling solver.

Only level 2 may reopen the v15.28 solver directly.

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

If a nontrivial `S_prov` is certified, does it possess either:

- a certified finite linear representation compatible with the v15.28 exact solver; or
- a canonical, already-earned functor to such a representation?

A merely covariant set-valued/nonlinear carrier is scientifically interesting but does not yet become a coupling-solver input.

The gate stops before solving any downstream gravity response.

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
CERTIFIED_LINEAR_REPRESENTATION
CERTIFIED_CANONICAL_LINEARIZATION
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

and does not reach the coupling solver.

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

Frozen provenance evidence does not determine whether `q`-equivalent representatives are physical/provenance-equivalent. Countermodels survive. No extension is earned.

### C. `PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION`

A certified nontrivial distinction exists inside `q` fibers, but there is no certified covariant action/label structure connecting that distinction to the v15.28 representation problem.

### D. `PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED`

A nontrivial typed carrier `S_prov`, projection `pi:S_prov->Q`, and certified natural transformation law are all earned without downstream tuning. This is an upstream structural result, but it does **not** by itself authorize the v15.28 coupling solver unless representation readiness is also certified.

### D2. `PROVENANCE_SOURCE_REPRESENTATION_READY`

Outcome D holds and, in addition, the carrier has a certified finite linear representation or a canonical frozen-theory functor into one. This is the only outcome that directly reopens the exact v15.28 coupling-space solver as a subsequent gate.

### E. `PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM`

The desired distinction can be obtained only by explicitly declaring new physical source semantics. v15.29 must stop and request separate approval rather than adopt it.

---

## 11. Breakthrough rule

v15.29 may issue an **upstream structural breakthrough alert** for outcome D or D2 only if all of the following are true:

- nontrivial provenance distinctions survive certified gauge;
- the projection to `q` is exact;
- the carrier/action are natural under the frozen relabeling structure;
- no arbitrary cross-domain embedding is inserted;
- no gravity observable or response target is used in selection;
- the result survives explicit countermodels.

D2 is stronger than D because it additionally certifies representation readiness.

Even for D2:

```text
signal_of_life = false
gravity_canary_certified = false
physical_gravity_derived = false
Pillar_3 = OPEN
```

A certified source representation is not a gravity signal. It merely supplies the missing typed input required to resume constitutive-coupling classification.

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

Construct a toy provenance extension with a declared nontrivial fiber label and an exact finite linear relabeling action. The gate must certify it as representation-ready.

This proves the machinery can recognize a valid extension. It is never admitted as UQCF physical evidence.

### Negative collapsed control

Construct a provenance record that is a deterministic function of `q` only. The gate must classify it as `PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE`.

### Negative arbitrary-representative control

Use raw `delta_b` labels with no provenance certificate. The gate must reject them despite their ability to distinguish cycle shifts.

### Negative supplied-map control

Reuse v14.04-style supplied intertwiners/maps. The gate must retain conditional status and refuse physical promotion.

### Nonlinear-but-covariant control

Construct a toy provenance carrier with a natural relabeling action but no canonical linearization. The gate may certify a typed extension but must not mark it representation-ready.

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
- representation-readiness tests;
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
→ extension status
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
- v15.25: bare compatibility does not force long-range response;
- v15.26: response target uniquely determines response only conditionally;
- v15.27: cycle-response target does not factor through q alone;
- v15.28: q-only coupling space is three-dimensional, while physical provenance carriers are blocked by missing representation links.

A positive v15.29 result may reopen representation/coupling classification, but it does not retroactively convert any supplied map into a derived law.

---

## 17. Exact stop rule

Stop immediately if any of the following occurs:

1. the only way to distinguish `q`-equivalent representatives is raw microscopic labeling with no frozen provenance certificate;
2. a distinction exists but its action under relabeling is unspecified;
3. a natural action requires choosing a node/site/provenance correspondence by hand;
4. a source extension is selected because it improves a gravity observable;
5. the conclusion requires identifying provenance legitimacy with quantum/operator source semantics;
6. countermodels show the frozen ontology permits both collapsed and noncollapsed provenance assignments;
7. a typed/covariant extension exists but no certified linear representation or canonical linearization exists — in this case stop at D, do not promote it to D2.

Do not continue searching the same frozen dependency set after an irreducibility/non-entailment result.

---

## 18. What a positive result would permit next

Only outcome

```text
PROVENANCE_SOURCE_REPRESENTATION_READY
```

permits a subsequent gate to feed the newly certified carrier into the exact v15.28 coupling solver and compute

\[
d_\eta(\mathcal S_{\rm prov}\to \mathcal Y_{\rm cyc}).
\]

That later gate must again freeze any one-dimensional form before exposing it to a gravity canary.

Outcome `PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED` without representation readiness requires a separate representation-origin gate first.

If v15.29 instead ends in A, B, C, D-without-D2, or E, no gravity canary is reopened.

---

## 19. Claim boundary

### May be derived in v15.29

- whether frozen provenance is constant on q-fibers;
- whether certified provenance distinctions survive gauge;
- whether a nontrivial typed source extension is entailed;
- whether a certified natural action exists;
- whether that extension is representation-ready for future coupling-space classification.

### Explicitly not derived in v15.29

- a constitutive response law;
- a unique coupling form;
- coupling scale;
- long-range gravity;
- spacetime/coframe;
- stress-energy;
- Newton/Einstein equations;
- entropy production;
- pruning;
- physical time;
- actual outcome selection;
- Pillar 3 closure.

---

## 20. Governance summary

v15.29 asks whether the frozen provenance ontology contains **more source information than q**, not whether retaining more information helps gravity.

The central discipline is:

\[
\boxed{
\text{provenance distinction}
\neq
\text{physical source distinction}
}
\]

unless the frozen theory supplies the typed, gauge-stable, covariant relationship required to make that inference.

The gate is successful scientifically whether it certifies an extension or proves that the extension is not entailed. A negative result is preferable to manufacturing the missing bridge.
