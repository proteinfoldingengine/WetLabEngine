# v16.24 — Types and general arguments H0–H6

Written before adjudication code. Self-reviewed mathematical arguments, not machine-formalized. Parent is v16.23 at `3dda0f9f0aa6882a9acacc39fd709f779460cfb2`. All references below are relative to `ResearchHistory/UQCF-GEM/` at that exact commit. No general novelty claim is made for the set-cover or linear-separation mathematics.

## Provenance/type ledger

| ID | Definition and type | Assumptions/provenance | Status |
|---|---|---|---|
| C1 | X finite rooted tree encoded by distinct full lineage words; i:Y->X literal inclusion; r_XY longest retained ancestor | Actual common Genesis and root-containing prefix subsets; v16.23 TYPE_LEDGER.md and PROOFS.md O1 | Inherited admitted category |
| C2 | V=(Y_i) finite nonempty indexed family; U=union Y_i; all intersections retain root | C1; v16.23 O1–O3 | Derived cover/union; no extra morphism |
| C3 | F_Y=Q^Y, F_Y^+=Q_{≥0}^Y; P_YJ sums singleton amounts over r_YJ fibers | v16.21 TYPE_LEDGER L6–L7; v16.23 O5 | Conditional formal signed/nonnegative source spaces, not physical attainability |
| C4 | Compatible family x_i in F_Yi^+ with P_Yi,J x_i=P_Yj,J x_j | J=Yi intersection Yj; v16.23 O2–O3 | Exact equality condition |
| C5 | c_v=sum of source in the local subtree of v in any view containing v; c_root common total | v16.23 O3 ensures independence and unique signed union completion | Derived coordinates, not a physical scalar law |
| C6 | For nonempty subfamily S, U_S=union_{i in S}Y_i and x_S(v)=c_v-sum_{w child of v in U_S}c_w | v16.23 O3,O6; x_S is actual P_U,U_S x_U | Derived signed reconstruction; subtraction is not an internal positive-cone operation |
| C7 | Ch_U(v) set of immediate children; A_i(v)=Ch_U(v) intersection Y_i; tau_v=min |S| with union A_i(v)=Ch_U(v), tau_v=0 for leaves | C1–C2; finite cover guarantees existence for nonleaves | Derived finite covering number; no units/coupling |
| C8 | h(V)=max(1,max_v tau_v) | C7; positive order counts nonempty view tests | Candidate exact consistency order proved H2–H3 |
| C9 | A:Q^U->direct sum_i Q^Yi stacks actual P_U,Yi; lambda in the algebraic dual of that direct sum | v16.23 O2 injectivity; finite pairing sum lambda_i y_i | Derived certificate type, not a source or potential identification |

## H0 — Meaning of the claim

For fixed V, h is the LEAST POSITIVE integer such that for EVERY compatible nonnegative rational family, realizability of every nonempty subfamily with at most h views implies realization on U. This is a worst-case property of the view family, not the order of failure of every particular data set. Some data pass globally; some fail sooner. We keep input compatibility separate from nonnegative feasibility. Rational proofs extend to R under the same finite ordered-scalar assumptions, not by density of tests.

## H1 — Complete inequalities, not empirical thresholds

By v16.23 O3, matching local data determine unique c on U and hence x_U(v)=c_v-sum_{Ch_U(v)}c_w. A nonnegative realization exists iff all these node amounts are nonnegative. Every c_v is nonnegative because it is a subtree sum of some nonnegative local source. For a subfamily S the same inverse formula on U_S gives its unique signed source. It is also the actual fiber pushforward of x_U because subtree sums restrict under ancestral pruning. Thus feasibility on S is exactly the inequalities with Ch_U(v) replaced by Ch_U(v) intersection U_S.

## H2 — Sufficiency of the child-cover number

At each nonleaf v select any subfamily S_v of size tau_v covering Ch_U(v). Those views necessarily contain v by prefix closure. If every subfamily of size at most h(V) is nonnegatively realizable, the amount at v in x_{S_v} is c_v-sum_{Ch_U(v)}c_w and is nonnegative. Leaves have c_v>=0 by singleton validity. Therefore EVERY full-union node inequality holds. This proves sufficiency for arbitrary finite V, no bound on tree size or branching. The selected minimum cover is only a proof/certificate witness; it need not be canonical or unique.

## H3 — Sharpness for each fixed cover

Suppose h(V)=t>1. Choose v with tau_v=t and write d=|Ch_U(v)|. Define c=d-1 on v and its ancestors, c=1 on each immediate child of v, and c=0 at all other vertices. Since t<=d and t>1, d>=2. For any subfamily of fewer than t views, at least one child of v is absent. At v its reconstructed amount is d-1 minus at most d-1, hence nonnegative. At ancestors of v there is at most one nonzero child contribution d-1; if the path stops earlier the ancestor keeps that amount. At the chosen children the amount is 1; descendants and unrelated branches have amount 0. Thus every such subfamily is nonnegative. In particular all original singleton views are valid and compatible, since they are restrictions of one c.

On the full union the amount at v is (d-1)-d=-1. Any minimum child-covering subfamily of size t already gives that same negative amount. All smaller subfamilies are feasible, so the worst-case order cannot be less than t. Together with H2, h(V) is exact. When h=1, H2 and the convention of positive orders establish the minimal value; no nonexistent order-zero experiment is claimed.

## H4 — Branching bound, binary sufficiency and unbounded hierarchy

Let b be the maximum number of children of a union vertex. Choosing one view for each child gives tau_v<=|Ch_U(v)|, so h(V)<=max(1,b). Thus on a binary prefix tree, compatible nonnegative local data with every pair nonnegatively realizable have a global nonnegative realization. Pairwise compatibility alone is still insufficient: pair FEASIBILITY is the additional premise.

This bound is sharp. On a star with m>=2 leaves, choose the m one-leaf views. Then tau_root=m. Give each leaf amount 1 and total m-1; each local vector is (m-2,1). Every proper subfamily of size r<m has root amount m-1-r>=0, while the full union has root -1. For any fixed k, m=k+1 refutes a universal k-view sufficiency claim on trees of unbounded branching. These are mathematical extensive-source witnesses, not higher-order quantum effects.

The exact h may be strictly BELOW b: if one view already contains all children of a vertex, tau_v=1. More generally a few views can cover many children. Number of views, tree depth and branching alone do not replace the declared cover incidence in the exact criterion.

## H5 — Independent separating certificate

Stack the actual fiber maps in A. For any full node v, choose one view containing v. The sum of its source coordinates over descendants of v equals c_v. For each immediate child w choose a view containing w, whose subtree sum equals c_w. Assign +1 coefficients to the former local positions and -1 to the latter, adding coefficients where positions repeat. This constructs a rational/integer lambda with lambda^t A=e_v^t. For the H3 witness, lambda^t local=x_U(v)=-1. A nonnegative global source x would give lambda^t A x=x_v>=0, contradiction. The verifier need only reconstruct A, verify the dual equation and evaluate the negative pairing. Positive rescaling of lambda is harmless and must be accepted. No optimization oracle, floating threshold or physical metric enters this proof.

## H6 — Equivalence, redundancy, refinement and scope

A parent-preserving relabeling maps child sets, view incidence, fibers and all source amounts bijectively; it preserves tau, h, feasibility, and the dual contradiction. Reordering views/vertex storage merely permutes the corresponding coordinates. Repeating a view adds no new covered child set and leaves h unchanged. Adding a subview of an existing view is likewise redundant for minimum child coverage; its source is already a pushforward of the larger view. Replacing views by smaller legal views with the same union cannot decrease h, because every child covering by k new views is dominated by at most k old views. Global feasibility for a fixed c is nevertheless unchanged: union inequalities are the same. The amount of information that must be jointly checked may change without changing that global source criterion.

All H1–H6 statements concern the existing source cone, actual retained maps and compatible local data. No restriction is placed on the v16.22 depth parameters: no response operator occurs in these extra conditions. The fixed inverse and v16.23 signed/response gluing are unchanged. Formal cone feasibility remains distinct from physical source attainability, response-law selection and the operational quantum leg. Time is pruning / ordered recoverability update.

Background only: Stacks Project sheaf equalizer definition (tag 00VM), https://stacks.math.columbia.edu/tag/00VM . The preceding direct arguments do not import a spacetime topology. H5 is a directly verified finite linear-separation certificate, not a novelty claim for linear alternatives.
