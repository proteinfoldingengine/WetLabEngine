# Q164 erratum: equal fibers can preserve the counting reference

Date: 2026-11-11 America/Phoenix. Author: GPT Work.
Corrects C4 and associated universal wording in the [original Q164 result](https://github.com/proteinfoldingengine/WetLabEngine/blob/f3aea1637b3f8f592c91eb6fa30ac969b63037cd/ResearchHistory/UQCF-GEM/research/physical-bridge/T420_EVIDENCE_ARCHIVE_2026-11-11/independent_2026-11-11_1836_q164/RESULT.md), blob `3aca24414f602f0d7aca3c6459318ddcc3a20bc8`.
The raw archive, original local tests and claimed ALL_PASS output remain unchanged. This is an analytical correction, not a newly certified campaign.

## Correct condition and proof

Let r:X->Y be an admitted prefix-tree retraction, n=|X|, m=|Y|, and b_y=|r^{-1}(y)|. P is its extensive-grade pushforward. Coordinatewise,

    [P(1_X/n)]_y = b_y/n.

Consequently,

    P(1_X/n)=1_Y/m  iff  b_y=n/m for every y.

The condition is **equal fiber cardinality**, not singleton fibers. The common size can exceed one.

## Nondegenerate counterexample

Use distinct full addresses:

    o=(), p=(0), u=(1), v=(0,0),
    X=(o,p,u,v), Y=(o,p).

Both carriers are root-containing and prefix closed. The admitted simultaneous deletion of u and v retracts u to o and v to p. Thus

    P = [[1,0,1,0],
         [0,1,0,1]],

and

    P(1/4,1/4,1/4,1/4) = (1/2,1/2).

This is genuine 4->2 pruning with two retained vertices and two fibers of size 2. It refutes the “iff nothing is removed” statement. It is a separate rejecting control for C4's universal claim; it does not change the original balanced-pair preparation or event.

## What remains valid

A single-leaf deletion with m>=2 has one fiber of size 2 and m-1 fibers of size 1, so its counting reference is not P1-covariant. The original 4->3 example and its +1/12 p-to-v reset contribution therefore remain intact.

C3's conditional statement also remains valid: if omega_Y=P omega_X, P6 preserves the retained response class for the transported zero-sum source. The nonconstant reference-reset contribution vanishes in that comparison. C4's overbroad statement was unnecessary for C3.

The accompanying wording “breaks the inherited P1 naturality whenever an event occurs” must be replaced by “the independently reset counting reference is not P1-covariant when the retraction has unequal-cardinality fibers.”

## Reference typing and sign precision

The algebraic prescription omega_Y:=P omega_X is distinct from a physical derivation requiring a selected reference to evolve that way. If the reference is an identified native extensive grade undergoing that P1 event, the transport rule applies within that typing. If it is an independently chosen diagnostic reference at each carrier, its covariance is an additional condition. An assertion that every physical reference must satisfy it needs the corresponding inherited operation/source, not merely the existence of P.

Q164 C2's displayed shift formula has the correct orientation:

    post-reset response minus naturally transported response
      = M G_Y(P1_X/n - 1_Y/m).

In pruning_consistency_audit.py:analyze, blob `94d946dfc5fb5aa150834a807eb35c29b3133604`, the named variable background is the OPPOSITE vector, 1_Y/m - P1_X/n. Thus the displayed response shift is **-M G_Y background**, not +M G_Y background. This corrects the prose identification, while preserving C2's displayed formula and the original +1/12 example.

## Verification and status

The counterexample and corrected equivalence follow directly from the retraction definition and coordinatewise multiplication. No scientific program was executed; the three-tree local check is not being rerun or represented as a universal proof. Future checks of C4 should include this equal-fiber proper-pruning control and preserve their original adverse evidence.

Posted first in [PR111 comment 6811938453](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6811938453). Native owner access remains open; no premise promotion, new physical law, independent acceptance, merge or numbered-stage closure.
