# C3 core-probe theorem — refutation replay and review disposition

Date: 2026-10-08.
Disposition: BOUNDED REPLAY PASS; SAME-ASSISTANT WHOLE-ARGUMENT CHECK FOUND NO REQUIRED MATHEMATICAL CORRECTION. INDEPENDENT MATHEMATICAL ACCEPTANCE NOT OBTAINED.

This is not a scoped scientific closeout, an independent reviewer verdict, or the post-acceptance publication audit. No external review job or polling was launched. Earlier independent acceptances do not transfer to this candidate.

## 1. Exact provenance and scope

Integrated parent b883c526cd4f19c4a7dcd69fec9cf01ab6f94a5d.
Original frozen scope 4e0cb8c68c807265fb48652b1f990a18d4a43a2c, blob 8891b150d4374a4f7fac6945fed2035f03648590.
Original proof e7dc592d0f98121c7c232f33018a0a199c30ba8e, blob d619932c44d051f2a0c698365709d6f42e02f078.
Original author audit 8ca82d010d21ccfe7c34d4507240e77e863b5c08, blob 1b2189c41a665a5bb91f97e44edd213aac0263a2.
Replay scope frozen before new executable implementation at 5a993893a99d6cab75c0a2fae4170cad61838117.
Replay source commit 4374f342a12c73bed8bffc7dad94e77316fbe14b.
Rejecting test suite commit fd46a381e10630675aedc4a5f1326bbd159929eb.
Full canonical evidence commit 93f2a284f5b9fb423f064fd4f86a7f7467787269.

The original theorem allows core edits at all four roots and arbitrary finite spectator palettes. The executable review fixes the first three roots to {a,b},{b,c},{a,c}, allows all ten signed core commands at root 4, and uses T={u} and T={u,v}. It is a strict bounded slice, not numerical proof of the entire theorem.

## 2. Whole-argument examination, explicitly same-assistant

The full original proof was reread at its immutable blob. The analytical examination checked the following obligations independently of whether the small replay passed:

- Nonempty projected root: replacing all spectator hits by one element of P4 preserves every root hit and cannot increase transversal size, since spectators occur only at root 4.
- Empty projected root: the floor requires at least two spectators; disjoint palettes give tau(P1,P2,P3)+1. The proof does not assign a finite transversal to a core family containing an empty support.
- Necessity: the same immutable Z satisfies every observed root-4 floor, yielding the maximum observed deficit D.
- Constructive sufficiency: replacing Z by any Z' with |Z'|>=D preserves floors, the exact hitting number, core observations, membership preconditions and each committed toggle. Rejection of a legal command remains permitted, so every rejected outcome can also be reproduced.
- Adaptation: identical observation prefixes give identical commands for the declared observation-driven deterministic controller; no hidden-support access enters the induction.
- Restoration and memory: +d is a legal successor of a successful -d probe, but finite operational restoration requires progress not supplied by the model. The retained deficit survives restoration only while Z stays invariant.
- Termination obstruction: the all-rejection execution is legal in both the empty and nonempty worlds. No finite common observation prefix on that execution determines the capacity bit. This is a model-specific obstruction, not a universal impossibility of observation.

No mathematical change to the candidate was required by this examination. This statement records the author's assessment, not a genuinely independent assessment.

## 3. Direct-support oracle and exact coverage

The replay generates actual full supports and enumerates full-palette hitting sets to decide native floors/band admissibility. It propagates every explicit spectator subset through every possible observed outcome. The formula {Z:|Z|>=D} is used only as a claim to compare against those explicit completion sets, not to generate them.

The finite graph is explored to a fixed point. A node retains current core support, the explicit compatible spectator-subset set, and the separately tracked deficit. Because spectators are invariant and each next outcome depends only on the current full supports and command, the graph represents every finite-length observation history in this restricted carrier; there is no arbitrary history-depth cutoff. This coverage statement does not extend to moving roots 1-3 or larger palettes.

| Frozen spectator palette | Reachable retained states | Command/outcome edges |
|---|---:|---:|
| {u} | 4 | 46 |
| {u,v} | 8 | 96 |

All 12 retained states and 142 command/outcome edges were reconstructed. There are 120 explicit rejection self-edges and 22 visibly committed-change edges. Each completion comparison is exact labelled SET equality, not merely equality of cardinalities.

The counts also have a simple hand audit. With the fixed triangle, a root-4 core containing a,b or c would reduce tau to 2, so only core projections {},{d},{e},{d,e} can occur admissibly. For N=1, D=0 occurs only at the initial {d,e}, while D=1 permits three nonempty projections: four states total. For N=2 the additional D=2 class permits all four projections: eight states total. Every state has ten rejection outcomes. The N=1 graph has six additional committed outcomes; the N=2 graph has two per state, sixteen total.

## 4. Refutation and omission controls

All four intentionally incorrect estimators were rejected with explicit counterexamples in the saved JSON:

1. Credit an attempted deletion even when it rejects: at unchanged {d,e}, the empty spectator world is still compatible, but the wrong estimator deletes it.
2. Forget history after restoring the core: restored {d,e} can retain only nonempty worlds, whereas the wrong estimator reintroduces the empty world.
3. Retain only the Boolean D>0 when exact completion families are required: an empty core requires two spectators, not merely one. The Boolean is sufficient for the weaker nonemptiness predicate, but not for the full completion-family target.
4. Discard a particular same-cardinality spectator identity: the observation cannot distinguish {u} from {v}; the wrong estimator omits a valid completion.

Separate test mutations delete an otherwise valid node, delete an outcome edge, or change one spectator identity while preserving the number of records. Fresh reconstruction rejects each. A direct empty-core test checks that root4={u,v} is admissible with tau=3 while root4={u} fails floor 2. Every command's rejection self-edge is explicitly required.

## 5. Actual execution record

Executed locally with Python 3.13.5, standard library only. An initial deliberately empty graph stub failed the graph-construction test (0 states versus expected 8); the implemented replay then passed the complete local review test suite. No repository-wide or inherited-stack test run is claimed.

Reproduction from this directory:

```sh
python -m unittest -v test_core_probe_replay
python COUPLED_C3_CORE_PROBE_REPLAY.py > /tmp/c3-probe-fresh.json
python COUPLED_C3_CORE_PROBE_REPLAY.py --check COUPLED_C3_CORE_PROBE_REPLAY_EVIDENCE.json
```

The final local `python -m unittest discover -v` run reported:

```text
test_changed_same_cardinality_identity_is_rejected ... ok
test_each_command_has_an_unchanged_outcome ... ok
test_empty_projected_root_is_real_and_admissible ... ok
test_every_node_compares_exact_labelled_completion_set ... ok
test_graph_is_constructed_from_all_hidden_worlds ... ok
test_omitted_node_is_rejected_by_fresh_enumeration ... ok
test_omitted_outcome_edge_is_rejected_by_fresh_enumeration ... ok
test_one_spectator_boundary ... ok
test_restored_core_can_have_three_different_history_fibers ... ok
test_wrong_estimators_are_rejected ... ok
Ran 10 tests in 0.020s
OK
```

Test names above omit the repeated Python module/class prefix only. Exit code was 0. The runtime is an observation of this small local run, not an efficiency benchmark.

Fresh JSON reconstruction/check output, exit 0:

```text
Exact evidence readback PASS; independent review remains unfulfilled.
```

The earlier audit's Python hand-check snippet was also copied from the immutable source and re-executed, exit 0. Executed snippet SHA-256: 6bc7415ef6cdd6a53df2028cb7fad8fc4d899ed33313d751dea05ec321d78730. This provides fresh execution evidence; it does not retrospectively establish provenance of an earlier execution.

Its actual stdout was:

```text
empty seed ['d', 'e'] tau= 3 floors= True history_D= 0 spectator_count= 0
one spectator ['d', 'e', 'z'] tau= 3 floors= True history_D= 0 spectator_count= 1
successful -d ['e', 'z'] tau= 3 floors= True history_D= 1 spectator_count= 1
restored +d ['d', 'e', 'z'] tau= 3 floors= True history_D= 1 spectator_count= 1
two spectators, -d ['e', 'u', 'v'] tau= 3 floors= True history_D= 1 spectator_count= 2
two spectators, -d,-e ['u', 'v'] tau= 3 floors= True history_D= 2 spectator_count= 2
rejected -d from empty: unchanged ['d', 'e'] tau= 3 floors= True history_D= 0 spectator_count= 0
Rejected invalid deletion must not raise D.
Single-root spectator premise is necessary.
Hidden spectator removal invalidates old D=1.
Local hand-case diagnostics completed.
```

## 6. Verified source/evidence bytes

Immutable readback at 93f2a284f5b9fb423f064fd4f86a7f7467787269 returned the following blob IDs, matching the locally executed or checked bytes:

| File | Git blob SHA-1 | SHA-256 |
|---|---|---|
| COUPLED_C3_CORE_PROBE_REPLAY.py | fdb103d73dfcdba0350acb710c18b46414b061f7 | c0bf42cb2086be8e2306de31106b556473c3f19641da131faefeae8cc1bd9e4b |
| test_core_probe_replay.py | a6a3691aed8ada7425f6ae1d0351e89668db6fd6 | 48bdd92293afe6a1b23e1d02e9acca69ed492f2ca9c0c7459f6daa7121f43c75 |
| COUPLED_C3_CORE_PROBE_REPLAY_EVIDENCE.json | 857f2d69a26d758455850d20467c08687c12a2ee | ef683b37affa80e970f23736877653893cc4f1a85e040f31645a36db8c5e77bd |

The evidence JSON uses compact formatting; its parsed records exactly match fresh generated output. Byte-level GitHub readback verifies publication integrity, not independent mathematical acceptance.

## 7. What this adds and what remains blocked

The candidate is now accompanied by a self-contained direct-support checker, complete bounded state/outcome evidence, and tests that reject both false inferences and omitted valid records. At the same restored core snapshot {d,e}, the two-spectator model supports three distinct retained completion families, corresponding to D=0,1,2. The ordered record can distinguish these even though the current core snapshot cannot. This strengthens the auditability of the native-history certificate; it does not add a physical observer primitive.

The closure blocker is review provenance: no new genuinely independent mathematical verdict has been obtained. The same-assistant analytical check and the executable oracle are not substitutions for that verdict. The separate post-acceptance publication audit and scoped closeout have therefore not been claimed or performed. No new external reviewer job is running, no CI/inherited replay is claimed, and no main-branch merge is claimed.

The original mathematical scope, proof and author audit remain unchanged. Native observer access and operational progress remain hypotheses or open obligations as before. Broader C3 and C4-C6 remain OPEN; no physical force, geometry, energy, GR/ADM, continuum or fundamental time is derived.
