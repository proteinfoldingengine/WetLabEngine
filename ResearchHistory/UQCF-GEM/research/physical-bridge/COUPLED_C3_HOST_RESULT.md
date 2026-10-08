# C3 optimal auxiliary host is uniquely selected in the four-root carrier

Date: 2026-10-07.
Status: ANALYTICAL CANDIDATE / AUTHOR-SIDE PROOF. Independent review pending.
Frozen scope: COUPLED_C3_HOST_SCOPE.md at 22d0f1cfa93406379e9e0950d12548c422495f28.

## 1. Carrier and length budget

Source E=({a,b},{b,c},{a,c},{d,e}).
Target C=({b,d},{b,c},{c,d},{a,e}).
All floors2, palette P={a,b,c,d,e,w}. w absent from endpoints. Each primitive toggles one root-label incidence, maintaining 3<=tau<=4.

There are exactly six endpoint-differing incidences:
 r1: +d,-a;
 r3: +d,-a;
 r4: +a,-d.

Any eight-edit exact path must toggle these six once each. The remaining two toggles must add then delete exactly one off-endpoint incidence. No other toggle can occur within eight edits. The previously closed eight-edit path proves this bound is attainable.

## 2. All first endpoint-only events are forbidden

Every root starts at floor2, so any first deletion is illegal.

The three endpoint additions +d(r1), +d(r3), +a(r4) yield two-covers {c,d}, {b,d}, {a,b}, respectively. Thus every protected eight-edit path must start with an off-endpoint addition.

## 3. Classification of off-endpoint first additions

All labels are a,b,c,d,e,w. An off-endpoint addition must add a label absent from its chosen root.

For r1={a,b}, off-endpoint candidates are c,e,w (d is its endpoint addition):
- +c(r1): triangle roots all contain c; {c,d} hits all four roots.
- +e(r1): {c,e} hits all four roots.
- +w(r1): no two-cover is created; w is fresh, and the original triangle still requires two hits plus r4's disjoint {d,e}, so tau=3.

For r2={b,c}, all additions are off-endpoint (r2 is unchanged):
- +a(r2): {a,d} hits all four roots.
- +d(r2): {a,d} hits all four roots.
- +e(r2): {a,e} hits all four roots.
- +w(r2): legal, tau=3.

For r3={a,c}, off-endpoint candidates are b,e,w (d is endpoint addition):
- +b(r3): {b,d} hits all four roots.
- +e(r3): {b,e} hits all four roots.
- +w(r3): legal, tau=3.

For r4={d,e}, off-endpoint candidates are b,c,w (a is endpoint addition):
- +b(r4): {a,b} hits all four roots.
- +c(r4): {a,c} hits all four roots.
- +w(r4): legal, tau=3.

Thus every legal first primitive in any eight-edit path is +w on exactly one of r1,r2,r3,r4.

## 4. Exclude r2 as an eight-edit host

After +w(r2), no endpoint-differing deletion is floor-legal: r1,r3,r4 still have size2. r2 has no endpoint differences, and deleting b or c would toggle an off-endpoint incidence, requiring a later restoration in addition to the already required -w. That exceeds the two-extra-toggle budget.

Every endpoint addition remains forbidden by the same two-covers as at source: those covers never used r2's absence of w, and adding w to r2 cannot destroy a preexisting two-cover.

Therefore no eight-edit path begins +w(r2).

## 5. Exclude r1 as an eight-edit host

After +w(r1), the only floor-legal endpoint deletion is -a(r1), and all endpoint additions are still forbidden by their source two-covers. Hence the second primitive must be -a(r1) for an eight-edit path.

Now the state is
 ({b,w},{b,c},{a,c},{d,e}).

Every remaining endpoint addition is forbidden:
- +d(r1) creates two-cover {c,d};
- +d(r3) creates two-cover {b,d};
- +a(r4) creates two-cover {a,b}.

Every other endpoint deletion is still floor-forbidden. The path is stuck within its eight-edit budget. Therefore r1 cannot host the single temporary w in an eight-edit repair.

## 6. Exclude r3 as an eight-edit host

After +w(r3), the only floor-legal endpoint deletion is -a(r3), and every endpoint addition remains forbidden by its source two-cover. Thus an eight-edit path must next delete a from r3.

Now the state is
 ({a,b},{b,c},{c,w},{d,e}).

Every remaining endpoint addition is forbidden:
- +d(r1) creates two-cover {c,d};
- +d(r3) creates two-cover {b,d};
- +a(r4) creates two-cover {a,c}.

All other endpoint deletions are floor-forbidden. Therefore r3 cannot host w in an eight-edit repair.

## 7. r4 is the unique optimal host

After +w(r4), endpoint additions remain forbidden until -d(r4). This deletion is floor-legal, leaving r4={e,w}. The previously independently accepted eight-edit sequence then completes:

 +w(r4), -d(r4), +d(r1), -a(r1), +d(r3), -a(r3), +a(r4), -w(r4).

Every intermediate state has tau=3, every floor2 is preserved, and the exact target is reached.

Therefore:

**Theorem H.** In this carrier, every shortest protected native repair (eight edits) must use r4 as the host of the unique temporary auxiliary incidence w, and its first two events are +w(r4), -d(r4).

This is an optimal-host necessity theorem in a single declared carrier, not a universal host-selection theorem. Longer paths using other temporary supports or additional off-endpoint edits are not excluded.

## 8. Retained-information selection rule and limits

A controller given the declared labelled endpoint supports, original floors, palette and the exact protected-band definition can determine the unique optimal host by the above finite symbolic certificate:
- reject first endpoint additions via explicit two-covers;
- reject first deletions via floor2;
- test each fresh-w host using forced second-step legality and explicit two-cover witnesses;
- select r4 as the only surviving host.

No hidden full-state read is needed in THIS fully specified carrier because the endpoint supports are explicitly retained. This is not evidence of compressed observer access or fiber-uniform host selection across distinct hidden full states.

Next frontier: characterize an actual family of overlapping carriers with a retained host-selection certificate and renewable handoff across multiple coupled obligations. Test rejecting families and distinguish optimal host from any legal host.

No numerical campaign, physical dynamics, geometry, energy, or fundamental time is inferred.
