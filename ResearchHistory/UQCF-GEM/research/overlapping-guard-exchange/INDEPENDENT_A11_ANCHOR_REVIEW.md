# Independent exact-source review: A11.X2

Verdict: ACCEPT the bounded analytical extension in the frozen candidate, conditional only on the explicitly inherited, accepted maximum-layer-removal theorem. No blocking mathematical gap found. This receipt does not independently recertify that inherited theorem and does not certify numerical work or implementation.

Signed: Codex independent reviewer `/root/a11_anchor_review`, 2026-10-03 (UTC). Review conducted from independently fetched immutable GitHub content, not an author's supplied local copy.

## Exact source identity and parent inspection

Repository: `proteinfoldingengine/WetLabEngine`.

- Candidate: `1cd572d2e90ba3880dc5598d260c14e8a92acc5c`.
- Proof: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_RENEWABLE_SINGLETON_ANCHORS.md`, Git blob `f4c295a21a545be746def65acb4fe38c781e3f14`, independently computed SHA256 `04000ea60376ae6778137ce87725ec1e50424c365a7deb976c18d926e8b379de`. Matches expected hash exactly.
- Scope: same subtree, `A11_RENEWABLE_ANCHOR_SCOPE.md`, Git blob `3da2afa1e953b12bd6b932916f26b1bb50268650`, SHA256 `7d5406fb5efd072d27e290b222740739505f7fa0d5ab496de9bd2a14ea1005c1`.
- Scope parent: `325bb35370a69b750215ef58578fdbff4bc361a0`. Independent comparison reports one commit ahead and only the proof added (114 lines), with no deletions. Scope fetched separately at the parent has the identical blob and bytes.
- Prior publication: `ff009ef63b0566de559eba4d07e5fd63e08d14c1`. Comparison to scope parent reports one commit ahead and only the scope file added (13 lines), with no deletions.
- Accepted comparison source: `ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/SINGLETON_ANCHOR_REDUCTION.md` at `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`, blob `bac4252c79de6efca40134bf5928fb02506c6cb7`, SHA256 `93eda3cc5c6f7904c5d88e6d99576d70892e638cda04e2414ad9bb2ea4fb932c`.

All three hashes were calculated over base64-decoded GitHub file bytes using SHA256. Hashing was source-identity verification, not a scientific numerical campaign.

## Mathematical findings

1. Set m=q-2. Feasibility gives k>=q=m+2 and r>=q. Selecting the same m ORIGINAL floor-one slots at both endpoints is legitimate and leaves at least two real nonanchor slots. Nonanchor floors remain arbitrary positive integers; no floor is silently lowered.

2. Individual contractions to singleton anchors preserve floors and cannot decrease tau. Duplicate-label repair is valid: the other singleton {p} forces p, making the union step {p}->{p,t} redundant; the subsequent deletion contracts that changed support and cannot lower tau. Distinctness increases strictly, and an unused label exists until all m selected labels are distinct. Endpoint normalization and its reverse are finite legal paths with tau>=q.

3. With m distinct singleton anchors, the sole possible hitting set of size at most m is U. Thus tau>=m+1 precisely when a nonanchor support is disjoint from U. At normalized endpoints tau>=m+2 implies at least two distinct nonanchor supports miss U: zero missed supports give cover U, and a single missed nonempty support gives a cover of size at most m+1. This proves existence of genuine labelled guard indices, not hypothetical witnesses.

4. Each selected guard's actual source support lies in P minus U, proving its original floor is at most k-m. Expansion to G(U)=P minus U uses individual additions and retains avoidance. Every renewed G(U') has the same cardinality k-m, so both ORIGINAL guard floors fit every future exchange.

5. All six stated toggles are individually legal. Guard cardinalities are k-m or k-m+1; anchor cardinalities are one or two. Before the anchor union, guard i excludes cover U; after the anchor replacement, guard j excludes U'. At the union stage, W of size m-1 is forced, and the only possible covers of size at most m are W union {p} and W union {t}; the two guards exclude these respective alternatives. Hence every primitive respects tau>=q-1. Both guards are renewed to G(U') at the end, so iteration is justified without consuming protection.

6. Ordered-injection scheduling is complete. Greedy free-target changes fix coordinates without disturbing fixed coordinates. Once no wrong coordinate has a free target, the current label set equals the target set and the residual mismatch consists of permutation cycles. An existing unused palette label breaks each cycle; a cycle of length ell uses ell+1 changes and releases its helper. If d direct changes and c cycles occur, the total is at most m+c<=2m. Every replacement label is outside the then-current anchor set. The resulting <=12m bound applies only to this exchange stage, before inherited path conversion; it is not a runtime or total converted-path bound.

7. Destination handover is sound. At least two destination nonanchor supports avoid V, so a destination guard b distinct from retained source guard i exists (possibly b=j). Keep i fixed while repairing b through individual union additions then deletions. Next keep completed C*_b fixed while repairing every other nonanchor slot, including i and j when applicable. During each contraction the current support contains the valid target support and therefore meets its original floor. This reaches the prescribed labelled C* tuple, not merely a permuted family.

8. Finite palette, finite slots, strictly increasing normalization distinctness, finite injection schedule, and finitely many additions/deletions per final root prove termination. Reversing the destination normalization restores every original labelled support exactly. No unproved continuation of an arbitrary safe prefix is used.

9. The newly proved construction yields a finite path with tau>=q-1 and ORIGINAL exact-q endpoints. The candidate invokes accepted GENERAL_PARENT_CONNECTIVITY.md Theorem A only once on this full path. I inspected its stated domain and conclusion at the immutable accepted baseline: width-floor tuples on a fixed palette, individual incidence moves, exact-q endpoints, and lower-path connectivity imply a path with tau in {q-1,q}. The candidate meets these input conditions. I did not independently review or recertify Theorem A's proof. Converted paths need not preserve the anchor invariant.

## Baseline comparison and limits

Accepted Theorem P requires at least q original floor-one slots for arbitrary remaining floors. Candidate X2 improves this sufficient condition to q-2 for q>=4. Accepted Theorem Q separately requires EVERY floor in {1,2}; neither is being rewritten or retrospectively recertified.

The q=4 corollary follows for every feasible exact-four endpoint pair on any fixed carrier with two original floor-one slots and arbitrary remaining positive floors. The stated two-floor-one/thirteen-floor-6006 carrier therefore satisfies the theorem's floor hypothesis. This review does not independently recertify A11.X1's historical carrier construction or safe-prefix counterexample.

Temporary incidences and repeated toggles are allowed. The construction can introduce incidences outside endpoint unions and can temporarily remove destination incidences. It therefore does NOT resolve universal A11 destination-directed scheduling, does NOT establish arbitrary safe-prefix extension, does NOT close the uniform-floor-three diagnostic, and does NOT close unrestricted general q>=4 or nested universality. Child-interface conditions remain necessary for any inherited lifting statement. Sufficiency does not establish minimality of q-2.

Issues: none blocking or requiring source revision within the frozen bounded scope. The explicitly inherited maximum-layer-removal dependency remains an acceptance dependency, not a newly certified result. No enumeration, numerical campaign, implementation, tests, workflow execution, repository mutation, or publication was performed in this review.
