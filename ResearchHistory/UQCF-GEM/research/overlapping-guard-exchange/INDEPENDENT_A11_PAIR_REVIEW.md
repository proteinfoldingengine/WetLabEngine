# Independent A11 pair-anchor analytical review

Verdict: **ACCEPT** the frozen analytical candidate, relative to its explicitly inherited accepted dependencies. No critical, important, or minor mathematical correction is required. This receipt approves the stated native connectivity result and preserved-profile corollary; it does not certify implementations, numerical results, or wider unresolved claims.

Reviewer: independent Codex scientific-review agent `/root/a11_pair_review`.
Signed: 2026-10-03 UTC.

## Exact source identity and isolation

Repository: `proteinfoldingengine/WetLabEngine`.
Candidate: `6525e708393c345b01e2004163fcc738f1e4d486`.
Scope parent: `f74b5afe9a81d2dbf328a515da506a87f401b6f3`.
Prior publication: `654840ae1bbbfbf701ab5b26623eb67c56003986`.
Subtree: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/`.

I independently fetched the proof and scope by immutable commit using the repository connector, rather than reviewing the mutable local draft. The fetched proof `A11_PAIR_ANCHOR_CONNECTIVITY.md` has Git blob SHA `79903ab4d85378d2a9eef6c908dce7711dcae896`, exactly 16,385 UTF-8 bytes, and SHA-256:

`7c60e7d5b80838acc9f24cf9d0659d132d5cbd3db80b6a843e17faa286d6cfc2`

This matches the expected review hash. Exact bytes include the final blank line. The independent fetched-byte copy is `A11_PAIR_REVIEW_REMOTE_PROOF.md` in the review scratch directory.

The scope blob SHA is `325cea1b5ca87c4b95b0a7b8cfa069e163a71dbb` at both scope parent and candidate. Independent commit comparisons establish that scope parent is one commit ahead of prior publication, adding only the 15-line scope file; candidate is one commit ahead of scope parent, adding only the 156-line proof. Both comparisons are ahead by one, behind by zero, with the respective base as merge base. No earlier source or receipt was changed in those comparisons.

## Inherited source domains checked

I fetched the following sources at immutable baseline `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`, under `ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/`:

- `GENERAL_PARENT_CONNECTIVITY.md`, blob `922ae44713c6810c5a99716c52ecb37738a880a6`: Lemma C permits zero capacities and proves finite capacity-preserving, element-cover-preserving owner transfers when total capacity exceeds palette size. Theorem A converts finite lower paths between exact endpoints to the downward one-unit band on the fixed width-floor carrier.
- `OVERLAPPING_CLIQUE_EXCHANGE.md`, blob `865f0797892a2e5e869ec2180d3c842026889445`: Lemma L applies to arbitrary overlapping supports, preserving labelled slots and floors through primitive transposition paths at exact completed hitting level.
- `GUARD_BUFFER_CONNECTIVITY.md`, blob `c6d018092e1ea18b1baaaadefde8c05e758bbb6d`: Theorem AC applies to uniform floors with the stated existing-slot threshold.

I also fetched `A11_RESIDUAL_THREE_ANCHOR_LIFT.md` at prior publication `654840ae1bbbfbf701ab5b26623eb67c56003986`, blob `5f541b6502bcfb1ab7882fb98946cb3ee60ad8cf`. Its common residual preparation and finite descent argument apply to the corollary with a changed anchor count and preserved floor-two slot. These are domain/applicability checks of accepted dependencies, not independent recertification of the baseline proofs.

## Main theorem obligations

1. **Exact compaction and symmetry:** the selected floor-two root contains an actual label of the minimum four-cover. Retaining that incidence plus another distinct incidence keeps floor two and the cover, while deletion cannot lower transversal. Thus every compaction primitive is exact four. Lemma L realizes the full-palette alignment, with exact-four completed stages and every primitive in {3,4}. Reversing destination normalization restores exact original labelled incidences.

2. **Actual guard:** for each residual x, forbidden triple {u,v,x} is missed by a nonanchor root avoiding both pair labels. Its residual complementary block contains x. Therefore these actual M blocks cover R. All M supports retain positive original floors; their residual transversal g is at least two. The tracked four-cover hits M with two or three residual labels, proving g<=3. Disjoint pair root and M give exactly 1+g and protect every two-label candidate during preparation.

3. **Strict derived slack:** M lies in the common floor-defined flexible set F. Coverage implies n<=sum_M |Q_i|<=sum_M c_i<=sum_F c_i. Equality at n forces a partition of R by saturated M blocks and zero capacity in every inactive flexible slot. Positive original floors force every partition part to have size at most n-1, hence at least two nonempty parts. A cross-part pair x,y cannot lie in one M block. Forbidden triple {u,x,y} cannot be contained in a Z complement (capacity at most one), an inactive F complement (capacity two), or the selected-root complement (which misses u). It would have to be contained in an M block, contradiction. The integer bound sum_F c_i>=n+1 is valid without an invented resource.

4. **Same residual carrier and every preparation primitive:** F/Z depend only on original floors and n, not on endpoint activity. Holding actual M and T fixed protects tau>=3. Adding R to each inactive flexible support and then deleting source-only labels respects its original floor. The old minimum four-cover hits expansion states through the old support and contraction states through R; H_R is nonempty. High-floor expansion retains its old support. Thus every preparation primitive also has tau<=4. At completion inactive flexible roots R are redundant for M's nonempty residual cover. Every subsequent permitted residual tuple has exact full transversal 1+tau_R; full-palette Z supports add no condition.

5. **Lemma C's additional upper band:** duplicate removal adds support incidences, so cannot increase g, and element coverage maintains g>=2. At an owner partition, at least two bins are nonempty because c_i<=n-1; labels in different bins form a two-cover of complementary supports, making g exactly two. Each add-before-delete transfer has only one block-addition intermediate, equivalently one legal support deletion; nonempty remaining support bounds its transversal by old g+1<=3. The inherited two-transfer buffering procedure returns to a partition between transfers and preserves capacities and coverage. Initial and target duplicate stages have the correct monotonic bounds; during target duplication each intermediate support contains its target support, giving g<=target g<=3. Zero-capacity bins present no problem. Spare space is an existing slot, and the Lemma C fixing count gives finite termination.

6. **Lift and restore:** complementary block toggles are individual support toggles at original indices with unchanged floors. Fixing T and Z=P lifts residual {2,3} exactly to full {3,4}. The finite concatenation of source normalization/preparation, residual connection, and reversed destination preparation/normalization restores C exactly. The main theorem constructs the band directly and makes no use of Theorem A.

These checks establish one original floor-two slot suffices at target four with arbitrary remaining positive floors. With accepted X3, the sufficient class includes every exact-four carrier with any original floor at most two.

## Corollary and boundary checks

For q>=5, choose exactly m=q-4 floor-one anchors excluding the distinct floor-two slot. X3's singleton normalization may raise hitting level, which is allowed in the preliminary lower path. Canonical singleton decomposition gives active residual level at least four. The residual palette size n=k-m is at least four; the distinguished floor-two slot is flexible and retains its original floor two even if preparation replaces its initial inactive support by R. Finite additions reach exact residual four before dropping below it, by the one-incidence bound and eventual all-R level one. Thus the residual endpoints satisfy this particular X4 theorem, with no universal target-four floor-vector premise. Its direct middle band lifts to {q-1,q}. Reversing destination construction preserves the lower bound, and accepted Theorem A removes possible upper excursions from the complete lower path. The q=4 corollary is exactly X4.

The all-twenty-triples example on six labels is analytically exact four. For a fixed triple anchor T, the only root avoiding all three anchor labels is R, whose residual transversal is one and whose residual complement is empty. Preparing every other root to R ends at full transversal two, so this particular preparation cannot maintain the required lower bound three. This is a method obstruction, not disconnection. Uniform h=3,q=4 gives N=C(5,3)=10 and r=20=2N, placing this carrier under inherited AC; the proof correctly does not advertise it as unresolved.

For a triple root, every candidate pair meeting T must be missed elsewhere to ensure lower transversal three. At exact four, each pair {a,b} in T and each x outside T belongs to a forbidden triple {a,b,x}, yielding an outside-label cover from roots avoiding that pair. There are three overlapping pair-indexed systems. The proof states their exact endpoint-derived protection condition and leaves simultaneous renewal with shared capacities unresolved; it does not substitute the failed all-triple-avoiding family for these systems.

The proof keeps its scientific boundaries: native temporaries and repeated toggles are permitted; universal destination-directed/monotone A11 scheduling remains open; no necessity or minimality claim is made; all-floor-at-least-three target-four cases remain unresolved outside accepted classes; unrestricted nested universality remains conditional on inherited child interfaces. No enumeration, numerical campaign, implementation, tests, workflows, publication action, efficiency claim, physical implication, or originality claim was used in this review.

## Signed disposition

**ACCEPT, no issues requiring revision.** The exact-source pair-anchor theorem, its derived slack and direct residual band, the higher-target preserved-profile corollary, and the stated remaining frontier meet the frozen scope.

Signed: independent Codex reviewer `/root/a11_pair_review`, 2026-10-03 UTC.
