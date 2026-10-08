# C3 four-root coupled endpoint deadlock and one-buffer bypass

Date: 2026-10-07.
Status: ANALYTICAL CANDIDATE; author-side proof only, independent review pending.
Frozen scope COUPLED_C3_DEADLOCK_SCOPE.md at 08eb9dada9c5d4665453768810522303119d2fe6.

## 1. Exact carrier

Palette P={a,b,c,d,e,w}. Four labelled roots, each original floor2.

Source E:
 r1={a,b}, r2={b,c}, r3={a,c}, r4={d,e}.

Exact target C:
 r1={b,d}, r2={b,c}, r3={c,d}, r4={a,e}.

The auxiliary w is absent from source and target.

## 2. Source and target hitting numbers

At source the first three roots form the triangle edges {a,b},{b,c},{a,c}. Any single label misses one triangle edge, while any two of {a,b,c} hit all three. Thus the triangle hitting number is2. The fourth root {d,e} is disjoint from the triangle palette, so every full transversal needs an additional label d or e. Therefore tau(E)=3.

At target the triangle edges are {b,d},{b,c},{c,d}, with hitting number2, and r4={a,e} is disjoint from their palette {b,c,d}. Hence tau(C)=3.

## 3. Exact endpoint-only deadlock

At source each root has size2, exactly its original floor. Every endpoint-only deletion as first primitive would leave a size1 root and violate its floor.

The ONLY endpoint-only additions available at source are:

A. Add d to r1:
 ({a,b,d},{b,c},{a,c},{d,e}).
 The pair {c,d} hits every root, so tau<=2.

B. Add d to r3:
 ({a,b},{b,c},{a,c,d},{d,e}).
 The pair {b,d} hits every root, so tau<=2.

C. Add a to r4:
 ({a,b},{b,c},{a,c},{a,d,e}).
 The pair {a,b} hits every root, so tau<=2.

No single label hits all four roots in any of these three states: the first three roots have empty total intersection, and adding an incidence to only one root does not create a common intersection. Thus each displayed state has exact tau=2.

Consequently there is NO legal endpoint-only first native incidence toggle from E, and hence no protected endpoint-only native path from E to C. This is a native endpoint-event obstruction, not merely a chosen macro policy deadlock.

## 4. One-buffer exact native path

Execute:

0. E=({a,b},{b,c},{a,c},{d,e}).
1. Add w to r4:
   ({a,b},{b,c},{a,c},{d,e,w}).
2. Delete d from r4:
   ({a,b},{b,c},{a,c},{e,w}).
3. Add d to r1:
   ({a,b,d},{b,c},{a,c},{e,w}).
4. Delete a from r1:
   ({b,d},{b,c},{a,c},{e,w}).
5. Add d to r3:
   ({b,d},{b,c},{a,c,d},{e,w}).
6. Delete a from r3:
   ({b,d},{b,c},{c,d},{e,w}).
7. Add a to r4:
   ({b,d},{b,c},{c,d},{a,e,w}).
8. Delete w from r4:
   ({b,d},{b,c},{c,d},{a,e})=C.

## 5. Exact protected-band proof

At every step, the first three roots form a subfamily of hitting number EXACTLY2.

For states0-2: {a,b},{b,c},{a,c} form the original triangle.

For state3: {a,b,d},{b,c},{a,c}. The pair {b,c} hits all three, and their total intersection is empty (first two intersect at b, which the third excludes).

For state4: {b,d},{b,c},{a,c}. The pair {b,c} hits all three; total intersection empty.

For state5: {b,d},{b,c},{a,c,d}. The pair {b,c} hits all three; total intersection empty.

For states6-8: {b,d},{b,c},{c,d} form the target triangle.

At states0-6, the fourth root uses only {d,e}, {d,e,w}, or {e,w}. At states0-2 the triangle labels are {a,b,c}; at states3-6 its labels are subsets of {a,b,c,d}. At states3-6 r4={e,w}, disjoint from every triangle root. At states0-2 r4 is also disjoint from every triangle root.

At states7-8 the triangle labels are {b,c,d}, while r4={a,e,w} or {a,e}, again disjoint.

Therefore throughout the eight primitive steps the fourth root is disjoint from all three triangle roots. Any transversal needs at least two labels for the triangle and one further label for r4. Conversely, two labels hit the triangle and one hits r4. Thus

    tau=3

after every primitive including both endpoints.

Each root has size>=2 at every step. All original floors2 are preserved. w is used only in r4 and removed exactly at the destination.

## 6. Sharp native edit count in the declared palette

Six endpoint-differing incidences must be toggled at least once: +d,-a on r1; +d,-a on r3; +a,-d on r4.

Section3 proves no endpoint-only first event is legal. Therefore every protected path must begin with some off-endpoint toggle. Since the source and exact target have identical values on every off-endpoint incidence, at least one further off-endpoint toggle is needed to restore it. Thus every protected sequential one-incidence path requires at least 6+2=8 toggles.

The displayed eight-edit path attains this bound. It is therefore a shortest protected native path in this exact palette/carrier, not a universal efficiency theorem.

## 7. Mechanism

The original source requires two triangle-cover labels plus one disjoint-edge label. Directly adding d to a triangle root allows d to hit both that root and r4, collapsing tau to2.

The temporary +w on r4 supplies one unit of capacity. Deleting d from r4 then moves r4 to {e,w}, preventing d from simultaneously hitting r4 and a triangle root. Both +d triangle additions become safe, and old a incidences are deleted.

Once the target triangle {b,d},{b,c},{c,d} is established, a is absent from the triangle, so adding a to r4 cannot collapse the hitting number. Removing w restores exact labelled destination.

The auxiliary therefore protects the lower bound by maintaining disjointness between a changing triangle subfamily and the fourth root, while also preserving r4's floor.

## 8. Why this is genuinely coupled

Three triangle roots overlap, all original floors are saturated, and r4 itself changes. r4's d incidence directly controls the legality of +d on TWO other changing roots, and its eventual a incidence is coupled to deletion of a from BOTH. This is neither a three-singleton-anchor construction nor passive padding nor a disjoint singleton permutation.

This is one example of a shared temporary buffer servicing multiple interacting endpoint obligations. It does NOT yet establish a reusable host-selection rule across arbitrary coupled cycles, or a universal one-buffer theorem.

## 9. Falsification and limits

- Every endpoint-only first addition is rejected by an explicit two-cover.
- Every endpoint-only first deletion is rejected by original floor2.
- The auxiliary path is certified at each native primitive, not merely at macro endpoints.
- The result uses one temporary label w on one host root r4 and a fixed known palette. It does not derive a host from compressed retained information over hidden-state fibers.
- No result for general overlapping supports, higher floors, arbitrary directed cycles, arbitrary exact endpoints, or physical forces/geometry/time.

C3's broad retained-controller and renewable handoff theorem remains OPEN. C4-C6 remain OPEN.

## 10. Next mathematical frontier

Derive a retained-information criterion selecting r4-like hosts for a family of overlapping triangle-plus-edge carriers and prove when one temporary label can be renewed across several coupled changes without hidden-state reads. Establish a counterexample where the criterion fails. This is the next C3 theorem-first obligation, not yet solved by the present bounded example.
