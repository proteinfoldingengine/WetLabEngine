# C2 — genuine four-root coupled endpoint dependency

Date: 2026-10-07.
Status: CORRECTED ANALYTICAL CANDIDATE / FRESH INDEPENDENT RE-REVIEW REQUIRED.
Frozen scope: COUPLED_C2_SCOPE.md at c00318259d31c92e2dd0bd7a3ce97755bf74ea02.

Correction provenance: the initial proof at 5d4e7548c03c7c13b04f25f5a39cb723a684ceb6 received independent REVISE; exact issue and verdict are preserved in COUPLED_C2_INDEPENDENT_REVIEW.md at 7da41a7d6792ef445862c07dfce01704c294c143. This revised document corrects only the K={a,c} witness explanation; source, target, all native edits and tau calculations are unchanged.

## 1. Carrier

Palette P={a,b,c,d,w}, with w unused. Floors all1.

Source E:
    r1={a}, r2={b}, r3={c}, r4={a,d}.

Exact target C:
    r1={b}, r2={a}, r3={c}, r4={b,c}.

Endpoint macros:
    M1: +b(r1), -a(r1).
    M2: +a(r2), -b(r2).
    M4: +b(r4), +c(r4), -a(r4), -d(r4).

At source, r1,r2,r3 force a,b,c respectively. The set {a,b,c} also hits r4, so tau(E)=3.

At target, r1,r2,r3 force b,a,c respectively. The same set {a,b,c} hits r4, so tau(C)=3.

Both endpoints have genuine overlap. Crucially, r4 is an active endpoint obligation, not a fixed padding root.

## 2. A complete protected endpoint-only schedule

Execute M1, then M2, then M4. The full sequence of root states and exact hitting numbers is:

0. ({a},{b},{c},{a,d}): tau=3.
1. +b(r1): ({a,b},{b},{c},{a,d}): tau=3.
2. -a(r1): ({b},{b},{c},{a,d}): tau=3.
3. +a(r2): ({b},{a,b},{c},{a,d}): tau=3.
4. -b(r2): ({b},{a},{c},{a,d}): tau=3.
5. +b(r4): ({b},{a},{c},{a,b,d}): tau=3.
6. +c(r4): ({b},{a},{c},{a,b,c,d}): tau=3.
7. -a(r4): ({b},{a},{c},{b,c,d}): tau=3.
8. -d(r4): ({b},{a},{c},{b,c}): tau=3.

Proof for states 4-8: the three singleton roots force distinct a,b,c, which also hit r4 at every step. Thus tau=3.

Proof for states 1-3: r3={c} forces c. No other single label hits all of r1,r2,r4:
- state1: r2={b} forces b, while r4={a,d} misses b, so a third label a or d is required;
- state2: r1=r2={b} force b, r4={a,d} is disjoint from b,c, so a third label is required;
- state3: r1={b} forces b, r4={a,d} is disjoint from b,c, so a third label is required.
The set {a,b,c} hits every root in each state, establishing tau=3 exactly.

Every root remains nonempty, so all original floors1 hold. The last state equals the exact labelled target and w was never used.

## 3. M2 cannot be first

The first primitive of M2 at source is +a(r2), giving
    ({a},{a,b},{c},{a,d}).

Now {a,c} hits every root:
- r1 through a;
- r2 through a;
- r3 through c;
- r4 through a.

Thus tau<=2 and the protected lower bound fails. M2 cannot begin at source under this endpoint macro.

## 4. M4 can finish at source, but changes the legality of the swap

Execute M4 alone at source. Throughout its four edits, r1={a},r2={b},r3={c} remain distinct singleton roots and r4 always contains at least one of a,b,c. Thus tau=3 after every primitive.

The resulting state is
    ({a},{b},{c},{b,c}).

Now try to start M1:
    +b(r1) gives ({a,b},{b},{c},{b,c}).
The pair {b,c} hits all four roots, so tau<=2. M1 is blocked.

Try to start M2:
    +a(r2) gives ({a},{a,b},{c},{b,c}).
The pair {a,c} hits all four roots, so tau<=2. M2 is blocked.

Therefore completing M4 first destroys the protected eligibility of BOTH remaining singleton exchange macros, even though M4 itself was safe and both full endpoints are protected.

This is a genuine coupled dependency: the active fourth root changes the global pair-witness protection needed by other endpoint obligations.

## 5. What the retained certificate reveals

For K={b,c}, the source r4={a,d} misses K and protects the lower bound when M1 adds b to r1. After M4 completes, r4={b,c} no longer misses K, and the same addition creates the two-cover {b,c}.

For K={a,c}, source r2={b} is an actual missed-root witness BEFORE M2's first addition. Adding a to r2 DESTROYS that witness, leaving every root hit by {a,c} and causing tau=2. After M1 completes, r1={b} instead misses K, so M2's +a no longer destroys the final witness and remains protected. Completing M4 first does not restore an alternative K-witness: r4={b,c} intersects K through c.

The retained pair-witness identities, not merely root counts, therefore explain the order sensitivity.

## 6. Exact scope and what remains unproved

This proves existence of a four-root carrier with genuinely interacting endpoint obligations, a complete endpoint-only protected repair, and a concrete order-dependent failure.

It does NOT prove:
- that the order M1,M2,M4 is unique;
- that every legal schedule must complete M4 last (partial M4 events may interleave);
- a cyclic endpoint-only deadlock;
- necessity or sufficiency of a temporary auxiliary w for general coupled carriers;
- an optimal edit count (8 is the exhibited length);
- an autonomous compressed retained controller for arbitrary endpoints;
- a physical force or geometry.

C2 is therefore a bounded positive dependency example, not completion of C3-C6. The next step must find a coupled carrier where an auxiliary is actually necessary or derive a no-go for the proposed minimal class.
