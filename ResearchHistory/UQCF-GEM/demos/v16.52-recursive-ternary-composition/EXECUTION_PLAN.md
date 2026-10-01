# Recursive binary-ternary interface implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. All numerical execution and tests run on GitHub; local work is source authoring/inspection and byte/log/archive audit only.

**Goal:** Certify that the same repair interface survives repeated binary and ternary composition, or report the precise failed obligation without claiming a nonunit barrier.

**Architecture:** Generalize the existing v16.51 constructor by recursive child-interface calls, retaining its proof-specific phase boundaries. Independently reconstruct the case universe and verify support sets, hitting numbers, minimal palettes and total excursion. Reuse inherited publication machinery with updated explicit manifests and no changes to old stages.

**Tech stack:** Python3.11, sympy1.13.3, mpmath1.3.0; GitHub Actions ubuntu24.04; pinned inherited action SHAs.

**Spec:** PREREGISTRATION.md at 693d0a77a83dbc2f162ad3bf655b386dc92a764e; INTERFACE_LEMMA.md is the candidate mathematical contract.

## Global constraints

- Parent76f373c8940433efc463762e675daf3e231f8cb5; isolated research/v16.52-recursive-ternary-composition branch, API-backed source mirror.
- Scope finite ordered trees of internal arity2 or3; no arity4 or physical claim.
- Frozen7236 identities; preserve1071 inherited checks and39 inherited scientific files.
- Genuine verifier-level preimplementation RED; preserve failed evidence. No post hoc amendment hiding missed timing.
- 45-minute execution job cap. No pruning the frozen domain on failure.
- Independent B1/Binf/Bs; failed construction is not a nonunit certificate.

## Review focus

1. Width-k child with nonsorted retained anchor: its initial normalization must use induced palette order and its roles must never be transported.
2. Nested ternary defect: primitive checks must sum deviations across ALL internal vertices, rejecting two simultaneous units.
3. Mixed arity: binary parents must invoke the same recursive interface for ternary children, not a binary-only implementation.
4. Exact identity coverage: omission, duplication, substitution, altered q or k must fail through verifier.verify, even if record count remains7236.
5. Source/start failure: retain the failed identity, failure phase and partial path; classify scientific construction failure separately from missing evidence.

## Task1: independent verifier and genuine RED

Create coverage.py, verifier.py, test_prospective_red.py, TEST_MANIFEST_RED.json and .github/workflows/v16.52-red.yml under the new stage/workflow paths. Do not create producer.py yet.

Interfaces:
- verifier.topology(tree) -> children,parent,internal in preorder.
- verifier.hitting(list[set[int]]) -> exact minimum by exhaustive label-subset checks.
- verifier.expected_specs() -> the independently reconstructed7236 dictionaries.
- verifier.model(tree,q,k,permutation,mode) -> minimum width,start,canonical endpoint using support sets.
- verifier.path_check(tree,k,q,path,start,end) -> peaks for totalL1,Linf,and nonzero-coordinate count.
- verifier.verify(doc) -> verified result or typed InterfaceNotPreserved / coverage ValueError.
- verifier.root_feasible(width_tuple,target,k) -> feasibility by3 or7 incidence-region counts, independently of recurrence.

- [ ] Implement verifier from protocol with no producer imports. Its model recursively constructs canonical support sets; its admission/path checker independently minimizes every hitting number. Validate minimum width at EVERY internal interface encountered, not only the global root.
- [ ] Use the separately tagged control-corpus design in CONTROL_PROTOCOL.md. A canonical zero-path corpus does not satisfy permutation/inflation starts for all7236 science identities. Do not monkeypatch expected starts, bypass path checks, or call that corpus valid science. Implement the frozen separately tagged canonical-coverage control mode, with the same7236 identities and common coverage gate, whose documented expected start and end are both canonical. The actual verifier.verify entrypoint must fully verify that mode and reject omissions. CONTROL_PROTOCOL.md prospectively records this refinement before RED; retain original registration unchanged. The scientific campaign mode must still reconstruct every permuted/inflated start exactly.
- [ ] Record expected missing-interface failure before producer exists. Record actual-verifier omission failure by injecting supplied-only identity handling into verifier.verify and asserting an omitted record is rejected. First verify the complete tagged control corpus with the actual verifier, then ensure the unmutated verifier rejects the omission and the supplied-only mutant fully accepts it, so the expected RED assertion fails without unrelated exceptions. Exact failure signatures and test identities are committed before execution.
- [ ] Run pinned-dependency RED on GitHub; download artifact and verify exact intended failures with zero errors. If the valid-corpus requirement cannot be satisfied before implementation, stop and correct the protocol prospectively rather than silently substituting a helper test.

## Task2: generic recursive producer and GREEN

Create producer.py, test_gate.py and TEST_MANIFEST_CAMPAIGN.json.

Interfaces mirror v16.51: layout(tree), data(tree,q), canonical(tree,k,q,order=None), initial(tree,k,q,permutation,mode), replace_role(state,nodes,child,x,y,path), normalize(state,tree,k,q,order=None,trace=None), specs(), produce(). No import of verifier from producer.

- [ ] Add failing tests for nested ternary and mixed binary-parent cases, width-k order, local-hole transport, ordered endpoint, attached contraction, palette-order equivariance, invalid state/move/root, stacked defects, all four identity corruptions, retained start exceptions and failure classification.
- [ ] Generalize data to arities0/2/3, canonical recursively, and normalization to call itself on every child. Leaf normalization returns its unchanged fixed root. Use q=1 shared-anchor expansion, q=arity disjoint role assignment, and ternary q=2 retained-pair/local-hole transport exactly as proved.
- [ ] Generalize initial inflation to the frozen preorder exact-preserving incidence scan; keep producer hitting implementation algorithmically separate from verifier enumeration.
- [ ] Generate all7236 specifications without filtering duplicates of physical starts. Preserve every case and partial failed path.
- [ ] Run GREEN on GitHub with pinned dependencies. Inspect exact test identities and expected assertions; commit the immutable campaign test manifest before definitive execution.

## Task3: full campaign and publication

Create run_campaign.py, integrity.py, run.py, snapshot.py, archive.py, publish.py, test_integrity.py and .github/workflows/v16.52-recursive-ternary-composition.yml by adapting v16.51, retaining its original frozen source.

- [ ] run_campaign.run(out) freshly invokes v16.51/run_campaign.py into parent51 and compares all39 inherited scientific files before new production; writes complete compressed attempts before independent validation.
- [ ] Freeze all1071 inherited test identities/assertion hashes and exact new tests. Include new protocol, proof, reviews, manifests and workflows in source bindings; exclude publication-generated evidence to avoid circularity.
- [ ] Independently review analytical lemma, source, failure handling, complete inherited manifests and workflow before definitive science.
- [ ] Execute preflight, primary science and separate fresh reproduction; archive source objects, raw certificates, exact logs, metadata, checksums and outcomes. Compare all42 deterministic scientific files (39 inherited plus new certificate/summary/verification).
- [ ] Publish complete evidence and both original execution archives with content manifests; audit every published blob and byte-bound scientific source. Never mark ready if proof, RED, full coverage or reproduction is missing.

## Task4: exact-head merge and independent receipt

- [ ] Review exact published PR100 head and update its description with scoped result and every deviation.
- [ ] Mark ready and merge only that head into the verified integrated branch. Check ordered parents and publication-tree equality.
- [ ] Run actual-merge full stack and campaign, compare all42 scientific bytes, audit downloaded artifact digests and durable receipt manifest.
- [ ] Obtain independent assistant receipt decision and publish it on the separate audit branch; read back exact bytes and terminal workflow status.
- [ ] Only then mark CLOSED/CERTIFIED. A failed or incomplete gate remains explicitly unresolved with evidence retained.

## Design review status

Mathematical interface review is separate from implementation approval. No implementation or numerical v16.52 execution has occurred. This written plan requires review before implementation under the brainstorming/writing-plans workflow; previous scope approval authorized preparation of this concrete specification.
