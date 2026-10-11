# Independent analytical review — same-union pruning and protected incidence records

Date: 2026-10-11. Reviewer: separate adversarial analytical agent (`/root/pruning_record_review`). Requested source parent: `95d0b2381f6006fb30c5fa7cd76ce80696bb3b2d`.

## Verdict

**ACCEPT** as a scoped conditional mathematical subbridge. No Critical or Important mathematical defect was found. One Minor wording correction is recommended below. Acceptance does not establish a physical pruning law, actual state selection, source initialization, observer access, a passed restored-marker gate, or scientific/publication closure.

This review covers the exact candidate bytes identified below. It is a proof and source review, not a numerical campaign, implementation test, complete historical archive audit, or Gemini review. The reviewer did not edit author files. No scientific test count was created or increased.

## Findings by severity

### Critical

None found within the declared conditional mathematical class.

### Important

None found. The interpretation limits in the candidate are essential to this verdict: deletion-only histories are an explicit additional premise about the considered history class, rather than a derived law of actual evolution. Removing this qualification would materially change the review outcome.

### Minor M1 — initial-state wording

Location: RESULT.md §4, paragraph beginning “The output R is a mathematical projection.” The phrase “the common initial state” is inaccurate for the full state: the two preparations differ at r. Their initial memory support at u is identical, and both full initial preparations have the same h profile. Replace with “either initial preparation” (or equivalent). The intended non-readability conclusion is correct, since both initial preparations and the positive endpoint have profile (2,1). This wording issue does not affect any theorem or witness.

## Independent mathematical assessment

### 1. Indexed-view/support transposition

The map Y_i={v:i in S_v} is bijective between the stated finite nested-support states and P-indexed root-containing prefix-closed covers of T. Root support P makes every view root-containing; nesting gives prefix closure; nonempty vertex supports give the cover property. The converse has the same three properties and both compositions are identities. Keeping indices is essential and the candidate does so, including duplicate and root-only views.

For an internal vertex v, a set of indices covers every immediate child precisely when its corresponding labels hit every child support. Thus local h_v equals tau_v, rather than merely being bounded by it. Relabeling the tree and palette transports literal membership, so the stated equivariance is justified. The argument does not supply an actual physical common-Genesis binding, and the candidate explicitly preserves that limitation.

Deletion of (v,i) at nonroot v preserves child nesting exactly when no immediate child still contains i. Prefix closure makes that equivalent to v being a leaf of the current indexed view Y_i. Nonemptiness at v is exactly coverage of v by a different indexed view after removal. Ancestor containment is automatically preserved by shrinking S_v. These are exactly the same-union atomic pruning conditions. No illicit extra move or inferred physical transition selector appears.

### 2. Directed endpoint criterion and total absolute-profile band

For exact preparation S with h(S)=q, E is reachable by admitted deletions if and only if E is a native state, E<=S, and D_q(E)<=B. Necessity is immediate. For sufficiency, at any intermediate F>=E choose a deepest incidence of F\E. No current descendant can retain that incidence: if it belongs to E, prefix closure would require the chosen ancestor incidence in E; otherwise it contradicts deepest choice. Deletion therefore preserves nesting. Some E label remains at the affected vertex, ensuring nonemptiness.

Coordinatewise monotonicity follows directly because a hitting set for smaller child supports also hits the larger ones. Hence q_v<=h_v(F)<=h_v(E) for every internal v throughout factorization. Since all deviations are nonnegative, D_q(F)=sum_v(h_v(F)-q_v)<=D_q(E), establishing the total absolute-profile bound at every primitive. The argument would not justify the same formula for a general inexact preparation relative to an unrelated q; the candidate correctly assumes exact preparation throughout its uses.

Every deletion path to E removes each incidence of S\E exactly once, giving the stated edit count. Exact endpoints force all intermediate local values to remain exact. The proof works for arbitrary finite arity, including unary vertices and the degenerate root-only tree where appropriate. This scope comes from general finite incidence/factorization arguments in v16.24–v16.26. It does not extrapolate the reversible arity-2/3/4 normalization interface of v16.53.

### 3. Pruning-cone criterion and optimal deletion cost

Absence of a at nonroot v forces absence at every descendant by nesting. Therefore every deletion endpoint exhibiting that absence is bounded above by C, the state formed by removing a throughout Desc(v). An initial descendant singleton {a} obstructs every such endpoint by nonemptiness. If none exists, C is a native nonempty state, and it is the largest deletion endpoint satisfying the absence.

With exact preparation, monotonicity yields q<=h(C)<=h(E) for any such E, so D_q(C)<=D_q(E). This proves both necessity and sufficiency of the band test on C. No cancellation in the absolute-value sum is silently assumed.

All initially present a incidences in Desc(v) must be removed before or at the first absence at v. Removing them descendant-first with (v,a) last achieves C with exactly that number of actual edits. The proposed m(v,a) is consequently optimal in the declared deletion-only class, with no claim about reversible-graph distance or physical time.

For two common-profile exact preparations, the positive test is nonvacuous and universally sound for original one exactly when the cone criterion succeeds for source one and fails for source zero. This refers to the fixed readout “a absent at v,” not arbitrary readout sufficiency. Persistence under future deletions follows directly from the absence being irreversible within the restricted class. Reachability does not force actual success, a distinction retained by the candidate.

### 4. Five-vertex witness and reversible counterhistory

Both preparations are valid and have h_o=2 because u and C are disjoint, and h_u=1 because r intersects w. For source one, deleting a(w) produces r=w={b} while u={a,b}; deleting a(u) then produces u=r=w={b}. All three states have profile (2,1). Both required deletions are forced by nesting before a can be absent at u, establishing the claimed two-edit minimum.

For source zero, r={a} cannot lose its only incidence under deletion. Nesting then permanently pins a in u. This proves impossibility under every allowed deletion history and every budget, not just against the displayed successful ordering. The unsuccessful source-one first move -b(w) leaves w={a}, h_u=2, and D_q=1; that singleton pins a in u thereafter. Thus even within B=1, source one has both success-capable and permanently unsuccessful branches, as claimed.

The four-toggle forgery from source zero is legal throughout: +b(r) makes r={a,b}; -a(r) makes r={b}; -a(w) makes w={b}; -a(u) makes u={b}. Each child remains contained in its parent, each support remains nonempty, and every state has profile (2,1). The terminal full state is the same as the positive source-one endpoint. This explicitly demonstrates that protection depends on banning additions; it is not native protection within the reversible grammar.

### 5. Necessary retained source-one-exclusive incidence

For common exact q and budget B, any native band endpoint E<=S_1 that also satisfies E<=S_0 is reachable from both by the endpoint criterion. Consequently every endpoint reached from S_1 with a universally sound positive readout must violate E<=S_0 and so retain at least one incidence present in S_1 but absent in S_0 at the same coordinate. Deletions cannot manufacture a new incidence or move an old coordinate. The proof applies to arbitrary endpoint readouts, including projections, because identical full endpoints give identical readouts.

The quantification here is over reachable positive endpoints, as introduced in the paragraph; unreachable states on which a total readout happens to equal one have no historical implication. The necessary condition does not claim sufficiency for a particular projection. In the witness the retained incidence is (r,b), so the example preserves rather than erases the original distinction. The result concerns erasure of source-one-exclusive incidences in the full state, not disappearance of all source differences relative to every possible observational algebra.

## Source and interpretation assessment

v16.24 C1–C7 and H6 support indexed covers and local child-cover identification. v16.25 R5 and P1 explicitly type same-union refinement as a declared admissible comparison and prove coordinatewise monotonicity. v16.26 P5 supplies the atomic factorization. v16.53 NATIVE_ADMISSIBILITY supplies the support carrier and reversible primitives while limiting its normalization research scope; the candidate does not borrow an arbitrary-arity normalization theorem from it.

The v16.32 collision demonstrates that profile/value-level data do not in general reconstruct indexed incidence. The candidate's own equal-profile witness already shows that h alone cannot read R. It correctly distinguishes mathematical projection from accessible output and does not promote its full-state argument to an observer or guard.

The native-control boundary excludes irreversible/pruning-only restrictions from its reversible connectivity corollary. The current note investigates one such explicitly restricted class without contradicting that corollary. Its added mathematical content is the exact directed reachable-set/cone classification, deletion cost, protection against every history in that class, and retained-source distinction necessity. These are more precise than another scripted conditional write, though they are direct consequences of inherited finite refinement structure rather than a new fundamental interaction. The classification and obstruction are legitimate scoped analytical content.

The physical-frontier and target-blind gate still require a justified action-to-record coupling, physical carrier/reference binding, and retained accessible output. The candidate explicitly leaves those open, declares a separately typed consumer, and does not claim the swapped-root gate passed. Accepting this note does not itself constitute physical progress past those missing connections. Its next research obligation must remain derivation of actual pruning applicability and output access; repeated conditional examples alone would not earn them.

The source AGENTS.md governs numbered stages and their scientific execution/closure. This packet discloses a pre-review analytical probe with no execution, retrospective preregistration, new test count, or CLOSED/CERTIFIED status. The scope is consistent with that distinction. No inherited stage was independently recertified by this review.

## Input identity and local verification

The following hashes identify the reviewed files. All ten source files were read in full. The reviewer recomputed SHA-256, byte length, and the Git blob identity SHA-1("blob " + decimal_length + NUL + bytes) for each and matched all three against source_readbacks.json. The bindings and readbacks agree on path, commit, blob, and URL. This establishes local byte identity against the supplied manifest; the reviewer did not independently query the remote Git tree to establish parent membership. That publication/provenance obligation remains with the parent workflow.

### Candidate and manifest hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| RESULT.md | 14709 | `6a6527f85650d3279fa704020d6aed36f5af13abe64b97c77baa5f58099186c9` |
| PLAN.md | 1548 | `68648da75b938aea33dc41492d71449e54158bd7d86fba5435c38c89ad37e525` |
| source_readbacks.json | 6211 | `ff9646714a0aad7e94e4c10f6e02fbc4b62279f87294a30a953d18560f58f7ce` |
| source_bindings.json | 5200 | `7517d4e0e2396c5c51709ecc14504e259d8ca25dc62c7f67427b6bd3b4503583` |

### Source bytes

All paths below are relative to this review directory. All local checks matched.

- `sources/ResearchHistory__UQCF-GEM__demos__v16.24-consistency-order__TYPE_AND_PROOF.md`
  - Bytes: 8819
  - SHA-256: `795c190c7ea7ffe0133517c3af9213a5d9f13cc026bff4fdecc9e7d0c48a2d29`
  - Git blob: `8c25e9501994bdc337e5cbbc8a4fc50a373d5140`
- `sources/ResearchHistory__UQCF-GEM__demos__v16.25-pruning-refinement-closure__TYPE_AND_PROOF.md`
  - Bytes: 3592
  - SHA-256: `6b52f4694d38d90aac75d807b79416dd708846085f22c8719246e8f158c7f2c2`
  - Git blob: `9dce6e323a1a7c27e057379f8c2032978b701fd5`
- `sources/ResearchHistory__UQCF-GEM__demos__v16.26-consistency-increment-law__TYPE_AND_PROOF.md`
  - Bytes: 1666
  - SHA-256: `6f8cb07548b763cdea4d4d95f4df2a79891b2aa92e75ba279566adbb0cc23bb4`
  - Git blob: `69ace252586ad0b323ca3c460304ead8da8fd917`
- `sources/ResearchHistory__UQCF-GEM__demos__v16.32-retained-state-reconstruction__PROOFS.md`
  - Bytes: 3610
  - SHA-256: `9a6be2b7a5939b2f2b1261f80fdaaa6ba0f0f8f2da82849759fe690e30fdcd74`
  - Git blob: `e1023f728c97b941c9201f3c32785fcf09c4602d`
- `sources/ResearchHistory__UQCF-GEM__demos__v16.53-four-child-boundary__NATIVE_ADMISSIBILITY.md`
  - Bytes: 3615
  - SHA-256: `a08edf466b041d00932e197dac01d6845bfd202ac317e6debf4695db770e9e23`
  - Git blob: `ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2`
- `sources/ResearchHistory__UQCF-GEM__research__physical-bridge__COUPLED_C3_NATIVE_CONTROL_BOUNDARY.md`
  - Bytes: 9116
  - SHA-256: `19d202ad5a57a7960ccf6b143336b366fe57e987be6b9f2c5fd03b39b1ac2188`
  - Git blob: `84204cef0faf2ebd5e6a7d41e960d34b649fbb2c`
- `sources/ResearchHistory__UQCF-GEM__research__physical-bridge__COUPLED_C3_PHYSICAL_FRONTIER_DECISION.md`
  - Bytes: 5170
  - SHA-256: `3362d45ae65a16e9326b0651cc19e46611f5c920fb1b1aa2f520558825b0cc60`
  - Git blob: `878e6c4b590a0dd64244d36755d70b080e08928d`
- `sources/ResearchHistory__UQCF-GEM__research__physical-bridge__COUPLED_C3_TARGET_BLIND_RESPONSE_GATE.md`
  - Bytes: 10784
  - SHA-256: `0c3771c923283001cd13b44e1ace0ae18e2d19f52efcef07dce0bc4cbb5ef594`
  - Git blob: `478aecf3df5b4214209cdfd0e615d78c552a3bd0`
- `sources/ResearchHistory__UQCF-GEM__research__physical-bridge__COUPLED_C3_RECORD_CONVERSION_RESULT.md`
  - Bytes: 8899
  - SHA-256: `a84f4622cbec898e2a08e7c3b538d0e7b2a656d24b4a54d60d508fa7d2c48eb2`
  - Git blob: `b6a03d8887fd4f55e8cd6c17684a9d76a14509a1`
- `sources/ResearchHistory__UQCF-GEM__AGENTS.md`
  - Bytes: 2368
  - SHA-256: `56d5ffb2d1f8f0d1a1660b6cc5b31ebae92b59fb48b547e7d47ea13f0bafdee0`
  - Git blob: `e5407215a81b914fc02f5c107333a2f0261634ee`

## Disposition

ACCEPT the stated conditional pruning-record classification and source-retention limit. Reconcile Minor M1 before publication if convenient. Preserve this raw review unchanged and record any author correction separately. Physical realization/access and broad C3/C4–C6 remain OPEN; no numerical or closure conclusion is implied.

## Reviewer addendum — author correction checked

While the raw review was being written, the author corrected Minor M1 and preserved the original candidate verbatim as REVIEWED_DRAFT.md. The initial complete proof/source review was of the original 14,626-byte draft with SHA-256 `d873d71d17444f88055bd0e0bee198f4d4980f19662258df09add44559805f3d`; this is the independently checked hash of REVIEWED_DRAFT.md. The candidate hash table above was captured after that author correction and therefore records the revised RESULT.md (14,709 bytes, SHA-256 `6a6527f85650d3279fa704020d6aed36f5af13abe64b97c77baa5f58099186c9`).

I inspected the complete diff between the original and revised candidates. Its only change replaces “the common initial state” with “both initial preparations” and adds “The initial memory at u is common; the complete initial preparations differ at r.” This fully resolves Minor M1 without altering the mathematics or scope. The original finding above is retained as review history. The final verdict remains **ACCEPT**, now with no unresolved findings. No author file was modified by the reviewer.
