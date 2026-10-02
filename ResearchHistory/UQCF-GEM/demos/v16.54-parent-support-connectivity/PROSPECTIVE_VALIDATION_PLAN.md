# v16.54 Mechanism Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if the user selects that approach. Steps use checkbox syntax. This plan is NOT execution authorization.

**Goal:** Implement and independently certify a bounded, mechanism-focused validation of the accepted v16.54 arguments, preserving all open mathematical claims.

**Architecture:** Separate deterministic path production from an independent set-based verifier and independent reconstruction of every protocol identity. Validate proof mechanisms and their failure boundaries, not a new population of deep trees. Keep mathematical proof acceptance, bounded implementation evidence and the unresolved universal conjecture as separate report fields.

**Tech Stack:** Python 3.11, standard library for new scientific routines; inherited stack dependencies sympy==1.13.3 and mpmath==1.3.0. GitHub Actions on ubuntu-24.04 only for scientific execution. Use the same pinned checkout, setup-python and upload-artifact action SHAs as the certified v16.53 workflow unless a separately recorded dependency amendment is approved.

**Spec:** RESEARCH_SCOPE.md and NATIVE_ADMISSIBILITY.md, the accepted proof/review ledger in FINDINGS.md, and the prospective protocol in Sections 2-4 below. This document proposes the transition from analytical work to implementation; it does not amend the already executed v16.53 claim.

## 1. Global constraints and approval boundary

- Current authorization is analytical only. Obtain user review of this written protocol/plan before writing implementation or running numerical work. Native execution is recommended because the producer/verifier interface is tightly coupled; independent review remains mandatory.
- Certified integrated parent: f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8. Accepted analytical additions are on research/v16.54-parent-support-connectivity and PR102; do not treat an unmerged analytical head as a new certified parent.
- Freeze the exact approved protocol commit and all analytical proof/review hashes in preregistration before the first scientific run. The freeze process resolves the then-current branch head by Git object identity, records it literally, and fails if a referenced object is unavailable. No floating branch is accepted as a scientific input.
- Record both workflow SHA and checked-out scientific SHA in every run. No local scientific execution. No random sampling, omitted difficult identities, reduced ranges, opportunistic timeouts, or successful-case-count completion criterion.
- Keep the palette, root slots, positive floors, exact endpoint target, single-incidence moves and global one-unit native budget unchanged. Lower-guard preliminary paths may exceed q only before the specified maximum-layer conversion; final path certificates must not.
- No finite passing result proves universal connectivity. A theorem precondition rejection is not a disconnected endpoint certificate. A disconnected width-floor graph is not by itself a native nested barrier.
- Do not start v16.55. Mark PR102 ready or merge only after premerge verification, publication and whole-source review. Mark v16.54 CLOSED/CERTIFIED only after the actual-merge audit passes.

## 2. Frozen objectives and identity conventions

Primary objective: every prescribed production path and local transformation satisfies its stated proof contract when independently checked at every primitive stage. Secondary objectives: exercise boundary refusal, preserve genuine rejecting evidence, and reproduce all deterministic scientific bytes independently.

Each identity is the UTF-8 compact JSON array [family,parameters,input_roots,choice] with integer labels 0,...,k-1, labelled root indices, increasing labels inside each root, and lexicographic ordering of identity records. Do not quotient labelled roots or apply unrecorded graph-isomorphism reduction. Formula-defined templates below use consecutive label intervals; that convention defines the whole template universe, rather than selecting representatives from an unstated larger universe.

For any production choice not fixed by a family below, use lexicographically least admissible minimum hitting set, ordered label pair, root index or finite assignment, in that order as applicable. This is a deterministic tie-breaker, not permission to omit identities explicitly quantified over all choices.

The independent verifier must regenerate the complete identity SET from these definitions, compare exact set equality and multiplicity, and reconstruct inputs without trusting producer records. Expected counts are derived independently after authorization; they are not currently measured or treated as preregistered discoveries. Manifest hashes freeze produced finite sets before path execution within the authorized campaign.

## 3. Complete bounded mechanism domains

These domains validate named mechanisms. They deliberately do not enumerate the large residual obstruction region derived analytically.

**M1: maximum layers and original-role packets.** For t in {4,5,6}, let P={0,...,t-1}; roots 0,...,t-1 are the corresponding singletons, and root t is each nonempty subset F of P. Singleton floors are 1; the last floor ranges from 1 through |F|. For every ordered pair of distinct labels (x,y), validate the original-role packet x<-y. For every ordered pair of such packets, including shared labels and repeated packets, validate their simultaneous ORIGINAL-membership union and its two-unit bound. For every legal incidence addition from each template vertex, validate the adjacent maximum-layer replacement rule for every minimum-cover merge choice at the endpoint(s) at level t. Include both orientations of each edge. For repeated layer removal, form one path from two endpoints obtained from the template by t-3 successive minimum-cover merges: choose the lexicographically first pair at every step for one endpoint and the last pair for the other, then join through the original template by reversing/concatenating these packet paths. Require the final converted path to stay in {2,3}. Original packet membership and recomputed sequential membership are distinct fields; a verifier must not silently substitute one for the other.

**M2: cycle buffering and ordinary element cover.** Enumerate every compact 3-row, 4-column binary matrix with nonempty rows, column sums at most 2 and total occupancy S<8. For every ordered pair with the same row-sum vector, validate the degree-two exchange construction and every primitive capacity/floor bound. Separately, for all bin-capacity vectors in {0,1,2,3,4}^3 with total at least 5, enumerate every assignment of labels {0,1,2,3} to bins within those capacities and every ordered endpoint pair; validate element-cover transfers. Add one explicit five-column repeated-color cycle: current rows {0,2}, {1,3}, {0,1,2,3}; target rows {1,3}, {0,2}, {0,1,2,3}; prescribed pending edges (0->1,row0), (1->2,row1), (2->3,row0), (3->0,row1), with buffer column 4. Verify that the prescribed pending pairing matches the endpoint differences before executing that local cycle. Coverage diagnostics must distinguish direct vacancy moves, buffered cycles, repeated row colors and the element-cover case where the spare bin is the old owner of the label being placed. An empty diagnostic category is reported as a missing mechanism witness, not counted as a success.

**M3: saturated exact endpoints.** For q in {3,4}, z in {0,1,2}, k in {q,q+1}, generate all ordered partitions of P into q nonempty parts, followed by z full-palette roots. Floors equal the part sizes and k for the full roots. Include all ordered partition pairs with the same floor vector. Verify exactness, delta=0, saturated classification and every swap's primitive band. Also classify every compact tuple for r=k=3 and every positive floor vector with total (r-q+1)k for q=3; this tiny full domain independently checks infeasibility as well as admitted saturation. No empty exact-endpoint class is reported as repair success.

**M4: clone guards and declared method failures.** Include exactly the symbolic root tuples and prescribed old/new operations from HYPEREDGE_CLONE_BOUNDARY.md and CONTRACTION_CLONE_GUARD.md, plus the latter's disjoint satellite extension for g in {0,1,2}. Also include the explicit empty-contraction fixture on palette {0,...,5}: roots {0,1},{0,2},{1,3},{4,5}, all floors 2, exact q=3, clone 0<-1 replacing {0,2} by {0,3}. Its retained {0,1} contracts to an empty edge. Their identities contain the source document hash and the complete literal root lists transcribed during implementation and independently checked against the documents. Verify sorted slot matching, f, contracted lambda (empty edge means infinity), completed tau, unsafe repeated-clone values, and safe exact endpoints. Generate all cyclic shifts of root indices of each tuple only when they preserve the floor vector; other root permutations and label permutations are not an additional universe here.

**M5: module and cyclic star relocations.** Modules: h in {3,4}, m in {1,2,3}, ordered sizes s_j in {h,h+1,h+2} with sum at most 10 and q=sum_j(s_j-h+1)>=3; tuples failing this prospective filter are outside M5, not successful module-theorem cases. Cycles: every ordered positive triple (a,b,c) with total k in {6,7,8,9}. For both families use r=core_count+d with d in {0,1,2}; extras are either all P or all duplicates of the lexicographically first core root, suppressing the identical duplicate identity when d=0. Validate every available directed/balancing relocation and deterministic full canonicalization. Modules choose the lexicographically first ordered pair of module indices with size drop at least two. Cycles first choose the lowest-index directed source with drop at least two; if none exists and the sizes are unbalanced, choose the unique maximum part in the exceptional case; stop when balanced. Choose the least source label, assign sorted desired star supports (h-subsets for modules, triples for cycles) to increasing editable root indices, and put P in excess slots. Canonical module sizes are sorted nondecreasingly, with original part indices breaking ties. Canonical cyclic sizes are the lexicographically least rotation of the balanced ordered size triple. Canonical labels follow sorted labels within each part and consecutive canonical intervals; use the first cyclic rotation matching that canonical balanced size order. Canonical root order is lexicographic support order, with original indices breaking duplicate ties. Require ordinary and exceptional cyclic balancing, exact slot counts and retained common labels. Require strict potential decrease on scheduled balancing relocations only; normalization and final permutations have no strict-decrease requirement; local directed relocations outside that schedule require only the proved slot nonincrease and band. Include the explicit (3,5) versus (4,4) module pair at r=11 and the (3,2,2) cyclic obstruction example. Method failure must not be recoded as native disconnection.

**M6: two-guard transfer and slot boundary.** For h in {2,3}, q in {3,4}, put N=C(h+q-2,h), let C be the first h+q-2 labels and E the following h labels. An endpoint consists of all h-subsets of C, followed by E and P fillers. Use r in {2N-1,2N}, k=2h+q-2. Pair the untransformed base endpoint against each transformed endpoint indexed by (shift,reversal), with shift in {0,...,r-1} and reversal in {0,1}. Apply palette reversal x->k-1-x when reversal=1, then send old root i to index (i+shift) mod r. The transformation index is part of the identity, so retain coincident endpoint tuples as distinct prescribed operation identities. Do not form all ordered pairs of transformed endpoints. Explicitly select the complete C core as the t-guard, to exercise its maximal classical size N. At r=2N, retain the base complete-core guard on its original indices and place the transformed target core in the lexicographically first N-index set outside it, ordered by target support then original index; place remaining target supports by original index in the remaining slots. Produce the corresponding exact-q endpoint permutation and verify AB/AC plus layer removal. At r=2N-1, require the disjoint-embedding routine to reject when the prescribed two N-slot guards cannot coexist; do not claim the endpoints disconnected or prohibit a different smaller guard.

**M7: palette splitting.** For q in {3,4}, r in {q,q+1,q+2}, floor vectors in {1,2,3}^r with S=sum floors<=10, and every partition of root indices into q nonempty groups, assign one common label to each group and then a distinct private label for every remaining incidence. Order groups by their least index and private labels by row then position. These tuples are exact-q. Use k in {S-1,S,S+1} whenever all input labels fit. For k>=S validate every permitted first split as a separate local identity; for the full splitting path repeatedly choose the lexicographically first (shared_label,root_index,unused_label) triple, then map sorted labels within each root to consecutive canonical intervals in root-index order. Use increasing-label transpositions to realize that permutation. Pair each input exact-q tuple A with B obtained by palette reversal x->k-1-x, retaining this prescribed pair even when A=B. Construct both A-to-canonical and B-to-canonical routes, concatenate the first with the reverse of the second, and only then apply layer removal between the two exact-q endpoints. Do not apply Theorem A to the single A-to-canonical route when r>q. For k<S require AE's sufficient-condition API to refuse without a barrier claim. Record actual active labels at every step.

**M8: finite-support simulation.** Use two fixed compact endpoints-as-loops: three distinct singleton roots (S=3,q=3), and roots {0,1},{1,2},{0,2},{3,4} (S=8,q=3). For each initially active label and chain length L in {1,S+2,S+3}, repeatedly globally rename that role to successive labels |U|,|U|+1,...,|U|+L-1 by adding the new role to every old-role root in increasing root-index order before deleting the old role in increasing root-index order, then reverse the path to the initial tuple. Set k=|U|+(S+1)+L, where U is the initial support union. At each original vertex select the lexicographically first floor-sized subset in each root, retaining the prescribed compact endpoints. Project by increasing root index and sorted surplus-to-deficit matching, then remap new active labels to the least unused member of the first S+1 labels outside U. Release a reserve assignment immediately after its last occurrence disappears. Verify the exact endpoint identity, injectivity, label release/reuse, hitting numbers and final band. This tests the prescribed finite family of paths, not every possible path.

**M9: inherited native lifting.** Run the COMPLETE inherited v16.53 foundational stack, not a selected subset. For new integration witnesses, use the M6 base-to-transformed pair with (shift,reversal)=(1,1) for each (h,q) at r=2N, and lift that identity's final AB/AC parent path after maximum-layer removal. Attach the initial child stars to the base endpoint; the final nested state is the one reached by clearance, not a separately imposed child-leaf target. Attach to every child a single h-leaf star with distinct labels chosen as the lexicographically first h-subset of that child's support, child target h, and root support equal to that support. Lift the produced parent path using the inherited fixed-root clearance. Check nesting, nonemptiness, one-nonroot-incidence primitives, every internal hitting coordinate and the GLOBAL sum of deviations<=1. These witnesses exercise clearance under parent excursion; they are not a deep-tree campaign.

## 4. Outcomes, resources and rejection controls

PASS means exact identity equality, every expected path/guard/refusal independently valid, every required mechanism diagnostic witnessed, all rejection controls rejected, inherited stack green, deterministic reproduction equal, publication bytes verified and actual-merge replay successful. FAIL retains the first invalid identity, its full path and independent reason. INCOMPLETE is mandatory on resource exhaustion, missing mechanism category, inaccessible inherited evidence or an unfinished domain. No fallback sampling, silent caps or automatic narrowing.

Each GitHub science or independent reproduction job has 60 minutes and a 4 GiB process memory limit. A single identity may use at most 1,000,000 primitive path vertices; exceeding it makes the campaign INCOMPLETE and retains the offending input. Use no more than eight concurrently running domain shards. Each shard contains complete protocol families or lexicographically contiguous identity intervals recorded before path processing. Changing limits or domains requires a prospective amendment before any affected rerun, with prior failures preserved.

Required rejecting controls: missing identity; duplicated identity; valid-looking substituted identity of equal count; wrong tau; wrong floor; an added external label; simultaneous two-incidence move; false packet source membership; empty contracted edge treated as finite; illegal below-floor buffer; invalid provenance SHA; corrupted scientific byte/digest; fake coverage category; a valid parent path whose lifted child incurs a second unit. Genuine RED test logs must precede the corresponding fixes. Controls test the verifier itself and cannot be converted into exclusions from the primary domain.

## 5. File and interface plan

All new scientific files go under ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/; earlier proof files remain immutable. No inherited scientific file is modified.

- protocol.json: approved finite domains, resource rules, proof hashes and preregistration binding.
- model.py: producer-only bit-mask State/Case/Path types and deterministic incidence primitives.
- mechanisms.py: proof-derived path construction; no verifier imports.
- universe.py: producer identities and deterministic ordering.
- verifier.py: independent frozenset representation, direct hitting-set search on active labels, primitive/nesting checks, and independently written universe reconstruction; imports neither producer model, universe nor mechanisms.
- run.py: CLI stages red, preflight, primary, verify, reproduce, package and audit.
- publish.py: artifact download/digest verification, deterministic comparison, durable manifests and post-merge receipt.
- tests/test_controls.py, tests/test_mechanisms.py, tests/test_universe.py, tests/test_lifting.py: named contract tests; executed on GitHub only.
- .github/workflows/v16.54-mechanism-validation.yml and v16.54-red.yml: pinned workflows; workflow_dispatch with required immutable scientific SHA, with separate post-merge audit dispatch.

Public interfaces: generate_cases(protocol: dict) -> iterator[dict]; produce(case: dict) -> dict; reconstruct_cases(protocol: dict) -> iterator[dict]; verify_record(case: dict, record: dict) -> list[str]; verify_universe(expected: iterator[dict], records: iterator[dict]) -> list[str]. Empty error lists mean validation success only after full iteration. A record contains its exact identity, original endpoints, preliminary path if used, final primitive path, typed intermediate guards, proof mechanism and source/protocol hashes. Refusal is a typed result with the violated sufficient condition and no barrier conclusion.

## 6. Review focus

1. Two maximum-layer packets share labels or have different original memberships: test_original_packet_membership.
2. Root-slot or palette reserve exactly exhausted: test_slot_boundary_refusal and test_palette_boundary_refusal.
3. Cyclic balancing lacks an immediate directed drop of two: test_cyclic_exceptional_move.
4. Parent excursion coincides with a child change: test_global_budget_rejects_second_unit.
5. Identical totals conceal missing/substituted objects: test_equal_count_substitution_rejected.

## 7. Implementation tasks after approval

### Task 1: Freeze protocol and independently reconstruct identities

Files: protocol.json, universe.py, verifier.py, tests/test_universe.py, tests/test_controls.py, v16.54-red.yml. Interfaces: generate_cases, reconstruct_cases and verify_universe as above.

- [ ] Commit the approved immutable protocol and proof ledger before the first numerical invocation; bind exact parent, workflow and scientific SHAs.
- [ ] Write tests for missing, duplicate and equal-count substituted identities, and false source SHA. Assert all produce nonempty error lists and that independent complete identity sets agree.
- [ ] Run the RED workflow on GitHub; preserve logs and artifact digests, including expected missing-implementation failures.
- [ ] Implement both universe builders independently, with explicit finite loops matching M1-M9 and canonical JSON serialization.
- [ ] Run the identity/control tests on GitHub; accept only exact identity/multiplicity agreement and all substantive controls rejected. Commit the result with genuine RED/GREEN receipts.

### Task 2: Local proof mechanisms and independent primitive verifier

Files: model.py, mechanisms.py, verifier.py, tests/test_mechanisms.py. Interfaces: produce and verify_record.

- [ ] Write failing tests for original packet membership, both maximum-layer neighbor cases, empty contraction, cycle buffering, saturation, exceptional cyclic move and slot refusal. Assertions are the exact mathematical inequalities in M1-M6 and one legal incidence per edge.
- [ ] Record the RED GitHub run before implementing each mechanism.
- [ ] Implement M1-M6 production, including maximum-layer iteration until the final maximum is q; implement independent direct hitting, floors and capacity checks.
- [ ] Run the complete M1-M6 domains and controls on GitHub. Every prescribed identity must have a verified result; a mechanism diagnostic with no witness makes the stage INCOMPLETE.
- [ ] Obtain independent source review of the exact commit, fix findings and rerun affected whole domains without deleting failures. Commit verified receipts.

### Task 3: Palette/support transformations and native integration

Files: mechanisms.py, verifier.py, tests/test_lifting.py, tests/test_mechanisms.py. Reuse inherited v16.53 clearance through a recorded read-only binding to its exact scientific files.

- [ ] Write failing tests for reserve reuse, fixed endpoint labels, palette-boundary refusal and second-unit rejection. Assert exact endpoint identity and global deviation<=1 at every primitive.
- [ ] Capture RED evidence on GitHub.
- [ ] Implement M7-M9, independently reconstructing the nested fixtures and verifying every internal coordinate; do not share producer hitting logic.
- [ ] Run all M7-M9 identities, controls and the complete inherited stack on GitHub. Retain failures and mark incomplete if any expected identity or inherited test is missing.
- [ ] Independently review exact source and new integration bindings; fix and rerun before acceptance.

### Task 4: Fresh reproduction and scientific publication

Files: run.py, publish.py, v16.54-mechanism-validation.yml and evidence manifests.

- [ ] Run preflight against the exact certified parent and complete approved source inventory.
- [ ] Run all primary families and the inherited stack at one immutable scientific SHA. Store complete records, manifests, logs, source archive, dependency pins, RED receipts and proof/spec hashes.
- [ ] In a fresh job, reconstruct all identities and independently reproduce all deterministic scientific bytes. Exclude only explicitly separated run-specific provenance from scientific equality; preserve that provenance separately.
- [ ] Download the original artifacts, compare GitHub-reported archive digests and internal file hashes, and commit durable verified evidence. A successful upload alone is insufficient.
- [ ] Review the whole exact branch, including native lifting assumptions, manifest exclusions and every historical failed run. Update claims to bounded implemented mechanisms; retain the universal OPEN field.

### Task 5: Integration and actual-merge closeout

Files: publication/audit receipts, README.md, FINDINGS.md, PROGRESS.md and the existing draft PR102.

- [ ] Verify the published source/evidence head, then mark ready and merge only within the user's approved execution scope and repository requirements.
- [ ] Replay every primary family, verifier, coverage check and complete inherited stack at the actual merge SHA; preserve the workflow/scientific SHA distinction.
- [ ] Verify original downloaded artifact digests and deterministic manifests again; commit a durable actual-merge audit receipt.
- [ ] Only then record CLOSED/CERTIFIED for the precisely bounded implementation claim. The general higher-floor conjecture remains OPEN unless a separately reviewed proof resolves it.

## 8. Self-review and handoff

The plan covers the user's four named mechanisms plus the later guards, star relocations, palette splitting and finite-support reduction. Source identities, primary/diagnostic objectives, competing outcomes, resource rules, independent reconstruction, rejecting controls, inherited stack and full publication/audit chain are explicit. No scientific execution or case-count claim has occurred while writing it.

This is a proposed protocol, not a retrospectively registered campaign. All analytical discoveries already known are disclosed in FINDINGS.md and their immutable proofs. Approval would authorize the implementation/execution scope described here; it would not establish a universal theorem or allow a larger arity campaign. Native execution is recommended, with independent reviews at the stated gates. User review of this plan is still required before execution.
