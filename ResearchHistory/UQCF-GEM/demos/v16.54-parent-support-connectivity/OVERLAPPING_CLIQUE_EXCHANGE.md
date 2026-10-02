# Overlapping witnesses: symmetry exchange and an extremal normal form

Status: candidate analytical proof for independent review. Parent analytical head: 834ab7e5e5203f3e46aac6db932d9d9f7e23a54e. No implementation, numerical enumeration or scientific execution. Previous accepted proofs are unchanged.

## 1. Objective and theorem

Continue in the native width-floor root carrier. Primitive moves toggle one root/label incidence, all roots stay nonempty and at their positive floors, and tau is the minimum label hitting-set size. Exact-q endpoints must be connected with tau in {q-1,q}. The earlier conditional lifting then preserves the single global native excursion budget when children supply the accepted interface.

The protected-root theorem cannot apply when the q smallest floors sum to more than k. The disjoint-triangle family showed that this can happen for valid exact-q states. Here we resolve an entire family of such carriers, including all their exact endpoints, using overlapping roots and an extremal classification rather than assuming disjoint witness roots.

**Theorem N (clique-boundary connectivity).** Let s>=3 and m>=1 be integers with q=m(s-1)>=3. Put

    k=ms, r=m*s*(s-1)/2, a_i=2 for every root i.

Every pair of exact-q endpoints on this palette and floor vector is connected by single-incidence moves with tau in {q-1,q}. No protected state with q pairwise-disjoint roots exists anywhere in this carrier, since 2q>k.

The proof has two reusable parts: general symmetry exchanges valid for arbitrary overlapping supports, and an equality-case argument forcing compact endpoints in this family to be unions of complete-graph modules. No branching number is fixed and no finite passing-case count is used. This is not the universal positive-slack theorem.

## 2. Global label exchange is one-unit safe

**Lemma L.** For any exact-q root tuple A and transposition sigma of two palette labels x,y, A and sigma(A) admit a floor-safe path with tau in {q-1,q}.

Proof. Let U_i=A_i union sigma(A_i). Any hitting set H for U can be repaired into a hitting set for A by adding at most one label. If H contains neither x nor y, every incidence it uses is unchanged. If it contains both, it already hits every old root that it hits through x or y in U. If it contains exactly one, add the other. Thus tau(U)>=q-1. The transposition preserves tau and every root size.

Expand A to U one incidence at a time, then contract U to sigma(A). During expansion every tuple contains A, so tau<=q; during contraction every tuple contains sigma(A), again giving tau<=q. Every tuple is contained in U, giving tau>=tau(U)>=q-1. Floors hold on expansion and because the final contraction endpoint meets them. This implements the transposition by native primitive moves, not by treating a relabeling as a primitive. Concatenate transpositions to implement any palette permutation; each completed transposition is exact-q, so excursions do not accumulate.

## 3. Reassigning roots is one-unit safe

**Lemma M.** Swapping two root supports is one-unit safe whenever both swapped supports meet their destination floors. More generally, any permutation of root supports whose final tuple meets all floors can be implemented by such safe swaps.

Proof of a swap. Write the two old supports as X,Y and replace both by X union Y to obtain U, leaving all other roots fixed. A hitting set for U hits at least one of X,Y; adding one label from the other if necessary hits the old tuple. Hence tau(U)>=q-1. Expand the old roots to U, then contract to the swapped tuple, toggling individual incidences. Each half contains its corresponding exact-q endpoint, and each state is contained in U. The same monotonic bounds give tau in {q-1,q}. Floors hold by legality of the endpoints.

For a general permitted permutation, regard equal supports as distinct tokens if necessary. Process destination slots in decreasing floor order. For the current slot j, find its desired token in an unfixed slot i and swap it into j. Its size meets a_j because the final assignment is permitted. The token currently in j has size at least a_j>=a_i and therefore fits i. Previously fixed slots are not moved. Every swap is permitted, and at least one more slot is fixed. This terminates.

Lemmas L and M apply to arbitrary overlapping roots; they do not require a disjoint witness family. They connect feasible symmetry-related exact endpoints. They alone do not connect endpoints with different incidence structure. The next classification supplies that missing fact for Theorem N.

## 4. Compact endpoints become graphs

Take any exact-q endpoint with floors 2. Choose a minimum q-label hitting set H. In each root retain one label of H that hits it and one other label; delete all other incidences one at a time. Each root has at least two labels, so this is possible and respects its floor. Deletions cannot lower tau, and retained H still hits every root, so tau stays exactly q.

The resulting roots are unordered pairs of distinct palette labels. Interpret them as edges of a graph on all k labels. Repeated roots initially give repeated edges; discard multiplicity only for the mathematical graph argument. Let e be the number of distinct edges, so e<=r. Isolated vertices are included. A set of labels hits every root exactly when it is a vertex cover of this graph. Its complementary vertices form an independent set. Therefore the independence number is

    alpha=k-q=m.

No graph simplification is performed as a native move. It is only used to analyze the compact endpoint.

## 5. Equality forces complete-graph modules

Let n=k=ms and let deg(v) be the simple graph degrees. For each ordering of the n vertices, select every vertex that precedes all its neighbors. The selected vertices form an independent set: two adjacent vertices cannot both precede each other. Averaging its size over all finite orderings gives

    alpha >= sum_v 1/(deg(v)+1)
          >= n^2/(2e+n)
          >= n^2/(2r+n)
          = m.

The first average uses only that v is first among itself and its neighbors in the fraction 1/(deg(v)+1) of orderings. The second inequality is Cauchy-Schwarz on the positive numbers deg(v)+1, with equality exactly when all are equal. The third uses e<=r. This is a finite analytical average, not a randomized execution.

Since alpha=m, every inequality is equality. Hence e=r, so no root pair is repeated, and all degrees equal 2r/n=s-1. Moreover every ordering must select exactly alpha vertices: each selects at most alpha and their average equals alpha.

Suppose the graph contained an induced path u-v-w, so u,w are not adjacent. Choose an ordering with u first, v second and w third, and all other vertices later. Then u is selected, v is not selected because u precedes it, and w is not selected because v precedes it. No neighbor of w is selected: v is not selected, u is not its neighbor, and every other neighbor comes after w. Thus w can be added to the selected independent set. That selected set had size at most alpha-1, contradicting the equality for every ordering.

There is therefore no induced three-vertex path. Each connected component is complete: a shortest path between nonadjacent vertices would begin with an induced three-vertex path. Regular degree s-1 then forces each component to contain exactly s vertices. There are exactly m components, each a complete graph on s vertices. Every pair edge occurs exactly once among the ordered roots.

This classification is forced for every compact exact-q endpoint in the specified carrier. It is not an assumption about the input and not just an exhibited family. Conversely a union of m such cliques has minimum vertex cover m(s-1)=q, so exact endpoints exist.

## 6. Connecting all exact endpoints

Choose a canonical partition of the ordered palette into m groups of size s and a canonical ordering of all pair edges within those groups. Every compact endpoint from Section 5 is a palette permutation and a root permutation of this canonical tuple. Lemma L moves its clique components and labels to the canonical partition, and Lemma M arranges its edges in the canonical root slots. All roots have floor 2, so every root permutation is permitted.

Every completed symmetry exchange is exact-q; each intermediate primitive state is in {q-1,q}. Compact the first endpoint, connect its compact form to the canonical tuple, reverse the analogous construction for the second endpoint, and reverse its compaction. Concatenation is finite and preserves the band and all floors. This proves Theorem N for every exact endpoint, including originally noncompact supports.

## 7. What obstruction this removes, and what remains

For these parameters the q smallest floors sum to 2m(s-1)>ms=k. Hence q disjoint nonempty floor-safe root witnesses are impossible everywhere in the carrier. Nevertheless Theorem N proves that all exact-q endpoints are connected by one-unit repair. This explicitly separates the earlier method obstruction from any connectivity obstruction.

The positive slack is

    delta = (r-q+1)k - 2r
          = ms(s-2)[m(s-1)/2 - 1] > 0,

under s>=3 and q>=3. The previously used disjoint-triangle family is s=3, m>=2. The theorem handles it and the higher clique modules uniformly. The roots inside each module overlap; disjointness only separates the modules' palettes.

The structural mechanism here is rigidity at an independence-number bound, followed by safe symmetry exchanges. It does not assume that degree deficit itself provides a buffer. It also does not imply that arbitrary exact-q endpoints share one symmetry type: outside this equality regime, compact endpoints may have different overlap structures and the averaging inequality may be strict.

The remaining universal question is whether such different overlap structures can be connected while preserving all required complementary subset covers. Theorem N does not settle it, supply a disconnected root example, or prove a native barrier. The earlier conditional lifting applies only with its child-interface hypotheses. No implementation correctness, numerical certification, efficiency or physical claim is made.

Independent review must check both symmetry exchanges, floor-safe permutation decomposition, exact compaction, every equality consequence of the independent-set average, the induced-path contradiction, and the distinction between this complete parameter-family theorem and universal positive-slack connectivity.
