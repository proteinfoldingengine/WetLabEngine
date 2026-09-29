# v16.22 — General arguments before adjudication

Status: written, self-reviewed mathematical arguments; not proof-assistant formalization. Exact finite certificates separately test implementations. Let F=Q, or conditionally R, with the explicit inherited signed-source assumptions in TYPE_LEDGER.md. Work at one fixed Genesis. Nothing below selects a physical response law or claims novelty for standard linear/category theory.

## T1 — The retained coordinates, not an assumed response ansatz

For every nonroot vertex v let its edge be (p(v),v). Define b_X(c)=sum_v c_v(delta_v-delta_p(v)). This maps into S_X. Its inverse is c_v=sum_{u descending from v} x_u: subtree sums telescope so the divergence at a nonroot vertex v is c_v-sum_children c_child=x_v, and the root equation follows from total zero. Hence b_X is an isomorphism without a metric choice.

Define d_X[phi]_v=phi_v-phi_p(v). Constants cancel. If all differences vanish, connectivity makes phi constant; given edge differences, sum them on each root-to-vertex path and set the root value zero. Hence d_X is an isomorphism W_X->F^{E_X}.

For actual retention Y subset X, if v is retained then p(v) is retained and P_XY b_X(e_v)=b_Y(e_v). If v is discarded, r(v)=r(p(v)), so P_XY b_X(e_v)=0. Similarly I_YX maps the retained edge source to the identical edge source in X. Restriction R selects exactly the retained edge differences. Pullback H has those same differences on retained edges and zero difference on discarded edges. Thus the four maps in these explicit coordinates are edge-coordinate deletion and zero insertion. This is derived from the full retained maps; neither map type nor a section is omitted.

## T2 — All comparison-compatible responses are diagonal in those coordinates

Write M_X=d_X T_X b_X. Let J:F^{E_Y}->F^{E_X} be insertion of the retained edges and Q its coordinate deletion. The two inherited diagrams become

    Q M_X = M_Y Q,          M_X J = J M_Y.

They imply that a retained edge and a discarded edge have zero matrix entries between them in BOTH directions. For any two distinct edges e,f of X there is a legal retained prefix subtree containing one but not the other: if one is ancestral to the other, take the path ending at the shallower edge; if incomparable, take the path ending at either edge. The two diagrams then force both M_X[e,f]=0 and M_X[f,e]=0. Therefore M_X is diagonal. No symmetry, positivity, inverse, or local response ansatz was assumed.

For edge e ending at depth k, retain exactly its ancestral path. The diagonal entry is equal to the last-edge entry of that path's matrix. Every rooted path of length k is isomorphic in this fixed-Genesis category. Naturality equates these entries, producing one scalar a_k for each positive integer depth. It does NOT equate different depths: none of the declared isomorphisms or retained inclusions shifts the root or deletes an ancestor of a retained edge.

## T3 — Converse and complete classification

For any scalar sequence (a_1,a_2,...) define

    T_X = d_X^{-1} diag(a_depth(e)) b_X^{-1}.

Every diagram of T2 commutes: retention selects edges of unchanged depth, and insertion adds zero edge coordinates. Every admitted rooted isomorphism preserves depth. Thus these families satisfy C. T2 and this converse give a bijection between C and scalar sequences over F. On the full subcategory of trees of at most N vertices the parameter space is F^{N-1}: a path realizes each depth through N-1 and no deeper edge is present. This is a theorem about equations and their allowed morphisms, not an inference from the finite solver.

Two- and three-stage diagrams follow by composing their actual P/I/R/H maps; all required equations are stable under composition and different parenthesizations. Inserting an intermediate legal pruning merely factors the same coordinate deletion/insertion. Hence these extra composition checks do not equate the depth parameters. This assertion is not made for re-rooting or non-prefix elimination, neither of which is in the admitted inventory.

Important: nonuniqueness of C is not nonexistence of canonical constructions. In particular a_k=1 is a distinguished construction once unweighted incidence is specified. The result only says the comparison equations alone do not require that particular choice.

## T4 — The original Green inverse remains unique

Let l_X be the unweighted Laplacian map W_X->S_X already proved invertible in v16.21 P4. By the definitions of incidence, l_X=b_X d_X: the edge potential differences produce their endpoint divergence. Therefore

    l_X T_X = b_X diag(a_depth(e)) b_X^{-1}.

The equation l_X T_X=id holds on all S_X iff every a_k=1. Since every depth occurs in a rooted path, C+INV has precisely the inherited family T^G_X=l_X^{-1}. We have NOT made its definition nonunique, removed its inverse axiom, or refuted its v16.21 compatibility. We have identified exactly which additional equation removes the comparison-family freedom. If that defining equation is included in the phrase 'full diagnostic', uniqueness holds.

For a source covariance condition alone C, no inference of physical INV is made. Whether a physical source/response interpretation requires or derives INV remains outside this mathematical campaign.

## T5 — Explicit nonproportional candidates and a positive reference check

Take a_k=1 and a_k=k. Both satisfy T3 for all finite trees. These are mathematical witnesses of nonuniqueness of C, not adopted models. Both have a_1=1, so the difference is not merely one overall unit scale. On the path root->v->w, in independent nonroot source coordinates and root-zero potential coordinates,

    T_unit  = [[1,1],[1,2]],
    T_depth = [[1,1],[1,3]],
    L_root_reduced = [[2,-1],[-1,1]].

The first is the inverse of the displayed L. The second is not: L T_depth=[[1,-1],[0,2]]. The balanced source k=(0,-1,1) has nonroot source coordinates (-1,1); the respective root-zero outputs are (0,1) and (0,2). They are different response classes. Both candidates agree on the two-node tree and cannot be global scalar multiples. Their admissibility under all declared maps is the theorem in T3 and is tested independently in the frozen finite universe.

Even requiring candidate invertibility would not restore selection: both sequences have nonzero entries at every depth. No invertibility requirement is inserted into C and no probabilistic or physical realizability follows from this observation.

## T6 — What is verified and what remains open

The primary solver uses arbitrary root-coordinate matrices, derives constraints from the actual diagrams and performs rational elimination. It is not permitted to insert T2's diagonal conclusion into its unknown space. The independent verifier changes to the explicitly proved edge coordinates, enumerates all embeddings independently and solves their equality/zero constraints by equivalence classes. It checks every production constraint and basis, reference inverse, witness, relabeling and composite map. Altered or missing data must fail, even when a producer's headline verdict is unchanged.

The classification is complete in C; reference uniqueness is complete in C+INV. Physical source attainability, an independently derived physical response-selection principle, more general retained morphisms and the quantum leg remain open. No arbitrary labels, metrics, fitted constants, quantum primitives or geometric targets are added. Depth is lineage address length, not time. Time is pruning / ordered recoverability update.

## References

Parent: v16.21 PROOFS.md P0–P7 and TYPE_LEDGER.md L1–L17, commit `6a9fe4450c4a711a4c0d3b2170e7e31eff550ee6`.
Standard natural-transformation definition: Stacks Project, tag 001I, https://stacks.math.columbia.edu/tag/001I . Computational matrix reference: https://docs.sympy.org/latest/modules/matrices/matrices.html . These are background references; the specific proofs above are supplied in full. No global priority claim is made.
