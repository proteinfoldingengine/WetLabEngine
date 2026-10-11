# Raw adversarial analytical review

Reviewed: RESULT.md, 2026-10-11.
Scope: mathematical reasoning and scope discipline, using the source characterizations supplied in the review assignment. I did not independently audit the linked source files. No implementation, numerical enumeration, empirical validation, or scientific campaign was performed.

## Verdict

PASS on the exact classification, unique-least distinction, non-selection conclusion, and branching example. No critical or important mathematical defect found. One minor source-scope wording correction is recommended before publication.

## Mathematical checks

1. Necessity is valid. For an omitted nonroot vertex v, prefix closure prevents any retained descendant on its path below the longest retained ancestor of its parent. In particular r_Y(v)=r_Y(p(v)); preservation at both endpoints makes their signatures equal. Every signature-changing child must therefore be retained, including all its ancestors.
2. Sufficiency is valid. The finite path below the longest retained prefix has no retained vertex. Because every changing child lies in Y_min and hence Y, each edge on that path has equal endpoint signatures. Equality along the path proves preservation. This also verifies the full family of sufficient sets, not merely one sufficient candidate.
3. Root inclusion handles an empty change set, including the empty observable family. No assumptions on codomain structure beyond equality enter the proof. Repeated signatures and a return to an earlier signature do not invalidate the necessity argument: preservation must hold at every intermediate vertex too.
4. A unique least sufficient set is distinct from a uniquely permitted set. X is always sufficient because its retraction is identity. Thus a proper Y_min yields at least two sufficient choices, whereas Y_min=X forbids pruning. Under this exact contract, preservation cannot uniquely mandate any proper retained subset. This conclusion does not prohibit an additional selection law or another preservation contract.
5. Prefix closure correctly propagates retention through equal-signature edges above later changes. Consequently changing-child endpoints alone are insufficient without their ancestors; the stated prefix closure is necessary.
6. In the four-vertex example, only a changes signature from its parent. The mandatory set is {root,a}; b and c are independently optional with all prefixes already retained. The four displayed sets are exactly the sufficient ones, and the two stated retraction images preserve signatures.

## Genuine objection

Minor — source qualification: the connection paragraph says that v15.22 constructs its most-forgetful sufficient conditional expectation “for a supplied next instrument.” The supplied source characterization is narrower: a supplied sharp event instrument. Omitting “sharp” may suggest coverage of arbitrary instruments, which has not been established by this review. Replace that phrase with “for a supplied sharp event instrument,” or state the exact source hypotheses. The separate two-event identity-only statement already limits itself to the source’s particular model and contract. This wording issue does not affect the lineage theorem.

## Scope checks

The result explicitly declares its observables and vertexwise preservation obligation, and does not mistake them for an acquired physical record, complete quantum-instrument preservation, or arbitrary extensive source-array recoverability. It derives a retraction only after a retained set is chosen and never treats a least element as actual dynamics. Its final research decision avoids claiming a physical pruning law, a universal no-go, a certified campaign, new scientific-test counts, or resolution of the listed open physical obligations. These limits are appropriate.

No further blocking objection found within this review’s declared scope. Linked-source correctness beyond the supplied characterizations remains outside this review.
