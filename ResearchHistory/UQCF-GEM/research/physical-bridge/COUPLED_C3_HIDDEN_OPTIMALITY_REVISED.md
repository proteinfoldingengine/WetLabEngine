# C3 hidden-spectator optimality discontinuity and minimal retained bit

Date: 2026-10-07.
Status: CORRECTED ANALYTICAL CANDIDATE; FRESH INDEPENDENT RE-REVIEW REQUIRED.
Frozen scope COUPLED_C3_HIDDEN_OPTIMALITY_SCOPE.md at c2383f36b4c099f8bb27582639b55c2cb59c94a2.

Revision provenance: initial proof f1531c690ba36662c5a016cd7f2a0cd6ab084275 received independent REVISE for an overstrong first-edit claim. This revised document retains the mathematical family and paths, and clarifies the native event universe and optimality distinction.

**Primitive universe:** one native edit toggles any single root-label incidence from the declared palette, subject to original floors and 3<=tau<=4. In particular +w(r1), +w(r2), +w(r3), and +w(r4) are candidate legal moves; w is NOT restricted to r4.

## 1. Family and retained projection

Core labels {a,b,c,d,e}, fresh auxiliary w, and hidden spectator palette T disjoint from all core labels and w. Let Z be any subset of T.

Original floors all2.

E(Z)=({a,b},{b,c},{a,c},{d,e} union Z).
C(Z)=({b,d},{b,c},{c,d},{a,e} union Z).

Z is a fixed unchanged spectator set, and each exact target preserves its particular hidden Z.

Retained record R consists of labelled core projections of both endpoints, floors2, the availability of fresh w, and the band 3<=tau<=4. R does NOT retain the full root sizes, |Z|, or a flag for Z nonempty.

Consequently R(E(empty),C(empty))=R(E(Z),C(Z)) for every Z, including nonempty ones. This equality is by the declared projection, not by an observer theorem.

## 2. Endpoint hitting numbers

The first three source roots form triangle {a,b},{b,c},{a,c}, with hitting number2. The fourth root {d,e} union Z is disjoint from every triangle label. Therefore tau(E(Z))=3 for all Z.

The first three target roots form triangle {b,d},{b,c},{c,d}, again with hitting number2. The fourth target root {a,e} union Z is disjoint from every target triangle label. Therefore tau(C(Z))=3 for all Z.

## 3. A uniform eight-edit protected route

For every Z, execute
  +w(r4), -d(r4), +d(r1), -a(r1),
  +d(r3), -a(r3), +a(r4), -w(r4).

At every primitive, r4 contains the original e and every spectator z in Z, and the r4 core support follows exactly the independently closed empty-Z eight-edit path.

Throughout the path r4 is disjoint from the union of the first three roots: before d leaves r4 the triangle is still {a,b},{b,c},{a,c}; while triangle acquires d and loses a, r4 has {e,w} union Z; and after the triangle is {b,d},{b,c},{c,d}, r4 may acquire a.

The first three roots have hitting number2 at every step by the already published explicit triangle checks. The fourth root requires one additional label and is nonempty, so tau=3 throughout.

All floors2 hold: r4 never has fewer than the two incidences {e,w} when d has been removed, and other roots use add-before-delete. Z remains unchanged. The exact C(Z) is reached, with w removed.

Thus R alone suffices for a FIBER-UNIFORM LEGAL eight-edit controller over this entire hidden-Z family, but optimality remains to be checked.

## 4. Empty-Z lower bound

For Z=empty, the independently closed bounded C3 theorem proves that no endpoint-only first primitive is legal, and the minimum protected native path has eight edits. The eight-edit route of Section3 attains this minimum.

In particular the first primitive of every eight-edit optimal path is +w(r4), as proved in the independently accepted unique-host theorem.

## 5. Nonempty-Z six-edit route

Suppose Z is nonempty. Execute ONLY the six endpoint-differing toggles:

0. ({a,b},{b,c},{a,c},{d,e} union Z).
1. -d(r4):
   ({a,b},{b,c},{a,c},{e} union Z).
2. +d(r1):
   ({a,b,d},{b,c},{a,c},{e} union Z).
3. -a(r1):
   ({b,d},{b,c},{a,c},{e} union Z).
4. +d(r3):
   ({b,d},{b,c},{a,c,d},{e} union Z).
5. -a(r3):
   ({b,d},{b,c},{c,d},{e} union Z).
6. +a(r4):
   ({b,d},{b,c},{c,d},{a,e} union Z)=C(Z).

At step1, r4 has |{e} union Z|=1+|Z|>=2, so deletion of d respects its original floor2.

At steps1-5, r4 contains only e and Z, disjoint from all first-three-root labels. At step0 r4 contains d but the triangle contains only a,b,c. At step6 the target triangle contains b,c,d and r4 contains a,e,Z, still disjoint.

At every step the first three roots have hitting number2:
- source triangle at steps0-1;
- intermediate triples {a,b,d},{b,c},{a,c} at step2;
  {b,d},{b,c},{a,c} at step3;
  {b,d},{b,c},{a,c,d} at step4;
- target triangle at steps5-6.
In each intermediate triple, {b,c} is a two-cover and no single label hits all three.

Therefore the disjoint fourth root forces one additional hitting label and tau=3 at all seven states. Floors2 hold in every root. Z remains untouched.

The six endpoint-differing incidences are mandatory in every exact native repair, so no path can have fewer than six toggles. The displayed path is therefore SHORTEST for every nonempty Z.

## 6. No R-only deterministic controller can be both fiber-uniform legal and optimal

The retained record R is identical for empty and nonempty Z, so a deterministic R-only controller must select the same first native event for both.

For Z=empty, the independently closed unique-host theorem shows every SHORTEST eight-edit protected path begins +w(r4). Other first edits, including +w(r1), +w(r2) and +w(r3), may be legal but cannot initiate an eight-edit optimal completion.

For Z nonempty, every optimal path has exactly six toggles and therefore can contain NO off-endpoint toggle; in particular it cannot begin +w(r4).

These optimal first-event requirements are incompatible. More directly, for nonempty Z, any shortest six-edit path contains only the six endpoint-differing toggles; of those only -d(r4) is initially legal. For empty Z, -d(r4) violates floor2. Therefore no common first native edit can begin a shortest protected repair in both fibers, even though several other edits are legal in the empty fiber. Thus no deterministic controller using only R can be simultaneously legal and SHORTEST for both hidden fibers.

This does NOT show R is insufficient for safe repair: Section3 supplies one R-only eight-edit legal controller for all Z. It shows R is insufficient for UNIFORM OPTIMALITY over this declared family.

## 7. One-bit refinement is necessary and sufficient within this family

Add the retained Boolean bit
    b = 1[Z nonempty].

If b=0, run the eight-edit +w buffer path.
If b=1, run the six-edit endpoint-only path.

Both routes are fully determined by the core address, floors and b; neither requires reading spectator identities or their number. Both preserve hidden Z exactly and achieve their respective shortest lengths.

Because R alone cannot support uniform optimality but R plus this single bit can, the bit separates the two necessary optimal-policy classes. This is an information lower bound of ONE BINARY DISTINCTION in this specific family, not a general Shannon entropy law or universal observer-access theorem.

## 8. Scientific boundary and next frontier

The original unique-host theorem is not contradicted: it assumed Z=empty and a fixed full palette. The new family changes the admissible hidden full states while preserving the same core projection.

The result identifies the exact role of otherwise unobserved spectator capacity: it can eliminate the need for a temporary buffer by making -d(r4) floor-legal.

The next retained-information question is whether this capacity bit can be derived from existing native retained invariants (such as original root size or permitted observable responses) rather than supplied as an extra primitive. The theorem does not establish that derivation.

No general coupled-cycle host-selection theorem, hidden-state reconstruction, force, geometry, continuum, or fundamental time follows.
