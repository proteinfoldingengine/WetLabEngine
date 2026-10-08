# C3 core readout — complete clarification and REVISE reconciliation
Status: clarification submitted for fresh independent review; not closed.
Original proof: f0fb556d39047e58e87e358b2433e58a0a25fb3b; scope d68f460d6b594c83c8d7f5f242c85e4e61847580.
Initial run37857965667: verification PASS; mathematical review REVISE, five requests labelled missing assumptions, zero counterexamples. Exact original response preserved in evidence/core-readout/initial_review.txt and review_revise.zip. This document supplies detailed proof steps; it does not add an observation, fairness assumption or transition.

## A. Disjoint GROUPS, not disjoint roots inside each group
Let U={a,b,c,d,w}, V={e,f,g,h}. U intersect V is empty. S1,S2 are subsets of U; S3,S4 are subsets of V. Their within-group overlaps w and e do not belong to the other group.
For any full hitting set H, H intersect U hits S1,S2 and H intersect V hits S3,S4. Therefore |H| >= |H intersect U|+|H intersect V| >= tau12+tau34. Conversely, minimum pair-hitting sets H12 subset U and H34 subset V have disjoint union which hits all four roots, with size tau12+tau34. Equality follows.
S1 always contains core label b; S2 always contains d; S3 contains e,f; S4 contains g,h. They remain nonempty even in the candidate configurations violating floors. Two nonempty roots have hitting number1 iff their intersection is nonempty, otherwise2. S1 intersect S2 is {w} iff x=y=1 and empty otherwise. S3 intersect S4 is {e} iff bridge switch b=1 and empty otherwise. This proves tau=4-xy-b for all32 configurations. The reviewer's suggestion that internal sharing invalidates this group-additivity argument is mathematically incorrect; the explicit partition resolves the ambiguity.
Since xy,b are nonnegative bits, tau<=4 automatically. Also
3<=4-xy-b iff 3+xy+b<=4 iff xy+b<=1.
With bit b, this is exactly b<=1-xy.

## B. Positive certificate sequence, including rejected attempts
At hidden pair11 and baseline, supports are (abw,cdw,ef,gh), sizes(3,3,2,2), tau3.
Actual -a(root1) gives (bw,cdw,ef,gh), sizes(2,3,2,2), tau3.
Actual -c(root2) then gives (bw,dw,ef,gh), sizes(2,2,2,2), tau3.
Both requests remove a present core label and both successors obey the band/floors. A rejection leaves its source unchanged. If the first rejects and the second commits, only d2=1 is observed and no conjunction-positive certificate is credited. If the first commits and the second rejects, only d1=1 is observed. The positive certificate is issued ONLY when the actual visible state has both d1=d2=1.
For any xy=0 baseline, +e(root4) gives (...,ef,egh), sizes of first roots2+x,2+y, then2,3; tau3. Its visible commitment is the negative certificate. In11 the same candidate successor would have tau2 and MUST reject.

## C. Complete interval invariance, not an unstated absence claim
The closed-world scope permits only six core-toggle commands during probe/restoration episodes, each a one-coordinate actual toggle or identity. Written in (x,y,d1,d2,b), every such map fixes the first TWO coordinates. Invalid requests and rejected valid requests are identity on all five. Induction over every finite prefix therefore fixes x,y for any number and ordering of these operations, including all rejections and restorations.
During anchored service there is exactly one extra pending request +/-w(root2), executed once as an actual y toggle or identity. It fixes x. There are no other maps, external writers, delayed commits or compensating changes in the relation. Hence over the ENTIRE interval from the old sound certificate, through restoration, the pending request, and all fresh probes, y_new equals either y_old or its complement, with complement precisely when that one request toggled. This coordinate statement follows from the declared complete alphabet, not from an empirical promise about unmodelled actors.
Old certificate values are historical after the request; they must not be reused as current-state truth until a fresh certificate exists. An infinite rejection suffix may prevent any fresh certificate, in which case no outcome is reported. The theorem is conditional on completed finite episodes; no limiting inference supplies a missing observation.

## D. Explicit hidden-writer rejecting trace
Take baseline10000 (x1,y0). Commit +e(root4) to10001, certifying y0, then restore -e(root4) to10000. Compare continuations with no controller payload request: A stays10000; B contains an UNREPORTED external +w(root2), reaching11000. Both now show the identical baseline core000; A has y0 and B has y1. The stored y0 certificate is invalid in B. The pair ['10000','11000'] records these final worlds. B is OUTSIDE the declared no-hidden-writer grammar, and demonstrates why extending the theorem to that grammar would fail. It is not claimed to be an allowed counterexample to the scoped theorem.

## E. Precisely limited improvement
The earlier single-root core-history carrier gave a positive hidden-capacity witness and no negative certificate under its own grammar. We do not claim to have obtained a negative certificate in that same carrier.
The shared-witness result used the present four core pairs with spectator-only commands and an explicit observed tau coordinate, giving immediate post-attempt decoding after tau3 synchronization. The current gate instead expands the command alphabet to core probes and removes tau from observations. Protected-band rejection remains in the native transition definition; it is NOT derived by the observer. A committed bridge-core addition supplies a negative conjunction/payload certificate, and floor-supported core deletion supplies a positive one. Readout is delayed and can stall, so this is not an unconditional dominance result over the earlier channel.
The improvement is removal of DIRECT TAU OBSERVATION for the stated conditional readout task, at the stated action/guard cost. Core observation genesis and physical enforcement remain OPEN. If all attempted edits must be uniformly known safe before issue, the new probe is disallowed: baseline00 and11 disagree about the bridge addition. No external legality-query output is introduced to repair that restriction.
