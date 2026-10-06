# A12.1-A12.5 self-contained audit protocol

Date: 2026-10-06 UTC.
Status: PROSPECTIVE VERIFICATION SCOPE; NOT AN EXECUTED TEST OR CLOSEOUT.
Integrated parent: 62b6bec4bea5e6446680aec5694fbd0d8f096165.
Authority: user approval of the self-contained recovery steps, following the process amendment at that parent.
Branch: research/uqcf-overlapping-guard-exchange. Tracking issue: #104.

## 1. Question and success criterion

Determine precisely which of the five existing A12 claims follow from finite labelled incidence states, positive original root floors, and the protected hitting-number band 3 <= tau <= 4. Complete their arguments and refutation record without adding a research stage or requiring an outside AI service.

Publish a consolidated corrected candidate and an author-side whole-argument audit. Preserve the original scope/proof files and historical review unchanged. A correction or narrower conclusion is explicit; a historical external verdict is never rewritten. This protocol's publication is not mathematical acceptance, computational PASS, independent review, or gate closure.

Closure requires the consolidated proof obligations, the bounded checks declared here, their deterministic reproduction, and a separate repository reporting/source/readback audit. A12 stays OPEN until those tasks are actually complete. Universal statements rest on the written arguments, not the number of finite checks.

## 2. Immutable source registry

Paths are relative to this directory. All ten scope/proof files were read from parent 62b6bec4bea5e6446680aec5694fbd0d8f096165. Historical freeze commits remain as follows.

| Result | Scope commit | Proof commit | Scope filename | Proof filename |
| --- | --- | --- | --- | --- |
| A12.1 | 8a9b9747a3e95118af46b5d16c2bffa5938d7d6e | 36220cab3f17f2f8b9b0308a59c5037bfadde108 | A12_1_SIGNED_ADMISSIBILITY_RESPONSE_SCOPE.md | A12_1_SIGNED_ADMISSIBILITY_RESPONSE.md |
| A12.2 | 824cc79ce006985499e0f2ffacab34b8f9e90786 | 72c361344c5eb0459285c791d7ae6440e8661c26 | A12_2_COLLECTIVE_RESPONSE_SCOPE.md | A12_2_COLLECTIVE_RESPONSE_HIERARCHY.md |
| A12.3 corrected candidate | 3ae51147985f885770dee3167eb73bd542f5192e | 05b1300fa877fad66e10c0acd1d6a093c125ccac | A12_3_DUAL_CERTIFICATE_FIELDS_SCOPE.md | A12_3_DUAL_CERTIFICATE_FIELDS.md |
| A12.4 | 5be2e81ff224761a0f9622104354ac804dc15bae | c10c68922fbcbf520d28b1ca509faa38fcf3bcd5 | A12_4_CANDIDATE_RESPONSE_MARGINS_SCOPE.md | A12_4_CANDIDATE_RESPONSE_MARGINS.md |
| A12.5 | fe6cf6207f5d9a007e52a75c088d0595d8c78a9d | 0f3a6790777ebe1ce1f6c2739c2ca99f0c2fa433 | A12_5_OVERLAP_LOCALITY_NOGO_SCOPE.md | A12_5_OVERLAP_LOCALITY_NOGO.md |

Scope/proof blob pairs:
- A12.1: 64685e2fcad2f77f6a590685368a1ac21896e057 / 54cf74c9d01548368b7e32814f2f06e7fba5d628.
- A12.2: 48c7698a38a69685643f040b59a6f040be3ac054 / bfb364b75e18a279f2e4aa53254370f563a9545c.
- A12.3: 0e8ac8ba64fe72e17c207d6532c7c51fd71b300a / b9fa20d44002d0d743278f3fd21cce3214d02600.
- A12.4: 7a7593740c65b87473cbe0bb36432064c278a428 / a0d38aeacac80f036f9cb997f08f921f4e0f4b59.
- A12.5: 001804a390c1ed9603e8bc15abac30cd255b981e / 0da2ddad7ed177219f3fed50e7e152b2e1ffa679.

The amended closeout request and STATUS at the parent remain governance. Older prospective status text in frozen proofs is historical, not a current gate verdict.

## 3. Definitions and proof obligations frozen before further changes

Use finite palette P, labelled supports E_i subset P, positive integer original floors f_i <= |E_i|, and incidence syntax (an added label is absent; a deleted label is present). A floor test is a distinct part of legality, not syntax. Legal states have nonempty supports. For evaluating an illegal deletion diagnostically, define tau=+infinity when a support is empty; the empty family has tau=0. These conventions must be explicit and must not silently enlarge the protected domain.

A12.1: prove hitting-number inclusion monotonicity; all four response signs for a legal first move and a distinct incidence candidate syntactically defined before and after; preserve same-root floor effects; verify four strict-sign controls; prove covariance and invariance of summary counts.

A12.2: check construction size against listed roots (the source says n+2 but lists n+3); prove every prefix/subset and candidate endpoint; state kappa(empty)=1, nonempty proper coefficients zero, full coefficient -1; delimit the growing-root-count quantifier. Do not infer an arbitrary full-response-graph insufficiency theorem merely from this candidate's vanishing lower-order coefficients.

A12.3: give explicit palette/root/floor domain and the small-palette counterexample to the unrestricted pair equivalence; prove W/C identities, affected-coordinate counts, monotonicity and one-update bounds; derive signs with commuting incidence updates rather than assuming candidate shadows stay fixed on a same-root edit; show the collective witness interpretation and covariance. No conservation assertion.

A12.4: prove the addition-shadow and surviving-cover iffs, including empty-shadow infinity; distinguish a fixed candidate identity from its changing shadow; separate local floor thresholds. Check the two original controls and, by relabeling those controls, whether the insufficiency of (mu_-,N4) persists with a fixed candidate identity. Do not assert scalar margin monotonicity merely from coordinatewise W monotonicity.

A12.5: verify the exact matched six-root states, initial and final hitting numbers, equal complete candidate overlap components and stated side information. Include the post-I lower bound from disjoint singleton roots. State the precise restricted input class of the impossibility claim, not a claim about every locality notion.

## 4. Bounded computational scope

No code or scientific execution is included in this protocol commit. The following scope is fixed in advance for the follow-on verifier; changing it requires an explicit prospective amendment before running the changed scope.

### 4.1 Complete primary universe

For p in {2,3,4}, m in {1,2,3}, palette {0,...,p-1}, enumerate EVERY ordered m-tuple of nonempty supports and EVERY floor tuple with 1 <= f_i <= |E_i|. Repeated supports and unequal floors remain distinct labelled states. No random sampling, symmetry quotient, supplied-case-only universe, or post hoc pruning is permitted.

For one root the number of support/floor choices is sum_(nonempty S subset P)|S| = p*2^(p-1). Thus the expected numbers of floored states, calculated before execution, are:
- p=2: 4+16+64 = 84;
- p=3: 12+144+1728 = 1,884;
- p=4: 32+1024+32768 = 33,824;
- total: 35,792.

Check pair and upper-cover equivalences on this universe; check primitive W/C changes and their coordinate counts for every syntactic incidence toggle (including illegal endpoints using the stated diagnostic convention). In protected initial states compare direct legality with certificate-margin legality, and check response signs for every legal first move and every distinct incidence candidate with common syntax. Test covariance under all adjacent-label transpositions and adjacent-root transpositions; these generate the finite permutation groups. Record actual counts by obligation rather than claiming that a state count is a proof count.

The m<=3 universe cannot test a 4-to-5 upper-band exit. The explicit five-root/six-label deletion fixtures below cover that boundary; no larger-universe completeness claim is made.

### 4.2 Independent calculation routes

Reference: calculate tau by enumerating all palette subsets in increasing cardinality and testing actual intersection with each support; calculate legality directly from the post-state and floors. Do not call W, C, A or D to obtain this reference answer.

Certificate route: enumerate physical pairs and H of size <=4, calculate W/C from supports, apply the symbolic update identities, and calculate candidate margins. Compare with fresh post-state fields and direct reference legality.

Universe coverage must be derived independently from the support/floor Cartesian product and checked by exact identity equality, not merely len(supplied_results). Include a rejecting control deleting one otherwise valid identity and another inserting a duplicate.

Both routes may be authored here; this provides separately specified calculations, not independent human/model peer review. Shared low-level representation must be disclosed.

### 4.3 Symbolic-family and edge fixtures

Reproduce all four A12.1 strict-sign examples, both A12.4 examples and their fixed-candidate relabelings, both A12.5 states and endpoints. Verify A12.2 for every n=2,...,8 and every intervention subset, every edge adding one intervention, and all Mobius coefficients. The general-n proof is separate.

Include palette-size 0/1 diagnostics, empty family, an empty support, a protected three-singleton state, a floor-forbidden deletion whose band alone would survive, an empty addition shadow, and a same-root edit changing a finite addition margin to infinity while candidate legality remains unchanged.

### 4.4 Rejecting controls

Before accepting the verifier, it must reject: missing/duplicate universe identities; n+2 metadata for the actual A12.2 family; the unqualified pair-equivalence claim at p=1; a wrong sign in a W update; a wrong changed-coordinate count; floor-free deletion legality; a reversed strict response sign; false conservation of N4 in a fixture where it changes; and a false A12.5 endpoint value. Preserve which bad statement/record each control rejects. Unsupported prose about arbitrary response graphs requires argument audit, not a numerical PASS label.

## 5. Execution and evidence budget

Scientific execution belongs in GitHub Actions only. Use a standalone Python standard-library verifier, Python 3.11, an Ubuntu runner, no network scientific inputs and no imported certified engine code. Freeze implementation and workflow commits before execution. An initial rejecting-test stage must demonstrate the targeted errors are caught before the complete candidate is called passing.

Run the complete bounded verifier twice from the same immutable source in fresh processes and require deterministic scientific-result equality. Allow at most 10 minutes per execution and 25 minutes for the workflow including evidence handling. Target <=2 MiB of text evidence, excluding platform logs. A timeout, resource excess, missing obligation, or partial enumeration is INCOMPLETE, not PASS; do not shrink the universe silently.

Record full scope/implementation identities, Python/environment details, exact commands, actual counts, canonical identity-set digests, rejecting-control outcomes, first failing witness if any, source SHA-256 manifest, run/job/attempt IDs, logs, and reproduction comparison. Hashes supplement the reproducible enumeration algorithm; do not describe hashes as retained full raw per-state output. Preserve original failed/incomplete run references. Publish the small final evidence durably in the repository and read it back by immutable commit.

Inherited dependency boundary: this isolated verifier consumes only the ten frozen A12 documents, this protocol and its new consolidated candidate/code. It neither imports nor changes certified v16.54/v16.55 implementations or evidence. Verify the unchanged-source boundary by Git comparison/blob checks. This scope does not claim a replay or recertification of the entire historical stack; if an inherited executable dependency is introduced, amend the replay requirements prospectively.

## 6. Reporting audit and exit

For each A12 claim record: exact final statement and hypotheses; proof location; source correction/narrowing; symbolic counterexample checks; bounded verification status; interpretation limits; unresolved obligations. Report author-side proof audit, bounded verifier PASS and genuinely separate review as distinct evidence types.

After mathematical and computational obligations are complete, check source identities, original-history preservation, claim wording, citations/live references and immutable publication readback. Only then publish one reconciled closeout and resolve #104. This protocol does not close the gate.

No A12.6; no outside-AI polling/dispatch; no efficiency campaign; no force, geometry, energy, GR/ADM, dark-matter replacement, physical nonlocality, continuum or fundamental-time inference. Certified v16.54/v16.55 and accepted A11 remain unchanged.
