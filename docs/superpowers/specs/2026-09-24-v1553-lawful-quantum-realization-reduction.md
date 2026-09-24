# v15.53 — Lawful Quantum Realization / Reduction Certification Design

Date: 2026-09-24

## Purpose

v15.52 proved the general observation-factorization theorem but rejected its submitted quantum witness because the candidate records were labels rather than independently validated quantum realizations. v15.53 will test the missing premise directly: whether an explicitly defined, finite, lawful quantum realization family contains two admissible realizations with the same retained readout and distinct earned target classes.

This is a certification experiment on a frozen finite family. It is not a universal theorem over all quantum theories, not a physical source law, and not a gravity result.

## Scientific question

For a frozen realization family M, retained reduction O:M->E, and earned equivalence-class map tau:M->K, does there exist a pair m1,m2 in M with O(m1)=O(m2) and tau(m1)!=tau(m2)?

If such a pair is independently validated, then v15.52 T1 applies and exact recovery of the target class from that retained readout is obstructed for this family.

If no such pair exists in the frozen family, the result is only NO_WITNESS_IN_FROZEN_FAMILY. It does not imply universal recoverability or universal absence of a quantum-origin obstruction.

## Frozen predecessor boundary

v15.53 must preserve these predecessor results without promoting them:

- v15.46 Stage C: REPRESENTATION_NONUNIQUE for audited two-sort expansions of the same frozen reduct.
- v15.50: retained leg derivable in the tested construction; quantum leg absent/unearned.
- v15.51: TESTED_PRIMITIVES_INSUFFICIENT for the tested finite operational packages.
- v15.52: T1 general factorization theorem proved; submitted label-only witness rejected; T2 NOT_CERTIFIED; T3 conditional.

The v15.53 implementation must pin the exact predecessor blobs it consumes.

## Design principle

The realization objects must carry mathematics, not names.

A candidate is admissible only if its carrier, states/operations, composition, recovery structure, and typed relations are explicitly represented and independently checked. No field named admissible, quantum, inequivalent, target_class, or similar may establish validity by assertion.

The reduction O must be computed from each realization. It may not copy a prebuilt retained observation dictionary into multiple candidate records.

The equivalence relation must be frozen before witness search and evaluated mechanically from the realization structure. Candidate IDs and enumeration order must not affect equivalence.

## Realization family M

Use a finite exact family with no floating-point tolerances.

Each realization record contains:

1. finite carrier sites with exact dimensions;
2. finite state/operation data represented by exact integer/rational tables or finite permutation/transition objects;
3. composition law with identity and associativity checks on the declared finite domain;
4. recovery-capable operations with exact closure and typing checks;
5. typed incidence/refinement assignments linking only structures permitted by the frozen family definition;
6. no retained-source node labels as privileged quantum-site selectors.

The first family should be deliberately minimal: large enough to contain nontrivial distinct realizations, small enough for exhaustive enumeration and independent replay.

No Hilbert-space dimension, node-site dictionary, matrix algebra, or downstream geometry may be injected from v15.52 target labels. If a carrier dimension is part of the family, it must be part of the family definition itself and applied uniformly before witness search.

## Admissibility predicate A(m)

A realization is admitted only if all of the following pass:

- schema/type validation;
- finite carrier consistency;
- identity and composition closure;
- associativity on every composable triple;
- recovery-operation typing and closure;
- incidence/refinement compatibility;
- no forbidden selector or target-derived field;
- canonical serialization and deterministic replay.

Admissibility is recomputed by the verifier. Producer status flags are ignored.

## Retained reduction O

The retained reduction is a deterministic function of the realization.

It must emit exactly the frozen v15.52 retained observable domain:

- object count;
- lineage incidence;
- dependency incidence;
- recoverability relation;
- composition table;
- refinement diagram;
- disjoint partition.

For each realization, the verifier recomputes these readouts from realization structure and checks that they satisfy the retained-source schema.

Two candidates count as observationally equal only when their independently computed canonical readouts are exactly equal.

The reduction must not access candidate target class, candidate ID, enumeration index, or post-result information.

## Earned target equivalence

The target equivalence relation is frozen before enumeration.

Two realizations are equivalent only when there exists an explicitly permitted structure-preserving isomorphism between their quantum-side data. The verifier must enumerate all permitted finite bijections and check preservation of:

- carrier dimensions/types;
- state/operation tables;
- composition;
- recovery-capable operations;
- typed incidence/refinement assignments.

Candidate labels are ignored. No new gauge may be declared after witness exposure.

The class map tau is the canonical equivalence class under this relation.

## Witness search

After the family, admissibility predicate, reduction, and equivalence are frozen:

1. enumerate all candidate realizations;
2. reject inadmissible candidates;
3. compute O(m) independently for every survivor;
4. compute tau(m) independently for every survivor;
5. partition candidates by retained readout;
6. within each retained fiber, search for more than one target equivalence class.

A positive witness requires two concrete admissible realizations with identical retained readout and distinct mechanically certified target classes.

The producer may report candidate pairs, but the independent verifier must reproduce the family, admissibility, reduction, target classes, and witness from scratch.

## Required verdicts

Exactly one primary result:

- CERTIFIED_FAMILY_OBSTRUCTION_WITNESS
- NO_WITNESS_IN_FROZEN_FAMILY
- FAMILY_INVALID
- VERIFICATION_FAILED

CERTIFIED_FAMILY_OBSTRUCTION_WITNESS permits only this statement:

"In the frozen v15.53 realization family, the registered retained reduction does not uniquely determine the registered quantum target equivalence class."

It does not establish a universal quantum-origin theorem, a physical source law, gravity, continuum physics, or Einstein equations.

## Mandatory controls

The verifier must fail or change verdict under each relevant mutation:

1. candidate labels swapped while structures remain fixed — verdict invariant;
2. enumeration order permuted — verdict invariant;
3. target class field injected — rejected;
4. retained readout copied rather than derived — detectable by mutation/recomputation;
5. one composition entry changed — candidate inadmissible;
6. associativity broken — candidate inadmissible;
7. recovery typing broken — candidate inadmissible;
8. post-result gauge added — frozen-contract mismatch;
9. one allowed isomorphism omitted — incomplete-equivalence detection;
10. an invented isomorphism added — invalid-equivalence detection;
11. malformed or duplicate candidates — rejected;
12. source relabeling within the retained domain — scientific verdict invariant;
13. JSON round-trip — verdict invariant;
14. deterministic double replay — byte-identical result.

## Independence requirement

The independent verifier must not call producer functions for admissibility, retained reduction, equivalence, class construction, or witness selection.

It may import or parse only the frozen contract and raw candidate data needed to reconstruct the computation.

A positive result produced only by the same code path that generated the candidates is not certified.

## TDD and execution gate

Development must use RED->GREEN.

Before implementation, tests must exist that fail because the realization family, lawful reduction, and semantic verifier are absent. Existing v15.46-v15.52 suites remain regression gates.

No predecessor scientific file may be edited to make v15.53 pass. Corrections to predecessor interpretation must be additive documentation only.

## Deliverables

Create a new directory:

ResearchHistory/UQCF-GEM/demos/v15.53-lawful-quantum-realization-reduction/

Planned components:

- realization_contract.py — frozen family definition and prohibited inputs.
- realization_family.py — raw finite realization enumeration only.
- reduction.py — producer-side deterministic retained reduction.
- equivalence.py — producer-side finite isomorphism/equivalence calculation.
- witness_search.py — producer-side partition/search.
- verify_realization_obstruction.py — independent recomputation and adjudication.
- focused test files for contract, family, admissibility, reduction, equivalence, witness search, and independent verification.
- docs/RESULTS.json and an exact-head CI receipt only after authoritative execution.
- a branch-scoped GitHub Actions workflow running v15.53 plus inherited v15.46-v15.52 regressions.

## Success criteria

v15.53 is scientifically successful if it resolves the missing premise honestly in either direction:

- a genuine mechanically certified same-readout/distinct-target pair is found; or
- the frozen lawful family is exhaustively shown not to contain one.

The experiment is not successful merely because tests are green. Green tests certify execution of the frozen experiment, not the desired scientific outcome.

## Claim firewall

Always preserve:

- source_correspondence=NOT_EVALUATED
- Pillar_3=OPEN
- no physical source law adopted
- no geometry/curvature result
- no continuum-limit result
- no empirical fit
- no fundamental physical time
- no dark-matter primitive introduced

The purpose of v15.53 is narrower: determine whether the v15.52 factorization theorem can be instantiated by an actual lawful finite quantum-side realization family rather than by labels.
