# FCV-1 — Proofs for retained closure, descent and comparison

Written before the new adjudication implementation. Review status: self-reviewed mathematical arguments; finite checks and deliberate-defect tests have separate receipts. A future GREEN does not prove these theorems by itself. All references to source and response objects use TYPE_LEDGER.md. This document corrects the broad missing-splitting/transport interpretation, not the historical program outputs.

## P0 — Scalar structure and linearity

For a finite set X and a specified commutative additive monoid M, finite additivity says mu(A)=sum_{x in A} mu({x}); fiber pushforward is meaningful and additive. No subtraction or vector-space kernel follows for a general M.

For F-valued signed measures with F=Q or R, singleton evaluation is a bijection to F^X: define mu_x(A)=sum_{v in A}x_v, and evaluate singleton sets for the inverse. Pointwise addition and scalar multiplication agree under this bijection. Therefore a finite fiber sum, zero extension, function restriction and pullback are F-linear. This is the explicit linear representation used in the inherited rational diagnostic, not a claim that every signed vector is a physically preparable grade. The symbolic proofs below hold over Q/R. Rational bounded tests check implementations; they are not a density argument for real universality.

## P1 — Admissibility, fiber composition and cumulative kernels

Let X superset Y superset Z be nonempty finite prefix-closed sets with one common Genesis/root. Define r_XY(x) as its longest prefix in Y. Every prefix of x in Z is a prefix of r_XY(x), and conversely a Z-prefix of r_XY(x) is a Z-prefix of x. Their longest elements are equal. Thus r_YZ r_XY=r_XZ. This proves composition from addresses, including identities and repeated pruning.

For z in Z the disjoint fiber identity is

    {x:r_XZ(x)=z} = disjoint union_{y:r_YZ(y)=z} {x:r_XY(x)=y}.

Finite additivity gives (P_YZ P_XY x)_z=sum_{r_XZ(v)=z}x_v=P_XZ x. The matrix product is a representation of this argument, not its premise. Summing over all fibers preserves total grade. In particular each K_j=ker P_0j lies in S_X0, and composition implies K_{j-1} subset K_j. No coarse recentering is substituted.

## P2 — Supplied source section and split loss sequence

Define I_YX on atoms by e_y -> e_{i(y)}; in singleton coordinates it is zero extension. Since r_XY i_YX=id_Y, P_XY I_YX=id_{F_Y}; both preserve total sum. These maps commute with every admissible relabeling because atom inclusion and ancestral fibers do. Hence

    F_X = ker P_XY direct-sum I_YX(F_Y),
    S_X = ker P_XY direct-sum I_YX(S_Y),
    x = (x-I_YX P_XY x) + I_YX P_XY x.

The first term is in ker P; the intersection is zero because PI=id. This is a section supplied by retention, not an arbitrary vector-space splitting. It is not claimed unique among all linear sections.

For X0->X_{j-1}->X_j, let P_a=P_0,j-1 and P_b=P_j-1,j. Restriction of P_a gives the exact sequence

    0 -> K_{j-1} -> K_j -> ker P_b -> 0.

Indeed P_b P_a x=0 for x in K_j. Its kernel is K_{j-1}. Given y in ker P_b, I_0,j-1 y belongs to K_j and P_a I_0,j-1 y=y, proving surjectivity and giving the section. All domains refer to actual nested sets, not equal cardinalities.

For cumulative E_j=I_0j P_0j on F_X0 (E_0=id), E_j^2=E_j and, for i<=j, E_i E_j=E_j E_i=E_j. To see this, I_0j factors through I_0i, and restricting ancestral pruning to X_i is its own X_i->X_j retraction. These address identities establish both products. Therefore D_j=E_{j-1}-E_j is idempotent, D_i D_j=0 for i!=j, and

    K_j = direct-sum_{l=1..j} im D_l,
    im D_j = I_0,j-1(ker P_j-1,j),
    sum_{l=a+1..b} D_l = E_a-E_b.

These are algebraically complementary projectors, not an assertion of orthogonality in a physical metric. Inserting an intermediate retained subset refines the decomposition by the last telescoping identity. Different factorizations with the same endpoints have the same total lost part, though their individual layer labels need not agree.

## P3 — Bare-filtration naturality obstruction (NOT a retained no-go)

Category: finite-dimensional F-vector spaces with fixed-length filtrations 0=K_0 subset ... subset K_m, with all filtration-preserving linear maps. The functors gr_j=K_j/K_{j-1} act by induced quotient maps.

Any natural family of linear maps tau:gr_j -> gr_{j+1} is zero. At any object choose vector-space complements solely to exhibit an automorphism a that acts by 2 on gr_j and identity on gr_{j+1}, preserving the whole flag. Naturality requires tau composed with 2id = id composed with tau, so tau=0 (F=Q/R). This addresses every natural transformation in the declared class; it is stronger than observing that the inclusion becomes zero. Trivial grades are covered automatically.

There is likewise no section of every bare extension 0->A->B->B/A->0 natural under all filtered linear maps when A and B/A are both nonzero. In temporary coordinates B=A direct-sum C, each shear a_u(a,c)=(a+u(c),c) is identity on A and B/A. A natural section s would satisfy a_u s=s for every u:C->A, impossible for a class c with u(c)!=0. A complement is used to exhibit symmetries in the proof, not selected as retained data.

P2 does not conflict: the retained category carries actual atoms, inclusions and retractions and excludes those arbitrary shears as structural relabelings. The external associated graded exists in both categories; a natural reconstruction of representatives depends on which data and morphisms are retained.

## P4 — Actual inherited response: quotient and invertibility

For finite connected prefix tree X, form L_X from unweighted parent-child incidence. Its row and column sums are zero. For real a,

    a^t L_X a = sum_{parent-child edges} (a_child-a_parent)^2.

This vanishes exactly for constants by connectivity. Over Q the same follows by embedding in R; the rooted reduced matrix has a nonzero rational determinant. Thus L_X induces an isomorphism l_X:W_X=F_X/F1 -> S_X. Put Z_X=id-11^t/n and U_X=11^t/n. L_X+U_X is invertible, and G_X=(L_X+U_X)^(-1)-U_X satisfies LG=GL=Z, G1=0, and ZG=G. These identities follow by decomposing into constants and S_X; no new inverse or inner-product selection is introduced beyond the inherited unweighted diagnostic.

T_X=q_X G_X|S_X is inverse to l_X. Its zero-mean representative is G_X x; its root-zero representative is G_X x-(G_X x)_root 1. They represent the SAME quotient class, not an identity of sources and potentials. For a root-only carrier S_X=W_X=0 and G_X=0, so the statements remain meaningful.

Every K_j lies in S_X0. Therefore the actual cumulative O_0j=T_X0|K_j is injective, with rank dim K_j. Its restriction to K_{j-1} has rank dim K_{j-1}. This predicts the mathematical restriction law; the independent verifier must still reconstruct and check actual matrices and admissible witnesses.

## P5 — Fixed-target descent, witness, and the distinct response quotient

For any linear T:K_j->W, the rule [x]->Tx with codomain W is representative independent iff T(K_{j-1})=0: necessity compares k and 0; sufficiency compares x+k and x. For the actual T_X0 restriction, P4 proves that this holds iff K_{j-1}=0. Once a previous pruning is nontrivial, fixed-target descent fails; identity stages after an earlier loss do not magically restore it.

An explicit admissible witness uses X0={(),(0),(0,0)}, X1={(),(0)}, X2={()}. In this listed order,

    L0 = [[1,-1,0],[-1,2,-1],[0,-1,1]],
    P01 = [[1,0,0],[0,1,1]],
    k = [0,-1,1],
    G0 k = [-1/3,-1/3,2/3].

P01 k=0, sum k=0, L0(G0 k)=k and sum(G0 k)=0. The output is not constant (last minus root equals 1), hence q0 G0 k !=0. k and 0 are the same class in K2/K1 but have different W0 outputs. k is a difference of two positive unit atoms within one admissible fiber; it is a formal signed source distinction in the inherited linear domain. No new physical source law is inferred.

Alternative, explicitly different codomain: F_j=T_X0(K_j) subset W0 is nested. The map

    bar O_j:K_j/K_{j-1} -> W0/F_{j-1}, [x]->[T_X0 x]

is well defined since representatives differ by a vector whose image is in F_{j-1}. It is injective because T_X0 is injective, and its image is F_j/F_{j-1}. It discards exactly the response subspace of previously lost sources; it does not recover that response unchanged. Quotient projections W0/F_i -> W0/F_j for i<=j compose canonically. P6-P7 are still needed to compare the different native stage carriers W_Xj.

## P6 — Already-earned boundary comparison and derived response lift

For actual retained inclusion define S_XY:F_X->F_Y by potential restriction. It sends constants to constants and induces R_XY:W_X->W_Y. From retraction define h_YX:F_Y->F_X by h psi=psi composed with r_XY; it induces H_YX:W_Y->W_X. These are typed differently from source P and I. In coordinates S=I^t and h=P^t, but their definitions use set maps, not an added physical metric.

On a prefix tree, a retraction fiber has exactly one retained vertex. Every edge crossing fibers is an original edge between retained vertices. Summing L_X phi over a fiber cancels internal edges and leaves precisely L_Y S phi. Hence

    P_XY L_X = L_Y S_XY.

This is the inherited corrected boundary theorem. Also h psi is constant along every internal fiber edge. At a discarded vertex L_X h psi=0, while at a retained vertex its value is L_Y psi. Thus independently

    L_X h_YX = I_YX L_Y.

It follows on the typed zero-sum sources that

    R_XY T_X = T_Y P_XY,
    T_X I_YX = H_YX T_Y,
    R_XY H_YX = id_WY.

On arbitrary raw source arrays the first equation instead has the necessary centering: Z_Y S_XY G_X=G_Y P_XY Z_X. Do not remove Z_X or replace P_XY Z_X by Z_Y P_XY. No arbitrary historical A_r is used: R is actual restriction, H is ancestral pullback, and the intertwining has just been proved from the existing tree.

Both comparisons commute with parent-preserving relabelings. R_YZ R_XY=R_XZ and H_YX H_ZY=H_ZX because the underlying set maps compose. For a general graph or a non-prefix retained subset the crossing-edge proof may fail. No theorem for those classes is asserted.

## P7 — Cumulative/stage obstruction compatibility without redefining either

Let X0->X1->X2, x in K2=ker P02. Then u=P01 x is in ker P12, z=x-I10 u is in K1, and x=z+I10 u. Linearity and P6 give the exact identity in ONE explicit codomain W0:

    O02(x) = O01(z) + H10 O12(u),
    z=x-I10 P01 x, u=P01 x.

Here O02:K2->W0 and O01:K1->W0 are cumulative/fine obstructions, O12:ker P12->W1 is the native stage obstruction, and H10:W1->W0 is the earned comparison. The stage pullback O12 P01 kills K1, but its lift is only the NEW component. It equals O02 only after the old component O01(z) is subtracted. Thus no tautological substitution certifies fixed-target descent.

Define response cumulative projectors E'_j=H_j0 R_0j on W0. P6 implies T0 E_j=E'_j T0 on S0. They are nested commuting idempotents, and D'_j=E'_{j-1}-E'_j gives T0 D_j=D'_j T0. Therefore the source splitting of P2 has a compatible response splitting in this SPECIFIC inherited finite-tree response, not merely from a source section alone.

For three or more stages, expand each source as its D_l components plus E_final and apply T0. Associativity follows from ordinary linear addition, P/I/R/H composition, and the already-proved telescoping projectors. Inserting an intermediate legal pruning replaces E_a-E_c by (E_a-E_b)+(E_b-E_c); applying T0 yields the exact corresponding response refinement. Different factorizations with the same endpoints have identical cumulative lost response, not literally identical individually indexed grades.

The selected representative on a new source grade is E_{j-1}x for x in K_j. It is independent of adding k in K_{j-1}. T0 E_{j-1}x realizes the quotient response in the supplied complement. This is NOT T0 x in general; the difference is the explicitly removed old response T0(Id-E_{j-1})x.

## Corrections and limits

The bare-filtration obstruction in P3 is real, but it does not prove a retained no-go once literal inclusion is restored. The full retained source splitting and the prefix-tree response comparison in P2/P6/P7 are contrary to the earlier broad missing-transport interpretation. The .15F non-descent computation is compatible with these results: fixed-target descent fails because the fixed full-fine response is injective, while canonical layer decomposition and quotient descent are different, available constructions. This is not evidence by itself of a new dynamical memory mechanism.

What is closed here: the algebra of the specified finite prefix-tree pruning, formal signed-source split sequences, and the already-fixed Green-response comparisons. What is not closed: selection of a physical response law, realizability of every formal source vector, arbitrary graph/refinement classes, independent Genesis identification, the quantum leg, or any metric/connection/curvature/gravity claim. Time remains pruning / ordered recoverability update.

## Mathematical context (no novelty claim)

Split exact sequences and quotient factorization are standard algebra: Stacks Project, Definition 12.5.9, https://stacks.math.columbia.edu/tag/010F . Graph boundary elimination is standard; see Dörfler and Bullo, Kron Reduction of Graphs with Applications to Electrical Networks, arXiv:1102.2950, https://arxiv.org/abs/1102.2950 . The direct prefix-tree arguments above are complete and do not assume an external geometric model or borrow a general graph theorem without checking its hypotheses.
