# Four-child interface implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native inline implementation task-by-task. All numerical science/tests run on GitHub; local work is source authoring, static inspection and byte/log/archive audit only.

**Goal:** Implement and independently validate the accepted four-child interface, preserving its native admissibility and global one-unit repair bound.

**Architecture:** Retain the inherited label-to-vertex bitset producer representation, but add separate four-root feasibility, fixed-root clearance and complementary-cover routines. Independently reconstruct support-set states and exact case identities in the verifier. Preserve the v16.52 source and publication stack, adapting only new-stage files and workflows.

**Tech Stack:** Python3.11, sympy1.13.3, mpmath1.3.0; GitHub Actions ubuntu24.04, inherited pinned actions.

**Spec:** NATIVE_ADMISSIBILITY.md, FOUR_CHILD_INTERFACE.md, NEXT_VALIDATION_GATE.md and VALIDATION_PROTOCOL.md in this directory. Accepted proof SHA256 a42d22c25568475f8e9373c6288646b1b68abdc90ecc657a517a0375990f8872.

## Global Constraints

- Parent b6bf95798ec5892963c29f4020f8b75069fd2e3b; branch research/v16.53-four-child-boundary; API-backed isolated source mirror, as in v16.52.
- Preserve native nonempty nested supports, fixed global root, single-incidence primitives and SUM of deviations over every internal vertex <=1.
- Internal arities2/3/4 only; no broader category or physical claim. All prior source/evidence stays unchanged.
- Exact F/R/N/M domains and canonical bit order are frozen in VALIDATION_PROTOCOL.md. No extra large directed campaign or deeper binary/ternary research sweep.
- All1,150 inherited checks and42 inherited scientific files remain required;45 total deterministic scientific files after the three new outputs.
- Numerical science/tests on GitHub only, pinned environment,45-minute cap. Stop INCOMPLETE on coverage/resource/provenance failure. Construction failure is not a nonunit witness.
- Written plan review precedes implementation. Native inline execution remains the chosen method; independent source and receipt reviews remain mandatory.

## Review Focus

1. Root=P but child width<k: clearance must work with the destination already present at the root; test_clearance_root_full_exact checks every interior coordinate and the fixed child root during clearance.
2. Full target cover bin and spare bin equal to the moving label's current bin: test_cover_spare_current_bin checks the specified four complement incidences and capacities at each one.
3. A full-width child has zero complement capacity; test_zero_capacity_child fixes its root while testing the other bins. Leaves use direct nonempty root deletion, not an internal-union assertion.
4. Parent already one unit from target: test_recursive_call_requires_exact_parent rejects a recursive normalization call in that phase and test_stacked_defect_rejected checks the global sum independently.
5. Failure after real clearance primitives: test_partial_clearance_retained preserves the global partial path; test_resource_failure_incomplete prevents scientific misclassification.

## Files and ownership

All stage files below live in ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/.
- feasibility.py: four-child producer region search and canonical compact tuples.
- cover.py: capacity-bounded complementary-cover primitive paths.
- producer.py: inherited representation, generic recursion, clearance and four-child joining.
- verifier.py: independent support-set feasibility, starts/endpoints, path and corpus gates.
- coverage.py: verifier-side frozen identities; producer enumeration stays in producer.py.
- test_red.py, test_mechanisms.py, test_gate.py, test_integrity.py and TEST_MANIFEST*.json: exact controls, RED receipts, assertion bindings.
- run_campaign.py, run.py, integrity.py, snapshot.py, archive.py, publish.py: adapted inherited execution and evidence machinery.
- .github/workflows/v16.53-red.yml and .github/workflows/v16.53-four-child-boundary.yml: development controls and definitive campaigns.

## Task1 — independent verifier and preimplementation RED

**Interfaces:** topology(tree)->(children,parent,internal); hitting(supports)->int; root_feasible(widths,q,k)->bool; canonical_roots(widths,q,k)->ordered tuple of sets or infeasible; model(tree,q,k,permutation,mode)->width,start,end; expected_specs(kind)->ordered identities; path_check(tree,k,q,path,start,end)->peaks; verify(document)->typed verified result or failure.

- [ ] Author coverage.py and verifier.py without producer imports. Derive F feasibility by explicit combinations of root-support subsets, independent of the producer's15-region count search. For recursive N minimum widths, use a separate exhaustive incidence-allocation feasibility routine with independent label-subset hitting checks; cache immutable questions only. Bound width search by sum(widths)-(arity-q), with existing proved2/3 formulas available as independently checked inherited boundaries.
- [ ] Implement the separately tagged one-case canonical control exactly as specified in the protocol. Assert complete control acceptance, unmutated omission rejection, and valid starts/endpoints before introducing the supplied-only coverage mutant.
- [ ] Write test_four_child_implementation_missing and test_actual_verifier_omission_red with exact assertion messages from the protocol. Missing implementation is an assertion failure, not an import exception. Freeze their source and TEST_MANIFEST_RED.json before execution; do not create producer.py yet.
- [ ] Run the pinned GitHub RED workflow. Require exactly two intended failures and zero errors; download and audit archive SHA, source identity, exact test IDs and messages. Preserve original archive and receipt in the new stage before continuing.
- [ ] Add GREEN verifier controls test_duplicate_rejected, test_substitution_rejected, test_wrong_profile_rejected, test_infeasible_not_construction_failure, test_native_unsafe_q2_rejected_as_unit and test_native_unsafe_q3_rejected_as_unit. Assert actual verify entrypoint rejection, not helper-only behavior. For unsafe paths assert admission passes and only the unit bound fails.
- [ ] Commit this independently testable verifier/RED deliverable; record status truthfully.

## Task2 — feasibility, clearance and cover primitives

**Interfaces:** feasibility.minimum(widths,q)->(m,canonical ordered supports); cover.reconfigure(start,target,capacities,order)->list of covers including endpoints; producer.clear_role(state,nodes,child,x,y,path)->None; producer.lift_root_path(state,tree,q,root_path,order,trace)->list of native states. Every cover step changes one membership; clear_role fixes the child root and changes only proper descendants.

- [ ] Before these implementations exist, add expected-failure tests for test_clearance_root_full_exact and test_cover_spare_current_bin using the literal protocol fixtures. Preserve GitHub RED with two intended missing-routine assertion failures and zero errors.
- [ ] Implement feasibility.minimum using15 nonempty incidence-region multiplicities, exact region-cover number and finite width search. Construct the Section2 child-major canonical tuple with bits1<0. Test it against all independently reconstructed F rows; for q4 also assert minimum=sum(widths) for all width tuples in {1,2}^4 beyond k=4 without claiming those unenumerated F rows were executed.
- [ ] Implement clear_role with fixed-root preorder additions and reverse-preorder deletions below the root. Reject a destination occurring in proper descendants; allow it at the root. Test no root movement, exact interior coordinates per primitive, unchanged proper-union size after completion, leaf deletion, and deletion-at-minimum rejection. Retain completed primitives on injected failure.
- [ ] Implement cover.reconfigure with deterministic single-owner reduction, first misplaced label, first misplaced occupant of a full target bin, first spare bin, and target extras restored last. For the specified fixture assert covers progress through ({0,1},{1,2},{},{}), ({0,1},{2},{},{}), ({0,1},{0,2},{},{}), then ({1},{0,2},{},{}). Check coverage/capacity after every intermediate duplicate.
- [ ] Implement lift_root_path. Before deleting a used child-root label, select the first root label outside the proper union, clear, then delete. Root additions need no descendant edit. Test zero-capacity children, root-full but non-full-width children, leaves, invalid root steps, and partial global-path propagation.
- [ ] Run all mechanism GREEN controls on GitHub. Audit exact identities/assertions and every expected failure signature before committing the mechanism deliverable.

## Task3 — recursive integration and focused definitive validation

**Interfaces:** producer.data(tree,q)->nodes,targets,widths; canonical(tree,k,q,order=None)->state; normalize(state,tree,k,q,order=None,trace=None)->path; specs()->F/R/N/M identities; produce()->complete attempted certificate. ConstructionFailure retains original exception/category and full global partial path. run_campaign.run(out)->three new deterministic outputs plus fresh parent52/42-file evidence.

- [ ] Add failing integration controls test_q2_expand_contract_guard, test_q3_cover_guard, test_q4_disjoint_exchange, test_four_child_under_binary_parent, test_repeated_four_child, test_recursive_call_requires_exact_parent, test_stacked_defect_rejected, test_canonical_endpoint, test_compact_contraction and test_transported_order_equivariance. The two nested tests use E and G protocol templates, not additional shape searches. Run and retain genuine GitHub RED before joining code.
- [ ] Extend only the new producer copy. Four-child q1/q2/q3 uses initial child normalization, guarded root path, exact-interior lifting and final child normalization. q4 uses the inherited disjoint-role assignment. Existing2/3 joins call the same generic child interface. Check and record exact parent at every recursive call boundary.
- [ ] Enumerate every protocol identity independently in producer and verifier. Preserve all attempted records, infeasible F observations, explicitly expected M rejections and partial failures. Verify exact identity equality and order, reconstructed starts and the canonical endpoint, native admission and all internal coordinates at every primitive.
- [ ] Add test_partial_clearance_retained and test_resource_failure_incomplete plus assertion-manifest tampering controls. Freeze new test identities, expected outcomes and complete AST assertion hashes; preserve all1,150 inherited identities/assertion hashes without weakening assertions.
- [ ] Adapt the inherited run/publication machinery. Freshly invoke v16.52/run_campaign.py and compare its42 outputs; retain parent52 plus CERTIFICATE.json.gz, SUMMARY.json and VERIFY.json, exactly45 scientific files. Source snapshot includes accepted proof/review, native protocol, plan, manifests, workflows and inherited source.
- [ ] Obtain independent whole-source review of proof correspondence, domain coverage, failure classification and workflow before definitive execution. Resolve every Critical/Important finding with targeted failing controls and review; preserve all corrections prospectively.
- [ ] Run pinned full preflight, primary science and separate fresh reproduction on GitHub. Require all inherited and frozen new checks, exact F/R/N/M coverage and all45 scientific bytes equal. Audit downloaded original archives, source bindings, logs and independent-verifier results. Stop explicitly on failure; do not reduce the domain.

## Task4 — durable publication and closeout

- [ ] Publish complete evidence, original execution archives in verified chunks when necessary, deterministic outputs, source objects, logs/API provenance and content manifests. Report mechanism coverage and scientific meaning separately from corpus totals.
- [ ] Audit every published blob and unchanged source. Independently review the exact published PR101 head; update its description with all deviations and scoped result.
- [ ] Mark ready and merge only that reviewed head into the verified integrated parent. Check ordered merge parents and publication-tree equality.
- [ ] Run actual-merge full stack and focused campaign on GitHub; require all45 bytes equal and audit original archive digests and durable receipt manifest.
- [ ] Obtain independent assistant receipt decision, publish it on a separate audit branch, read back exact bytes and recheck terminal workflow success. Only then report CLOSED/CERTIFIED. Analytical acceptance remains separately documented if implementation gates fail.

## Plan self-review and handoff

The tasks cover every NEXT_VALIDATION_GATE obligation, including the five Review Focus conditions. No code or scientific execution accompanies this plan. Native inline execution preserves the existing session method and avoids parallel edits to tightly coupled proof routines. Written-plan approval is the next implementation gate required by the writing-plans skill.
