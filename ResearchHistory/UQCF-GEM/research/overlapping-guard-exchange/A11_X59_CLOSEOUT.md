# A11.X59 closeout - prescribed anchor mixing with moving upper protection

Date: 2026-10-05 UTC.
Status: accepted analytical checkpoint, subject to separate publication-integrity review and final immutable readback.
Parent: d955a6e884cba250eb0f2c8bcdaa393460fb7a4d.
Scope: 8b55b187d3738b886f8450b40d246788109a7813.
Exact mathematical candidate: 75c411628357330520d7f769c32a2c3fa27e4bff.
Candidate tree: 2f6bf1bf8d893ec5281e076c19a59f512e38d437.
Proof blob: da839ade5f44613f78a397277c25569d99dd2102.
Whole review: INDEPENDENT_A11_X59_WHOLE_REVIEW.md.

## Exact new statements

On X58's actual colored carrier satisfying vc(Gamma_J)>|J| for every nonempty anchor subset J, prescribed pi may now mix anchor and outside roles.

1. EVERY pi has an explicit complete LOWER-protected path to the exact labelled destination, renewing all-color seeds/reserves and attaining the outer endpoint incidence Hamming minimum.
2. For t>=2, an inactive column supplies the upper cover on the SAME path, so EVERY pi has direct minimum repair in {3,4}.
3. For t=1 with no exceptional pair S satisfying S union pi(S)=A, an interleaved all-add/all-delete bridge gives direct minimum repair with a moving upper cover.
4. For t=1 with exceptions, set B=A intersect pi(A) intersect pi^{-1}(A), U={Q:Q avoids pi^{-1}(A)}, V={Q:Q avoids pi(A)}. If B meets every exceptional S and actual U intersect V is empty, seeds chosen in B followed by all U copies and then remaining copies DERIVE a direct minimum repair on one joint lower/upper schedule.

All statements permit arbitrary positive original labelled multiplicities, fixed unequal padding and original positive individual floors up to endpoint sizes, including unequal saturation. The single-column no-padding floor3 case requires no inactive upper-cover labels.

## Assumption removed and mechanism

Anchor preservation pi(A)=A is removed for complete lower renewal and all multi-column direct-minimum repair. For the stated single-column sufficient classes, upper protection genuinely changes from the source anchor-label cover to the labels indexed by pi^{-1}(A).

The exceptional-pair characterization survives arbitrary pi. Their family need not be closed under complement, so ALL-color reserves remain untouched while selected seeds are built. Each old complementary-color witness persists until an actual new seed in S completes. Shared roots protect several obligations without allocating separate capacities.

Common-hit seed colors B meet both endpoint cover identities at both root endpoints. They are outside both actual upper exception families. Processing all U copies before V therefore gives a moving-cover relay on the SAME lower-safe path. Covers hit active endpoints and old/new copies simultaneously, through each add-before-delete primitive.

## Continuation, reuse, restoration and minimum

Actual finite seed/copy/incidence lists supply the next absent addition or present deletion. Endpoint containment preserves every original floor. Completed columns restore role sizes, exact four and the seed/reserve/upper certificate for the next column. Finite unresolved-column count terminates at every original labelled destination support.

Every outer endpoint-differing incidence toggles once; every common incidence and padding incidence remains fixed. Exact global primitive minimum is
L=t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|.
Repeated separate legs are minimum per leg only, not necessarily between their outermost endpoints.

## Discriminating controls

For pi=(0 1 2 3 4 5), B={1,2} meets the sole exceptional pair {0,2}; seed2 and the derived relay work on EVERY valid colored carrier.

For pi=(0 1)(2 3 4 5), B={0,1} meets the two exceptional pairs {0,2},{1,2}. Their family is not complement-closed. The two seeds and all-color reserves transfer both while the physical upper cover changes. This also works on EVERY valid colored carrier.

On the private eight-type carrier, one copy/type gives exact counts20t and18t respectively. Shared five-edge graph carriers and arbitrary unequal copy multiplicities are covered by the theorem. These mixed singleton no-padding endpoints have distinct unique four-covers, so two physical cover identities are necessary and suffice. Their endpoint-union transversal is exactly two; no unchanged background root supplies the lower guard.

The transposition pi=(0 4) calibration has no exceptional pair and admits the interleaved union bridge. Actual U/V overlap rejects X51's STRICT block-stable/boundary-separated relay certificate, not all whole-root paths. The reviewer supplied a valid carrier with a single common U/V type that can be processed first by switching cover inside that root at its union. This countercontrol is included in the corrected proof.

## Review history and remaining obligation

Initial candidate4bfd65d40bcf85e532e41685bb7c92036e73bbe1 had private-count arithmetic corrected before review at c798aa722d3934ceb72402d6ff0d727a8c69ddbc. Independent whole review then required narrowing the method-obstruction claim. Exact accepted source 75c411628357330520d7f769c32a2c3fa27e4bff includes the narrowed statement and countercontrol. Positive construction hypotheses did not change. Earlier sources remain preserved as historical commits, not accepted candidates.

General direct-minimum SINGLE-column repair with nonempty exceptions outside the derived B/U/V criterion remains open. Complete lower repair in that case is proved; accepted maximum-layer A applies only AFTER the complete original-ended lower path. It establishes a band path without a proved minimum/schedule guarantee.

Next: derive another moving-cover/interleaving mechanism when B misses an exceptional obligation or actual U/V overlap, or characterize a precise limitation of the chosen method. A failed certificate is not native disconnection. No arbitrary accessibility, unrestricted mixed/directed/higher-target/nested universality or physical claim follows.

This is analytical only. No scientific execution, numerical campaign, workflow, integration merge, new numbered certificate or efficiency benchmark. Completed v16.54/v16.55, frozen inherited sources and original evidence remain unchanged. Separate efficiency runner/fixtures/benchmarks remain unstarted.
