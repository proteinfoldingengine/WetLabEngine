# v15.52 Task 4 — factorization proof and witness-admissibility audit

Date: 2026-09-24. Audited scientific head: `9623fcefdef304ed9e22a64625e170a622094b8f`.

## Decision

The general observation-factorization lemma below is proved. The archived Task-3 packet is **not a certified quantum-origin obstruction witness**. The independent audit rejects it; it does not manufacture replacement quantum models or change the frozen earned equivalence. T2 is not certified and T3 remains conditional. A green audit run certifies execution of these checks, not the missing quantum premises or the whole v15.52 program.

## Recovered progress and scope

v15.46 Stage C recorded `REPRESENTATION_NONUNIQUE` for its audited two-sort expansions. v15.50 left the quantum leg absent and target gauge uncertified. v15.51 recorded `TESTED_PRIMITIVES_INSUFFICIENT` for nine tested packages. These are predecessor results, not a universal impossibility theorem.

Task 3's run 36008297724 succeeded on the audited head. All 17 original v15.52 tests also passed in the blob-verified local mirror. Nevertheless, the packet and checker do not meet the frozen specification's explicit requirement that inequivalence be substantive, not merely labels.

The source files, frozen spec, original tests, predecessor outcomes and identity-only equivalence are preserved unchanged. This document is an additive audit and interpretation correction, not a silent revision of the preregistration.

## T1: exact observation-factorization theorem

Let M be a set of admissible models, let O:M->D be an observation map, and let tau:M->K assign the target equivalence class to each model. No topology, measure, quantum mechanics, geometry or physical time is needed.

There exists h:im(O)->K satisfying tau = h composed with O if and only if

    O(m1) = O(m2) implies tau(m1) = tau(m2), for every m1,m2 in M.

Equivalently, ker(O) is contained in ker(tau), where kernels here mean equality relations on fibers, not vector-space null spaces.

**Proof, necessity.** If tau=h composed with O, equal observations are equal arguments to h, hence give equal target classes.

**Proof, sufficiency.** For d in im(O), define h(d) to be the unique value tau(m) among models with O(m)=d. That fiber is nonempty by definition of im(O), and the stated condition makes the value unique. This defines a function without making arbitrary choices among models, and h(O(m))=tau(m) for every m. The empty-model case is included by the unique empty function. QED.

Thus a valid pair with equal observations and distinct target classes rules out a uniformly correct reconstruction of the target from these observations.

### Choice is not identification

A constant rule h(d)=A is still a function. On a two-model fiber with target values A and B it is correct for one and wrong for the other. Therefore the unqualified statement "no deterministic selector can choose one" would be false. The established obstruction concerns uniformly correct recovery/unique identification, not the existence of arbitrary choices or conventions.

No no-equivariant-section theorem is claimed: that would additionally require a specified target action, compatibility with the source action, and an appropriate no-fixed-point or related obstruction. The archived packet supplies no such target action.

### Randomness

For finite target classes, a randomized decoder using only d and randomness independent of the hidden model has the same output distribution at equal d. It cannot assign probability one to each of two distinct target classes at that same d. Randomness therefore cannot yield almost-sure correct recovery for both models. This does not prohibit approximate inference under additional distributional assumptions.

### Conditional T3

For a fixed admissible model class and fixed target task, any augmented observation O' that permits exact recovery must separate every pair previously having equal O and distinct tau. Restricting the admissible model class or coarsening the target equivalence is a different task. These logical alternatives must not be silently folded into a claim that one particular physical symmetry-breaking law is necessary. The theorem identifies no physical primitive.

## Why the archived quantum application does not follow

1. `obstruction_witness.py` constructs strings `Q_A/S_A/R_A/FQ_A` and `Q_B/S_B/R_B/FQ_B`. It does not construct quantum systems, operations, compositions, or typed functors, or check their laws. Identity-only dictionary inequality checks record inequality, not quantum-model inequivalence.
2. No realization family, admissibility predicate, reduction map from a quantum realization to the retained source, or independently evaluated quantum equivalence certificate is registered. The two displayed observation dictionaries are copied from the same source rather than derived from quantum models. Merely adding an `admissible=true` label does not fill this gap.
3. Both Q records reference the same mutable observation dictionary. Mutating Q1's object count to 999 also changes Q2, and the old separation checker still returns no separator. The new verifier recomputes readouts from the source and detects both corruptions.
4. Passing an empty automorphism list still yields `WITNESS_FOUND` in the archived producer. The independent verifier enumerates all finite permutations and rejects missing, duplicate, malformed or invented maps and false reported counts.
5. For the actual four-object fixture, the complete automorphism group has order one: only `(0,1,2,3)`. This is not itself a proof or disproof of target-fiber nonidentifiability. It does mean that a nontrivial source-automorphism obstruction has not been exhibited.
6. The original automorphism routine inspects only `refinement[0]`. A diagnostic second refinement diagram reduces the true group from two to one while the original routine still returns two. The new enumerator checks every diagram. This diagnostic is a software control, not a newly adopted physical fixture.
7. Equality of seven declared readouts is not a theorem that a valid quantum witness survives every extension permitted by the prose definition of E. The proved statement is conditional on a fixed observation map; one finite fixture does not establish a universal existence statement over all such extensions.

An actual T2 application needs a frozen lawful realization family M, an independently justified observation/reduction map O, an earned target equivalence defining tau, and concrete admissible m1,m2 with O(m1)=O(m2) but tau(m1)!=tau(m2). Readout closure and any covariance/naturality claim need their own proof. Diagnostic quantum models, if later introduced, must be distinguished from a first-principles derivation of the quantum target.

## Independent executable audit

`verify_obstruction.py` does not call the producer's equivalence, preservation or separation predicates. It separately checks the archived contract, all source incidences/refinement diagrams, the complete finite permutation set, and source-computed readouts. Its command-line entry point verifies nine original Git blobs before importing the producer to obtain the packet.

The implementation deliberately has **no positive quantum-certification path** under this frozen contract: no quantum-semantic validator is registered. This is a fail-closed audit, not a generic quantum theorem prover. Candidate self-attestations and differently shaped invented records cannot open that path.

The exact finite factorization checker is tested on all 1,555 tables with 0--4 models, three possible observation values and two target classes, against independent enumeration of every decoder on each observation image. These are finite regression checks supporting the implementation; the mathematical proof is the argument above, not extrapolation from those tests. No proof-assistant certification is claimed.

Additional controls cover all 24 source relabelings, common-mode and one-sided readout corruption, shared mutable records, false gauge changes, missing/extra readouts, hidden selectors, and missing/duplicate automorphisms. Two self-review regressions ensure mappings do not collapse into sequences and boolean contract flags do not collapse into integers.

The exhaustive automorphism helper is limited to at most seven source objects to bound audit cost. That computational limit does not redefine the theorem's E class. Relational typing checks do not certify category laws or quantum admissibility.

## Execution ledger and rulings

- Local setup: a nine-file mirror was reconstructed and verified against original Git blob hashes because container DNS could not reach GitHub. It is not a full repository checkout. Authoritative inherited testing is delegated to the existing branch-scoped GitHub workflow with a full checkout, not inferred from the mirror.
- RED: run 36009511693, job 107666284298, on `62667ec83e311b47c759495b83a398d9dccee424` ran 50 tests: the 17 preserved tests passed and 33 new tests failed for the explicitly asserted absence of the independent verifier. Inherited/replay stages were correctly skipped at RED.
- Local GREEN: all 52 v15.52 tests passed after implementation, including two additional exact-type self-review tests that first failed locally. Two canonical audit outputs matched byte-for-byte.
- Ruling: uphold the original spec's prohibition on label-only witnesses rather than accepting the old test names as evidence. Cost: positive quantum certification remains unavailable; inventing it would be worse.
- Ruling: express T1 as exact recovery/identification, not the nonexistence of arbitrary selection. Cost: the theorem is narrower than loose earlier prose, but has a valid proof.
- Ruling: preserve the archived producer and tests; add independent rejection rather than rewrite history. The old `WITNESS_FOUND` status must not be consumed as a certificate.
- Review: author self-review, not independent human review or a proof-assistant check. Two canonical-type defects in the new checker were reproduced RED and fixed GREEN. No external review is claimed.

The exact-head GREEN run and receipt are recorded separately after execution. Full Task 5 adjudication and positive quantum-origin certification are not claimed by this Task-4 audit. No exhaustive search of quantum realizations was performed because no admissible family was registered; absence of that search is not a proof that no valid witness exists.

## Downstream boundary

`source_correspondence=NOT_EVALUATED`; `Pillar_3=OPEN`. No physical source law is adopted. No gravity, Einstein-equation, continuum-limit, empirical or fundamental-time result is asserted. The scope is an observation-factorization proof plus a falsification of this submitted certificate's adequacy.
