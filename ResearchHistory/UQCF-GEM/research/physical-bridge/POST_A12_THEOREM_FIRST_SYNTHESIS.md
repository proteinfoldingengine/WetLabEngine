# Post-A12 theorem-first synthesis — current continuation index

Updated: 2026-10-07 (America/Phoenix).
Status: C1/C2 AND BOUNDED C3 CLOSED; C3 HIDDEN-SPECTATOR OPTIMALITY CANDIDATE UNDER REVIEW; BROADER C3-C6 OPEN.
Branch: research/uqcf-overlapping-guard-exchange.

The original proposal, its publication history and precise B1/B2 questions remain immutable at commit 963ad536d9f110e7fe51b443e90c1f8afc461096, blob 29f61b20b72665e3972abdae49b5020eb5547c17. This file now points to the approved follow-on work; it does not retroactively change that proposal or the closed A12 sources.

## Completed work and authoritative records

The user approved studying A11.X2's six-move handover, the information it needs, its repeatability, and BOTH protected-band bounds.

- [Selected carrier and frozen retained-input model](https://github.com/proteinfoldingengine/WetLabEngine/blob/906f38894df287944a6742ab2f3685e39976b7dc/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_HANDOVER_SCOPE.md).
- [Complete analytical result and counterexamples](https://github.com/proteinfoldingengine/WetLabEngine/blob/2c6d87e67a29a98e483f921f07a525b302b96ebf/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_HANDOVER_RESULT.md).
- [Whole-argument audit and scoped closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/ef317a97b72a869bd3c6ceb38a1bc8bb65375090/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_HANDOVER_CLOSEOUT.md).

The exact new identity is T0=T1=T2, T3=T0 union T6, T4=T5=T6 for the actual transversal families along the prepared handover. Thus its hitting numbers are (a,a,a,min(a,b),b,b,b). Both prepared endpoints being in 3<=tau<=4 is necessary and sufficient for this entire macro to be band-safe.

A Boolean table F_R derived from the FIXED residual roots, plus declared carrier/anchor/target/phase information, suffices to decide and update this policy without repeated access to individual residual supports. It has at most binomial(k,2) residual bits and is demonstrably non-injective on a fixed carrier; initialization can still require global information. This is not a theorem that global W/C alone determines an arbitrary repair policy.

Complete safe handovers connect exactly the ordered anchor pairs in the same component of the graph derived from F_R. A decreasing integer rank proves termination. If a three-label set hits all residual roots, the graph is connected and any two protected prepared states can be joined in at most six handovers (36 incidence edits). The bound is analytical, not a measured performance claim.

The result also supplies valid exact-four endpoints whose macro graph is disconnected. A different native path joins them, so this refutes universal sufficiency of the prescribed handover policy, not X2 or general native repair.

## Dynamic residual updateability now completed

The next obligation from the fixed-residual closeout has now been resolved for DECLARED residual edits:

- [Frozen dynamic-residual scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/716ff49fe1b1105695945d3ee7e808a927820cfa/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_DYNAMIC_RESIDUAL_SCOPE.md).
- [Exact miss-count update theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/d1aeaeba5ddb6a6748a5a80cb69d5ab76fdf8db7/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_DYNAMIC_RESIDUAL_RESULT.md).
- [Argument audit and scoped closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/46ccf73fafb974d8721bfd6736de7201d4cb95d7/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_DYNAMIC_RESIDUAL_CLOSEOUT.md).

The old Boolean F_R table is provably not update-closed once a residual root changes: the published same-record counterexample gives identical retained F_R and identical declared edits but tau=4 versus tau=5 after the second primitive.

The exact update-closed replacement is the residual miss-count field

    M_R(H)=#{r:S_r intersect H=empty}, 1<=|H|<=4.

For a named residual edit S->S', each coordinate updates locally by subtracting the old root's miss indicator and adding the new one. Pair coordinates M_R(K) are exactly the residual contribution to lower witnesses; zero coordinates M_R(H)=0 identify residual small covers. Combined with explicitly retained controlled supports, the same field reconstructs both target-four band tests and can be updated without rereading any other residual support.

This closes legality/updateability for DECLARED edits. It does not select a hidden residual root, discover its unretained support, or prove arbitrary endpoint completion.

## Binary labelled selection/completion now completed

The first bounded selection/completion theorem is now published:

- [Frozen selection/completion scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/eff1e50769c4e73bd325fe8b1ff06a72ea06d2ee/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_SELECTION_COMPLETION_SCOPE.md).
- [Exact labelled-address theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/1e89814d397763cbfe8157b7cc484a3ba45b5819/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_SELECTION_COMPLETION_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/b5883356c2ec2eadf57fc1f9655998b687bd2129/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_SELECTION_COMPLETION_CLOSEOUT.md).

In the selected binary-singleton residual class, the aggregate M_R field depends only on how many labelled residual roots carry {a} versus {b}, not which roots carry them. Two same-count sources can therefore have identical M_R and the same exact target but require different labelled first edits.

Retaining the labelled mismatch set Q resolves selection. The deterministic controller repairs the least root in Q by {b}->{a,b}->{a}; every primitive remains in 3<=tau<=4, |Q| decreases by one per macro, and the exact labelled target is reached in 2|Q| edits.

For fixed mismatch count m, any deterministic no-read endpoint-directed controller must distinguish all binomial(n,m) labelled mismatch sets; otherwise two hidden states with the same retained record and same aggregate M trajectory eventually require disjoint next roots. Thus the supplemental address record needs at least ceil(log2 binomial(n,m)) fixed-length bits in that policy model.

In this deliberately tiny class Q itself reconstructs the residual incidence state, so M_R is redundant once Q is known. The result establishes the certificate/address distinction but is NOT yet a nontrivial compression theorem.

## Hidden-spectator factorization now completed

A richer exact-completion class now proves genuine retained-state reduction:

- [Frozen hidden-spectator scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/1dde3e9887cc840a42e8bbe6bb750710094ecf81/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_RICHER_FACTORIZATION_SCOPE.md).
- [Exact hidden-spectator completion theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/eee9eba17ec2f272949051dcd7533e4424ab33f3/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_RICHER_FACTORIZATION_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/3c1f302324e8560424d7a7fa3d22da64b84ff409/ResearchHistory/UQCF-GEM/research/physical-bridge/POST_A12_RICHER_FACTORIZATION_CLOSEOUT.md).

Each labelled residual root carries a mutable core a/b plus an arbitrary immutable spectator subset Z_r from s spectator labels. The controller retains only the labelled core mismatch set Q. It repairs b->a in each mismatched root by Add a then Del b, while never reading or toggling Z_r.

The band is structural: c,d are forced by the anchors, the guards force one of a,b, and {a,b,c,d} remains a four-cover because every residual root always contains a or b. Thus every primitive stays in 3<=tau<=4.

For fixed Q there are 2^(ns) different labelled spectator assignments with the same controller transcript; with all residual floors fixed to1, even floor metadata is identical. The exact final supports {a} union Z_r are restored because the hidden spectator incidences are invariant. Q therefore does NOT reconstruct the full residual state.

This is a genuine information-factorization result, but M_R is unnecessary because legality is structurally guaranteed. It does not yet make aggregate certificate information and reduced address information simultaneously active.

## Joint certificate+address factorization now completed

The first class in which both retained channels are simultaneously active is now closed analytically:

- [Frozen joint scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/0fa27e915b77742e21657c91bfd49b4cf0f6a1e5/ResearchHistory/UQCF-GEM/research/physical-bridge/JOINT_RETAINED_SCOPE.md).
- [Corrected joint theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/6454074a95b526bf2125272f76bfad392e2f468f/ResearchHistory/UQCF-GEM/research/physical-bridge/JOINT_RETAINED_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/63f1be4edbf0ee99f9df22012e99285d7a256829/ResearchHistory/UQCF-GEM/research/physical-bridge/JOINT_RETAINED_CLOSEOUT.md).

Two labelled payloads begin with core a and must end at distinct target cores b,c. A third invariant environment root is either {b} or {c}. A core-projected miss-count field identifies the environment target type that must be established first; a labelled target-address record identifies which payload carries that target obligation.

Repairing the matching payload first gives tau sequence (4,4,4,4,4). Repairing the other payload first gives (4,4,5) on its first macro and exits the protected band.

Both retained channels are necessary for the declared deterministic complete-macro policy. Yet for fixed environment and target address, 2^s arbitrary spectator assignments on one payload give identical retained certificate/address data and controller transcript while producing distinct full labelled states and targets. Thus the joint retained state still does not reconstruct the full incidence state.

## Retained-quotient precedence interface now completed

The two-payload precedence has been extracted into a reusable sufficient interface:

- [Frozen precedence-interface scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/28ec21aee2b2bcc3aaee271b75c0ee85bda9d422/ResearchHistory/UQCF-GEM/research/physical-bridge/PRECEDENCE_INTERFACE_SCOPE.md).
- [Retained quotient precedence theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/00a58b1b3d9d6b1c0c190995a18c5d5e5d19cd40/ResearchHistory/UQCF-GEM/research/physical-bridge/PRECEDENCE_INTERFACE_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/e81c236b707d2ed1c5e07ebe806858bac83f1f25/ResearchHistory/UQCF-GEM/research/physical-bridge/PRECEDENCE_INTERFACE_CLOSEOUT.md).

A retained state is treated as a quotient of full incidence states. For each unfinished obligation set, retained data derive a precedence graph. The key hypothesis is fiber-uniformity: every indegree-zero macro must be legal for every hidden full state represented by the retained record and must map all of them to one deterministic next retained record.

Under exact obligation completion and graph renewal by induced-subgraph deletion, any acyclic retained graph yields protected exact completion after exactly one macro per obligation. A directed cycle is an exact deadlock for the indegree-zero-only macro policy because no cycle vertex can become eligible while the cycle persists. This is explicitly not a native-disconnection theorem.

The closed two-payload joint theorem embeds as the one-edge graph P_x -> P_y while retaining 2^s hidden spectator states.

## Concrete three-payload precedence now completed

The retained precedence interface now has a genuine multi-vertex native realization:

- [Final fiber-uniform scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/005857e5b486e07545d91bd89f161a59c0ac972d/ResearchHistory/UQCF-GEM/research/physical-bridge/THREE_PAYLOAD_PRECEDENCE_SCOPE.md).
- [Three-payload fork theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/e83e85afd4f5c2dcb08f4c7cb5067337fece4b93/ResearchHistory/UQCF-GEM/research/physical-bridge/THREE_PAYLOAD_PRECEDENCE_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/d7394285e70d21476dadc08ffd713a4787799e35/ResearchHistory/UQCF-GEM/research/physical-bridge/THREE_PAYLOAD_PRECEDENCE_CLOSEOUT.md).

Three payloads begin at core a with targets b,c,b and an invariant environment root at b. Retained core miss counts plus labelled target address derive the fork graph p->q and r->q. Either b-target may be completed first; graph renewal gives the induced one-edge graph. The c-target q is uniformly unsafe until both predecessors complete: its addition leaves tau=4 but its deletion gives tau=5. After both predecessors complete q is safe.

Both topological orders p,r,q and r,p,q reach the exact destination in six primitive edits. An arbitrary hidden spectator subset on p gives 2^s distinct full states following the same retained graph trajectory.

Two prospective scope corrections were made before the proof because broader hidden spectator placement could rescue the nominal tau5 state. The final carrier is therefore genuinely fiber-uniform rather than silently depending on hidden incidences.

## Retained macro-cycle and native interleaving escape now completed

Cycle realizability has a positive, carefully scoped answer:

- [Frozen macro-cycle scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/a0a1f6a9205375f2ca2c844702d7264791650487/ResearchHistory/UQCF-GEM/research/physical-bridge/MACRO_CYCLE_SCOPE.md).
- [Macro-cycle and interleaving theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/956d270b653a2c7eb23683de356674dd17027188/ResearchHistory/UQCF-GEM/research/physical-bridge/MACRO_CYCLE_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/430bf224c7e83da105e76f830d316fdf44efc269/ResearchHistory/UQCF-GEM/research/physical-bridge/MACRO_CYCLE_CLOSEOUT.md).

The residual source has unique two-cover {a,c}; the target has unique two-cover {a,b}. Completing any one of the three declared endpoint macros first destroys every residual two-cover and gives full tau=5. Hence the complete-macro policy has no initial source. Any faithful indegree-zero precedence-graph representation must contain a directed cycle, although the retained certificate does not select one canonical cycle orientation.

Native connectivity survives. Preparing p and q by adding b before completing either macro creates an overlap state in which BOTH {a,c} and {a,b} are residual covers. The remaining deletions then preserve {a,b}. The explicit six-primitive path stays at full tau=4 and reaches the exact destination.

Thus the macro cycle is a resolution artifact: atomic completion hides the certificate-overlap state needed for handoff.

## Phased retained-event interface now completed

The macro-cycle escape has been promoted to a reusable event-level theorem:

- [Frozen phased-event scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/66556bbeb7c49a17e1a53f6efa59da8bda8c94d9/ResearchHistory/UQCF-GEM/research/physical-bridge/PHASED_EVENT_INTERFACE_SCOPE.md).
- [Phased retained-event theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/4675afe7b90515502245ff09b39d992d54daf22e/ResearchHistory/UQCF-GEM/research/physical-bridge/PHASED_EVENT_INTERFACE_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/e50ccd46bd3adae7ae9b9f359570a04a297a8ae5/ResearchHistory/UQCF-GEM/research/physical-bridge/PHASED_EVENT_INTERFACE_CLOSEOUT.md).

A retained repair may now expose native PREPARE and FINISH events plus proof-only certificate HANDOFF markers. Fiber-uniform event legality/update and an acyclic retained event graph imply exact protected completion.

The closed macro-cycle carrier embeds with acyclic event graph Pp,Pq -> H -> Fr,Fp,Fq1 -> Fq2. Before H the old cover {a,c} persists; after both preparations the replacement cover {a,b} also exists; after H the new cover protects all finishing deletions.

Crucially, this acyclic event graph has no topological execution satisfying whole-macro contiguity: p's finish requires q's preparation, q's finish requires p's preparation, and r requires the handoff. The earlier macro deadlock is therefore formally identified as a coarse scheduling/contiguity effect, not native disconnection.

## Automatic upper-cover handoff now completed

The phased prepare/handoff/finish structure can now be derived automatically for the upper certificate channel:

- [Frozen automatic-cover scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/9569cbcd8f6797ee93134cb5cded4a40e5139298/ResearchHistory/UQCF-GEM/research/physical-bridge/AUTO_COVER_HANDOFF_SCOPE.md).
- [Automatic upper-cover theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/9a34fb8d949c325cf03d52afebc72b4c0d331fdf/ResearchHistory/UQCF-GEM/research/physical-bridge/AUTO_COVER_HANDOFF_RESULT.md).
- [Scoped analytical closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/e13f829e5bef68d8558d355300ec07b18f53d8b6/ResearchHistory/UQCF-GEM/research/physical-bridge/AUTO_COVER_HANDOFF_CLOSEOUT.md).

Given an old <=4 cover H0 and replacement <=4 cover H1, retained endpoint signatures determine the event graph root-by-root. A root without a common H1 hit receives a selected destination-only H1 gain before the handoff. A root without a common H0 hit retains one selected source-only H0 incidence until after the handoff. All additions precede deletions within each root for floor safety.

The resulting graph is automatically acyclic by levels addition -> handoff -> deletion. H0 is guaranteed before handoff, H1 at and after handoff. With an independent lower certificate this gives a complete protected endpoint path.

Applied to the macro-cycle carrier, the rule reconstructs the essential p/q preparations and held p/q/r deletions without being supplied the earlier safe schedule. It also correctly discovers that q's deletion of f does not threaten H0 and may occur before handoff.

## Automatic lower-witness handoff and joint event cycle now completed

The lower certificate channel is now automatically derived:

- [Lower-witness scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/5f9a109c68c9784b2a04c80e82a2ad3450a8c77a/ResearchHistory/UQCF-GEM/research/physical-bridge/AUTO_LOWER_WITNESS_SCOPE.md).
- [Automatic lower-witness theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/ee25f0bc94ecef95b5e2c602258423be3e634b6a/ResearchHistory/UQCF-GEM/research/physical-bridge/AUTO_LOWER_WITNESS_RESULT.md).
- [Lower-witness closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/371f999d7dd0ef894f29b2bd104d6f4bc75969a5/ResearchHistory/UQCF-GEM/research/physical-bridge/AUTO_LOWER_WITNESS_CLOSEOUT.md).

For each physical pair K, deletions that establish the selected new missed-root witness are forced before a pair handoff marker, and K-additions that would destroy the selected old witness are forced after it. The lower-only graph is acyclic by deletion -> marker -> addition.

Combining this with floor edges produces the first exact joint event cycle:

- [Joint-cycle scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/19847a5e7e0f75563e4933cd7dda96446687cff0/ResearchHistory/UQCF-GEM/research/physical-bridge/JOINT_AUTO_EVENT_CYCLE_SCOPE.md).
- [Joint-cycle and temporary bypass theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/2d7ced1826c0b3cd05bf6bec07252afd8234a96a/ResearchHistory/UQCF-GEM/research/physical-bridge/JOINT_AUTO_EVENT_CYCLE_RESULT.md).
- [Scoped closeout](https://github.com/proteinfoldingengine/WetLabEngine/blob/537a959126ca2ff89faf8445619064424af8809c/ResearchHistory/UQCF-GEM/research/physical-bridge/JOINT_AUTO_EVENT_CYCLE_CLOSEOUT.md).

For saturated singleton swap r1:{x}->{y}, r2:{y}->{x} with fixed {z}, lower witness handoffs and necessary floor edges give
    A1->D1->rho_x->A2->D2->rho_y->A1.
No endpoint-only native event is legal from the source.

One temporary off-endpoint label w breaks the cycle:
    +w(r1), -x(r1), +x(r2), -y(r2), +y(r1), -w(r1).
Every state has tau=3 and floors1, and the exact target is restored.

This is distinct from the earlier macro-cycle escape: that obstruction vanished under endpoint-event interleaving; this one requires a temporary off-endpoint incidence.

## One reusable auxiliary for singleton permutation cycles — candidate under review

- [Frozen scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/51bb75d3ca71f35c62b480eee21e6f9afcdd6fbb/ResearchHistory/UQCF-GEM/research/physical-bridge/AUXILIARY_PERMUTATION_SCOPE.md).
- [Complete proof candidate](https://github.com/proteinfoldingengine/WetLabEngine/blob/dcec4d02f79539c4b4ba0e5eb827917149040e77/ResearchHistory/UQCF-GEM/research/physical-bridge/AUXILIARY_PERMUTATION_RESULT.md).
- [Author-side audit and independent-review gate](https://github.com/proteinfoldingengine/WetLabEngine/blob/167e826370f7911aa17924a6cc7071a9b00dcd06/ResearchHistory/UQCF-GEM/research/physical-bridge/AUXILIARY_PERMUTATION_AUDIT.md).

For n=3 or4 floor1 singleton roots with distinct labels and a target permutation, a single fresh auxiliary label w is reused to repair every nontrivial permutation cycle. The proposed exact schedule uses 2m+2c native edits for m moved roots in c nontrivial cycles and preserves pairwise disjoint supports, hence tau=n throughout. For n=3 any nonidentity target permutation is endpoint-only blocked; for n=4 endpoint-only swaps can sometimes succeed, so w is not universally necessary.

The frozen result received an independent mathematical ACCEPTED verdict at 361e5931368e44b2bfc6c82fad7483d92c05455a and a separate independent publication-consistency acceptance (with reporting clarifications) published at fc618c3223e19c38f94fb9abd38b965cbaaef7e9. Reporting reconciliation is published at b6b738f54dd7cef3861da79415151a0b81192b20. The final scoped closeout is at 4f9a65bfb0e71be48e8bb14b4f9dcf3cf567ab5d. The frozen proof is unchanged.


## Coupled-cycle theorem-first program opened (2026-10-07)

- [Prospectively frozen C1-C6 scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/f95cdfef30b452e1688172b978ee2e25fb1924d8/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_AUXILIARY_SCOPE.md).
- [C1 minimum-overlap lemma candidate](https://github.com/proteinfoldingengine/WetLabEngine/blob/5836e007044372fd61316a360a0b224e2fd1c8ea/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C1_MINIMAL_OVERLAP.md).
- [C1 author-side audit and padded-overlap rejecting control](https://github.com/proteinfoldingengine/WetLabEngine/blob/ec471f259e6ab88f75d0f051dd6f1869e115ad1e/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C1_AUDIT.md).

For n nonempty labelled roots, tau=n iff their supports are pairwise disjoint. Therefore n=3 cannot exhibit overlap in the protected band; the smallest overlapping protected carrier has n=4, with tau=3 at any overlapping endpoint. This is a proved author-side structural filter, not an independently certified coupled-cycle result.

The audit also rejects a padded four-root singleton swap with a fixed overlapping root: genuine overlap does not by itself create coupled endpoint obligations. C2 must identify actual interacting obligations, with native witness/cover evidence. C3-C6 remain open. No numerical campaign has been authorized.


## C1 accepted; active four-root C2 carrier published (2026-10-07)

- [C1 independent mathematical verdict](https://github.com/proteinfoldingengine/WetLabEngine/blob/29e259186a1dafb976a565a62b549b02e986ba09/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C1_INDEPENDENT_REVIEW.md) — ACCEPTED with minor declaration of the auxiliary palette label w in the padded control.
- [Frozen C2 carrier](https://github.com/proteinfoldingengine/WetLabEngine/blob/c00318259d31c92e2dd0bd7a3ce97755bf74ea02/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C2_SCOPE.md).
- [C2 complete proof candidate](https://github.com/proteinfoldingengine/WetLabEngine/blob/5d4e7548c03c7c13b04f25f5a39cb723a684ceb6/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C2_RESULT.md).
- [C2 author-side audit](https://github.com/proteinfoldingengine/WetLabEngine/blob/e12dca9218de6e3db9bbea5f6971b01158b879d3/ResearchHistory/UQCF-GEM/research/physical-bridge/COUPLED_C2_AUDIT.md).

The C2 carrier has four active labelled roots with source ({a},{b},{c},{a,d}) and target ({b},{a},{c},{b,c}), all floors1. A complete eight-edit endpoint-only path preserves tau=3. M2-first is unsafe, and completing M4 first changes both other macros' first additions from potentially protected to tau=2 violations. Unlike the earlier padded control, M4 is itself an endpoint obligation that changes witness availability.

This establishes a concrete candidate for coupled order-dependence, NOT an auxiliary-necessity or coupled-cycle theorem. Fresh external C2 mathematical review launched: job 01a11835-dee1-77ee-8285-5854a3f05566. C3-C6 remain open. No numerical campaign or physical claim.


## C2 independent closeout completed

- [Initial REVISE record](https://github.com/proteinfoldingengine/WetLabEngine/commit/7da41a7d6792ef445862c07dfce01704c294c143).
- [Corrected frozen proof](https://github.com/proteinfoldingengine/WetLabEngine/commit/0d91bb646a3b641cce7c9c90ca462aa767400ce8).
- [Fresh independent mathematical ACCEPTED review](https://github.com/proteinfoldingengine/WetLabEngine/commit/3aea01fdd5acfdd4b66089b148fcff21c0f63e03).
- [Separate independent publication audit](https://github.com/proteinfoldingengine/WetLabEngine/commit/d36b3a068b29a2f869ccb173f263b58200d1711e) — ACCEPTED WITH REPORTING CORRECTIONS.
- [Final scoped C2 closeout](https://github.com/proteinfoldingengine/WetLabEngine/commit/787467cc6a1bfc9f09f586809948ebfe16d32742).

The revised proof's header still says re-review was required; that is an immutable pre-review snapshot, superseded by the later independent ACCEPTED review. The bounded C2 theorem is now closed. It establishes an eight-edit tau=3 protected path and order-dependent witness failures in one active four-root carrier. It does NOT establish necessity of an auxiliary or a coupled-cycle deadlock. C3-C6 remain OPEN.


## C3 first obstruction gate: three singleton anchors

- [Frozen C3 structural scope](https://github.com/proteinfoldingengine/WetLabEngine/commit/f12d6775214b827ede8e5a5248e9b8f92721c048).
- [C3 analytical lemma candidate](https://github.com/proteinfoldingengine/WetLabEngine/commit/f99a7622a968d8a5ebdfebb4e43c76dc4e925fb0).
- [Author-side audit](https://github.com/proteinfoldingengine/WetLabEngine/commit/f6291c0c46248465e0f6e625f78866e28f03e8ef).

For four nonempty roots with three distinct frozen singleton supports {a},{b},{c}, every nonempty fourth support has 3<=tau<=4. Therefore an active fourth root can always execute its own endpoint-only additions before deletions while the singleton triple stays frozen, preserving floors and the band. This excludes an initial endpoint-only deadlock in that special carrier but does not prove full endpoint connectivity or general auxiliary impossibility.

Fresh independent mathematical review launched: job 01a1195c-f9c9-724f-bac6-e7d7d3e901c8. C3 remains OPEN. The next genuinely discriminating carrier must not rely on three frozen singleton anchors.


## C3 four-root coupled endpoint-only deadlock and one-buffer bypass candidate

- [Frozen prospective scope](https://github.com/proteinfoldingengine/WetLabEngine/commit/08eb9dada9c5d4665453768810522303119d2fe6).
- [Analytical proof candidate](https://github.com/proteinfoldingengine/WetLabEngine/commit/a2346862f2aa9c1a4b03b986b2ae3abf2381ec37).
- [Author-side audit](https://github.com/proteinfoldingengine/WetLabEngine/commit/745065f7fe938d729aba4b473f0753bfaa2ca02b).
- [Earlier independently accepted C3 anchor lemma](https://github.com/proteinfoldingengine/WetLabEngine/commit/3069106e708714fcaac36553cc39ef5967938b05).

The new carrier has source ({a,b},{b,c},{a,c},{d,e}) and target ({b,d},{b,c},{c,d},{a,e}), floors2. At source every endpoint-only deletion violates its floor and each endpoint-only addition creates an explicit two-cover. The proposed native eight-edit path using temporary w on r4 keeps tau=3 at every state and removes w at exact target. The author-side proof also gives a carrier-specific 8-edit lower bound.

This is a stronger, genuinely coupled positive candidate than the C2 order-dependence example, but not a universal retained host-selection or renewable-cycle theorem. Fresh independent mathematical review launched: job 01a11962-0b81-76ac-865b-f75aac9fd5c3. Do not promote C3 to closed before review and further retained-controller work.


## Bounded C3 coupled deadlock independently closed

- [Independent mathematical acceptance](https://github.com/proteinfoldingengine/WetLabEngine/commit/50b3073e09a4dd7afff0e2ec0f05efd901056e5e).
- [Separate independent publication audit](https://github.com/proteinfoldingengine/WetLabEngine/commit/d31e3654bd020532d6fd04dc08f0ed9790da9c81).
- [Final scoped closeout](https://github.com/proteinfoldingengine/WetLabEngine/commit/fae793e6fb586c949845e495ec243bd996b0cdf4).

The frozen four-root carrier has no legal endpoint-only first edit, but one temporary w on its fourth root gives a minimum eight-edit protected path with tau=3 throughout and exact cleanup. Independent mathematical and publication reviews accepted this bounded result. The initial REVISE was a source-retrieval issue, not a mathematical counterexample.

Broader C3 is still OPEN: derive a fiber-uniform retained host-selection rule and renewable protection across multiple genuinely coupled changes. C4-C6 remain OPEN. No numerical, formal proof-assistant, or physical validation claim.


## C3 optimal auxiliary host selection — new analytical candidate

- [Frozen scope](https://github.com/proteinfoldingengine/WetLabEngine/commit/22d0f1cfa93406379e9e0950d12548c422495f28).
- [Complete proof candidate](https://github.com/proteinfoldingengine/WetLabEngine/commit/b91a850caf5b9e56094698cdd475243b793c62db).
- [Author-side audit](https://github.com/proteinfoldingengine/WetLabEngine/commit/9911ffebc3dc87d44646b6be3af7f02eb8ae50ac).

In the already accepted four-root coupled carrier, the new theorem candidate classifies every possible first off-endpoint addition and proves only +w on r4 can initiate an eight-edit minimum protected path. In fact +w(r4),-d(r4) are forced first two events in any optimal path. The result uses the declared labelled endpoint supports and explicit two-cover witnesses, not an undeclared hidden-state read. It is NOT a general compressed retained host-selection theorem. Independent review job 01a1198c-a99c-70a8-98fc-60a33c47fc84 is processing.


## C3 unique optimal host independently closed

- [Independent mathematical ACCEPTED review](https://github.com/proteinfoldingengine/WetLabEngine/commit/c714fe91b55eccd919d6f402ce2b3bbb4cfb788d).
- [Reporting addendum](https://github.com/proteinfoldingengine/WetLabEngine/commit/663130a41cb1d8ac17b2b9eaee6949146011fd20).
- [Independent publication audit ACCEPTED](https://github.com/proteinfoldingengine/WetLabEngine/commit/2a3780b9ad5438b43667dde79c5c4a92b8b6a61e).
- [Final bounded closeout](https://github.com/proteinfoldingengine/WetLabEngine/commit/e34768054850ebcea714c6f56834cae2231a80df).

In the declared four-root carrier, r4 is the unique auxiliary host in EVERY minimum eight-edit protected repair, with forced prefix +w(r4),-d(r4). All other first additions are excluded by explicit two-covers, and r1,r2,r3 hosts cannot finish within the eight-edit budget. This is an independently reviewed bounded optimal-host result, NOT a general retained-information host-selection theorem. Broader C3 and C4-C6 remain open.


## C3 hidden-spectator optimality discrimination (candidate)

- [Frozen scope](https://github.com/proteinfoldingengine/WetLabEngine/commit/c2383f36b4c099f8bb27582639b55c2cb59c94a2).
- [Proof candidate](https://github.com/proteinfoldingengine/WetLabEngine/commit/f1531c690ba36662c5a016cd7f2a0cd6ab084275).
- [Author-side audit](https://github.com/proteinfoldingengine/WetLabEngine/commit/4fde7e4c9ac8ccb5b254e62802509ef115ee0f65).

In the bounded coupled four-root family, add an arbitrary hidden spectator subset Z to r4 at BOTH endpoints, with all spectators invariant. The original eight-edit buffer route remains uniformly LEGAL. But for nonempty Z, a six-edit endpoint-only route is legal and optimal, whereas empty Z requires eight edits. Both fibers share the deliberately restricted core projection R. Thus R alone cannot select a shortest protected repair uniformly across both fibers; one extra retained bit 1[Z nonempty] suffices in this family.

This is an author-side candidate, not an independently accepted result. It does not show that the bit can be recovered from native observer variables. Independent mathematical review job 01a11997-77e2-75ac-9c97-8e8d6fc5aa1e is pending. Broader C3/C4-C6 remain open.

## Next unresolved obligation

The full B1/B2 program is NOT closed. The one-buffer singleton permutation-cycle theorem is independently reviewed and publication-closed. Its bounded scientific gate is complete.

The next mathematical frontier is COUPLED CYCLE BREAKING beyond disjoint singleton permutations: overlapping supports, shared witness obligations, and original floors that cannot be represented as independent label cycles. A valid theorem must derive a retained host-selection rule, maintain both protected-band bounds, prove finite termination and exact cleanup, and show where one buffer fails.

No numerical universe or implementation is launched by this continuation update.

## Evidence and unchanged boundaries

The earlier fixed-residual handover item was written mathematics with author-side review only. The newer singleton-permutation auxiliary theorem separately received independent AI mathematical and publication-consistency reviews. Neither result is a formal proof-assistant certification, numerical PASS, numbered v16 certification or physical validation.

A12.1-A12.5 remains closed at bbc6e6f68beaf7d2d1641e711b46b55ae0bf62db; issue #104, accepted A11 sources and certified v16.54/v16.55 remain untouched. No A12.6 is opened. No physical force, geometry, energy, GR/ADM, dark-matter replacement, physical nonlocality, continuum, observer field or fundamental-time claim follows from the handover result.
