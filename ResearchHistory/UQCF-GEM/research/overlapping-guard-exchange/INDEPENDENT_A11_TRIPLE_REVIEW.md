# Independent exact-source review: A11.X5 triple-anchor renewal

**Verdict: ACCEPT the conditional analytical theorem as written.** No critical, important, or minor mathematical defect found. This acceptance is restricted to the frozen declared input and inherited dependency domains; it is not universal triple-anchor availability, destination-directed scheduling closure, implementation certification, or unrestricted native lifting.

Signed: **Codex independent reviewer /root/a11_triple_review**, 2026-10-03 UTC. This is an attributable analytical review signature, not a cryptographic signature.

## Exact source and isolation

Repository: proteinfoldingengine/WetLabEngine. All scientific sources were independently fetched through the GitHub connector using the immutable refs below, rather than relying on another agent's transcription or local checkout.

- Prior publication: `c39e169dff22c3b9754ff7062b6c7fc99f88f0a0`.
- Scope: `aad997b37eba3fef5059d8729c46ebfec87a3eef`, `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_TRIPLE_ANCHOR_SCOPE.md`.
- Proof: `3857dfcc33eccb2c01456a1273426ab9dd94bade`, `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_TRIPLE_ANCHOR_RENEWAL.md`.
- Proof Git blob SHA: `a799c157067a137756f2bfe0b63dcf78e806ca4c`.
- Independently saved UTF-8 proof: **13,130 bytes**.
- Independently computed SHA256: **`de5ab2e018f7c3e5ede7f69e205828c729d6abfbd331458b7a8fe35306266e35`**, exactly the supplied expected digest.

Git data commit responses show the scope commit's sole parent is the prior publication, and the proof commit's sole parent is the scope commit. GitHub comparisons show each transition is ahead by exactly one commit, behind by zero. Prior-to-scope changes only add the 13-line scope file; scope-to-proof changes only add the 121-line proof file. Thus the scope and proof are isolated document additions, with no implementation, tests, workflows, or inherited source edits in either transition.

Exact-source URLs:

- [Scope](https://github.com/proteinfoldingengine/WetLabEngine/blob/aad997b37eba3fef5059d8729c46ebfec87a3eef/ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_TRIPLE_ANCHOR_SCOPE.md)
- [Proof](https://github.com/proteinfoldingengine/WetLabEngine/blob/3857dfcc33eccb2c01456a1273426ab9dd94bade/ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A11_TRIPLE_ANCHOR_RENEWAL.md)

## Inherited sources and domain checks

The following were independently fetched at integrated baseline `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`, under `ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/`:

1. `GENERAL_PARENT_CONNECTIVITY.md`, Section 5, Lemma C: finite capacity-bounded element-cover connectivity when total capacity is at least palette size plus one, including zero capacities. X5 invokes this only in its strict-slack regime. Its residual blocks cover the finite palette R; capacities are integral, nonnegative, and at most n-1; and their total is at least n+1. All these hypotheses are verified, so the domain is correct.
2. `OVERLAPPING_CLIQUE_EXCHANGE.md`, Section 2, Lemma L: primitive realization of any palette transposition from an exact-q tuple in {q-1,q}, preserving root sizes and floors. X5 invokes it only after exact-four compaction and between completed exact-four stages. There is no root permutation or alteration of labelled floors.

`A11_PAIR_ANCHOR_CONNECTIVITY.md` was independently fetched at prior publication `c39e169dff22c3b9754ff7062b6c7fc99f88f0a0`, under the same research subtree as X5. Its Section 6 upper-band argument is applied with its actual residual hypotheses checked in X5 Section 4. X4's universal floor-two input theorem and derived strict slack are not imported into the triple-anchor setting. The saturated case is handled separately. These are dependency-domain checks, not recertification of inherited results.

## Detailed mathematical findings

### 1. Input is conditional at both endpoints

The theorem requires exact-four A and C on the same fixed palette and labelled positive-floor carrier, with the same distinguished ORIGINAL floor-three slot. At EACH endpoint the supplied triple T lies in that root and meets a supplied four-label hitting set H. The actual family of OTHER roots disjoint from T must have residual transversal at least two. The requirement refers to existing supports, not hypothetical guards or only one endpoint.

Because exact four gives |P|>=4, R is initially nonempty. For positive supports contained in R, residual transversal at least two is equivalent to every residual label being missed by some family member. Consequently the complementary M blocks cover R. The hitting set H intersects T and its residual portion hits M with at most three labels. Thus the residual level is two or three; in particular M is nonempty and n>=2. There is no inference of this guard merely from a floor-three slot.

### 2. Compaction and alignment are exact at completed stages

Compacting only the distinguished root to supplied T preserves its original floor three. H continues hitting that root because T intersects H; it hits all untouched roots. Deletion cannot decrease transversal, so each compaction primitive remains exact four. Lemma L realizes the chosen palette permutation with single incidence moves in {3,4}; each completed transposition remains exact four. Guard membership and residual transversal are transported by the permutation. Reversing the destination's own word later restores its original labels, not merely a support isomorphism.

### 3. Common residual carrier and preparation are valid

F and Z are defined using original floors and common n, so both endpoints yield the same labelled F, Z, and capacities c_i=n-a_i. M is contained in F because its supports fit R. For each F-minus-M root, the union bridge to R never violates the floor; Z expansion to P is legal. Fixed T plus the unchanged actual M family has transversal 1+g>=3 and protects the lower bound. The old H remains a four-cover on every primitive: expansions contain the old support; contractions contain R, hit by nonempty H_R.

At completion every F support lies in R and every Z support equals P. F is nonempty, and any positive residual cover hits a whole-R root. The full transversal equals one plus residual transversal, because T and F occupy disjoint label sets and P roots add no constraint. This equality is valid for every subsequent permitted residual tuple, not just the endpoint count. The endpoint inequality n<=sum_M|Q_i|<=sum_M c_i<=sum_F c_i correctly leaves both integral capacity regimes possible.

### 4. Strict slack has a primitive upper-band proof

Removing duplicate block incidences adds support incidences, so the residual transversal cannot rise; retained element coverage prevents level one. Owner partitions have exact residual level two: two labels in distinct nonempty bins hit every complementary support, while every singleton is missed at its owner. Distinct nonempty bins exist because capacities are at most n-1.

Each inherited C transfer passes through only one duplicated-owner state, a single legal support deletion from a level-two partition. Remaining support positivity supplies the standard one-label repair of an old cover, bounding that state by three. Buffering consists of two sequential completed transfers, with a partition between them; no accumulated two-unit bound is needed. Target duplicate restoration keeps each block inside its target and hence each support above its target, bounding transversal by the target level. Thus all residual primitives lie in {2,3}; additivity gives full {3,4}. Finite progress is inherited from C within its verified domain.

### 5. Saturation derives three existing reserves

When total capacity equals n, equality in the endpoint chain forces the actual M blocks to partition R at full capacities; every F-minus-M capacity is zero; every positive-capacity F slot belongs to M. Positive original floors give each block size at most n-1, so two source labels can be chosen in distinct owner bins.

In the aligned exact-four source before preparation, each triple {t,x_0,y_0} must miss an existing root. Such a root is not the anchor; it is not M because no M partition block contains the cross-bin pair; and it is not Z because a support avoiding three labels has size at most n, below every Z floor. It therefore belongs to F-minus-M, with ORIGINAL floor n. Avoidance bounds its support by the n-element set (R minus {x_0,y_0}) union (T minus {t}); its floor forces equality. The three such supports differ, so the root slots are distinct. The argument is existential at the exact source and does not execute an unsafe reversal of preparation.

These reserves are existing labelled zero-capacity F slots. Their prepared supports are R. Their common original floor n permits reuse for arbitrary later cross-bin pairs. No extra root, palette label, or unit of residual slack is postulated.

### 6. Every primitive of renewal and owner exchange is safe

Reserve construction first adds two anchor labels, then removes x and y. Each reserve retains size at least n. Throughout construction, the unchanged T and positive-capacity owner partition maintain the lower bound three. Each intermediate contains R on the addition half or B_t on the deletion half. The same containment statement holds on reversal.

The four owner edits remove x from its old block and y from its old block before inserting them into the opposite blocks. Their supports remain in R, satisfy original floors, and all requested incidences are present or absent as needed. In particular y starts in support i, since its original owner is j, and x starts in support j. Capacity is freed before either insertion.

For the lower bound during these four edits: residual-residual pairs miss T; anchor-anchor pairs miss any positive-capacity F support; mixed pairs involving z outside {x,y} miss the unchanged owner of z; mixed pairs involving x or y miss installed B_t. Every set of at most two labels extends to a pair since |P|=n+3>=5. Thus no two-cover appears even when both exchanged labels are temporarily ownerless.

For the upper bound throughout construction, exchange, and restoration, any two distinct anchor labels u,v together with x,y form a four-cover. Every B_t meets {u,v}; each union bridge intermediate contains R or B_t; untouched whole-R/P roots meet that cover. No positive-capacity block contains both x and y at any owner-edit stage, so each corresponding support meets {x,y}. This bound does not rely on an unjustified exact-four claim at reserve stages. After the exchange the saturated partition is restored, and T plus it protects reserve restoration. Once all reserves again equal R, the full level is exactly three.

The n=2 edge case also satisfies these arguments: B_t consists solely of the two anchor labels other than t; the four-cover still hits it, and positive-capacity R supports still witness all anchor-anchor pair misses.

### 7. Renewal supplies finite reachability and labelled restoration

Destination bins have the same saturated cardinalities c_i. A misplaced x destined for j implies j contains some y not destined there; otherwise its existing c_j correctly destined occupants plus x would exceed destination cardinality. Swapping x and this misplaced y fixes x and displaces no correct label. The misplaced count decreases by at least one. At most n swaps suffice, and reserve restoration occurs within every swap word, so the next exchange remains available.

Final owner equality restores all positive-capacity F supports. Zero-capacity F supports are R and Z supports P, with the original reserve slots restored as well. Reversing the destination preparation, alignment, and compaction restores every original labelled support. All pieces are finite primitive words, preserve original floors, and retain the same {3,4} band upon reversal.

## Boundaries and issue disposition

No critical, important, or minor issue was identified. The receipt approves the exact frozen source without requesting amendments.

The supplied actual avoiding-family condition remains essential to this sufficient mechanism. The six-label all-twenty-triples example has only complementary R avoiding fixed T and residual transversal one, so it lies outside X5. This failed guard is not a disconnection claim. Its accepted-class coverage is inherited from the prior X4 statement, not newly certified here.

X5 adds a conditional target-four floor-three class. It establishes no minimum-floor necessity, universal guard existence, incidence-monotone or destination-directed schedule, unrestricted root/nested universality, efficiency, physical, originality, or implementation claim. Native lifting is conditional on the accepted child interfaces. No numerical enumeration, scientific computation, campaign, code execution, tests, workflow changes, repository mutation, or publication was performed for this review; shell commands only handled and hashed the fetched document.

**Final signed assessment:** the frozen source proves the declared conditional theorem, including strict slack, saturation with existing renewable reserves, all primitive floor/band obligations, finite progress, and exact labelled endpoint restoration. — Codex independent reviewer /root/a11_triple_review, 2026-10-03 UTC.
