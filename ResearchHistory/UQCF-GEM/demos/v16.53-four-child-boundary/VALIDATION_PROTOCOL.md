# v16.53 prospective implementation validation protocol

Status: written for plan review; no implementation or numerical execution has started. User approved proceeding with focused implementation validation on 2026-10-01. This document freezes the proposed domains before code and execution; the written execution plan remains subject to its review gate.

## Scientific basis and limits

Use NATIVE_ADMISSIBILITY.md and the independently accepted FOUR_CHILD_INTERFACE.md at 8216591e29f9bdda3065315d5650dbc3e8fd7160, proof SHA256 a42d22c25568475f8e9373c6288646b1b68abdc90ecc657a517a0375990f8872. Do not change the proof, admission category, canonical order, or previous stages to accommodate implementation results. Target is faithful clearance, complementary-cover reconfiguration, and composable normalization. Case totals are accounting, not the scientific conclusion.

## Frozen domains

Labels are 0 through k-1; all tuples are ordered. Producer and verifier enumerate identities separately. A support is serialized as its increasing label list. Profiles list internal targets in preorder. Every listed family is mandatory.

**F — compact feasibility.** Every width tuple in {1,2}^4, every q in {1,2,3,4}, and every k in {1,2,3,4}. Identity (F,widths,q,k). Preserve infeasible results explicitly. Producer uses the 15-region specification; independent verifier enumerates four root-support subsets of the required sizes and computes hitting numbers by label-subset enumeration. For feasible rows it derives the lexicographically selected compact tuple using child-major positional bits with 1 before 0. These bounded rows do not replace the general feasibility proof.

**R — exhaustive native four-leaf boundary.** For k in {1,2,3}, enumerate every ordered tuple of four NONEMPTY subsets of the palette. Set q to its independently computed hitting number. Identity (R,k,A_1,A_2,A_3,A_4); start is that exact native state, endpoint is the specified canonical endpoint for q and k. Do not quotient label permutations or duplicate physical descriptions. At k=4 add precisely the 24 ordered permutations of the four singleton roots, target4, to exercise the disjoint boundary at its minimum palette. No other k=4 four-leaf states are included.

**N — new interface composition.** Let L=(), B=(L,L), T=(L,L,L), Q=(L,L,L,L). Use these shape/profile templates only:
- C=(B,L,L,L), profiles (2,2) and (3,2).
- Z=(T,L,L,L), profile (3,3), for a full-width child and zero complementary capacity at its minimum palette.
- D=(B,B,B,L), profile (3,2,2,2), for the triangle-overlap capacity boundary.
- E=(Q,L), profiles (2,2) and (2,3), for a four-child interface consumed by a binary parent.
- G=(Q,L,L,L), profiles (2,3) and (3,3), for repeated four-child composition.
For each template use proved minimum palette M and M+1; permutations identity, reversal, cyclic; start modes compact and exact-preserving inflated. Inflation scans nonroot vertices in preorder and labels increasingly, adding an available parent incidence iff the entire profile remains exact. Identity (N,shape_name,profile,k,permutation,mode). No filtering on path success. These nested cases test the NEW interface boundary, not further binary/ternary depth as a scientific result.

**M — explicit mechanism records.** Preserve primitive paths and invariant checks for:
- fixed-root clearance: P={0,1,2,3}; four child roots (P,{0},{1},{2}); child0 is B with leaves {0},{1}, target2, outer target3. Clear label0 from proper descendants into label2, then delete0 at the child root. Root-full means current root=P; it does not mean child width=k.
- spare-is-current-bin cover transfer: P={0,1,2}, capacities (2,2,2,0), start cover ({0},{1,2},{},{}), target ({1},{0,2},{},{}). Deterministic first misplaced label0 targets full bin1; occupant1 moves to spare bin0, then label0 moves to bin1. This is a cover-lemma mechanism case, not an exact-parent q3 endpoint claim.
- unsafe target2 transport: ({a},{a},{b},{b}) on {a,b,c,d}; replace second a by c, then fourth b by d, each add-before-delete. Native admission must pass; unit-path acceptance must fail.
- unsafe target3 transport: ({a},{a},{b},{c}) on {a,b,c}; replace b by a, then c by a, add-before-delete. Native admission must pass; unit-path acceptance must fail.
Identity is (M,name), with names clearance_root_full, spare_current_bin, unsafe_q2, unsafe_q3. Rejected unit paths are expected control outcomes, never successful scientific normalization records.

## Verification and genuine RED

Certificate schema is version1 with kind campaign or canonical_admission_control and an ordered records list. Every record has its JSON-array identity and status. F records contain feasible and, when feasible, canonical_roots as four increasing label lists. R/N records contain tree, q, k, start, end and path in the inherited label-to-vertex-bitset representation; the verifier converts them to support sets and independently reconstructs all expected metadata and endpoints. M clearance/unsafe records use the same state/path representation, with expected_outcome exact_interior_clearance or native_but_not_unit; the cover record contains start_cover, target_cover, capacities and the full cover path, represented as four increasing label lists per cover. An interrupted normalization instead records phase, exception_type, category (construction or incomplete), and partial_path. No success is inferred from a missing path or missing record. Compress canonical sorted-key JSON with gzip mtime0.

The verifier imports no producer implementation, width solver, canonical builder, or case enumerator. It checks nonemptiness, nesting, global-root constancy, exactly one incidence per primitive, every internal hitting number, total excursion, reconstructed start, exact endpoint, and identity equality. Infeasible F rows are successful feasibility observations; construction failure on an admitted normalization is INTERFACE_NOT_PRESERVED. Resource, evidence, or coverage failures are INCOMPLETE. Neither implies a nonunit barrier.

Before producer implementation, preserve two intended assertion failures with zero errors on GitHub: FOUR_CHILD_IMPLEMENTATION_MISSING and OMITTED_BOUNDARY_CONTROL_ACCEPTED. For the second, first verify a separately tagged exact canonical control with Q, k=3, q=3 and roots ({0},{0},{1},{2}), start=end. Its control manifest contains exactly that identity. The real verifier must accept it and reject its omission. A deliberately supplied-only coverage mutant must accept the omitted corpus, causing the omission-rejection assertion to fail. Only the coverage equality is mutated; do not alter native admission, expected starts or path checks. The control tag is excluded from scientific families F/R/N/M.

Then add failing mechanism tests before clearance/cover routines exist, preserving their expected missing-feature failures without import or syntax errors. Freeze exact test identities, expected outcomes, and AST assertion hashes before definitive validation. Retain all failures and any prospective correction; never rewrite this protocol after seeing outcomes without a disclosed amendment.

## Execution and certification

All numerical science/tests run on GitHub only: Python3.11, sympy1.13.3, mpmath1.3.0, ubuntu24.04, inherited pinned action SHAs, 45-minute execution cap. No numerical local baseline or exploratory enumeration. A timeout yields INCOMPLETE without pruning cases.

Preserve all 1,150 inherited checks and freshly reproduce all 42 v16.52 scientific files. New deterministic scientific files are CERTIFICATE.json.gz, SUMMARY.json, VERIFY.json; certificates retain all F/R/N/M rows, attempted paths and precise failure categories. Total scientific files: 45. Source snapshots include this protocol, the plan, proof/review, exact test manifests, and all required inherited source. Primary and independent fresh reproduction must agree on all 45 scientific files.

Full certification additionally requires independent source review, durable original archives and complete manifest-bound evidence, exact published-head review/merge into parent b6bf95798ec5892963c29f4020f8b75069fd2e3b, actual-merge full replay, and an independently accepted durable receipt. If that parent changes, reassess provenance rather than silently rebasing. Keep analytical acceptance separate from implementation/full-stage status throughout.
