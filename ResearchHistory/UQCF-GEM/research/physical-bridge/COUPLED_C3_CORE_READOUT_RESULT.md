# C3 core-visible two-sided readout — proof candidate
Status: AUTHOR-SIDE PROOF; independent gates pending.
Scope: d68f460d6b594c83c8d7f5f242c85e4e61847580. No assumptions beyond that scope are added.

## 1. Full supports and admissibility
Write the full state as
S1={b} union ({a} if d1=0) union ({w} if x=1),
S2={d} union ({c} if d2=0) union ({w} if y=1),
S3={e,f}, S4={g,h} union ({e} if b=1).
Here the bit b in formulas denotes the root4 bridge switch, whereas the label b in {a,b} is a core label; they are different typed objects. All snapshots report labelled core sets, so switches d1,d2,b are directly read from those sets.

The label universes of (S1,S2) and (S3,S4) are disjoint. A minimum hitting set therefore splits into independent hits for those two groups, and their transversal numbers add: restricting any full hitting set gives the lower bound, and uniting two minimum covers gives the matching upper bound.
S1,S2 are nonempty and share exactly w iff xy=1, hence their hitting number is 2-xy. S3,S4 share exactly e iff b=1, hence their hitting number is 2-b. Thus tau=4-xy-b, including configurations failing floors.
Their sizes are 2-d1+x,2-d2+y,2,2+b. Floors2 hold exactly when d1<=x,d2<=y. The upper band is automatic; the lower bound is equivalent to xy+b<=1. Consequently the complete native state domain is
d1<=x, d2<=y, b<=1-xy.
This classification follows from actual support geometry in the combinatorial sense, not inserted spacetime geometry.

## 2. Two complementary visible certificates
In any admissible state:
- d1=1 implies x=1 by floor1.
- d2=1 implies y=1 by floor2.
- d1=d2=1 therefore implies xy=1.
- b=1 implies xy=0 by the protected lower hitting bound.
The last two records are disjoint: an admissible state cannot contain both certificates.
Only observed core membership is used. The controller never reads tau, x,y, full supports, or an acknowledgement. Knowing the native constraint is not observing its value.

From a baseline state with xy=0, +e(root4) is a valid admissible toggle and its actual commitment yields b=1. From xy=1, -a(root1) followed by -c(root2) are admissible toggles and actual commitments yield d1=d2=1. Thus each hidden pair admits a finite certificate-producing execution. This is existential reachability; it does not assert that attempts succeed. For example, a controller can alternate a bridge-probe phase and a floor-probe phase, restoring all observed core modifications before switching phases; each relevant finite successful branch is possible in the declared relation. No rejection itself is evidence of either bit.

At the baseline the core observation is identical for all four hidden pairs. The infinite all-NOOP execution is allowed from each. Therefore no policy can guarantee a finite two-sided decision for all executions. Stopping with a definite conjunction on a common all-NOOP prefix would be wrong for one of 00 and11.

## 3. Exact core restoration and retained information
Restore by reinserting any missing a,c, then removing e from root4 if present. These toggles reduce d1,d2,b toward0. The inequalities above persist: lowering d1 or d2 preserves its floor inequality, lowering b preserves the band inequality. Membership syntax is determined by the visible core sets. Every restoration toggle is admissible in every hidden state compatible with its current visible configuration.
Each actual restoration is itself core-visible. Rejections can delay restoration without causing a false completion signal. Reaching the exact baseline is recognizable and reachable; it is not guaranteed. Since no probe/restoration edit changes x or y, a sound stored certificate remains true after restoration. This is a retained-history inference, not an additional externally supplied bit.

## 4. Core-certified anchor and delayed payload channel
A visible removal of a establishes x=1, independently of y. Restore a before service. Under exclusive root2 payload editing, x remains1 without further hidden reads. The branch that acquires this anchor is conditional; if initially x=0 and only the core-probe alphabet is used, no such anchor certificate is reachable. The conjunction certificate still has a negative branch there. No hidden-anchor preparation is silently assumed.

On the certified x=1 sector, d2=1 certifies y=1; b=1 certifies y=0. At either baseline payload state the matching certificate path is admissible and reachable: -c for y=1, +e(root4) for y=0. Restore the full core before any payload request.

Given a retained certified y_old at baseline, issue exactly one +/-w(root2) request. With x=1 and baseline core, either payload occupancy preserves floors and tau in{3,4}; a syntactically valid actual toggle changes y once, while a rejection/invalid-membership request leaves it fixed. Hide the outcome as stipulated. Mark the old certificate invalid for current-state use after the attempt. Allow no further payload requests or hidden writers while probing.

If a fresh core certificate subsequently gives y_new, then y_new!=y_old iff that one pending payload request actually toggled w. Equality certifies NOOP under this exact relation. Restore the core again before further payload service. Induction over completed readout/service/restoration episodes gives arbitrary finite repeated use. This is DELAYED certificate-conditioned commit detection; immediate outcome decoding is unavailable from the unchanged core snapshot directly after a hidden payload attempt. Certificate acquisition and restoration may stall indefinitely.

## 5. Rejecting controls and boundary
- Baseline core observations for00 and11 agree although xy differs. Omitting all core changes, or inferring a bit from rejection, fails.
- At baseline +e(root4) is admissible for00 but not11. Therefore it is NOT uniformly safe as a proposed committed edit across the original fiber. The inherited guarded transition relation supplies rejection for inadmissible requests. The same protocol is not valid under a rule forbidding even attempts not known safe.
- Committing +e from11 would make tau=2. If the native band guard is removed or misimplemented, the negative certificate fails.
- Removing a from x=0 violates its original floor. If that guard is removed, the anchor certificate fails.
- After certifying a bit, an unreported spectator toggle can invalidate it while leaving core observations unchanged. Completeness/exclusive writing is load-bearing.
- An all-NOOP run prevents guaranteed decision and completion.
- A full hidden-support read used to implement an observer-side legality oracle would add forbidden information; no such implementation is derived or supplied here.

## 6. What is genuinely new
The earlier core-history theorem supplied only a positive-capacity certificate, and the shared-witness channel assumed observed exact tau. Here two different native constraints produce complementary ACTUAL CORE witnesses: floor-supported deletion certifies presence, and lower-band-supported addition certifies absence. Together they provide a two-sided conjunction readout and, on a core-certified anchor sector, a repeatable delayed payload channel without direct tau observation or a separate commit acknowledgement.

The improvement is conditional on already accessible core snapshots and enforced admissible-or-NOOP native transitions. It is not an unconditional solution of native record genesis, enforcement, physical measurement or progress. Broad C3 remains OPEN. No quantum-carrier alignment, RAS/RCR selection, force, spacetime metric, fundamental time or GR derivation is made.
