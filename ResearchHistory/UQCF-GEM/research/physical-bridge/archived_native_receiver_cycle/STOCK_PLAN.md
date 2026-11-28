# Why the four fixed archived M9 plans cannot deliver a remote leaf distinction

**Claim.** Consider two admitted preparations of one of the four archived v16.54 M9 plans. Fix its dimensions, target and guard order, and keep one receiver's starting row identical. Its complete ordered sequence of leaf values, after omitting repeated copies, agrees across the preparations. Other rows may differ in arbitrarily many starting incidences. This permits different parent paths, delays and transient parent acquisitions. The new eight-label, six-row experiment changes the original dimensions and is a positive example in the same producer.

## The three smaller plans

Write h for the row floor, q for the ceiling on the hitting number, k for the palette size and r for the number of rows. For a peak above q, each of the binomial(k,q) possible q-element covers must miss some row. At most binomial(k−h,q) of these covers miss any given row. Multiplying by r gives upper bounds of 6 out of 10, 12 out of 15 and 32 out of 35 in the three smaller plans. Therefore clipping cannot run on any preparation with those floors. Each local replacement has the fixed target for that row and a fixed order. All rows reach the same intermediate tuple before reordering. This proves the claim for those plans.

## The largest plan

The palette has eight labels and there are twenty rows of size at least three. A hitting number above five would require each of the 56 three-element complements of five-label sets to contain a row. That requires 56 distinct triples. Hence five is the largest possible peak.

At such a peak, some five-label cover contains both 0 and 1. Otherwise each of the twenty triples on labels 2 through 7 would have to contain an entire row. These would exhaust all twenty rows, and the family of all triples on six labels has hitting number four. The lexicographically least minimum cover therefore begins with 0 and 1. Every peak replacement adds 0 to rows containing 1. The resulting four remaining cover labels, including 0, hit all rows. During the subsequent bridge between replaced vertices, the historical routine makes all additions before any removals. Every intermediate state contains its starting or ending state row by row. A second clipping layer is unnecessary.

In the archived intermediate tuple, the last ten rows are the ten triples on labels 3 through 7. The first ten rows are full rows or {0,1,2}. Consider one receiver before and during its single scheduled replacement. Its preliminary path consists of additions followed by sorted removals. Between these moves, allow the shadow to turn on and off arbitrarily, including while other rows move.

- A target that contains 0 acquires it by the end of the addition phase and keeps it. Before then, an inserted 0 can only appear at a receiver missing 0, where its leaves do not yet hold 0. No other label is withdrawn in the addition phase. During the deletion phase the projected parent is exactly the planned parent.
- A high-triple target contains neither 0 nor 1. If the receiver holds 1, the only ordinary deletion that can precede its deletion is that of 0. All planned additions finish before either deletion. A shadow may delay a scheduled removal of 0 until 1 disappears. If they disappear on the same bridge, historical ascending removal clears 0 first. The holdings available for that clearance are the same as in the preliminary route. Any later temporary re-addition of 0 before 1 disappears leaves it unoccupied. If 0 was absent initially, temporary copies likewise disappear before 1 can be cleared. Receivers that lack 1 throughout this replacement never acquire a shadow.

Before the scheduled replacement, a receiver may idle while 0 is added and removed. An initially absent 0 cannot enter an occupied leaf during such idling. After the replacement the local target contains 0 or lacks 1, so shadowing has no further local effect. The full state now reaches a common tuple. Every row used during its subsequent reorder contains a member of the family of target rows. The cover {0,3,4,5} meets every member, and the entire reorder is below or at the ceiling.

**Finite verification.** For each of the 219 starting supports of size at least three, the checker tries all twelve distinct row targets extracted from the hash-pinned original record. At every preliminary row it permits both the original support and its clipped support. It allows any number of switches between them during idle steps and replays each join in its prescribed order. All 2,628 local cases yield a single history of leaf values, equal to the unclipped history. Allowing independent shadow choices at every frame includes every schedule that the full hitting-number test could produce. It is a verification of local behavior, separate from the historical verifier runs on the positive experiments.

This extends the bots' fixed-plan analysis. Their archive census excluded one-bit activation on the original starting rows, and their largest-plan example reached a remote parent without a leaf consuming the edit. The argument here covers all admissible alternative starting rows at those four fixed targets. [Archive census](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7231352634) · [Largest-plan example](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7231850783)

Run the checker from the repository root.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/stock_shadow.py
```
