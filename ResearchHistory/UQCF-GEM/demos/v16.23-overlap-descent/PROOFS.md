# v16.23 — Overlapping retained views: proofs before computation

Status: written mathematical arguments, self-reviewed, not machine-formalized. The new computational verification has separate evidence. No geometric target or physical response law is selected. The parent is v16.22 at a02202bc218adb4080489c54dd37a1f9e5ec77d1. Types are fixed in TYPE_LEDGER.md.

## O1 — The existing retained subsets form a lattice

Fix one finite common-Genesis prefix tree X. All carriers here are actual nonempty root-containing prefix-closed subsets of X. For Y,Z let U=Y union Z and J=Y intersection Z. Both are admissible. We do not assert a common carrier for unrelated Genesis objects. For each vertex v, the retained ancestors in Y and Z are two initial segments of its one ancestor chain. Their longest elements are comparable; the shallower is r_J(v), the deeper is r_U(v). Hence r_Y r_Z=r_Z r_Y=r_J, using the literal inclusions into X between the retractions. This is not an invented rerooting or depth-shifting arrow.

On formal signed sources F_X=Q^X define E_Y=I_YX P_XY. Applying these maps to every atom delta_v gives

    E_Y E_Z=E_J,     E_Y+E_Z-E_J=E_U.

The difference on the right is derived in the signed space, not claimed meaningful in every additive monoid. On response classes W_X=Q^X/Q1 use F_Y=H_YX R_XY. Evaluation on the ancestor chain proves the same meet/join identities. These maps are algebraic idempotents, not a physical metric projection.

## O2 — Signed source gluing and its universal property

For x_Y in F_Y, x_Z in F_Z suppose P_YJ x_Y=P_ZJ x_Z=c. Define the source on the UNION, not on all of X, by

    x_U=I_YU x_Y+I_ZU x_Z-I_JU c.                       (G)

Here I is literal atom inclusion/zero extension. The mixed relation P_UY I_ZU=I_JY P_ZJ follows by sending a Z atom to its longest ancestor in Y, which lies in J. Similarly in the other direction. Therefore P_UY x_U=x_Y and P_UZ x_U=x_Z. Conversely, (O1) on U gives (G) for any x_U, proving uniqueness. Thus

    F_U -> F_Y x_(F_J) F_Z

is an isomorphism, with the fiber product defined by the ACTUAL source pushforwards. Equivalently 0 -> F_U -> F_Y direct-sum F_Z -> F_J -> 0 is exact, the last map being (P_YJ,-P_ZJ). Surjectivity follows by inserting any c into Y and taking zero in Z. The same proof applies to balanced source spaces S (total zero), since all P/I preserve total and (G) then has total zero.

For views inside a larger X, the joint-readout kernel is exactly ker P_XU, not necessarily zero. Indeed E_Y x=E_Z x=0 implies E_U x=0 by O1, and the converse follows by retraction composition. Gluing does not reconstruct discarded information outside U.

## O3 — Finite covers, associativity, and information coordinates

There is an invertible source coordinate map already available from the lineage: c_root=sum_X x and c_v=sum_{u descendant of v} x_u for each nonroot v. The inverse is x_v=c_v-sum_{children w}c_w, with the same formula for the root. Subtree sums telescope. Under admissible pruning these coordinates are simply restricted to the retained vertices: every retained subtree collects exactly its former descendant sources. Thus pairwise matching on overlaps means the c coordinates agree wherever views overlap. They glue uniquely on the union for any finite cover. Balanced sources set c_root=0; no physical scalar attainability is inferred.

This gives a general proof of finite-cover descent independent of matrix rank samples. Repeated views and different parenthesizations of the binary operation (G) give the same unique c and hence the same x. For three views the inclusion-exclusion expression is the sum of three included local sources minus the three included pair-overlap sources plus the included triple-overlap source. It equals either binary parenthesization. Refining a cover without changing its union does not change the reconstructed source. All statements commute with consistent root/parent-preserving lineage relabelings. The coordinate choice is a computational representation, not extra information.

## O4 — Response gluing and v16.22's depth freedom

Potential restriction preserves constants. For classes phi_Y in W_Y and phi_Z in W_Z with equal restrictions to W_J, choose their unique root-zero representatives. Because the SAME retained root belongs to J, equality as classes on J is then equality of representatives. Their values glue on U uniquely; changing either original representative by a constant does not change the resulting class. This uses a shared retained identity, not external frame alignment.

Equivalently, in classes,

    phi_U=H_YU phi_Y+H_ZU phi_Z-H_JU phi_J.

To check the formula, at a vertex in Y the Z retraction and the J retraction agree unless that vertex is also in Z, where all compatible values agree; similarly on Z. The response exact sequence is 0 -> W_U -> W_Y direct-sum W_Z -> W_J -> 0. The last map is the difference of restrictions; a class on J can be extended through its ancestral pullback into Y.

Let T be ANY v16.22 comparison-compatible linear family, not only the fixed Green inverse. Naturality makes T_Y x_Y and T_Z x_Z compatible, and T_U applied to (G) has precisely those response restrictions. Uniqueness of response gluing proves

    T_U glue_source(x_Y,x_Z)=glue_response(T_Y x_Y,T_Z x_Z).

The same holds for all finite covers by O3. Therefore imposing these overlap-gluing relations on the already classified comparison family adds NO depth-selection condition: every scalar sequence a_depth remains compatible. This is a logical-consequence theorem, not a claim that no other earned relation can constrain depth. C+INV still fixes all a_depth=1. The bounded verifier tests the FULL certified four-dimensional parent solution basis, not only two hand-picked sequences.

## O5 — Nonnegative sources are a different category

For nonnegative rational source vectors, all pushforwards and zero extensions are available, but subtraction is not an internal operation. Finite additivity alone did not earn arbitrary negative physical amounts. Given compatible nonnegative x_Y,x_Z, there is at most one nonnegative global source because O2 establishes uniqueness in the containing signed space. Its signed candidate (G) is nonnegative outside J automatically. At each v in J its value is

    x_U(v)=x_Y(v)+x_Z(v)-c(v).

Consequently a nonnegative global source exists IFF x_Y(v)+x_Z(v)>=c(v) for EVERY v in J. This is an exact membership criterion for the declared rational cone, not a fitted threshold or a new source law. A failure means these formal nonnegative local data do not jointly realize one nonnegative source on U; it does not mean the local data are invalid individually.

Explicit two-view counterexample: X={root,a,b}, Y={root,a}, Z={root,b}; local vectors (0,1) and (0,1). Both have total 1 and agree after pruning to the shared root. The unique signed gluing is (-1,1,1). No nonnegative gluing exists. Adding a constant to this source is NOT a gauge transformation: it changes its pushforward and total. Potential gauge freedom cannot repair source negativity.

## O6 — Pairwise nonnegative realizability need not be global

Take the four-node rooted star X={root,a,b,c}, and views {root,a}, {root,b}, {root,c}. Each local source is (1,1), total 2. All overlap sources are the root source 2. Every pair has the nonnegative gluing (0,1,1), total 2. But all three have the unique signed gluing (-1,1,1,1), so there is no global nonnegative source. This example satisfies all actual prefix/Genesis conditions and is inside the preregistered size bound.

More generally finite-cover gluing in O3 determines c at each union vertex. Nonnegative membership is exactly c_v>=sum_{children in U}c_child at every vertex (including leaves and root). A family of views can satisfy the inequalities separately, or on each pair, and fail an inequality after the full union is assembled. These are extensive aggregation constraints, not quantum contextuality, a new physical mechanism, or evidence of geometry/gravity.

## O7 — Scope, evidence and correction discipline

O1-O4 close overlapping-view comparison in the SAME finite prefix-tree/formal signed category used in v16.21-v16.22. They do not supply rerooting, identify independent origins, alter the fixed inverse, or remove the known cumulative fine-response obstruction. O5-O6 classify one explicitly declared nonnegative rational subcategory; they do not establish which positive sources nature can prepare. Positivity of potential representatives is not an invariant notion in W and is not imposed on response selection.

Every universal statement above has a constructive argument; finite exact checks audit implementations and reject false certificates. The computational bound is not a physical cutoff. The governing requirements are WORKER_ASSIGNMENT.md in the parent campaign. No original report or executable is rewritten.

The gluing/equalizer terminology is standard mathematics, not a novelty claim. Background definition: Stacks Project, Sheaves, tag 00VL, https://stacks.math.columbia.edu/tag/00VL . We do not assume a spacetime/topological geometry to prove any identity here.

Time is pruning / ordered recoverability update.
