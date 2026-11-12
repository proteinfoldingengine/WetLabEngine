# Draft 15: E5+ retains its positivity condition

Author: proteinfolding-gpt. Date: 2026-10-19 UTC.
Status: **UNREVIEWED ANALYTICAL QUALIFICATION**. Additive scope note; no new scientific execution, independent review or certification is claimed.

## Preserve the positive result

The main equivalence in Theorem 21.2(c) is sound on its declared E1-E4 class, including the cone-carrier premises:

    CN-parent <=> CN-every-cone <=> E5 <=> R <=> P1.

Its proof needs no positivity: conservation and ancestor-only credit in the re-rooted parent cone force the removed leaf's amount to its parent; CN transports that result to the ambient carrier. Actual CN, occurrence, ownership and access remain declared inputs.

This note qualifies only the additional claim that **E5+** joins that equivalence without positivity. The frozen draft's header and section-21 novelty paragraph make that claim; the review's novelty assessment and the [published receipt](https://github.com/proteinfoldingengine/WetLabEngine/blob/b14db95922a6ca46dd49be662df587f68dfab773/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d15_review/STATUS.md) repeat it. The main theorem's displayed equivalence correctly excludes E5+.

## The existing signed counterexample

Section 19.8 defines E5+ as conservation of the receiver's own cone total and explicitly uses positive crediting for its equivalence. Its signed weights (1,1,-1) already show why that condition matters.

Take the chain o -> a -> p -> l, prune leaf l, keep every retained basis input unchanged, and define

    T(e_l) = e_p + e_a - e_o.

Extend linearly. E1, E3 and ancestor-only E4 hold. The coefficients sum to one, so global conservation E2 holds. The parent cone contains p and l before pruning and p afterward; its total is conserved for every input:

    (T x)_p = x_p + x_l.

Thus E5+ holds. But in the re-rooted cone {p,l}, E2 and E4 force T_cone(e_l)=e_p. Zero extension gives e_p, which differs from T(e_l); CN fails. The a-cone receives coefficient two from e_l, so full ancestry retention R fails as well.

For a rule family, use these weights at depth three and P1 at other depths. This preserves E1-E4 and parent-cone conservation on every carrier while still violating CN. No new counterexample search is required.

## Minimal qualification and provenance

Keep the main CN/E5/R/P1 equivalence above without positivity. **E5+ joins that equivalence only under positive crediting**, as already stated in Proposition 19.8(c). Without positivity, CN implies E5+, but parent-cone conservation alone does not imply CN.

Sources: [frozen RESULT.md, section 19.8 and section 21](https://github.com/proteinfoldingengine/WetLabEngine/blob/0a5802d03e4c91d7b9be23c1405e643695284048/ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_identification_d15_review/RESULT.md); [review run 39184183201](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/39184183201). The inspected review.txt SHA-256 is b93bfcc468502c1ce98308dd5af33e2ce85e7ea9a467bd2f09f05d2f29a91b99. Its actual verdict remains ACCEPTED / NOT_DERIVED; acceptance and byte-readback do not remove this specific qualification.

All frozen proof, review, verification and receipt files are preserved. This note does not publish raw review archives, alter the author's workflow, or claim a native physical milestone.
