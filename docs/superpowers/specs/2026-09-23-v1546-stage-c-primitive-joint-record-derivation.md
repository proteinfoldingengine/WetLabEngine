# v15.46 Stage C — Primitive Joint-Record Derivation Gate

**Status:** DESIGN FREEZE — implementation not started  
**Purpose:** determine whether the already-earned retained/pruning ontology uniquely determines a quantum joint-record representation, rather than merely permitting one.

## Scientific question

Given only frozen retained primitives that are already earned before the source/geometry construction, does the ontology determine, up to explicitly declared gauge,

`(Hilbert carrier, factorization/subsystem inclusions, joint state, overlap structure)`?

Stage C tests **derivability and uniqueness**, not whether one attractive quantum representation can be authored.

## Frozen inputs

The gate may consume only hash-pinned predecessor statements about:
1. retained records / lineage and their dependency structure;
2. ordered recoverability / pruning relations;
3. compatibility constraints already certified;
4. Genesis provenance constraints and the v15.09 carrier-origin boundary.

It may not consume v15.39's newly assumed incidence source as evidence that a quantum carrier was derived, nor any v15.43–v15.45 curvature output, source-response agreement, gravity target, continuum target, or empirical fit.

## Representation contract

A candidate representation must explicitly provide:
- total Hilbert space dimension;
- tensor/subsystem factorization or algebra inclusions;
- joint density operator;
- overlap maps/inclusions;
- a provenance map from frozen retained primitives to every non-gauge representation choice.

No convenient completion, maximum-entropy rule, minimum-norm selector, spectral-edge choice, or geometry-selected representation is admissible unless independently present in the frozen inputs.

## Primary adjudication

The primary test is uniqueness modulo **earned gauge**.

- `UNIQUE_UP_TO_EARNED_GAUGE`: every admissible representation is connected by a gauge transformation already certified by the frozen ontology.
- `REPRESENTATION_NONUNIQUE`: construct two admissible representations satisfying every frozen primitive constraint but not related by earned gauge.
- `NO_REPRESENTATION_DERIVED`: the frozen constraints do not even provide the typed data needed to define an admissible representation.
- `ILL_TYPED`: a required comparison cannot be made without adding a cross-domain identification.

Merely relabeling quantum sites counts as gauge only when the retained ontology itself earns that identification. v15.09's two-sort boundary therefore remains active.

## Adversarial controls

1. **Dimension control:** a representation with a different compatible carrier dimension cannot be silently identified with the certified C^125 parent.
2. **Factorization control:** the neutral state `I_D/D` must not select a tensor decomposition.
3. **Cross-domain control:** independently rigid retained nodes and quantum sites do not define a node-site bijection.
4. **State-family control:** if multiple joint states satisfy the same retained constraints, no state may be selected by downstream curvature.
5. **Gauge control:** a claimed equivalence must exhibit the already-earned gauge action, not a newly declared isomorphism.
6. **Null control:** failure to derive a representation is not a zero physical source.

## Execution strategy

Task C1 freezes a machine-readable primitive contract and verifies its predecessor hashes.  
Task C2 constructs the smallest exact representation family satisfying that contract.  
Task C3 searches for two inequivalent realizations and produces an explicit witness if they exist.  
Task C4 independently checks the witness against every frozen constraint and the gauge definition.  
Task C5 records the mechanical verdict and stops. Geometry and incidence coupling remain unexecuted unless the verdict is `UNIQUE_UP_TO_EARNED_GAUGE`.

All executable work uses test-first RED→GREEN development, deterministic exact arithmetic where possible, CPython 3.13.5, and fail-closed source pins.

## Claim boundary

A nonuniqueness result would establish that the **audited frozen ontology does not uniquely derive the joint quantum record**. It would not prove that quantum mechanics is non-emergent in every extension of UQCF-GEM.

A uniqueness result would establish only uniqueness relative to the frozen finite contract and earned gauge; it would not by itself establish gravity, stress-energy, continuum GR or empirical validity.

No new physical source law is adopted. Source correspondence remains `NOT_EVALUATED`. Pillar 3 remains **OPEN**.
